---
title: "Synthesis: kepano/obsidian-skills"
type: source-synthesis
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
tags: [obsidian, skills, agent-skills, claude-code, codex-cli, markdown, json-canvas]
---

# Synthesis: kepano/obsidian-skills

## Summary

This repository, maintained by Kepano (the creator of Obsidian), provides the official set of Agent Skills for Obsidian. The skills follow the Agent Skills specification (agentskills.io), making them compatible with any skills-compatible agent including Claude Code, Codex CLI, and OpenCode. The collection includes five skills: obsidian-markdown (creating and editing Obsidian Flavored Markdown with wikilinks, embeds, callouts, and properties), obsidian-bases (creating and editing Obsidian Bases with views, filters, formulas, and summaries), json-canvas (creating and editing JSON Canvas files with nodes, edges, groups, and connections), obsidian-cli (interacting with vaults via the Obsidian CLI for plugin and theme development), and defuddle (extracting clean markdown from web pages using the Defuddle tool to remove clutter and save tokens).

## Key Insights

- **Official skills from the Obsidian creator**: This repository carries special authority as it comes from Kepano, the founder and primary developer of Obsidian. These represent the canonical way to teach AI agents about Obsidian-specific formats and capabilities.

- **Agent Skills specification compliance**: All skills follow the open agentskills.io specification, which means they are not locked to a single AI agent platform. They work with Claude Code, Codex CLI, OpenCode, and any future agent that implements the spec.

- **Five distinct skills covering Obsidian's formats**: The skills cover Obsidian Flavored Markdown (the core note format), Obsidian Bases (a newer structured data feature), JSON Canvas (the infinite canvas format), CLI interaction, and web page extraction. Together they represent comprehensive coverage of Obsidian's file formats and interaction modes.

- **Multiple installation methods**: Skills can be installed via the plugin marketplace, npx, or manual copy to the appropriate directory for each agent (`.claude/` for Claude Code, `~/.codex/skills` for Codex CLI, `~/.opencode/skills/` for OpenCode).

- **Defuddle skill for token-efficient web ingestion**: The defuddle skill extracts clean markdown from web pages, removing clutter. This is specifically designed to save tokens when feeding web content into LLMs, directly supporting the LLM Wiki Pattern's ingestion workflow.

- **Bases skill reflects Obsidian's evolution**: The inclusion of an obsidian-bases skill signals that Obsidian's newer structured data features (views, filters, formulas, summaries) are important enough to warrant dedicated AI agent support.

## Deep Analysis

As the official Obsidian skills from the tool's creator, this repository sets the standard for how AI agents should interact with Obsidian vaults. The five skills map to Obsidian's core capabilities: markdown editing, structured data (Bases), visual mapping (Canvas), programmatic interaction (CLI), and content ingestion (Defuddle).

The adherence to the agentskills.io specification is strategically significant. Rather than building a proprietary plugin system, Kepano adopted an open standard, which means these skills benefit from and contribute to the broader agent skills ecosystem. This approach increases distribution while reducing maintenance burden.

The defuddle skill is particularly interesting in the context of the LLM Wiki Pattern. It addresses the same problem the Web Clipper solves for human users (getting clean content from web pages into Obsidian) but optimized for AI agent consumption: stripped of visual clutter, formatted as clean markdown, and minimal in token count.

Compared to the other Obsidian skill repos (axton-obsidian-visual-skills and pablo-mano/Obsidian-CLI-skill), this repository is broader but shallower. It covers five areas at the specification level rather than going deep into any single capability. The other repos extend specific areas (visual diagram generation and comprehensive CLI coverage) with much more detailed implementation.

## Open Questions

- How frequently are these skills updated as Obsidian's features evolve? (Requires: external observation of the kepano/obsidian-skills repo update cadence over time; no wiki page covers this update frequency)
- Will additional skills be added as Obsidian introduces new features? (Requires: external Obsidian roadmap information; no wiki page covers upcoming Obsidian feature plans)

### Answered Open Questions

**Q: Do the skills handle edge cases in Obsidian Flavored Markdown that differ from standard markdown?**

Cross-referencing `Obsidian Skills Ecosystem` and `Skills Architecture Patterns`: the Obsidian Skills Ecosystem page documents that the kepano/obsidian-skills obsidian-markdown skill specifically covers "Obsidian Flavored Markdown with wikilinks, embeds, callouts, and properties" — features that are Obsidian-specific extensions not present in standard CommonMark. The Skills Architecture Patterns comparison notes kepano's skills are "specification-level" rather than "generation-level," meaning the obsidian-markdown skill teaches agents the format specification, including edge cases like wikilink resolution ambiguity, embed syntax, and frontmatter properties. However, the Obsidian Skills Ecosystem page also notes that kepano's skills are "thinner" than community skills — pablo-mano's comprehensive skill covers "130+ commands" including property operations that depend on Obsidian-specific frontmatter parsing. The conclusion: kepano's skill handles the documented Obsidian Markdown edge cases (those specified in the agentskills.io format), while undocumented or plugin-specific edge cases (e.g., Dataview query syntax, Templater variables embedded in markdown) are outside the skill's scope and require community extensions.

**Q: Is there a testing or validation framework for skills following the agentskills.io spec?**

Cross-referencing `Skills Architecture Patterns` and `Harness Engineering`: the Skills Architecture Patterns page identifies this as a tension — "official vs. community quality: kepano's official Obsidian skills follow the agentskills.io spec but are thinner than community skills... quality variance in community skills creates reliability uncertainty." The page also notes that the agentskills.io specification itself is "still emerging." No wiki page documents a testing or validation framework for agentskills.io-compliant skills. The closest analogy in existing wiki knowledge is the harness engineering approach from the Harness Engineering page: runtime guardrails (hooks, TypeScript rules R01-R13) that enforce behavior at execution time — applying this to skill testing would mean writing test cases that invoke each skill with known inputs and validate outputs. The Skills Architecture Patterns page notes that "composition (skills referencing skills) remains largely unsolved across all ecosystems" — a validation framework faces the same unsolved problem: skills are compressed instructions that LLMs expand at runtime, making deterministic testing difficult. The current state per wiki knowledge: no standardized testing framework exists; informal testing via manual invocation and output review is the norm.

## Relationships

- DERIVED FROM: src-kepano-obsidian-skills
- FEEDS INTO: Obsidian Skills Ecosystem
- EXTENDS: Claude Code Skills
- RELATES TO: Obsidian Knowledge Vault
- IMPLEMENTS: LLM Wiki Pattern

## Backlinks

[[src-kepano-obsidian-skills]]
[[Obsidian Skills Ecosystem]]
[[Claude Code Skills]]
[[Obsidian Knowledge Vault]]
[[LLM Wiki Pattern]]
[[Skill Specification Is the Key to Ecosystem Interoperability]]
