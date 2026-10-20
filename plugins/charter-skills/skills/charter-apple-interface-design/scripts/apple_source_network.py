from __future__ import annotations

from html.parser import HTMLParser
import pathlib
import re
import unicodedata
import urllib.error
import urllib.request

TIMEOUT_SECONDS = 20.0
WWDC_PAGE_TITLE_RE = re.compile(
    r"^(?P<session>.+?)\s+-\s+WWDC\d{2}\s+-\s+Videos\s+-\s+Apple Developer$"
)


class SessionTitleCheck:
    __slots__ = ("ok", "status", "observed_page_title", "detail")

    def __init__(
        self,
        ok: bool,
        status: int | None,
        observed_page_title: str | None,
        detail: str | None,
    ) -> None:
        self.ok = ok
        self.status = status
        self.observed_page_title = observed_page_title
        self.detail = detail


class _PageTitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._inside_title = False
        self._parts: list[str] = []

    def handle_starttag(
        self, tag: str, attrs: list[tuple[str, str | None]]
    ) -> None:
        del attrs
        if tag.casefold() == "title" and not self._parts:
            self._inside_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() == "title":
            self._inside_title = False

    def handle_data(self, data: str) -> None:
        if self._inside_title:
            self._parts.append(data)

    def title(self) -> str | None:
        title = " ".join("".join(self._parts).split())
        return title or None


def request_status(url: str, method: str) -> int:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "charter-apple-interface-source-check/1.0"},
        method=method,
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        return int(response.status)


def request_page(url: str) -> tuple[int, str]:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "charter-apple-interface-source-check/1.0"},
        method="GET",
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        body = response.read().decode(charset)
        return int(response.status), body


def check_url(url: str) -> tuple[bool, int | None, str | None]:
    try:
        status = request_status(url, "HEAD")
        return (200 <= status < 400, status, None)
    except urllib.error.HTTPError as exc:
        if exc.code not in {403, 405}:
            return (False, exc.code, exc.reason)
        try:
            status = request_status(url, "GET")
            return (200 <= status < 400, status, None)
        except urllib.error.HTTPError as inner_exc:
            return (False, inner_exc.code, inner_exc.reason)
        except urllib.error.URLError as inner_exc:
            return (False, None, str(inner_exc.reason))
    except urllib.error.URLError as exc:
        return (False, None, str(exc.reason))


def check_asset(skill_dir: pathlib.Path, asset_ref: str) -> bool:
    return (skill_dir / asset_ref).is_file()


def extract_page_title(page_html: str) -> str | None:
    parser = _PageTitleParser()
    parser.feed(page_html)
    parser.close()
    return parser.title()


def _normalized_semantic_title(value: str) -> str:
    punctuation_normalized = value.translate(
        str.maketrans({"\u2018": "'", "\u2019": "'", "\u00a0": " "})
    )
    return " ".join(unicodedata.normalize("NFKC", punctuation_normalized).split()).casefold()


def check_wwdc_session_title(url: str, expected_title: str) -> SessionTitleCheck:
    try:
        status, page_html = request_page(url)
    except urllib.error.HTTPError as exc:
        return SessionTitleCheck(False, exc.code, None, str(exc.reason))
    except urllib.error.URLError as exc:
        return SessionTitleCheck(False, None, None, str(exc.reason))
    except UnicodeError as exc:
        return SessionTitleCheck(False, None, None, f"page decode failed: {exc}")

    if not 200 <= status < 400:
        return SessionTitleCheck(False, status, None, "unexpected HTTP status")

    page_title = extract_page_title(page_html)
    if page_title is None:
        return SessionTitleCheck(False, status, None, "official page has no HTML title")

    match = WWDC_PAGE_TITLE_RE.fullmatch(page_title)
    if match is None:
        return SessionTitleCheck(
            False,
            status,
            page_title,
            "official page title is not a semantic WWDC session title",
        )

    observed_title = match.group("session")
    if _normalized_semantic_title(observed_title) != _normalized_semantic_title(
        expected_title
    ):
        return SessionTitleCheck(
            False,
            status,
            page_title,
            f"expected session title {expected_title!r}; observed {observed_title!r}",
        )
    return SessionTitleCheck(True, status, page_title, None)
