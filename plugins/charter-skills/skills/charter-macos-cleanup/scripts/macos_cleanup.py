#!/usr/bin/env python3
"""Agent-facing inspect → qualify → plan → clean/reclaim → status protocol."""

# ruff: noqa: E402 -- isolated Python needs its canonical sibling import path first.

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

from _cleanup_common import (
    HELPER_VERSION,
    CleanupError,
    contract_digest,
    envelope,
    read_json,
    write_json,
)

if sys.version_info < (3, 11):
    print(
        json.dumps(
            envelope(
                None,
                "blocked",
                issues=[
                    {
                        "code": "unsupported_python_version",
                        "message": "This helper requires Python 3.11 or newer",
                        "detected_version": ".".join(map(str, sys.version_info[:3])),
                        "next_action": "Select an existing Python 3.11+ interpreter outside the cleanup targets",
                    }
                ],
            )
        )
    )
    raise SystemExit(2)

from _cleanup_discovery import discover
from _cleanup_execute import execute_plan, status
from _cleanup_fs import FilesystemError, activity, guard_remove, remove_snapshots, venv_lock
from _cleanup_native import discover_native, execute_native, read_native, revalidate_native
from _cleanup_plan import make_plan, qualification_unchanged, seal, summary, validate_document

OWNERS = ("npm", "uv", "pnpm", "apple-buildkit", "apple-container", "orbstack-buildx", "orbstack")


class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise CleanupError("invalid_arguments", message, next_action="Read --help for this command")


def parser():
    root = Parser(
        description=__doc__,
        epilog="Use absolute canonical paths. JSON on stdout; no interactive prompts or force flag.",
    )
    root.add_argument(
        "--json",
        action="store_true",
        help="JSON is always the output protocol; this flag is optional",
    )
    commands = root.add_subparsers(dest="command", required=True)
    inspect = commands.add_parser(
        "inspect", help="Read candidates into a new scan file, or page through an existing scan"
    )
    inspect.add_argument(
        "--root",
        action="append",
        default=[],
        help="Filesystem discovery root; repeat for a bounded inventory",
    )
    inspect.add_argument(
        "--candidate-path",
        action="append",
        default=[],
        help="Explicit output below a root; requires agent qualification",
    )
    inspect.add_argument(
        "--project-root",
        action="append",
        default=[],
        help="Declare an unfamiliar project's consumer boundary within a scanned root; repeat for separate projects",
    )
    inspect.add_argument(
        "--include-caches",
        action="store_true",
        help="Include local tool/download cache seeds, not blanket cache deletion",
    )
    inspect.add_argument(
        "--owner", choices=OWNERS, help="Discover a version-qualified local native owner"
    )
    inspect.add_argument(
        "--target",
        help="Owner-specific exact store, running container ID or builder name; see owner-routes.md",
    )
    inspect.add_argument(
        "--output", help="Create-new scan JSON outside cleanup targets; parent must exist"
    )
    inspect.add_argument("--scan", help="Read a saved scan without rescanning")
    inspect.add_argument(
        "--candidate", help="Show this candidate's qualification template from --scan"
    )
    inspect.add_argument(
        "--cursor", default="0", help="Next offset returned by inspect (default 0)"
    )
    inspect.add_argument(
        "--limit", type=int, default=20, help="Candidate page size, 1–100 (default 20)"
    )
    plan = commands.add_parser(
        "plan",
        help="Bind selected candidates to qualification and reconstruction evidence; no cleanup",
    )
    plan.add_argument("--scan", required=True)
    plan.add_argument(
        "--selection",
        required=True,
        help="JSON schema_version:1, groups:[{ids,reason,reconstruction,evidence_paths,consumer_roots}]",
    )
    plan.add_argument(
        "--output", required=True, help="Create-new plan JSON outside cleanup targets"
    )
    plan.add_argument("--kind", choices=("cleanup", "reclaim"), default="cleanup")
    for name in ("clean", "reclaim"):
        action = commands.add_parser(
            name,
            help="Execute an authorized exact plan once; unresolved resource claims prevent replay",
        )
        action.add_argument("--plan", required=True)
        action.add_argument(
            "--confirm-digest",
            required=True,
            help="Digest from plan; binds scope, does not create human authority",
        )
        action.add_argument(
            "--operation",
            required=True,
            help="Create-new durable operation JSON outside targets, never reuse as a retry",
        )
    state = commands.add_parser(
        "status",
        help="Discover retained claims or reconcile one operation without replay; may settle its custody record",
    )
    state.add_argument(
        "--operation", help="Operation JSON; omit to discover shared resource claims"
    )
    return root


def _inspect(args):
    if not 1 <= args.limit <= 100 or not args.cursor.isdecimal():
        raise CleanupError("invalid_page", "Use limit 1–100 and the returned numeric cursor")
    if args.scan:
        if (
            args.root
            or args.owner
            or args.output
            or args.target
            or args.candidate_path
            or args.project_root
            or args.include_caches
        ):
            raise CleanupError(
                "invalid_arguments",
                "--scan reads an existing inventory; do not combine it with discovery options",
            )
        scan = read_json(args.scan)
        validate_document(scan, "scan")
    else:
        if not args.output or not (args.root or args.owner) or args.candidate:
            raise CleanupError(
                "invalid_arguments",
                "Discovery requires --output and --root or --owner; --candidate requires --scan",
            )
        if (
            args.target
            and not args.owner
            or (args.candidate_path or args.project_root)
            and not args.root
        ):
            raise CleanupError(
                "invalid_arguments",
                "--target requires --owner; --candidate-path and --project-root require --root",
            )
        found = (
            discover(args.root, args.candidate_path, args.include_caches, args.project_root)
            if args.root
            else {"candidates": [], "coverage": {}, "issues": []}
        )
        if args.owner:
            native = discover_native(args.owner, args.target)
            found["candidates"].extend(native if isinstance(native, list) else [native])
        scan = seal(
            {
                "schema_version": 1,
                "helper_version": HELPER_VERSION,
                "type": "scan",
                "contract_digest": contract_digest(),
                "roots": args.root,
                "project_roots": args.project_root,
                **found,
            }
        )
        write_json(args.output, scan, exclusive=True)
    candidates = scan["candidates"]
    if args.candidate:
        chosen = next((c for c in candidates if c["id"] == args.candidate), None)
        if chosen is None:
            raise CleanupError(
                "candidate_not_found", "Candidate is not in this scan", candidate_id=args.candidate
            )
        return {"digest": scan["digest"], "candidate": summary(chosen, detail=True)}, 0
    offset = int(args.cursor)
    end = offset + args.limit
    data = {
        "scan_path": str(Path(args.scan or args.output).absolute()),
        "digest": scan["digest"],
        "coverage": scan["coverage"],
        "issues": scan["issues"],
        "total_candidates": len(candidates),
        "candidates": [summary(c) for c in candidates[offset:end]],
        "next_cursor": str(end) if end < len(candidates) else None,
    }
    return data, 0


def _preflight(candidate):
    changed = qualification_unchanged(candidate)
    if changed:
        return changed
    if candidate["kind"] == "native":
        revalidate_native(candidate)
        if candidate["owner"] not in {"npm", "uv", "pnpm"}:
            return None
        paths = [s["path"] for s in candidate["scopes"] if s["kind"] == "path"]
        # Absence is bound by native destination identity, not a visibility
        # failure. The adapter revalidates again immediately before submission.
        paths = [path for path in paths if os.path.lexists(path)]
        if not paths:
            return {
                "state": "no_change",
                "execution_ended": True,
                "note": "Every qualified native destination is absent; no cleanup submitted",
            }
    else:
        paths = [candidate["path"]]
    observed = activity(
        paths,
        consumer_roots=candidate["qualification"]["consumer_roots"],
        owner_roots=[candidate["owner_root"]] if candidate.get("owner_root") else [],
    )
    if observed["busy"] or not observed["complete"]:
        return {
            "state": "skipped",
            "execution_ended": True,
            "activity": observed,
            "issues": [
                {
                    "code": "consumer_busy" if observed["busy"] else "activity_incomplete",
                    "message": "Candidate retained; do not stop consumers or force through incomplete visibility",
                }
            ],
        }
    return None


def _host_measurement(path):
    root = Path(path)
    while not root.exists() and root != root.parent:
        root = root.parent
    try:
        info = root.stat()
        fs = os.statvfs(root)
        return {
            "device": info.st_dev,
            "observed_at_path": str(root),
            "available_bytes": fs.f_bavail * fs.f_frsize,
        }
    except OSError:
        return None


def _execute(candidate, checkpoint, protected_roots):
    if candidate["kind"] == "native":
        return execute_native(candidate, before_submit=checkpoint)
    before = _host_measurement(candidate["path"])
    if candidate["category"] == "venv_payload":
        with venv_lock(candidate["path"]) as lock:
            # Lock acquisition can race an installer; recheck evidence while held.
            changed = qualification_unchanged(candidate)
            result = changed or remove_snapshots(
                [entry["snapshot"] for entry in candidate["payload_files"]],
                protected_roots=protected_roots,
            )
            result["cooperative_lock"] = lock
    else:
        result = guard_remove(candidate["snapshot"], protected_roots=protected_roots)
    result.update(
        execution_ended=True,
        reconstruction=candidate["qualification"]["reconstruction"],
        host_before=before,
        host_after=_host_measurement(candidate["path"]),
        measurement_note="Host availability includes concurrent changes; unlinked allocation is not physical space recovered",
    )
    return result


def _readback(candidate, record):
    return read_native(candidate, {**record.get("lifecycle", {}), **record.get("outcome", {})})


def _operation_summary(record):
    result = {
        k: v for k, v in record.items() if k not in {"plan", "actions", "claims", "operation"}
    }
    if "actions" in record:
        result["actions"] = [
            {k: v for k, v in action.items() if k != "lifecycle"} for action in record["actions"]
        ]
        for action in result["actions"]:
            outcome = dict(action.get("outcome", {}))
            if "removed_paths" in outcome:
                outcome["removed_path_count"] = len(outcome.pop("removed_paths"))
            action["outcome"] = outcome
    if "claims" in record:
        result["claims"] = [
            {
                k: claim.get(k)
                for k in ("claim_id", "operation_id", "operation_path", "state", "writer_active")
            }
            for claim in record["claims"]
        ]
    if record.get("operation") is not None:
        result["operation"] = _operation_summary(record["operation"])
    return result


def dispatch(args):
    if args.command == "inspect":
        data, code = _inspect(args)
        return envelope("inspect", "completed", data), code
    if args.command == "plan":
        plan = make_plan(read_json(args.scan), read_json(args.selection), args.kind)
        write_json(args.output, plan, exclusive=True)
        return envelope(
            "plan",
            "completed",
            {
                "plan_path": str(Path(args.output).absolute()),
                "digest": plan["digest"],
                "kind": plan["kind"],
                "candidates": [
                    dict(summary(c), qualification=c["qualification"]) for c in plan["candidates"]
                ],
            },
        ), 0
    if args.command == "status":
        result = status(args.operation, readback=_readback)
        code = (
            1
            if result["claims"] or result["issues"]
            else result.get("operation", {}).get("exit_code", 0)
            if result.get("operation")
            else 0
        )
        return envelope("status", result["state"], _operation_summary(result)), code
    plan = read_json(args.plan)
    validate_document(plan, "plan")
    protected = [*plan.get("protected_roots", []), str(Path(args.plan).absolute())]
    result = execute_plan(
        plan,
        args.operation,
        args.confirm_digest,
        "cleanup" if args.command == "clean" else "reclaim",
        preflight=_preflight,
        execute=lambda c, checkpoint: _execute(c, checkpoint, protected),
    )
    return envelope(args.command, result["state"], _operation_summary(result)), result["exit_code"]


def main(argv=None):
    command = None
    try:
        args = parser().parse_args(argv)
        command = args.command
        result, code = dispatch(args)
    except (CleanupError, FilesystemError) as error:
        issue = (
            error.as_dict()
            if isinstance(error, CleanupError)
            else {"code": error.code, "message": str(error)}
        )
        result, code = envelope(command, "blocked", issues=[issue]), 2
    except FileExistsError as error:
        result, code = (
            envelope(
                command,
                "conflict",
                issues=[
                    {
                        "code": "output_exists",
                        "message": "Use a new report path; use status for an existing operation",
                        "path": error.filename,
                    }
                ],
            ),
            1,
        )
    except (OSError, ValueError, TypeError, KeyError) as error:
        result, code = (
            envelope(
                command, "blocked", issues=[{"code": "input_unavailable", "message": str(error)}]
            ),
            2,
        )
    except KeyboardInterrupt:
        result, code = (
            envelope(
                command,
                "execution_unresolved",
                issues=[{"code": "interrupted", "message": "Read status before further effects"}],
            ),
            1,
        )
    print(json.dumps(result, sort_keys=True, allow_nan=False))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
