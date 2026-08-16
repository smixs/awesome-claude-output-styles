"""Hermetic answer generation for the style benchmark.

One job: get an answer to a prompt with a style OFF (default arm) or ON (styled
arm) under identical conditions, so the style file is the only variable.

Hermetic means the ambient machine is switched off: `--setting-sources ""` drops
user/project settings, CLAUDE.md and hooks; `--strict-mcp-config` drops MCP; every
tool is disallowed; the working directory is an empty scratch dir. Both arms then
answer from the model's own knowledge and runs reproduce.

Answers are cached on disk by (model, style body, prompt). The default arm is
generated once and reused by every style, which is where most of the cost goes.
"""

import hashlib
import json
import os
import re
import subprocess
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
CACHE = os.environ.get("BENCH_CACHE", os.path.join(HERE, "results", "cache"))

MODEL = os.environ.get("BENCH_MODEL", "claude-opus-5")
TIMEOUT = int(os.environ.get("BENCH_TIMEOUT", "300"))

# Every tool denied: a benchmark answer must come from the model's own knowledge,
# never from the operator's files, shell or network, or the two arms answer
# different questions and nothing reproduces.
_DISALLOWED = (
    "Bash,Read,Edit,Write,MultiEdit,NotebookEdit,Glob,Grep,Task,Agent,WebFetch,"
    "WebSearch,TodoWrite,BashOutput,KillBash,SlashCommand,ExitPlanMode"
)
_FORCE_DEFAULT_STYLE = json.dumps({"outputStyle": "default"})
_SCRATCH = os.path.join(tempfile.gettempdir(), "acos_bench_scratch")

_FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n", re.S)


def style_body(path):
    """The style file minus its YAML frontmatter — exactly the text Claude Code
    injects into the system prompt."""
    text = open(path, encoding="utf-8").read()
    body = _FRONTMATTER.sub("", text).strip()
    if not body:
        raise SystemExit(f"empty style body: {path}")
    return body


def style_name(path):
    for line in open(path, encoding="utf-8"):
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip()
    return os.path.splitext(os.path.basename(path))[0]


def styles():
    """Every style file in the repo, by stem."""
    d = os.path.join(REPO, "output-styles")
    return {os.path.splitext(f)[0]: os.path.join(d, f)
            for f in sorted(os.listdir(d)) if f.endswith(".md")}


def _cache_path(model, body, prompt, rep):
    key = "\0".join([model, body or "", prompt, str(rep)])
    return os.path.join(CACHE, hashlib.sha256(key.encode()).hexdigest() + ".txt")


def generate(prompt, body=None, rep=0, model=MODEL, refresh=False):
    """One hermetic answer. body=None is the default arm, a string is styled.

    `rep` only varies the cache key, so repeated runs sample the model again
    instead of returning the same cached text.
    """
    os.makedirs(CACHE, exist_ok=True)
    os.makedirs(_SCRATCH, exist_ok=True)
    path = _cache_path(model, body, prompt, rep)
    if os.path.exists(path) and not refresh:
        return open(path, encoding="utf-8").read()

    cmd = ["claude", "-p",
           "--model", model,
           "--setting-sources", "",
           "--strict-mcp-config",
           "--disallowedTools", _DISALLOWED,
           "--settings", _FORCE_DEFAULT_STYLE]
    if body:
        cmd += ["--append-system-prompt", body]
    # The prompt goes in on stdin: --disallowedTools is variadic and would
    # swallow a positional prompt.
    run = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                         timeout=TIMEOUT, cwd=_SCRATCH)
    if run.returncode != 0:
        raise RuntimeError(f"generate failed: {run.stderr.strip()[:400]}")
    answer = run.stdout.strip()
    with open(path, "w", encoding="utf-8") as f:
        f.write(answer)
    return answer


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
