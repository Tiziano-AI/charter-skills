"""Descriptor-relative snapshots and macOS guarded deletion; no shell removal.

The kernel guard protects open regular files, not directories or future lazy
consumers. Identity checks and unlinkat are separate syscalls: this is not an
atomic compare-and-delete or a transaction. Callers must exclude active writers.
"""

from __future__ import annotations

import ctypes
import errno
import fcntl
import hashlib
import json
import os
import stat
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path

AT_REMOVEDIR = 0x0080
AT_SYMLINK_NOFOLLOW_ANY = 0x0800
AT_RESOLVE_BENEATH = 0x2000
AT_NODELETEBUSY = 0x4000
GUARD_FLAGS = AT_NODELETEBUSY | AT_SYMLINK_NOFOLLOW_ANY | AT_RESOLVE_BENEATH
_DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC
_QUALIFICATION = None
MAX_ENTRIES = 200000
MAX_DEPTH = 128


class FilesystemError(Exception):
    def __init__(self, code, message):
        self.code, self.message = code, message
        super().__init__(message)


def _issue(code, message):
    return {"code": code, "message": message}


def _digest(value):
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode()).hexdigest()


def _identity(value):
    return {key: value[key] for key in ("device", "inode", "mode", "uid", "gid", "flags")}


def _signature(value):
    return {
        "device": value.st_dev,
        "inode": value.st_ino,
        "mode": value.st_mode,
        "uid": value.st_uid,
        "gid": value.st_gid,
        "flags": getattr(value, "st_flags", 0),
        "nlink": value.st_nlink,
        "size": value.st_size,
        "mtime_ns": value.st_mtime_ns,
        "ctime_ns": value.st_ctime_ns,
        "allocated_bytes": getattr(value, "st_blocks", 0) * 512,
    }


def _path(path, protected_roots=()):
    if not isinstance(path, str) or not path or "\0" in path:
        raise FilesystemError("invalid_path", "A nonempty absolute path is required.")
    if not os.path.isabs(path) or path != os.path.normpath(path) or path.startswith("//"):
        raise FilesystemError(
            "invalid_path", "Use a normalized absolute path without dot components."
        )
    if ".git" in path.split("/"):
        raise FilesystemError("protected_git_metadata", "Git metadata is never a cleanup payload.")
    # Also refuse ancestors of protected roots: removing their parent reaches them.
    roots = ["/", os.path.expanduser("~"), os.getcwd(), *protected_roots]
    for root in roots:
        root = os.path.realpath(os.fspath(root))
        if path == root or (root != "/" and root.startswith(path + "/")):
            raise FilesystemError("protected_root", f"Removal would reach a protected root: {root}")
    return path


def _relative(path):
    if not isinstance(path, str) or not path or path.startswith("/") or "\0" in path:
        raise FilesystemError("invalid_relative_path", "Expected a nonempty relative path.")
    if any(part in ("", ".", "..") for part in path.split("/")):
        raise FilesystemError(
            "invalid_relative_path",
            "Relative paths cannot escape or contain dot components.",
        )
    return path


def _parent(path):
    """Open each ancestor without following links; return a held immediate parent."""
    fd = os.open("/", _DIRECTORY_FLAGS)
    ancestors = [{"path": "/", "signature": _identity(_signature(os.fstat(fd)))}]
    prefix = ""
    try:
        for part in path.split("/")[1:-1]:
            prefix += "/" + part
            next_fd = os.open(part, _DIRECTORY_FLAGS, dir_fd=fd)
            os.close(fd)
            fd = next_fd
            ancestors.append({"path": prefix, "signature": _identity(_signature(os.fstat(fd)))})
        return fd, os.path.basename(path), ancestors
    except BaseException:
        os.close(fd)
        raise


def _walk(parent_fd, name, relative, device, entries):
    if name == ".git":
        raise FilesystemError("protected_git_metadata", "Git metadata is never a cleanup payload.")
    if len(entries) >= MAX_ENTRIES or relative.count("/") >= MAX_DEPTH:
        raise FilesystemError(
            "snapshot_limit",
            "Tree exceeds bounded snapshot coverage; qualify a narrower selection.",
        )
    before = _signature(os.stat(name, dir_fd=parent_fd, follow_symlinks=False))
    if before["device"] != device:
        raise FilesystemError(
            "device_boundary", f"Refusing filesystem boundary at {relative or '.'}."
        )
    mode = before["mode"]
    if not (stat.S_ISREG(mode) or stat.S_ISDIR(mode) or stat.S_ISLNK(mode)):
        raise FilesystemError(
            "unsupported_file_type",
            f"Not a regular file, directory or link: {relative or '.'}",
        )
    row = {"relative_path": relative, "signature": before}
    if stat.S_ISLNK(mode):
        row["link_target"] = os.readlink(name, dir_fd=parent_fd)
    entries.append(row)
    if stat.S_ISDIR(mode):
        fd = os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
        try:
            if _signature(os.fstat(fd)) != before:
                raise FilesystemError("tree_changed", "Directory changed while opening it.")
            for child in sorted(os.listdir(fd)):
                _walk(
                    fd,
                    child,
                    f"{relative}/{child}" if relative else child,
                    device,
                    entries,
                )
            if _signature(os.fstat(fd)) != before:
                raise FilesystemError("tree_changed", "Directory changed during inventory.")
        finally:
            os.close(fd)
    after = _signature(os.stat(name, dir_fd=parent_fd, follow_symlinks=False))
    if after != before:
        raise FilesystemError("tree_changed", "Object changed during inventory.")


def snapshot(path: str, *, protected_roots=()) -> dict:
    """Metadata preimage, including every relative name; never traverses symlinks.

    An inaccessible, unstable or special tree returns complete=False. Invalid or
    protected paths raise FilesystemError. A symlinked owner root must be resolved
    and separately admitted by the caller; ancestor symlinks are rejected.
    """
    path = _path(path, protected_roots)
    result = {
        "path": path,
        "lexical_path": path,
        "complete": False,
        "entries": [],
        "issues": [],
    }
    try:
        fd, name, ancestors = _parent(path)
        try:
            root_stat = os.stat(name, dir_fd=fd, follow_symlinks=False)
            result.update(device=root_stat.st_dev, inode=root_stat.st_ino, ancestors=ancestors)
            _walk(fd, name, "", root_stat.st_dev, result["entries"])
        finally:
            os.close(fd)
        check_fd, _, after = _parent(path)
        os.close(check_fd)
        if after != ancestors:
            raise FilesystemError("ancestor_changed", "An ancestor changed during inventory.")
        result["complete"] = True
    except (OSError, FilesystemError) as error:
        result["issues"].append(_issue(getattr(error, "code", "snapshot_unavailable"), str(error)))
    unique = {}
    for row in result["entries"]:
        sig = row["signature"]
        unique[(sig["device"], sig["inode"])] = sig
    result["logical_bytes"] = sum(s["size"] for s in unique.values() if not stat.S_ISDIR(s["mode"]))
    result["allocated_bytes"] = sum(s["allocated_bytes"] for s in unique.values())
    result["digest"] = _digest({key: result.get(key) for key in ("path", "ancestors", "entries")})
    return result


def _unlinkat(parent_fd, name, directory=False):
    if sys.platform != "darwin":
        raise FilesystemError(
            "guard_unsupported",
            "Guarded deletion is supported only on qualified macOS hosts.",
        )
    libc = ctypes.CDLL(None, use_errno=True)
    try:
        function = libc.unlinkat
    except AttributeError as error:
        raise FilesystemError(
            "guard_unsupported", "The runtime does not expose unlinkat."
        ) from error
    function.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
    function.restype = ctypes.c_int
    flags = GUARD_FLAGS | (AT_REMOVEDIR if directory else 0)
    ctypes.set_errno(0)
    result = function(parent_fd, os.fsencode(name), flags)
    number = ctypes.get_errno()
    if result != 0:
        # Some new-kernel beneath refusals have returned -1 with no errno.
        raise OSError(number or errno.EPERM, os.strerror(number or errno.EPERM), name)


def qualify_guards() -> dict:
    """Test actual syscall behavior against private disposable fixtures once/process."""
    global _QUALIFICATION
    if _QUALIFICATION is not None:
        return dict(_QUALIFICATION)
    result = {
        "supported": False,
        "issues": [],
        "platform": sys.platform,
        "kernel": os.uname().release,
    }
    if sys.platform != "darwin":
        result["issues"].append(
            _issue("guard_unsupported", "This route requires macOS guarded unlinkat.")
        )
        _QUALIFICATION = result
        return dict(result)
    try:
        # Only our fresh private scratch tree is ever removed by TemporaryDirectory.
        with tempfile.TemporaryDirectory(
            prefix="charter-cleanup-guard-", dir="/private/tmp"
        ) as scratch:
            base = Path(scratch)
            (base / "inside").mkdir()
            (base / "outside").write_bytes(b"retain")
            (base / "busy").write_bytes(b"retain until closed")
            (base / "through").symlink_to("inside", target_is_directory=True)
            (base / "inside" / "leaf").write_bytes(b"retain")
            root_fd = os.open(scratch, _DIRECTORY_FLAGS)
            child_fd = os.open(base / "inside", _DIRECTORY_FLAGS)
            busy_fd = os.open(base / "busy", os.O_RDONLY | os.O_NOFOLLOW)
            try:
                try:
                    _unlinkat(root_fd, "busy")
                except OSError as error:
                    if error.errno != errno.EBUSY:
                        raise FilesystemError(
                            "guard_unsupported", "Open-file guard did not report EBUSY."
                        ) from error
                else:
                    raise FilesystemError(
                        "guard_unsupported", "Open-file guard removed an open file."
                    )
                for start, path, survivor in (
                    (root_fd, "through/leaf", base / "inside" / "leaf"),
                    (child_fd, "../outside", base / "outside"),
                ):
                    try:
                        _unlinkat(start, path)
                    except OSError:
                        if not survivor.exists():
                            raise FilesystemError(
                                "guard_unsupported",
                                "Path guard removed its protected fixture.",
                            )
                    else:
                        raise FilesystemError(
                            "guard_unsupported",
                            "Path escape or symlink traversal was accepted.",
                        )
                os.close(busy_fd)
                busy_fd = None
                _unlinkat(root_fd, "busy")
                _unlinkat(root_fd, "through")
                _unlinkat(child_fd, "leaf")
                _unlinkat(root_fd, "inside", directory=True)
                result.update(
                    supported=True,
                    regular_file_busy=True,
                    symlink_traversal_refused=True,
                    beneath_escape_refused=True,
                    directory_busy_guard=False,
                )
            finally:
                if busy_fd is not None:
                    os.close(busy_fd)
                os.close(child_fd)
                os.close(root_fd)
    except (OSError, FilesystemError) as error:
        result["issues"].append(_issue("guard_unsupported", str(error)))
    _QUALIFICATION = result
    return dict(result)


def _check(expected, protected_roots):
    if not expected.get("complete"):
        raise FilesystemError(
            "incomplete_snapshot", "An incomplete snapshot cannot authorize removal."
        )
    current = snapshot(expected["path"], protected_roots=protected_roots)
    if not current["complete"] or current["digest"] != expected.get("digest"):
        raise FilesystemError(
            "preimage_changed",
            "Path identity, ancestors or contents changed after selection.",
        )
    return current


def _is_lock(path):
    name = os.path.basename(path).lower()
    return name in {"lock", ".lock", "lockfile", ".lockfile"} or name.endswith(
        (".lock", ".lockfile")
    )


def _result(state="no_change", count=0, issues=None, **extra):
    return {"state": state, "removed_count": count, "issues": issues or [], **extra}


def _remove(expected, selected, protected_roots):
    """Delete only listed names, deepest first; stop at the first new conflict."""
    path = expected["path"]
    entries = {row["relative_path"]: dict(row["signature"]) for row in expected["entries"]}
    removed = []
    root_parent, root_name, _ = _parent(path)
    try:
        for relative in sorted(selected, key=lambda name: (name.count("/"), name), reverse=True):
            # Reopen absolute ancestors to detect moves before each bounded effect.
            fresh_fd, _, ancestors = _parent(path)
            os.close(fresh_fd)
            if ancestors != expected["ancestors"]:
                raise FilesystemError("ancestor_changed", "An ancestor changed before removal.")
            target = entries[relative]
            parts = relative.split("/") if relative else []
            fd = os.dup(root_parent)
            try:
                components = [root_name, *parts]
                walked = ""
                for index, component in enumerate(components[:-1]):
                    actual = _signature(os.stat(component, dir_fd=fd, follow_symlinks=False))
                    wanted = entries[walked]
                    if _identity(actual) != _identity(wanted):
                        raise FilesystemError(
                            "ancestor_changed",
                            "A selected directory changed before removal.",
                        )
                    next_fd = os.open(component, _DIRECTORY_FLAGS, dir_fd=fd)
                    if _identity(_signature(os.fstat(next_fd))) != _identity(wanted):
                        os.close(next_fd)
                        raise FilesystemError(
                            "ancestor_changed", "A directory changed during open."
                        )
                    os.close(fd)
                    fd = next_fd
                    if index < len(parts) - 1:
                        walked = "/".join(parts[: index + 1])
                name = components[-1]
                actual = _signature(os.stat(name, dir_fd=fd, follow_symlinks=False))
                directory = stat.S_ISDIR(target["mode"])
                # Own earlier child removals change directory times and allocation.
                equal = _identity(actual) == _identity(target) if directory else actual == target
                if not equal:
                    raise FilesystemError(
                        "preimage_changed",
                        "An object changed immediately before removal.",
                    )
                if directory and _open_for_listing(fd, name):
                    raise FilesystemError(
                        "new_content",
                        "Directory contains retained or newly added entries.",
                    )
                _unlinkat(fd, name, directory)
                removed.append(relative)
                # Unlinking one hardlink changes nlink/ctime of its remaining peers.
                if not directory and target["nlink"] > 1:
                    for peer, signature in entries.items():
                        if peer in removed or (
                            signature["device"],
                            signature["inode"],
                        ) != (target["device"], target["inode"]):
                            continue
                        peer_path = path if not peer else path + "/" + peer
                        peer_now = _signature(os.lstat(peer_path))
                        stable = set(signature) - {"nlink", "ctime_ns"}
                        if (
                            any(peer_now[key] != signature[key] for key in stable)
                            or peer_now["nlink"] != signature["nlink"] - 1
                        ):
                            raise FilesystemError(
                                "preimage_changed",
                                "A hardlink peer changed beyond the recorded unlink.",
                            )
                        entries[peer] = peer_now
            finally:
                os.close(fd)
        return _result("completed" if removed else "no_change", len(removed), removed_paths=removed)
    except (OSError, FilesystemError) as error:
        code = getattr(
            error,
            "code",
            "busy_file"
            if getattr(error, "errno", None) == errno.EBUSY
            else "guarded_remove_failed",
        )
        return _result(
            "partial" if removed else "conflict",
            len(removed),
            [_issue(code, str(error))],
            removed_paths=removed,
        )
    finally:
        os.close(root_parent)


def _open_for_listing(parent_fd, name):
    # os.listdir accepts descriptors but does not own/close them.
    fd = os.open(name, _DIRECTORY_FLAGS, dir_fd=parent_fd)
    try:
        return os.listdir(fd)
    finally:
        os.close(fd)


def guard_remove(expected: dict, preserve=(), *, protected_roots=()) -> dict:
    try:
        current = _check(expected, protected_roots)
        qualification = qualify_guards()
        if not qualification["supported"]:
            return _result("skipped", issues=qualification["issues"])
        keep = {_relative(name) for name in preserve}
        selected = set()
        for row in current["entries"]:
            relative = row["relative_path"]
            if _is_lock(relative or current["path"]):
                keep.add(relative)
        for row in current["entries"]:
            relative = row["relative_path"]
            if any(
                relative == saved
                or saved.startswith(relative + "/")
                or relative.startswith(saved + "/")
                or relative == ""
                for saved in keep
            ):
                continue
            selected.add(relative)
        result = _remove(current, selected, protected_roots)
        result["retained_paths"] = sorted(
            row["relative_path"]
            for row in current["entries"]
            if row["relative_path"] not in selected
        )
        return result
    except (OSError, FilesystemError, KeyError, TypeError) as error:
        return _result(
            "conflict",
            issues=[_issue(getattr(error, "code", "invalid_snapshot"), str(error))],
        )


def remove_snapshots(snapshots: list[dict], *, protected_roots=()) -> dict:
    """Precheck all exact files before removal; retain the directory skeleton."""
    removed = []
    try:
        current = [_check(item, protected_roots) for item in snapshots]
        paths = sorted(item["path"] for item in current)
        if len(paths) != len(set(paths)) or any(
            right.startswith(left + "/") for left, right in zip(paths, paths[1:])
        ):
            raise FilesystemError(
                "overlapping_targets",
                "Exact targets must be unique and non-overlapping.",
            )
        if any(
            len(item["entries"]) != 1 or stat.S_ISDIR(item["entries"][0]["signature"]["mode"])
            for item in current
        ):
            raise FilesystemError(
                "not_payload_file",
                "Exact payload removal accepts files and links, not directories.",
            )
        if any(_is_lock(item["path"]) for item in current):
            raise FilesystemError(
                "persistent_lock", "Persistent lock names are retained, never unlinked."
            )
        qualification = qualify_guards()
        if not qualification["supported"]:
            return _result("skipped", issues=qualification["issues"])
        for item in current:
            result = _remove(item, {""}, protected_roots)
            if result["state"] != "completed":
                return _result(
                    "partial" if removed else result["state"],
                    len(removed),
                    result["issues"],
                    removed_paths=removed,
                )
            removed.append(item["path"])
            removed_signature = item["entries"][0]["signature"]
            if removed_signature["nlink"] > 1:
                for peer in current:
                    signature = peer["entries"][0]["signature"]
                    if peer["path"] in removed or (
                        signature["device"],
                        signature["inode"],
                    ) != (removed_signature["device"], removed_signature["inode"]):
                        continue
                    now = _signature(os.lstat(peer["path"]))
                    stable = set(signature) - {"nlink", "ctime_ns"}
                    if (
                        any(now[key] != signature[key] for key in stable)
                        or now["nlink"] != signature["nlink"] - 1
                    ):
                        return _result(
                            "partial",
                            len(removed),
                            [
                                _issue(
                                    "preimage_changed",
                                    "A hardlink peer changed beyond our unlink.",
                                )
                            ],
                            removed_paths=removed,
                        )
                    peer["entries"][0]["signature"] = now
        return _result("completed" if removed else "no_change", len(removed), removed_paths=removed)
    except (OSError, FilesystemError, KeyError, TypeError) as error:
        return _result(
            "partial" if removed else "conflict",
            len(removed),
            [_issue(getattr(error, "code", "invalid_snapshot"), str(error))],
            removed_paths=removed,
        )


@contextmanager
def venv_lock(environment_path: str):
    """Cooperate with an existing uv lock inode; never create or replace one."""
    path = _path(environment_path) + "/.lock"
    parent_fd, name, ancestors = _parent(path)
    lock_fd = None
    held = False
    yielded = False
    try:
        try:
            before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            yielded = True
            yield {"held": False, "reason": "not_present", "path": path}
            return
        if not stat.S_ISREG(before.st_mode):
            raise FilesystemError(
                "lock_invalid", "The persistent environment lock is not a regular file."
            )
        lock_fd = os.open(name, os.O_RDWR | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent_fd)
        if _signature(os.fstat(lock_fd)) != _signature(before):
            raise FilesystemError("lock_changed", "The environment lock changed while opening.")
        try:
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise FilesystemError(
                "lock_busy", "Another cooperating operation holds the environment lock."
            ) from error
        held = True
        after = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        check_fd, _, fresh_ancestors = _parent(path)
        os.close(check_fd)
        if _signature(after) != _signature(before) or fresh_ancestors != ancestors:
            raise FilesystemError(
                "lock_changed",
                "Environment lock identity or ancestors changed during acquisition.",
            )
        yielded = True
        yield {
            "held": True,
            "path": path,
            "device": before.st_dev,
            "inode": before.st_ino,
        }
    except OSError as error:
        if yielded:
            raise
        raise FilesystemError("lock_unavailable", str(error)) from error
    finally:
        if lock_fd is not None:
            if held:
                fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
        os.close(parent_fd)


def activity(paths: list[str], *, consumer_roots=(), owner_roots=()) -> dict:
    from _cleanup_processes import activity as inspect_activity

    return inspect_activity(paths, consumer_roots=consumer_roots, owner_roots=owner_roots)
