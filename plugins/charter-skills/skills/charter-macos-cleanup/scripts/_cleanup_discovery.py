"""Bounded, passive candidate discovery. A candidate is not a deletion decision."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

from _cleanup_common import canonical_digest
from _cleanup_fs import FilesystemError, snapshot
from _cleanup_python import (
    evidence_preimages,
    evidence_unchanged,
    inventory_environment,
    issue,
    open_directory,
    read_metadata,
)

MAX_ENTRIES = 100_000
MAX_DEPTH = 24
MAX_ROOTS = 64
GUIDES = {"AGENTS.md", "AGENTS.override.md", "README.md", "CLAUDE.md"}
MANIFESTS = {
    "package.json",
    "pyproject.toml",
    "Cargo.toml",
    "Package.swift",
    "CMakeLists.txt",
    "requirements.txt",
    "setup.py",
    "setup.cfg",
    "Pipfile",
}
LOCKS = {
    "package-lock.json",
    "npm-shrinkwrap.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "bun.lock",
    "bun.lockb",
    "uv.lock",
    "poetry.lock",
    "Pipfile.lock",
    "Cargo.lock",
    "Package.resolved",
}
EXCLUDED_DIRS = {".git", ".hg", ".svn"}
OPAQUE_DIRS = {"node_modules", "site-packages", "vendor"}
RETAINED_PARTS = {
    ".git",
    "test-results",
    "test-results.json",
    "playwright-report",
    "evidence",
    "acceptance",
    "releases",
    "recovery",
    "snapshots",
    "__snapshots__",
}


def _absolute(raw: str) -> Path:
    if not isinstance(raw, str) or not raw or "\x00" in raw:
        raise ValueError("path must be a nonempty string")
    expanded = Path(os.path.expanduser(raw))
    if not expanded.is_absolute() or ".." in expanded.parts:
        raise ValueError("an absolute path without parent traversal is required")
    return expanded


def _inside(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def _context(path: Path, names: set[str], inherited: dict, issues: list[dict]) -> dict:
    evidence = sorted(names & (GUIDES | MANIFESTS | LOCKS))
    local = names & MANIFESTS
    evidence_issues = list(inherited.get("evidence_issues", []))
    preimages = inherited.get("evidence_preimages", []) + evidence_preimages(
        [str(path / name) for name in evidence], evidence_issues
    )
    context = {
        **inherited,
        "evidence_paths": sorted(
            set(inherited["evidence_paths"] + [str(path / name) for name in evidence])
        ),
        "evidence_preimages": preimages,
        "evidence_issues": evidence_issues,
    }
    if local or ".git" in names:
        context = {
            "owner_root": str(path),
            "owner_basis": "manifest" if local else "repository",
            "evidence_paths": context["evidence_paths"],
            "evidence_preimages": preimages,
            "evidence_issues": evidence_issues,
            "owner_issues": inherited.get("owner_issues", []),
            "manifests": sorted(local),
            "node_tools": [],
        }
        if "package.json" in names:
            try:
                package = json.loads(read_metadata(path / "package.json"))
                if not isinstance(package, dict):
                    raise ValueError("package.json must be an object")
                context["node_tools"] = sorted(
                    set(package.get("dependencies", {})) | set(package.get("devDependencies", {}))
                )
                context["scripts"] = {
                    name: command
                    for name, command in package.get("scripts", {}).items()
                    if name in {"build", "clean"} and isinstance(command, str)
                }
            except (OSError, ValueError, TypeError, AttributeError) as exc:
                issues.append(issue("manifest_unreadable", path / "package.json", str(exc)))
                evidence_issues.append(
                    issue("manifest_unreadable", path / "package.json", str(exc))
                )
    return context


def _recognize(
    path: Path, context: dict, names: set[str], include_caches: bool
) -> tuple[str, str] | None:
    name = path.name
    manifests = context.get("manifests", [])
    owner_child = path.parent == Path(context["owner_root"])
    if name == "node_modules" and owner_child and "package.json" in manifests:
        return (
            "dependencies",
            "package.json identifies JavaScript dependencies; select the package manager and lock before qualification",
        )
    if owner_child and name == "target" and "Cargo.toml" in manifests:
        return (
            "build_output",
            "Cargo manifest found; inspect retained artifacts and the selected build/profile",
        )
    if owner_child and name == ".build" and "Package.swift" in manifests:
        return (
            "build_output",
            "Swift package manifest found; inspect accepted binaries and test evidence",
        )
    tools = context.get("node_tools", [])
    if owner_child and (
        (name == ".next" and "next" in tools) or (name == "dist" and "vite" in tools)
    ):
        return (
            "build_output",
            "build-tool manifest relationship found; confirm output configuration and retained contents",
        )
    if name == "__pycache__":
        return (
            "python_cache",
            "Python bytecode cache; preserve source inputs and check current consumers",
        )
    if include_caches and name in {".pytest_cache", ".mypy_cache", ".ruff_cache"}:
        return "python_cache", "tool cache name observed; confirm owner and retained contents"
    if include_caches and name == "_cacache" and path.parent.name == ".npm":
        return (
            "download_cache",
            "npm content cache; use the qualified native owner route, not direct store editing",
        )
    if (
        include_caches
        and path.suffix.lower() in {".tgz", ".zip", ".dmg", ".pkg"}
        and path.parent.name.lower() in {"downloads", "download-cache"}
    ):
        return (
            "download_cache",
            "archive under a download-cache seed; establish a redownload route and distinguish retained originals",
        )
    return None


def _protected(candidate: dict) -> str | None:
    path = Path(candidate["path"])
    if any(part in RETAINED_PARTS for part in path.parts):
        return "candidate is within retained evidence, recovery, release or Git material"
    if candidate["category"] == "download_cache" and path.name == "_cacache":
        return "package-manager store requires its qualified native owner route"
    for entry in candidate["snapshot"].get("entries", []):
        relative = Path(entry.get("relative_path", ""))
        if any(part in RETAINED_PARTS or part.endswith(".xcresult") for part in relative.parts):
            return (
                "mixed parent contains retained-purpose material; select qualified children instead"
            )
        if relative.name in {"AGENTS.md", "AGENTS.override.md"}:
            return "nested project guidance must be read; split or qualify a narrower output"
    return None


class _Discovery:
    def __init__(
        self,
        roots: list[str],
        candidates: list[str],
        include_caches: bool,
        project_roots: list[str],
    ):
        self.raw_roots = roots
        self.requested = candidates
        self.requested_projects = project_roots
        self.include_caches = include_caches
        self.roots: list[Path] = []
        self.explicit: set[Path] = set()
        self.seen_explicit: set[Path] = set()
        self.project_roots: dict[Path, tuple[int, int]] = {}
        self.seen_projects: set[Path] = set()
        self.candidates: list[dict] = []
        self.issues: list[dict] = []
        self.excluded: list[dict] = []
        self.inspected_roots: list[str] = []
        self.remaining = MAX_ENTRIES
        self.visited = 0
        self.complete = True

    def problem(self, code: str, path: Path | str, detail: str) -> None:
        self.issues.append(issue(code, path, detail))
        self.complete = False

    def prepare(self) -> None:
        if len(self.raw_roots) > MAX_ROOTS:
            self.problem("root_limit", "", f"at most {MAX_ROOTS} roots can be inspected")
        for raw in self.raw_roots[:MAX_ROOTS]:
            try:
                root = _absolute(raw)
                if any(_inside(root, existing) for existing in self.roots):
                    continue
                self.roots = [existing for existing in self.roots if not _inside(existing, root)]
                self.roots.append(root)
            except (OSError, ValueError) as exc:
                self.problem("invalid_root", raw, str(exc))
        for raw in self.requested_projects:
            try:
                path = _absolute(raw)
                if str(path).startswith("//") or not any(
                    _inside(path, root) for root in self.roots
                ):
                    raise ValueError("project root must be canonical and within an inspected root")
                if any(part in EXCLUDED_DIRS or part.endswith(".app") for part in path.parts):
                    raise ValueError(
                        "repository metadata and installed applications cannot be declared projects"
                    )
                if path in self.project_roots:
                    continue
                if any(
                    _inside(path, other) or _inside(other, path) for other in self.project_roots
                ):
                    raise ValueError("distinct declared project roots must not overlap")
                fd = open_directory(path)
                try:
                    info = os.fstat(fd)
                    self.project_roots[path] = (info.st_dev, info.st_ino)
                finally:
                    os.close(fd)
            except (OSError, ValueError) as exc:
                self.problem("invalid_project_root", raw, str(exc))
        for raw in self.requested:
            try:
                path = _absolute(raw)
                if not any(_inside(path, root) and path != root for root in self.roots):
                    raise ValueError("explicit candidate must be below an inspected root")
                if any(part in EXCLUDED_DIRS for part in path.parts):
                    raise ValueError("Git and other repository metadata are excluded")
                if any(_inside(path, other) or _inside(other, path) for other in self.explicit):
                    raise ValueError("explicit candidate paths must not overlap")
                self.explicit.add(path)
            except (OSError, ValueError) as exc:
                self.problem("invalid_candidate_path", raw, str(exc))

    def project_context(self, path: Path, fd: int, context: dict) -> dict:
        if path not in self.project_roots:
            return context
        self.seen_projects.add(path)
        current = os.fstat(fd)
        conflict = None
        if self.project_roots[path] != (current.st_dev, current.st_ino):
            conflict = "declared project directory changed after validation"
        elif context["owner_root"] != str(path) and context["owner_basis"] in {
            "manifest",
            "repository",
            "declared",
        }:
            conflict = f"declaration would narrow established {context['owner_basis']} owner {context['owner_root']}"
        if conflict:
            problem = issue("project_boundary_conflict", path, conflict)
            self.issues.append(problem)
            self.complete = False
            return {**context, "owner_issues": context.get("owner_issues", []) + [problem]}
        if context["owner_basis"] in {"manifest", "repository"}:
            return context
        return {**context, "owner_root": str(path), "owner_basis": "declared"}

    def add_candidate(self, path: Path, category: str, hint: str, context: dict) -> None:
        try:
            extra = {}
            if category == "venv_payload":
                extra = inventory_environment(path, Path(context["owner_root"]))
                observed = extra.pop("snapshot")
            else:
                observed = snapshot(str(path))
            candidate = {
                "kind": "filesystem",
                "category": category,
                "path": str(path),
                "owner_root": context["owner_root"],
                "owner_basis": context["owner_basis"],
                "snapshot": observed,
                "scopes": [{"kind": "path", "path": str(path)}],
                "evidence_paths": context["evidence_paths"],
                "reconstruction_hints": [hint],
                **extra,
            }
            candidate["evidence_paths"] = sorted(
                set(context["evidence_paths"] + extra.get("evidence_paths", []))
            )
            preimages = context.get("evidence_preimages", []) + extra.get("evidence_preimages", [])
            preimage_issues = list(context.get("evidence_issues", []))
            evidence_unchanged(preimages, preimage_issues)
            candidate["evidence_preimages"] = list({row["path"]: row for row in preimages}.values())
            if preimage_issues:
                observed["complete"] = False
                candidate["evidence_issues"] = preimage_issues
            if category == "venv_payload":
                candidate["scopes"] = [
                    {"kind": "path", "path": row["path"]} for row in candidate["payload_files"]
                ]
            reason = _protected(candidate)
            if context.get("owner_issues"):
                candidate["owner_issues"] = context["owner_issues"]
                reason = (
                    "declared ownership conflicts with an established owner; inspect owner_issues"
                )
            if any(_inside(project, path) for project in self.project_roots):
                reason = "candidate reaches a declared project root; select output below its owner"
            if not observed.get("complete"):
                reason = (
                    reason or "candidate inventory or snapshot is incomplete; inspect its issues"
                )
                self.problem("candidate_incomplete", path, reason)
            if reason:
                candidate["retained_reason"] = reason
            candidate["id"] = (
                "fs-"
                + canonical_digest({"path": str(path), "snapshot": observed}).removeprefix(
                    "sha256:"
                )[:24]
            )
            self.candidates.append(candidate)
        except (OSError, ValueError, FilesystemError) as exc:
            self.problem("candidate_unreadable", path, str(exc))

    def walk(self, path: Path, fd: int, device: int, depth: int, context: dict) -> None:
        if depth > MAX_DEPTH or self.remaining <= 0:
            self.problem(
                "discovery_limit", path, "uninspected subtree: depth or entry budget exhausted"
            )
            return
        try:
            before = os.fstat(fd)
            entries = []
            with os.scandir(fd) as scan:
                for entry in scan:
                    self.remaining -= 1
                    self.visited += 1
                    if self.remaining < 0:
                        self.problem(
                            "discovery_entry_limit", path, "directory is only partially inspected"
                        )
                        break
                    entries.append((entry.name, entry.stat(follow_symlinks=False)))
            names = {name for name, _ in entries}
            context = _context(path, names, context, self.issues)
            context = self.project_context(path, fd, context)
            if "pyvenv.cfg" in names:
                self.add_candidate(
                    path,
                    "venv_payload",
                    "distribution inventory only; preserve the environment skeleton and select a synchronization recipe",
                    context,
                )
                self.seen_explicit.add(path)
                return
            for name, info in sorted(entries):
                child = path / name
                if name in EXCLUDED_DIRS or name.endswith(".app"):
                    self.excluded.append(
                        issue(
                            "owner_boundary",
                            child,
                            "repository metadata or installed application is not traversed",
                        )
                    )
                    continue
                if stat.S_ISLNK(info.st_mode):
                    self.excluded.append(
                        issue(
                            "symlink_not_followed",
                            child,
                            "resolve an explicit actual target in a separate scope",
                        )
                    )
                    continue
                if info.st_dev != device:
                    self.problem(
                        "mount_boundary", child, "not traversed; select that filesystem explicitly"
                    )
                    continue
                recognized = _recognize(child, context, names, self.include_caches)
                explicit = child in self.explicit
                nested_explicit = any(child in candidate.parents for candidate in self.explicit)
                if explicit or (recognized and not nested_explicit):
                    if not stat.S_ISDIR(info.st_mode) and not stat.S_ISREG(info.st_mode):
                        self.problem(
                            "unsupported_candidate_type",
                            child,
                            "candidate is not a regular file or directory",
                        )
                        continue
                    category, hint = recognized or (
                        "build_output",
                        "caller-declared output; its name does not establish reconstructibility or retention",
                    )
                    # Venv roots must be inventoried, never treated as generic subtrees.
                    if stat.S_ISDIR(info.st_mode):
                        child_fd = os.open(
                            name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
                        )
                        try:
                            if "pyvenv.cfg" in os.listdir(child_fd):
                                category = "venv_payload"
                        finally:
                            os.close(child_fd)
                    self.add_candidate(child, category, hint, context)
                    self.seen_explicit.add(child)
                    continue
                if stat.S_ISDIR(info.st_mode):
                    if name in OPAQUE_DIRS and not nested_explicit:
                        self.excluded.append(
                            issue(
                                "unqualified_dependency_tree",
                                child,
                                "contents not traversed; owner manifest or explicit candidate is required",
                            )
                        )
                        continue
                    child_fd = os.open(
                        name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd
                    )
                    try:
                        opened = os.fstat(child_fd)
                        if (opened.st_dev, opened.st_ino) != (info.st_dev, info.st_ino):
                            raise ValueError("directory changed while opening")
                        self.walk(child, child_fd, device, depth + 1, context)
                    finally:
                        os.close(child_fd)
            after = os.fstat(fd)
            if (before.st_mtime_ns, before.st_ctime_ns) != (after.st_mtime_ns, after.st_ctime_ns):
                self.problem(
                    "directory_changed", path, "directory metadata changed during discovery"
                )
        except (OSError, ValueError) as exc:
            self.problem("directory_unreadable", path, str(exc))

    def run(self) -> dict:
        self.prepare()
        for root in sorted(self.roots):
            try:
                fd = open_directory(root)
                try:
                    self.inspected_roots.append(str(root))
                    self.walk(
                        root,
                        fd,
                        os.fstat(fd).st_dev,
                        0,
                        {
                            "owner_root": str(root),
                            "owner_basis": "scan_root",
                            "evidence_paths": [],
                            "manifests": [],
                            "node_tools": [],
                        },
                    )
                finally:
                    os.close(fd)
            except (OSError, ValueError) as exc:
                self.problem("root_unreadable", root, str(exc))
        for path in sorted(self.explicit - self.seen_explicit):
            self.problem(
                "candidate_not_inspected",
                path,
                "not found or behind an excluded/uninspected boundary",
            )
        for path in sorted(self.project_roots.keys() - self.seen_projects):
            self.problem(
                "project_root_not_inspected",
                path,
                "declaration is behind an excluded, candidate or uninspected boundary",
            )
        return {
            "candidates": sorted(self.candidates, key=lambda row: row["path"]),
            "coverage": {
                "complete": self.complete and not self.issues,
                "requested_roots": self.raw_roots,
                "inspected_roots": self.inspected_roots,
                "requested_project_roots": self.requested_projects,
                "inspected_project_roots": [str(path) for path in sorted(self.seen_projects)],
                "metadata_entries": self.visited,
                "limits": {"entries": MAX_ENTRIES, "depth": MAX_DEPTH, "roots": MAX_ROOTS},
                "excluded": self.excluded,
            },
            "issues": self.issues,
        }


def discover(
    roots: list[str],
    candidate_paths: list[str] | None = None,
    include_caches: bool = False,
    project_roots: list[str] | None = None,
) -> dict:
    return _Discovery(roots, candidate_paths or [], include_caches, project_roots or []).run()
