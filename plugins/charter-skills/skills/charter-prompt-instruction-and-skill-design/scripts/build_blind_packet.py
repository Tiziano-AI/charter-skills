#!/usr/bin/env python3
"""Build blinded prompt review packets in reversed orders and a private label mapping."""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import secrets
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build review-packet-<n>.md files and a private mapping.json from a JSON manifest. "
            "With the default two orders, the second packet lists the same labels in reverse order."
        )
    )
    parser.add_argument("manifest", type=Path, help="JSON manifest path")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Output directory; existing packets or mapping.json are never overwritten",
    )
    parser.add_argument("--seed", help="Optional reproducible shuffle seed")
    parser.add_argument(
        "--orders",
        type=int,
        choices=(1, 2),
        default=2,
        help="1 writes one shuffled packet; 2 (default) also writes the reversed order",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise SystemExit(f"Cannot read manifest: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit("Manifest must be a JSON object")
    return data


def candidate_text(candidate: dict[str, Any], base: Path) -> str:
    has_path = "path" in candidate
    has_text = "text" in candidate
    if has_path == has_text:
        raise SystemExit("Each variant must contain exactly one of 'path' or 'text'")
    if has_path:
        raw_path = candidate["path"]
        if not isinstance(raw_path, str) or not raw_path:
            raise SystemExit("Variant 'path' must be a non-empty string")
        path = (base / raw_path).resolve()
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise SystemExit(f"Cannot read variant path {raw_path!r}: {exc}") from exc
    else:
        text = candidate["text"]
        if not isinstance(text, str):
            raise SystemExit("Variant 'text' must be a string")
    if not text.strip():
        raise SystemExit("Variant text must not be empty")
    return text


def fence_for(text: str) -> str:
    current = 0
    longest = 0
    for char in text:
        if char == "`":
            current += 1
            longest = max(longest, current)
        else:
            current = 0
    return "`" * max(3, longest + 1)


def review_instructions(top_n: int | None) -> list[str]:
    lines = [
        "## What to return",
        "",
        "Read every candidate in full before judging. Candidate labels and their order are",
        "arbitrary; infer nothing about quality or authorship from either. Then return:",
        "",
        "1. The candidate you recommend for the governing question, or a coherent synthesis",
        "   (for example one candidate's approach with another's exact constraint).",
        "2. The decisive language: the passages that make the difference, quoted.",
        "3. The strongest plausible failure of what you recommend.",
        "4. What makes the nearest alternative lose.",
    ]
    if top_n is not None:
        lines.append(f"5. Your top {top_n} candidates in order, each with one line of reason.")
    return lines


def write_new_text(path: Path, text: str) -> None:
    try:
        with path.open("x", encoding="utf-8") as stream:
            stream.write(text)
    except FileExistsError as exc:
        raise SystemExit(f"Refusing to overwrite existing output: {path.name}") from exc


def main() -> None:
    args = parse_args()
    manifest_path = args.manifest.resolve()
    manifest = load_manifest(manifest_path)

    question = manifest.get("question")
    if not isinstance(question, str) or not question.strip():
        raise SystemExit("Manifest 'question' must be a non-empty string")
    variants = manifest.get("variants")
    if not isinstance(variants, list) or len(variants) < 2:
        raise SystemExit("Manifest must contain at least two variants")
    top_n = manifest.get("top_n")
    if top_n is not None:
        if not isinstance(top_n, int) or isinstance(top_n, bool) or top_n < 1:
            raise SystemExit("Manifest 'top_n' must be a positive integer")
        if top_n > len(variants):
            raise SystemExit("Manifest 'top_n' cannot exceed the number of variants")

    prepared: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_hashes: dict[str, str] = {}
    for index, variant in enumerate(variants, start=1):
        if not isinstance(variant, dict):
            raise SystemExit(f"Variant {index} must be an object")
        private_id = variant.get("id")
        if not isinstance(private_id, str) or not private_id.strip():
            raise SystemExit(f"Variant {index} requires a non-empty string 'id'")
        if private_id in seen_ids:
            raise SystemExit(f"Duplicate variant id: {private_id}")
        seen_ids.add(private_id)
        text = candidate_text(variant, manifest_path.parent)
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        if digest in seen_hashes:
            raise SystemExit(
                f"Duplicate variant text for {private_id!r} and {seen_hashes[digest]!r}"
            )
        seen_hashes[digest] = private_id
        prepared.append(
            {
                "private_id": private_id,
                "text": text,
                "sha256": digest,
                "private_metadata": {
                    k: v for k, v in variant.items() if k not in {"id", "text"}
                },
            }
        )

    seed = args.seed or secrets.token_hex(16)
    random.Random(seed).shuffle(prepared)
    for index, item in enumerate(prepared, start=1):
        item["label"] = f"C{index}"

    orders = [prepared]
    if args.orders == 2:
        orders.append(list(reversed(prepared)))

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    packet_paths = [output_dir / f"review-packet-{n}.md" for n in range(1, len(orders) + 1)]
    mapping_path = output_dir / "mapping.json"
    existing = [
        path.name for path in (*packet_paths, mapping_path) if path.exists() or path.is_symlink()
    ]
    if existing:
        raise SystemExit(f"Refusing to overwrite existing output: {', '.join(existing)}")

    packets = []
    for packet_path, ordered in zip(packet_paths, orders):
        lines = [
            "# Blinded Prompt Review",
            "",
            "## Governing question",
            "",
            question.strip(),
            "",
            *review_instructions(top_n),
            "",
            "## Candidates",
            "",
        ]
        for item in ordered:
            fence = fence_for(item["text"])
            lines.extend([f"### {item['label']}", "", fence, item["text"], fence, ""])
        write_new_text(packet_path, "\n".join(lines))
        packets.append(
            {
                "file": packet_path.name,
                "order": [item["label"] for item in ordered],
                "sha256": hashlib.sha256(packet_path.read_bytes()).hexdigest(),
            }
        )

    mapping = {
        "seed": seed,
        "question": question,
        "top_n": top_n,
        "packets": packets,
        "variants": [
            {
                "label": item["label"],
                "private_id": item["private_id"],
                "sha256": item["sha256"],
                "private_metadata": item["private_metadata"],
            }
            for item in prepared
        ],
    }
    write_new_text(mapping_path, json.dumps(mapping, indent=2, ensure_ascii=False) + "\n")
    print(
        json.dumps(
            {
                "packets": [str(path) for path in packet_paths],
                "mapping": str(mapping_path),
                "seed": seed,
            }
        )
    )


if __name__ == "__main__":
    main()
