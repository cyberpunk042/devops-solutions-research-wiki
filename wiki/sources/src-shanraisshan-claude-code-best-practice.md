---
title: "Synthesis: Claude Code Best Practice (shanraisshan)"
type: source-synthesis
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
tags: [claude-code, best-practices, subagents, commands, skills, hooks, orchestration, workflows, CLAUDE-md, tips, boris-cherny, context-engineering]
---

# Synthesis: Claude Code Best Practice (shanraisshan)

## Summary

This is a comprehensive, community-maintained GitHub repository (142k+ stars, trending #1 on GitHub) that catalogs Claude Code best practices, tips, architectural patterns, and development workflows. It covers the full Claude Code feature surface: subagents, commands, skills, hooks, MCP servers, plugins, settings, memory (CLAUDE.md), checkpointing, and CLI flags. It aggregates 69 tips from Boris Cherny (Claude Code's creator), Thariq, Cat Wu, and community contributors, organized by category (prompting, planning, CLAUDE.md, agents, commands, skills, hooks, workflows, git/PR, debugging, utilities, daily habits). It also catalogs 10 major open-source development workflow frameworks (Everything Claude Code, Superpowers, Spec Kit, gstack, Get Shit Done, BMAD-METHOD, OpenSpec, oh-my-claudecode, Compound Engineering, HumanLayer) that all converge on a Research-Plan-Execute-Review-Ship pattern. The repo includes an orchestration workflow demonstrating the Command-Agent-Skill architecture, and a set of "billion-dollar questions" representing unsolved problems in AI-assisted development.

## Key Insights

- **Orchestration architecture**: The central architectural pattern is Command (user-invoked prompt template injected into context) triggers Agent (autonomous actor in isolated context with its own tools and permissions) which uses Skills (configurable, preloadable knowledge with progressive disclosure). This Command-Agent-Skill hierarchy is the organizing principle for extending Claude Code.

- **CLAUDE.md under 200 lines**: Boris Cherny recommends keeping CLAUDE.md files lean -- under 200 lines per file. Treat it as an index pointing to where more data lives rather than an exhaustive reference. Every message re-reads CLAUDE.md, so bloat compounds. HumanLayer's practical CLAUDE.md is only 60 lines. Use `.claude/rules/` to split large instructions into separate files.

- **Plan mode before execution**: Consistently the top recommendation across sources. Start every significant task with plan mode to prevent the biggest source of waste: Claude going down the wrong path and having to scrap work. Boris recommends using Opus for planning and Sonnet for coding. Multiple tips reinforce asking Claude to interview you before building.

- **Skills as folders, not files**: Skills should use subdirectories (references/, scripts/, examples/) for progressive disclosure. The skill description field is a trigger for the model ("when should I fire?"), not a human summary. Include a Gotchas section for known failure points that grows over time.

- **Context: fork for isolation**: Skills can use `context: fork` to run in an isolated subagent where the main context only sees the final result, not intermediate tool calls. This prevents skill execution from polluting the main conversation context.

- **Hooks for automation**: Use PreToolUse hooks to measure skill usage, PostToolUse hooks for auto-formatting, Stop hooks to nudge Claude to verify its work. Permission requests can be routed to Opus via a hook for automated safety review.

- **Manual /compact at 50%**: Do not wait for auto-compact at 95% when context is already degraded. Manually compact at 50% capacity. Use /clear when switching to unrelated tasks. This single habit dramatically extends session life.

- **Small PRs, squash merge**: Boris's team maintains a p50 of 118 lines per PR across 141 daily PRs. Always squash merge for clean linear history. Commit at least once per hour.

- **Agentic search over RAG**: Claude Code tried and discarded vector databases internally because code drifts out of sync. Glob + grep (agentic search) beats RAG for code navigation. This aligns with Karpathy's wiki pattern insight about structured files versus embeddings.

- **Development workflow convergence**: All 10 cataloged workflow frameworks independently converge on Research-Plan-Execute-Review-Ship, differing mainly in whether the planning layer uses agents, commands, or skills. This suggests the pattern is fundamental rather than accidental.

- **Billion-dollar questions remain open**: Key unsolved problems include why Claude ignores CLAUDE.md instructions even with MUST in all caps, when to use command vs. agent vs. skill, whether codebases can be regenerated from specs alone, and how to handle spec ripple effects across features.

## Relationships

- DERIVED FROM: src-shanraisshan-claude-code-best-practice
- ENABLES: Claude Code Best Practices
- ENABLES: Claude Code Context Management
- BUILDS ON: Claude Code Skills
- RELATES TO: LLM Wiki Pattern

## Backlinks

[[src-shanraisshan-claude-code-best-practice]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[Claude Code Skills]]
[[LLM Wiki Pattern]]
