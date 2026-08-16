"""Deterministic text metrics. No LLM judge anywhere in this file.

Three families, each tied to a claim this repo makes about its styles:

  size      chars/words — the "shorter" claim.
  shape     how the text scans: distance to the first anchor, longest anchor-free
            block, anchors per 100 words. Classic reading grades (Flesch-Kincaid
            and friends) only see word and sentence length, so a wall of short
            plain words scores "easy" on every one of them. These do not.
  register  sentence length against the ASD-STE100 20-word rule, and hits from
            the 2026 Claudism list (docs/claudisms-2026.md) — the patterns the
            no-slop styles exist to remove.

Fenced and inline code is stripped before any prose metric: a shell one-liner is
not a 30-word sentence, and a style is never allowed to touch code anyway.
"""

import re
import statistics

_FENCE = re.compile(r"```.*?(?:```|\Z)", re.S)
_INLINE_CODE = re.compile(r"`[^`\n]+`")
_TABLE_ROW = re.compile(r"^\s*\|.*$", re.M)
_HEADING_MARK = re.compile(r"^\s*#+\s*", re.M)
_ANCHOR_LINE = re.compile(r"^\s*(?:[-*+>#→•]|\d+[.)])\s", re.M)
_BOLD = re.compile(r"\*\*(?!\s).+?\*\*", re.S)
_WORD = re.compile(r"[^\W\d_]+", re.UNICODE)
_SENT_END = re.compile(r"(?<=[.!?])[\s\n]+")
_ABBREV = re.compile(r"\b(?:e\.g|i\.e|etc|vs|Mr|Dr|Fig|approx|no)\.\Z", re.I)

# Claudisms from docs/claudisms-2026.md. Safe to spell out here: this file is a
# measuring tool and never enters a system prompt.
_CLAUDISMS = [
    r"\bload-bearing\b", r"\bsmoking gun\b", r"\bhand-waving\b",
    r"\breflexive hedging\b", r"\bhonest framing\b",
    r"\bworth (?:stating|naming) (?:plainly|precisely)\b",
    r"\bthe real tension\b", r"\bcarry the argument\b",
    r"\bthe (?:right|smart|obvious) move\b", r"\bthe unlock\b",
    r"\bheterogeneous\b", r"\b(?:quintile|decile)s?\b",
    r"\bhere'?s where I'?d (?:push back|hold the line)\b",
    r"\b(?:serves|stands|functions) as\b",
    r"\byou'?re right to (?:push back|call)\b",
    r"\bthat'?s on me\b",
    # Sentence-initial negative parallelism: "It is not X, it is Y."
    r"(?:^|(?<=[.!?]\s))(?:It|This|That)(?:'s| is| was)? not\b[^.!?\n]{0,80}?,?\s*"
    r"(?:it|this|that)(?:'s| is| was)\b",
]
_CLAUDISM_RE = [re.compile(p, re.I | re.M) for p in _CLAUDISMS]


def prose(text):
    """Text with the non-prose removed: fenced blocks and table rows out, inline
    code down to one token, heading hashes dropped. A markdown table is a layout,
    not a 60-word sentence, and counting it as one would swamp every metric."""
    out = _FENCE.sub("\n", text)
    out = _TABLE_ROW.sub("", out)
    out = _INLINE_CODE.sub("code", out)
    return _HEADING_MARK.sub("", out)


def words(s):
    return len(_WORD.findall(s))


def _units(text):
    """Prose split into units a sentence cannot cross. A list item is its own
    unit even without a full stop, otherwise six terse bullets read as one
    50-word sentence and every length metric lies."""
    units, buf = [], []
    for line in prose(text).splitlines():
        stripped = line.strip()
        if not stripped or _ANCHOR_LINE.match(line):
            if buf:
                units.append(" ".join(buf))
                buf = []
            if stripped and _ANCHOR_LINE.match(line):
                units.append(stripped)
            continue
        buf.append(stripped)
    if buf:
        units.append(" ".join(buf))
    return units


def sentences(text):
    """Sentence split that does not break on e.g. / i.e. / vs. abbreviations."""
    out = []
    for unit in _units(text):
        buf = ""
        for piece in _SENT_END.split(unit):
            buf = f"{buf} {piece}".strip() if buf else piece
            if _ABBREV.search(buf):
                continue
            if buf.strip():
                out.append(buf.strip())
            buf = ""
        if buf.strip():
            out.append(buf.strip())
    return [s for s in out if words(s)]


def paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", prose(text).strip()) if p.strip()]


def _anchored(paragraph):
    return bool(_ANCHOR_LINE.search(paragraph) or _BOLD.search(paragraph))


def words_to_first_anchor(text):
    """Words the eye travels before the first thing that lands (bold or a list
    marker). No anchor at all means the whole answer is undifferentiated, so the
    score is its full word count. Lower is better."""
    body = prose(text)
    hits = [m.start() for m in (_BOLD.search(body), _ANCHOR_LINE.search(body)) if m]
    return words(body[:min(hits)]) if hits else words(body)


def longest_wall_words(text):
    """Longest paragraph with no anchor at all — the biggest block a reader must
    grind through with nothing to grab. Lower is better."""
    walls = [words(p) for p in paragraphs(text) if not _anchored(p)]
    return max(walls) if walls else 0


def anchors_per_100w(text):
    body = prose(text)
    n = words(body)
    hits = len(_BOLD.findall(body)) + len(_ANCHOR_LINE.findall(body))
    return round(100 * hits / n, 2) if n else 0.0


def claudisms_per_1000w(text):
    body = prose(text)
    n = words(body)
    hits = sum(len(r.findall(body)) for r in _CLAUDISM_RE)
    return round(1000 * hits / n, 2) if n else 0.0


def measure(text):
    sents = sentences(text)
    lens = [words(s) for s in sents] or [0]
    paras = [words(p) for p in paragraphs(text)] or [0]
    return {
        "chars": len(text),
        "words": words(prose(text)),
        "mean_sentence_words": round(statistics.mean(lens), 1),
        "max_sentence_words": max(lens),
        "over_20w_sentence_pct": round(100 * sum(1 for x in lens if x > 20) / len(lens), 1),
        "mean_paragraph_words": round(statistics.mean(paras), 1),
        "words_to_first_anchor": words_to_first_anchor(text),
        "longest_wall_words": longest_wall_words(text),
        "anchors_per_100w": anchors_per_100w(text),
        "claudisms_per_1000w": claudisms_per_1000w(text),
    }


KEYS = ("chars", "words", "mean_sentence_words", "max_sentence_words",
        "over_20w_sentence_pct", "mean_paragraph_words", "words_to_first_anchor",
        "longest_wall_words", "anchors_per_100w", "claudisms_per_1000w")

# Direction each metric should move for the style to be doing its job. Size and
# register metrics have a target; shape metrics are descriptive, not scored.
BETTER = {
    "chars": "lower", "words": "lower",
    "mean_sentence_words": "lower", "max_sentence_words": "lower",
    "over_20w_sentence_pct": "lower", "mean_paragraph_words": "lower",
    "words_to_first_anchor": "lower", "longest_wall_words": "lower",
    "anchors_per_100w": "higher", "claudisms_per_1000w": "lower",
}
