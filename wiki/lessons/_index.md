# Lessons

Structured failure analysis and convergence insights synthesized from real incidents, post-mortems, and cross-source pattern detection. Every lesson has a trigger, a finding, and an action.

**Model:** [[Model: Quality and Failure Prevention]] | **Standards:** [[Quality Standards — What Good Failure Prevention Looks Like]]

### Start Here

1. [[The Agent Must Practice What It Documents]] — The root failure lesson
2. [[LLM-Maintained Wikis Outperform Static Documentation]] — The root convergence lesson
3. [[Agent Orchestration Is the Highest-Connected Concept in the Wiki]] — The most connected hub

### Failure Lessons

Hard-won rules from post-mortems and agent death analyses.

| Lesson | Core finding |
|--------|-------------|
| [[The Agent Must Practice What It Documents]] | Documenting methodology without following it is the deepest failure |
| [[Never Skip Stages Even When Told to Continue]] | "Get started" means the current stage, not "skip to the end" |
| [[Never Synthesize from Descriptions Alone]] | A README about a format is not understanding the format |
| [[Shallow Ingestion Is Systemic, Not Isolated]] | Subagents consistently read only ~60 lines of 300-1000+ line files |
| [[Infrastructure Must Be Reproducible, Not Manual]] | Never manually create systemd/cron; build into reproducible tooling |
| [[Models Are Built in Layers, Not All at Once]] | Models follow SFIF: scaffold, fill, iterate, finish |

### Practice Lessons

Operational patterns that improve agent effectiveness.

| Lesson | Core finding |
|--------|-------------|
| [[Always Plan Before Executing]] | Explicit plans before action produce dramatically better results |
| [[CLI Tools Beat MCP for Token Efficiency]] | CLI + skill files outperform MCP for token efficiency |
| [[Context Management Is the Primary LLM Productivity Lever]] | Context window management is the biggest productivity multiplier |
| [[Multi-Stage Ingestion Beats Single-Pass Processing]] | Extract, cross-reference, identify gaps, deepen — not one-shot |

### Convergence Lessons

Independent sources arriving at the same conclusion.

| Lesson | Core finding |
|--------|-------------|
| [[LLM-Maintained Wikis Outperform Static Documentation]] | LLM maintenance with validation and quality gates beats static docs |
| [[Skills Architecture Is the Dominant LLM Extension Pattern]] | Bundled markdown packages are the dominant extension pattern |
| [[Graph-Enhanced Retrieval Bridges Wiki Navigation and Vector Search]] | Wiki navigation vs vector RAG is a false binary |
| [[Automated Knowledge Validation Prevents Silent Wiki Decay]] | Wikis without automated validation decay silently |
| [[Obsidian as Knowledge Infrastructure Not Just Note-Taking]] | Obsidian is programmable knowledge infrastructure, not a markdown editor |
| [[NotebookLM as Grounded Research Engine Not Just Note Storage]] | NotebookLM is a grounded research engine, not just note storage |
| [[The Wiki Maintenance Problem Is Solved by LLM Automation]] | LLMs solve the maintenance burden that killed every previous wiki attempt |
| [[Skill Specification Is the Key to Ecosystem Interoperability]] | Open specification roots make skills portable across platforms |
| [[Schema Is the Real Product — Not the Content]] | The schema file is the real product; content is generated from it |

### Domain Hubs

Lessons that synthesize an entire domain's structural position.

| Lesson | Domain |
|--------|--------|
| [[Agent Orchestration Is the Highest-Connected Concept in the Wiki]] | ai-agents |
| [[Automation Is the Bridge Between Knowledge and Action]] | automation |
| [[Knowledge Systems Is the Foundational Domain for the Entire Wiki]] | knowledge-systems |

## Pages

- [Lesson: Agent Orchestration Is the Highest-Connected Concept in the Wiki](agent-orchestration-is-highest-connected-concept.md) — Agent Orchestration Patterns is the most inbound-linked concept in the ai-agents domain
- [Always Plan Before Executing](always-plan-before-executing.md) — LLM agents produce dramatically better results when they produce an explicit plan before taking action — not as a sof...
- [Automated Knowledge Validation Prevents Silent Wiki Decay](automated-knowledge-validation-prevents-wiki-decay.md) — Wikis without automated validation decay silently: pages go stale, relationships break, orphaned concepts accumulate,...
- [Lesson: Automation Is the Bridge Between Knowledge and Action](automation-is-bridge-between-knowledge-and-action.md) — The automation domain occupies a distinct structural position in this wiki: it bridges what the knowledge-systems dom...
- [CLI Tools Beat MCP for Token Efficiency](cli-tools-beat-mcp-for-token-efficiency.md) — When integrating external tools into LLM-powered workflows, CLI tools paired with skill files consistently outperform...
- [Context Management Is the Primary LLM Productivity Lever](context-management-is-primary-productivity-lever.md) — Across all sources analyzing Claude Code effectiveness — practitioner guides, harness engineering frameworks, accurac...
- [Graph-Enhanced Retrieval Bridges Wiki Navigation and Vector Search](graph-enhanced-retrieval-bridges-wiki-and-vector-search.md) — The choice between wiki-style navigation and vector RAG is a false binary
- [Infrastructure Must Be Reproducible, Not Manual](infrastructure-must-be-reproducible-not-manual.md) — The AI agent attempted to create a systemd service file by directly writing it with `cat >` instead of building the s...
- [Lesson: Knowledge Systems Is the Foundational Domain for the Entire Wiki](knowledge-systems-is-foundational-domain.md) — The knowledge-systems domain is the only domain in this wiki where the wiki documents how it works
- [LLM-Maintained Wikis Outperform Static Documentation](llm-maintained-wikis-outperform-static-documentation.md) — Having an LLM maintain a structured wiki — with validation, relationship discovery, quality gates, and index auto-mai...
- [Models Are Built in Layers, Not All at Once](models-are-built-in-layers-not-all-at-once.md) — Building the 14 named models for this wiki followed the same SFIF pattern that the wiki documents as universal: scaff...
- [Multi-Stage Ingestion Beats Single-Pass Processing](multi-stage-ingestion-beats-single-pass.md) — Ingestion should be multi-pass — extract, then cross-reference, then identify gaps, then deepen — rather than one-shot
- [Never Skip Stages Even When Told to Continue](never-skip-stages-even-when-told-to-continue.md) — When the user said "you have everything to get started," the agent interpreted this as permission to skip the brainst...
- [Never Synthesize from Descriptions Alone](never-synthesize-from-descriptions-alone.md) — Reading a README that describes a format is not the same as reading an actual instance of that format
- [NotebookLM as Grounded Research Engine Not Just Note Storage](notebooklm-as-grounded-research-engine.md) — Three independent implementations of NotebookLM integrations (PleasePrompto, claude-world, and the notebooklm-py work...
- [Obsidian as Knowledge Infrastructure Not Just Note-Taking](obsidian-as-knowledge-infrastructure.md) — Multiple independent projects converge on Obsidian not as a markdown editor but as programmable knowledge infrastruct...
- [Lesson: Schema Is the Real Product — Not the Content](schema-is-the-real-product.md) — Karpathy's primary source document identifies the schema file (CLAUDE
- [Shallow Ingestion Is Systemic, Not Isolated](shallow-ingestion-is-systemic-not-isolated.md) — Subagents consistently read only the first ~60 lines of raw files that were 300-1000+ lines long, due to the Read too...
- [Skill Specification Is the Key to Ecosystem Interoperability](skill-specification-is-key-to-interoperability.md) — When a skill definition format is rooted in an open specification rather than a proprietary platform, skills become p...
- [Skills Architecture Is the Dominant LLM Extension Pattern](skills-architecture-is-dominant-extension-pattern.md) — Skills — bundled markdown packages that combine instructions, context, scripts, and design guidance — have emerged as...
- [The Agent Must Practice What It Documents](the-agent-must-practice-what-it-documents.md) — The research wiki documented methodology extensively — stage gates, brainstorm-before-spec, research-before-design, m...
- [The Wiki Maintenance Problem Is Solved by LLM Automation](wiki-maintenance-problem-solved-by-llm-automation.md) — Every personal wiki attempt before LLMs failed for the same reason: maintenance burden grew faster than value, and hu...

## Tags

`failure-lesson`, `methodology`, `quality`, `llm-wiki`, `second-brain`, `orchestration`, `cross-domain`, `claude-code`, `automation`, `maintenance`, `skills`, `compounding-knowledge`, `knowledge-graph`, `openfleet`, `harness-engineering`, `planning`, `agent-behavior`, `wiki-decay`, `pipeline`, `mcp`
