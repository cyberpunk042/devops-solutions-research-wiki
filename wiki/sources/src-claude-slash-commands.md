---
title: "Claude Code Slash Commands (artemgetmann)"
type: source-synthesis
domain: ai-agents
status: synthesized
confidence: medium
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-claude-slash-commands
    type: github-repo
    url: https://github.com/artemgetmann/claude-slash-commands
    file: raw/articles/artemgetmannclaude-slash-commands.md
tags: [claude-code, slash-commands, commands, cli, automation, workflow]
---

# Claude Code Slash Commands (artemgetmann)

## Summary

A small open-source collection of reusable Claude Code slash commands installable globally (`~/.claude/commands/`) or per-project (`.claude/commands/`). Demonstrates command authoring patterns including frontmatter-based configuration, argument passing, file references, and scoped tool permissions — making it a practical reference for building custom command libraries.

## Key Insights

- **Two installation scopes**: personal (`~/.claude/commands/`) for cross-project availability vs. project-level (`.claude/commands/`) for team-shared workflows. The distinction enables a clean separation between individual power-user utilities and shared automation.

- **Frontmatter drives configuration**: Commands use YAML frontmatter (`allowed-tools`, `description`, `argument-hint`) to declare permissions and surface discoverability metadata. This is the authoritative interface contract for command authoring.

- **Three bundled commands**:
  - `/add-command` — interactive wizard for scaffolding new slash commands, teaches structure, security rules, and patterns in-context
  - `/askgpt5-web-search` — bridges Claude Code to GPT-5 web browsing for real-time data (requires OpenAI API key)
  - `/system-prompt-editor` — manages the global `CLAUDE.md` file (view, edit, backup), treating the system prompt as a versioned artifact

- **Security model**: Bash execution (`!command`) is sandboxed to the project directory; file references (`@file`) can access any path. `allowed-tools` acts as a capability declaration scoped per command.

- **`/add-command` as meta-command**: Including a command that teaches users how to write more commands is a self-bootstrapping pattern — the collection is designed to grow via its own tooling.

- **Cross-agent compatibility gap**: The `/askgpt5-web-search` command introduces an explicit dependency on a second AI provider (OpenAI). This is a signal that multi-model orchestration at the slash-command layer is an emerging pattern, not yet standardized.

## Open Questions

- Are there community conventions or registries for sharing slash command libraries across teams?
- How does command discovery work when both personal and project-level commands define the same name? (override behavior?)
- What's the versioning story for commands distributed this way — no lockfile or pinning mechanism shown.
- Does the `allowed-tools` restriction compose with Claude Code's global tool allowlist, or does it override it?

## Relationships

- EXTENDS: Claude Code Skills (adds concrete command examples to the skills architecture)
- IMPLEMENTS: Skills Architecture Patterns (demonstrates per-command tool scoping and argument patterns)
- RELATES TO: Claude Code Best Practices (command authoring is an extension of best practice guidance)
- RELATES TO: Claude Code (core platform this builds on)
- FEEDS INTO: Claude Code Scheduling (personal automation commands can be chained with scheduling)

## Backlinks

[[Claude Code Skills (adds concrete command examples to the skills architecture)]]
[[Skills Architecture Patterns (demonstrates per-command tool scoping and argument patterns)]]
[[Claude Code Best Practices (command authoring is an extension of best practice guidance)]]
[[Claude Code (core platform this builds on)]]
[[Claude Code Scheduling (personal automation commands can be chained with scheduling)]]
[[Per-Role Command Architecture]]
