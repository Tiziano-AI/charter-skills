"""Shared protocol and private report I/O; no resource mutation."""

from __future__ import annotations

import hashlib
import json
import os
import stat
import uuid
from pathlib import Path

SCHEMA_VERSION = 1
HELPER_VERSION = "1"


class CleanupError(Exception):
    def __init__(self, code: str, message: str, **details):
        super().__init__(message)
        self.code, self.message, self.details = code, message, details

    def as_dict(self):
        return {"code": self.code, "message": self.message, **self.details}


def canonical_digest(value):
    data = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)
    return "sha256:" + hashlib.sha256(data.encode()).hexdigest()


def contract_digest():
    return canonical_digest(
        {
            p.name: hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(Path(__file__).parent.glob("*.py"))
        }
    )


def _pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise CleanupError("duplicate_key", "Duplicate JSON key", key=key)
        result[key] = value
    return result


def _parent(path):
    target = Path(os.path.abspath(os.fspath(path)))
    if target.name in {"", ".", ".."}:
        raise CleanupError("invalid_path", "Expected a report file", path=str(path))
    descriptor = os.open("/", os.O_RDONLY | os.O_DIRECTORY)
    try:
        for part in target.parent.parts[1:]:
            child = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        return descriptor, target.name
    except BaseException:
        os.close(descriptor)
        raise


def read_json(path):
    parent, name = _parent(path)
    try:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent)
        with os.fdopen(fd, "r", encoding="utf-8") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_size > 256 * 1024 * 1024:
                raise CleanupError("invalid_report", "Expected a bounded regular JSON file")
            try:
                return json.load(
                    stream,
                    object_pairs_hook=_pairs,
                    parse_constant=lambda _: (_ for _ in ()).throw(
                        ValueError("Non-finite JSON number")
                    ),
                )
            except (ValueError, UnicodeError) as exc:
                raise CleanupError("invalid_json", str(exc), path=str(path)) from exc
    finally:
        os.close(parent)


def write_json(path, value, exclusive=False):
    """Write a caller-owned report; refuse symlink traversal and foreign modes."""
    payload = (json.dumps(value, sort_keys=True, indent=2, allow_nan=False) + "\n").encode()
    parent, name = _parent(path)
    temp = None
    try:
        if exclusive:
            fd = os.open(
                name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent
            )
        else:
            try:
                old = os.stat(name, dir_fd=parent, follow_symlinks=False)
                if not stat.S_ISREG(old.st_mode) or old.st_uid != os.getuid():
                    raise CleanupError("unsafe_report", "Report is not an owned regular file")
            except FileNotFoundError:
                pass
            temp = ".cleanup-" + uuid.uuid4().hex
            fd = os.open(
                temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent
            )
        with os.fdopen(fd, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        if temp:
            os.replace(temp, name, src_dir_fd=parent, dst_dir_fd=parent)
            temp = None
        os.fsync(parent)
    finally:
        if temp:
            os.unlink(temp, dir_fd=parent)
        os.close(parent)


def envelope(command, state, data=None, issues=None):
    return {
        "schema_version": SCHEMA_VERSION,
        "command": command,
        "state": state,
        "data": data or {},
        "issues": issues or [],
    }
