"""Regular-file observations and exclusive report destinations, not mutation plans."""

from __future__ import annotations

import os
from pathlib import Path
import stat


def scan_tree(root: Path) -> tuple[list[Path], list[dict[str, str]]]:
    """Read a quiescent tree without traversing symlinks.

    Symlinks and special nodes are reported as excluded rows. A directory or
    entry that cannot be read becomes an ``unreadable`` row carrying its error,
    and the scan continues, so the caller can emit a partial report.
    """
    root = root.resolve(strict=True)
    if not root.is_dir():
        raise NotADirectoryError(root)
    files: list[Path] = []
    excluded: list[dict[str, str]] = []

    def record_unreadable(path: Path, error: OSError) -> None:
        excluded.append(unreadable_row(root, path, error))

    def on_walk_error(error: OSError) -> None:
        record_unreadable(Path(error.filename) if error.filename else root, error)

    for directory, dirs, names in os.walk(root, followlinks=False, onerror=on_walk_error):
        parent = Path(directory)
        for name in sorted(dirs + names):
            path = parent / name
            try:
                mode = path.lstat().st_mode
            except OSError as error:
                record_unreadable(path, error)
                if name in dirs:
                    dirs.remove(name)
                continue
            if stat.S_ISLNK(mode) or not (
                stat.S_ISDIR(mode) or stat.S_ISREG(mode)
            ):
                excluded.append({
                    "path": relative_path(root, path),
                    "kind": "symlink" if stat.S_ISLNK(mode) else "special",
                })
                if name in dirs:
                    dirs.remove(name)
            elif stat.S_ISREG(mode):
                files.append(path)
        dirs.sort()
    return sorted(files), sorted(excluded, key=lambda row: row["path"])


def relative_path(root: Path, path: Path) -> str:
    """Return a root-relative path string, "." for the root itself."""
    return str(Path(path).relative_to(root))


def unreadable_row(
    root: Path, path: Path, error: OSError | ValueError, kind: str = "unreadable",
) -> dict[str, str]:
    """Describe a path whose observation failed, keeping the reason."""
    reason = getattr(error, "strerror", None) or str(error)
    return {
        "path": relative_path(root, path),
        "kind": kind,
        "error": f"{type(error).__name__}: {reason}",
    }


def split_unreadable(
    excluded: list[dict[str, str]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Separate deliberate exclusions from paths the scan could not read."""
    unreadable = [row for row in excluded if row["kind"] == "unreadable"]
    return [row for row in excluded if row["kind"] != "unreadable"], unreadable


def file_identity(info: os.stat_result) -> dict[str, int]:
    """Describe one observed regular file, without promising future identity."""
    return {
        "device": info.st_dev, "inode": info.st_ino, "size": info.st_size,
        "mtime_ns": info.st_mtime_ns, "ctime_ns": info.st_ctime_ns,
    }


def report_path(root: Path, output: Path) -> Path:
    """Select a new report path outside the source tree; do not create it."""
    output = output.expanduser().absolute()
    parent = output.parent.resolve(strict=True)
    target = parent / output.name
    if target.is_relative_to(root.resolve(strict=True)):
        raise ValueError("report output must be outside the archive root")
    if target.exists() or target.is_symlink():
        raise FileExistsError(target)
    return target


def write_report(root: Path, output: Path, text: str) -> None:
    """Exclusively create an output, preserving any existing path."""
    target = report_path(root, output)
    with target.open("x", encoding="utf-8") as handle:
        handle.write(text)
