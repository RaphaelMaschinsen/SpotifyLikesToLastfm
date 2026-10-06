"""Strips release cruft such as "- 2014 Remaster" from Spotify track titles before loving them on Last.fm."""

import re
from typing import Optional

YEAR = r"(?:19|20)\d{2}"
SEP = r"\s*[-–]?\s*"
REMASTER = r"remaster(?:ed|ing)?"
REMASTER_QUALIFIERS = ["digital", "hd", "expanded", "deluxe", r"super\s+deluxe", "mono", "stereo"]
EDITION_WORDS = [
    r"(?:super\s+)?deluxe", "expanded", "legacy", "special", "definitive", r"collector'?s",
    "japanese", REMASTER, "reissue", "anniversary",
]


def _remaster_patterns() -> list:
    out = []
    for qualifier in [""] + REMASTER_QUALIFIERS:
        prefix = qualifier + r"\s+" if qualifier else ""
        # "Master" alone is a real title word, so it only counts behind a qualifier ("Digital Master").
        words = [REMASTER] + ([r"master(?:ed)?"] if prefix else [])
        for word in words:
            for suffix in ["", r"\s+version"]:
                out += [
                    f"{prefix}{word}{suffix}",
                    f"{prefix}{YEAR}{SEP}{word}{suffix}",
                    f"{prefix}{word}{SEP}{YEAR}{suffix}",
                    f"{YEAR}{SEP}{prefix}{word}{suffix}",
                ]
    localized = r"remasteriza(?:d[oa]s?|ci[óo]n|[çc][ãa]o)"
    for prefix in ["", r"(?:versi[óo]n|vers[ãa]o)\s+"]:
        for suffix in ["", r"\s+digital"]:
            word = f"{prefix}{localized}{suffix}"
            out += [word, f"{word}{SEP}{YEAR}", f"{YEAR}{SEP}{word}"]
    return out


def _edition_pattern() -> str:
    word = "(?:" + "|".join(EDITION_WORDS) + ")"
    join = r"(?:\s+|\s*&\s*|\s+and\s+)"
    return rf"(?:\d+(?:st|nd|rd|th)\s+)?{word}(?:{join}{word})*(?:\s+(?:edition|version))?"


# A closed list matched against the WHOLE trailing segment: "(Live)" or "Pt. II" style content is never touched.
MARKERS = [
    re.compile(rf"^\s*(?:{p})\s*$", re.IGNORECASE)
    for p in _remaster_patterns() + [
        _edition_pattern(),
        rf"expanded\s+{YEAR}",
        rf"deluxe\s+{YEAR}",
        r"bonus\s+tracks?(?:\s+version)?",
        r"bonus\s+versions?",
        r"explicit(?:\s+version)?",
        r"clean(?:\s+version)?",
    ]
]
# The mix is real information, so "(Mono Remastered)" keeps "Mono" rather than vanishing.
RETAINED_WORDS = [(re.compile(r"\bmono\b", re.IGNORECASE), "Mono"), (re.compile(r"\bstereo\b", re.IGNORECASE), "Stereo")]
BARE_YEAR = re.compile(rf"^\s*{YEAR}\s*$")
ENDS_IN_YEAR = re.compile(rf"{YEAR}\s*$")
MAX_PASSES = 3


def _split_tail(title: str) -> Optional[tuple]:
    candidates = []
    if title.endswith(")") and "(" in title:
        i = title.rindex("(")
        candidates.append((i, title[:i], title[i + 1:-1]))
    if title.endswith("]") and "[" in title:
        i = title.rindex("[")
        candidates.append((i, title[:i], title[i + 1:-1]))
    if " - " in title:
        i = title.rindex(" - ")
        candidates.append((i, title[:i], title[i + 3:]))
    if not candidates:
        return None
    _, head, segment = max(candidates)
    return head, segment


def _is_marker(segment: str) -> bool:
    return any(m.match(segment) for m in MARKERS)


def clean_title(title: str) -> str:
    """Returns the title with trailing release markers removed, or the title unchanged."""
    current = title
    retained = None
    passes = 0
    while passes < MAX_PASSES:
        tail = _split_tail(current)
        if tail is None:
            break
        head, segment = tail
        matched = _is_marker(segment)
        # A year left behind by a stripped marker is cruft ("- 2012 - Remaster"), unless it ends a range.
        continuation = not matched and passes > 0 and BARE_YEAR.match(segment) and not ENDS_IN_YEAR.search(head)
        if not matched and not continuation:
            break
        head = head.rstrip()
        if len(head) < 2 or not any(c.isalnum() for c in head):
            break
        if matched:
            for pattern, word in RETAINED_WORDS:
                if pattern.search(segment):
                    retained = word
        current = head
        passes += 1
    if retained is not None:
        current += f" - {retained}"
    return current if current.lower() != title.lower() else title
