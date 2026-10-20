"""Foreground batch execution with durable intent and host-wide resource custody."""

from __future__ import annotations

import os
import sys
import sysconfig
import uuid
from collections import Counter
from pathlib import Path

from _cleanup_common import (
    CleanupError,
    canonical_digest,
    contract_digest,
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
        payload = candidate.get("payload_files")
        if (
            not isinstance(payload, list)
            or not payload
            or not all(
                isinstance(row, dict)
                and isinstance(row.get("path"), str)
                and row["path"].startswith(target.rstrip("/") + "/")
                for row in payload
            )
        ):
            raise CleanupError(
                "invalid_scopes",
                "Python payload files must remain below the retained environment.",
            )
        paths = {row["path"] for row in payload}
        declared = {scope["path"] for scope in scopes if scope["kind"] == "path"}
        if paths != declared or len(paths) != len(payload):
            raise CleanupError(
                "invalid_scopes",
                "Python payload files must match the closed scope selection.",
            )
        snapshots = ((row["path"], row.get("snapshot")) for row in payload)
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


def _summary(record: dict) -> dict:
    counts = dict(
        Counter(action["outcome"]["state"] for action in record["actions"] if "outcome" in action)
    )
    for state in sorted(STATES):
        counts.setdefault(state, 0)
    counts["not_started"] = len(record["plan"]["candidates"]) - sum(counts.values())
    record["counts"] = counts
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
    record["state"] = result
    record["exit_code"] = 0 if result in {"completed", "no_change"} else 1
    return record


def _run_action(
    candidate: dict, record: dict, path: Path, custody: Custody, preflight, execute
) -> bool:
    action = {"candidate_id": candidate["id"], "state": "checking"}
    record["actions"].append(action)
    lease = None
    invoked = False
    interrupted = False
    try:
        lease = custody.claim(candidate, str(path), record["operation_id"])
        action["claim_id"] = lease.claim["claim_id"]
        write_json(path, record)
        denied = preflight(candidate)
        if denied is not None:
            result = _outcome(denied, native=candidate["kind"] == "native", invoked=False)
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
                action.setdefault("lifecycle", {}).update(facts)
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
    action["state"] = result["state"]
    action["outcome"] = result
    try:
        if lease is not None:
            lease.update(state=result["state"], action=action)
        write_json(path, record)
        if lease is not None:
            if result.get("execution_ended") is True:
                lease.release()
    finally:
        if lease is not None:
            lease.close()
    return interrupted


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
        result = {
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
    elif claim["candidate"]["kind"] == "filesystem":
        result = {
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
    elif readback is not None:
        result = readback(claim["candidate"], action)
        if result is None:
            return None
        result = _outcome(result, native=claim["candidate"]["kind"] == "native", invoked=True)
    else:
        return None
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
            actions[index] = action
        write_json(Path(claim["operation_path"]), _summary(operation))
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
            else (operation["state"] if operation is not None else "completed")
        )
        return {
            "schema_version": 1,
            "state": state,
            "exit_code": 0 if state in {"completed", "no_change"} and not issues else 1,
            "custody_path": str(custody.path),
            "claims": claims,
            "settled": settled,
            "operation": operation,
            "issues": issues,
        }
    finally:
        custody.close()
