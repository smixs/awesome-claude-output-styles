---
name: style-maker
description: >
  Interviews the user with ~10 questions about how they want Claude to talk,
  optionally collects writing samples they like and hate, then generates a
  personal Claude Code output style file and activates it. Use when the user
  says "make my output style", "build me a custom style", "I want Claude to
  talk like...", "create a personal writing style", or complains about
  Claude's tone and wants a tailored fix rather than a preset.
---

# style-maker: interview → personal output style

Build the user a personal output style through a short interview, then write
it as `~/.claude/output-styles/<slug>.md` and activate it. The result must
follow the authoring conventions below — countable specs, positive framing,
guardrails — not a pile of adjectives.

## Step 1 — the interview (one block, ~10 questions)

Ask all questions in ONE message, numbered, so the user answers in a single
reply. Adapt wording to their language. Questions:

1. **Who are you, and who reads your answers?** (developer, founder, student,
   manager relaying to a team…)
2. **What annoys you most in Claude's current answers?** Paste one real
   answer you disliked, if you have it.
3. **Length:** short verdicts, medium, or full detail? Rough word cap?
4. **Jargon level:** full technical terms / terms defined on the spot / plain
   words only?
5. **Analogies:** love them, sometimes, or never?
6. **Format:** prose, bullets, numbered steps, tables? What should be rare?
7. **Tone dial** from dry-professional (1) to lively-casual (10) — pick a
   number. Profanity welcome, tolerated, or banned?
8. **Structure of a typical answer:** answer-first then reasons? Story?
   Steps? Whatever fits?
9. **What must NEVER be shortened or stylized?** (code, security notes,
   risk analysis, cost numbers…)
10. **Paste one or two short samples of writing you LIKE** (yours or anyone's)
    — and, if handy, one you find unbearable.

If the user skips questions, use sensible defaults and say which defaults you
picked. Do not re-ask; one round-trip, maybe two.

## Step 2 — synthesize the style

Turn answers into a style file. Hard conventions (each exists because it
measurably works — specs hold, adjectives drift):

- Frontmatter: `name` (Title Case, short), `description` (plain, what it
  does, no self-praise, no em dashes), `keep-coding-instructions: true`.
- **Mirror the built-in style structure** — the file body is injected into
  the system prompt verbatim, so write machine directives, not documentation.
  Body starts with the identity line: "You are an interactive agent that
  helps users with software engineering tasks. In addition to completing
  those tasks, you must <core directive>." Then a `# <Name> Style Active`
  header, then the rules ("In every response: …").
- **Specs, not adjectives.** Convert every preference into a checkable rule:
  "tone 3/10" becomes "no exclamation marks, no emoji, contractions
  allowed"; "shortish" becomes "core answer under 120 words".
- **Positive framing.** Describe the wanted voice with rules and examples.
  At most one or two negative rules, only where no positive equivalent
  exists. Never include lists of banned words — naming patterns summons
  them.
- **Mine the samples.** From liked samples extract: sentence length,
  person (I/we/you), rhythm, how they open and close, signature moves.
  Encode as rules + one imitation example. From the hated sample extract the
  *positive opposite* (it says "X annoys me" — write the rule for the
  opposite behavior, without quoting X).
- **Guardrails block, always:** code, commands, error messages, file paths,
  identifiers, and numbers stay byte-for-byte exact; plain complete language
  for security warnings, confirmations of destructive or irreversible
  actions, and multi-step instructions where order matters; plus everything
  the user listed in question 9. "Cut ceremony, not reasoning."
- **One positive example only** — the user's OWN pasted disliked answer
  rewritten in the new voice if they gave one, otherwise a realistic invented
  one from their domain. Never include the disliked original in the file:
  the body lands in the system prompt, and quoting a bad pattern there
  summons it every session.
- **Cover the failure modes of the constraint you just wrote.** Any budget,
  template or persona has cases where obeying it makes the answer worse, and
  the model will obey it straight into a wrong answer unless you say
  otherwise. Four rules, adapted to their voice:
  - A depth request ("explain it properly", "why did this happen") suspends
    the length budget and the template for that reply. Voice stays.
  - A requested artefact — commit message, email, snippet — is the whole
    reply, with nothing wrapped around it. A persona steps out of character
    inside the artefact.
  - Never widen a scoped condition ("only under load") into a blanket
    ("always"), never round off a number that makes a claim actionable.
  - Fewer words, not fewer points; a warning is the last thing cut.
- **A verify clause:** 1–3 countable self-checks derived from their top
  priorities.
- Keep the whole file under ~80 lines. A style is a lens, not a novel.

## Step 3 — show the draft, iterate

Show the full draft file in a code block, plus a live demo: answer one
realistic question from their domain in the new voice (pick one from the
interview context). Ask what to adjust. Apply edits until they approve.
One approval question is enough — do not loop endlessly.

## Step 4 — install and activate

1. Slugify the name (`My Style` → `my-style`) and write the file to
   `~/.claude/output-styles/<slug>.md`.
2. Set `"outputStyle": "<Name>"` in `~/.claude/settings.json` (merge the
   key, preserve everything else in the file; create the file if missing).
3. Tell the user: the style takes effect after restarting Claude Code or
   `/clear`; switch or turn it off anytime via `/config` → Output style.
4. Offer the enforcement hook: Claude Code re-reminds itself about built-in
   styles every turn but never about custom ones, so custom voices fade in
   long sessions. If the user wants the style permanently enforced, install
   [hooks/style-reminder.sh](https://github.com/smixs/awesome-claude-output-styles/blob/main/hooks/style-reminder.sh)
   to `~/.claude/hooks/` and register it under `hooks.UserPromptSubmit` in
   `~/.claude/settings.json` (the repo installer does this with `--enforce`).

## Notes

- The old `/output-style` command was removed in Claude Code v2.1.91 — never
  mention it; activation is `/config` or settings.json.
- If a style with the same slug exists, show it and ask: update it or pick a
  new name. Never overwrite silently.
