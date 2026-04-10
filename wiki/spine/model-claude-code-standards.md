---
title: "Claude Code Standards — What Good Agent Configuration Looks Like"
type: concept
domain: cross-domain
layer: spine
status: synthesized
confidence: high
maturity: seed
created: 2026-04-09
updated: 2026-04-09
sources:
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    url: "https://github.com/shanraisshan/claude-code-best-practice"
    title: "Claude Code Best Practices"
  - id: src-harness-engineering-article
    type: article
    url: "https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0"
    title: "Building Claude Code with Harness Engineering"
  - id: src-claude-code-accuracy-tips
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=D5bRTv6GhXk"
    title: "Claude Code Works Better When You Do This"
tags: [claude-code, standards, quality, configuration, skills, hooks, context-management, harness, gold-standard, anti-patterns]
---

# Claude Code Standards — What Good Agent Configuration Looks Like

## Summary

This page defines the quality bar for CLAUDE CODE CONFIGURATION. Where [[Model: Claude Code]] defines the system (agent loop, extension levels, context discipline, harness engineering), this page shows what GOOD looks like at every level — and what it looks like when configuration is wrong. ==Every gold standard on this page is a real instance from this ecosystem.== The harness is only as good as its weakest level: a perfect CLAUDE.md with no skills wastes context on every message. Perfect skills with no hooks have ~60% compliance. The standard is the full stack working together.

## Key Insights

- **CLAUDE.md quality is the highest-leverage configuration.** It loads on EVERY message. A 500-line CLAUDE.md wastes 500 tokens per message × every message × every session. A 180-line CLAUDE.md that routes to detailed files saves thousands of tokens per session while giving the agent the same access to information.

- **A skill is a system definition, not a text file.** The difference between a good skill and a bad skill is the same as the difference between a good model page and a reading list. A good skill teaches a CAPABILITY with progressive disclosure, gotchas, and scripts. A bad skill is a wall of instructions.

- **Hook enforcement is binary — it works or it doesn't.** There is no "partially enforced" hook. A PreToolUse hook either blocks the operation or it doesn't fire. The quality question is: are the RIGHT operations hooked? Not: are hooks "strong enough"?

- **The harness test is adoption.** Can someone clone this project, read CLAUDE.md, invoke a skill, and operate the system without prior knowledge? If yes, the harness is good. If they need to ask questions, the harness has gaps.

## Deep Analysis

### Gold Standard: CLAUDE.md

What a well-configured project root looks like.

> [!info] **Reference: this research wiki's CLAUDE.md** (~180 lines)

> [!success] **What makes it the standard**
> - **Under 200 lines** — respects the per-message cost. Every line is charged on every message in every conversation.
> - **Routes, doesn't contain** — points to `wiki/config/methodology.yaml` and `wiki/config/agent-directive.md` instead of containing 424 lines of methodology inline. Points to `config/wiki-schema.yaml` instead of embedding the schema.
> - **Structured as sections** — Project Structure, Page Schema, Ingestion Modes, Quality Gates, Post-Ingestion, Tooling, Agent Methodology, Conventions. The agent can scan section headers to find what it needs.
> - **Commands listed with exact syntax** — `python3 -m tools.pipeline post`, `python3 -m tools.validate`, etc. The agent doesn't guess the command format.
> - **Quality gates are explicit** — 9 gates listed, each with a testable condition (Summary ≥30 words, ≥1 relationship, title matches heading).
> - **Methodology section with stage gates** — the 5 stages, the rules (never skip, never rush, always log directives), per-scale artifact requirements. This is OPERATIONAL — the agent follows these rules because they're in CLAUDE.md.

> [!bug]- **Anti-pattern: the encyclopedia CLAUDE.md**
> A 500+ line CLAUDE.md that contains the full methodology, all schema definitions, all tool documentation, all conventions, and every rule ever learned. Loads on every message. 500 tokens wasted per message × 100 messages per session = 50,000 tokens burned on repeated context before any real work happens.
>
> **The fix:** CLAUDE.md as routing table. Point to files. `wiki/config/methodology.yaml` for methodology. `config/wiki-schema.yaml` for schema. Skills for capability instructions. CLAUDE.md tells the agent WHERE to look, not WHAT to know.

> [!bug]- **Anti-pattern: the empty CLAUDE.md**
> A project with no CLAUDE.md or a 10-line stub. Every conversation starts from zero. The agent doesn't know the project structure, conventions, or quality gates. It re-discovers them by reading files — burning tokens on exploration that should be free.
>
> **The fix:** Even a minimal CLAUDE.md (project structure, key commands, 3-5 conventions) gives the agent a foundation. 50 lines beats 0 lines. 180 lines is the sweet spot.

---

### Gold Standard: Skills

What a well-built skill looks like.

> [!info] **Reference: this wiki's `model-builder` skill** (skills/model-builder/skill.md)

> [!success] **What makes it the standard**
> - **Folder structure, not single file** — `skill.md` at root, with the option for `references/`, `scripts/`, `examples/` subdirectories
> - **Operations as clear triggers** — "Build a New Model", "Review an Existing Model", "Evolve a Model", "List All Models" — each with trigger phrases the model recognizes
> - **Process per operation** — Build follows 6 steps (Document → Design → Scaffold → Implement → Test → Update super-model). Not "create a model page" — a full workflow.
> - **Quality bar defined** — explicit checklist: ≥150 lines, define a SYSTEM not list pages, explain how to ADOPT, pass `pipeline post`
> - **Styling standards included** — the skill evolved to include callout vocabulary guidance, section-specific patterns, and a styling checklist. The skill teaches BOTH content and presentation.
> - **The super-model tree** — visual map showing where new models fit in the hierarchy. The skill carries structural knowledge, not just procedural.

> [!example]- **Reference: this wiki's `wiki-agent` skill**
> The wiki-agent skill teaches: 3 ingestion modes (auto, guided, smart), quality gates, post-ingestion chain, how to handle new domains, how to resolve contradictions, depth verification rule. It's a complete operational manual for wiki maintenance — not "use the wiki tools" but HOW to operate the wiki system.
>
> **Why it works:** A subagent loaded with just this skill and CLAUDE.md can ingest a source, create wiki pages, validate them, and maintain quality — without any other context. The skill is SELF-CONTAINED for its domain.

> [!bug]- **Anti-pattern: the instruction dump skill**
> A skill that is a wall of text: "When the user asks you to do X, do the following: step 1, step 2, step 3..." with no structure, no trigger phrases, no quality bar, no gotchas. The agent reads it but doesn't know WHEN to use it or HOW WELL the result should be.
>
> **The fix:** Structure every skill with: trigger phrases (when to load), operations (what it does), process (how to do each operation), quality bar (what "done" looks like), gotchas (known failure modes).

> [!bug]- **Anti-pattern: the skill that should be CLAUDE.md**
> A skill that contains project conventions, naming rules, and schema definitions. These load per-invocation instead of per-message. But if the agent needs them on EVERY task, they belong in CLAUDE.md, not a skill. Skills are for CAPABILITIES (things the agent does sometimes), not CONVENTIONS (things the agent follows always).
>
> **The diagnostic:** Is this information needed on every message regardless of task? → CLAUDE.md. Is it needed only when performing a specific operation? → Skill.

---

### Gold Standard: Hooks

What well-configured enforcement looks like.

> [!info] **Reference: claude-code-harness R01-R13 guardrail rules**

> [!success] **What makes it the standard**
> The 13 rules cover four enforcement categories:
>
> | Category | Rules | What they block |
> |----------|-------|----------------|
> | **Denial** | R01-R04 | `sudo`, `.git/` writes, `.env` writes, `--force` push |
> | **Query** | R05-R07 | Out-of-scope file writes, unexpected package installs |
> | **Security** | R08-R10 | `--no-verify`, direct main/master pushes, credential patterns |
> | **Post-execution** | R11-R13 | Assertion tampering, test skipping, coverage reduction |
>
> These are TypeScript hooks running as `PreToolUse` handlers. They return `block` to prevent the operation. ~98% compliance vs ~60% for instruction-only approaches. The difference is structural: instructions can be forgotten or overridden by the model's reasoning. Hooks execute at the infrastructure level — the model never gets to complete the blocked operation.

> [!example]- **How stage-gate enforcement should work via hooks**
> A `PreToolUse` hook for stage-gate methodology:
> 1. Read the current task's `current_stage` from frontmatter
> 2. If `current_stage = document`, block all `Write`/`Edit` calls to `src/`, `tools/`, `scripts/`
> 3. If `current_stage = scaffold`, block all `Write`/`Edit` that create files >50 lines (business logic signal)
> 4. If `current_stage = implement`, block all `Write`/`Edit` to test files
> 5. If `current_stage = test`, block all `Write`/`Edit` to source files
>
> This closes the gap between methodology (instructions in CLAUDE.md that get ~60% compliance) and enforcement (hooks that get ~98%). OpenArms Bug 5 — scaffold producing 135 lines of business logic — could not happen with this hook.
>
> **Status:** Not yet implemented in this wiki. Currently operating at enforcement levels 0-1 (prompt guidance + workflow orchestration). This is the planned next step.

> [!bug]- **Anti-pattern: hooks as instructions**
> A "hook" that writes a warning to the console but doesn't actually block the operation. "Warning: you are about to write to .env" — the agent sees the warning, reasons about it, and proceeds anyway. This is a notification, not enforcement.
>
> **The fix:** If an operation should be blocked, the hook must return `block`. If it should be flagged for human review, return `ask`. Warnings that the agent can ignore are instructions wearing hook costumes.

> [!bug]- **Anti-pattern: hooking everything**
> Every tool call has a PreToolUse and PostToolUse hook. Every file write triggers validation. Every Bash command gets security-scanned. The overhead compounds: each hook adds latency, and the agent spends more time waiting for hooks than doing work.
>
> **The fix:** Hook the DANGEROUS operations (sudo, force-push, .env, credential patterns) and the STRUCTURAL boundaries (stage gates). Leave routine operations (Read, Grep, Glob) unhitched. The 13 R01-R13 rules are a good ceiling — 13 rules cover the critical surface without drowning in noise.

---

### Gold Standard: Context Management

What disciplined context usage looks like in practice.

> [!success] **The research wiki session pattern (verified)**
> - CLAUDE.md at ~180 lines — lean routing table, not encyclopedia
> - Skills loaded only when needed — `/ingest` loads wiki-agent, `/build-model` loads model-builder, neither loaded by default
> - Subagents for bulk operations — parallel source fetching, evolution scoring, file exploration delegated to isolated workers
> - Targeted reads — `Read offset=50 limit=30` for specific sections, not whole-file reads of 1,000-line sources
> - Fresh sessions over infinite continuation — session summary transferred to new conversation when context feels heavy
> - `pipeline post` as the validation primitive — one command checks everything, no manual multi-step verification

> [!bug]- **Anti-pattern: the immortal session**
> A conversation that runs for hours, compacts 4+ times, and keeps going. Each compaction loses detail. By the 4th compaction, the agent has a summary of a summary of a summary — and makes confident claims about details it no longer has.
>
> **The fix:** At natural breakpoints (completed a task, finished an ingestion batch, hit a session milestone), start a fresh session with a transferred summary. This wiki uses `docs/SESSION-{date}.md` artifacts for exactly this purpose.

> [!bug]- **Anti-pattern: pre-loaded everything**
> 3 MCP servers connected (wiki, NotebookLM, Obsidian), all tool schemas loaded at startup. 5 skills pre-loaded in instructions. Full methodology.yaml inlined in CLAUDE.md. The conversation starts with 20,000 tokens of context before the user says anything.
>
> **The fix:** Connect only the MCP servers needed for this session. Load skills on demand. CLAUDE.md routes to files. Start lean, load as needed.

---

### Gold Standard: The Complete Harness

What all four levels working together looks like.

> [!info] **Reference: OpenArms deployment**
> | Level | Implementation | What it does |
> |-------|---------------|-------------|
> | 0 — CLAUDE.md | AGENTS.md (351 lines, symlinked) | Architecture boundaries, plugin SDK, channel protocol |
> | 0 — Progressive disclosure | Per-subsystem AGENTS.md files | `src/plugin-sdk/AGENTS.md`, `src/channels/AGENTS.md`, `src/gateway/AGENTS.md` |
> | 1 — Skills | 50+ skills, ClawHub marketplace | Each skill teaches one capability with setup + use phases |
> | 1 — Wiki | Embedded wiki with backlog | Epics, modules, tasks with frontmatter state machines |
> | 2 — Methodology | `methodology.yaml` + `agent-directive.md` | Stage gates, ALLOWED/FORBIDDEN per stage, work loop |
> | 2 — `read_when` | Docs declare their own relevance | Agents know WHEN to load a doc without reading everything |

> [!abstract] **What makes this a gold standard harness**
> - Every extension level is populated — not just CLAUDE.md and hope
> - Documentation layers have clear owners (CLAUDE.md = agent, wiki/ = knowledge, docs/ = humans, src/ = developers)
> - Methodology is enforceable — `methodology.yaml` defines what's allowed per stage, `agent-directive.md` defines the work loop
> - Skills are the capability layer — 50+ skills means the agent doesn't reconstruct knowledge from scratch
> - `read_when` metadata is an innovation — docs self-declare relevance so the agent doesn't have to read everything to decide what's relevant

> [!warning] **What's missing from OpenArms (and this wiki)**
> Neither project has Level 2 hooks for stage-gate enforcement yet. Both operate with instruction-based methodology (~60% compliance). The 13 R01-R13 guardrail rules from claude-code-harness demonstrate what Level 2 looks like — but neither ecosystem project has implemented them. This is the identified gap.

---

### Anti-Pattern Summary

| Anti-pattern | Level | What goes wrong | Fix |
|-------------|-------|----------------|-----|
| **Encyclopedia CLAUDE.md** | 0 | 500+ tokens wasted per message | Route to files, keep under 200 lines |
| **Empty CLAUDE.md** | 0 | Agent starts from zero every session | 50+ lines minimum — structure, commands, conventions |
| **Instruction dump skill** | 1 | Agent doesn't know when/how to use it | Trigger phrases, operations, process, quality bar, gotchas |
| **Skill as CLAUDE.md** | 1 | Per-invocation loading of always-needed info | Conventions → CLAUDE.md. Capabilities → Skills. |
| **Warning-only hooks** | 2 | Agent ignores warnings, proceeds anyway | Block the operation, don't warn about it |
| **Hook everything** | 2 | Latency drowns productivity | Hook dangerous ops and structural boundaries only |
| **Immortal session** | Context | Summary of summary of summary | Fresh sessions with transferred summaries |
| **Pre-loaded everything** | Context | 20K tokens before first message | Connect what's needed, load on demand |
| **No methodology** | All | Stages skipped, artifacts missing | methodology.yaml + agent-directive.md minimum |

---

### The Configuration Checklist

> [!tip] **Run this when setting up a new Claude Code project**
> - [ ] CLAUDE.md exists and is under 200 lines
> - [ ] CLAUDE.md routes to detailed files, doesn't contain them
> - [ ] At least 1 skill per major workflow, structured as a folder
> - [ ] Each skill has trigger phrases, process steps, and quality bar
> - [ ] Commands exist for user-facing skill triggers (`/command` per skill)
> - [ ] Safety hooks block dangerous operations (sudo, force-push, .env writes minimum)
> - [ ] MCP servers connected only when needed, not by default
> - [ ] Context management strategy documented (when to compact, when to fresh-session)

> [!tip] **Run this when reviewing an existing Claude Code project**
> - [ ] CLAUDE.md line count checked — still under 200?
> - [ ] Skills cover all major workflows — any manual processes that should be skills?
> - [ ] Hook coverage matches risk surface — any dangerous ops not hooked?
> - [ ] Context hygiene in practice — are sessions staying lean or ballooning?
> - [ ] Methodology enforcement — are stage gates followed or skipped? (check git log for stage-per-commit pattern)

## Open Questions

> [!question] **What is the ideal CLAUDE.md structure?**
> Should CLAUDE.md have a standardized section order across all projects? (Project Structure → Schema → Commands → Quality Gates → Methodology → Conventions?) Or should each project adapt freely? (Requires: comparing CLAUDE.md across 5+ projects)

> [!question] **Should skills have a quality schema?**
> Like wiki pages have `wiki-schema.yaml`, should skills have a validation schema checking for trigger phrases, operations, quality bar, and gotchas? (Requires: enough skills to see the pattern — currently 5 in this wiki, 50+ in OpenArms)

> [!question] **How do you test hooks without breaking things?**
> Hook testing requires triggering the blocked operation and verifying the block. But the blocked operation IS the dangerous thing. Dry-run mode for hooks? Test harness that simulates tool calls? (Requires: hook testing infrastructure design)

## Relationships

- BUILDS ON: [[Model: Claude Code]]
- BUILDS ON: [[Claude Code Best Practices]]
- RELATES TO: [[Harness Engineering]]
- RELATES TO: [[Hooks Lifecycle Architecture]]
- RELATES TO: [[Claude Code Skills]]
- RELATES TO: [[LLM Wiki Standards — What Good Looks Like]]
- RELATES TO: [[Wiki Design Standards — What Good Styling Looks Like]]
- RELATES TO: [[Methodology Standards — What Good Execution Looks Like]]

## Backlinks

[[Model: Claude Code]]
[[Claude Code Best Practices]]
[[Harness Engineering]]
[[Hooks Lifecycle Architecture]]
[[Claude Code Skills]]
[[LLM Wiki Standards — What Good Looks Like]]
[[Wiki Design Standards — What Good Styling Looks Like]]
[[Methodology Standards — What Good Execution Looks Like]]
[[Quality Standards — What Good Failure Prevention Looks Like]]
