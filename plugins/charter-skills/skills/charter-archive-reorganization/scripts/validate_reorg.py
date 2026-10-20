#!/usr/bin/env python3
"""Check a reorganized archive tree against its configured top-level entries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from archive_scan import report_path, write_report
from reorg_validation_core import validate_reorg_tree


def main() -> int:
    """Write the report; exit 1 only when a top-level entry is outside the config."""
    parser = argparse.ArgumentParser(description="Validate a reorganized archive tree.")
    parser.add_argument("root", help="Root path to validate.")
    parser.add_argument("--config", required=True, help="Validation config JSON.")
    parser.add_argument("--out", required=True, help="Output JSON report.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve(strict=True)
    output = report_path(root, Path(args.out))
    config = json.loads(
        Path(args.config).expanduser().resolve().read_text(encoding="utf-8")
    )
    report = validate_reorg_tree(root=root, config=config)
    write_report(root, output, json.dumps(report, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
