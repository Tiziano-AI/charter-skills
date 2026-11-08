"""Foreground batch execution with durable intent and host-wide resource custody."""

from __future__ import annotations

import os
import sys
import sysconfig
import uuid
from collections import Counter
from pathlib import Path

import _cleanup_common as reports
from _cleanup_common import (
    CleanupError,
    bounded_json,
    canonical_digest,
    contract_digest,
    encoded_size,
    read_json,
    write_json,
)
from _cleanup_custody import (
    Custody,
    account_home,
    candidate_scopes,
    custody_path,
    normalize_scopes,
    path_overlaps,
    scopes_overlap,
)
from _cleanup_fs import FilesystemError, validate_payload_snapshot

STATES = {
    "completed",
    "no_change",
    "skipped",
    "conflict",
    "partial",
    "execution_unresolved",
    "blocked",
    "failed",
}


def _action_budget(candidate: dict) -> int:
    # Diagnostics have a bounded inline representation. Identity, command and
    # reconstruction scale with this exact reviewed candidate, not its file count.
    return 8192 + encoded_size(
        {
            "identity": candidate.get("identity"),
            "action": candidate.get("action"),
            "reconstruction": candidate.get("qualification", {}).get("reconstruction"),
        }
    )


def _orphan_outcome(*, not_submitted: bool = False) -> dict:
    if not_submitted:
        return {
            "state": "blocked",
            "execution_ended": True,
            "not_submitted": True,
            "issues": [
                {
                    "code": "not_invoked",
                    "message": "Writer ended before submission; selected work remains untouched.",
                }
            ],
        }
    return {
        "state": "partial",
        "execution_ended": True,
        "attribution": "unknown",
        "issues": [
            {
                "code": "writer_ended",
                "message": "Filesystem writer ended; inspect surviving files before replanning.",
            }
        ],
    }


def _diagnostic_text(value, budget: int) -> str:
    text = str(value)[:budget]
    low, high = 0, len(text)
    while low < high:
        middle = (low + high + 1) // 2
        if encoded_size(text[:middle]) <= budget:
            low = middle
        else:
            high = middle - 1
    return text[:low]


def _custody_issue(action: dict, phase: str, cause: dict) -> dict:
    return {
        "code": "custody_finalize_failed",
        "message": "Outcome retained but custody finalization failed; use status, never replay.",
        "candidate_id": action["candidate_id"],
        "claim_id": action["claim_id"],
        "phase": phase,
        "error": {
            "code": _diagnostic_text(cause["code"], 128),
            "message": _diagnostic_text(cause["message"], 256),
        },
    }


def _action_envelope(candidate: dict) -> int:
    action = {
        "candidate_id": candidate["id"],
        "claim_id": "0" * 32,
        "state": "execution_unresolved",
        "outcome": None,
        "caller_reported_outcome": None,
        "lifecycle": None,
    }
    issue = _custody_issue(action, "record_outcome", {"code": "x" * 128, "message": "x" * 256})
    # Both the action and the aggregate carry this issue. Charge actual identity
    # bytes and encoded diagnostic caps, including when many native claims remain.
    return encoded_size({**action, "custody_issue": issue}) + encoded_size(issue)


def validate_capacity(plan: dict, operation_path="") -> None:
    """Admit the complete durable journey before creating custody or effects."""
    prospective = {
        "schema_version": 1,
        "helper_version": "1",
        "operation_id": "0" * 32,
        "operation_path": str(operation_path),
        "kind": plan["kind"],
        "plan": plan,
        "actions": [],
        "request_coverage": _request_coverage(
            plan, {candidate["id"]: "execution_unresolved" for candidate in plan["candidates"]}
        ),
    }
    reserve = 4096
    for candidate in plan["candidates"]:
        reserve += _action_budget(candidate) + _action_envelope(candidate)
        # Native recovery can add another full owner readback. Filesystem
        # recovery either reuses its terminal receipt or adds a fixed orphan
        # outcome; reserve those actual facts, not a second arbitrary payload.
        if candidate["kind"] == "native":
            reserve += _action_budget(candidate) + 4096 + encoded_size(candidate)
        else:
            reserve += max(
                encoded_size(_orphan_outcome(not_submitted=True)),
                encoded_size(_orphan_outcome()),
            )
    if reserve >= reports.MAX_REPORT_BYTES:
        raise CleanupError("report_too_large", "Select fewer candidates to retain durable outcomes")
    bounded_json(prospective, reserve_bytes=reserve)


def _bounded_outcome(value: dict, candidate: dict) -> dict:
    if encoded_size(value) <= _action_budget(candidate):
        return value
    # Completion and recovery facts survive diagnostic compaction. The original
    # preimages and reconstruction remain in the plan; omitted diagnostics are
    # explicitly identified, never presented as a complete owner transcript.
    keys = {
        "state",
        "reported_state",
        "execution_ended",
        "not_submitted",
        "interrupted",
        "process",
        "command",
        "exit_code",
        "transport_complete",
        "attribution",
        "owner_identity",
        "reconstruction",
        "removed_count",
        "removed_prefix_count",
        "removed_path_count",
        "selection_digest",
        "next_relative_path",
        "engine_reclaimed_bytes",
        "engine_byte_precision",
        "engine_reclaimed_reported",
    }
    result = {key: value[key] for key in keys if key in value}
    result["diagnostics"] = {
        "complete": False,
        "source_digest": canonical_digest(value),
        "source_bytes": encoded_size(value),
        "omitted_fields": sorted(set(value) - keys - {"issues"}),
    }
    result["issues"] = [
        {
            "code": str(issue.get("code", "unknown"))[:128],
            "message": str(issue.get("message", ""))[:256],
        }
        for issue in value.get("issues", [])[:8]
        if isinstance(issue, dict)
    ]
    if isinstance(value.get("activity"), dict):
        _retain_activity(result, value["activity"], _action_budget(candidate))
    if encoded_size(result) > _action_budget(candidate):
        raise CleanupError("report_too_large", "Owner recovery facts exceed the admitted budget")
    return result


def _retain_activity(result: dict, observed: dict, budget: int) -> None:
    """Keep refusal causes ahead of bulky metadata bindings, within admission."""
    rows = {key: observed.get(key, []) for key in ("busy", "issues", "dangling_references")}
    summary = {
        key: observed[key]
        for key in (
            "complete",
            "process_complete",
            "consumer_complete",
            "consumer_metadata_inspected",
            "process_uid",
            "other_uid_open_files_unobserved",
        )
        if key in observed
    }
    summary.update(
        **{key: [] for key in rows},
        busy_count=len(rows["busy"]),
        issue_count=len(rows["issues"]),
        dangling_reference_count=len(rows["dangling_references"]),
        omitted_counts={
            **{key: len(items) for key, items in rows.items()},
            "consumer_metadata": len(observed.get("consumer_metadata", [])),
        },
    )
    result["activity"] = summary
    coverage = observed.get("consumer_coverage")
    if isinstance(coverage, dict):
        roots = coverage.get("roots", [])
        summary["consumer_coverage"] = {
            key: coverage[key]
            for key in (
                "complete",
                "metadata_binding_limit",
                "metadata_bindings",
                "metadata_entries_inspected",
            )
            if key in coverage
        }
        summary["consumer_coverage"].update(
            requested_root_count=len(coverage.get("requested_roots", [])),
            root_count=len(roots),
            omitted_root_count=len(roots),
            root_states=dict(Counter(root.get("state") for root in roots)),
            roots=[],
        )
    result["diagnostics"]["omitted_fields"].remove("activity")
    result["diagnostics"]["summarized_fields"] = ["activity"]
    # Interleave examples so many busy records cannot erase visibility issues.
    # Every retained row is exact; counts disclose unsaved records, not truncated
    # paths that might name another object. Full metadata stays out of outcomes.
    for index in range(8):
        for key, items in rows.items():
            if index >= len(items):
                continue
            summary[key].append(items[index])
            summary["omitted_counts"][key] -= 1
            if encoded_size(result) > budget:
                summary[key].pop()
                summary["omitted_counts"][key] += 1
    if isinstance(coverage, dict):
        retained = summary["consumer_coverage"]
        for root in roots:
            retained["roots"].append(root)
            retained["omitted_root_count"] -= 1
            if encoded_size(result) > budget:
                retained["roots"].pop()
                retained["omitted_root_count"] += 1


def _issue(error: BaseException) -> dict:
    if isinstance(error, CleanupError):
        return error.as_dict()
    return {
        "code": getattr(
            error,
            "code",
            "execution_interrupted" if not isinstance(error, Exception) else "execution_error",
        ),
        "message": str(error) or type(error).__name__,
    }


def _protect(scopes: list[dict], operation: Path, state: Path) -> None:
    protected = [
        str(Path(__file__).resolve().parent.parent),
        os.path.realpath(sys.executable),
        os.path.realpath(sysconfig.get_path("stdlib")),
        os.path.realpath(state),
        os.path.realpath(operation),
    ]
    if (Path(sys.prefix) / "pyvenv.cfg").exists():
        protected.append(os.path.realpath(sys.prefix))
    roots = ["/", str(account_home()), os.path.realpath(os.getcwd())]
    for scope in scopes:
        if scope["kind"] != "path":
            continue
        target = scope["path"]
        if target in roots or any(path_overlaps(target, path) for path in protected):
            raise CleanupError(
                "protected_target",
                "Selection reaches the helper, its runtime, custody or report.",
                path=target,
            )
        if any(root.startswith(target.rstrip("/") + "/") for root in roots[1:]):
            raise CleanupError(
                "protected_target",
                "Selection contains the account or workspace root.",
                path=target,
            )


def _validate(plan: dict, confirm_digest: str, kind: str, operation: Path, state: Path) -> None:
    if (
        not isinstance(plan, dict)
        or plan.get("schema_version") != 1
        or plan.get("helper_version") != "1"
        or plan.get("type") != "plan"
        or kind not in {"cleanup", "reclaim"}
        or plan.get("kind") != kind
        or not isinstance(plan.get("candidates"), list)
    ):
        raise CleanupError("invalid_plan", "Expected a current cleanup or reclaim plan.")
    digest = canonical_digest({key: value for key, value in plan.items() if key != "digest"})
    if plan.get("digest") != digest or confirm_digest != digest:
        raise CleanupError(
            "plan_digest_mismatch", "Confirmed digest does not match this exact plan."
        )
    if plan.get("contract_digest") != contract_digest():
        raise CleanupError("stale_contract", "Helper changed; inspect and plan again.")
    seen, selection = set(), []
    for candidate in plan["candidates"]:
        if (
            not isinstance(candidate, dict)
            or not isinstance(candidate.get("id"), str)
            or not candidate["id"]
            or candidate["id"] in seen
            or candidate.get("kind") not in {"filesystem", "native"}
        ):
            raise CleanupError("invalid_plan", "Candidate identities must be unique and supported.")
        seen.add(candidate["id"])
        scopes = normalize_scopes(candidate.get("scopes"))
        expected = "reclaim" if candidate.get("operation") == "reclaim" else "cleanup"
        if expected != kind:
            raise CleanupError("operation_mismatch", "Cleanup and reclaim require separate plans.")
        if candidate["kind"] == "filesystem":
            _validate_filesystem_scopes(candidate, scopes)
        _protect(scopes, operation, state)
        claimed = candidate_scopes(candidate)
        _protect(claimed, operation, state)
        if any(scopes_overlap(claimed, prior) for prior in selection):
            raise CleanupError(
                "overlapping_targets",
                "Selected candidates have overlapping resource scopes.",
            )
        selection.append(claimed)


def _validate_filesystem_scopes(candidate: dict, scopes: list[dict]) -> None:
    target = candidate.get("path")
    normalize_scopes([{"kind": "path", "path": target}])
    if candidate.get("category") == "venv_payload":
        if scopes != [{"kind": "path", "path": target}]:
            raise CleanupError(
                "invalid_scopes",
                "Python payload custody must cover the retained environment.",
            )
        snapshot = candidate.get("snapshot")
        if not isinstance(snapshot, dict) or snapshot.get("path") != target:
            raise CleanupError("invalid_snapshot", "Payload snapshot must match its environment.")
        try:
            validate_payload_snapshot(snapshot)
        except (FilesystemError, KeyError, TypeError, ValueError) as error:
            raise CleanupError("invalid_snapshot", str(error)) from error
        return
    elif not any(
        scope["kind"] == "path"
        and (target == scope["path"] or target.startswith(scope["path"].rstrip("/") + "/"))
        for scope in scopes
    ):
        raise CleanupError(
            "invalid_scopes", "Filesystem target must be covered by its resource claim."
        )
    else:
        snapshots = ((target, candidate.get("snapshot")),)
    for path, snapshot in snapshots:
        if not isinstance(snapshot, dict) or snapshot.get("path") != path:
            raise CleanupError(
                "invalid_snapshot",
                "Removal snapshot must match the reported filesystem target.",
                path=path,
            )


def _outcome(value: dict, *, native: bool, invoked: bool) -> dict:
    if not isinstance(value, dict) or value.get("state") not in STATES:
        raise CleanupError("invalid_outcome", "Action did not return a supported outcome.")
    value = dict(value)
    if native and invoked and value.get("execution_ended") is not True:
        value["reported_state"] = value["state"]
        value["state"] = "execution_unresolved"
        value["execution_ended"] = False
    elif not native or not invoked:
        value["execution_ended"] = True
    return value


def _aggregate(outcomes: list[dict], expected: int) -> dict:
    counts = dict(Counter(outcome["state"] for outcome in outcomes))
    for state in sorted(STATES):
        counts.setdefault(state, 0)
    counts["not_started"] = expected - sum(counts.values())
    if counts["execution_unresolved"]:
        result = "execution_unresolved"
    elif counts["partial"] or counts["not_started"]:
        result = "partial"
    elif any(counts[key] for key in ("failed", "blocked", "conflict", "skipped")):
        present = [
            key
            for key in (
                "failed",
                "blocked",
                "conflict",
                "skipped",
                "completed",
                "no_change",
            )
            if counts[key]
        ]
        result = present[0] if len(present) == 1 else "partial"
    else:
        result = "completed" if counts["completed"] else "no_change"
    return {
        "counts": counts,
        "state": result,
        "exit_code": 0 if result in {"completed", "no_change"} else 1,
    }


def _request_coverage(plan: dict, outcomes: dict) -> dict | None:
    coverage = plan.get("request_coverage")
    if coverage is None:
        return None
    rows = [
        {
            **row,
            "state": outcomes.get(row["id"], "not_started")
            if row["selection_state"] == "selected"
            else row["selection_state"],
        }
        for row in coverage["candidates"]
    ]
    accounted = (
        coverage["inspection_complete"]
        and not coverage["native_findings"]
        and all(row["state"] in {"completed", "no_change", "retained"} for row in rows)
    )
    return {**coverage, "candidates": rows, "state": "accounted" if accounted else "partial"}


def _summary(record: dict) -> dict:
    record.update(
        _aggregate(
            [action["outcome"] for action in record["actions"] if "outcome" in action],
            len(record["plan"]["candidates"]),
        )
    )
    custody_issues = [
        action["custody_issue"] for action in record["actions"] if "custody_issue" in action
    ]
    record["custody_recovery_required"] = bool(custody_issues)
    record["issues"] = [
        issue
        for issue in record.get("issues", [])
        if issue.get("code") != "custody_finalize_failed"
    ] + custody_issues
    if custody_issues and record["state"] != "execution_unresolved":
        record.update(state="partial", exit_code=1)
    record["result_scope"] = "selected_plan"
    coverage = _request_coverage(
        record["plan"],
        {
            action["candidate_id"]: action.get("outcome", {}).get("state", "not_started")
            for action in record["actions"]
        },
    )
    if coverage is not None:
        record["request_coverage"] = coverage
    return record


def _save_custody_failure(
    action: dict, record: dict, path: Path, phase: str, error: BaseException
) -> bool:
    # Preserve the known effect separately from unfinished custody. This report
    # is caller-owned: only durable claim evidence or native readback can settle it.
    action["custody_issue"] = _custody_issue(action, phase, _issue(error))
    if not isinstance(error, Exception) or isinstance(error, InterruptedError):
        record["interrupted"] = True
    write_json(path, _summary(record))
    return True


def _finish_action(action: dict, record: dict, path: Path, lease) -> bool:
    """Persist a known outcome even when custody cannot record or release it."""
    if lease is not None:
        try:
            # Report-only evidence must never become the durable termination
            # outcome that status trusts. action.outcome comes from execution or
            # the trusted claim/owner readback, never the caller's old receipt.
            trusted = {
                key: value
                for key, value in action.items()
                if key not in {"caller_reported_outcome", "custody_issue"}
            }
            lease.update(state=action["state"], action=trusted)
        except BaseException as error:
            return _save_custody_failure(action, record, path, "record_outcome", error)
    write_json(path, record)
    if lease is not None and action["outcome"].get("execution_ended") is True:
        try:
            lease.release()
        except BaseException as error:
            return _save_custody_failure(action, record, path, "release", error)
    return False


def _run_action(
    candidate: dict, record: dict, path: Path, custody: Custody, preflight, execute
) -> bool:
    action = {"candidate_id": candidate["id"], "state": "checking"}
    record["actions"].append(action)
    lease = None
    invoked = False
    interrupted = False
    checked = None
    try:
        lease = custody.claim(candidate, str(path), record["operation_id"])
        action["claim_id"] = lease.claim["claim_id"]
        write_json(path, record)
        checked = preflight(candidate)
        if checked is not None and "state" in checked:
            result = _outcome(checked, native=candidate["kind"] == "native", invoked=False)
        else:
            action["state"] = "preparing" if candidate["kind"] == "native" else "invoking"
            write_json(path, record)
            lease.update(state=action["state"], action=action)

            def checkpoint(facts: dict) -> None:
                nonlocal invoked
                if not isinstance(facts, dict):
                    raise CleanupError(
                        "invalid_checkpoint", "Lifecycle checkpoint must be an object."
                    )
                action["state"] = "invoking"
                lifecycle = {**action.get("lifecycle", {}), **facts}
                if encoded_size(lifecycle) > 4096 + encoded_size(candidate):
                    raise CleanupError("report_too_large", "Lifecycle exceeds its admitted budget")
                action["lifecycle"] = lifecycle
                lease.update(state="invoking", action=action)
                write_json(path, record)
                # Native dispatch must cross this durable before-submit
                # boundary before effects. Revalidation precedes it.
                invoked = True

            invoked = candidate["kind"] != "native"
            result = _outcome(
                execute(candidate, checkpoint),
                native=candidate["kind"] == "native",
                invoked=True,
            )
            interrupted = result.get("interrupted") is True
            if interrupted:
                record["interrupted"] = True
    except BaseException as error:
        interrupted = not isinstance(error, Exception) or isinstance(error, InterruptedError)
        unresolved = invoked and candidate["kind"] == "native"
        result = {
            "state": "execution_unresolved"
            if unresolved
            else "partial"
            if invoked
            else "conflict"
            if getattr(error, "code", None) == "native_conflict"
            else "blocked",
            "execution_ended": not unresolved,
            "issues": [_issue(error)],
        }
        if candidate["kind"] == "native" and not invoked:
            result["not_submitted"] = True
        if interrupted:
            record["interrupted"] = True
    if checked is not None and "activity" in checked:
        result["activity"] = checked["activity"]
    result = _bounded_outcome(result, candidate)
    action["state"] = result["state"]
    action["outcome"] = result
    try:
        custody_failed = _finish_action(action, record, path, lease)
    finally:
        if lease is not None:
            lease.close()
    return interrupted or custody_failed


def execute_plan(
    plan: dict,
    operation_path,
    confirm_digest: str,
    kind: str,
    *,
    preflight,
    execute,
    state_dir=None,
) -> dict:
    """Callbacks are internal dispatch, never caller-supplied command strings.

    preflight(candidate) returns None or an untouched-candidate outcome.
    execute(candidate, checkpoint) returns an outcome; native terminal outcomes
    explicitly assert execution_ended. Native dispatch must call checkpoint
    before submitting any effect, after its final read-only revalidation.
    """
    path = Path(operation_path).absolute()
    state = Path(state_dir) if state_dir is not None else custody_path()
    _validate(plan, confirm_digest, kind, path, state)
    validate_capacity(plan, path)
    record = {
        "schema_version": 1,
        "helper_version": "1",
        "operation_id": uuid.uuid4().hex,
        "operation_path": str(path),
        "kind": kind,
        "state": "running",
        "plan": plan,
        "actions": [],
    }
    try:
        write_json(path, record, exclusive=True)
    except FileExistsError:
        return {
            "state": "operation_exists",
            "exit_code": 1,
            "operation_path": str(path),
            "operation": status(path, state_dir=state_dir),
        }
    try:
        custody = Custody(state_dir)
    except (OSError, CleanupError) as error:
        record.update(
            state="blocked",
            exit_code=1,
            issues=[_issue(error)],
            counts={"not_started": len(plan["candidates"])},
        )
        write_json(path, record)
        return record
    try:
        for candidate in plan["candidates"]:
            if _run_action(candidate, record, path, custody, preflight, execute):
                break
        _summary(record)
        write_json(path, record)
        return record
    finally:
        custody.close()


def _settle(lease, readback, operation: dict | None) -> dict | None:
    claim = lease.claim
    action = claim.get("action", {})
    recorded = action.get("outcome", {})
    if recorded.get("execution_ended") is True:
        result = recorded
    elif claim.get("state") in {"admitted", "preparing"}:
        result = _orphan_outcome(not_submitted=True)
    elif claim["candidate"]["kind"] == "filesystem":
        result = _orphan_outcome()
    elif readback is not None:
        result = readback(claim["candidate"], action)
        if result is None:
            return None
        result = _outcome(result, native=claim["candidate"]["kind"] == "native", invoked=True)
    else:
        return None
    result = _bounded_outcome(result, claim["candidate"])
    action = dict(
        action,
        candidate_id=claim["candidate"]["id"],
        claim_id=claim["claim_id"],
        state=result["state"],
        outcome=result,
    )
    if operation is not None:
        actions = operation["actions"]
        index = next(
            (
                i
                for i, old in enumerate(actions)
                if old.get("candidate_id") == action["candidate_id"]
            ),
            None,
        )
        if index is None:
            actions.append(action)
        else:
            previous = actions[index]
            if "caller_reported_outcome" in previous:
                action["caller_reported_outcome"] = previous["caller_reported_outcome"]
            elif previous.get("outcome") is not None and previous["outcome"] != result:
                action["caller_reported_outcome"] = previous["outcome"]
            actions[index] = action
        _summary(operation)
        if _finish_action(action, operation, Path(claim["operation_path"]), lease):
            issue = action["custody_issue"]
            raise CleanupError(
                issue["code"],
                issue["message"],
                **{key: value for key, value in issue.items() if key not in {"code", "message"}},
            )
    else:
        # Custody owns termination evidence even without a writable caller report.
        lease.update(state=result["state"], action=action)
        if result.get("execution_ended") is True:
            lease.release()
    return result


def status(operation_path=None, *, state_dir=None, readback=None) -> dict:
    """Read surviving effects; trusted route readback may settle, never replay."""
    path = Path(operation_path).absolute() if operation_path is not None else None
    operation = read_json(path) if path is not None else None
    if operation is not None and (
        not isinstance(operation, dict)
        or operation.get("schema_version") != 1
        or not isinstance(operation.get("actions"), list)
        or not isinstance(operation.get("plan"), dict)
        or not isinstance(operation["plan"].get("candidates"), list)
    ):
        raise CleanupError("invalid_operation", "Not a cleanup operation record.")
    custody = Custody(state_dir, create=False)
    claims, settled, issues = [], [], []
    try:
        for claim in custody.claims():
            if path is not None and claim["operation_path"] != str(path):
                continue
            lease = custody.acquire_orphan(claim["claim_id"])
            if lease is None:
                claims.append(dict(claim, writer_active=True))
                continue
            try:
                # An existing caller-owned report is not required to retain or read back custody.
                current = operation
                if current is None:
                    try:
                        current = read_json(Path(claim["operation_path"]))
                    except (OSError, CleanupError):
                        current = None
                if current is not None and (
                    not isinstance(current, dict)
                    or current.get("operation_id") != claim["operation_id"]
                    or not isinstance(current.get("actions"), list)
                    or not isinstance(current.get("plan", {}).get("candidates"), list)
                ):
                    raise CleanupError(
                        "operation_changed",
                        "Resource claim points to a different or invalid operation.",
                    )
                result = _settle(lease, readback, current)
                if result is not None and result.get("execution_ended") is True:
                    settled.append({"claim_id": claim["claim_id"], "outcome": result})
                else:
                    claims.append(dict(lease.claim, writer_active=False))
            except Exception as error:
                issues.append(_issue(error))
                claims.append(dict(lease.claim, writer_active=False))
            finally:
                lease.close()
        if operation is not None and operation.get("state") == "running" and not claims:
            operation["recorded_state"] = "running"
            _summary(operation)
            if operation["counts"]["not_started"]:
                issues.append(
                    {
                        "code": "operation_incomplete",
                        "message": "Selected work remains unexecuted in the saved record; status does not replay it.",
                    }
                )
        state = (
            "execution_unresolved"
            if claims
            else operation["state"]
            if operation is not None
            else _aggregate([entry["outcome"] for entry in settled], len(settled))["state"]
        )
        return {
            "schema_version": 1,
            "state": state,
            "observation_state": "partial" if issues else "completed",
            "custody_state": "retained" if claims else "clear",
            "result_scope": "operation" if path is not None else "recovered_claims",
            "exit_code": 0 if state in {"completed", "no_change"} and not issues else 1,
            "custody_path": str(custody.path),
            "claims": claims,
            "settled": settled,
            "operation": operation,
            "issues": issues,
        }
    finally:
        custody.close()
