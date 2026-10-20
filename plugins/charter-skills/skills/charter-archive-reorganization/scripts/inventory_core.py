"""Inventory classification helpers for archive taxonomy workflows."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from archive_scan import file_identity, scan_tree, unreadable_row

MEDIA_EXTENSIONS = {
    # still images and design files
    ".ai", ".bmp", ".gif", ".heic", ".heif", ".jpeg", ".jpg", ".png", ".psd",
    ".tif", ".tiff", ".webp",
    # camera RAW originals
    ".arw", ".cr2", ".cr3", ".dng", ".nef", ".orf", ".raf", ".rw2",
    # video
    ".avi", ".m4v", ".mkv", ".mov", ".mp4", ".mts",
    # audio
    ".aif", ".aiff", ".flac", ".m4a", ".mid", ".mp3", ".wav",
}

UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.I
)
NUMERIC_RE = re.compile(r"^\d{8,}$")
SCREENSHOT_RE = re.compile(r"^screenshot\s+\d{4}", re.I)
CAMERA_COUNTER_RE = re.compile(
    r"^(?:img|vid|dsc[nf]?|_dsc|mvi|gopr|dji|pxl)[_-]?\d{3,}(?:[_-]\d+)*$", re.I
)


def is_opaque_name(name: str) -> bool:
    """Return whether a filename has low semantic placement confidence."""
    stem = Path(name).stem.strip()
    if UUID_RE.fullmatch(stem):
        return True
    if NUMERIC_RE.fullmatch(stem):
        return True
    if SCREENSHOT_RE.match(stem) or CAMERA_COUNTER_RE.fullmatch(stem):
        return True
    return not any(char.isalpha() for char in stem)


def normalize_ascii(text: str) -> str:
    """Normalize text to ASCII for naming-risk review."""
    text = unicodedata.normalize("NFKD", text)
    return text.encode("ascii", "ignore").decode("ascii")


def inventory_record(root: Path, path: Path) -> dict[str, object]:
    """Return one deterministic inventory record for a file."""
    rel = path.relative_to(root)
    suffix = path.suffix.lower()
    observed = path.lstat()
    return {
        "path": str(rel),
        "top_level": rel.parts[0] if rel.parts else "",
        "name": path.name,
        "ascii_name": normalize_ascii(path.name),
        "suffix": suffix if suffix else "[no_ext]",
        "size": observed.st_size,
        "mtime": observed.st_mtime,
        "identity": file_identity(observed),
        "is_media": suffix in MEDIA_EXTENSIONS,
        "opaque_name": is_opaque_name(path.name),
    }


def inventory_records(root: Path) -> tuple[list[dict[str, object]], list[dict[str, str]]]:
    """Return regular-file records and explicit excluded or unreadable nodes."""
    root = root.resolve(strict=True)
    files, excluded = scan_tree(root)
    records: list[dict[str, object]] = []
    for path in files:
        try:
            records.append(inventory_record(root, path))
        except OSError as error:
            excluded.append(unreadable_row(root, path, error))
    return records, sorted(excluded, key=lambda row: row["path"])
