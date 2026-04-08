---
title: "MCP Integration Architecture"
type: concept
domain: automation
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-user-directive-integration
    type: notes
    file: raw/notes/2026-04-08-user-directive-integration-vision.md
    title: "User Directive — Integration Vision & Service Architecture"
    ingested: 2026-04-08
  - id: src-user-directive-ecosystem
    type: notes
    file: raw/notes/2026-04-08-user-directive-ecosystem-connections.md
    title: "User Directive — Ecosystem Connections & Automation Vision"
    ingested: 2026-04-08
tags: [mcp, model-context-protocol, integration, services, daemon, watcher, rsync, bidirectional-sync, claude-replaceable]
---

# MCP Integration Architecture

## Summary

The MCP Integration Architecture is the evolutionary target for the research wiki system — moving from CLI tools invoked by Claude Code to MCP servers that expose wiki operations as native tools in any Claude Code conversation. The user directive states: "By the end of all this you will do only what you absolutely need to be doing and you will even eventually be replaceable easily if needed." This means the system's intelligence lives in the tools, services, and MCP servers — not in Claude. Three MCP servers (wiki operations, NotebookLM, Obsidian), two service daemons (wiki watcher, WSL↔Windows rsync), and bidirectional sync with external systems. Claude focuses on reasoning, connections, questions, and standards — the mechanical work is offloaded to infrastructure.

## Key Insights

- **Three planned MCP servers**: (1) Wiki MCP — ingest, query, lint, export, stats, gap analysis as tools callable from any conversation. (2) NotebookLM MCP — push sources, query, generate artifacts via notebooklm-py. (3) Obsidian MCP — sync, detect changes, manage vault via Obsidian CLI.

- **Two service daemons**: (1) Wiki watcher — detects changes in wiki/, raw/, Obsidian vault, NotebookLM. Triggers appropriate pipeline stages automatically. (2) WSL↔Windows rsync daemon — keeps wiki/ synced to Windows Obsidian vault. Already prototyped in scripts/sync-obsidian.sh.

- **Bidirectional sync vision**: Detect when user adds a note in NotebookLM → ingest it. Detect when user edits in Obsidian → process changes. Detect when wiki changes → sync to Obsidian + notify. The system reacts to changes from any entry point.

- **Claude becomes replaceable**: The persistent intelligence is the wiki, tools, services, and MCP servers — not Claude. Any LLM that can call MCP tools can operate the system. Claude's unique value is reasoning quality, but the operational mechanics are LLM-agnostic.

- **Chain/group/tree orchestration via MCP**: MCP tools can be composed in conversations: "ingest these 5 URLs, then cross-reference, then export to openfleet" becomes a sequence of MCP tool calls. Group calls run in parallel (subagents each calling MCP tools). Tree operations branch and merge.

- **Entry point evolution**: Current: CLI tools + Claude Code conversation. Target: MCP servers (usable from any IDE, agent, or client), service daemons (autonomous operation), webhooks (external triggers), scheduled tasks (cron-based research runs).

## Deep Analysis

### MCP Server Designs

**Wiki MCP Server** (highest priority):
```
Tools:
  wiki_ingest(url_or_path, mode="smart")    → trigger ingestion pipeline
  wiki_query(question)                       → search wiki, return cited answer
  wiki_lint()                                → run lint, return report
  wiki_validate()                            → run validation, return errors
  wiki_stats()                               → return current wiki statistics
  wiki_export(target="openfleet")            → export to sister project
  wiki_gaps()                                → identify research priorities
  wiki_manifest()                            → regenerate and return manifest
```

**NotebookLM MCP Server** (wraps notebooklm-py):
```
Tools:
  nlm_create_notebook(title)                 → create NotebookLM notebook
  nlm_add_source(notebook_id, url_or_path)   → add source to notebook
  nlm_ask(notebook_id, question)             → query sources
  nlm_generate(notebook_id, type="audio")    → generate artifact
  nlm_download(notebook_id, type, path)      → download artifact
  nlm_research(notebook_id, query)           → trigger web research
```

**Obsidian MCP Server** (wraps Obsidian CLI):
```
Tools:
  obs_search(query)                          → search vault
  obs_read(file)                             → read note
  obs_create(name, content, template)        → create note
  obs_backlinks(file)                        → get backlinks
  obs_orphans()                              → find orphan pages
  obs_properties(file, format="json")        → read/set frontmatter
  obs_sync()                                 → trigger rsync to Windows
```

### Service Architecture

```
┌─────────────────────────────────────────────────────┐
│  Claude Code / Any MCP Client                        │
│  (reasoning, connections, questions, standards)       │
└──────────┬────────────┬────────────┬────────────────┘
           │            │            │
    ┌──────▼──────┐ ┌───▼────┐ ┌────▼─────┐
    │  Wiki MCP   │ │NLM MCP │ │ Obs MCP  │
    │  (port TBD) │ │(port)  │ │ (port)   │
    └──────┬──────┘ └───┬────┘ └────┬─────┘
           │            │            │
    ┌──────▼──────────────────────────▼──────┐
    │  tools/*.py    notebooklm-py  obsidian │
    │  (Python)      (Python/CLI)   (CLI)    │
    └──────┬──────────────────────────┬──────┘
           │                          │
    ┌──────▼──────┐          ┌───────▼───────┐
    │ Wiki Watcher │          │ rsync Daemon  │
    │ (inotify)    │          │ (WSL→Windows) │
    └──────────────┘          └───────────────┘
```

### Implementation Priority

1. **Wiki MCP** (unlocks: any conversation can query/modify wiki)
2. **rsync daemon** (unlocks: automatic Obsidian sync)
3. **Wiki watcher** (unlocks: reactive processing of new raw files)
4. **NotebookLM MCP** (unlocks: source mirroring, cross-validation)
5. **Obsidian MCP** (unlocks: bidirectional vault management)

## Open Questions

- How to handle MCP server authentication for multi-user scenarios? (Requires: external research on MCP auth patterns; not covered in existing wiki pages)
- Can one MCP server expose all three tool sets, or should they be separate servers? (Requires: external research on MCP server multi-namespace patterns; not covered in existing wiki pages)

### Answered Open Questions

**Q: What MCP framework to use? FastMCP (Python), TypeScript MCP SDK, or custom?**

Cross-referencing `Decision: MCP vs CLI for Tool Integration`: the decision page documents that the wiki already has a prototyped MCP server (`tools/mcp_server.py`) written in Python, with 15 tools exposed. The decision page also establishes that "CLI+Skills is the default preferred approach for operational tool integration" and that MCP is used "for external service bridges and tool discovery." Combining these: Python (FastMCP or the existing mcp_server.py implementation) is the correct framework choice for the wiki MCP server, since all existing tooling is Python and the `tools/mcp_server.py` file is already implemented. TypeScript MCP SDK would be appropriate only for the NotebookLM or Obsidian MCP servers if their integrations are TypeScript-native. For the planned three-server architecture, a Python framework for the Wiki MCP server (already proven) and TypeScript only where the integration requires it is the pragmatic choice.

**Q: Should the wiki watcher use inotify, polling, or git hooks for change detection?**

Cross-referencing `WSL2 Development Patterns`: the watcher architecture is definitively resolved. The `WSL2 Development Patterns` page documents: "inotify does not work reliably on /mnt/c — this matters for any daemon that watches files in Windows-accessible paths." The watcher must use polling for /mnt/c paths, and can use inotify for the Linux-side wiki/ path. The page further documents the two-daemon architecture: `tools/watcher.py` polls wiki/ on the Linux filesystem (where inotify is reliable) and `tools/sync.py` separately bridges to Windows. Git hooks are not appropriate here — they only fire on git operations, not on arbitrary file saves from Claude Code's Bash tool writes. The answer: polling for WSL2 wiki watching, with the Linux-side path kept on ext4 for reliable inotify if event-driven performance is ever needed.

**Q: What is the startup/shutdown lifecycle for service daemons on WSL2?**

Cross-referencing `WSL2 Development Patterns`: the lifecycle is fully documented. Service daemons deploy as systemd user services via `python -m tools.setup --services wiki-sync` (or `wiki-watcher`). This writes service files to `~/.config/systemd/user/` and runs `systemctl enable`. Systemd must be enabled in `/etc/wsl.conf` with `[boot] systemd=true` and a `wsl --shutdown` restart to take effect. The `WSL2 Development Patterns` page notes this is the ecosystem's IaC pattern applied to daemon lifecycle: no manual systemctl commands in CLAUDE.md, only reproducible setup scripts. The open question about what happens to user services after WSL2 restart is noted there — they should auto-restart if enabled, but this is flagged as needing verification.

## Relationships

- BUILDS ON: Wiki Ingestion Pipeline
- BUILDS ON: Obsidian CLI
- BUILDS ON: notebooklm-py CLI
- BUILDS ON: Claude Code
- ENABLES: Research Pipeline Orchestration
- RELATES TO: OpenFleet
- RELATES TO: AICP
- RELATES TO: Wiki Event-Driven Automation

## Backlinks

[[Wiki Ingestion Pipeline]]
[[Obsidian CLI]]
[[notebooklm-py CLI]]
[[Claude Code]]
[[Research Pipeline Orchestration]]
[[OpenFleet]]
[[AICP]]
[[Wiki Event-Driven Automation]]
[[Agent Orchestration Patterns]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Four-Project Ecosystem]]
[[Harness Engineering]]
[[Multi-Channel AI Agent Access]]
[[OpenArms]]
[[Plan Execute Review Cycle]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
[[WSL2 Development Patterns]]
