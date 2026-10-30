"""Semantically bounded native owners. No caller-supplied command is executable.

Discovery invokes only local, non-bootstrapping reads. A dynamic owner operation
binds its destinations and policy, not a frozen inventory of cache entries.
"""

from __future__ import annotations

import hashlib
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

ADAPTER_VERSION = "native-owners-2"
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
    "NODE_OPTIONS",
    "NODE_PATH",
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


def _read(argv: list[str], *, environment: dict | None = None) -> str:
    try:
        result = subprocess.run(
            argv,
            cwd="/",
            env=dict(_env(), **(environment or {})),
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except UnicodeError as error:
        raise CleanupError(
            "native_output_invalid", "Native owner read is not valid text", command=argv
        ) from error
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
    if len(result.stdout.encode("utf-8")) > 1024 * 1024:
        raise CleanupError(
            "native_output_limit",
            "Native discovery output exceeds the bounded read budget",
            command=argv,
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
        {
            "path": path,
            "resolved_path": resolved,
            "size": s.st_size,
            "mtime_ns": s.st_mtime_ns,
            "sha256": _file_digest(Path(resolved)),
        }
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
        elif Path(name).name == "container":
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


def _file_digest(path: Path) -> str:
    before = path.stat()
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    after = path.stat()
    if (before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns) != (
        after.st_ino,
        after.st_size,
        after.st_mtime_ns,
        after.st_ctime_ns,
    ):
        raise CleanupError("native_conflict", "Owner implementation changed while being read")
    return digest.hexdigest()


def _version(exe: dict, owner: str, args: list[str] | None = None) -> str:
    text = _read([exe["path"], *(args or ["--version"])])
    versions = set(re.findall(r"(?<![\d.])v?(\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?)(?![\d.])", text))
    if len(versions) != 1:
        raise CleanupError(
            "native_output_invalid",
            "Owner did not report one unambiguous version",
            owner=owner,
        )
    return versions.pop()


def _capabilities(argv: list[str], options: tuple[str, ...]) -> None:
    """Check command spelling, not deletion semantics or release eligibility."""
    help_text = _read([*argv, "--help"])
    missing = [option for option in options if not re.search(re.escape(option) + r"\b", help_text)]
    if missing:
        raise CleanupError(
            "native_capability_missing", "Owner lacks required command options", missing=missing
        )


def _environment_digest() -> str:
    return canonical_digest(
        {
            k: v
            for k, v in _env().items()
            if k in _ENV_KEYS or k.lower().startswith(("npm_config_", "pnpm_", "uv_", "container_"))
        }
    )


def _npm_implementation(exe: dict) -> dict:
    """Bind installed code, not an approved source hash or a tiny launcher alone."""
    root = Path(exe.get("resolved_path", exe["path"])).parent.parent
    try:
        package = json.loads((root / "package.json").read_text())
        if (
            not isinstance(package, dict)
            or package.get("name") != "npm"
            or not (root / "lib/commands/cache.js").is_file()
        ):
            raise ValueError("npm package layout is absent")
        rows = []
        for base in (root / "package.json", root / "npmrc", root / "lib", root / "node_modules"):
            pending = [(base, frozenset())]
            while pending:
                path, ancestors = pending.pop()
                if not path.exists() and path.name == "npmrc":
                    continue
                resolved = path.resolve(strict=True)
                if not resolved.is_relative_to(root):
                    raise ValueError("npm implementation escapes its installed package")
                if path.is_dir():
                    if resolved in ancestors:
                        raise ValueError("npm implementation has a directory-link cycle")
                    pending.extend((child, ancestors | {resolved}) for child in path.iterdir())
                elif path.is_file():
                    rows.append([str(path.relative_to(root)), str(resolved), _file_digest(path)])
                else:
                    raise ValueError("npm implementation contains a non-regular module")
        return {
            "root": str(root),
            "version": package.get("version"),
            "files": len(rows),
            "digest": canonical_digest(sorted(rows)),
        }
    except (OSError, ValueError, TypeError) as error:
        raise CleanupError(
            "native_implementation_unavailable",
            "Cannot bind installed npm modules",
            reason=str(error),
        ) from error


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
        environment_digest=_environment_digest(),
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
        identity["implementation"] = _npm_implementation(exe)
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
        disabled = _env().get("UV_NO_CACHE", "false").lower()
        if not target and disabled not in {"false", "0", "no", "off"}:
            raise CleanupError(
                "native_configuration_unsupported",
                "UV_NO_CACHE disables a persistent cache; select an exact persistent target",
                variable="UV_NO_CACHE",
            )
        environment = {"UV_NO_CACHE": "false"} if target else {}
        _capabilities([binary, "cache", "prune"], ("--cache-dir",))
        args = [binary, "cache", "dir"] + (["--cache-dir", target] if target else [])
        cache = _resolved(_read(args, environment=environment))
        if target and cache != _resolved(target):
            raise CleanupError(
                "native_scope_unsupported", "uv did not resolve the selected persistent cache"
            )
        paths = [cache]
        action = {
            "type": "uv_cache_prune",
            "cache": cache,
            "environment": environment,
            "effect": "Prune dangling cache entries, all centralized project environments and temporary build environments; native uv lock does not protect external Python consumers",
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
        _capabilities([*args, "store", "prune"], ("--ignore-workspace", "--store-dir"))
        for key in ("cache-dir", "global-dir"):
            if config[key] is not None and (not isinstance(config[key], str) or not config[key]):
                raise CleanupError(
                    "native_output_invalid", "pnpm directory configuration is ambiguous", key=key
                )
        age = config["dlx-cache-max-age"]
        if age is not None and (type(age) is not int or age < 0):
            raise CleanupError(
                "native_output_invalid", "pnpm dlx expiry must be a nonnegative integer"
            )
        age = 1440 if age is None else age
        # Resolve the layout through the installed owner, not a frozen v11
        # path. The read-only bin override avoids an unrelated PATH validation
        # in global root; it changes neither the global nor engine store root.
        env = _env()
        cache = config["cache-dir"] or str(
            Path(env["XDG_CACHE_HOME"]) / "pnpm"
            if env.get("XDG_CACHE_HOME")
            else Path.home() / "Library/Caches/pnpm"
        )
        global_pkg_dir = _resolved(
            _read([*args, "--config.global-bin-dir=/usr/bin", "root", "--global"])
        )
        engine_root = _resolved(str(Path(global_pkg_dir).parent.parent / "package-manager-store"))
        engine_store = _resolved(
            _read([binary, "--ignore-workspace", "--store-dir", engine_root, "store", "path"])
        )
        if not Path(engine_store).is_relative_to(engine_root):
            raise CleanupError(
                "native_scope_unsupported", "pnpm engine store escaped its configured root"
            )
        private = str(Path(engine_store) / "tmp/private")
        paths = [_resolved(str(Path(cache) / "dlx")), store, _resolved(private)]
        identity["config"] = dict(
            config,
            cache_dir=_resolved(cache),
            global_pkg_dir=global_pkg_dir,
            store=store,
            private_engine_installs=paths[2],
            engine_store=engine_store,
        )
        action = {
            "type": "pnpm_store_prune",
            "store": store,
            "cache_dir": _resolved(cache),
            "global_dir": str(Path(global_pkg_dir).parent),
            "dlx_cache_max_age": age,
            "phases": [
                {
                    "kind": "expired_dlx",
                    "path": paths[0],
                    "max_age_minutes": age,
                    "protection": "external activity check; expiry is not proof of disuse",
                },
                {
                    "kind": "unreferenced_packages",
                    "path": store,
                    "protection": "native reference/link/loader policy",
                },
                {
                    "kind": "abandoned_private_installs",
                    "path": paths[2],
                    "protection": "native in-use lock with age fallback",
                },
            ],
            "effect": "Sequentially remove expired dlx entries, prune the selected store, then abandoned private engine installs",
        }
    identity["destinations"] = [_path_identity(p, missing=True) for p in paths]
    result = _candidate(
        owner, target, action, identity, [{"kind": "path", "path": p} for p in paths], paths=paths
    )
    if owner == "uv":
        result["retained_reason"] = {
            "code": "native_environment_scope_conflict",
            "message": "uv cache prune also removes all centralized project environments; environment retirement is outside cache cleanup and there is no native exclusion selector",
        }
    return result


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
    if candidate["action"]["type"] == "orbstack_observe_reclaim":
        return None
    exe, action = candidate["identity"]["executable"]["path"], candidate["action"]
    match action["type"]:
        case "npm_cacache_clean":
            return [exe, "cache", "clean", "--force", "--cache", action["cache"]]
        case "uv_cache_prune":
            return [exe, "cache", "prune", "--cache-dir", action["cache"]]
        case "pnpm_store_prune":
            return [
                exe,
                "--ignore-workspace",
                "--store-dir",
                action["store"],
                "--config.cache-dir=" + action["cache_dir"],
                "--config.global-dir=" + action["global_dir"],
                "--config.dlx-cache-max-age=" + str(action["dlx_cache_max_age"]),
                "store",
                "prune",
            ]
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


def _run_effect(
    argv: list[str],
    before_submit: Callable[[dict], None] | None,
    *,
    environment: dict | None = None,
) -> dict:
    checkpoint = before_submit or (lambda value: None)
    checkpoint({"phase": "intent", "command": argv, "execution_ended": False})
    process = None
    process_identity = None
    try:
        process = subprocess.Popen(
            argv,
            cwd="/",
            env=dict(_env(), **(environment or {})),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
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
    if fresh.get("retained_reason"):
        raise CleanupError(**fresh["retained_reason"])
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
                if any(
                    not isinstance(row, dict) or type(row.get("size")) is not int or row["size"] < 0
                    for row in rows
                ):
                    raise ValueError("unrecognized cache sizes")
                result["engine_reclaimed_bytes"] = sum(row["size"] for row in rows)
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
