from __future__ import annotations

import pathlib
import re
from urllib.parse import urlparse

URL_RE = re.compile(r"https://[^\s>]+")
ASSET_RE = re.compile(r"assets/[A-Za-z0-9._/\-]+")
APPLE_HOSTS = {"developer.apple.com", "www.apple.com", "apple.com"}
WWDC_SESSION_RE = re.compile(
    r"https://developer\.apple\.com/videos/play/wwdc\d{4}/\d+/$"
)

# This is the semantic owner for WWDC session URL-to-title verification. Every
# WWDC session linked by the package must have one declared official title here.
WWDC_SESSION_TITLES = {
    "https://developer.apple.com/videos/play/wwdc2025/219/": "Meet Liquid Glass",
    "https://developer.apple.com/videos/play/wwdc2025/220/": (
        "Say hello to the new look of app icons"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/284/": (
        "Build a UIKit app with the new design"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/310/": (
        "Build an AppKit app with the new design"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/323/": (
        "Build a SwiftUI app with the new design"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/337/": (
        "What's new in SF Symbols 7"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/356/": (
        "Get to know the new design system"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/359/": (
        "Design foundations from idea to interface"
    ),
    "https://developer.apple.com/videos/play/wwdc2025/361/": (
        "Create icons with Icon Composer"
    ),
    "https://developer.apple.com/videos/play/wwdc2026/250/": (
        "Principles of great design"
    ),
    "https://developer.apple.com/videos/play/wwdc2026/269/": "What's new in SwiftUI",
    "https://developer.apple.com/videos/play/wwdc2026/278/": (
        "Modernize your UIKit app"
    ),
    "https://developer.apple.com/videos/play/wwdc2026/289/": (
        "Modernize your AppKit app"
    ),
    "https://developer.apple.com/videos/play/wwdc2026/292/": (
        "Design intuitive search experiences"
    ),
}


def default_paths(skill_dir: pathlib.Path) -> list[pathlib.Path]:
    paths = [skill_dir / "SKILL.md", skill_dir / "agents" / "metadata.yaml"]
    paths.extend(sorted((skill_dir / "references").glob("*.md")))
    return [path for path in paths if path.exists()]


def normalize_url(raw: str) -> str:
    trimmed = raw.rstrip(".,;:]")
    while trimmed.endswith(")") and trimmed.count(")") > trimmed.count("("):
        trimmed = trimmed[:-1]
    return trimmed


def iter_urls(paths: list[pathlib.Path]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for match in URL_RE.findall(text):
            url = normalize_url(match)
            if _is_official_apple_url(url) and url not in seen:
                seen.add(url)
                ordered.append(url)
    return ordered


def _is_official_apple_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname in APPLE_HOSTS


def is_wwdc_session_url(url: str) -> bool:
    return WWDC_SESSION_RE.fullmatch(url) is not None


def iter_asset_paths(paths: list[pathlib.Path]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for match in ASSET_RE.findall(text):
            if match not in seen:
                seen.add(match)
                ordered.append(match)
    return ordered
