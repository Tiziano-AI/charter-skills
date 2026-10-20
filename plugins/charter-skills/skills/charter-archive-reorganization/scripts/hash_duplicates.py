#!/usr/bin/env python3
"""Report equal-content regular files without changing the archive."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from archive_scan import report_path, write_report
from duplicate_core import duplicate_report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", help="Local quiescent archive root.")
    parser.add_argument("--out", required=True, help="New JSON path outside the archive.")
    args = parser.parse_args()
    root = Path(args.root).expanduser().resolve(strict=True)
    output = report_path(root, Path(args.out))
    report = duplicate_report(root=root)
    write_report(root, output, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps({
        "duplicate_group_count": report["duplicate_group_count"],
        "hardlink_set_count": len(report["hardlink_sets"]),
        "complete": report["complete"],
        "unreadable_count": len(report["unreadable"]),
        "report": str(output),
    }))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
