#!/usr/bin/env python3
"""Benchmark runner for the styles in this repo.

Four questions, each answered without an LLM judge:

  work      does the style change the code? 12 tasks with hidden tests, style off
            vs on, pass/fail is ground truth. This is the `keep-coding-instructions:
            true` promise, tested.
  size      how much shorter is the answer, per question.
  shape     does it get to the point and stay scannable (see metrics.py).
  purity    asked to produce a deliverable, does it hand back only the deliverable?

Usage:
  uv run benchmarks/run.py selfcheck
  uv run benchmarks/run.py run caveman executive [--reps 2] [--limit 4]
  uv run benchmarks/run.py run --all
  uv run benchmarks/run.py report

The default (no-style) arm is generated once and cached on disk, so adding a style
only costs the styled arm. Answers live in benchmarks/results/cache/.

WARNING: `work` executes model-generated Python locally, in a subprocess with a
timeout. Tasks are small pure functions, but run this on a machine you are willing
to hand that.
"""

import argparse
import concurrent.futures as cf
import json
import os
import re
import statistics
import subprocess
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import harness
import metrics
from tasks import DELIVERABLES, TASKS

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
QUESTIONS = os.path.join(HERE, "questions.jsonl")
TEST_TIMEOUT = 20

_CODE_BLOCK = re.compile(r"```(?:python|py)?\s*\n(.*?)```", re.S)

# Wrapper tells: framing addressed to the user, wrapped around the thing asked for.
_OPENER = re.compile(
    r"^\s*(?:\*\*)?(?:here'?s|here is|sure|certainly|of course|below is|below you|"
    r"i'?ve\s+(?:drafted|written|put together|got)|this is (?:a|the)|the following|"
    r"absolutely|happy to|got it|no problem|alright|okay[,!.]|ok[,!.])",
    re.I)
_CLOSER = re.compile(
    r"(?:let me know if you|want me to|happy to (?:adjust|tweak|revise|change|"
    r"shorten|expand|help)|i can (?:adjust|tweak|revise|shorten|expand)|"
    r"does this work|if you'?d like me to|hope this helps|just say the word|"
    r"feel free to (?:adjust|tweak|customize|edit|use))", re.I)
# A framing sentence that then introduces the real deliverable in a block.
_LEAD_IN = re.compile(r"[:.]\s*\n+\s*(?:>|```|\*\*)", re.S)


# --------------------------------------------------------------------------- work

def extract_code(text):
    """The Python the model actually wrote: fenced blocks, else the raw text."""
    blocks = _CODE_BLOCK.findall(text)
    return "\n\n".join(blocks) if blocks else text


def run_hidden_test(code, task):
    """Run one task's hidden test against `code`. Returns (passed, detail)."""
    script = textwrap.dedent("""
        import json, sys
        src = json.loads(sys.stdin.readline())
        cases = json.loads(sys.stdin.readline())
        raises = json.loads(sys.stdin.readline())
        fn_name = json.loads(sys.stdin.readline())
        ns = {}
        exec(src, ns)
        fn = ns.get(fn_name)
        if fn is None:
            print(json.dumps([False, "function %s not defined" % fn_name])); raise SystemExit
        for args, expected in cases:
            try:
                got = fn(*args)
            except Exception as e:
                print(json.dumps([False, "%r raised %s" % (args, e)])); raise SystemExit
            if got != expected:
                print(json.dumps([False, "%r -> %r, expected %r" % (args, got, expected)]))
                raise SystemExit
        for args in raises:
            try:
                fn(*args)
            except ValueError:
                continue
            except Exception as e:
                print(json.dumps([False, "%r raised %s, expected ValueError" % (args, e)]))
                raise SystemExit
            print(json.dumps([False, "%r did not raise" % (args,)])); raise SystemExit
        print(json.dumps([True, "ok"]))
    """)
    payload = "\n".join(json.dumps(x) for x in (
        code,
        [[list(a), e] for a, e in task["cases"]],
        [list(a) for a in task.get("raises", [])],
        task["fn"],
    ))
    try:
        out = subprocess.run([sys.executable, "-c", script], input=payload,
                             capture_output=True, text=True, timeout=TEST_TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, "timeout"
    line = out.stdout.strip().splitlines()[-1] if out.stdout.strip() else ""
    if not line:
        return False, (out.stderr.strip()[:200] or "no output")
    passed, detail = json.loads(line)
    return passed, detail


def selfcheck():
    """Prove the hidden tests are right before trusting any style result."""
    bad = 0
    for task in TASKS:
        passed, detail = run_hidden_test(task["reference"], task)
        print(f"{'ok  ' if passed else 'FAIL'} {task['id']}" + ("" if passed else f"  {detail}"))
        bad += 0 if passed else 1
    print(f"\n{len(TASKS) - bad}/{len(TASKS)} reference solutions pass their own tests")
    return 1 if bad else 0


# ------------------------------------------------------------------------- purity

def is_pure(text):
    """A deliverable is pure when it is the deliverable and nothing else.

    A fenced block is the deliverable, so it is never searched for wrapper
    tells — a commit message that says "as follows:" on its own third line is
    not a wrapper. What matters is the frame: anything left once the blocks are
    removed. An empty frame means the reply is the artefact and nothing else.
    """
    body = text.strip()
    if _CODE_BLOCK.search(body):
        frame = _CODE_BLOCK.sub("", body).strip()
        if not frame:
            return True, ""
        first = next((l for l in frame.splitlines() if l.strip()), "")
        if _OPENER.search(first):
            return False, "opener"
        if _CLOSER.search(frame):
            return False, "closer"
        return False, "framed"
    first = next((l for l in body.splitlines() if l.strip()), "")
    if _OPENER.search(first):
        return False, "opener"
    if _CLOSER.search(body):
        return False, "closer"
    if _LEAD_IN.search(body):
        return False, "lead-in"
    return True, ""


# ---------------------------------------------------------------------- the run

def _gen(prompt, body, rep, refresh=False):
    return harness.generate(prompt, body=body, rep=rep, refresh=refresh)


def _parallel(jobs, workers):
    with cf.ThreadPoolExecutor(max_workers=workers) as pool:
        return list(pool.map(lambda j: j(), jobs))


def measure_style(stem, path, reps, limit, workers, refresh):
    body = harness.style_body(path)
    questions = harness.load_jsonl(QUESTIONS)
    tasks = TASKS
    delivs = DELIVERABLES
    if limit:
        questions, tasks, delivs = questions[:limit], tasks[:limit], delivs[:limit]

    print(f"[{stem}] size+shape: {len(questions)} questions x {reps} reps x 2 arms")
    jobs = []
    for q in questions:
        for rep in range(reps):
            jobs.append(lambda q=q, r=rep: _gen(q["question"], None, r, refresh))
            jobs.append(lambda q=q, r=rep: _gen(q["question"], body, r, refresh))
    answers = _parallel(jobs, workers)
    default_ans = answers[0::2]
    styled_ans = answers[1::2]

    per_metric = {k: {"default": [], "styled": []} for k in metrics.KEYS}
    for arm, texts in (("default", default_ans), ("styled", styled_ans)):
        for text in texts:
            m = metrics.measure(text)
            for k in metrics.KEYS:
                per_metric[k][arm].append(m[k])
    reductions = [100 * (1 - s / d) if d else 0.0
                  for d, s in zip(per_metric["chars"]["default"],
                                  per_metric["chars"]["styled"])]

    print(f"[{stem}] work: {len(tasks)} tasks x {reps} reps x 2 arms")
    jobs = []
    for t in tasks:
        for rep in range(reps):
            jobs.append(lambda t=t, r=rep: _gen(t["prompt"], None, r, refresh))
            jobs.append(lambda t=t, r=rep: _gen(t["prompt"], body, r, refresh))
    code_ans = _parallel(jobs, workers)
    work = {"default_pass": 0, "styled_pass": 0, "n": 0, "failures": []}
    idx = 0
    for t in tasks:
        for rep in range(reps):
            for arm in ("default", "styled"):
                passed, detail = run_hidden_test(extract_code(code_ans[idx]), t)
                work[f"{arm}_pass"] += 1 if passed else 0
                if not passed:
                    work["failures"].append(f"{arm}:{t['id']}:rep{rep}: {detail}")
                idx += 1
            work["n"] += 1

    print(f"[{stem}] purity: {len(delivs)} deliverables x {reps} reps x 2 arms")
    jobs = []
    for d in delivs:
        for rep in range(reps):
            jobs.append(lambda d=d, r=rep: _gen(d, None, r, refresh))
            jobs.append(lambda d=d, r=rep: _gen(d, body, r, refresh))
    deliv_ans = _parallel(jobs, workers)
    purity = {"default_clean": 0, "styled_clean": 0, "n": 0}
    for i in range(0, len(deliv_ans), 2):
        purity["default_clean"] += 1 if is_pure(deliv_ans[i])[0] else 0
        purity["styled_clean"] += 1 if is_pure(deliv_ans[i + 1])[0] else 0
        purity["n"] += 1

    result = {
        "style": stem,
        "name": harness.style_name(path),
        "model": harness.MODEL,
        "reps": reps,
        "questions": len(questions),
        "size": {
            "chars_cut_pct_mean": round(statistics.mean(reductions), 1),
            "chars_cut_pct_median": round(statistics.median(reductions), 1),
            "chars_cut_pct_min": round(min(reductions), 1),
            "chars_cut_pct_max": round(max(reductions), 1),
        },
        "shape": {k: {"default": round(statistics.mean(v["default"]), 1),
                      "styled": round(statistics.mean(v["styled"]), 1)}
                  for k, v in per_metric.items()},
        "work": work,
        "purity": purity,
    }
    harness.write_json(os.path.join(RESULTS, f"{stem}.json"), result)
    return result


def print_style(r):
    w, p = r["work"], r["purity"]
    print(f"\n=== {r['name']} ({r['style']}) · {r['model']} · {r['reps']} rep(s)")
    print(f"  output cut       {r['size']['chars_cut_pct_mean']}% mean, "
          f"{r['size']['chars_cut_pct_median']}% median, "
          f"range {r['size']['chars_cut_pct_min']}–{r['size']['chars_cut_pct_max']}%")
    print(f"  hidden tests     default {w['default_pass']}/{w['n'] * r['reps']}, "
          f"styled {w['styled_pass']}/{w['n'] * r['reps']}")
    print(f"  deliverables     default {p['default_clean']}/{p['n']} clean, "
          f"styled {p['styled_clean']}/{p['n']} clean")
    print(f"  {'metric':<24}{'default':>10}{'styled':>10}   better")
    for k in metrics.KEYS:
        if k == "chars":
            continue
        v = r["shape"][k]
        print(f"  {k:<24}{v['default']:>10}{v['styled']:>10}   {metrics.BETTER[k]}")


def report():
    files = sorted(f for f in os.listdir(RESULTS) if f.endswith(".json")) \
        if os.path.isdir(RESULTS) else []
    rows = [json.load(open(os.path.join(RESULTS, f), encoding="utf-8")) for f in files]
    if not rows:
        print("no results yet: run `uv run benchmarks/run.py run --all` first")
        return 1
    head = (f"| {'Style':<16} | cut % | tests off/on | clean off/on | to point | "
            f"max sent | claudisms |")
    print(head)
    print("|" + "|".join(["-" * len(c) for c in head.split("|")[1:-1]]) + "|")
    for r in sorted(rows, key=lambda x: -x["size"]["chars_cut_pct_mean"]):
        w, p, s = r["work"], r["purity"], r["shape"]
        n = w["n"] * r["reps"]
        print(f"| {r['style']:<16} | {r['size']['chars_cut_pct_mean']:>5.1f} "
              f"| {w['default_pass']}/{n} → {w['styled_pass']}/{n} "
              f"| {p['default_clean']}/{p['n']} → {p['styled_clean']}/{p['n']} "
              f"| {s['words_to_first_anchor']['default']:.0f} → "
              f"{s['words_to_first_anchor']['styled']:.0f} "
              f"| {s['max_sentence_words']['default']:.0f} → "
              f"{s['max_sentence_words']['styled']:.0f} "
              f"| {s['claudisms_per_1000w']['default']:.2f} → "
              f"{s['claudisms_per_1000w']['styled']:.2f} |")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("selfcheck", help="run hidden tests against the reference solutions")
    sub.add_parser("report", help="table over everything in benchmarks/results/")
    run = sub.add_parser("run", help="benchmark one or more styles")
    run.add_argument("styles", nargs="*", help="style file stems, e.g. caveman")
    run.add_argument("--all", action="store_true", help="every style in the repo")
    run.add_argument("--reps", type=int, default=1, help="generations per cell")
    run.add_argument("--limit", type=int, default=0, help="first N items of each set")
    run.add_argument("--workers", type=int, default=4, help="parallel generations")
    run.add_argument("--refresh", action="store_true", help="ignore the answer cache")
    args = ap.parse_args()

    if args.cmd == "selfcheck":
        return selfcheck()
    if args.cmd == "report":
        return report()

    available = harness.styles()
    picked = list(available) if args.all else args.styles
    if not picked:
        return ap.error("name a style, or pass --all")
    unknown = [s for s in picked if s not in available]
    if unknown:
        return ap.error(f"unknown style(s): {', '.join(unknown)}. "
                        f"Available: {', '.join(available)}")
    failed = []
    for stem in picked:
        # One style dying (CLI timeout, transport error) must not throw away the
        # hour the other eighteen just spent. Their answers are cached anyway.
        try:
            print_style(measure_style(stem, available[stem], args.reps, args.limit,
                                      args.workers, args.refresh))
        except Exception as exc:
            failed.append(stem)
            print(f"[{stem}] FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
    if failed:
        print(f"\nfailed styles ({len(failed)}): {', '.join(failed)}", file=sys.stderr)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
