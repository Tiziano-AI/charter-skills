"""Equal-content observations for regular files; no survivor or deletion policy."""

from __future__ import annotations

from collections import defaultdict
import hashlib
import os
from pathlib import Path
import stat

from archive_scan import (
    file_identity, relative_path, scan_tree, split_unreadable, unreadable_row,
)


def hash_file(path: Path) -> tuple[str, dict[str, int]]:
    """Hash one regular file and reject observed changes during its read."""
    before = path.lstat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError(f"not a regular file: {path}")
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, "rb") as handle:
        opened = os.fstat(handle.fileno())
        if file_identity(opened) != file_identity(before):
            raise ValueError(f"file changed before hashing: {path}")
        digest = hashlib.sha256()
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
        after = os.fstat(handle.fileno())
    if (file_identity(before) != file_identity(after)
            or file_identity(after) != file_identity(path.lstat())):
        raise ValueError(f"file changed during hashing: {path}")
    return digest.hexdigest(), file_identity(after)


def duplicate_report(*, root: Path) -> dict[str, object]:
    """Report equal-content candidates without deciding which path is dispensable.

    Names that share one filesystem object (hard links) are hashed once and
    reported together, because removing one of those names frees nothing.
    Unreadable or changing files are recorded and skipped.
    """
    root = root.resolve(strict=True)
    files, scanned = scan_tree(root)
    excluded, unreadable = split_unreadable(scanned)
    by_size: dict[int, list[tuple[Path, os.stat_result]]] = defaultdict(list)
    for path in files:
        if path.name == ".DS_Store":
            continue
        try:
            info = path.lstat()
        except OSError as error:
            unreadable.append(unreadable_row(root, path, error))
            continue
        by_size[info.st_size].append((path, info))
    groups: list[dict[str, object]] = []
    hardlink_sets: list[dict[str, object]] = []
    for size, candidates in sorted(by_size.items()):
        if len(candidates) < 2:
            continue
        objects: dict[tuple[int, int], list[Path]] = defaultdict(list)
        for path, info in candidates:
            objects[(info.st_dev, info.st_ino)].append(path)
        for names in objects.values():
            if len(names) > 1:
                hardlink_sets.append({
                    "size": size, "paths": [relative_path(root, p) for p in names],
                })
        if len(objects) < 2:
            continue
        by_hash: dict[str, list[dict[str, object]]] = defaultdict(list)
        for names in objects.values():
            try:
                digest, identity = hash_file(names[0])
            except OSError as error:
                unreadable.append(unreadable_row(root, names[0], error))
                continue
            except ValueError as error:
                unreadable.append(unreadable_row(root, names[0], error, "changed_during_read"))
                continue
            if identity["size"] != size:
                unreadable.append(unreadable_row(
                    root, names[0], ValueError("size changed since grouping"),
                    "changed_during_read",
                ))
                continue
            by_hash[digest].append({
                "path": relative_path(root, names[0]),
                "identity": identity,
                "hardlink_names": [relative_path(root, p) for p in names[1:]],
            })
        for digest, members in sorted(by_hash.items()):
            if len(members) > 1:
                groups.append({"size": size, "sha256": digest, "files": members})
    return {
        "root": str(root),
        "observation": "per-file reads; not an atomic snapshot or deletion plan",
        "complete": not unreadable,
        "excluded_nodes": excluded,
        "unreadable": sorted(unreadable, key=lambda row: row["path"]),
        "duplicate_group_count": len(groups),
        "groups": groups,
        "hardlink_sets": hardlink_sets,
    }
