# User Directive — 2026-04-08 — Integration Vision & Service Architecture

## Verbatim

> There is a whole integation to do with obsidian and notebooklm cli and like I said toward making those even MCP to use in this conversation and make group and chain calls and trigger and manage and follow orchestrations. everything I talked about that are in the notes we will need to address.
> By the end of all this you will do only what you absolutely need to be doing and you will even eventually be replacable easily if needed.
> You will be able to sync and detect when I added a note on notebook or did something else and similar thing via obsidian. You will focus on the reasoning and making the right connection and generating the right questions and conclusions and estabiblishing and following the high standards.
>
> again you add this to notes and you make sure to plan for it. this clearly mean the entrypoint of this project will evolve and there will probably be a service or even two considering the optional wsl <-> winsdows rsync I talked about which we also need to do.

## Interpretation

### Architecture evolution — from CLI tools to services:

**1. MCP servers (new entry points):**
- Wiki operations exposed as MCP tools (ingest, query, lint, export, stats)
- NotebookLM operations exposed as MCP tools (push, query, create notebook)
- Obsidian operations exposed as MCP tools (sync, detect changes, manage vault)
- These MCPs allow Claude Code to use the wiki natively in any conversation

**2. Chain/group/tree orchestration:**
- Group calls: batch operations across multiple tools
- Chain calls: ingest → process → cross-reference → validate → sync in one operation
- Tree operations: parallel ingestion branches that merge into synthesis
- Trigger management: detect events (new file in Obsidian, new notebook in NotebookLM) and react

**3. Service layer (daemon/watcher):**
- Service 1: Wiki watcher — detects changes in wiki/, raw/, Obsidian vault, NotebookLM
- Service 2: WSL ↔ Windows rsync daemon — keeps wiki/ synced to Windows for Obsidian
- These run independently of Claude Code sessions

**4. Claude's role evolves:**
- Offload mechanical tasks to services and MCPs
- Claude focuses on: reasoning, connections, questions, conclusions, standards
- Eventually replaceable — the system works without Claude if needed
- The wiki, tools, services, and MCPs are the persistent intelligence

**5. Bidirectional sync:**
- Detect when user adds a note in NotebookLM → ingest it
- Detect when user adds/edits in Obsidian → process changes
- Detect when wiki changes → sync to Obsidian + notify
