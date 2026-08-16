# Using these styles with other agents

The body of every style is plain markdown with no Claude-Code-specific behaviour.
Only the YAML frontmatter is Claude Code's — the `name` / `description` block its
picker reads. Other agents either ignore frontmatter or choke on it, so strip it.

`install.sh --body` does that and prints the result to stdout:

```bash
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- --body caveman
```

Nothing is added to the file for this to work — no markers, no version stamps. A
style body is system-prompt text, and every byte in it competes with the
instructions, so the repo keeps it clean and does the stripping outside.

Swap `caveman` for any style from `--list`.

## Codex

Global instructions live in `~/.codex/AGENTS.md`. Fence the block so you can
update or remove it later without duplicates:

```bash
mkdir -p ~/.codex
{ printf '\n<!-- acos:start -->\n'
  curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- --body caveman
  printf '<!-- acos:end -->\n'; } >> ~/.codex/AGENTS.md
```

Before re-installing, delete the old block:

```bash
sed -i.bak '/<!-- acos:start -->/,/<!-- acos:end -->/d' ~/.codex/AGENTS.md
```

## Cursor

Project rules live in `.cursor/rules/`, as `.mdc` files with their own
frontmatter. `alwaysApply: true` makes the style permanent:

```bash
mkdir -p .cursor/rules
{ printf -- '---\ndescription: Output style\nalwaysApply: true\n---\n\n'
  curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh | bash -s -- --body caveman
} > .cursor/rules/output-style.mdc
```

## Windsurf

Project rules go in `.windsurf/rules/`:

```bash
mkdir -p .windsurf/rules
curl -fsSL https://raw.githubusercontent.com/smixs/awesome-claude-output-styles/main/install.sh \
  | bash -s -- --body caveman > .windsurf/rules/output-style.md
```

## Anything with AGENTS.md or GEMINI.md

Agents that walk up from the working directory looking for `AGENTS.md` or
`GEMINI.md` take the same fenced-append treatment as Codex. Put the file in your
repo root for one project, or in `~` for everything under your home directory.

## Notes

- These are instruction files, not output styles: nothing enforces them per turn.
  Inside Claude Code the [`--enforce` hook](../hooks/style-reminder.sh) does that;
  elsewhere expect the voice to fade over a long session.
- A style body is roughly 400–700 tokens of input, loaded once per session. Claude
  Code caches it after the first request; other agents may not. The benchmark
  measures the output savings at [20–40%](../benchmarks/README.md), so the input
  cost is paid back within a couple of replies either way.
- The `awk` strip inside `--body` needs a POSIX shell. On Windows use WSL or Git
  Bash.
