"""Bind agent qualification to discovered objects and reconstruction inputs."""

from __future__ import annotations

import hashlib
import os
import stat
from pathlib import Path

from _cleanup_common import HELPER_VERSION, CleanupError, canonical_digest, contract_digest


def seal(document):
    document["digest"] = canonical_digest({k: v for k, v in document.items() if k != "digest"})
    return document


def validate_document(document, kind):
    if not isinstance(document, dict) or document.get("type") != kind:
        raise CleanupError("invalid_document", f"Expected a {kind} document")
    if document.get("schema_version") != 1 or document.get("helper_version") != HELPER_VERSION:
        raise CleanupError("unsupported_contract", "Inspect again with this helper")
    digest = canonical_digest({k: v for k, v in document.items() if k != "digest"})
    if document.get("digest") != digest:
        raise CleanupError("document_changed", "Document digest does not match its contents")
    if document.get("contract_digest") != contract_digest():
        raise CleanupError("stale_contract", "Helper changed; inspect and plan again")


def evidence(path):
    source = Path(path).absolute()
    info = source.lstat()
    if not stat.S_ISREG(info.st_mode) or info.st_size > 4 * 1024 * 1024:
        raise CleanupError(
            "invalid_evidence", "Evidence must be a small regular file", path=str(source)
        )
    # Bind both the resolved ancestor chain and the file read, without executing it.
    resolved = source.resolve(strict=True)
    fd = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        with os.fdopen(fd, "rb", closefd=False) as stream:
            data = stream.read(4 * 1024 * 1024 + 1)
        after = os.fstat(fd)
    finally:
        os.close(fd)

    def signature(s):
        return s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns

    if signature(info) != signature(before) or signature(before) != signature(after):
        raise CleanupError(
            "evidence_changed", "Evidence changed during inspection", path=str(source)
        )
    return {
        "path": str(source),
        "resolved": str(resolved),
        "signature": list(signature(after)),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def _qualification(group, candidate):
    allowed = {"ids", "reason", "reconstruction", "evidence_paths", "consumer_roots"}
    if set(group) - allowed:
        raise CleanupError(
            "selection_fields", "Unknown qualification fields", fields=sorted(set(group) - allowed)
        )
    for key in ("reason", "reconstruction"):
        if not isinstance(group.get(key), str) or not group[key].strip():
            raise CleanupError("qualification_missing", f"Supply {key} for the selected objects")
    paths = group.get("evidence_paths", [])
    consumers = group.get("consumer_roots", [])
    if not isinstance(paths, list) or not all(isinstance(x, str) for x in paths):
        raise CleanupError("selection_fields", "evidence_paths must be a list of paths")
    if not isinstance(consumers, list) or not all(isinstance(x, str) for x in consumers):
        raise CleanupError("selection_fields", "consumer_roots must be a list of paths")
    if candidate["kind"] == "filesystem" and (not paths or not consumers):
        raise CleanupError(
            "qualification_missing",
            "Filesystem removal needs evidence_paths and bounded consumer_roots",
        )
    if candidate.get("owner") in {"npm", "uv", "pnpm"} and not consumers:
        raise CleanupError(
            "qualification_missing",
            "Package-cache cleanup needs bounded consumer_roots; an idle store is not proof of no installed consumer",
        )
    normalized = []
    for path in consumers:
        root = Path(path).absolute()
        if not (root.is_dir() or root.is_file()) or root.is_symlink():
            raise CleanupError(
                "consumer_scope_invalid",
                "Consumer scope must be an existing real directory or metadata file",
                path=str(root),
            )
        normalized.append(str(root.resolve()))
    all_paths = list(dict.fromkeys(candidate.get("evidence_paths", []) + paths))
    return {
        "reason": group["reason"],
        "reconstruction": group["reconstruction"],
        "evidence": [evidence(path) for path in all_paths],
        "consumer_roots": normalized,
    }


def make_plan(scan, selection, kind="cleanup"):
    validate_document(scan, "scan")
    if (
        not isinstance(selection, dict)
        or set(selection) != {"schema_version", "groups"}
        or selection["schema_version"] != 1
    ):
        raise CleanupError(
            "selection_schema",
            "Use schema_version:1 and groups:[{ids,reason,reconstruction,evidence_paths,consumer_roots}]",
        )
    if kind not in {"cleanup", "reclaim"}:
        raise CleanupError("invalid_kind", "Choose cleanup or reclaim")
    available = {c["id"]: c for c in scan["candidates"]}
    selected, seen = [], set()
    groups = selection["groups"]
    if not isinstance(groups, list) or not groups:
        raise CleanupError("empty_selection", "Select at least one qualified candidate")
    for group in groups:
        if (
            not isinstance(group, dict)
            or not isinstance(group.get("ids"), list)
            or not group["ids"]
        ):
            raise CleanupError("selection_schema", "Each group needs a nonempty ids list")
        for identifier in group["ids"]:
            if not isinstance(identifier, str) or identifier not in available or identifier in seen:
                raise CleanupError(
                    "candidate_selection",
                    "Unknown or duplicate candidate ID",
                    candidate_id=identifier,
                )
            seen.add(identifier)
            candidate = available[identifier]
            for previous in candidate.get("evidence_preimages", []):
                try:
                    current = evidence(previous["path"])
                except (OSError, CleanupError) as exc:
                    raise CleanupError(
                        "scan_evidence_changed",
                        "Reconstruction inputs changed; inspect again",
                        path=previous["path"],
                    ) from exc
                if current != previous:
                    raise CleanupError(
                        "scan_evidence_changed",
                        "Reconstruction inputs changed; inspect again",
                        path=previous["path"],
                    )
            if (
                candidate.get("retained_reason")
                or candidate.get("snapshot", {}).get("complete") is False
            ):
                raise CleanupError(
                    "candidate_not_qualified",
                    "Candidate has unresolved mechanical exclusions",
                    candidate_id=identifier,
                    reason=candidate.get("retained_reason"),
                )
            expected = "reclaim" if candidate.get("operation") == "reclaim" else "cleanup"
            if expected != kind:
                raise CleanupError(
                    "operation_mismatch",
                    "Cleanup and reclaim require separate plans",
                    candidate_id=identifier,
                )
            selected.append({**candidate, "qualification": _qualification(group, candidate)})
    return seal(
        {
            "schema_version": 1,
            "helper_version": HELPER_VERSION,
            "type": "plan",
            "kind": kind,
            "contract_digest": contract_digest(),
            "scan_digest": scan["digest"],
            "protected_roots": sorted(set(scan.get("roots", []) + scan.get("project_roots", []))),
            "candidates": selected,
        }
    )


def qualification_unchanged(candidate):
    for previous in candidate["qualification"]["evidence"]:
        try:
            current = evidence(previous["path"])
        except (OSError, CleanupError) as exc:
            return {
                "state": "conflict",
                "issues": [{"code": "evidence_changed", "message": str(exc)}],
            }
        if current != previous:
            return {
                "state": "conflict",
                "issues": [{"code": "evidence_changed", "message": previous["path"]}],
            }
    return None


def summary(candidate, detail=False):
    result = {
        k: v
        for k, v in candidate.items()
        if k
        not in {
            "snapshot",
            "payload_files",
            "qualification",
            "evidence_preimages",
            "distributions",
            "scopes",
        }
    }
    result["scope_count"] = len(candidate.get("scopes", []))
    if candidate.get("category") != "venv_payload":
        result["scopes"] = candidate.get("scopes", [])
    snap = candidate.get("snapshot", {})
    if snap:
        result["measurement"] = {
            k: snap.get(k) for k in ("logical_bytes", "allocated_bytes", "complete")
        }
    if detail:
        result["snapshot_identity"] = {
            k: snap[k]
            for k in ("path", "device", "inode", "digest", "complete", "issues")
            if k in snap
        }
        result["distributions"] = [
            {k: d.get(k) for k in ("name", "version", "metadata_path")}
            for d in candidate.get("distributions", [])
        ]
        result["payload_file_count"] = len(candidate.get("payload_files", []))
        result["selection_template"] = {
            "schema_version": 1,
            "groups": [
                {
                    "ids": [candidate["id"]],
                    "reason": "",
                    "reconstruction": "",
                    "evidence_paths": candidate.get("evidence_paths", []),
                    "consumer_roots": [],
                }
            ],
        }
    return result
