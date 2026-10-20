"""Version-qualified native owners. No caller-supplied command is executable.

Discovery invokes only local, non-bootstrapping reads. A dynamic owner operation
binds its destinations and policy, not a frozen inventory of cache entries.
"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import signal
import stat
import subprocess
from pathlib import Path
from typing import Callable

from _cleanup_common import CleanupError, canonical_digest

ADAPTER_VERSION = "native-owners-1"
VERSIONS = {
    "npm": "11.19.0",
    "uv": "0.12.23",
    "pnpm": "12.9.1",
    "container": "1.5.0",
    "buildx": "0.33.0",
    "orb": "2.2.3",
}
PACKAGE_OWNERS = {"npm", "uv", "pnpm"}
ENGINE_OWNERS = {"apple-buildkit", "apple-container", "orbstack-buildx", "orbstack"}
_ENV_KEYS = {
    "HOME",
    "PATH",
    "XDG_CACHE_HOME",
    "XDG_CONFIG_HOME",
    "XDG_DATA_HOME",
    "PNPM_HOME",
    "UV_CACHE_DIR",
    "UV_CONFIG_FILE",
    "DOCKER_CONFIG",
    "BUILDX_CONFIG",
    "DOCKER_HOST",
    "DOCKER_CONTEXT",
    "CONTAINER_ROOT",
}


def _env() -> dict[str, str]:
    result = dict(os.environ)
    # Version/config queries must not produce npm log files or update checks.
    result.update(
        {
            "NO_COLOR": "1",
            "CI": "1",
            "UV_OFFLINE": "1",
            "UV_NO_PROGRESS": "1",
            "npm_config_update_notifier": "false",
            "npm_config_logs_max": "0",
        }
    )
    return result


def _read(argv: list[str]) -> str:
    try:
        result = subprocess.run(
            argv,
            cwd="/",
            env=_env(),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        raise CleanupError(
            "native_read_unavailable",
            "Native owner read did not complete",
            command=argv,
            reason=str(error),
        ) from error
    if result.returncode:
        raise CleanupError(
            "native_read_failed",
            "Native owner refused a read",
            command=argv,
            exit_code=result.returncode,
        )
    return result.stdout.strip()


def _json_read(argv: list[str]):
    try:
        return json.loads(_read(argv))
    except (ValueError, TypeError) as error:
        raise CleanupError(
            "native_output_invalid", "Owner returned invalid JSON", command=argv
        ) from error


def _path_identity(path: str, *, missing: bool = False) -> dict:
    p = Path(path)
    if not p.is_absolute() or "\0" in path:
        raise CleanupError("native_path_invalid", "Owner path must be absolute", path=path)
    resolved = p.resolve()
    try:
        s = resolved.stat()
    except FileNotFoundError:
        if not missing:
            raise CleanupError("native_path_missing", "Owner path no longer exists", path=path)
        ancestor = resolved.parent
        while not ancestor.exists():
            ancestor = ancestor.parent
        return {"path": str(resolved), "missing": True, "ancestor": _path_identity(str(ancestor))}
    return {
        "path": str(resolved),
        "device": s.st_dev,
        "inode": s.st_ino,
        "type": stat.S_IFMT(s.st_mode),
    }


def _executable(name: str) -> dict:
    path = shutil.which(name)
    if not path:
        raise CleanupError(
            "native_owner_missing", "Install the owner separately before inspection", owner=name
        )
    path = str(Path(path).absolute())
    identity = _path_identity(path)
    resolved = identity["path"]
    s = Path(resolved).stat()
    # Multicall executables such as OrbStack's docker-tools dispatch by argv[0].
    # Retain the public entrypoint spelling while binding its resolved bytes.
    identity.update(
        {"path": path, "resolved_path": resolved, "size": s.st_size, "mtime_ns": s.st_mtime_ns}
    )
    # Bind the interpreter as well as npm's JavaScript entrypoint. Other scripts
    # and package-manager shims can bootstrap and are deliberately not admitted.
    with open(resolved, "rb") as stream:
        script = stream.read(8193)
    first = script.split(b"\n", 1)[0]
    if first.startswith(b"#!"):
        if name == "npm" and first in (b"#!/usr/bin/env node", b"#!/usr/bin/node"):
            interpreter = "node" if first == b"#!/usr/bin/env node" else "/usr/bin/node"
            identity["interpreter"] = _executable(interpreter)
        elif name == "container":
            wrapper = re.fullmatch(
                rb'#!/bin/bash\nCONTAINER_INSTALL_ROOT="([^"$`\\\n]+)" exec "([^"$`\\\n]+)"[ \t]+"\$@"\n?',
                script,
            )
            if not wrapper:
                raise CleanupError(
                    "native_wrapper_unsupported",
                    "Container wrapper is not the qualified Homebrew exec wrapper",
                )
            root, target = (part.decode() for part in wrapper.groups())
            dependency = _executable(target)
            install = _path_identity(root)
            if (
                Path(dependency["resolved_path"]).name != "container"
                or Path(dependency["resolved_path"]).parent != Path(install["path"]) / "libexec"
            ):
                raise CleanupError(
                    "native_wrapper_unsupported",
                    "Container wrapper target does not belong to its install root",
                )
            identity.update(
                interpreter=_executable("/bin/bash"),
                wrapper={
                    "type": "homebrew_container_exec",
                    "install_root": install,
                    "target": dependency,
                    "content_digest": canonical_digest(script.decode()),
                },
            )
        else:
            raise CleanupError(
                "native_wrapper_unsupported",
                "Resolve a native owner executable; wrapper not qualified",
                owner=name,
                path=path,
            )
    return identity


def _version(exe: dict, owner: str, args: list[str] | None = None) -> str:
    text = _read([exe["path"], *(args or ["--version"])])
    found = re.search(r"(?<![\d.])v?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)(?![\d.])", text)
    version = found.group(1) if found else None
    if version != VERSIONS[owner]:
        raise CleanupError(
            "native_version_unsupported",
            "Owner version has not been qualified for this route",
            owner=owner,
            observed=version,
            supported=VERSIONS[owner],
        )
    return version


def _resolved(path: str) -> str:
    identity = _path_identity(path, missing=True)
    value = identity["path"]
    if value in ("/", str(Path.home().resolve())):
        raise CleanupError(
            "native_scope_unsafe", "Owner destination is a filesystem or home root", path=value
        )
    return value


def _measurement(paths: list[str]) -> dict:
    """Bounded root allocation only; never label a directory inode its tree size."""
    files, filesystems = [], {}
    for path in paths:
        p = Path(path)
        try:
            q = p
            while not q.exists():
                q = q.parent
            if p.exists():
                s = p.stat()
                if stat.S_ISREG(s.st_mode):
                    files.append(
                        {
                            "path": path,
                            "logical_bytes": s.st_size,
                            "allocated_bytes": s.st_blocks * 512,
                        }
                    )
            fs = os.statvfs(q)
            filesystems[str(q.stat().st_dev)] = {
                "device": q.stat().st_dev,
                "available_bytes": fs.f_bavail * fs.f_frsize,
                "observed_at_path": str(q),
            }
        except OSError:
            continue
    return {
        "files": files,
        "filesystems": list(filesystems.values()),
        "logical_bytes": None,
        "allocated_bytes": None,
        "engine_bytes": None,
        "coverage": "file allocation and same-device host availability; directory trees not traversed",
        "attribution": "Host changes may include concurrent activity; engine bytes are not host bytes",
    }


def _measurement_report(before: dict, after: dict) -> dict:
    """Signed deltas preserve growth and never turn engine sizes into host space."""
    previous_files = {row["path"]: row for row in before.get("files", [])}
    previous_fs = {row["device"]: row for row in before.get("filesystems", [])}
    files = []
    for row in after.get("files", []):
        old = previous_files.get(row["path"])
        if old is not None:
            files.append(
                {
                    "path": row["path"],
                    "logical_delta_bytes": row["logical_bytes"] - old["logical_bytes"],
                    "allocated_delta_bytes": row["allocated_bytes"] - old["allocated_bytes"],
                }
            )
    filesystems = [
        {
            "device": row["device"],
            "available_delta_bytes": row["available_bytes"]
            - previous_fs[row["device"]]["available_bytes"],
        }
        for row in after.get("filesystems", [])
        if row["device"] in previous_fs
    ]
    return {
        "before": before,
        "after": after,
        "file_deltas": files,
        "filesystem_deltas": filesystems,
        "delta_semantics": "after minus before; negative file allocation is shrink, positive host availability is more space",
        "attribution": "Observed host changes may include concurrent activity; engine bytes are separate",
    }


def _candidate(
    owner: str,
    target: str | None,
    action: dict,
    identity: dict,
    scopes: list[dict],
    *,
    operation: str = "clean",
    paths: list[str] | None = None,
) -> dict:
    identity = dict(
        identity,
        adapter=ADAPTER_VERSION,
        environment_digest=canonical_digest(
            {
                k: v
                for k, v in _env().items()
                if k in _ENV_KEYS
                or k.lower().startswith(("npm_config_", "pnpm_", "uv_", "container_"))
            }
        ),
    )
    candidate = {
        "kind": "native",
        "category": owner,
        "owner": owner,
        "target": target,
        "operation": operation,
        "selection_type": "bounded_owner_operation",
        "action": action,
        "identity": identity,
        "scopes": scopes,
        "measurements": _measurement(paths or []),
        "measurement_paths": paths or [],
        "effects": action["effect"],
        "denials": [
            "no stop/start/bootstrap",
            "no remote endpoint",
            "no arbitrary argv",
            "no retry of unresolved execution",
        ],
    }
    candidate["id"] = (
        "native-"
        + canonical_digest(
            {
                k: candidate[k]
                for k in ("owner", "target", "operation", "action", "identity", "scopes")
            }
        ).split(":")[-1][:24]
    )
    return candidate


def _package(owner: str, target: str | None) -> dict:
    exe = _executable(owner)
    identity = {"executable": exe, "version": _version(exe, owner), "cwd": "/"}
    binary = exe["path"]
    if owner == "npm":
        cache = _resolved(target or _read([binary, "config", "get", "cache"]))
        cache_child = Path(cache) / "_cacache"
        if cache_child.is_symlink():
            raise CleanupError(
                "native_scope_unsupported", "A symlinked _cacache needs separate qualification"
            )
        paths = [str(cache_child)]
        action = {
            "type": "npm_cacache_clean",
            "cache": cache,
            "effect": "Remove the entire npm _cacache; preserve _npx and installed tools",
        }
        identity["config"] = {"cache": cache}
    elif owner == "uv":
        args = [binary, "cache", "dir"] + (["--cache-dir", target] if target else [])
        cache = _resolved(_read(args))
        paths = [cache]
        action = {
            "type": "uv_cache_prune",
            "cache": cache,
            "effect": "Prune unused uv cache entries with native in-use protection; never force",
        }
        identity["config"] = {"cache": cache}
    else:
        if platform.system() != "Darwin":
            raise CleanupError(
                "native_platform_unsupported", "pnpm defaults are qualified only on macOS"
            )
        args = [binary, "--ignore-workspace"]
        if target:
            args += ["--store-dir", _resolved(target)]
        store = _resolved(_read([*args, "store", "path"]))
        config = {
            key: _json_read([*args, "config", "get", key, "--json"])
            for key in ("cache-dir", "global-dir", "dlx-cache-max-age")
        }
        # pnpm 12.9.1 config get reports explicit values. These fallbacks are
        # its defaults.rs / derive_layout.rs, not inferred from another pnpm.
        env = _env()
        cache = config["cache-dir"] or str(
            Path(env["XDG_CACHE_HOME"]) / "pnpm"
            if env.get("XDG_CACHE_HOME")
            else Path.home() / "Library/Caches/pnpm"
        )
        pnpm_home = env.get("PNPM_HOME") or str(
            Path(env["XDG_DATA_HOME"]) / "pnpm"
            if env.get("XDG_DATA_HOME")
            else Path.home() / "Library/pnpm"
        )
        global_root = config["global-dir"] or str(Path(pnpm_home) / "global")
        global_pkg_dir = _resolved(str(Path(global_root) / "v11"))
        private = str(Path(global_pkg_dir).parent.parent / "package-manager-store/v11/tmp/private")
        paths = [_resolved(str(Path(cache) / "dlx")), store, _resolved(private)]
        identity["config"] = dict(
            config,
            cache_dir=_resolved(cache),
            global_pkg_dir=global_pkg_dir,
            store=store,
            private_engine_installs=paths[2],
        )
        action = {
            "type": "pnpm_store_prune",
            "store": store,
            "effect": "Sequentially remove expired dlx entries, prune the selected store, then abandoned private engine installs",
        }
    identity["destinations"] = [_path_identity(p, missing=True) for p in paths]
    return _candidate(
        owner, target, action, identity, [{"kind": "path", "path": p} for p in paths], paths=paths
    )


def discover_native(owner: str, target: str | None = None) -> list[dict]:
    if owner in PACKAGE_OWNERS:
        return [_package(owner, target)]
    if owner in ENGINE_OWNERS:
        from _cleanup_engines import discover_engine

        return [discover_engine(owner, target)]
    raise CleanupError(
        "native_owner_unsupported",
        "Select a supported native owner",
        owner=owner,
        supported=sorted(PACKAGE_OWNERS | ENGINE_OWNERS),
    )


def revalidate_native(candidate: dict) -> dict:
    fresh = discover_native(candidate["owner"], candidate.get("target"))[0]
    if any(
        candidate.get(key) != fresh[key] for key in ("action", "identity", "scopes", "operation")
    ):
        raise CleanupError(
            "native_conflict",
            "Native owner, policy, identity or destination changed; inspect again",
            candidate=candidate.get("id"),
        )
    return fresh


def _argv(candidate: dict) -> list[str] | None:
    exe, action = candidate["identity"]["executable"]["path"], candidate["action"]
    match action["type"]:
        case "npm_cacache_clean":
            return [exe, "cache", "clean", "--force", "--cache", action["cache"]]
        case "uv_cache_prune":
            return [exe, "cache", "prune", "--cache-dir", action["cache"]]
        case "pnpm_store_prune":
            return [exe, "--ignore-workspace", "--store-dir", action["store"], "store", "prune"]
        case _:
            from _cleanup_engines import engine_argv

            return engine_argv(candidate)


def _process_identity(pid: int) -> dict | None:
    try:
        result = subprocess.run(
            ["/bin/ps", "-p", str(pid), "-o", "lstart="],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        raise CleanupError(
            "process_visibility_unavailable", "Cannot establish native process identity", pid=pid
        )
    if result.returncode == 1 and not result.stdout.strip():
        return None
    if result.returncode or not result.stdout.strip():
        raise CleanupError(
            "process_visibility_unavailable", "Process identity read failed", pid=pid
        )
    return {"pid": pid, "started": result.stdout.strip()}


def _run_effect(argv: list[str], before_submit: Callable[[dict], None] | None) -> dict:
    checkpoint = before_submit or (lambda value: None)
    checkpoint({"phase": "intent", "command": argv, "execution_ended": False})
    process = None
    process_identity = None
    try:
        process = subprocess.Popen(
            argv,
            cwd="/",
            env=_env(),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            start_new_session=True,
        )
        process_identity = _process_identity(process.pid)
        checkpoint(
            {
                "phase": "submitted",
                "command": argv,
                "process": process_identity,
                "execution_ended": False,
            }
        )
        stdout, stderr = process.communicate()
        return {
            "exit_code": process.returncode,
            "stdout": stdout[-65536:],
            "stderr": stderr[-16384:],
            "stdout_truncated": len(stdout) > 65536,
            "stderr_truncated": len(stderr) > 16384,
            "process": process_identity,
            "command": argv,
            "transport_complete": True,
        }
    except BaseException as error:
        if process is None:
            # No process was returned: an OSError from Popen means no invocation.
            if isinstance(error, OSError):
                return {
                    "exit_code": None,
                    "transport_complete": True,
                    "not_submitted": True,
                    "error": type(error).__name__,
                    "command": argv,
                }
            raise
        # Stop only the child group we created. Remote/native work can outlive
        # it, and even a successful kill is not an owner completion receipt.
        try:
            os.killpg(process.pid, signal.SIGTERM)
            process.communicate(timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            pass
        return {
            "state": "execution_unresolved",
            "execution_ended": False,
            "interrupted": isinstance(error, KeyboardInterrupt),
            "transport_complete": False,
            "process": process_identity,
            "command": argv,
            "error": type(error).__name__,
        }


def execute_native(candidate: dict, *, before_submit: Callable[[dict], None] | None = None) -> dict:
    fresh = revalidate_native(candidate)
    argv = _argv(fresh)
    before = fresh["measurements"]
    if argv is None:
        # Fresh identity validation permits comparison with the reviewed
        # observation, rather than throwing away shrink since discovery.
        report = _measurement_report(candidate["measurements"], before)
        shrink = any(row["allocated_delta_bytes"] < 0 for row in report["file_deltas"])
        return {
            "state": "completed" if shrink else "no_change",
            "execution_ended": True,
            "mode": "observation_only",
            "owner_identity": fresh["identity"],
            "measurements": report,
            "engine_reclaimed_bytes": None,
            "note": "Observed sparse-storage allocation since discovery; no trim command was submitted",
        }
    result = _run_effect(argv, before_submit)
    result["owner_identity"] = fresh["identity"]
    result["measurements"] = _measurement_report(before, _measurement(fresh["measurement_paths"]))
    result["engine_reclaimed_bytes"] = None
    if not result.get("transport_complete"):
        return result
    if result.get("not_submitted"):
        return dict(
            result,
            state="blocked",
            execution_ended=True,
            issue={
                "code": "native_submit_failed",
                "message": "The owner could not be invoked; nothing submitted",
            },
        )
    if result["exit_code"] == 0:
        result.update(state="completed", execution_ended=True)
        if fresh["owner"] == "apple-buildkit":
            try:
                if result.get("stdout_truncated"):
                    raise ValueError("incomplete output")
                rows = [json.loads(line) for line in result["stdout"].splitlines() if line.strip()]
                result["engine_reclaimed_bytes"] = sum(row["Size"] for row in rows)
                result["engine_byte_precision"] = "exact owner-reported cache sizes, not host bytes"
            except (ValueError, KeyError, TypeError):
                result["engine_byte_precision"] = "unknown: output incomplete or unrecognized"
        elif fresh["owner"] == "orbstack-buildx":
            match = re.search(r"^Total:\s*(.*?)\s*$", result["stdout"], re.M)
            result["engine_reclaimed_reported"] = match.group(1) if match else None
    elif fresh["owner"] in PACKAGE_OWNERS and result["exit_code"] > 0:
        result.update(
            state="partial",
            execution_ended=True,
            note="Owner exited with an error; earlier removals may survive",
        )
    else:
        result.update(
            state="execution_unresolved",
            execution_ended=False,
            note="CLI failure does not establish completion of the engine request",
        )
    return result


def read_native(candidate: dict, record: dict) -> dict:
    """Read surviving execution, never invoke cleanup or use size as completion."""
    if record.get("execution_ended"):
        return record
    process = record.get("process")
    if candidate["owner"] in PACKAGE_OWNERS and process:
        current = _process_identity(process["pid"])
        if current != process:
            return {
                "state": "partial",
                "execution_ended": True,
                "attribution": "unknown",
                "note": "Original local owner process ended; no invocation is replayed",
                "measurements": _measurement(candidate.get("measurement_paths", [])),
            }
    if candidate["owner"] in ENGINE_OWNERS:
        from _cleanup_engines import read_engine

        settled = read_engine(candidate, record)
        if settled:
            return settled
    return {
        "state": "execution_unresolved",
        "execution_ended": False,
        "process": process,
        "owner_identity": record.get("owner_identity", candidate["identity"]),
        "note": "No owner receipt establishes that further effects are impossible; retain the claim, do not restart or retry",
    }
