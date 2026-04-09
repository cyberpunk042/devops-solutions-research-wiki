---
title: "Synthesis: Context Mode — MCP Sandbox for Context Saving"
type: source-synthesis
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-context-mode
    type: documentation
    url: "https://github.com/mksglu/context-mode"
    file: raw/articles/mksglucontext-mode.md
    title: "mksglu/context-mode"
    ingested: 2026-04-09
tags: [context-mode, mcp, context-management, sandbox, session-continuity, fts5, bm25, rrf, hooks, think-in-code, claude-code-plugin, 12-platform]
---

# Synthesis: Context Mode — MCP Sandbox for Context Saving

## Summary

Context Mode is an MCP server and multi-platform plugin that solves the context window problem from three angles simultaneously: sandbox tools that prevent raw data from ever entering context (315 KB → 5.4 KB over a full session, 98% reduction), a SQLite-backed session tracking system that survives context compaction with full state restoration, and a "Think in Code" paradigm that mandates the LLM write scripts rather than process data directly. It supports 12 platforms (Claude Code, Gemini CLI, VS Code Copilot, Cursor, OpenCode, KiloCode, OpenClaw, Codex CLI, Antigravity, Kiro, Zed, Pi) with varying hook support levels, extends usable session length from ~30 minutes to ~3 hours, and uses an FTS5 knowledge base with BM25 ranking, Reciprocal Rank Fusion, and proximity reranking for precision retrieval. This complements — rather than replaces — the CLI-over-MCP pattern: context-mode sandboxes MCP tool output at execution time, while CLI+Skills avoids MCP schema overhead at session initialization time.

## Key Insights

### 1. The three-sided problem

Context Mode frames the context window problem as three distinct failure modes, each requiring a separate mechanism:

**Context flooding (raw data dumping):** Every unmediated MCP tool call injects its full payload into context. Playwright snapshot: 56.2 KB. Twenty GitHub issues: 58.9 KB. Access log (500 requests): 45.1 KB. Analytics CSV (500 rows): 85.5 KB. After 30 minutes of agent work, 40% of the context window is consumed by data the model already processed and no longer needs. The sandbox tools (`ctx_execute`, `ctx_execute_file`, `ctx_batch_execute`) intercept these calls: data is processed in an isolated subprocess and only `console.log()` output reaches context.

**Compaction amnesia:** When context fills, the agent compacts the conversation — dropping older messages. Without state tracking, the model forgets which files it was editing, pending tasks, resolved errors, and the last user request. Context-mode captures every meaningful session event in a per-project SQLite database. A PreCompact hook builds a priority-tiered snapshot (≤2 KB) before compaction fires; SessionStart re-injects the structured Session Guide on resumption. The model continues from the exact last user prompt with full working state intact.

**LLM-as-data-processor anti-pattern:** Reading 50 files into context to count functions is the wrong paradigm. The "Think in Code" principle codifies this: the LLM should write a script that does the counting and `console.log()` only the result. One script replaces ten tool calls and avoids 100x the context cost. This is enforced as a mandatory paradigm across all 12 supported platforms — it is not a suggestion but an architectural requirement of the system.

### 2. The 6 sandbox tools

| Tool | Purpose | Context saved |
|---|---|---|
| `ctx_batch_execute` | Run multiple commands + search multiple queries in ONE call | 986 KB → 62 KB |
| `ctx_execute` | Run code in 11 languages; only stdout enters context | 56 KB → 299 B |
| `ctx_execute_file` | Process files in sandbox; raw content never leaves | 45 KB → 155 B |
| `ctx_index` | Chunk markdown into FTS5 with BM25 ranking | 60 KB → 40 B |
| `ctx_search` | Query indexed content with multiple queries in one call | On-demand retrieval |
| `ctx_fetch_and_index` | Fetch URL, chunk and index; 24h TTL cache — repeat calls skip network | 60 KB → 40 B |

Four utility tools also exist: `ctx_stats` (session savings report), `ctx_doctor` (installation diagnostics), `ctx_upgrade` (version update), `ctx_purge` (delete all indexed content).

**Sandbox mechanics:** Each `ctx_execute` call spawns an isolated subprocess with its own process boundary — scripts cannot access each other's memory or state. Eleven language runtimes are available: JavaScript, TypeScript, Python, Shell, Ruby, Go, Rust, PHP, Perl, R, and Elixir. Bun is auto-detected for 3–5x faster JS/TS execution. Authenticated CLIs (`gh`, `aws`, `gcloud`, `kubectl`, `docker`) work via credential passthrough — environment variables and config paths are inherited without being exposed to the conversation.

**Intent-driven filtering:** When output exceeds 5 KB and an `intent` parameter is provided, context-mode switches to intent-driven filtering: full output is indexed into FTS5, then searched for sections matching the intent. Only relevant snippets are returned plus a vocabulary of searchable terms for follow-up queries.

**Progressive throttling on `ctx_search`:** Calls 1–3 return normal results (2 per query). Calls 4–8 return reduced results (1 per query) with a warning. Calls 9+ are blocked and redirected to `ctx_batch_execute`. This prevents search from becoming its own source of context accumulation in long sessions.

### 3. FTS5 knowledge base: BM25, RRF, and proximity reranking

The `ctx_index` tool chunks markdown content by headings while keeping code blocks intact, then stores chunks in a **SQLite FTS5** virtual table. The search pipeline has five layers:

**BM25 ranking:** Probabilistic relevance algorithm scoring documents by term frequency, inverse document frequency, and document length normalization. Titles and headings are weighted **5x** for navigational queries. Porter stemming is applied at index time so "running", "runs", and "ran" match the same stem.

**Reciprocal Rank Fusion (RRF):** Search runs two parallel strategies merged via RRF:
- Porter stemming: FTS5 MATCH with porter tokenizer — "caching" matches "cached", "caches", "cach"
- Trigram substring: FTS5 trigram tokenizer for partial strings — "useEff" finds "useEffect", "authenticat" finds "authentication"

RRF merges both ranked lists; a document ranking well in both strategies surfaces higher than one ranking well in only one. This replaces the previous cascading fallback approach.

**Proximity reranking:** Multi-term queries get an additional pass — results where query terms appear close together are boosted. `"session continuity"` ranks passages with adjacent terms higher than pages where "session" and "continuity" appear paragraphs apart.

**Fuzzy correction:** Levenshtein distance corrects typos before re-searching. "kuberntes" becomes "kubernetes", "autentication" becomes "authentication".

**Smart snippets:** Instead of returning the first N characters, context-mode finds where query terms appear in content and returns windows around those matches — extracting the important section, not the document header.

**TTL cache:** Indexed content persists in a per-project SQLite database at `~/.context-mode/content/`. When `ctx_fetch_and_index` is called for a URL indexed within the last 24 hours, the fetch is skipped entirely — the model searches the existing index. Cache hint returned is 0.3 KB vs. 48 KB+ for a fresh fetch. Stale content (>24h) is re-fetched silently. `force: true` bypasses cache regardless. 14-day cleanup removes old databases on startup. `--continue` sessions preserve indexed docs across restarts.

### 4. Session continuity: 5 hook types, priority-tiered snapshots

Full session continuity requires five hooks working in concert:

| Hook | Role | Captures |
|---|---|---|
| **PreToolUse** | Enforces sandbox routing before execution; blocks dangerous commands | Routing decisions |
| **PostToolUse** | Captures events after each tool call | File edits, git ops, errors, tasks, env changes |
| **UserPromptSubmit** | Captures user decisions and corrections | User corrections, role directives, intent, data references |
| **PreCompact** | Builds priority-tiered snapshot before conversation compaction | All session state in ≤2 KB XML |
| **SessionStart** | Restores state after compaction or `--continue` resume | Injects Session Guide into context |

**15-category event capture table (by priority):**

- P1 Critical: Files (read/edit/write/glob/grep), Tasks (create/update/complete), Rules (CLAUDE.md paths + content), User Prompts (every message)
- P2 High: Decisions (user corrections/preferences), Git (checkout/commit/merge/rebase/stash/push/pull), Errors (failures, non-zero exit codes), Environment (cwd changes, venv, nvm, conda, package installs)
- P3 Normal: MCP Tools (all `mcp__*` calls with counts), Subagents (agent tool invocations), Skills (slash command invocations), Role (persona/behavioral directives)
- P4 Low: Intent (session mode: investigate/implement/debug), Data (large user-pasted data >1 KB)

**Compaction survival sequence:**
```
PreCompact fires
  → Read all session events from SQLite
  → Build priority-tiered XML snapshot (≤2 KB)
  → Store snapshot in session_resume table

SessionStart fires (source: "compact")
  → Retrieve stored snapshot
  → Write structured events file → auto-indexed into FTS5
  → Build Session Guide with 15 categories
  → Inject <session_knowledge> directive into context
  → Model continues from last user prompt with full working state
```

If the 2 KB budget is tight, lower-priority events (intent, MCP tool counts) are dropped first. Critical state — active files, pending tasks, rules, key decisions — is always preserved.

**The Session Guide** contains 15 structured sections: Last Request (exact user prompt for seamless continuation), Tasks (checkbox format with `[x]`/`[ ]` status), Key Decisions, Files Modified, Unresolved Errors, Git operations, Project Rules, MCP Tools Used, Subagent Tasks, Skills Used, Environment, Data References, Session Intent, and User Role. Detailed event data is also indexed into FTS5 for on-demand retrieval.

### 5. 12-platform integration matrix

Context-mode supports 12 platforms with three integration architectures: plugin/extension (deep native integration), hook-capable (shell-command hooks), and MCP-only (no hooks). Hook support is the critical differentiator — hooks enforce routing programmatically (~98% savings) vs. instruction files that guide via prompting (~60% savings).

| Platform | Architecture | PreToolUse | PostToolUse | PreCompact | SessionStart | Session Completeness |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Claude Code** | Plugin marketplace | Yes | Yes | Yes | Yes | **Full** |
| **Gemini CLI** | Config file | Yes | Yes | Yes | Yes | **High** |
| **VS Code Copilot** | Config file | No | Yes | Yes | Yes | **High** |
| **OpenClaw** | Native gateway plugin | Plugin | Plugin | Plugin | Plugin | **High** |
| **Pi Coding Agent** | Extension | Yes (tool_call) | Yes (tool_result) | Yes (session_before_compact) | Yes (session_start) | **High** |
| **OpenCode** | TypeScript plugin | Plugin | Plugin | Plugin | No | **High** |
| **KiloCode** | TypeScript plugin | Plugin | Plugin | Plugin | Depends | **High** |
| **Cursor** | Config file | Yes | Yes | No | No | **Partial** |
| **Kiro** | Config file | Yes | Yes | No | No | **Partial** |
| **Codex CLI** | Config file | Ready | Ready | Ready | Ready | **Partial (pending dispatch)** |
| **Antigravity** | MCP-only | No | No | No | No | **None** |
| **Zed** | MCP-only | No | No | No | No | **None** |

**Platform-specific notes:**

- **Claude Code** (v1.0.33+): Install via `/plugin marketplace add mksglu/context-mode`. Plugin registers all 5 hooks automatically. No routing file written to project. Slash commands: `/context-mode:ctx-stats`, `/context-mode:ctx-doctor`, `/context-mode:ctx-upgrade`, `/context-mode:ctx-purge`. Only platform with plugin marketplace and slash command support.
- **Gemini CLI**: Single `~/.gemini/settings.json` file registers MCP + all 4 hooks. BeforeTool matcher targets only output-heavy tools (`run_shell_command`, `read_file`, `read_many_files`, `grep_search`, `search_file_content`, `web_fetch`) to avoid overhead on lightweight tools. Missing UserPromptSubmit so user decisions are not captured.
- **VS Code Copilot** (Copilot Chat v0.32+): Separate `.vscode/mcp.json` and `.github/hooks/context-mode.json`. Missing UserPromptSubmit.
- **Cursor**: Has `preToolUse`, `postToolUse`, and `stop` hooks. `sessionStart` rejected by Cursor's validator as of current versions. Routing via `.cursor/rules/context-mode.mdc`. Known limitation: `additional_context` in hook responses is not surfaced to the model.
- **OpenCode/KiloCode**: TypeScript plugin paradigm — hooks run as in-process functions via `tool.execute.before`, `tool.execute.after`, and `experimental.session.compacting`. Compaction recovery works; startup/resume restore blocked pending SessionStart implementation.
- **OpenClaw** (>2026.1.29): Native gateway plugin targeting Pi Agent sessions. Registers via `api.on()` lifecycle hooks and `api.registerHook()` commands — no separate MCP server process. 8 hooks total. Falls back to DB snapshot reconstruction on older gateway versions.
- **Codex CLI**: MCP tools work. Hook dispatch is `Stage::UnderDevelopment` (issue #16685). **Warning:** `codex exec` mode cancels all MCP tool calls in v0.118.0 due to `tool_call_mcp_elicitation` approval prompt — pin to ≤0.116.0 for exec-mode MCP.
- **Antigravity/Zed**: MCP-only, no hooks. Platform auto-detected via MCP protocol handshake (`clientInfo.name`). Routing via manually-copied instruction files only (~60% compliance).
- **Kiro**: `preToolUse`/`postToolUse` hooks work. `agentSpawn` (SessionStart equivalent) not yet wired. Requires manually copying `KIRO.md`.
- **Pi Coding Agent**: Extension model with full lifecycle hook support (`tool_call`, `tool_result`, `session_start`, `session_before_compact`).

### 6. Benchmark data

| Scenario | Raw | In Context | Saved |
|---|---|---|---|
| Playwright snapshot | 56.2 KB | 299 B | 99% |
| GitHub Issues (20) | 58.9 KB | 1.1 KB | 98% |
| Access log (500 requests) | 45.1 KB | 155 B | 100% |
| Context7 React docs | 5.9 KB | 261 B | 96% |
| Analytics CSV (500 rows) | 85.5 KB | 222 B | 100% |
| Git log (153 commits) | 11.6 KB | 107 B | 99% |
| Test output (30 suites) | 6.0 KB | 337 B | 95% |
| Repo research (subagent) | 986 KB | 62 KB | 94% |
| Large JSON API (20k records) | 7.5 MB | 0.9 KB | 99% |
| **Full session aggregate** | **315 KB** | **5.4 KB** | **98%** |

Session length extends from ~30 minutes to ~3 hours. The full benchmark covers 21 scenarios; these are the headline figures. **The 98% savings figure requires hooks to be active.** A single unrouted Playwright snapshot call can dump 56 KB into context, wiping out an entire session's worth of savings.

### 7. "Think in Code" as mandatory paradigm

"Think in Code" is not a tip — it is the foundational architectural principle of context-mode. The LLM should program the analysis, not compute it. Rather than reading 50 files into context to count functions, the model writes a script that counts them and `console.log()`s only the result. One script replaces ten tool calls and saves 100x context.

The principle is enforced across all 12 platforms via hooks (programmatic block of direct data-processing tool chains) or instruction files (routing guidance when hooks are unavailable). The paradigm shift requires treating the LLM as a code generator at all times — even for one-off data queries — rather than as a data processor that reads inputs and produces outputs within the conversation context.

### 8. Routing enforcement: hooks vs. instruction files

The compliance gap between enforcement mechanisms is measured and significant:

| Enforcement mechanism | Compliance | How it works |
|---|---|---|
| Hooks (programmatic) | ~98% saved | Intercepts tool calls before execution; can block commands; cannot be ignored |
| Instruction files only | ~60% saved | Guides model via prompt; model can deviate under load or complexity |

Routing instruction files were previously auto-written to project directories on first session start but this was disabled to prevent git tree pollution (issues #158, #164). Hook-capable platforms need no file — routing is injected programmatically. Non-hook platforms (Zed, Antigravity) require a one-time manual copy.

The 38-point compliance gap means that without hooks, approximately 40% of tool calls that should be sandboxed are not — each one potentially dumping tens of kilobytes into context. Hook-capable platforms should always enable hooks; instruction-file-only platforms should treat the 60% figure as the realistic expectation.

### 9. Security model

Context-mode enforces the same permission rules as the host platform but extends them into the MCP sandbox. A `sudo` block in Claude Code's `.claude/settings.json` also blocks `sudo` inside `ctx_execute`, `ctx_execute_file`, and `ctx_batch_execute`.

Permission syntax (Claude Code settings format, honored by all platforms):
```json
{
  "permissions": {
    "deny": ["Bash(sudo *)", "Bash(rm -rf /*)", "Read(.env)", "Read(**/.env*)"],
    "allow": ["Bash(git:*)", "Bash(npm:*)"]
  }
}
```

Commands chained with `&&`, `;`, or `|` are split — each segment is checked independently. `deny` always wins over `allow`. Project-level rules override global rules. Codex CLI security enforcement requires `codex_hooks` feature flag to be enabled.

### 10. OpenClaw native gateway integration

OpenClaw is the only platform where context-mode runs as a native gateway plugin rather than a separate MCP server process. Installation via `npm run install:openclaw` handles: `npm install`, `npm run build`, `better-sqlite3` native rebuild, extension registration in `runtime.json`, and gateway restart via SIGUSR1. Requires OpenClaw >2026.1.29 — older versions have a silent lifecycle hook failure bug from PR #9761. The plugin registers 8 hooks via `api.on()` (lifecycle) and `api.registerHook()` (commands). Falls back to DB snapshot reconstruction on older gateway versions. Targets Pi Agent sessions (Read/Write/Edit/Bash tools).

### 11. Relationship to CLI-over-MCP and the two-layer optimization

Context-mode and the CLI-over-MCP pattern attack different phases of the same problem:

**CLI+Skills addresses session initialization overhead:** MCP servers load their full JSON schema into context at startup regardless of whether tools are ever called. Skills inject instructions only when invoked. For a project-internal tool used on 30% of sessions, MCP wastes schema tokens on every session including the 70% where it is never needed.

**Context-mode addresses execution-time output overhead:** Given MCP tools you must use — Playwright, GitHub APIs, third-party integrations — how do you prevent their output from consuming context? Sandboxing processes data outside the context boundary.

The two strategies are orthogonal and stackable. A well-optimized agent could use CLI+Skills for internal tools (eliminating schema overhead) and context-mode for external MCP tools (eliminating output overhead). The unifying pattern is Context-Aware Tool Loading: load the minimum needed, when it is needed, for the immediate task. Context-mode extends this principle into the execution layer — not just which tool to load, but how to prevent the tool's output from accumulating.

The practical implication for the research wiki: the 15-tool `research-wiki` MCP server loads schema tokens at every session start. Context-mode would not address this (schema overhead is pre-execution). CLI+Skills is the right lever for schema overhead; context-mode is the right lever for the output side of wiki tool calls if they produce large responses.

### 12. Privacy, architecture, and licensing

All processing occurs in sandboxed subprocesses on the local machine. No telemetry, no cloud sync, no usage tracking, no account required. Session SQLite databases live in `~/.context-mode/` and are deleted at session end unless `--continue` is specified. Licensed under **Elastic License 2.0** (ELv2) — source-available but cannot be offered as a hosted/managed service or repackaged as competing closed-source SaaS. Bun is auto-detected as a runtime replacement for Node.js (3–5x faster JS/TS, no native compilation needed). On older glibc systems (CentOS 7/8, RHEL 7/8, Alpine without musl prebuilts), `better-sqlite3` falls back to compiling from source and requires a C++20 compiler.

## Open Questions

- How does context-mode interact with the research wiki's `research-wiki` MCP server? Context-mode addresses output overhead; the wiki MCP's 15-tool schema loads at initialization. Are both relevant simultaneously, or does the wiki's CLI+Skills fallback make context-mode less important here?
- Does `ctx_fetch_and_index` + `ctx_search` supersede the wiki's `wiki_fetch` + `wiki_search` workflow for ad-hoc URL research? The wiki provides structured knowledge with relationships and backlinks; context-mode provides fast indexed retrieval with TTL cache. Are these complementary layers?
- Could `ctx_execute` replace `Bash` calls in the wiki's ingestion pipeline to reduce context noise during long processing sessions (manifest rebuild, validate, lint, obsidian all run in sequence)?
- At what session length does context-mode's overhead (hook invocations, SQLite writes per tool call, snapshot construction) become worthwhile? The benchmarks show clear wins for 30-minute+ sessions — what is the break-even for a 5-minute targeted query?
- For fleet use cases (OpenFleet agents): would context-mode installed fleet-wide (via OpenClaw gateway plugin) reduce per-agent context pressure enough to justify the dependency? Each agent is already a Claude Code instance; compaction amnesia in long-running fleet tasks is a real failure mode.
- The `ctx_batch_execute` tool combines multiple commands + searches into a single call (986 KB → 62 KB). For the wiki's post-ingestion chain (6 sequential pipeline steps), would batching them via `ctx_batch_execute` materially reduce the context footprint of post-processing runs?
- What is the behavior when `ctx_execute` is called from within a subagent? The hook architecture captures subagent invocations as P3 events — but does the subagent's sandbox inherit the parent session's permission rules and credential passthrough?

## Relationships

- EXTENDS: Context-Aware Tool Loading
- COMPLEMENTS: CLI Tools Beat MCP for Token Efficiency
- IMPLEMENTS: Context-Aware Tool Loading
- RELATES TO: MCP Integration Architecture
- RELATES TO: Claude Code Context Management
- RELATES TO: Claude Code Skills
- RELATES TO: Claude Code
- RELATES TO: OpenClaw
- FEEDS INTO: Research Pipeline Orchestration
- FEEDS INTO: Wiki Ingestion Pipeline

## Backlinks

[[Context-Aware Tool Loading]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[MCP Integration Architecture]]
[[Claude Code Context Management]]
[[Claude Code Skills]]
[[Claude Code]]
[[OpenClaw]]
[[Research Pipeline Orchestration]]
[[Wiki Ingestion Pipeline]]
[[Hooks Lifecycle Architecture]]
