---
title: "Obsidian Skills Ecosystem"
type: concept
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-kepano-obsidian-skills
    type: documentation
    url: "https://github.com/kepano/obsidian-skills"
    file: raw/articles/kepanoobsidian-skills.md
    title: "kepano/obsidian-skills"
    ingested: 2026-04-08
  - id: src-axton-obsidian-visual-skills
    type: documentation
    url: "https://github.com/axtonliu/axton-obsidian-visual-skills"
    file: raw/articles/axtonliuaxton-obsidian-visual-skills.md
    title: "axtonliu/axton-obsidian-visual-skills"
    ingested: 2026-04-08
  - id: src-pablo-mano-obsidian-cli-skill
    type: documentation
    url: "https://github.com/pablo-mano/Obsidian-CLI-skill"
    file: raw/articles/pablo-manoobsidian-cli-skill.md
    title: "pablo-mano/Obsidian-CLI-skill"
    ingested: 2026-04-08
tags: [obsidian, skills, agent-skills, claude-code, visual-diagrams, cli, ecosystem]
---

# Obsidian Skills Ecosystem

## Summary

A growing ecosystem of AI agent skills has emerged around Obsidian, enabling AI coding agents like Claude Code to create, read, edit, and visualize content within Obsidian vaults. Three repositories represent different layers of this ecosystem: kepano/obsidian-skills provides the official, broad-coverage skill set from Obsidian's creator covering five core capabilities (Obsidian Flavored Markdown, Bases, JSON Canvas, CLI, and Defuddle web extraction); axtonliu/axton-obsidian-visual-skills focuses specifically on visual diagram generation (Excalidraw, Mermaid, Canvas) from natural language; and pablo-mano/Obsidian-CLI-skill delivers the deepest CLI integration with 130+ commands covering all vault operations across 8+ agent platforms. Together, these three repositories create a layered capability stack where official specs meet community extensions that go deeper into specific domains.

## Key Insights

- **Three layers of capability**: The ecosystem naturally stratifies into official specification skills (kepano), visual generation skills (axton), and deep operational skills (pablo-mano). Each layer builds on the one below: kepano defines the formats, axton generates visual content in those formats, and pablo-mano provides programmatic control over the vault that holds them.

- **Official vs. community skills**: kepano/obsidian-skills carries the authority of Obsidian's creator and follows the agentskills.io specification. The community skills (axton, pablo-mano) extend specific capabilities far beyond what the official set covers, demonstrating that the skill system benefits from both official standards and community depth.

- **Overlapping CLI coverage**: Both kepano and pablo-mano include Obsidian CLI skills, but at very different levels of detail. kepano's obsidian-cli is one of five skills with a brief description. pablo-mano's covers 130+ commands with platform-specific troubleshooting, multiple invocation modes, and installation guides for 8 agent platforms. They complement rather than conflict: kepano provides the canonical format definition, pablo-mano provides exhaustive operational reference.

- **Overlapping Canvas coverage**: Similarly, both kepano (json-canvas skill) and axton (obsidian-canvas-creator skill) address Canvas files. kepano's skill teaches agents the JSON Canvas specification. axton's skill generates Canvas files from natural language with MindMap and Freeform layout algorithms, color coding, and spacing logic. Again, specification vs. generation.

- **Cross-agent compatibility varies**: kepano's skills follow agentskills.io and work with Claude Code, Codex CLI, and OpenCode. pablo-mano's skill supports 8+ agents (Claude Code, Cursor, Cortex Code, Copilot, Windsurf, Nanoclaw, Openclaw, and any system prompt). axton's skills target Claude Code primarily via the plugin marketplace and manual installation.

- **SKILL.md as the universal format**: All three repositories use SKILL.md as the skill definition format. Pablo-mano's README explicitly demonstrates that SKILL.md content can be pasted into any agent's system prompt or custom instructions field, making it a de facto universal format for agent knowledge.

- **Visual skills fill a generation gap**: kepano teaches agents what Obsidian formats look like. axton teaches agents how to generate visual content (Excalidraw with 8 diagram types, Mermaid with 6 diagram types, Canvas with 2 layout modes). This generation capability is absent from the official skills.

- **Defuddle bridges web and vault**: kepano's defuddle skill extracts clean markdown from web pages, reducing token waste. This directly supports ingestion workflows in the LLM Wiki Pattern by providing AI-optimized web content extraction.

## Deep Analysis

The Obsidian skills ecosystem reflects a common pattern in developer tool extensibility: an official, authoritative base layer provides format definitions and basic capabilities, while community contributors build deeper, more specialized extensions on top.

### Capability Matrix

| Capability | kepano | axton | pablo-mano |
|---|---|---|---|
| Markdown editing | obsidian-markdown | - | - |
| Bases (structured data) | obsidian-bases | - | base:query, base:views, base:create |
| JSON Canvas (spec) | json-canvas | - | - |
| Canvas generation | - | obsidian-canvas-creator | - |
| Excalidraw generation | - | excalidraw-diagram | - |
| Mermaid generation | - | mermaid-visualizer | - |
| CLI (basic) | obsidian-cli | - | - |
| CLI (comprehensive) | - | - | 130+ commands |
| Web extraction | defuddle | - | - |
| Agent compatibility | 3 agents | Claude Code | 8+ agents |

### Complementary Installation

A user wanting comprehensive Obsidian AI agent support would install all three:
1. kepano/obsidian-skills for canonical format understanding and web extraction
2. axton/obsidian-visual-skills for diagram and canvas generation
3. pablo-mano/Obsidian-CLI-skill for full programmatic vault control

The overlap in CLI and Canvas coverage is not problematic because the overlapping skills serve different purposes (specification vs. generation, basic vs. comprehensive). An AI agent with all three installed would have both the format knowledge and the generation/operational capabilities.

### Ecosystem Maturity

The ecosystem is still young. axton explicitly labels the visual skills as experimental with variable output quality. pablo-mano's skill depends on Obsidian v1.12's CLI which was only recently released. kepano's official skills follow an open specification (agentskills.io) that is itself still emerging. This means the ecosystem will likely consolidate and improve significantly as these foundations mature.

The dependence on Obsidian's desktop app for CLI operations (pablo-mano) is a meaningful constraint. It means AI agents cannot manage Obsidian vaults in headless server environments without workarounds (xvfb on Linux). This limits use in CI/CD pipelines and cloud-based agent deployments.

## Open Questions

- Will the agentskills.io specification become the dominant standard for AI agent skills, or will platform-specific formats win?
- How will skill conflicts be managed when multiple skills overlap (e.g., two Canvas skills, two CLI skills)?
- Will Obsidian introduce a plugin API that makes CLI-over-IPC unnecessary for agent interaction?
- Can visual generation skills (axton) achieve deterministic, production-quality output, or will output variability remain a fundamental limitation?
- What is the path from experimental community skills to officially endorsed Obsidian extensions?
- Cross-source insight: The three-layer ecosystem pattern here (official spec, visual generation, deep CLI) parallels the Command-Agent-Skill hierarchy in Claude Code Best Practices. In both cases, different abstraction levels serve different purposes and compose rather than compete. This suggests a general principle: agent extensibility systems naturally stratify into specification, generation, and control layers.

## Relationships

- DERIVED FROM: src-kepano-obsidian-skills
- DERIVED FROM: src-axton-obsidian-visual-skills
- DERIVED FROM: src-pablo-mano-obsidian-cli-skill
- EXTENDS: Claude Code Skills
- BUILDS ON: Obsidian Knowledge Vault
- RELATES TO: NotebookLM Skills
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Skills Architecture Patterns

## Backlinks

[[src-kepano-obsidian-skills]]
[[src-axton-obsidian-visual-skills]]
[[src-pablo-mano-obsidian-cli-skill]]
[[Claude Code Skills]]
[[Obsidian Knowledge Vault]]
[[NotebookLM Skills]]
[[LLM Wiki Pattern]]
[[Skills Architecture Patterns]]
[[Obsidian CLI]]
[[Obsidian as Knowledge Infrastructure Not Just Note-Taking]]
[[OpenClaw]]
[[Synthesis: axtonliu/axton-obsidian-visual-skills]]
[[Synthesis: kepano/obsidian-skills]]
[[Synthesis: pablo-mano/Obsidian-CLI-skill]]
