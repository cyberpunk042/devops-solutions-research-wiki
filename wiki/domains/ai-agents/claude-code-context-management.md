---
title: "Claude Code Context Management"
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
tags: [claude-code, context-window, token-management, CLAUDE-md, compact, prompt-caching, MCP-overhead, cost-optimization, memory, context-engineering]
---

# Claude Code Context Management

## Summary

Context management in Claude Code is the discipline of controlling what occupies the model's limited context window to maximize both output quality and session longevity. Every Claude Code message re-reads the entire conversation history, CLAUDE.md files, MCP server definitions, system prompts, skills, and referenced files -- making costs compound exponentially rather than linearly as conversations grow. A developer tracking a 100+ message chat found that 98.5% of tokens were spent re-reading old history. Context management encompasses three concerns: reducing invisible overhead (lean CLAUDE.md, disconnecting unused MCPs, controlling command output), managing session lifecycle (starting fresh conversations, manual compaction at 60%, strategic clearing before breaks), and making costs visible (/context, /cost, status line monitoring). The "lost in the middle" phenomenon -- where models attend most to the beginning and end of context, ignoring the middle -- means that bloated context degrades output quality in addition to increasing cost.

## Key Insights

- **Exponential cost compounding**: Every message re-reads all prior messages plus their responses. Message 1 costs approximately 500 tokens; message 30 costs approximately 15,000 tokens (31x more). After 30 messages, cumulative token consumption approaches 250,000. This is not linear addition -- it is geometric growth that makes long conversations vastly more expensive per-token than fresh ones.

- **Invisible overhead is substantial**: Before a single word of conversation, a fresh Claude Code session already consumes approximately 51,000 tokens from system prompts, system tools, custom agents, skills, and memory files. MCP servers add more -- a single server can cost 18,000 tokens per message, loaded invisibly on every turn. The total invisible overhead can represent a significant fraction of the context window before any work begins.

- **CLAUDE.md as context engineering**: CLAUDE.md is re-read on every message, making it the single most impactful factor in per-message overhead. The best practice is: keep it under 200 lines, treat it as an index/router rather than an encyclopedia, use `.claude/rules/` to split large instructions, and wrap critical rules in `<important if="...">` tags to prevent them from being ignored as files grow. Every line in CLAUDE.md is effectively multiplied by the total number of messages in every session.

- **Prompt cache 5-minute TTL**: Claude Code caches prompt context to avoid reprocessing unchanged content, but the cache expires after 5 minutes of inactivity. Returning after a break means the next message reprocesses everything from scratch at full token cost. Either compact or clear before stepping away.

- **Manual compaction at 60%**: Auto-compact triggers at 95% capacity, by which point context is already degraded due to the lost-in-the-middle phenomenon. The recommendation is to manually run /compact with specific instructions about what to preserve at 60%. After 3-4 consecutive compactions, quality degrades noticeably -- at that point, get a session summary, /clear, feed the summary into a fresh session, and continue.

- **MCP servers are a major cost vector**: Every connected MCP server loads all its tool definitions on every message. The recommendation is to disconnect unused servers at session start using `/mcp` and prefer CLIs over MCPs where possible. The token hacks source suggests the future moves toward agents using CLIs rather than MCPs because CLIs are faster and cheaper.

- **Command output enters context**: When Claude runs shell commands, the full output (git log with 200 commits, verbose build output, etc.) enters the context window as tokens. Being intentional about what Claude is allowed to run -- and denying permissions for noisy commands in specific projects -- prevents silent context bloat.

- **Lost in the middle**: Research shows models attend most strongly to the beginning and end of the context window, with reduced attention to content in the middle. This means a long conversation is not just more expensive -- the middle sections are actively producing worse output. Fresh conversations with relevant context always outperform continuing a bloated session.

- **Visibility tools are essential**: /context breaks down what is consuming the context window (conversation history, MCP overhead, loaded files). /cost shows actual token usage and estimated spend. Setting up a status line showing model, context percentage, and token count provides continuous ambient awareness. The Claude usage dashboard shows remaining allocation and reset time.

- **Model selection as cost control**: Sonnet for default coding, Haiku for sub-agents and simple formatting tasks, Opus only for deep architectural planning when Sonnet is insufficient (keep under 20% of usage). Sub-agents cost 7-10x more tokens than single-agent sessions because each spawns with its own full context reload.

- **Peak hour awareness**: The 5-hour session window drains faster during peak hours (8 AM - 2 PM Eastern weekdays). Scheduling heavy refactors and multi-agent sessions for off-peak hours (afternoons, evenings, weekends) gives more actual compute per session window.

- **Batch prompts to reduce re-reads**: Three separate messages cost roughly three times what one combined message costs because each message triggers a full context re-read. Combining related instructions into a single prompt reduces the number of re-reads. If Claude makes a small error, editing the original message and regenerating replaces the bad exchange entirely, while a follow-up correction stacks permanently onto history.

## Deep Analysis

Context management is arguably the most impactful Claude Code skill because it determines the fundamental economics of every session. A developer who practices good context hygiene gets 3-5x more useful work per session than one who does not, simply by reducing the geometric growth of token consumption.

The insight that CLAUDE.md is re-read on every message transforms how it should be designed. The traditional instinct is to make CLAUDE.md comprehensive -- documenting every convention, every architecture decision, every workflow. But this is precisely wrong: a 1,000-line CLAUDE.md means 1,000 lines of tokens charged on every single message, even a simple "yes" response. The correct mental model is that CLAUDE.md is a hot path in a performance-critical system. Every line must justify its per-message cost by being referenced frequently enough. Infrequently needed information should live in files that CLAUDE.md points to but that are only loaded on demand.

The MCP overhead finding connects to a broader pattern: Claude Code's extensibility mechanisms (skills, MCPs, agents) all have context costs that are invisible to the user but very real in token terms. The architectural implication is that Claude Code users face a tradeoff curve between capability breadth (more tools available) and context efficiency (less overhead per message). The optimal point varies by task: a focused coding session needs minimal MCP connections, while an orchestration task might justify the overhead of multiple servers.

The compaction strategy (manual at 60%, summarize-and-clear after 3-4 compacts) reveals that context management is not just about individual messages but about session lifecycle design. A well-managed session has three phases: an initial phase where context is fresh and work is most productive, a middle phase where strategic compaction preserves key context while reclaiming space, and a transition phase where the session is gracefully ended and key state is transferred to a new session. Users who treat sessions as indefinitely extensible (just keep going until hitting the limit) are fighting the geometry of token compounding.

The connection between context management and the LLM Wiki Pattern is direct. The wiki pattern's approach -- structured markdown with indexes, no vector databases -- is itself a context management strategy. By pre-organizing knowledge into navigable structures, the wiki reduces the amount of context needed per query compared to dumping raw documents into the conversation. The CLAUDE.md-as-index principle is the same pattern applied to the agent's own configuration.

The 5-minute prompt cache TTL is a subtle but important operational detail. It means that the difference between a 4-minute break and a 6-minute break can be thousands of tokens on the next message. Developers who understand this will either compact before stepping away or plan their breaks to be either very short (under 5 minutes) or preceded by a context management step.

## Open Questions

- What is the exact relationship between context window utilization and output quality degradation? Is there a sharp knee or a gradual decline?
- Can the prompt cache TTL be extended or configured by the user?
- What is the optimal CLAUDE.md size in practice -- is 200 lines a hard ceiling, or is the real metric total token count (which varies with content complexity)?
- How does the lost-in-the-middle phenomenon interact with compaction -- does compacting effectively move important content back to the "edges" of attention?
- Is there a tool or technique to profile per-message token cost broken down by component (conversation history vs. CLAUDE.md vs. MCP overhead vs. system prompt)?
- How do the economics change with different subscription plans -- is context management equally important on the $200/month plan as on the $20/month plan?
- Cross-source insight: How does the cost of a full wiki linting pass (which reads the entire wiki) interact with context window limits? LLM Knowledge Linting and context management are fundamentally in tension -- linting requires broad reads while context management demands narrow ones. Incremental linting (only pages changed since last pass) may be the resolution.
- Cross-source insight: The wiki ingestion pipeline's batch mode (36 transcripts in 14 minutes) implies significant context consumption per batch. What are optimal batch sizes given context compounding?

## Relationships

- DERIVED FROM: src-shanraisshan-claude-code-best-practice
- DERIVED FROM: src-token-hacks-claude-code
- BUILDS ON: Claude Code Skills
- BUILDS ON: Claude Code Best Practices
- RELATES TO: LLM Wiki Pattern
- RELATES TO: Memory Lifecycle Management
- RELATES TO: Wiki Knowledge Graph
- CONSTRAINS: Wiki Ingestion Pipeline
- CONSTRAINS: LLM Knowledge Linting
- RELATES TO: Skills Architecture Patterns
- EXTENDS: Claude Code

## Backlinks

[[src-shanraisshan-claude-code-best-practice]]
[[src-token-hacks-claude-code]]
[[Claude Code Skills]]
[[Claude Code Best Practices]]
[[LLM Wiki Pattern]]
[[Memory Lifecycle Management]]
[[Wiki Knowledge Graph]]
[[Wiki Ingestion Pipeline]]
[[LLM Knowledge Linting]]
[[Skills Architecture Patterns]]
[[Claude Code]]
[[CLI Tools Beat MCP for Token Efficiency]]
[[Context-Aware Tool Loading]]
[[Decision: MCP vs CLI for Tool Integration]]
[[Synthesis: 18 Claude Code Token Hacks in 18 Minutes]]
[[Synthesis: Claude Code Accuracy Tips]]
[[Synthesis: Claude Code Best Practice (shanraisshan)]]
[[Synthesis: Playwright CLI vs MCP — Automate QA with Less Tokens]]
[[Synthesis: Playwright MCP for Visual Development Testing]]
