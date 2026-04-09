---
title: "Claude Code Skills"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-claude-notebooklm-content-team
    type: youtube-transcript
    file: raw/transcripts/claude-notebooklm-content-team.txt
    title: "Claude + NotebookLM = Your 24/7 Content Team"
    ingested: 2026-04-08
  - id: src-obsidian-claude-code-second-brain
    type: youtube-transcript
    url: "https://www.youtube.com/watch?v=Y2rpFa43jTo"
    file: raw/transcripts/obsidian-claude-code-the-second-brain-setup-that-actually-works.txt
    title: "Obsidian + Claude Code: The Second Brain Setup That Actually Works"
    ingested: 2026-04-08
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
tags: [claude-code, skills, markdown, agent-configuration, extensibility, obsidian-cli, multi-step-workflows, gmail-integration, progressive-disclosure, context-forking, hooks]
---

# Claude Code Skills

## Summary

Skills in Claude Code are markdown files that serve as instruction sets for the AI agent, teaching it how to perform specific tasks, interact with external tools, and follow design guidelines. A skill file contains prerequisites (such as packages to install), setup procedures (such as authentication flows), operational instructions for using a tool, and domain-specific guidance (such as slide design specifications). When a skill is sent to Claude Code, it reads the instructions and can autonomously perform the setup steps and then use the capability on demand. Skills are the primary mechanism for extending Claude Code's capabilities beyond its built-in functionality.

## Key Insights

- **Skills are plain markdown**: A skill is simply a text file in markdown format — no special format, no compiled code. This makes skills easy to create, share, read, and modify. The presenter explicitly states: "a skill is just a markdown file... a text file that gives your agent instructions."

- **Two-phase operation — setup then use**: When Claude Code receives the NotebookLM skill, it performs two automatic steps: (1) install the required package (notebooklm-py), and (2) prompt the user to authenticate with Google. After this one-time setup, the skill is available for repeated use.

- **Design guidance embedded in skills**: The NotebookLM skill includes a "slide generation component" section with specific design instructions — color schemes, font choices, title formatting, and layout parameters. This means skills can encode not just functional behavior but also aesthetic and brand standards.

- **Skills are iteratively refinable**: Users can ask Claude to modify a skill through natural language. The presenter demonstrates asking Claude to change the slide style from "orange blackboard" to "blue corporate navy" and then to save both as named style options within the skill. Claude reads the skill, edits the relevant sections, and writes the updated file.

- **Skills enable repeatable, consistent outputs**: Because the design system and operational instructions are codified in the skill file, outputs are consistent across runs. The presenter emphasizes that the slides maintain a consistent style "every time" because of the skill.

- **Skills can have multiple presets**: The presenter demonstrates adding a second slide style ("corporate navy blue") alongside the default ("blackboard"), creating a multi-option skill where the user can direct Claude to use a specific style at runtime.

- **Skills are folders with progressive disclosure (from best practices repo)**: According to Anthropic's Thariq, skills should be folders with subdirectories (references/, scripts/, examples/) rather than single files. The SKILL.md description field is a trigger written for the model ("when should I fire?"), not a human summary. Skills should include a Gotchas section for known failure points and should contain scripts/libraries so Claude composes rather than reconstructs boilerplate.

- **Context forking for isolation (from best practices repo)**: Skills can use `context: fork` to run in an isolated subagent where the main context only sees the final result, not intermediate tool calls. This prevents skill execution from polluting the main conversation's context window -- an important consideration for token management.

- **On-demand hooks in skills (from best practices repo)**: Skills can include on-demand hooks like /careful (blocks destructive commands) and /freeze (blocks edits outside a directory), providing contextual safety guardrails that activate only when the skill is in use.

- **Skills as shareable packages**: The presenter mentions making the skill pack available through their community, indicating that skills are designed to be distributable and usable by others with minimal configuration.

- **Clarifying question pattern**: When modifying skills, the presenter recommends asking Claude to ask clarifying questions first ("Ask me clarifying questions so that the intention is clear"), establishing a Q&A alignment step before the skill is edited. This is described as "one of the most powerful things you can do."

- **Obsidian CLI skills (from second brain video)**: The Eric Tech video demonstrates installing Obsidian CLI skills that teach Claude Code to interact with Obsidian programmatically -- creating notes, managing folders, and using markdown and JSON Canvas through the command line. These skills are installable via marketplace or npx.

- **Complex multi-step workflow skills**: The "onboard projects" skill demonstrated in the second brain video goes well beyond simple tool wrappers. It includes: multi-source data collection (Gmail API via OAuth2, local filesystem, user-pasted text/screenshots), conditional processing logic (summarize conversations vs. preserve static documents like NDAs as-is), structured output generation (per-project folders with overview, conversation log, links, documents), and dashboard maintenance (updating a central projects database).

- **Skills can include custom scripts**: The onboard projects skill bundles custom scripts for Gmail integration (fetching labels, messages, threads, downloading attachments) alongside the skill's markdown instructions. This shows skills can coordinate between multiple code artifacts, not just a single instruction file.

- **Skills compose with each other**: The second brain video demonstrates skills that reference and build on other Obsidian CLI skills (markdown, database, Canvas), suggesting a composition pattern where higher-level workflow skills orchestrate lower-level capability skills.

## Deep Analysis

The skill system represents a practical approach to agent extensibility that prioritizes simplicity and accessibility over formal plugin architectures. By using plain markdown rather than structured APIs or plugin manifests, skills lower the barrier to extending Claude Code's capabilities. Any user who can write a text file can create a skill.

The NotebookLM skill demonstrated in the transcript bundles several concerns into a single file: dependency management (installing notebooklm-py), authentication (Google account login flow), operational instructions (how to create notebooks, load sources, generate assets), and design guidance (slide styling). This multi-concern bundling means a single skill can take Claude from zero capability to full operational readiness with an external tool.

The iterative refinement workflow is notable: rather than requiring users to manually edit markdown files, they can ask Claude to modify the skill through conversation. This creates a meta-capability where the agent can improve its own instruction set based on user feedback. The progression shown — default style, then user requests a new style, then user asks to save both as options — demonstrates how skills evolve through use.

The fact that Claude "reconstructed" a detailed prompt under the hood (specifying a seven-slide deck with design parameters and font guidance) based on the skill instructions shows that skills act as compressed knowledge that Claude expands into detailed operational prompts at execution time. The user never sees or writes these detailed prompts directly.

The connection to long-running agent sessions is important: skills persist across interactions, meaning a configured agent retains its capabilities over time. This is what enables the scheduling use case — a skill installed once continues to function in future automated runs.

### Skills as Workflow Automations (from second brain video)

The "onboard projects" skill from the Obsidian + Claude Code video represents a significant complexity jump from the NotebookLM skill. Where the NotebookLM skill is essentially a tool wrapper (install package, authenticate, use API), the onboard projects skill is a multi-step workflow automation that coordinates across data sources, applies conditional logic, and maintains structured output. It includes five distinct phases: project creation, source collection (Gmail + local + pasted), processing with duplicate/format detection, auto-extraction of metadata, and summary generation.

This suggests that Claude Code skills exist on a complexity spectrum: simple skills wrap a single tool, medium skills combine a tool with formatting/design guidance, and complex skills orchestrate multi-source data pipelines with conditional logic. The upper bound of skill complexity -- the point where a skill becomes too large or nuanced for the LLM to follow reliably -- remains an open question but appears to be further out than initially assumed.

## Open Questions

- Is there a versioning or update mechanism for skills, or must they be manually replaced? (Requires: external research on skill versioning conventions; the `Skills Architecture Patterns` page asks the same question: "How should skill versioning work — semantic versioning for breaking changes in instruction format?" and notes it requires "empirical data from large-scale skill deployment")
- Can skills reference or compose other skills, or is each skill self-contained? (Partially answered: skills are folders that can include scripts and references, and skills can use context: fork for isolation, but formal skill-to-skill composition is not yet documented. The `Skills Architecture Patterns` page identifies this as unresolved: "Composition (skills referencing skills) remains largely unsolved across all ecosystems.")

## Answered Open Questions

### What is the maximum practical complexity of a skill before it becomes unreliable?

Cross-referencing `CLI Tools Beat MCP for Token Efficiency` and `Context-Aware Tool Loading`: the complexity ceiling is not a fixed line count but a function of session context pressure. The `CLI Tools Beat MCP for Token Efficiency` lesson documents that Claude Code accuracy drops significantly at 40% context usage and becomes unreliable at 60%+. Any skill large enough to consume a substantial fraction of the context window will trigger this degradation before the task begins. The `Context-Aware Tool Loading` pattern provides the resolution: use `context: fork` for any skill whose instructions are extensive — this isolates skill execution in a sub-agent context so the parent session context is not polluted. The `Skills Architecture Patterns` page's answered question on this topic confirms: "for production-grade skills like claude-world's 13-tool pipeline, the recommended architecture is `context: fork` (sub-agent isolation) to prevent the skill from polluting the parent session context." The practical upper bound for an unfork'd skill is roughly ~100 lines before degradation risk becomes significant; with `context: fork`, the complexity ceiling is effectively the sub-agent's full context budget.

### How does Claude Code handle conflicts between multiple skills that might give contradictory instructions?

Cross-referencing `Claude Code Best Practices` and `Context-Aware Tool Loading`: conflict resolution between skills is governed by invocation order and CLAUDE.md routing, not a registry-level priority system. The `Claude Code Best Practices` page states that "CLAUDE.md project instructions override community defaults (CLAUDE.md is read on every message), personal skills loaded explicitly override ambient skills, and `<important if='...'>` tags in CLAUDE.md provide the highest-priority override mechanism for rules that must not be ignored." Skills are loaded contextually — they enter the context window only when invoked — so a skill loaded later in a session with explicit instructions takes precedence over one loaded earlier. The `Context-Aware Tool Loading` pattern confirms there is no formal precedence specification beyond this: "the architecture resolves most conflicts via explicit routing" through CLAUDE.md acting as a routing table. For skills with direct contradictions, the pattern recommendation is to use `context: fork` for each skill, which isolates each skill's instructions in a sub-agent and prevents cross-contamination.

### How does skill performance degrade as the markdown file grows larger with more presets and options?

Cross-referencing `CLI Tools Beat MCP for Token Efficiency` and `Skills Architecture Patterns`: degradation follows the context saturation curve directly. The `CLI Tools Beat MCP for Token Efficiency` lesson documents that "schema tokens from unused tools occupy space that could hold recent conversation turns or retrieved file content, pushing relevant history out of the window earlier." For skill files, the same mechanism applies: each additional preset, option, or example section added to a skill file increases the token load every time the skill is active. The `Skills Architecture Patterns` comparison matrix notes: "context cost is the primary constraint on skill complexity — active skills consume tokens on every message." The resolution from existing wiki knowledge: instead of adding more presets to a single skill file, refactor them as separate named skills (each loaded on demand) or use progressive disclosure — the SKILL.md references detailed option files in references/ subdirectories that are only read into context when that specific option is selected. This mirrors the `Context-Aware Tool Loading` pattern's deferred loading principle applied at the intra-skill level.

## Relationships

- DERIVED FROM: src-claude-notebooklm-content-team
- DERIVED FROM: src-obsidian-claude-code-second-brain
- DERIVED FROM: src-shanraisshan-claude-code-best-practice
- DERIVED FROM: src-token-hacks-claude-code
- ENABLES: AI-Driven Content Pipeline
- ENABLES: Claude Code Scheduling
- ENABLES: Claude Code Best Practices
- ENABLES: Claude Code Context Management
- ENABLES: Wiki Event-Driven Automation
- BUILDS ON: NotebookLM
- RELATES TO: Obsidian Knowledge Vault
- RELATES TO: Skills Architecture Patterns
- USED BY: OpenFleet
- USED BY: AICP
- BUILDS ON: OpenClaw
- BUILDS ON: Claude Code

## Backlinks

[[src-claude-notebooklm-content-team]]
[[src-obsidian-claude-code-second-brain]]
[[src-shanraisshan-claude-code-best-practice]]
[[src-token-hacks-claude-code]]
[[AI-Driven Content Pipeline]]
[[Claude Code Scheduling]]
[[Claude Code Best Practices]]
[[Claude Code Context Management]]
[[Wiki Event-Driven Automation]]
[[NotebookLM]]
[[Obsidian Knowledge Vault]]
[[Skills Architecture Patterns]]
[[OpenFleet]]
[[AICP]]
[[OpenClaw]]
[[Claude Code]]
[[Always Plan Before Executing]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Context Management Is the Primary LLM Productivity Lever]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Harness Engineering]]
[[Multi-Channel AI Agent Access]]
[[NotebookLM Skills]]
[[Obsidian CLI]]
[[Obsidian Skills Ecosystem]]
[[Obsidian as Knowledge Infrastructure Not Just Note-Taking]]
[[OpenArms]]
[[Plan Execute Review Cycle]]
[[Skill Specification Is the Key to Ecosystem Interoperability]]
[[Skills Architecture Is the Dominant LLM Extension Pattern]]
[[Synthesis: 18 Claude Code Token Hacks in 18 Minutes]]
[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Claude Code Best Practice (shanraisshan)]]
[[Synthesis: Claude Code Harness Engineering]]
[[Synthesis: NotebookLM + Claude Code Workflow via notebooklm-py]]
[[Synthesis: Obsidian + Claude Code Second Brain Setup]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
[[Synthesis: PleasePrompto/notebooklm-skill]]
[[Synthesis: Superpowers Plugin — End of Vibe Coding (Full Tutorial)]]
[[Synthesis: axtonliu/axton-obsidian-visual-skills]]
[[Synthesis: claude-world/notebooklm-skill]]
[[Synthesis: kepano/obsidian-skills]]
[[Synthesis: pablo-mano/Obsidian-CLI-skill]]
[[notebooklm-py CLI]]
