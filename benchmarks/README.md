# Benchmark

Does a style actually do what its description claims, and does it damage the work
on the way? Four measurements, **no LLM judge in any of them**, every number
reproducible from this directory.

A style is a system prompt. A system prompt that makes answers shorter can also
make them wrong, drop a warning, or quietly change the code. So the work and the
talking are measured separately.

| What | How | Claim it tests |
|---|---|---|
| **work** | 12 tasks with hidden tests, style off vs on, pass/fail | `keep-coding-instructions: true` — the engineering survives |
| **size** | characters cut per question, off vs on | "shorter" |
| **shape** | distance to the first anchor, longest anchor-free block, sentence length | "scannable", "≤20-word sentences" |
| **purity** | asked to produce a deliverable, is the reply only the deliverable? | "cut ceremony" |

## Run it

```bash
uv run benchmarks/run.py selfcheck
```

`selfcheck` runs every hidden test against a known-correct reference solution
first. A broken test would otherwise look like a broken style.

```bash
uv run benchmarks/run.py run caveman --limit 4
```

One style, first 4 items of each set — the cheap smoke test.

```bash
uv run benchmarks/run.py run --all --reps 2 --workers 6
```

Everything. Costs real tokens: 19 styles × 40 cells × 2 reps.

```bash
uv run benchmarks/run.py report
```

One table over every result in `results/`.

## Single variable

`harness.py` generates both arms through the `claude` CLI with the machine
switched off:

- `--setting-sources ""` — no user or project settings, no `CLAUDE.md`, no hooks,
  no ambient output style
- `--strict-mcp-config` — no MCP servers
- `--disallowedTools <all>` — no shell, no files, no web; the answer comes from the
  model's own knowledge
- an empty scratch working directory
- `--settings '{"outputStyle":"default"}'` — the default arm is genuinely vanilla

The styled arm adds one thing: the style file body on `--append-system-prompt`.
That is the only difference between the arms.

Answers are cached in `results/cache/` by (model, style body, prompt, rep). The
default arm is generated once and reused by every style, so style number 19 costs
the same as style number 2. Pass `--refresh` to ignore the cache.

## What the metrics mean

Classic reading grades (Flesch-Kincaid and its family) only see word and sentence
length, so a wall of short plain words scores "easy" on all of them. That is the
exact failure these styles exist to fix, so they are not used here. `metrics.py`
measures text shape instead:

- **words_to_first_anchor** — words read before the first bold or list marker.
  Lower is faster to the point. A prose-only style will score *worse* than default
  here, and that is a real trade-off, not a bug.
- **longest_wall_words** — the longest paragraph with nothing to grab.
- **max_sentence_words / over_20w_sentence_pct** — the ASD-STE100 20-word rule,
  counted. Directly checkable for `plain-english` and `wait-what`.
- **claudisms_per_1000w** — hits from [docs/claudisms-2026.md](../docs/claudisms-2026.md):
  the vocabulary and structure tells the `no-slop` styles target.

Markdown tables, fenced code and inline code are stripped before any prose metric.
A 6-column table is a layout, not a 60-word sentence.

## Config

| Variable | Default | Purpose |
|---|---|---|
| `BENCH_MODEL` | `claude-opus-5` | model under test |
| `BENCH_TIMEOUT` | `300` | seconds per generation |
| `BENCH_CACHE` | `benchmarks/results/cache` | answer cache |

## Limits

- **Work-equivalence is shown on small verifiable functions**, the class that has
  ground truth. It says nothing about open-ended design work.
- **Small n.** 20 questions, 12 tasks, 8 deliverables. Run `--reps 3` before
  trusting a small gap between two styles.
- The shape metrics are deterministic proxies for how a human reads. They are not
  a comprehension study.
- `run` executes model-generated Python locally, in a subprocess with a 20s
  timeout. The tasks are small pure functions, but that is still code from a model
  running on your machine.
