# Changelog

Versions before 0.3.0 were never tagged; they are reconstructed from the git
history so the numbering has a spine.

## 0.4.0 — 2026-08-20

- **`unslop`**, a twentieth style, and the third in the Terse tier to take on
  slop. `no-slop` and `no-ai-slop` both work on voice; this one works on the
  mechanical tells underneath it: em dashes and colons used as connectors,
  curly quotes, title-case headings, bold labels that restate their own line,
  passive voice, `utilize` and `leverage`, abstract metaphor nouns like
  `substrate` and `vector`, and sentences that name a feeling where a mechanism
  belongs. It also carries the half most slop removers skip: have an opinion,
  vary the rhythm, let some mess in. Sterile writing is its own tell.
- Adapted from the [unslop skill](https://github.com/cursor/plugins/tree/main/pstack/skills/unslop)
  in `cursor/plugins` `pstack` by Lauren Tan, MIT. Their taxonomy, their
  self-audit question and much of their per-rule phrasing carry over,
  restructured into the house skeleton the way `wait-what` was. `cursor/plugins`
  licenses per plugin rather than at the repository root, so the notice to
  preserve is `pstack/LICENSE`; it is now in [LICENSE](LICENSE) alongside the
  other adapted sources, with the detail in
  [docs/CREDITS.md](docs/CREDITS.md).
- Measured, one rep through the benchmark harness. The engineering is intact:
  12/12 hidden tests pass on both arms. Deliverable purity goes from 1/8 clean
  unstyled to 7/8, the best of the three slop styles. The cost is scannability
  and length, and it is not small: answers run about 12% longer (569 to 640
  words), anchors per 100 words fall from 3.5 to 1.1, and the distance to the
  first anchor goes from 33 words to 172. That is rule 8 doing exactly what it
  says, converting bold labels and inline-header lists into prose. Pick this
  style for prose quality, not for skimming.
- This is the one style whose body breaks a local habit on purpose. Every other
  style file uses em dashes freely; a style that bans them and then uses them
  teaches the model the rule is optional, so `unslop.md` contains none, and no
  curly quotes either. Its guardrail block also carries a clause the others do
  not need: the punctuation and quote rules never rewrite a string literal, an
  error message, or quoted text.

## 0.3.0 — 2026-08-16

- **Every style now covers the failure modes of its own constraint.** A depth
  request suspends the length budget and the template; a requested artefact
  ships bare, with the persona stepping out of character inside it; scoped
  conditions and numbers are never widened or rounded off. Written in each
  style's own voice, and now convention 11 in the
  [format guide](docs/format-guide.md). Measured: unstyled Opus 5 returns 1 of
  8 deliverables without a wrapper, the styles 5–8 of 8.
- **Benchmark harness.** Four deterministic measurements per style, no LLM judge:
  work-equivalence on 12 tasks with hidden tests, size, text shape, deliverable
  purity. Both arms generate through the `claude` CLI with settings, `CLAUDE.md`,
  hooks, MCP and tools switched off, so the style file is the only variable.
  See [benchmarks/README.md](benchmarks/README.md).
- **`/style`**, a picker for switching the active style. Pages nineteen styles
  four at a time, writes to the settings file that matches where the style lives.
  Install with `install.sh style-command`, bundled in `--all`.
- **Other agents.** `install.sh --body <style>` prints a style body with the
  frontmatter stripped, for Codex, Cursor, Windsurf and anything reading
  `AGENTS.md` / `GEMINI.md`. See [docs/other-agents.md](docs/other-agents.md).
  No markers were added to the style files: the stripping happens outside, so
  no byte is spent inside the system prompt.

## 0.2.0 — 2026-08-07

- All 19 styles restructured to match the shape Claude Code uses for its own
  built-in styles: identity line, `# <Name> Style Active` marker, procedural
  rules. Styles written like documentation get treated like documentation.
- Everything human-facing removed from the style bodies — credits, links,
  before/after blocks. A body is injected verbatim into the system prompt, so
  those bytes were diluting the instructions. Attribution moved to
  [docs/CREDITS.md](docs/CREDITS.md).
- **`--enforce`**: a `UserPromptSubmit` hook that re-states the active style every
  turn. Claude Code does this for its built-in styles and not for custom ones,
  which is why custom voices fade in long sessions.
- Format guide rewritten around the native prompt shape.

## 0.1.0 — 2026-08-06

- First release. 19 styles across four tiers (Understand, Business, Terse, Fun),
  each credited to the author or standard it was distilled from.
- `install.sh` with per-style, `--all` and `--list` modes, and activation through
  `~/.claude/settings.json`.
- `style-maker` skill: an interview that generates a personal style.
- [Claudisms 2026 field guide](docs/claudisms-2026.md) and the
  [format guide](docs/format-guide.md).
