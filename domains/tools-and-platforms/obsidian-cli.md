---
title: "Obsidian CLI"
type: concept
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-obsidian-cli-official
    type: documentation
    url: "https://help.obsidian.md/cli"
    file: raw/articles/obsidian-cli-official-docs.md
    title: "Obsidian CLI — Official Documentation"
    ingested: 2026-04-08
  - id: src-pablo-mano-obsidian-cli-skill
    type: documentation
    url: "https://github.com/pablo-mano/Obsidian-CLI-skill"
    file: raw/articles/pablo-manoobsidian-cli-skill.md
    title: "pablo-mano/Obsidian-CLI-skill"
    ingested: 2026-04-08
tags: [obsidian, cli, automation, scripting, tui, vault-management, pipeline-integration, agent-tools, second-brain]
---

# Obsidian CLI

## Summary

The Obsidian CLI is a first-party command-line interface shipping with Obsidian v1.12.7+ that exposes the full power of the Obsidian application to the terminal. It provides 130+ commands covering file operations, search, tags, properties, links, tasks, daily notes, plugins, sync, publish, themes, bases (databases), workspaces, and developer tooling. It supports both single-command execution and an interactive Terminal User Interface (TUI) with autocomplete, history, and reverse search. The CLI requires the Obsidian desktop app to be running (it auto-launches if not) and communicates via IPC, making it the canonical bridge between AI agents, shell scripts, cron jobs, and Obsidian vaults.

## Key Insights

- **Full app parity**: "Anything you can do in Obsidian you can do from the command line." This is not a subset — it covers file CRUD, search, link analysis, plugin management, sync, publish, themes, workspaces, properties, and developer tools.

- **Two execution modes**: Single-command mode (`obsidian search query="AI"`) for scripting and automation, and TUI mode (`obsidian` alone) for interactive exploration with autocomplete, command history, and Ctrl+R reverse search.

- **Vault targeting**: Commands default to the vault in the current working directory or the active vault. Override with `vault=<name>` or `vault=<id>` as the first parameter, enabling multi-vault scripting.

- **File resolution**: Two targeting modes — `file=<name>` (wikilink-style fuzzy resolution) and `path=<path>` (exact path from vault root). Use `path=` when filenames aren't unique.

- **Structured output**: Many commands support `format=json|csv|tsv|md` output, making results parseable by scripts, jq, and downstream tools. The `--copy` flag sends output to clipboard.

- **Link graph queries from the terminal**: `backlinks`, `links`, `unresolved`, `orphans`, `deadends` commands expose the same relationship graph that powers Obsidian's graph view, but in scriptable form.

- **Task management**: `tasks` command supports filtering by status, done/todo, daily, file, with JSON/TSV/CSV output. `task toggle` flips completion state by line reference.

- **Property (frontmatter) operations**: `property:set`, `property:read`, `property:remove` enable programmatic YAML frontmatter manipulation — critical for wiki systems that use structured metadata.

- **Plugin lifecycle management**: `plugin:install`, `plugin:enable`, `plugin:disable`, `plugin:uninstall`, `plugin:reload` — full plugin management without touching the GUI. Essential for automated vault setup.

- **Developer tooling**: `eval code=<js>` executes arbitrary JavaScript in the Obsidian context, `dev:cdp` exposes Chrome DevTools Protocol, `dev:screenshot` captures the app state. This enables deep automation beyond standard commands.

- **Publish integration**: `publish:add`, `publish:remove`, `publish:status` manage Obsidian Publish from the command line, enabling CI/CD-style publishing workflows.

- **Sync control**: `sync [on|off]`, `sync:status`, `sync:history`, `sync:restore` — pause, resume, and manage Obsidian Sync programmatically.

- **Platform setup varies**: macOS gets a symlink at `/usr/local/bin/obsidian`, Linux copies a binary to `~/.local/bin/obsidian` (needs PATH), Windows uses an `Obsidian.com` terminal redirector. All require the Settings > General > CLI toggle.

## Deep Analysis

### Why the CLI Changes Everything for Agent Workflows

Before the CLI, AI agents interacting with Obsidian had to either modify raw markdown files directly (bypassing Obsidian's indexing and plugin system) or use the `obsidian://` URI scheme (limited to opening files and basic navigation). The CLI eliminates this gap entirely — agents can now read vault state, modify content, query the link graph, manage plugins, and trigger sync through the same interface a power user would use.

For the research wiki specifically, the CLI enables:

1. **Bidirectional sync verification**: After `tools/obsidian.py` generates wikilinks and `scripts/sync-obsidian.sh` rsyncs to Windows, the CLI can verify vault state: `obsidian unresolved` checks for broken links, `obsidian orphans` finds disconnected pages, `obsidian search query="..."` confirms content landed correctly.

2. **Automated vault setup**: `scripts/configure-obsidian.sh` currently writes config files manually. The CLI's `plugin:install`, `plugin:enable`, `theme:install`, and `theme:set` commands could replace manual config with programmatic setup.

3. **Property-based automation**: Since wiki pages use YAML frontmatter (status, confidence, domain, etc.), the CLI's `property:set` and `property:read` commands enable scripts to update metadata without parsing markdown — e.g., marking pages stale, bumping confidence levels, or tagging domains.

4. **Task extraction pipeline**: `obsidian tasks format=json` + `obsidian tasks daily` could feed into project management integrations (Plane, openfleet), extracting action items from wiki pages automatically.

5. **Graph analysis from scripts**: `obsidian backlinks format=json`, `obsidian links`, `obsidian orphans`, `obsidian deadends` provide the same graph intelligence that `tools/manifest.py` builds manually — but from Obsidian's own live index, which includes community plugin extensions.

### Limitations for This Project

The CLI requires the Obsidian desktop app to be running. On WSL2, this means either:
- Running Obsidian on the Windows side and using the CLI through WSL→Windows interop (`/mnt/c/.../Obsidian.com`)
- Running Obsidian in WSL with a display server (xvfb or WSLg)
- Using the vault files directly (current approach) and reserving CLI for Windows-side operations

The current `scripts/sync-obsidian.sh` rsync approach sidesteps this by treating Obsidian as a read-only viewer. The CLI becomes relevant when we want Obsidian to be a read-write participant — detecting edits, updating properties, managing plugins.

### Command Categories by Automation Value

| Category | Commands | Automation Value |
|----------|----------|-----------------|
| Search & Analysis | search, backlinks, links, orphans, deadends, unresolved | High — graph intelligence |
| File Operations | create, read, append, prepend, move, rename, delete | High — content pipeline |
| Properties | property:set, property:read, property:remove | High — metadata automation |
| Tasks | tasks, task toggle | Medium — PM integration |
| Plugins | plugin:install/enable/disable/reload | Medium — vault setup |
| Daily Notes | daily, daily:append | Medium — journal automation |
| Sync/Publish | sync, publish:add | Medium — deployment pipeline |
| Developer | eval, dev:cdp, dev:screenshot | Low (niche) — debugging |

## Open Questions

- Can the Obsidian CLI be invoked from WSL2 targeting a Windows Obsidian instance, or does it require running on the same OS as the app?
- What is the latency overhead of CLI commands vs direct file manipulation for bulk operations (e.g., updating properties on 100+ pages)?
- Does `obsidian eval` have access to community plugin APIs, enabling automation of Dataview queries, Templater scripts, and other plugin-specific operations?
- Can the CLI's `base:query` command replace or augment `tools/manifest.py` for structured wiki querying?
- How does the CLI handle concurrent access — can multiple scripts issue commands simultaneously without conflicts?

## Relationships

- BUILDS ON: Obsidian Knowledge Vault
- ENABLES: Wiki Event-Driven Automation
- ENABLES: Obsidian Skills Ecosystem
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Claude Code Skills
- USED BY: AI-Driven Content Pipeline
- PARALLELS: notebooklm-py CLI
- ENABLES: Wiki Ingestion Pipeline

## Backlinks

[[Obsidian Knowledge Vault]]
[[Wiki Event-Driven Automation]]
[[Obsidian Skills Ecosystem]]
[[LLM Wiki Pattern]]
[[Claude Code Skills]]
[[AI-Driven Content Pipeline]]
[[notebooklm-py CLI]]
[[Wiki Ingestion Pipeline]]
[[Claude Code]]
[[MCP Integration Architecture]]
[[Research Pipeline Orchestration]]
