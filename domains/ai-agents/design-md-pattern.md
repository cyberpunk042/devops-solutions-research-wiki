---
title: "Design.md Pattern"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-design-md-research
    type: article
    url: "https://github.com/VoltAgent/awesome-design-md"
    file: raw/articles/design-md-pattern-research.md
    title: "Design.md Pattern Research"
    ingested: 2026-04-08
  - id: src-google-stitch-design-md
    type: article
    url: "https://www.mindstudio.ai/blog/what-is-google-stitch-design-md-file"
    title: "What Is Google Stitch's Design.md File?"
    ingested: 2026-04-08
tags: [design-md, design-system, ai-agents, claude-md, google-stitch, markdown-config, ui-consistency, agent-context]
---

# Design.md Pattern

## Summary

Design.md is a plain-text design system document introduced by Google Stitch that AI coding agents read to generate consistent UI. It captures an entire visual design system — colors, typography, spacing, component patterns, responsive behavior — in a single markdown file placed at the project root. When an AI agent generates UI code, it reads Design.md as binding constraints rather than making arbitrary visual decisions. This extends the CLAUDE.md pattern (project instructions for agent behavior) into the visual design domain, and represents a broader convergence on "markdown files as AI configuration."

## Key Insights

- **9-section standard structure**: Visual Theme, Color Palette, Typography, Component Styles, Layout Principles, Depth & Elevation, Do's and Don'ts, Responsive Behavior, and Agent Prompt Guide. Each section is machine-readable but also human-reviewable.

- **Constraint-based generation**: Google Stitch passes the full Design.md as context alongside every prompt to Gemini. The model treats it as binding constraints — your specific hex values, font families, and spacing scales, not generic defaults.

- **58+ design systems already captured**: The VoltAgent/awesome-design-md repository contains Design.md files for Claude, Stripe, Vercel, Linear, Figma, Spotify, Tesla, and dozens more. Drop one into a project and AI agents build matching UI.

- **Companion files ecosystem**: DESIGN.md (how it should look) complements CLAUDE.md (how the agent should behave) and AGENTS.md (how to build). Together they give an AI agent complete project context without stuffing everything into a single file.

- **Tool-agnostic**: Consumed by Google Stitch, Claude Code, Cursor, Gemini CLI, and Antigravity. The markdown format is the interoperability layer — any tool that reads markdown can use it.

- **Preview artifacts**: Each Design.md comes with preview.html and preview-dark.html files that render the design system visually, allowing human verification before AI generates code.

## Deep Analysis

### The Broader Pattern: Markdown as AI Configuration

Design.md is not an isolated innovation — it's part of an emerging pattern where project-root markdown files serve as persistent AI context. The timeline:

1. **CLAUDE.md** — First mover. Project instructions, coding conventions, test commands. Read at session start by Claude Code.
2. **DESIGN.md** — Visual design system. Colors, typography, components. Read by design-aware agents (Stitch, Cursor).
3. **AGENTS.md** — Build instructions. How to construct the project, deployment patterns, architecture decisions.

Each file addresses a different dimension of AI agent context. The key insight is that these are NOT documentation for humans — they're configuration files for AI agents that happen to be human-readable. The markdown format serves both audiences.

### Implications for Knowledge Systems

For this wiki project, Design.md validates a hypothesis: structured markdown files are the optimal interface between human intent and AI execution. CLAUDE.md already proved this for coding conventions. Design.md proves it for visual design. The wiki itself is proving it for knowledge management.

The pattern suggests that any domain where an AI agent needs persistent, structured context will converge on a project-root markdown file. Future candidates: TESTING.md (test strategy), SECURITY.md (security constraints), DEPLOY.md (deployment rules).

### Integration with Skills Architecture

Design.md files are static context (loaded at session start). Skills are dynamic context (loaded when relevant). The optimal architecture uses both: Design.md provides the persistent visual constraints, while a "design review" skill provides the workflow for when and how to apply them. This mirrors the CLAUDE.md + Skills relationship already documented in the wiki.

## Open Questions

- Should this wiki adopt a DESIGN.md for its own Obsidian vault appearance (graph colors, note styling)?
- Will AGENTS.md become a standard alongside CLAUDE.md for Claude Code projects?
- How does Design.md interact with component libraries like Tailwind or Shadcn that already encode design decisions?
- What's the token cost of loading a full Design.md into context? Does it suffer the same context pollution as MCP schemas?
- Can Design.md be used with local models (e.g., via AICP routing) or is it too context-heavy for smaller models?

## Relationships

- EXTENDS: Claude Code Best Practices (CLAUDE.md is the same pattern for coding)
- RELATES TO: Skills Architecture Patterns (static vs dynamic AI context)
- RELATES TO: Harness Engineering (project-root config as agent guardrails)
- RELATES TO: Claude Code Context Management (context budget considerations)
- ENABLES: MCP Integration Architecture (Design.md + MCP Stitch server)
- RELATES TO: LLM Wiki Pattern (markdown as AI-native knowledge format)

## Backlinks

[[Claude Code Best Practices (CLAUDE.md is the same pattern for coding)]]
[[Skills Architecture Patterns (static vs dynamic AI context)]]
[[Harness Engineering (project-root config as agent guardrails)]]
[[Claude Code Context Management (context budget considerations)]]
[[MCP Integration Architecture (Design.md + MCP Stitch server)]]
[[LLM Wiki Pattern (markdown as AI-native knowledge format)]]
