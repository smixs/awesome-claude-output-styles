# Changelog

Versions before 0.3.0 were never tagged; they are reconstructed from the git
history so the numbering has a spine.

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
