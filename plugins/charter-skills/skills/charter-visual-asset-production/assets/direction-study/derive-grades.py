"""Derive three colour treatments without changing the source's geometry.

Run with Python 3 and Pillow, naming a new or empty output folder:

    python3 derive-grades.py /absolute/path/to/new-folder

The script reads expected-source.jpg beside itself and writes the three grades
to that folder, so the bundled grades stay as they are to compare with. The
source is decoded once; every grade uses the same 8-bit luminance plane and a
pointwise colour lookup. No crop, warp, retouch or further generation occurs.
"""

import sys
from pathlib import Path

from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parent
GRADES = {
    "blue": ("#102331", "#617d9d", "#dbe9f7"),
    "gold": ("#261e14", "#8d7642", "#f6e5b7"),
    "teal": ("#10292a", "#467d7c", "#d7f0e7"),
}


def derive(output: Path) -> None:
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise SystemExit(f"Refusing a nonempty or non-directory output: {output}")
    output.mkdir(parents=True, exist_ok=True)
    with Image.open(ROOT / "expected-source.jpg") as source:
        luminance = source.convert("RGB").convert("L")
    for name, (shadow, middle, highlight) in GRADES.items():
        grade = ImageOps.colorize(
            luminance,
            black=shadow,
            white=highlight,
            mid=middle,
            blackpoint=0,
            midpoint=128,
            whitepoint=255,
        )
        grade.save(
            output / f"expected-{name}.jpg",
            quality=88,
            subsampling=0,
            optimize=True,
            progressive=True,
        )


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 derive-grades.py /absolute/path/to/new-folder")
    derive(Path(sys.argv[1]).expanduser().resolve())
