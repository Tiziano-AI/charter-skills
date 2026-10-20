#!/usr/bin/env python3
"""Verify Apple source URLs and local asset references used by the skill."""

from __future__ import annotations

import argparse
import pathlib
import sys

from apple_source_network import check_asset, check_url, check_wwdc_session_title
from apple_source_scan import (
    WWDC_SESSION_TITLES,
    default_paths,
    is_wwdc_session_url,
    iter_asset_paths,
    iter_urls,
)


def _paths_from_args(skill_dir: pathlib.Path, values: list[str]) -> list[pathlib.Path]:
    if values:
        return [pathlib.Path(value).resolve() for value in values]
    return default_paths(skill_dir)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify official Apple URLs and local asset references."
    )
    parser.add_argument("paths", nargs="*", help="Text files to scan.")
    args = parser.parse_args()

    skill_dir = pathlib.Path(__file__).resolve().parents[1]
    paths = _paths_from_args(skill_dir, list(args.paths))
    if not paths:
        print("No files found to scan.", file=sys.stderr)
        return 1

    failures = 0
    for url in iter_urls(paths):
        if is_wwdc_session_url(url):
            expected_title = WWDC_SESSION_TITLES.get(url)
            if expected_title is None:
                failures += 1
                print(f"FAIL -   {url} (WWDC session title is not declared)")
                continue
            check = check_wwdc_session_title(url, expected_title)
            if check.ok:
                print(f"OK   {check.status} {url} [{expected_title}]")
            else:
                failures += 1
                observed = (
                    f"; page title {check.observed_page_title!r}"
                    if check.observed_page_title is not None
                    else ""
                )
                print(
                    f"FAIL {check.status if check.status is not None else '-'}   "
                    f"{url} ({check.detail}{observed})"
                )
            continue

        ok, status, detail = check_url(url)
        if ok:
            print(f"OK   {status} {url}")
        else:
            failures += 1
            print(f"FAIL {status if status is not None else '-'}   {url} ({detail})")

    for asset_ref in iter_asset_paths(paths):
        if check_asset(skill_dir, asset_ref):
            print(f"OK   asset {asset_ref}")
        else:
            failures += 1
            print(f"FAIL asset {asset_ref} (missing)")

    if failures:
        print(f"\n{failures} integrity check(s) failed.", file=sys.stderr)
        return 1
    print("\nOfficial Apple source and local asset checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
