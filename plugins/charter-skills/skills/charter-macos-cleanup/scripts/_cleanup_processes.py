"""Read-only process and bounded installed-consumer observations.

Metadata is read as bytes, never imported or evaluated. Completeness describes
the supplied consumer scope, not every possible dynamic reference on the Mac.
"""

from __future__ import annotations

import json
import os
import plistlib
import shlex
import stat
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

from _cleanup_fs import _DIRECTORY_FLAGS, _parent

_METADATA_NAMES = {
    "package.json",
    "settings.json",
    "config.json",
    "pyvenv.cfg",
    "direct_url.json",
    "extensions.json",
    "extensions.yaml",
    "extensions.yml",
}
_METADATA_SUFFIXES = {".pth", ".egg-link", ".plist", ".toml", ".yaml", ".yml"}


def _issue(code, message):
    return {"code": code, "message": message}


def _related(value, target, *, parents=False):
    value = value.rstrip("/") or "/"
    target = target.rstrip("/") or "/"
    return (
        value == target
        or value.startswith(target + "/")
        or (parents and value != "/" and target.startswith(value + "/"))
    )


def _run(arguments):
    try:
        result = subprocess.run(arguments, capture_output=True, timeout=45, check=False)
        return result.returncode, result.stdout, result.stderr
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, b"", str(error).encode()


def _lsof(data, targets):
    rows = []
    pid, descriptor = None, None
    for field in data.split(b"\0"):
        field = field.lstrip(b"\n")
        if not field:
            continue
        code, value = chr(field[0]), os.fsdecode(field[1:])
        if code == "p":
            pid, descriptor = int(value), None
        elif code == "f":
            descriptor = value
        elif code == "n" and pid is not None and pid != os.getpid():
            for target in targets:
                if _related(value, target):
                    rows.append(
                        {
                            "path": target,
                            "pid": pid,
                            "kind": "cwd" if descriptor == "cwd" else "open_file",
                            "reference": value,
                        }
                    )
    return rows


def _argument_paths(command):
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()
    for token in tokens:
        value = token.split("=", 1)[-1] if "=" in token else token
        if value.startswith("/"):
            yield value


def _ps(data, targets):
    rows = []
    for line in os.fsdecode(data).splitlines():
        columns = line.strip().split(None, 2)
        if len(columns) != 3:
            raise ValueError("Process output lacked pid, uid or arguments.")
        pid = int(columns[0])
        if pid == os.getpid():
            continue
        for value in _argument_paths(columns[2]):
            for target in targets:
                if _related(value, target) or _related(os.path.realpath(value), target):
                    rows.append(
                        {
                            "path": target,
                            "pid": pid,
                            "kind": "process_argument",
                            "reference": value,
                        }
                    )
    return rows


def _strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, list):
        for item in value:
            yield from _strings(item)
    elif isinstance(value, dict):
        for item in value.values():
            yield from _strings(item)


def _references(path, content):
    """Return static path strings, never execute .pth, shebangs or configuration."""
    if path.suffix == ".plist":
        values = list(_strings(plistlib.loads(content)))
    elif path.suffix == ".json":
        values = list(_strings(json.loads(content)))
    else:
        text = content.decode("utf-8")
        values = text.splitlines()
    for value in values:
        value = value.strip()
        if value.startswith("file://"):
            parsed = urlparse(value)
            if parsed.netloc in ("", "localhost"):
                yield unquote(parsed.path)
        if (
            path.suffix in {".pth", ".egg-link"}
            and value
            and not value.startswith(("#", "import ", "import\t"))
        ):
            yield os.path.abspath(path.parent / value)
        if value.startswith("#!"):
            value = value[2:].strip()
        yield from _argument_paths(value)
        # Metadata often embeds paths after TOML/YAML assignment or JSON values.
        if value.startswith("/"):
            yield value


def _consumer_files(roots, issues, *, maximum_files=20000):
    """Bound reads explicitly; report every exhausted/unreadable scope."""
    count = 0
    for root_text in roots:
        root = Path(root_text)
        try:
            parent_fd, name, _ = _parent(str(root))
            try:
                initial = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            finally:
                os.close(parent_fd)
            if stat.S_ISLNK(initial.st_mode) or stat.S_ISREG(initial.st_mode):
                yield root, initial
                continue
            if not stat.S_ISDIR(initial.st_mode):
                issues.append(
                    _issue(
                        "consumer_scope_unreadable",
                        f"Not a directory or metadata file: {root}",
                    )
                )
                continue
            pending = [root]
            while pending:
                parent = pending.pop()
                ancestor_fd, name, _ = _parent(str(parent))
                try:
                    directory_fd = os.open(name, _DIRECTORY_FLAGS, dir_fd=ancestor_fd)
                finally:
                    os.close(ancestor_fd)
                try:
                    before = os.fstat(directory_fd)
                    if before.st_dev != initial.st_dev:
                        issues.append(
                            _issue(
                                "consumer_scope_changed",
                                f"Consumer directory crosses a filesystem: {parent}",
                            )
                        )
                        continue
                    with os.scandir(directory_fd) as children:
                        for child in children:
                            count += 1
                            if count > maximum_files:
                                issues.append(
                                    _issue(
                                        "consumer_scope_incomplete",
                                        "Consumer scope exceeds bounded coverage.",
                                    )
                                )
                                return
                            entry = child.stat(follow_symlinks=False)
                            candidate = parent / child.name
                            if entry.st_dev != initial.st_dev:
                                issues.append(
                                    _issue(
                                        "consumer_device_boundary",
                                        f"Skipped filesystem boundary: {candidate}",
                                    )
                                )
                            elif stat.S_ISDIR(entry.st_mode):
                                pending.append(candidate)
                            elif stat.S_ISLNK(entry.st_mode) or stat.S_ISREG(entry.st_mode):
                                yield candidate, entry
                    after = os.fstat(directory_fd)
                    if (before.st_dev, before.st_ino, before.st_mtime_ns) != (
                        after.st_dev,
                        after.st_ino,
                        after.st_mtime_ns,
                    ):
                        issues.append(
                            _issue(
                                "consumer_scope_changed",
                                f"Consumer directory changed while inspected: {parent}",
                            )
                        )
                finally:
                    os.close(directory_fd)
        except OSError as error:
            issues.append(_issue("consumer_scope_unreadable", str(error)))


def _consumers(roots, targets):
    busy, issues, inspected = [], [], 0
    if not roots:
        return (
            [],
            [
                _issue(
                    "source_consumer_scope_missing",
                    "No bounded installed-consumer metadata scope was supplied.",
                )
            ],
            0,
        )
    for path, observed in _consumer_files(roots, issues):
        try:
            references = []
            kind = "installed_metadata"
            if stat.S_ISLNK(observed.st_mode):
                references = [os.path.realpath(path)]
                kind = "installed_symlink"
            elif (
                path.name in _METADATA_NAMES
                or path.suffix in _METADATA_SUFFIXES
                or observed.st_mode & 0o111
            ):
                parent_fd, name, _ = _parent(str(path))
                try:
                    fd = os.open(
                        name,
                        os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC,
                        dir_fd=parent_fd,
                    )
                finally:
                    os.close(parent_fd)
                try:
                    opened = os.fstat(fd)
                    if (opened.st_dev, opened.st_ino) != (
                        observed.st_dev,
                        observed.st_ino,
                    ):
                        raise OSError("Consumer metadata changed while opening.")
                    prefix = os.read(fd, 2)
                    script = (
                        observed.st_mode & 0o111
                        and path.name not in _METADATA_NAMES
                        and path.suffix not in _METADATA_SUFFIXES
                    )
                    if script and prefix != b"#!":
                        continue
                    if observed.st_size > 1024 * 1024:
                        issues.append(
                            _issue(
                                "consumer_metadata_too_large",
                                f"Metadata exceeds bounded read: {path}",
                            )
                        )
                        continue
                    content = prefix + os.read(fd, 1024 * 1024 + 1)
                    after = os.fstat(fd)
                    if (opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != (
                        after.st_size,
                        after.st_mtime_ns,
                        after.st_ctime_ns,
                    ):
                        raise OSError("Consumer metadata changed while reading.")
                finally:
                    os.close(fd)
                if script:
                    kind = "installed_shebang"
                references = list(_references(path, content))
                if path.suffix == ".pth" and any(
                    line.lstrip().startswith((b"import ", b"import\t"))
                    for line in content.splitlines()
                ):
                    issues.append(
                        _issue(
                            "dynamic_consumer_reference",
                            f"Executable .pth content was not evaluated: {path}",
                        )
                    )
            else:
                continue
            inspected += 1
            for reference in references:
                for target in targets:
                    if _related(reference, target):
                        busy.append(
                            {
                                "path": target,
                                "kind": kind,
                                "consumer": str(path),
                                "reference": reference,
                            }
                        )
        except (
            OSError,
            ValueError,
            UnicodeError,
            plistlib.InvalidFileException,
        ) as error:
            issues.append(_issue("consumer_metadata_unreadable", f"{path}: {error}"))
    return busy, issues, inspected


def _scope_ownership(paths):
    issues = []
    for path in paths:
        try:
            parent_fd, name, _ = _parent(path)
            try:
                value = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            finally:
                os.close(parent_fd)
            if value.st_uid != os.geteuid():
                issues.append(
                    _issue(
                        "process_scope_owner_unobservable",
                        "The selected scope is not owned by the observed user.",
                    )
                )
        except OSError as error:
            issues.append(_issue("activity_scope_unavailable", str(error)))
    return issues


def _visible_pids(data):
    return {
        int(field[1:]) for raw in data.split(b"\0") if (field := raw.lstrip(b"\n")).startswith(b"p")
    }


def _resolve_census_gaps(missing, targets, busy):
    """Reconcile only exact PIDs missing across the two sequential snapshots."""
    if not missing:
        return []
    selection = ",".join(str(pid) for pid in sorted(missing))
    code, output, error = _run(["/usr/sbin/lsof", "-nP", "-a", "-p", selection, "-F0pfn"])
    if code not in (0, 1) or error.strip():
        return [
            _issue(
                "process_visibility_incomplete",
                "Targeted process descriptor readback failed.",
            )
        ]
    try:
        busy.extend(_lsof(output, targets))
        unresolved = missing - _visible_pids(output)
        if not unresolved:
            return []
        code, output, error = _run(
            [
                "/bin/ps",
                "-p",
                ",".join(map(str, sorted(unresolved))),
                "-o",
                "pid=,uid=,stat=",
            ]
        )
        if code not in (0, 1) or error.strip():
            return [
                _issue(
                    "process_visibility_incomplete",
                    "Missing-process liveness readback failed.",
                )
            ]
        alive = set()
        for line in os.fsdecode(output).splitlines():
            columns = line.strip().split()
            if len(columns) != 3:
                raise ValueError("Missing-process readback lacked pid, uid or state.")
            pid = int(columns[0])
            if pid in unresolved and not columns[2].startswith("Z"):
                alive.add(pid)
        if alive:
            return [
                _issue(
                    "process_visibility_incomplete",
                    f"{len(alive)} live user processes lack descriptor visibility.",
                )
            ]
        return []
    except (ValueError, UnicodeError) as error:
        return [_issue("process_visibility_incomplete", str(error))]


def activity(paths: list[str], *, consumer_roots=(), owner_roots=()) -> dict:
    targets = list(dict.fromkeys(os.fspath(path) for path in [*paths, *owner_roots]))
    issues, busy = [], []
    if sys.platform != "darwin":
        issues.append(
            _issue(
                "process_visibility_unsupported",
                "This activity reader is qualified for macOS only.",
            )
        )
    if not targets or any(
        not path.startswith("/") or os.path.normpath(path) != path for path in targets
    ):
        issues.append(
            _issue(
                "invalid_activity_scope",
                "Activity targets must be normalized absolute paths.",
            )
        )
        return {
            "complete": False,
            "process_complete": False,
            "consumer_complete": False,
            "busy": [],
            "issues": issues,
        }
    issues.extend(_scope_ownership(targets))
    outputs = {}
    for arguments, parser, name in (
        (["/usr/sbin/lsof", "-nP", "-F0pfn"], _lsof, "lsof"),
        (["/bin/ps", "-axww", "-o", "pid=,uid=,command="], _ps, "ps"),
    ):
        code, stdout, stderr = _run(arguments)
        outputs[name] = stdout
        if code != 0 or stderr.strip() or not stdout.strip():
            issues.append(
                _issue(
                    "process_visibility_incomplete",
                    f"{name} could not provide complete visibility (exit {code}).",
                )
            )
        try:
            busy.extend(parser(stdout, targets))
        except (ValueError, UnicodeError) as error:
            issues.append(
                _issue(
                    "process_visibility_incomplete",
                    f"{name} output could not be read: {error}",
                )
            )
    try:
        visible_pids = _visible_pids(outputs["lsof"])
        expected_pids, foreign_pids = set(), set()
        for line in os.fsdecode(outputs["ps"]).splitlines():
            columns = line.strip().split(None, 2)
            if len(columns) != 3:
                continue
            pid = int(columns[0])
            sensor = columns[2].startswith("/bin/ps -axww -o pid=,uid=,command=")
            if pid > 0 and pid != os.getpid() and not sensor:
                if int(columns[1]) == os.geteuid():
                    expected_pids.add(pid)
                else:
                    foreign_pids.add(pid)
        missing = expected_pids - visible_pids
        issues.extend(_resolve_census_gaps(missing, targets, busy))
    except (ValueError, UnicodeError):
        foreign_pids, visible_pids = set(), set()
        issues.append(
            _issue(
                "process_visibility_incomplete",
                "Process census could not be joined to open-file records.",
            )
        )
    process_complete = not issues
    consumers, consumer_issues, inspected = _consumers(consumer_roots, targets)
    busy.extend(consumers)
    issues.extend(consumer_issues)
    unique = {json.dumps(row, sort_keys=True): row for row in busy}
    return {
        "complete": process_complete and not consumer_issues,
        "process_complete": process_complete,
        "consumer_complete": not consumer_issues,
        "consumer_scope": list(map(os.fspath, consumer_roots)),
        "consumer_metadata_inspected": inspected,
        "process_uid": os.geteuid(),
        "other_uid_open_files_unobserved": len(foreign_pids - visible_pids),
        "busy": list(unique.values()),
        "issues": issues,
        "limitations": [
            "Open-file completeness covers current-user processes and owned scopes; "
            "other users' arguments are checked; their descriptors may be hidden.",
            "Observes supplied static consumer scope; "
            "unresolved dynamic references are not executed.",
            "A negative observation does not reserve files against future consumers.",
        ],
    }
