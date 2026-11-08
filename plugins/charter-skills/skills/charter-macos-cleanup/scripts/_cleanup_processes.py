"""Read-only process and bounded installed-consumer observations.

Metadata is read as bytes, never imported or evaluated. Completeness describes
the supplied consumer scope, not every possible dynamic reference on the Mac.
"""

from __future__ import annotations

import ast
import hashlib
import json
import os
import plistlib
import shlex
import stat
import subprocess
import sys
from bisect import bisect_left
from pathlib import Path
from urllib.parse import unquote, urlparse

from _cleanup_fs import _DIRECTORY_FLAGS, _parent, _removal_names

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
_MAX_METADATA_BYTES = 1024 * 1024
MAX_CONSUMER_METADATA = 20000


class _MetadataLimit(ValueError):
    """A real metadata read, rather than directory discovery, hit its bound."""


# These are syntax fingerprints of generated distutils shims, not tool-version
# or filename admission rules. The complete referenced source must match; only
# comments, formatting and docstrings are ignored. An altered/unknown hook is
# unresolved, even under a familiar filename. Sources:
# astral-sh/uv: crates/uv-virtualenv/src/_virtualenv.py (0.12.23, 0.13.4)
# and the earlier distutils-only template observed in this project's environment.
# pypa/setuptools: _distutils_hack/__init__.py (80.9.0)
_GENERATED_MODULES = {
    "8539fc3ceec96d14170b77004c60e04ee9032875b50c69f17e90f60a55e0d519": "virtualenv",
    "7801fa5c5161c003fb923d66d132b10a8b0db1d36a4df6ff19b9348f2870667a": "virtualenv",
    "0a5f2c37997a7e95ec1143e1f71392e35705c3a6343fb8b1b5ea1756142866e2": "distutils",
}
_DISTUTILS_HOOK = (
    "import os; var = 'SETUPTOOLS_USE_DISTUTILS'; "
    "enabled = os.environ.get(var, 'local') == 'local'; "
    "enabled and __import__('_distutils_hack').add_shim()"
)


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


def _syntax_digest(tree):
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
            and node.body
            and isinstance(node.body[0], ast.Expr)
            and isinstance(node.body[0].value, ast.Constant)
            and isinstance(node.body[0].value.value, str)
        ):
            node.body.pop(0)

    def shape(value):
        if isinstance(value, ast.AST):
            # ast.dump's omission of empty fields changed between supported
            # Python releases. Empty generic parameters also appeared in 3.12.
            return [
                type(value).__name__,
                [
                    [name, shape(item)]
                    for name, item in ast.iter_fields(value)
                    if name != "type_params" or item
                ],
            ]
        if isinstance(value, list):
            return [shape(item) for item in value]
        return [type(value).__name__, repr(value)]

    return hashlib.sha256(json.dumps(shape(tree), separators=(",", ":")).encode()).hexdigest()


def _literal_references(tree):
    for node in ast.walk(tree):
        if not isinstance(node, ast.Constant) or not isinstance(node.value, str):
            continue
        value = node.value
        if value.startswith("/"):
            yield os.path.normpath(value)
        elif value.startswith("file://"):
            parsed = urlparse(value)
            if parsed.netloc in ("", "localhost"):
                yield os.path.normpath(unquote(parsed.path))


def _direct_url_values(content):
    """Distinguish installation provenance from an editable runtime source link.

    PyPA direct-url data structure: archive_info and vcs_info record provenance;
    dir_info.editable defaults to false. Unknown shapes are not a negative
    consumer observation. The caller binds and revalidates this metadata even
    when the recognized origin emits no runtime reference.
    """

    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError("Ambiguous direct_url.json contains duplicate fields.")
            result[key] = value
        return result

    try:
        data = json.loads(content, object_pairs_hook=unique_object)
    except RecursionError as error:
        raise ValueError("direct_url.json nesting exceeds interpretable metadata.") from error
    if not isinstance(data, dict) or not isinstance(data.get("url"), str):
        raise ValueError("direct_url.json must be an object with a URL string.")
    if set(data) - {"url", "archive_info", "dir_info", "vcs_info", "subdirectory"} or (
        "subdirectory" in data and not isinstance(data["subdirectory"], str)
    ):
        raise ValueError("direct_url.json contains unknown or malformed fields.")
    url = data["url"]
    parsed = urlparse(url)
    if not parsed.scheme or not (parsed.netloc or parsed.path) or any(ord(c) < 32 for c in url):
        raise ValueError("direct_url.json URL is malformed.")
    origins = {key for key in ("archive_info", "dir_info", "vcs_info") if key in data}
    if len(origins) != 1:
        raise ValueError("direct_url.json origin is missing or ambiguous.")
    origin = origins.pop()
    info = data[origin]
    if not isinstance(info, dict):
        raise ValueError("direct_url.json origin information must be an object.")
    if origin == "vcs_info":
        if (
            set(info) - {"vcs", "commit_id", "requested_revision", "resolved_revision"}
            or not isinstance(info.get("vcs"), str)
            or info.get("vcs") not in {"git", "hg", "bzr", "svn"}
            or not isinstance(info.get("commit_id"), str)
            or not info["commit_id"]
            or any(
                key in info and not isinstance(info[key], str)
                for key in ("requested_revision", "resolved_revision")
            )
        ):
            raise ValueError("direct_url.json VCS information is malformed or unknown.")
        return []
    if origin == "archive_info":
        if (
            set(info) - {"hash", "hashes"}
            or "hash" in info
            and not isinstance(info["hash"], str)
            or "hashes" in info
            and (
                not isinstance(info["hashes"], dict)
                or not all(isinstance(value, str) for value in info["hashes"].values())
            )
        ):
            raise ValueError("direct_url.json archive information is malformed or unknown.")
        return []
    editable = info.get("editable", False)
    if set(info) - {"editable"} or type(editable) is not bool:
        raise ValueError("direct_url.json editable state is malformed or unknown.")
    if (
        parsed.scheme != "file"
        or parsed.netloc not in ("", "localhost")
        or not parsed.path.startswith("/")
    ):
        raise ValueError("direct_url.json directory URL is not an observable local absolute path.")
    return [unquote(parsed.path)] if editable else []


def _references(path, content):
    """Return static path strings, never execute .pth, shebangs or configuration."""
    if path.name == "direct_url.json":
        yield from _direct_url_values(content)
        return
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


def _metadata_signature(value):
    return [
        value.st_dev,
        value.st_ino,
        value.st_mode,
        value.st_size,
        value.st_mtime_ns,
        value.st_ctime_ns,
    ]


def _ancestor_digest(ancestors):
    return hashlib.sha256(json.dumps(ancestors, sort_keys=True).encode()).hexdigest()


def _metadata_read(path, bindings, observed=None):
    """Read and bind a real file and its ancestors, without invoking its loader."""
    key = str(path)
    if key in bindings:
        return bindings[key]["content"]
    if len(bindings) >= MAX_CONSUMER_METADATA:
        raise _MetadataLimit("Referenced metadata exceeds bounded coverage.")
    parent_fd, name, ancestors = _parent(key)
    try:
        before = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if not stat.S_ISREG(before.st_mode) or before.st_size > _MAX_METADATA_BYTES:
            raise ValueError("Referenced metadata is not a bounded regular file.")
        if observed is not None and _metadata_signature(before) != _metadata_signature(observed):
            raise OSError("Consumer metadata changed before opening.")
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent_fd)
        try:
            opened = os.fstat(fd)
            with os.fdopen(fd, "rb", closefd=False) as stream:
                content = stream.read(_MAX_METADATA_BYTES + 1)
            after = os.fstat(fd)
        finally:
            os.close(fd)
        if (
            _metadata_signature(before) != _metadata_signature(opened)
            or _metadata_signature(opened) != _metadata_signature(after)
            or len(content) != after.st_size
        ):
            raise OSError("Consumer metadata changed while reading.")
    finally:
        os.close(parent_fd)
    bindings[key] = {
        "content": content,
        "evidence": {
            "path": key,
            "signature": _metadata_signature(after),
            "ancestor_sha256": _ancestor_digest(ancestors),
            "sha256": hashlib.sha256(content).hexdigest(),
        },
    }
    return content


def _verify_metadata(bindings, issues):
    for record in bindings.values():
        evidence = record["evidence"]
        try:
            fd, name, ancestors = _parent(evidence["path"])
            try:
                fresh = os.stat(name, dir_fd=fd, follow_symlinks=False)
            finally:
                os.close(fd)
            if (
                _metadata_signature(fresh) != evidence["signature"]
                or _ancestor_digest(ancestors) != evidence["ancestor_sha256"]
            ):
                raise OSError("Metadata identity or ancestors changed after reading.")
        except OSError as error:
            issues.append(_issue("consumer_metadata_changed", f"{evidence['path']}: {error}"))


def _local_module(path, name):
    """Resolve only an unambiguous adjacent source module; never ask importlib."""
    if not name.isidentifier():
        return None
    candidates = [path.parent / f"{name}.py", path.parent / name / "__init__.py"]
    present = [candidate for candidate in candidates if os.path.lexists(candidate)]
    alternatives = [*path.parent.glob(f"{name}.*"), *path.parent.glob(f"{name}/__init__.*")]
    if len(present) != 1 or any(
        candidate.suffix in {".so", ".pyd", ".pyc"} for candidate in alternatives
    ):
        return None
    return present[0]


def _static_path_hook(tree):
    """Recognize literal sys.path insertion, not arbitrary code around it."""
    if not tree.body or ast.dump(tree.body[0]) != ast.dump(ast.Import([ast.alias("sys")])):
        return False
    for node in tree.body[1:]:
        if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
            return False
        call = node.value
        if not isinstance(call.func, ast.Attribute) or call.keywords:
            return False
        if ast.dump(call.func.value) != ast.dump(ast.parse("sys.path", mode="eval").body):
            return False
        arguments = call.args
        if call.func.attr == "insert" and len(arguments) == 2:
            if not isinstance(arguments[0], ast.Constant) or type(arguments[0].value) is not int:
                return False
            arguments = arguments[1:]
        elif call.func.attr != "append" or len(arguments) != 1:
            return False
        if not isinstance(arguments[0], ast.Constant) or not isinstance(arguments[0].value, str):
            return False
        if not arguments[0].value.startswith("/"):
            return False  # Relative paths depend on the consumer's working directory.
    return True


def _hook_references(path, line, bindings):
    """Interpret bounded syntax and recognized generated source, never execute it."""
    try:
        tree = ast.parse(line)
        references = list(_literal_references(tree))
        if _static_path_hook(tree):
            return references, True
        expected, generated_name = None, None
        if _syntax_digest(tree) == _syntax_digest(ast.parse(_DISTUTILS_HOOK)):
            generated_name, expected = "_distutils_hack", "distutils"
        elif (
            len(tree.body) == 1
            and isinstance(tree.body[0], ast.Import)
            and len(tree.body[0].names) == 1
            and tree.body[0].names[0].asname is None
        ):
            generated_name, expected = tree.body[0].names[0].name, "virtualenv"
        names = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, ast.Import)
            for alias in node.names
        }
        if generated_name:
            names.add(generated_name)
        qualified = False
        for name in sorted(names):
            module = _local_module(path, name)
            if module is None:
                continue
            references.append(str(module))
            if module.is_symlink():
                continue  # A source/cache link is a dependency, not trusted source.
            content = _metadata_read(module, bindings)
            source = ast.parse(content.decode("utf-8"))
            references.extend(_literal_references(source))
            if name == generated_name and expected:
                qualified = _GENERATED_MODULES.get(_syntax_digest(source)) == expected
        return references, qualified
    except (SyntaxError, RecursionError):
        return [], False


def _removal_scope(snapshot, targets):
    if snapshot is None:
        return None
    anchor = snapshot.get("path")
    if not snapshot.get("complete") or anchor not in targets:
        raise ValueError("Removal snapshot must be complete and anchored at an activity target.")
    names = _removal_names(snapshot)
    paths = {str(Path(anchor) / name) if name else anchor for name in names}
    return {"anchor": anchor, "paths": paths, "sorted_paths": sorted(paths)}


def _removal_reference(reference, removal):
    """Match removed objects, including a retained search directory containing them."""
    if not _related(reference, removal["anchor"]):
        return False
    selected = removal["paths"]
    path = reference
    while _related(path, removal["anchor"]):
        if path in selected:
            return True
        path = os.path.dirname(path)
    prefix = reference.rstrip("/") + "/"
    position = bisect_left(removal["sorted_paths"], prefix)
    return position < len(removal["sorted_paths"]) and removal["sorted_paths"][position].startswith(
        prefix
    )


def _consumer_files(roots, issues, *, removal=None, coverage=None):
    """Stream every real entry; only actual metadata reads have a count bound."""
    records = []
    if coverage is not None:
        coverage.update(requested_roots=list(map(os.fspath, roots)), roots=records)
    admitted = {}
    for root_text in sorted(
        set(map(os.fspath, roots)), key=lambda path: (len(Path(path).parts), path)
    ):
        covering = next(
            (
                parent
                for parent, observed in admitted.items()
                if observed["state"] in {"complete", "selected_removal"}
                and _related(root_text, parent)
            ),
            None,
        )
        record = {
            "path": root_text,
            "state": "covered" if covering else "complete",
            "entries_visited": 0,
            "directories_inspected": 0,
            "removed_origins_excluded": 0,
            "metadata_omitted": 0,
        }
        records.append(record)
        if covering:
            record["covered_by"] = covering
            continue
        admitted[root_text] = record
        root = Path(root_text)
        try:
            parent_fd, name, _ = _parent(str(root))
            try:
                initial = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            finally:
                os.close(parent_fd)
            record["entries_visited"] += 1
            if removal and root_text in removal["paths"]:
                record["removed_origins_excluded"] += 1
                record["state"] = "selected_removal"
                continue
            if stat.S_ISLNK(initial.st_mode) or stat.S_ISREG(initial.st_mode):
                yield root, initial, record
                continue
            if not stat.S_ISDIR(initial.st_mode):
                record["state"] = "incomplete"
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
                    record["directories_inspected"] += 1
                    if before.st_dev != initial.st_dev:
                        record["state"] = "incomplete"
                        issues.append(
                            _issue(
                                "consumer_scope_changed",
                                f"Consumer directory crosses a filesystem: {parent}",
                            )
                        )
                        continue
                    with os.scandir(directory_fd) as children:
                        for child in children:
                            record["entries_visited"] += 1
                            entry = child.stat(follow_symlinks=False)
                            candidate = parent / child.name
                            if entry.st_dev != initial.st_dev:
                                record["state"] = "incomplete"
                                issues.append(
                                    _issue(
                                        "consumer_device_boundary",
                                        f"Skipped filesystem boundary: {candidate}",
                                    )
                                )
                            elif removal and str(candidate) in removal["paths"]:
                                record["removed_origins_excluded"] += 1
                            elif stat.S_ISDIR(entry.st_mode):
                                pending.append(candidate)
                            elif stat.S_ISLNK(entry.st_mode) or stat.S_ISREG(entry.st_mode):
                                yield candidate, entry, record
                    after = os.fstat(directory_fd)
                    if (before.st_dev, before.st_ino, before.st_mtime_ns) != (
                        after.st_dev,
                        after.st_ino,
                        after.st_mtime_ns,
                    ):
                        record["state"] = "incomplete"
                        issues.append(
                            _issue(
                                "consumer_scope_changed",
                                f"Consumer directory changed while inspected: {parent}",
                            )
                        )
                finally:
                    os.close(directory_fd)
        except OSError as error:
            record["state"] = "incomplete"
            issues.append(_issue("consumer_scope_unreadable", f"{root}: {error}"))


def _matching_targets(path, reference, targets, owner_roots, removal):
    references = {reference, os.path.realpath(reference)}
    matched = set()
    for target in targets:
        if any(
            _removal_reference(value, removal)
            if removal and target == removal["anchor"]
            else _related(value, target)
            for value in references
        ):
            matched.add(target)
    # A launcher outside this owner may load its source lazily. A normal
    # in-owner link is not an installed consumer merely because it resolves
    # elsewhere in that same project. References to actual removal remain above.
    for owner in owner_roots:
        if not _related(str(path), owner) and any(_related(value, owner) for value in references):
            matched.add(owner)
    return matched


def _consumers(roots, targets, *, metadata=None, owner_roots=(), removal=None, coverage=None):
    busy, issues, inspected = [], [], 0
    bindings = {}
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
    scope = {} if coverage is None else coverage
    for path, observed, record in _consumer_files(roots, issues, removal=removal, coverage=scope):
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
                script = (
                    observed.st_mode & 0o111
                    and path.name not in _METADATA_NAMES
                    and path.suffix not in _METADATA_SUFFIXES
                )
                # Executable binaries are not metadata; inspect only their prefix
                # instead of binding/reading every installed program in full.
                if script:
                    parent_fd, name, _ = _parent(str(path))
                    try:
                        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=parent_fd)
                        try:
                            if os.read(fd, 2) != b"#!":
                                continue
                        finally:
                            os.close(fd)
                    finally:
                        os.close(parent_fd)
                content = _metadata_read(path, bindings, observed)
                if script:
                    kind = "installed_shebang"
                references = list(_references(path, content))
                if path.suffix == ".pth":
                    for line in content.decode("utf-8").splitlines():
                        if not line.lstrip().startswith(("import ", "import\t")):
                            continue
                        extra, qualified = _hook_references(path, line.strip(), bindings)
                        references.extend(extra)
                        if not qualified:
                            issues.append(
                                _issue(
                                    "dynamic_consumer_reference",
                                    f"Unresolved executable .pth content was not evaluated: {path}",
                                )
                            )
                        else:
                            bindings[str(path)].setdefault("qualified_hooks", 0)
                            bindings[str(path)]["qualified_hooks"] += 1
            else:
                continue
            inspected += 1
            for reference in references:
                for target in sorted(
                    _matching_targets(path, reference, targets, owner_roots, removal)
                ):
                    busy.append(
                        {
                            "path": target,
                            "kind": kind,
                            "consumer": str(path),
                            "reference": reference,
                        }
                    )
        except _MetadataLimit:
            record["state"] = "incomplete"
            record["metadata_omitted"] += 1
        except (
            OSError,
            ValueError,
            UnicodeError,
            plistlib.InvalidFileException,
        ) as error:
            record["state"] = "incomplete"
            issues.append(_issue("consumer_metadata_unreadable", f"{path}: {error}"))
    for record in scope.get("roots", []):
        if record["metadata_omitted"]:
            issues.append(
                _issue(
                    "consumer_scope_incomplete",
                    f"Metadata binding limit {MAX_CONSUMER_METADATA} reached; "
                    f"{record['metadata_omitted']} entries not fully inspected in {record['path']}.",
                )
            )
    _verify_metadata(bindings, issues)
    scope.update(
        complete=not issues,
        metadata_binding_limit=MAX_CONSUMER_METADATA,
        metadata_bindings=len(bindings),
        metadata_entries_inspected=inspected,
    )
    if metadata is not None:
        metadata.extend(
            dict(record["evidence"], qualified_hooks=record.get("qualified_hooks", 0))
            for record in bindings.values()
        )
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


def activity(paths: list[str], *, consumer_roots=(), owner_roots=(), removal_snapshot=None) -> dict:
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
    metadata = []
    consumer_coverage = {}
    removal = None
    removal_issues = []
    try:
        removal = _removal_scope(removal_snapshot, paths)
    except (KeyError, TypeError, ValueError) as error:
        removal_issues.append(_issue("invalid_removal_scope", str(error)))
    consumers, consumer_issues, inspected = _consumers(
        consumer_roots,
        paths,
        metadata=metadata,
        owner_roots=owner_roots,
        removal=removal,
        coverage=consumer_coverage,
    )
    consumer_issues.extend(removal_issues)
    consumer_coverage["complete"] = not consumer_issues
    busy.extend(consumers)
    issues.extend(consumer_issues)
    unique = {json.dumps(row, sort_keys=True): row for row in busy}
    return {
        "complete": not issues,
        "process_complete": process_complete,
        "consumer_complete": not consumer_issues,
        "consumer_scope": list(map(os.fspath, consumer_roots)),
        "consumer_metadata_inspected": inspected,
        "consumer_metadata": metadata,
        "consumer_coverage": consumer_coverage,
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
