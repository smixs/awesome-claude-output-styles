<p align="center">
  <img src="docs/assets/banner.jpg" alt="awesome-claude-output-styles" width="720">
</p>

<h1 align="center">awesome-claude-output-styles</h1>

<p align="center">
  <strong>same brain. twenty mouths.</strong>
</p>

<p align="center">
  Make Claude talk like a human. <strong>20 installable output styles</strong> for Claude Code,<br>
  each distilled from a <strong>credited author's methodology</strong> — from Boeing-manual English<br>
  to the Minto Pyramid to bedtime stories. One curl to install and switch.
</p>

<p align="center">
  <a href="https://github.com/smixs/awesome-claude-output-styles/stargazers"><img src="https://img.shields.io/github/stars/smixs/awesome-claude-output-styles?style=flat&color=yellow" alt="stars"></a>
  <a href="#the-styles"><img src="https://img.shields.io/badge/styles-20_across_4_tiers-orange?style=flat" alt="20 styles"></a>
  <a href="CHANGELOG.md"><img src="https://img.shields.io/badge/version-0.3.0-6f42c1?style=flat" alt="version"></a>
  <a href="benchmarks/"><img src="https://img.shields.io/badge/benchmarked-no_LLM_judge-2ea44f?style=flat" alt="benchmarked"></a>
  <a href="https://github.com/smixs/awesome-claude-output-styles/commits/main"><img src="https://img.shields.io/github/last-commit/smixs/awesome-claude-output-styles?style=flat" alt="last commit"></a>
  <a href="LICENSE"><img src="https://img.shields.io/github/license/smixs/awesome-claude-output-styles?style=flat" alt="license"></a>
</p>

<p align="center">
  <a href="#before--after">See it</a> ·
  <a href="#install">Install</a> ·
  <a href="#the-styles">The styles</a> ·
  <a href="#does-it-actually-work">Measured</a> ·
  <a href="#make-your-own-style-maker">Make your own</a> ·
  <a href="#shared-design-rules">Design rules</a> ·
  <a href="#the-wider-catalog">Catalog</a>
</p>

---

Output styles are the right layer for fixing Claude's voice: they rewrite the
system prompt itself and reframe the agent's identity around your voice —
unlike CLAUDE.md rules, which are injected as context alongside everything
else. Every style here mirrors the exact structure of Anthropic's built-in
styles (identity line, `Style Active` marker, procedural rules), and the
optional `--enforce` hook gives them the same per-turn reminder the built-ins
get from the harness. One markdown file each, correct 2026 frontmatter,
MIT-licensed, with the original author credited in the table below.

## Why

<p align="center">
  <a href="https://gruhn.me/blog/2026-08-03/">
    <img src="docs/assets/dont-be-a-meat-proxy.png" alt="Don't be a meat proxy — Niklas Gruhn, Aug 03 2026: 'NATS control-plane events: stream leader election / R3 quorum re-form during pod churn.' Jesus. I had to lookup almost every word to make sense of this." width="720">
  </a>
</p>
<p align="center"><sub>Niklas Gruhn, <a href="https://gruhn.me/blog/2026-08-03/">"Don't be a meat proxy"</a> · as shared by <a href="https://x.com/joshtriedcoding/status/2084571316263256150">Josh (@joshtriedcoding)</a></sub></p>

> Jesus. I had to lookup almost every word to make sense of this.

He's not alone — the August 2026 complaint threads run hundreds of upvotes,
and the word "Claudisms" now has [its own field guide](docs/claudisms-2026.md).
The model is brilliant; the register is exhausting. Pick a voice below and fix
it in one command.

## Before / after

Real, unedited Opus 5 voice, July 2026 threads:

> The reason your React component is re-rendering is likely because you're
> creating a new object reference on each render cycle, which breaks React's
> referential equality check, so you may want to consider memoization…

The same answer, seven voices:

<table>
<tr><th width="34%" align="left">Voice</th><th align="left">Same answer</th></tr>
<tr><td valign="top">

**`wait-what`**<br><sub>after **[Matt Pocock](https://github.com/mattpocock/skills)** ([@mattpocockuk](https://x.com/mattpocockuk)) — context first, ASD-STE100, your project's vocabulary</sub>

</td><td valign="top">

> We are hunting the extra re-renders in your list view. Your code creates a
> new object on each render. React sees a new object and draws again. Wrap
> the object in `useMemo`. Then React gets the same object and does not draw
> again.

</td></tr>
<tr><td valign="top">

**`caveman`**<br><sub>after [Julius Brussee](https://github.com/JuliusBrussee/caveman) ([@julius_brussee](https://x.com/julius_brussee)), 95k★</sub>

</td><td valign="top">

> New object ref each render. Inline object prop = new ref = re-render. Wrap
> in `useMemo`. Done.

</td></tr>
<tr><td valign="top">

**`no-ai-slop`**<br><sub>after **[Peter Yang](https://github.com/petergyang/no-ai-slop)** ([@petergyang](https://x.com/petergyang)) — direct, opinionated, zero filler</sub>

</td><td valign="top">

> The inline object is new on every render, and React compares props by
> identity — so it re-renders each time. Wrap it in `useMemo`. Don't reach
> for `React.memo` here: it treats the symptom, this fixes the cause.

</td></tr>
<tr><td valign="top">

**`no-slop`**<br><sub>the school of [Siqi Chen](https://github.com/blader/humanizer) ([@blader](https://x.com/blader)) — the anti-Claudism voice</sub>

</td><td valign="top">

> The component re-renders because the prop object is new each time, not
> because its contents changed. React checks identity, not contents. Wrap
> the object in `useMemo` and the identity stays stable.

</td></tr>
<tr><td valign="top">

**`unslop`**<br><sub>after [Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack)'s unslop skill (cursor/plugins) — surface tells out, an opinion in</sub>

</td><td valign="top">

> React compares props by identity, not by contents, so a fresh object literal
> on every render is a new reference and any memoized child sees a changed prop.
> Wrap it in `useMemo` with the values it depends on and the reference stays
> stable. If it holds no render-dependent state at all, hoist it to module
> scope so it is created once.

</td></tr>
<tr><td valign="top">

**`adhd`**<br><sub>after [Ayoub Ghriss](https://github.com/ayghri/i-have-adhd)'s i-have-adhd, 17k★</sub>

</td><td valign="top">

> Wrap the inline object in `useMemo` — that stops the re-renders (~2 min).
> Why: a new object every render makes React think the prop changed.

</td></tr>
<tr><td valign="top">

**`gen-z`**

</td><td valign="top">

> found it, no cap: you hand React a brand-new object every render, so it
> thinks something changed and redraws. wrap it in `useMemo` and it's a
> clean W.

</td></tr>
</table>

```
┌──────────────────────────────────────────────────┐
│  styles                          20              │
│  credited authors & standards    20+             │
│  code touched by any persona     never           │
│  jargon left unexplained         0, by spec      │
└──────────────────────────────────────────────────┘
```

## Install

One style (installs **and** activates it):

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- eli15
```

Everything (installs all 20 + the style-maker skill; activate later via `/config`):

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- --all
```

**After install — 3 steps.** Styles only load at session start, so nothing
changes until you **restart Claude Code**:

1. Restart Claude Code (or run `/clear`).
2. Type `/config` and find the **Output style** setting.
3. Pick the style you want from the list. Done — Claude answers in that voice
   from the next message on.

<p align="center">
  <img src="docs/assets/pick-style.gif" alt="Picking an output style: /config, then Output style, then choose from the list" width="600">
</p>

If you installed a single style, it's already selected — you only need step 1.
Switching back: `/config` → **Output style** → `Default`.

> [!TIP]
> The old `/output-style` command was removed in Claude Code v2.1.91 — most
> guides online still mention it and are outdated. `/config` is the way.

### Switching without `/config`: the `/style` command

Twenty styles do not fit a settings menu comfortably. `--all` installs the
`/style` command; on its own:

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- style-command
```

`/style` opens a picker over every style you have installed, four at a time,
with `Default` always one click away. `/style caveman` switches straight to
one. User styles are written to `~/.claude/settings.json`, project styles to
`.claude/settings.local.json`, so a personal preference never lands in a
teammate's checkout.

### Make it stick: `--enforce`

Claude Code reinforces its **built-in** styles every single turn — but never
custom ones, so custom voices fade over a long session. Add `--enforce` to any
install command and a tiny [`UserPromptSubmit` hook](hooks/style-reminder.sh)
gives whatever style you have active the same per-turn reinforcement:

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- eli15 --enforce
```

The hook is silent for built-in styles (no double reminders) and for
`default`. Remove it anytime by deleting the entry from
`~/.claude/settings.json` → `hooks.UserPromptSubmit`.

### Other agents

A style body is plain markdown; only the frontmatter is Claude Code's.
`--body` prints the body without it, ready to paste into any agent's rules
file:

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- --body caveman
```

Copy-paste commands for Codex, Cursor, Windsurf and `AGENTS.md` / `GEMINI.md`
agents: [docs/other-agents.md](docs/other-agents.md). Nothing is added to the
style files to make this work — no markers, no version stamps. Those bytes
would compete with the instructions in every session.

## The styles

### Understand — for explaining to humans

| Style | What it does | Method · author |
|---|---|---|
| [`wait-what`](output-styles/wait-what.md) | Context first, Simplified Technical English, your project's own vocabulary | **[Matt Pocock](https://github.com/mattpocock/skills)** ([@mattpocockuk](https://x.com/mattpocockuk)) — his wait-what skill as an always-on style |
| [`plain-english`](output-styles/plain-english.md) | ≤20-word sentences, one word one meaning, active voice | [ASD-STE100](https://www.asd-ste100.org/) (aerospace, 1983) · [Amin Boulegroun](https://github.com/AminBlg/SimpleEnglish) |
| [`eli15`](output-styles/eli15.md) | Smart-teenager explanations: one analogy, its breaking point, a line to remember | ELI5 prompt research · r/explainlikeimfive house rules |
| [`analogy-engine`](output-styles/analogy-engine.md) | One sustained analogy with part-by-part mapping | IEEE ProComm · Reijnierse et al. (JCOM 2025) · CMU metaphor checklist |
| [`feynman`](output-styles/feynman.md) | Teaches, names the hard part, checks understanding with questions | Richard Feynman's technique |
| [`thing-explainer`](output-styles/thing-explainer.md) | Only the ten hundred most common words | [Randall Munroe](https://xkcd.com/1133/) (xkcd, *Thing Explainer*) |
| [`ladder`](output-styles/ladder.md) | Every answer at 3 levels: like I'm 5 → 15 → pro | the classic r/PromptEngineering pattern |

### Business — for decision-makers

| Style | What it does | Method · author |
|---|---|---|
| [`executive`](output-styles/executive.md) | Answer first, ≤3 reasons, evidence on request | Barbara Minto's [Pyramid Principle](https://www.barbaraminto.com/) · BLUF · [Sruthi Reddy](https://github.com/sruthir28/enterprise-ai-skills) · [Joe Cotellese](https://joecotellese.com) ([@jcotellese](https://x.com/jcotellese)) |
| [`smart-brevity`](output-styles/smart-brevity.md) | 6-word tease, "Why it matters:", "Go deeper:" | Smart Brevity · Jim VandeHei, Mike Allen, Roy Schwartz (Axios) |
| [`coach`](output-styles/coach.md) | One note, one image, one next action | Hemingway App rules · Paul Graham's ["Write Like You Talk"](https://paulgraham.com/talk.html) · [Hardik Pandya](https://github.com/hardikpandya/stop-slop) ([@hvpandya](https://x.com/hvpandya)) |

### Terse — for speed

| Style | What it does | Method · author |
|---|---|---|
| [`caveman`](output-styles/caveman.md) | Ultra-compact: same signal, all fluff dropped | [Julius Brussee](https://github.com/JuliusBrussee/caveman) ([@julius_brussee](https://x.com/julius_brussee)) · [Carlos Duplar Mello](https://github.com/carlosduplar/caveman-output-style-claude-code) |
| [`adhd`](output-styles/adhd.md) | Action first, numbered steps, lists ≤5, visible progress | [Ayoub Ghriss](https://github.com/ayghri/i-have-adhd) · Ramsay & Rostain (*The Adult ADHD Tool Kit*) |
| [`no-slop`](output-styles/no-slop.md) | A plain, specific human voice — the anti-Claudism style | [Siqi Chen](https://github.com/blader/humanizer) ([@blader](https://x.com/blader)) · [Conor Bronsdon](https://github.com/conorbronsdon/avoid-ai-writing) ([@ConorBronsdon](https://x.com/ConorBronsdon)) · Joe Cotellese's generic-sentence test |
| [`no-ai-slop`](output-styles/no-ai-slop.md) | Direct, opinionated, zero filler — slop removed at the source | **[Peter Yang](https://github.com/petergyang/no-ai-slop)** ([@petergyang](https://x.com/petergyang)) — his editing principles as Claude's default voice |
| [`unslop`](output-styles/unslop.md) | Plain punctuation, concrete words, sentence-case headings, and an actual opinion | **[Lauren Tan](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)** (cursor/plugins `pstack`) — their 31 named patterns, plus the add-soul half most slop removers skip |

### Fun — personas that still get it right

| Style | What it does | Method · author |
|---|---|---|
| [`street`](output-styles/street.md) | Sharp senior engineer in modern street slang. **18+**, profanity | house style, sibling of [pohuy](https://github.com/smixs/pohuy) |
| [`gen-z`](output-styles/gen-z.md) | Brainrot wrapper, exact engineering inside. Slang dated by design | [Anirudh Konidala](https://github.com/kidskoding/gen-z-claude-bro) · [Steve Nims](https://github.com/sjnims/gen-alpha-output-style) |
| [`sportscaster`](output-styles/sportscaster.md) | Live play-by-play on your codebase | STAA Play-by-Play Pyramid · broadcasters' craft rules |
| [`yoda`](output-styles/yoda.md) | Plain answer first; the closing lesson, inverted it is | house style |
| [`bedtime-story`](output-styles/bedtime-story.md) | Concepts as tiny calming stories, real mechanism inside | house style |

## Make your own: style-maker

Presets not fitting? Install the interview skill:

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- style-maker
```

Then tell Claude **"make my output style"**. It asks ~10 questions (audience,
length, jargon level, tone, samples of writing you like and hate), generates
a personal style file following this repo's conventions — countable specs,
positive framing, safety guardrails — shows you a live demo, and activates it.

## Shared design rules

Every style in this hub follows the same conventions
(full authoring guide: [docs/format-guide.md](docs/format-guide.md)):

- **Specs, not adjectives.** "No sentence over 20 words" is checkable;
  "be clear" is not.
- **Positive framing.** Styles describe the voice they want. Ban lists summon
  the banned patterns — so the [Claudism list](docs/claudisms-2026.md) lives
  in docs for humans, not inside prompts.
- **Byte-exact guardrails.** Code, commands, error messages, file paths, and
  numbers are never stylized. Every persona shuts off for security warnings,
  destructive-action confirmations, and order-critical instructions.
- **Cut ceremony, not reasoning.** Styles shrink the wrapper, never the
  "why".
- **Every constraint names its own failure modes.** A depth request
  ("explain it properly", "why did this happen") suspends the length budget
  and the template. A requested artefact — commit message, email, snippet —
  is the whole reply, with the persona stepping out of character inside it.
  Scoped conditions and numbers are never widened or rounded off: a
  simplified fact is a wrong fact.
- `keep-coding-instructions: true` everywhere — the engineering stays intact.

## The wider catalog

Original-author projects worth knowing, beyond what's adapted here:

- [mattpocock/skills](https://github.com/mattpocock/skills) — Matt Pocock
  ([@mattpocockuk](https://x.com/mattpocockuk)): `wait-what`, the four-line
  re-pitch panic button, and `writing-for-agents`, the best methodology for
  writing agent-consumed docs. Install from his repo.
- [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman) — Julius
  Brussee ([@julius_brussee](https://x.com/julius_brussee)): the original,
  with six intensity levels, 30+ agent integrations and real benchmarks.
- [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) — Ayoub Ghriss:
  the top community answer to Opus 5 verbosity.
- [AminBlg/SimpleEnglish](https://github.com/AminBlg/SimpleEnglish) — Amin
  Boulegroun: ASD-STE100 enforcement with a deterministic linter.
- [blader/humanizer](https://github.com/blader/humanizer) — Siqi Chen
  ([@blader](https://x.com/blader)): the definitive AI-writing-pattern
  remover (33 patterns, self-audit loop).
- [petergyang/no-ai-slop](https://github.com/petergyang/no-ai-slop) — Peter
  Yang ([@petergyang](https://x.com/petergyang)): 20+ slop patterns with a
  voice-preservation-first stance and a self-check eval the skill runs on its
  own output.
- [cursor/plugins](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)
  — Lauren Tan's `unslop` skill in the `pstack` plugin: 31 numbered patterns in
  seven groups, with an "adding soul" half most slop removers skip.
- [hardikpandya/stop-slop](https://github.com/hardikpandya/stop-slop) —
  Hardik Pandya ([@hvpandya](https://x.com/hvpandya)): 8 rules plus a
  50-point scoring rubric.
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing)
  — Conor Bronsdon ([@ConorBronsdon](https://x.com/ConorBronsdon)): the most
  rigorous pattern catalog (61 categories, severity tiers).
- [nattergabriel/claude-code-output-styles](https://github.com/nattergabriel/claude-code-output-styles) —
  13 well-crafted styles (Socratic, Roast, Ship It…).
- [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) —
  the canonical Claude Code index, with an Output Styles category.

## Sister project

[**pohuy**](https://github.com/smixs/pohuy) — the Russian profanity output
style that started this collection. Same guardrails, four roots, 18+.

## Star this repo

If one of these voices saved you a re-read, a star helps the next person find
it — and helps the credited authors get found too. ⭐

## Contributing

PRs welcome. One style per PR, following
[docs/format-guide.md](docs/format-guide.md): built-in prompt structure
(identity line, `Style Active` header), countable specs, positive framing,
the shared guardrails block, one positive example, a verify clause, credits
in [docs/CREDITS.md](docs/CREDITS.md) — not in the style body. If you're the
original author of a methodology we adapted and want changes — open an issue,
you outrank us.

## License

[MIT](LICENSE). Adapted styles preserve their sources' copyright notices; see
[docs/CREDITS.md](docs/CREDITS.md) and the catalog tables above.

---

<sub>
<strong>Docs:</strong> <a href="docs/format-guide.md">Format guide</a> · <a href="docs/claudisms-2026.md">Claudisms field guide</a> · <a href="skills/style-maker/SKILL.md">style-maker</a> · <a href="https://github.com/smixs/awesome-claude-output-styles/issues">Issues</a>
<br>
<strong>Also by smixs:</strong> <a href="https://github.com/smixs/pohuy">pohuy</a> — Russian profanity output style · <a href="https://github.com/smixs/visual-skills">visual-skills</a> — image prompting skills
<br><br>
MIT — the voices are free; the credit stays with their authors.
</sub>
