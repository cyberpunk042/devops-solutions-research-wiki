---
title: "Synthesis: pablo-mano/Obsidian-CLI-skill"
type: source-synthesis
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-09
sources:
  - id: src-pablo-mano-obsidian-cli-skill
    type: documentation
    url: "https://github.com/pablo-mano/Obsidian-CLI-skill"
    file: raw/articles/pablo-manoobsidian-cli-skill.md
    title: "pablo-mano/Obsidian-CLI-skill"
    ingested: 2026-04-08
tags: [obsidian, cli, claude-code, skill, vault-management, cross-agent, cursor, copilot, cortex-code, windsurf, nanoclaw, openclaw, ipc, headless, troubleshooting, marketplace, plugin, skill-portability]
---

# Synthesis: pablo-mano/Obsidian-CLI-skill

## Summary

This repository provides a comprehensive Claude Code skill (and multi-agent compatible plugin) that enables AI agents to control Obsidian vaults through the official Obsidian CLI introduced in v1.12. It covers 130+ commands across all major vault operation areas: file CRUD, daily notes, full-text search, properties, tags, tasks, links, bookmarks, templates, plugins, sync, themes, snippets, commands, bases, history, workspace, diff, developer tools, and vault management. The skill supports installation on Claude Code (as a plugin marketplace listing, direct load, or settings.json), Cursor, Cortex Code, GitHub Copilot, Windsurf, Nanoclaw, and Openclaw — plus any agent with a system prompt field — making it the most broadly compatible Obsidian skill available. It requires Obsidian Desktop v1.12+ with CLI enabled and the desktop app running (CLI communicates over IPC). Available as skill v1.3.0.

## Key Insights

- **130+ commands for full vault control**: Every major Obsidian operation area is covered. The command surface includes: Files (`read`, `create`, `append`, `prepend`, `move`, `rename`, `delete`, `files`, `folders`, `file`, `random`), Daily Notes (`daily`, `daily:read`, `daily:append`, `daily:prepend`, `daily:path`), Search (`search`, `search:context` with scoping, limits, JSON output), Properties (`properties`, `property:read`, `property:set`, `property:remove`, `aliases`), Tags (`tags`, `tag` with counts and filtering), Tasks (`tasks`, `task` — query, filter, toggle), Links (`backlinks`, `links`, `unresolved`, `orphans`, `deadends`), Bookmarks, Templates (`templates`, `template:read`, `template:insert`), Plugins (`plugins`, `plugin`, `plugin:enable/disable/install/uninstall`, `plugins:restrict`), Sync (`sync`, `sync:status`, `sync:history`, `sync:read`, `sync:restore`, `sync:deleted`), Themes (`themes`, `theme`, `theme:set`, `theme:install/uninstall`), Snippets (`snippets`, `snippets:enabled`, `snippet:enable/disable`), Commands (`commands`, `command`, `hotkeys`, `hotkey`), Bases (`bases`, `base:query`, `base:views`, `base:create`), History (`history`, `history:list`, `history:read`, `history:restore`), Workspace (`workspace`, `tabs`, `tab:open`), Diff (`diff`), Developer (`eval`, `dev:screenshot`, `dev:debug`, `dev:console`, `dev:errors`, `dev:css`, `dev:dom`, `devtools`), Vault (`vault`, `vaults`, `version`, `reload`, `restart`, `recents`, `outline`, `wordcount`).

- **Broadest agent compatibility**: Installation instructions cover 8+ different AI agents/editors — more than any other Obsidian skill. Claude Code (plugin marketplace, direct load, settings.json), Cursor (native skills system), Cortex Code (remote install, project-local, user-level), GitHub Copilot (repository-wide or path-scoped custom instructions), Windsurf (rules system with 12k char limit per file), Nanoclaw (`.claude/skills/` format), Openclaw (`skills/` directory format), and any agent with a system prompt field (paste SKILL.md content directly).

- **Three activation modes**: Natural language (usually works for clear Obsidian requests), explicit prefix `$obsidian-cli` (always works), and Strict Mode (always loaded via Claude Code settings). If Claude answers without executing commands, say "use obsidian-cli" to retry with the skill active.

- **Requires running desktop app**: The CLI communicates with Obsidian over IPC (inter-process communication), meaning the desktop application must be running. This is an architectural constraint that limits headless/server automation scenarios — though xvfb workarounds exist for headless Linux.

- **Platform-specific installation details**:
  - **macOS/Linux**: `obsidian` binary is added to PATH automatically when CLI is enabled in Settings
  - **Windows**: Requires an `Obsidian.com` redirector file placed alongside `Obsidian.exe`. Must run from a normal-privilege terminal — admin terminals produce silent failures
  - **Headless Linux**: Use `.deb` package (not snap). Run under `xvfb` and prefix commands with `DISPLAY=:5`. Set `PrivateTmp=false` if running as a systemd service (snap confinement restricts IPC)

- **Claude Code installation: 3 options**: Option A — Marketplace install (`/plugin marketplace add https://github.com/pablo-mano/Obsidian-CLI-skill` then `/plugin install obsidian-cli`), Option B — Direct plugin load (`claude --plugin-dir ./Obsidian-CLI-skill`), Option C — Persistent via `settings.json` with `"plugins": {"obsidian-cli": {"source": {"source": "github", "repo": "pablo-mano/Obsidian-CLI-skill"}}}`. The `.claude-plugin/marketplace.json` manifest makes the repository compatible with Claude Code's marketplace system.

- **Cursor installation**: Cursor launched a native skills system in Feb 2026 directly compatible with SKILL.md format — no rules file conversion needed. Install: clone repo to `/tmp`, copy `skills/obsidian-cli` to `~/.cursor/skills/obsidian-cli`, remove tmp. Cursor picks it up automatically without restart.

- **Cortex Code installation: 3 options**: Option A — Remote install (`/skill add https://github.com/pablo-mano/Obsidian-CLI-skill.git`); Option B — Project-local install (curl SKILL.md to `.cortex/skills/obsidian-cli/`); Option C — User-level install (copy to `~/.snowflake/cortex/skills/obsidian-cli/`). Verify with `/skill list`. Invoke with `$obsidian-cli` prefix or natural language.

- **GitHub Copilot installation**: Uses custom instructions feature. Option A — Repository-wide: create `.github/copilot-instructions.md` and paste SKILL.md body. Option B — Path-scoped: create `.github/instructions/obsidian-cli.instructions.md` with `applyTo: "**/*"` frontmatter.

- **Windsurf installation**: Uses Rules system (`.windsurf/rules/`). 12,000 character limit per file requires splitting across two files: `obsidian-cli.md` (SKILL.md body) and `obsidian-cli-reference.md` (command-reference.md). Set activation mode to Always On or Model Decision.

- **Nanoclaw and Openclaw**: Both directly compatible with SKILL.md format. Nanoclaw uses `.claude/skills/` directory; Openclaw uses `skills/` at project root. Copy skill folder and (re)start agent — skills auto-discovered.

- **SKILL.md as universal format**: For any agent without native skill support, paste the SKILL.md contents into the system prompt or custom instructions field. Optionally include the full command-reference.md for complete coverage. This makes the skill agent-agnostic by design.

- **Quick examples from README**:
  - Append to daily note: `obsidian daily:append content="- [ ] Review pull requests"`
  - Search vault with JSON output: `obsidian search query="meeting notes" format=json | jq '.[].path'`
  - Vault health check: `obsidian files total`, `obsidian tags counts sort=count`, `obsidian tasks`, `obsidian orphans`, `obsidian unresolved`
  - Create note from template with metadata: `obsidian create path="projects/new-feature" template="project-template"` then `obsidian property:set ...`

- **Troubleshooting matrix**: Common failure modes and fixes: empty output/hangs (Obsidian not running or admin terminal on Windows — start Obsidian; use normal-privilege terminal), `command not found` (re-enable CLI in Settings; restart terminal), Unicode errors (bug fixed in v1.12.2+ — update Obsidian), wrong vault targeted (pass vault name as first argument), IPC socket not found on Linux (`PrivateTmp=false` in systemd unit), snap confinement errors (use `.deb` package), `property:set` list value stored as string (edit frontmatter directly or use `eval`), colon+params exit 127 missing `.com` (reinstall from obsidian.md/download), colon+params exit 127 in Git Bash/MSYS2 (create `~/bin/obsidian` wrapper script pointing to `Obsidian.com`).

- **Full command reference**: `skills/obsidian-cli/references/command-reference.md` covers all commands, parameters, flags, output formatting, multi-vault usage, and headless Linux setup. This is the companion document for complete coverage beyond what SKILL.md summarizes.

- **Plugin marketplace distribution**: Uses Claude Code's marketplace system via a `.claude-plugin/marketplace.json` manifest, enabling one-command installation (`/plugin marketplace add`). This is the recommended distribution path for Claude Code users.

## Deep Analysis

This skill represents the deepest integration between an AI agent and Obsidian, leveraging the official CLI rather than browser automation or file-system manipulation. The 130+ command coverage means an AI agent with this skill has essentially the same level of vault control as a human user in the Obsidian UI.

The broad compatibility across 8+ agent platforms is a deliberate strategy. By providing installation instructions for Claude Code, Cursor, Cortex Code, Copilot, Windsurf, Nanoclaw, and Openclaw, the skill maximizes its potential user base while demonstrating that SKILL.md-format skills are not locked to any single platform. The universal fallback (paste into any system prompt) ensures the skill works with any AI agent ever built.

The IPC communication model (requiring the desktop app to be running) is both a strength and a limitation. It provides full access to Obsidian's capabilities through the official API, ensuring reliability and feature coverage. However, it prevents the skill from being used in CI/CD pipelines, cloud environments, or fully headless servers without workarounds.

The `eval` developer command (executes arbitrary JavaScript in the Obsidian context) is the most powerful and most dangerous command in the set. Since community plugins register their APIs into the Obsidian app context, `eval` is the plausible mechanism for invoking plugin-specific functionality beyond the official CLI surface — but this is not a documented, tested use case.

Compared to kepano/obsidian-skills which includes an obsidian-cli skill among its five skills, this repository goes dramatically deeper on CLI coverage specifically. The 130+ commands vs. the brief description in kepano's cli skill suggests this is a much more complete reference for AI agents that need comprehensive vault management capabilities.

The troubleshooting matrix is unusually comprehensive for a README. Documenting platform-specific failure modes (Windows admin terminal silent failures, Linux snap confinement, Git Bash `.com` redirector) signals production-grade usage context rather than a toy proof-of-concept.

## Open Questions

- How does performance scale with vault size when running commands like full-text search or orphan detection? (Requires: empirical benchmarking with large vaults; the Obsidian CLI page notes this as an open question and no wiki page documents CLI latency at scale)
- What is the maintenance burden of keeping the skill updated as Obsidian CLI evolves? (Requires: external observation over time; no wiki page documents the update cadence of the Obsidian CLI skill relative to Obsidian CLI releases)

### Answered Open Questions

**Q: Can the skill be extended to trigger Obsidian community plugin commands via the CLI?**

Cross-referencing `Obsidian CLI` and `Obsidian Skills Ecosystem`: the Obsidian CLI page documents a direct answer: "Does `obsidian eval` have access to community plugin APIs, enabling automation of Dataview queries, Templater scripts, and other plugin-specific operations? (Requires: external testing against community plugin APIs; the Obsidian Skills Ecosystem page describes what community plugins expose but does not document whether `eval` can invoke their APIs)." The `eval code=<js>` command "executes arbitrary JavaScript in the Obsidian context" — since community plugins register their APIs into the Obsidian app context, `eval` is the plausible mechanism for invoking them. However, no wiki page documents this as confirmed behavior. The pablo-mano skill's 130+ commands cover the official Obsidian CLI surface; community plugin extension is a separate capability layer that would require either `eval`-based workarounds or community plugin CLI hooks (not yet documented). The practical answer from existing wiki knowledge: the IPC-based CLI provides the `eval` command as a potential extension point, but community plugin triggering is not a documented, supported workflow in any existing wiki page.

**Q: How does the IPC-based CLI handle concurrent access from multiple AI agents?**

Cross-referencing `Obsidian CLI` and `WSL2 Development Patterns`: the Obsidian CLI page lists concurrent access as an open question: "How does the CLI handle concurrent access — can multiple scripts issue commands simultaneously without conflicts? (Requires: external testing or Obsidian documentation on IPC concurrency; no existing wiki page covers this)" — confirming no wiki page documents concurrent IPC behavior. The WSL2 Development Patterns page provides useful architectural context: the current project design avoids concurrent Obsidian access by using a two-daemon architecture where the wiki-watcher daemon detects changes and triggers the post-chain sequentially, and the wiki-sync daemon separately copies results to Windows. This sequential architecture sidesteps IPC concurrency concerns by design. For multi-agent scenarios where concurrent CLI access would be required, the WSL2 page notes the CLI must run on the same OS as the app, adding a coordination constraint. The wiki's current recommendation from these pages: design agent workflows to avoid concurrent Obsidian CLI calls; if concurrency is required, implement a command queue at the orchestration layer rather than relying on IPC to handle simultaneous requests safely.

## Relationships

- DERIVED FROM: src-pablo-mano-obsidian-cli-skill
- FEEDS INTO: Obsidian Skills Ecosystem
- EXTENDS: Claude Code Skills
- RELATES TO: Obsidian Knowledge Vault
- COMPARES TO: src-kepano-obsidian-skills

## Backlinks

[[src-pablo-mano-obsidian-cli-skill]]
[[Obsidian Skills Ecosystem]]
[[Claude Code Skills]]
[[Obsidian Knowledge Vault]]
[[src-kepano-obsidian-skills]]
