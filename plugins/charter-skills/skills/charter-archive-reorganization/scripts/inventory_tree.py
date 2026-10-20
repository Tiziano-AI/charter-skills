#!/usr/bin/env python3
"""Inventory a local archive tree into deterministic JSON artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from archive_scan import report_path
from inventory_core import inventory_records
from inventory_output import write_inventory


def main() -> int:
    """Write JSONL inventory records and a summary for one tree."""
    parser = argparse.ArgumentParser(
        description="Inventory a directory tree into JSONL plus summary JSON."
    )
    parser.add_argument("root", help="Absolute path to inventory.")
    parser.add_argument(
        "-o",
        "--out-dir",
        required=True,
        help="Output directory for inventory JSON files.",
    )
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve(strict=True)
    out_dir = report_path(root, Path(args.out_dir))
    records, excluded = inventory_records(root)
    summary = write_inventory(root=root, out_dir=out_dir, records=records, excluded=excluded)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
