---
description: Switch the active Claude Code output style from a picker
argument-hint: "[style name | default]"
allowed-tools: Glob, Read, Write, Edit, AskUserQuestion
disable-model-invocation: true
---

Switch the active output style. Argument (may be empty): `$1`

Do exactly these five steps and nothing else. No summaries of the repo, no
suggestions, no extra file reads.

## 1. Find the installed styles

`Glob` both locations, expanding `~` to the user's home directory:

- user: `~/.claude/output-styles/*.md`
- project: `.claude/output-styles/*.md`, relative to the current directory

`Read` each file. Note its frontmatter `name:` and `description:`, and which of the
two locations it came from. When the same `name:` exists in both, keep the project
copy and drop the user copy — that is Claude Code's own precedence.

Note the style already active, so the picker can lead with it: read `outputStyle`
from `.claude/settings.local.json` if that file exists, otherwise from
`~/.claude/settings.json`.

If neither location has a single style file, say so in one line, point at
`https://github.com/smixs/awesome-claude-output-styles#install`, and stop.

## 2. Decide the target

If `$1` is not empty, match it case-insensitively against the `name:` values and
the filename stems. `default`, `none` and `off` all mean "remove the setting". No
match: say so, list the valid names, stop.

If `$1` is empty, ask with `AskUserQuestion`, header `Style`, question "Which
output style?". One option per style: label is its `name:`, description is its
frontmatter `description:`, prefixed with `Project style.` when it came from the
project directory, so the user can see which settings file is about to change.

The popup holds four options, and this collection ships nineteen styles, so page
them:

- Order: the active style first, then the rest alphabetically by `name:`. Stable
  across runs. Never order by modification time — installing several styles at
  once gives them near-identical timestamps and the pages come out shuffled.
- Every page carries `Default` ("Claude Code's built-in style, no custom
  instructions"), so switching off is always one click away.
- Three styles or fewer: one page holding all of them plus `Default`.
- More: each page holds two styles, `Default`, and `More styles…`. The last page
  holds up to three styles plus `Default`.
- Whatever the user types under Other is matched exactly like `$1`.

## 3. Pick the settings file

Take it from where the chosen style lives, so a style is never activated in a
project that does not have it:

- a user style → `~/.claude/settings.json`
- a project style → `.claude/settings.local.json`, which is personal and
  git-ignored by convention, so the choice stays out of a teammate's checkout

## 4. Write it

Treat each settings file as JSON, never as lines: a line edit corrupts a minified
or single-key file. `Read` the file and parse it first when it exists.

- A style was chosen: set the top-level `"outputStyle"` to that style's exact
  `name:` value. Add the key when absent, change the value when present, leave
  every other key untouched. When the file is missing or empty, `Write`
  `{ "outputStyle": "<Name>" }`.
- `Default` was chosen: remove `"outputStyle"` from **both** settings files.
  Clearing one leaves the other still setting a style, so "off" would not be off.
  When removing the key empties the object, write `{}` — an empty file is invalid
  JSON and Claude Code fails to load it. A file that is absent or has no
  `"outputStyle"` is left alone.

Keep the file valid JSON at every step.

## 5. Report

Two lines. What the style is now and which file you wrote. Then: it applies to the
next session, so run `/clear` or restart Claude Code.
