---
title: "Skill Specification Is the Key to Ecosystem Interoperability"
type: lesson
domain: cross-domain
layer: 4
status: synthesized
confidence: high
maturity: growing
created: 2026-04-08
updated: 2026-04-10
derived_from:
  - "Synthesis: kepano/obsidian-skills"
  - "Obsidian Skills Ecosystem"
sources:
  - id: src-kepano-obsidian-skills
    type: documentation
    url: "https://github.com/kepano/obsidian-skills"
    title: "kepano/obsidian-skills"
  - id: src-axton-obsidian-visual-skills
    type: documentation
    url: "https://github.com/axtonliu/axton-obsidian-visual-skills"
    title: "axtonliu/axton-obsidian-visual-skills"
  - id: src-pablo-mano-obsidian-cli-skill
    type: documentation
    url: "https://github.com/pablo-mano/Obsidian-CLI-skill"
    title: "pablo-mano/Obsidian-CLI-skill"
tags: [skills, interoperability, specification, obsidian, agent-skills, portability, standards]
---

# Skill Specification Is the Key to Ecosystem Interoperability

## Summary

When a skill definition format is rooted in an open specification rather than a proprietary platform, skills become portable artifacts that any conforming agent can load. Kepano's adoption of the agentskills.io SKILL.md format for the official Obsidian skills set a de facto standard that the entire Obsidian skill ecosystem now follows — enabling pablo-mano's community CLI skill to work across 8+ agent platforms by simply pasting SKILL.md content into any system prompt.

## Context

This lesson applies whenever a tool ecosystem is deciding how to structure its AI agent skill layer. The triggering situation is the emergence of competing skill implementations for the same tool (in this case, Obsidian) — each with different scope and depth. Without a shared format, skills would be platform-locked and the community's depth would be wasted on incompatible implementations. The Obsidian case occurred in 2025-2026 as Claude Code, Codex CLI, OpenCode, and other agents became capable of vault interactions.

## Insight

> [!success] Open Spec Creates a Gravity Well
> Kepano's adoption of the agentskills.io SKILL.md format for official Obsidian skills set a de facto standard. Community contributors who want maximum distribution follow the spec; tools that implement the spec gain access to the entire growing library of skills. One format works across 8+ agent platforms.

The SKILL.md format became a universal packaging contract for compressed agent knowledge. Because Kepano — the creator of Obsidian and therefore the authoritative source — chose the agentskills.io open specification rather than building Obsidian-specific plugin infrastructure, every subsequent community contributor inherited cross-agent portability for free. This is the lesson: an official specification adoption creates a gravity well. Community contributors who want maximum distribution follow the spec; tools that implement the spec gain access to the entire growing library of skills.

The corollary is equally important: skill portability enables depth stratification without fragmentation. The three-layer ecosystem that emerged (kepano's specification-level skills, axton's generation-level visual skills, pablo-mano's operation-level CLI skill) works precisely because all three layers share the same SKILL.md container. If each layer had invented its own format, users would need to configure three different systems. Instead, the shared format means a user can compose all three by installing SKILL.md files into a single `.claude/` or `~/.codex/skills` directory — no integration overhead.

## Evidence

The Obsidian Skills Ecosystem page documents the convergence explicitly: "All three repositories use SKILL.md as the skill definition format." Pablo-mano's README demonstrates the format's portability by showing that SKILL.md content "can be pasted into any agent's system prompt or custom instructions field, making it a de facto universal format for agent knowledge." The coverage spans 8 named agent platforms: Claude Code, Cursor, Cortex Code, Copilot, Windsurf, Nanoclaw, Openclaw, and any system-prompt-configurable agent.

The specification-level vs. generation-level vs. operation-level stratification is visible in the capability matrix documented in the Obsidian Skills Ecosystem: kepano's `json-canvas` skill teaches the Canvas file format; axton's `obsidian-canvas-creator` generates Canvas files from natural language. Both coexist because the SKILL.md format has no constraint on what level of abstraction a skill operates at — it is a container, not a prescriptive API.

The overlap resolution mechanism also confirms the lesson: both kepano and pablo-mano have CLI skills, but they serve different purposes (specification vs. 130+ command operational depth). The Obsidian Skills Ecosystem answered question on skill conflicts states: "The conflict management mechanism is trigger description differentiation — if two skills have distinct enough description fields, the model routes to the correct one for each task." This works because the SKILL.md format includes a description field that the model can use for routing — a feature of the shared format, not something each tool had to invent.

## Applicability

This lesson applies directly to:

- **Any tool building an AI agent integration layer**: Adopt an open skill specification rather than building proprietary plugin APIs. The one-time cost of spec compliance returns compounding distribution gains as the skill ecosystem grows.
- **Devops ecosystem skill design** (openfleet, AICP, DSPD): If AICP or OpenFleet publish SKILL.md files describing their agent APIs, they inherit compatibility with every Claude Code, Codex CLI, and OpenCode user without building separate integrations.
- **This wiki's skill system**: The `skills/` directory already uses SKILL.md format. This lesson confirms that format choice was correct and that wiki skills should be published as agentskills.io-conformant files for maximum portability.
- **Team knowledge distribution**: Any team encoding operational knowledge in SKILL.md format can deploy that knowledge to any conforming agent platform without rewriting.

## Relationships

- DERIVED FROM: [[Synthesis: kepano/obsidian-skills]]
- DERIVED FROM: [[Obsidian Skills Ecosystem]]
- BUILDS ON: [[Skills Architecture Patterns]]
- RELATES TO: [[Claude Code Skills]]
- RELATES TO: [[NotebookLM Skills]]
- ENABLES: [[Obsidian Skills Ecosystem]]
- FEEDS INTO: [[LLM Wiki Pattern]]

## Backlinks

[[Synthesis: kepano/obsidian-skills]]
[[Obsidian Skills Ecosystem]]
[[Skills Architecture Patterns]]
[[Claude Code Skills]]
[[NotebookLM Skills]]
[[LLM Wiki Pattern]]
[[Model: Skills, Commands, and Hooks]]
