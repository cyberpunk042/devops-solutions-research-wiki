---
title: "Claude Code Best Practices"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    url: "https://github.com/shanraisshan/claude-code-best-practice"
    file: raw/articles/shanraisshanclaude-code-best-practice.md
    title: "shanraisshan/claude-code-best-practice"
    ingested: 2026-04-08
  - id: src-token-hacks-claude-code
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=49V-5Ock8LU"
    file: raw/transcripts/18-claude-code-token-hacks-in-18-minutes.txt
    title: "18 Claude Code Token Hacks in 18 Minutes"
    ingested: 2026-04-08
tags: [claude-code, best-practices, orchestration, plan-mode, subagents, skills, commands, hooks, workflows, prompting, git, debugging, development-workflow]
---

# Claude Code Best Practices

## Summary

Claude Code best practices encompass the patterns, habits, and architectural decisions that maximize output quality while minimizing token waste and wasted effort. Drawing from Boris Cherny (Claude Code's creator), Anthropic team members, and a large community of power users, these practices span the full development lifecycle: prompting strategy (challenge Claude, avoid micromanaging), planning discipline (always plan before executing, have Claude interview you), memory architecture (lean CLAUDE.md under 200 lines, rules in separate files), extensibility patterns (the Command-Agent-Skill hierarchy with progressive disclosure), workflow automation (hooks for formatting, safety, and monitoring), context hygiene (compact early, clear often, batch prompts), git discipline (small PRs, squash merges, frequent commits), and debugging techniques (screenshots, browser MCPs, background terminals). The overarching pattern is that all successful development workflows converge on a Research-Plan-Execute-Review-Ship cycle, regardless of which specific framework implements it.

## Key Insights

- **Plan before you build**: The single most consistently recommended practice across all sources. Use plan mode (or Opus for planning, Sonnet for execution) before any significant task. The biggest source of token waste is not expensive models -- it is Claude going down the wrong path and having to scrap work. Boris Cherny recommends: "Do not make any changes until you have 95% confidence in what you need to build. Ask me follow-up questions until you reach that confidence level."

- **Command-Agent-Skill architecture**: Claude Code's extensibility hierarchy has three layers. Commands are user-invoked prompt templates injected into the existing context (lightweight, for repeated workflows). Agents are autonomous actors in fresh isolated contexts with their own tools, permissions, model, and memory. Skills are configurable, preloadable knowledge bundles with progressive disclosure and context forking. The pattern is: Command orchestrates, Agent executes in isolation, Skill provides specialized knowledge.

- **Don't babysit, but do watch**: Several tips carry the "do not babysit" marker -- let Claude work autonomously on bug fixes, code generation, and exploration. However, watching the initial direction of a task prevents the catastrophic token waste of Claude going down a wrong path in a loop. The balance is: watch the first few steps, then let it run.

- **CLAUDE.md is an index, not an encyclopedia**: Keep it under 200 lines. Treat it as a routing table that tells Claude where to find detailed information, not as the detailed information itself. Every message re-reads the entire CLAUDE.md, so bloat compounds across every interaction. Use `.claude/rules/` for splitting large instruction sets. For persistent rules that must not be ignored, wrap them in `<important if="...">` tags.

- **Skills are folders with progressive disclosure**: A skill is not a single markdown file -- it is a folder containing a SKILL.md, references/, scripts/, and examples/ subdirectories. The SKILL.md description is a trigger written for the model ("when should I fire?"), not a human-readable summary. Include a Gotchas section that accumulates known failure points over time. Use `context: fork` to run skills in isolated subagents so intermediate tool calls do not pollute the main context.

- **Hooks as automation glue**: PostToolUse hooks for auto-formatting code (Claude generates well-formatted code, the hook handles the last 10%), PreToolUse hooks for measuring skill usage (finding undertriggering skills), Stop hooks to nudge Claude to verify or continue, and permission-routing hooks that send requests to Opus for automated safety classification. On-demand hooks in skills (like /careful to block destructive commands) add contextual safety.

- **All workflows converge on one pattern**: Ten major open-source Claude Code workflow frameworks (Everything Claude Code, Superpowers, Spec Kit, gstack, Get Shit Done, BMAD-METHOD, OpenSpec, oh-my-claudecode, Compound Engineering, HumanLayer) independently arrived at Research-Plan-Execute-Review-Ship. They differ in implementation (agents vs. commands vs. skills for the planning layer, different spec formats, different verification approaches) but the fundamental cycle is the same. This convergence suggests the pattern is inherent to effective AI-assisted development.

- **Agentic search beats RAG for code**: Claude Code tried and discarded vector databases internally because code drifts out of sync and permissions are complex. Glob + grep (agentic search) is both more accurate and simpler for navigating codebases. This mirrors the LLM Wiki Pattern's insight about structured files outperforming embeddings at moderate scale.

- **Git discipline amplifies everything**: Small, focused PRs (p50 of 118 lines), squash merges for clean history, committing at least once per hour, and using /code-review for multi-agent PR analysis. Tag @claude on a colleague's PR to auto-generate lint rules from recurring review feedback -- automating yourself out of code review.

- **Prototype over PRD**: Boris Cherny's counterintuitive advice: build 20-30 prototype versions instead of writing detailed specs, because the cost of building is now low enough to take many shots. This inverts the traditional spec-first workflow for exploratory features.

## Deep Analysis

The Claude Code best practices landscape reveals a fundamental tension between autonomy and control. The "don't babysit" philosophy (let Claude fix bugs without micromanaging, trust it to explore) coexists with the planning discipline (never let Claude start building without a vetted plan). The resolution is temporal: control at the planning phase, autonomy at the execution phase. Plan mode creates a contract; execution mode fulfills it.

The Command-Agent-Skill hierarchy represents Claude Code's answer to the age-old software engineering question of modularity. Commands are analogous to shell aliases -- lightweight, context-injected shortcuts. Agents are analogous to microservices -- isolated executors with their own state. Skills are analogous to libraries -- reusable knowledge packages that multiple agents can consume. The orchestration workflow (Command triggers Agent which loads Skills) mirrors the controller-service-library pattern in traditional architectures.

The convergence of 10 independent workflow frameworks on Research-Plan-Execute-Review-Ship is the strongest evidence that this is not just one approach among many but the effective workflow for AI-assisted development at current capability levels. The variation between frameworks is in implementation details, not fundamental structure. This suggests that investing in any framework that follows this pattern is likely to remain valuable even as specific tools evolve.

The "agentic search beats RAG" finding has implications beyond Claude Code. It suggests that for codebases and structured knowledge (as opposed to unstructured document collections), explicit file navigation by an agent outperforms similarity-based retrieval. This reinforces the LLM Wiki Pattern's approach and explains why the wiki pattern works surprisingly well despite having no embedding infrastructure.

The unsolved "billion-dollar questions" reveal the current frontier: why do models sometimes ignore explicit instructions in CLAUDE.md? When exactly should you use a command vs. an agent vs. a skill? Can a codebase be fully regenerated from specs? These are not just Claude Code questions -- they are fundamental questions about the reliability and completeness of LLM-driven development workflows that will define the next generation of tooling.

## Open Questions

- Why does Claude sometimes ignore CLAUDE.md instructions even when marked with MUST or ALWAYS? Is there a character/line threshold above which compliance drops? (Requires: external research or empirical testing; the accuracy tips source documents the context degradation curve — accuracy drops at 40% usage — which is a related mechanism, but the specific CLAUDE.md compliance threshold is not documented in existing wiki pages.)
- Can the Research-Plan-Execute-Review-Ship pattern be further optimized, or is it already at its minimum viable complexity? (Requires: external research or comparative analysis of workflow frameworks not yet ingested.)
- How do best practices change as models improve — does plan mode become less necessary as models get better at self-correction? (Requires: external research on model capability trajectories; not answerable from current wiki knowledge.)

## Answered Questions (moved from Open Questions)

### What is the decision tree for choosing between a command, an agent, and a skill?

Cross-referencing the Harness Engineering page and the Context-Aware Tool Loading pattern: the decision tree is documented implicitly across multiple sources and can now be stated explicitly. Use a **command** when: the workflow is a repeated prompt template that needs to be injected into the current context without isolation (no fresh context needed, no tool permission changes). Use an **agent** when: the task needs an isolated context (to prevent context pollution), parallel execution with other agents, or different tool permissions than the parent session. Use a **skill** when: specialized knowledge or operational procedures need to be loaded on demand without pre-loading overhead — skills provide progressive disclosure (SKILL.md + references/ + scripts/ + examples/) and support `context: fork` to run in isolated subagents. The Harness Engineering page documents the same pattern as a hierarchy: Level 2 (workflow orchestration via skills) sits below Level 3 (runtime guardrails via hooks) — meaning skills are the right tool for sequencing and knowledge, hooks are the right tool for enforcement.

### How do community skills and personal skills interact when they give conflicting instructions?

Cross-referencing the Context-Aware Tool Loading pattern: skill files are loaded contextually — they enter the context window when invoked, not at startup. This means precedence is governed by invocation order and CLAUDE.md routing, not by a registry-level priority system. The CLAUDE.md Best Practices page states CLAUDE.md should be an "index, not an encyclopedia" — it routes to the right skill. In practice, the precedence model is: CLAUDE.md project instructions override community defaults (CLAUDE.md is read on every message), personal skills loaded explicitly override ambient skills, and `<important if="...">` tags in CLAUDE.md provide the highest-priority override mechanism for rules that must not be ignored. There is no formal precedence specification beyond this in the existing wiki, but the architecture resolves most conflicts via explicit routing.

### What is the practical upper bound on skill complexity before a skill becomes unreliable?

Cross-referencing the CLI Tools Beat MCP for Token Efficiency lesson and the Context-Aware Tool Loading pattern: the reliability boundary for skills maps directly onto the context degradation curve. The accuracy tips source documents that Claude Code reliability drops significantly at 40% context usage and becomes unreliable at 60%+. A skill occupies context budget once loaded; a large skill (extensive SKILL.md + examples + scripts read into context) compounds the degradation curve sooner. The practical upper bound is not a fixed line count but a function of: (1) how much other context the session carries, (2) whether the skill is loaded alongside many other skills, and (3) whether the skill uses `context: fork` (isolated subagent clears this entirely). The actionable best practice from existing wiki knowledge: use `context: fork` for any skill whose instructions exceed ~100 lines to keep skill execution from polluting the main session context.

### Agentic search vs RAG: the domain-dependency resolution

Confirmed by cross-referencing the CLI Tools Beat MCP for Token Efficiency lesson and the LLM Wiki vs RAG comparison: the tension is resolved by domain. The "agentic search beats RAG" finding applies specifically to **code**, where content drifts out of sync with embeddings rapidly (every commit changes the ground truth). The LLM Wiki v2 hybrid search recommendation applies to **knowledge bases**, where content is curated and stable enough for semantic embeddings to remain valid. The CLI Tools lesson independently documents the same split: "CLI+Skills for project-internal tooling" (code-like domain, frequent change) vs. "MCP with vector indexing for cross-project discovery" (knowledge-like domain, stable). The best practice is explicitly domain-dependent: use agentic search (glob + grep or wiki navigation) for frequently-changing structured content; use hybrid search (BM25 + vector + graph) for stable curated knowledge bases.

### Skills as single files vs. structured folders: the complexity spectrum

Confirmed by cross-referencing the Context-Aware Tool Loading pattern and the Harness Engineering page: these are not conflicting descriptions but different points on a maturity spectrum. A seed skill is a single SKILL.md; a mature production skill is a folder with SKILL.md + references/ + scripts/ + examples/. The Harness Engineering page documents the same progression as its Pattern Hierarchy table — Level 0 (prompt guidance in a single file) evolves toward Level 3 (runtime guardrails with hooks and scripts). The actionable guidance from existing wiki knowledge: start with a single SKILL.md to validate the skill trigger and core instructions, then graduate to a folder structure when the skill accumulates external scripts, reference documents, or known failure cases (Gotchas section). The pattern mirrors how this wiki's own skills are structured.

## Relationships

- DERIVED FROM: src-shanraisshan-claude-code-best-practice
- DERIVED FROM: src-token-hacks-claude-code
- BUILDS ON: Claude Code Skills
- ENABLES: Claude Code Context Management
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Wiki Ingestion Pipeline
- RELATES TO: Wiki Event-Driven Automation
- RELATES TO: LLM Wiki vs RAG
- RELATES TO: Skills Architecture Patterns
- EXTENDS: Claude Code

## Backlinks

[[src-shanraisshan-claude-code-best-practice]]
[[src-token-hacks-claude-code]]
[[Claude Code Skills]]
[[Claude Code Context Management]]
[[LLM Wiki Pattern]]
[[Wiki Ingestion Pipeline]]
[[Wiki Event-Driven Automation]]
[[LLM Wiki vs RAG]]
[[Skills Architecture Patterns]]
[[Claude Code]]
[[Agent Orchestration Patterns]]
[[Agentic Search vs Vector Search]]
[[Always Plan Before Executing]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Harness Engineering]]
[[Infrastructure as Code Patterns]]
[[Plan Execute Review Cycle]]
[[Rework Prevention]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: 18 Claude Code Token Hacks in 18 Minutes]]
[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Claude Code Best Practice (shanraisshan)]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
