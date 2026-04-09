---
title: "Synthesis: Claude Code Best Practice (shanraisshan)"
type: source-synthesis
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-09
sources:
  - id: src-shanraisshan-claude-code-best-practice
    type: documentation
    url: "https://github.com/shanraisshan/claude-code-best-practice"
    file: raw/articles/shanraisshanclaude-code-best-practice.md
    title: "shanraisshan/claude-code-best-practice"
    ingested: 2026-04-08
tags: [claude-code, best-practices, subagents, commands, skills, hooks, orchestration, workflows, CLAUDE-md, tips, boris-cherny, context-engineering, git, debugging, planning, specs, hot-features, billion-dollar-questions, development-workflows]
---

# Synthesis: Claude Code Best Practice (shanraisshan)

## Summary

A community-maintained GitHub repository (142k+ stars, trending #1 on GitHub) cataloging Claude Code best practices, tips, architectural patterns, and development workflows. It covers the full Claude Code feature surface — subagents, commands, skills, hooks, MCP servers, plugins, settings, memory (CLAUDE.md), checkpointing, and CLI flags — aggregating 69 tips from Boris Cherny (Claude Code's creator), Thariq, Cat Wu, and community contributors. It also catalogs 10 major open-source development workflow frameworks (Everything Claude Code, Superpowers, Spec Kit, gstack, Get Shit Done, BMAD-METHOD, OpenSpec, oh-my-claudecode, Compound Engineering, HumanLayer) and highlights newly released "hot" features (Ultraplan, Claude Code Web, Auto Mode, Agent Teams, No Flicker Mode, Computer Use, Voice Dictation). It includes an orchestration workflow demonstrating the Command-Agent-Skill architecture, a startups-displaced table, 9 companion reports, and 13 "billion-dollar questions" representing unsolved problems in AI-assisted development.

## Key Insights

### Feature Architecture

- **Full feature surface documented**: The CONCEPTS table covers every major Claude Code extension point: Subagents (`.claude/agents/`), Commands (`.claude/commands/`), Skills (`.claude/skills/<name>/SKILL.md`), Hooks (`.claude/hooks/`), MCP Servers (`.mcp.json`), Plugins (distributable bundles of skills + agents + hooks + MCP + LSP), Settings (`.claude/settings.json`), Memory (CLAUDE.md + `.claude/rules/`), Checkpointing (git-based rewind), and CLI Startup Flags.

- **Orchestration architecture**: The central pattern is Command (user-invoked prompt template injected into existing context) triggers Agent (autonomous actor in fresh isolated context with its own tools, permissions, model, memory, and persistent identity) which uses Skills (configurable, preloadable, auto-discoverable knowledge with progressive disclosure). This Command-Agent-Skill hierarchy is the organizing principle for extending Claude Code.

- **Hot new features (2026)**: Ultraplan (cloud-based plan drafting with browser review and inline comments), Claude Code Web (cloud infrastructure for long-running tasks, PR auto-fix, parallel sessions), Auto Mode (background safety classifier replacing manual permission prompts, toggled with `--enable-auto-mode` or `Shift+Tab`), Agent Teams (parallel agents on the same codebase with shared task coordination), No Flicker Mode (`CLAUDE_CODE_NO_FLICKER=1` for alt-screen rendering), Computer Use (macOS screen control via MCP server), Voice Dictation (`/voice` with 20-language support), Channels (push events from Telegram/Discord/webhooks into running sessions), and Scheduled Tasks (`/loop` local, `/schedule` cloud).

### Tips: 69 Across 13 Categories

**Prompting (3 tips):**
- Challenge Claude with verification gates: "grill me on these changes", "prove to me this works"
- After mediocre output: "knowing everything you know now, scrap this and implement the elegant solution"
- Paste the bug, say "fix" — do not micromanage how Claude solves it

**Planning/Specs (6 tips):**
- Always start with plan mode to prevent wrong-path waste
- Ask Claude to interview you using AskUserQuestion tool before building, then make a new session to execute
- Make phase-wise gated plans with unit, automation, and integration tests at each phase
- Spin up a second Claude (or Opus cross-model) to review your plan as a staff engineer
- Write detailed specs to reduce ambiguity before handing off — specificity directly correlates with output quality
- Prototype beats PRD: build 20-30 versions rather than writing specs; the cost of building is now low

**CLAUDE.md (7 tips + 1):**
- Keep CLAUDE.md under 200 lines per file; treat it as an index, not an exhaustive reference — HumanLayer's production CLAUDE.md is only 60 lines
- Wrap domain-specific rules in `<important if="...">` tags to prevent Claude from ignoring them as files grow longer
- Use multiple CLAUDE.md for monorepos — ancestor + descendant loading
- Use `.claude/rules/` to split large instructions into separate files
- CLAUDE.md and constitution.md do not guarantee compliance (still-open reliability issue)
- Any developer should be able to say "run the tests" on first try — if not, CLAUDE.md is missing setup commands
- Keep codebases clean and finish migrations — partially migrated frameworks cause models to pick wrong patterns
- Use `settings.json` for deterministic harness-enforced behavior (permissions, attribution, model) instead of CLAUDE.md text instructions

**Agents (4 tips):**
- Use feature-specific subagents with skills (progressive disclosure) rather than generic "backend engineer" agents
- Say "use subagents" to throw more compute at a problem, keeping main context clean
- Use Agent Teams with tmux and git worktrees for parallel development
- Use test-time compute: separate context windows improve results; one agent can introduce bugs, another (same model) can find them

**Commands (3 tips):**
- Prefer commands over subagents for workflows
- Create slash commands for every "inner loop" workflow done multiple times daily — commands live in `.claude/commands/` and are git-tracked
- If you do something more than once a day, turn it into a skill or command (build `/techdebt`, context-dump, analytics)

**Skills (9 tips):**
- Use `context: fork` to run a skill in an isolated subagent — main context only sees the final result, not intermediate tool calls
- Use skills in subfolders for monorepos
- Skills are folders, not files — use `references/`, `scripts/`, `examples/` subdirectories for progressive disclosure
- Build a Gotchas section in every skill — highest-signal content, grows over time with Claude's known failure points
- Skill description field is a trigger, not a summary — write it for the model ("when should I fire?")
- Do not state the obvious in skills — focus only on what pushes Claude out of its default behavior
- Do not railroad Claude in skills — give goals and constraints, not prescriptive step-by-step instructions
- Include scripts and libraries in skills so Claude composes rather than reconstructs boilerplate
- Embed `` !`command` `` in SKILL.md to inject dynamic shell output into the prompt at invocation time

**Hooks (5 tips):**
- Use on-demand hooks in skills — `/careful` blocks destructive commands, `/freeze` blocks edits outside a directory
- Measure skill usage with a PreToolUse hook to find popular or undertriggering skills
- Use a PostToolUse hook to auto-format code — Claude generates the code, the hook handles the last 10% for CI
- Route permission requests to Opus via a hook — let it scan for attacks and auto-approve safe ones
- Use a Stop hook to nudge Claude to keep going or verify its work at the end of a turn

**Workflows (7 tips):**
- Manual `/compact` at 50% context capacity — do not wait for auto-compact at 95% when context is already degraded
- Vanilla Claude Code beats any workflow framework for smaller tasks
- Use Opus for plan mode and Sonnet for coding to get the best of both models
- Enable thinking mode (to see reasoning) and Output Style Explanatory (to see ★ Insight boxes) in `/config`
- Use `ultrathink` keyword for high-effort reasoning
- Use `/rename` for important sessions and `/resume` them later — label multiple simultaneous instances
- Use `Esc Esc` or `/rewind` to undo when Claude goes off-track instead of trying to fix in same context

**Workflows Advanced (6 tips):**
- Use ASCII diagrams extensively to clarify architecture to Claude
- Use `/loop` for local recurring monitoring (up to 3 days); `/schedule` for cloud-based tasks that run when machine is off
- Use the Ralph Wiggum plugin for long-running autonomous tasks
- Use `/permissions` with wildcard syntax (`Bash(npm run *)`, `Edit(/docs/**)`) instead of dangerously-skip-permissions
- Use `/sandbox` for file and network isolation — Anthropic achieved 84% reduction in permission prompts internally
- Invest in product verification skills (signup-flow-driver, checkout-verifier) — worth spending a week to perfect

**Git / PR (5 tips):**
- Keep PRs small and focused — Boris's team maintains p50 of 118 lines per PR across 141 daily PRs
- Always squash merge PRs — clean linear history, one commit per feature, easy `git revert` and `git bisect`
- Commit at least once per hour, as soon as a task is completed
- Tag @claude on a coworker's PR to auto-generate lint rules for recurring review feedback — automate yourself out of code review
- Use `/code-review` for multi-agent PR analysis catching bugs, security vulnerabilities, and regressions

**Debugging (7 tips):**
- Share screenshots with Claude whenever stuck with any issue
- Use MCP (Claude in Chrome, Playwright, Chrome DevTools) to let Claude see Chrome console logs on its own
- Run terminals with logs as background tasks for better debugging visibility
- Use `/doctor` to diagnose installation, authentication, and configuration issues
- Fix compaction errors by switching to a 1M token model via `/model` then running `/compact`
- Use cross-model QA: Codex for plan and implementation review
- Agentic search (glob + grep) beats RAG — Claude Code tried and discarded vector databases because code drifts and permissions are complex

**Utilities (5 tips):**
- Use iTerm/Ghostty/tmux terminals instead of IDE-based Claude
- Use `/voice` or Wispr Flow for voice prompting (10x productivity)
- claude-code-hooks repo for Claude feedback mechanisms
- Status line plugin for context awareness and fast compacting
- Explore settings.json features like Plans Directory and Spinner Verbs

**Daily (2 tips):**
- Update Claude Code daily
- Start your day by reading the changelog

### Development Workflows

10 frameworks cataloged, all converging on Research-Plan-Execute-Review-Ship:

| Framework | Stars | Distinguishing Feature | Plan Layer |
|-----------|-------|------------------------|------------|
| Everything Claude Code | 142k | instinct scoring, AgentShield, multi-lang rules | Agent planner (47 agents, 82 commands, 182 skills) |
| Superpowers | 137k | TDD-first, Iron Laws, whole-plan review | Skill: writing-plans |
| Spec Kit | 86k | spec-driven, constitution, 22+ tools | Command: speckit.plan |
| gstack | 65k | role personas, /codex review, parallel sprints | Skill: autoplan (34 skills) |
| Get Shit Done | 48k | fresh 200K contexts, wave execution, XML plans | Agent: gsd-planner (24 agents, 68 commands) |
| BMAD-METHOD | 44k | full SDLC, agent personas, 22+ platforms | Skill: bmad-create-prd |
| OpenSpec | 38k | delta specs, brownfield, artifact DAG | Command: opsx:propose |
| oh-my-claudecode | 25k | teams orchestration, tmux workers, skill auto-inject | Skill: ralplan (19 agents, 36 skills) |
| Compound Engineering | 13k | Compound Learning, Multi-Platform CLI, Plugin Marketplace | Skill: ce-plan (50 agents, 4 commands, 42 skills) |
| HumanLayer | 10k | RPI, context engineering, 300k+ LOC | Command: create_plan |

Additional notable workflows: Cross-Model (Claude Code + Codex), RPI, Ralph Wiggum Loop, Andrej Karpathy's workflow, Peter Steinberger's workflow.

### Startups Displaced by Claude Code Features

Claude Code natively replaces: Greptile/CodeRabbit/Devin Review (Code Review), Wispr Flow/SuperWhisper (Voice Dictation), OpenClaw (Remote Control), Playwright MCP/Chrome DevTools MCP (Claude in Chrome), OpenAI CUA (Computer Use), ChatGPT Agent/Perplexity Computer/Manus (Cowork), Beads (Tasks), Agent OS (Plan Mode), YC AI wrapper startups (Skills/Plugins).

### Companion Reports (9)

Agent SDK vs CLI System Prompts, Browser Automation MCP, Global vs Project Settings, Skills in Monorepos, Agent Memory, Advanced Tool Use, Usage & Rate Limits, Agents vs Commands vs Skills, LLM Degradation.

### Billion-Dollar Questions (13)

**Memory & Instructions (4):**
1. What exactly should you put inside CLAUDE.md — and what should you leave out?
2. If you have a CLAUDE.md, is a separate constitution.md actually needed?
3. How often should you update CLAUDE.md, and how do you know when it's stale?
4. Why does Claude still ignore CLAUDE.md even when instructions say MUST in all caps?

**Agents, Skills & Workflows (6):**
1. When should you use a command vs agent vs skill — when is vanilla Claude Code just better?
2. How often should you update agents, commands, and workflows as models improve?
3. Does giving a subagent a detailed persona improve quality? What does the "perfect persona" for a research/QA agent look like?
4. Should you use Claude's built-in plan mode or build your own planning command/agent enforcing your team's workflow?
5. How do you incorporate community skills without conflicts with personal skills — and who wins when they disagree?
6. Can an existing codebase be converted to specs, code deleted, and AI regenerate the exact same code from those specs?

**Specs & Documentation (3):**
1. Should every feature have a spec as a markdown file?
2. How often do specs need updating to avoid becoming obsolete when a new feature is implemented?
3. When implementing a new feature, how do you handle the ripple effect on specs for other features?

## Open Questions

- How does the settings.json enforcement model interact with inherited CLAUDE.md rules when both configure the same behavior (e.g., model selection)? (Requires: external testing of precedence rules)
- What is the practical performance ceiling for Agent Teams with tmux+git worktrees on large monorepos? (Requires: empirical benchmarking at scale)

## Relationships

- DERIVED FROM: src-shanraisshan-claude-code-best-practice
- ENABLES: Claude Code Best Practices
- ENABLES: Claude Code Context Management
- BUILDS ON: Claude Code Skills
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Claude Code Hooks
- COMPARES TO: Everything Claude Code
- COMPARES TO: Superpowers Skills Framework

## Backlinks

[[src-shanraisshan-claude-code-best-practice]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[Claude Code Skills]]
[[LLM Wiki Pattern]]
[[Claude Code Hooks]]
[[Everything Claude Code]]
[[Superpowers Skills Framework]]
