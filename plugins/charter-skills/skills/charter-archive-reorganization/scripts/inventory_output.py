"""Writers for archive inventory JSONL and summary outputs."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

from archive_scan import report_path, split_unreadable


def build_summary(root: Path, records: list[dict[str, object]]) -> dict[str, object]:
    """Return a summary row for inventory records."""
    top_sizes: dict[str, int] = defaultdict(int)
    for record in records:
        top_sizes[str(record["top_level"])] += record_size(record)
    return {
        "root": str(root),
        "file_count": len(records),
        "opaque_name_count": sum(1 for record in records if record["opaque_name"]),
        "top_level_file_counts": dict(
            Counter(record["top_level"] for record in records).most_common()
        ),
        "top_level_size_bytes": dict(
            sorted(top_sizes.items(), key=lambda item: item[1], reverse=True)
        ),
        "suffix_counts": dict(
            Counter(record["suffix"] for record in records).most_common()
        ),
        "type_counts": dict(
            Counter("media" if record["is_media"] else "other" for record in records)
        ),
    }


def record_size(record: dict[str, object]) -> int:
    """Return an inventory record size as an integer."""
    value = record.get("size", 0)
    if isinstance(value, int):
        return value
    return int(str(value))


def write_inventory(
    *, root: Path, out_dir: Path, records: list[dict[str, object]],
    excluded: list[dict[str, str]]
) -> dict[str, object]:
    """Write inventory JSONL and summary JSON files."""
    out_dir = report_path(root, out_dir)
    out_dir.mkdir()
    with (out_dir / "inventory.jsonl").open("x", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    summary = build_summary(root, records)
    excluded, unreadable = split_unreadable(excluded)
    summary["complete"] = not unreadable
    summary["excluded_nodes"] = excluded
    summary["unreadable"] = unreadable
    summary["observation"] = "per-file reads; not an atomic filesystem snapshot"
    with (out_dir / "summary.json").open("x", encoding="utf-8") as handle:
        handle.write(json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    return summary
