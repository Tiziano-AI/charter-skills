"""Passive distribution inventory; never import or run the inspected environment."""

from __future__ import annotations

import csv
import io
import json
import os
import re
import stat
import sys
import tomllib
from pathlib import Path

from _cleanup_common import CleanupError, canonical_digest
from _cleanup_fs import FilesystemError, snapshot
from _cleanup_plan import evidence

MAX_METADATA_BYTES = 4 * 1024 * 1024
MAX_ENV_ENTRIES = 200_000
BOOTSTRAP = {"pip", "setuptools", "wheel"}


def issue(code: str, path: Path | str, detail: str, *, blocking: bool = True) -> dict:
    return {"code": code, "path": str(path), "detail": detail, "blocking": blocking}


def evidence_preimages(paths: list[str], issues: list[dict]) -> list[dict]:
    result = []
    for path in sorted(set(paths)):
        try:
            result.append(evidence(path))
        except (OSError, ValueError, CleanupError) as exc:
            issues.append(issue("discovery_evidence_unreadable", path, str(exc)))
    return result


def evidence_unchanged(preimages: list[dict], issues: list[dict]) -> None:
    for previous in preimages:
        try:
            if evidence(previous["path"]) != previous:
                issues.append(
                    issue(
                        "discovery_evidence_changed",
                        previous["path"],
                        "evidence changed after it was inventoried",
                    )
                )
        except (OSError, ValueError, CleanupError) as exc:
            issues.append(issue("discovery_evidence_changed", previous["path"], str(exc)))


def open_directory(path: Path) -> int:
    """Hold every ancestor while opening the next one without following links."""
    if not path.is_absolute():
        raise ValueError("an absolute path is required")
    fd = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in path.parts[1:]:
            if part in {".", ".."}:
                raise ValueError("relative traversal is not allowed")
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
        return fd
    except BaseException:
        os.close(fd)
        raise


def read_metadata(path: Path) -> str:
    """Read only a bounded regular metadata file through no-follow descriptors."""
    parent = open_directory(path.parent)
    try:
        fd = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
        try:
            before = os.fstat(fd)
            if not stat.S_ISREG(before.st_mode) or before.st_size > MAX_METADATA_BYTES:
                raise ValueError("metadata is not a bounded regular file")
            chunks = []
            remaining = MAX_METADATA_BYTES + 1
            while remaining:
                chunk = os.read(fd, min(remaining, 65536))
                if not chunk:
                    break
                chunks.append(chunk)
                remaining -= len(chunk)
            after = os.fstat(fd)
            if (before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
                after.st_size,
                after.st_mtime_ns,
                after.st_ctime_ns,
            ) or remaining == 0:
                raise ValueError("metadata changed while being read or exceeds the limit")
            return b"".join(chunks).decode("utf-8")
        finally:
            os.close(fd)
    finally:
        os.close(parent)


def _name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _environment_files(root: Path) -> tuple[dict[str, os.stat_result], list[dict]]:
    files: dict[str, os.stat_result] = {}
    issues: list[dict] = []
    budget = [MAX_ENV_ENTRIES]

    def walk(fd: int, relative: Path, device: int, depth: int) -> None:
        if depth > 40:
            issues.append(issue("environment_depth_limit", root / relative, "not inspected"))
            return
        try:
            with os.scandir(fd) as entries:
                for entry in entries:
                    budget[0] -= 1
                    if budget[0] < 0:
                        issues.append(
                            issue("environment_entry_limit", root, "inventory incomplete")
                        )
                        return
                    rel = relative / entry.name
                    if entry.name == ".git":
                        issues.append(
                            issue(
                                "environment_repository_metadata",
                                root / rel,
                                "retained repository metadata is not traversed",
                            )
                        )
                        continue
                    info = entry.stat(follow_symlinks=False)
                    if info.st_dev != device:
                        issues.append(
                            issue("environment_mount_boundary", root / rel, "not traversed")
                        )
                    elif stat.S_ISDIR(info.st_mode):
                        child = os.open(
                            entry.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
                        )
                        try:
                            if os.fstat(child).st_ino != info.st_ino:
                                raise ValueError("directory changed while opening")
                            walk(child, rel, device, depth + 1)
                        finally:
                            os.close(child)
                    else:
                        files[rel.as_posix()] = info
        except (OSError, ValueError) as exc:
            issues.append(issue("environment_unreadable", root / relative, str(exc)))

    try:
        fd = open_directory(root)
        try:
            walk(fd, Path(), os.fstat(fd).st_dev, 0)
        finally:
            os.close(fd)
    except (OSError, ValueError) as exc:
        issues.append(issue("environment_unreadable", root, str(exc)))
    return files, issues


def _record_target(root: Path, site: Path, raw: str) -> str:
    if not raw or "\\" in raw or "\x00" in raw or Path(raw).is_absolute():
        raise ValueError("RECORD path is empty, absolute or ambiguous")
    target = Path(os.path.normpath(site / raw))
    try:
        relative = target.relative_to(root)
    except ValueError as exc:
        raise ValueError("RECORD path escapes environment") from exc
    if not relative.parts or any(part in {".git", ".lock"} for part in relative.parts):
        raise ValueError("RECORD points into retained material")
    if relative.as_posix() == "pyvenv.cfg" or (
        relative.parts[0] in {"bin", "Scripts"}
        and (
            relative.name.startswith(("python", "activate", "Activate", "pip"))
            or relative.name in {"wheel", "easy_install"}
        )
    ):
        raise ValueError("RECORD points into the retained interpreter or bootstrap")
    return relative.as_posix()


def _lock_versions(owner: Path, issues: list[dict]) -> tuple[dict[str, set[str]], list[str]]:
    versions: dict[str, set[str]] = {}
    evidence = []
    for name in ("uv.lock", "poetry.lock"):
        path = owner / name
        if not os.path.lexists(path):
            continue
        evidence.append(str(path))
        try:
            parsed = tomllib.loads(read_metadata(path))
            for package in parsed.get("package", []):
                if isinstance(package, dict) and package.get("name") and package.get("version"):
                    versions.setdefault(_name(package["name"]), set()).add(str(package["version"]))
        except (OSError, ValueError, TypeError) as exc:
            issues.append(issue("python_lock_unreadable", path, str(exc)))
    return versions, evidence


def _distribution(root: Path, metadata: str, files: dict, issues: list[dict]) -> dict | None:
    dist = Path(metadata).parent
    site = root / dist.parent
    try:
        fields = {}
        for line in read_metadata(root / metadata).splitlines():
            if ": " in line and not line.startswith((" ", "\t")):
                key, value = line.split(": ", 1)
                if key in {"Name", "Version"}:
                    fields[key] = value
        if not fields.get("Name") or not fields.get("Version"):
            raise ValueError("METADATA lacks Name or Version")
        bootstrap = _name(fields["Name"]) in BOOTSTRAP
        record = dist / "RECORD"
        if record.as_posix() not in files:
            raise ValueError("distribution RECORD is missing")
        selected = []
        for row in csv.reader(io.StringIO(read_metadata(root / record))):
            if len(row) != 3:
                raise ValueError("malformed RECORD row")
            # Bootstrap ownership is retained, including its entry points.
            if bootstrap:
                target = Path(os.path.normpath(site / row[0]))
                relative = target.relative_to(root).as_posix()
            else:
                relative = _record_target(root, site, row[0])
            if relative not in files:
                raise ValueError(f"recorded file is missing: {relative}")
            if not stat.S_ISREG(files[relative].st_mode):
                raise ValueError(f"recorded payload is not a regular file: {relative}")
            selected.append(relative)
        metadata_files = {name for name in files if name.startswith(dist.as_posix() + "/")}
        if not metadata_files.issubset(selected):
            raise ValueError("distribution metadata contains unrecorded files")
        direct = dist / "direct_url.json"
        direct_url = None
        if direct.as_posix() in files:
            direct_url = json.loads(read_metadata(root / direct))
            if not isinstance(direct_url, dict):
                raise ValueError("direct_url.json must be an object")
            directory_info = direct_url.get("dir_info", {})
            if not isinstance(directory_info, dict):
                raise ValueError("direct_url.json dir_info must be an object")
            if directory_info.get("editable"):
                issues.append(
                    issue(
                        "editable_distribution",
                        root / direct,
                        "source-linked consumer requires retention assessment",
                        blocking=False,
                    )
                )
            # Never copy source URLs: they can contain credentials or signed queries.
            direct_url = {
                "editable": bool(directory_info.get("editable")),
                "source_kind": "local"
                if str(direct_url.get("url", "")).startswith("file:")
                else "remote",
            }
        return {
            "name": fields["Name"],
            "version": fields["Version"],
            "metadata_path": str(root / metadata),
            "record_path": str(root / record),
            "files": sorted(set(selected)),
            "bootstrap": bootstrap,
            "direct_url": direct_url,
        }
    except (OSError, ValueError, TypeError, KeyError, csv.Error) as exc:
        issues.append(issue("distribution_record_invalid", root / dist, str(exc)))
        return None


def _check_locked_versions(distributions, owner, issues, root):
    versions, lock_evidence = _lock_versions(owner, issues)
    for distribution in distributions:
        name = _name(distribution["name"])
        if distribution["bootstrap"]:
            continue
        if not versions:
            issues.append(
                issue(
                    "installed_state_uncompared",
                    root,
                    "no readable supported version lock; compare installed inventory to reconstruction inputs",
                    blocking=False,
                )
            )
            break
        if name not in versions or distribution["version"] not in versions[name]:
            issues.append(
                issue(
                    "installed_version_drift",
                    distribution["metadata_path"],
                    "installed distribution is absent from the lock or has a different version",
                )
            )
    return lock_evidence


def inventory_environment(root: Path, owner: Path) -> dict:
    """Inventory exact distribution files while preserving the environment skeleton."""
    files, issues = _environment_files(root)
    site_files = {name for name in files if "site-packages" in Path(name).parts}
    distributions = []
    metadata = sorted(
        name
        for name in site_files
        if Path(name).name == "METADATA" and Path(name).parent.name.endswith(".dist-info")
    )
    input_paths = [str(root / "pyvenv.cfg")]
    input_paths += [
        str(owner / name) for name in ("uv.lock", "poetry.lock") if os.path.lexists(owner / name)
    ]
    input_paths += [
        str(root / name)
        for name in site_files
        if Path(name).name in {"METADATA", "RECORD", "direct_url.json"}
        and Path(name).parent.name.endswith(".dist-info")
    ]
    preimages = evidence_preimages(input_paths, issues)
    for path in metadata:
        distribution = _distribution(root, path, files, issues)
        if distribution:
            distributions.append(distribution)
    dist_dirs = {
        Path(name).parts[
            : next(i for i, part in enumerate(Path(name).parts) if part.endswith(".dist-info")) + 1
        ]
        for name in site_files
        if any(part.endswith(".dist-info") for part in Path(name).parts)
    }
    if len(dist_dirs) != len(metadata):
        issues.append(issue("distribution_metadata_missing", root, "dist-info without METADATA"))
    claimed: dict[str, str] = {}
    protected = {name for name in files if "site-packages" not in Path(name).parts}
    selected: set[str] = set()
    for distribution in distributions:
        for name in distribution["files"]:
            if name in claimed and claimed[name] != distribution["name"]:
                issues.append(
                    issue(
                        "distribution_shared_file",
                        root / name,
                        "file is claimed by multiple distributions",
                    )
                )
            claimed[name] = distribution["name"]
            if distribution["bootstrap"]:
                protected.add(name)
            else:
                selected.add(name)
                protected.discard(name)
    for name in sorted(site_files - claimed.keys()):
        path = Path(name)
        # uv/virtualenv startup metadata belongs to the retained skeleton.
        if path.name in {"_virtualenv.py", "_virtualenv.pth"} or path.name == ".lock":
            protected.add(name)
            continue
        # Bytecode generated after installation belongs with its recorded source.
        source = (
            (path.parent.parent / (path.name.split(".", 1)[0] + ".py"))
            if path.parent.name == "__pycache__" and path.suffix == ".pyc"
            else None
        )
        if source and source.name == "_virtualenv.py" and source.as_posix() in files:
            protected.add(name)
        elif source and source.as_posix() in claimed and stat.S_ISREG(files[name].st_mode):
            if source.as_posix() in selected:
                selected.add(name)
            else:
                protected.add(name)
        else:
            issues.append(
                issue(
                    "unowned_environment_payload",
                    root / name,
                    "not attributable to a distribution RECORD",
                )
            )
    lock_evidence = _check_locked_versions(distributions, owner, issues, root)
    for executable in {
        Path(os.path.abspath(sys.executable)),
        Path(os.path.realpath(sys.executable)),
    }:
        if executable == root or root in executable.parents:
            issues.append(
                issue("helper_environment", root, "the helper runtime is inside this environment")
            )
            break
    payload = []
    for relative in sorted(selected):
        try:
            observed = snapshot(str(root / relative))
            payload.append(
                {"relative_path": relative, "path": str(root / relative), "snapshot": observed}
            )
            if not observed.get("complete"):
                issues.append(
                    issue("payload_snapshot_incomplete", root / relative, "snapshot incomplete")
                )
            original = files[relative]
            entries = observed.get("entries", [])
            entry = entries[0].get("signature", {}) if entries else {}
            expected = {
                "device": original.st_dev,
                "inode": original.st_ino,
                "size": original.st_size,
                "mtime_ns": original.st_mtime_ns,
                "ctime_ns": original.st_ctime_ns,
            }
            if any(entry.get(key) != value for key, value in expected.items()):
                issues.append(
                    issue(
                        "environment_changed",
                        root / relative,
                        "file identity or metadata changed during inventory",
                    )
                )
        except (OSError, ValueError, FilesystemError) as exc:
            issues.append(issue("payload_snapshot_failed", root / relative, str(exc)))
    root_stat = root.lstat()
    evidence_unchanged(preimages, issues)
    unique = {
        (p["snapshot"].get("device"), p["snapshot"].get("inode")): p["snapshot"]
        for p in payload
        if "device" in p["snapshot"] and "inode" in p["snapshot"]
    }
    aggregate = {
        "path": str(root),
        "device": root_stat.st_dev,
        "inode": root_stat.st_ino,
        "digest": canonical_digest(payload),
        "logical_bytes": sum(p["logical_bytes"] for p in unique.values()),
        "allocated_bytes": sum(p["allocated_bytes"] for p in unique.values()),
        "entries": [
            {"relative_path": p["relative_path"], "snapshot": p["snapshot"]} for p in payload
        ],
        "complete": not any(i["blocking"] for i in issues),
    }
    return {
        "snapshot": aggregate,
        "payload_files": payload,
        "distributions": distributions,
        "protected_paths": [str(root / name) for name in sorted(protected)],
        "inventory_issues": issues,
        "evidence_preimages": preimages,
        "evidence_paths": sorted(set(input_paths + lock_evidence)),
    }
