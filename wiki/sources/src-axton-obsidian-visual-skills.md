---
title: "Synthesis: axtonliu/axton-obsidian-visual-skills"
type: source-synthesis
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-axton-obsidian-visual-skills
    type: documentation
    url: "https://github.com/axtonliu/axton-obsidian-visual-skills"
    file: raw/articles/axtonliuaxton-obsidian-visual-skills.md
    title: "axtonliu/axton-obsidian-visual-skills"
    ingested: 2026-04-08
tags: [obsidian, excalidraw, mermaid, canvas, visual-diagrams, claude-code, skills]
---

# Synthesis: axtonliu/axton-obsidian-visual-skills

## Summary

This repository provides a Visual Skills Pack for Obsidian that enables Claude Code to generate Excalidraw diagrams, Mermaid charts, and Obsidian Canvas files from natural language text input. It contains three distinct skills: an Excalidraw Diagram Generator with three output modes (Obsidian, Standard, Animated) supporting 8 diagram types; a Mermaid Visualizer for 6 diagram types with built-in syntax error prevention; and an Obsidian Canvas Creator with MindMap and Freeform layout modes. The pack is experimental in status and focuses on visual knowledge representation, including full Chinese text support. Skills are prompt-based markdown files that Claude Code loads on demand rather than compiled code or MCP servers.

## Key Insights

- **Three complementary visual formats**: Excalidraw (hand-drawn aesthetic), Mermaid (code-rendered flowcharts and diagrams), and JSON Canvas (Obsidian's native infinite canvas) cover the major visual representation modes available in Obsidian.

- **Excalidraw versatility**: The Excalidraw skill alone supports 8 diagram types (flowchart, mind map, hierarchy, relationship, comparison, timeline, matrix, freeform) across 3 output modes (Obsidian .md, standard .excalidraw, animated .excalidraw). This is the most feature-rich individual skill in the pack.

- **Built-in syntax error prevention for Mermaid**: The Mermaid skill includes rules to prevent common syntax errors (list conflicts, subgraph naming, special characters). This is a practical addition since Mermaid syntax has many subtle pitfalls that cause rendering failures.

- **Trigger word activation**: Skills are activated by natural language trigger words (e.g., "Excalidraw", "diagram", "flowchart", "mind map") rather than explicit command syntax. Chinese trigger words are also supported.

- **Canvas layout algorithms**: The Canvas Creator includes smart node sizing based on content length, automatic edge creation with labeled relationships, color-coded nodes (6 presets plus custom hex), and spacing algorithms to prevent overlap.

- **Experimental status acknowledged**: The README explicitly states the project is a public prototype focused on demonstrating how tools and systems work together, not on production reliability. Output quality varies by model version and input structure.

- **Bilingual support**: Full Chinese text support throughout, including CJK font handling for Excalidraw and Chinese trigger words for all skills.

## Deep Analysis

This skill pack fills a specific gap in the Obsidian-AI agent ecosystem: visual output. While kepano/obsidian-skills teaches agents about Obsidian's file formats (including JSON Canvas), this pack goes further by implementing generation logic for visual diagrams.

The Excalidraw skill is notable because it bridges two worlds: the hand-drawn aesthetic of whiteboard-style diagrams and the programmatic generation capabilities of AI agents. By supporting Obsidian-native output (.md with Excalidraw frontmatter), standard Excalidraw files, and animated variants, it covers use cases from personal note-taking to presentation creation.

The Mermaid syntax error prevention is a pragmatic feature. Mermaid diagrams frequently fail to render due to subtle syntax issues that LLMs commonly produce (improper quoting, conflicting subgraph names, unsupported characters). By encoding these prevention rules in the skill, the pack reduces the trial-and-error cycle of getting diagrams to render correctly.

The experimental status is honest and instructive. It highlights a current limitation of skills-based AI capabilities: output quality is not deterministic. Different model versions, input structures, and context lengths produce varying results. This is a general challenge for any skill that produces structured output (code, diagrams, configurations).

## Open Questions

- How does output quality compare across different Claude model versions?
- Can the Excalidraw animation feature be used to create step-by-step explanatory animations?
- What is the practical node limit for Canvas layouts before the spacing algorithms break down?
- Would a validation step (rendering and checking the output) improve reliability?

## Relationships

- DERIVED FROM: src-axton-obsidian-visual-skills
- FEEDS INTO: Obsidian Skills Ecosystem
- EXTENDS: Claude Code Skills
- RELATES TO: Obsidian Knowledge Vault
- COMPARES TO: src-kepano-obsidian-skills

## Backlinks

[[src-axton-obsidian-visual-skills]]
[[Obsidian Skills Ecosystem]]
[[Claude Code Skills]]
[[Obsidian Knowledge Vault]]
[[src-kepano-obsidian-skills]]
