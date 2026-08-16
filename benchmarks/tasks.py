"""Work-equivalence tasks: 12 small functions, each with a hidden test.

The prompt states the exact signature and nothing about edge cases. The test then
checks the edge cases anyway, which is where a rushed or over-compressed answer
fails. Pass or fail is ground truth, so no judge is involved.

Every task carries a reference solution; `run.py selfcheck` runs the hidden tests
against it first, so a broken test can never be mistaken for a broken style.
"""

TASKS = [
    {
        "id": "slugify",
        "prompt": "Write a Python function `slugify(text)` that turns a title into a "
                  "URL slug. Return only the function.",
        "fn": "slugify",
        "cases": [
            (("Hello World",), "hello-world"),
            (("  Multiple   spaces  ",), "multiple-spaces"),
            (("Symbols & Stuff!",), "symbols-stuff"),
            (("already-a-slug",), "already-a-slug"),
            (("",), ""),
            (("--Trim--",), "trim"),
        ],
        "reference": '''
import re, unicodedata
def slugify(text):
    t = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    t = re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()
    return t
''',
    },
    {
        "id": "parse_duration",
        "prompt": "Write a Python function `parse_duration(text)` that parses a "
                  "duration like '1h30m' or '90s' and returns the total number of "
                  "seconds as an int. Return only the function.",
        "fn": "parse_duration",
        "cases": [
            (("1h30m",), 5400),
            (("90s",), 90),
            (("2d",), 172800),
            (("1h",), 3600),
            (("45m30s",), 2730),
            (("0s",), 0),
        ],
        "reference": '''
import re
def parse_duration(text):
    units = {"d": 86400, "h": 3600, "m": 60, "s": 1}
    return sum(int(n) * units[u] for n, u in re.findall(r"(\\d+)([dhms])", text))
''',
    },
    {
        "id": "sliding_window",
        "prompt": "Write a Python function `sliding_window(items, size)` that returns "
                  "a list of consecutive overlapping windows of the given size. "
                  "Return only the function.",
        "fn": "sliding_window",
        "cases": [
            (([1, 2, 3, 4], 2), [[1, 2], [2, 3], [3, 4]]),
            (([1, 2, 3], 3), [[1, 2, 3]]),
            (([1, 2], 3), []),
            (([], 2), []),
            (([1, 2, 3], 1), [[1], [2], [3]]),
        ],
        "reference": '''
def sliding_window(items, size):
    items = list(items)
    if size <= 0 or size > len(items):
        return []
    return [items[i:i + size] for i in range(len(items) - size + 1)]
''',
    },
    {
        "id": "to_snake_case",
        "prompt": "Write a Python function `to_snake_case(name)` that converts a "
                  "camelCase or PascalCase identifier to snake_case. Return only the "
                  "function.",
        "fn": "to_snake_case",
        "cases": [
            (("camelCase",), "camel_case"),
            (("PascalCase",), "pascal_case"),
            (("HTTPResponse",), "http_response"),
            (("already_snake",), "already_snake"),
            (("a",), "a"),
            (("",), ""),
        ],
        "reference": '''
import re
def to_snake_case(name):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\\1_\\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\\1_\\2", s)
    return s.lower()
''',
    },
    {
        "id": "format_bytes",
        "prompt": "Write a Python function `format_bytes(n)` that formats a byte "
                  "count as a human-readable string using B, KB, MB, GB with 1 "
                  "decimal place for values above 1 KB and 1024 as the step. "
                  "Examples: 512 -> '512 B', 1536 -> '1.5 KB'. Return only the "
                  "function.",
        "fn": "format_bytes",
        "cases": [
            ((512,), "512 B"),
            ((1536,), "1.5 KB"),
            ((0,), "0 B"),
            ((1024,), "1.0 KB"),
            ((1048576,), "1.0 MB"),
            ((1073741824,), "1.0 GB"),
        ],
        "reference": '''
def format_bytes(n):
    if n < 1024:
        return f"{n} B"
    value = float(n)
    for unit in ("KB", "MB", "GB"):
        value /= 1024
        if value < 1024 or unit == "GB":
            return f"{value:.1f} {unit}"
''',
    },
    {
        "id": "compare_semver",
        "prompt": "Write a Python function `compare_semver(a, b)` that compares two "
                  "semantic version strings and returns -1, 0 or 1. Ignore any "
                  "pre-release suffix. Return only the function.",
        "fn": "compare_semver",
        "cases": [
            (("1.2.3", "1.2.4"), -1),
            (("1.10.0", "1.9.0"), 1),
            (("2.0.0", "2.0.0"), 0),
            (("1.0.0-beta", "1.0.0"), 0),
            (("0.1.0", "0.0.9"), 1),
        ],
        "reference": '''
def compare_semver(a, b):
    def parts(v):
        core = v.split("-")[0].split("+")[0]
        return [int(x) for x in core.split(".")]
    pa, pb = parts(a), parts(b)
    return (pa > pb) - (pa < pb)
''',
    },
    {
        "id": "truncate_words",
        "prompt": "Write a Python function `truncate_words(text, limit)` that cuts "
                  "text to at most `limit` words and appends an ellipsis character "
                  "'…' when it actually cut something. Return only the function.",
        "fn": "truncate_words",
        "cases": [
            (("one two three four", 2), "one two…"),
            (("one two", 5), "one two"),
            (("", 3), ""),
            (("one two three", 3), "one two three"),
            (("  spaced   out  words ", 2), "spaced out…"),
        ],
        "reference": '''
def truncate_words(text, limit):
    words = text.split()
    if len(words) <= limit:
        return " ".join(words)
    return " ".join(words[:limit]) + "\\u2026"
''',
    },
    {
        "id": "merge_deep",
        "prompt": "Write a Python function `merge_deep(a, b)` that recursively merges "
                  "dict b into dict a and returns a new dict, without mutating "
                  "either input. Return only the function.",
        "fn": "merge_deep",
        "cases": [
            (({"x": 1}, {"y": 2}), {"x": 1, "y": 2}),
            (({"a": {"b": 1}}, {"a": {"c": 2}}), {"a": {"b": 1, "c": 2}}),
            (({"a": {"b": 1}}, {"a": {"b": 9}}), {"a": {"b": 9}}),
            (({"a": 1}, {"a": {"b": 2}}), {"a": {"b": 2}}),
            (({}, {}), {}),
        ],
        "reference": '''
import copy
def merge_deep(a, b):
    out = copy.deepcopy(a)
    for k, v in b.items():
        if isinstance(out.get(k), dict) and isinstance(v, dict):
            out[k] = merge_deep(out[k], v)
        else:
            out[k] = copy.deepcopy(v)
    return out
''',
    },
    {
        "id": "topo_sort",
        "prompt": "Write a Python function `topo_sort(graph)` that takes a dict "
                  "mapping a node to the list of nodes it depends on, and returns a "
                  "list of nodes in dependency order. Raise ValueError on a cycle. "
                  "Return only the function.",
        "fn": "topo_sort",
        "cases": [
            (({"a": [], "b": ["a"]},), ["a", "b"]),
            (({"a": []},), ["a"]),
            (({},), []),
            (({"c": ["b"], "b": ["a"], "a": []},), ["a", "b", "c"]),
        ],
        "raises": [({"a": ["b"], "b": ["a"]},)],
        "reference": '''
def topo_sort(graph):
    order, state = [], {}
    def visit(n):
        if state.get(n) == 2:
            return
        if state.get(n) == 1:
            raise ValueError(f"cycle at {n}")
        state[n] = 1
        for dep in graph.get(n, []):
            visit(dep)
        state[n] = 2
        order.append(n)
    for node in graph:
        visit(node)
    return order
''',
    },
    {
        "id": "parse_csv_line",
        "prompt": "Write a Python function `parse_csv_line(line)` that splits one CSV "
                  "line into a list of fields, honouring double-quoted fields that "
                  "contain commas and doubled quotes as an escaped quote. Return only "
                  "the function.",
        "fn": "parse_csv_line",
        "cases": [
            (('a,b,c',), ["a", "b", "c"]),
            (('a,"b,c",d',), ["a", "b,c", "d"]),
            (('"say ""hi""",x',), ['say "hi"', "x"]),
            (('',), [""]),
            (('a,,c',), ["a", "", "c"]),
        ],
        "reference": '''
import csv, io
def parse_csv_line(line):
    return next(csv.reader(io.StringIO(line)), [""])
''',
    },
    {
        "id": "wrap_text",
        "prompt": "Write a Python function `wrap_text(text, width)` that wraps text to "
                  "lines no longer than `width` characters, breaking on spaces only, "
                  "and returns a list of lines. Return only the function.",
        "fn": "wrap_text",
        "cases": [
            (("the quick brown fox", 10), ["the quick", "brown fox"]),
            (("short", 10), ["short"]),
            (("", 10), []),
            (("aaaa bbbb", 4), ["aaaa", "bbbb"]),
            (("supercalifragilistic", 5), ["supercalifragilistic"]),
        ],
        "reference": '''
def wrap_text(text, width):
    lines, current = [], ""
    for word in text.split():
        candidate = f"{current} {word}".strip()
        if current and len(candidate) > width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines
''',
    },
    {
        "id": "percentile",
        "prompt": "Write a Python function `percentile(values, p)` that returns the "
                  "p-th percentile of a list of numbers using linear interpolation "
                  "between the two closest ranks, with p given from 0 to 100. Return "
                  "only the function.",
        "fn": "percentile",
        "cases": [
            (([1, 2, 3, 4], 50), 2.5),
            (([1, 2, 3, 4], 0), 1),
            (([1, 2, 3, 4], 100), 4),
            (([5], 50), 5),
            (([1, 2, 3, 4, 5], 25), 2.0),
        ],
        "reference": '''
def percentile(values, p):
    xs = sorted(values)
    if not xs:
        raise ValueError("empty")
    k = (len(xs) - 1) * p / 100
    lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)
''',
    },
]

# Deliverable prompts: ask the model to PRODUCE a thing. A clean answer is the
# thing itself, with no "Here's a draft…" wrapper and no "let me know if…" tail.
DELIVERABLES = [
    "Write a git commit message for a change that fixes an off-by-one error in the "
    "pagination offset.",
    "Write a two-sentence Slack message telling the team that staging is down until "
    "14:00.",
    "Write a one-paragraph out-of-office reply for two weeks of parental leave.",
    "Write a polite email declining a vendor demo invitation.",
    "Write a PR description for adding retry with exponential backoff to the payments "
    "client.",
    "Write the error message shown when a file upload exceeds the size limit.",
    "Write a changelog entry for a release that adds dark mode and fixes two crashes.",
    "Write a Slack message asking the team to review the on-call rota by Thursday.",
]
