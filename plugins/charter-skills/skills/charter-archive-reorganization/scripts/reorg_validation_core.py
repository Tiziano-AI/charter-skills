"""Configured structural observations, not retrieval or disposition certification.

Only a top-level entry outside ``canonical_top_entries`` fails validation. Names
are compared in Unicode NFC, so a folder stored decomposed (NFD) matches its
composed spelling in the config. A regular root ``.DS_Store`` is ambient
metadata, not a top-level entry. ``.DS_Store`` counts and exact-duplicate
groups are optional observations: intentional replicas and platform metadata
are acceptable in an archive, so they never fail validation.
"""

from __future__ import annotations

from pathlib import Path
import stat
import unicodedata

from archive_scan import scan_tree, split_unreadable
from duplicate_core import duplicate_report

AMBIENT_METADATA_NAME = ".DS_Store"


def nfc(name: str) -> str:
    """Return the composed Unicode form used for name comparison."""
    return unicodedata.normalize("NFC", name)


def validate_reorg_tree(*, root: Path, config: dict[str, object]) -> dict[str, object]:
    """Observe configured checks and preserve unobserved values as null."""
    if not isinstance(config, dict):
        raise ValueError("validation config must be an object")
    root = root.resolve(strict=True)
    canonical = config.get("canonical_top_entries")
    if not isinstance(canonical, list) or not all(isinstance(v, str) for v in canonical):
        raise ValueError("canonical_top_entries must be a string list")
    check_ds_store = config.get("check_ds_store", False)
    check_duplicates = config.get("check_exact_duplicates", False)
    if not isinstance(check_ds_store, bool) or not isinstance(check_duplicates, bool):
        raise ValueError("check flags must be booleans")
    files, scanned = scan_tree(root)
    excluded, unreadable = split_unreadable(scanned)

    top_entries = sorted(path.name for path in root.iterdir())
    canonical_forms = {nfc(name) for name in canonical}
    present_forms = {nfc(name) for name in top_entries}
    remaining = [
        name for name in top_entries
        if nfc(name) not in canonical_forms and not _is_ambient_metadata(root / name)
    ]
    absent = [name for name in canonical if nfc(name) not in present_forms]

    ds_store = (
        sum(path.name == AMBIENT_METADATA_NAME for path in files) if check_ds_store else None
    )
    duplicate_groups = hardlink_sets = None
    if check_duplicates:
        duplicates = duplicate_report(root=root)
        duplicate_groups = duplicates["duplicate_group_count"]
        hardlink_sets = len(duplicates["hardlink_sets"])
        seen = {(row["path"], row["kind"]) for row in unreadable}
        unreadable += [
            row for row in duplicates["unreadable"]
            if (row["path"], row["kind"]) not in seen
        ]
    return {
        "root": str(root),
        "top_entries": top_entries,
        "remaining_noncanonical_top_entries": remaining,
        "absent_canonical_top_entries": absent,
        "ds_store_count": ds_store,
        "exact_duplicate_group_count": duplicate_groups,
        "hardlink_set_count": hardlink_sets,
        "file_count": len(files),
        "excluded_nodes": excluded,
        "unreadable": sorted(unreadable, key=lambda row: row["path"]),
        "complete": not unreadable,
        "failed": bool(remaining),
    }


def _is_ambient_metadata(path: Path) -> bool:
    """Return whether a root entry is a regular platform metadata file."""
    if path.name != AMBIENT_METADATA_NAME:
        return False
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except OSError:
        return False
