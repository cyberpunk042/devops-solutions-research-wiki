# User Directive — 2026-04-08 — MCP Cost Analysis, Design.md, New Sources

## Verbatim

> new sources with an intriging point about cli + skills vs mcp... I usually explore the 3 but I never though about the fact mcp was so costly... in his example we are talking 12X more cost with less accuracy thant skills + cli....
> https://www.youtube.com/watch?v=D5bRTv6GhXk
> he even says he has a proof video.
> So mcp would probably be better mostly for aggregated / group calls / operations. not that you can develop individual ones first but that you should probably not mindlessly add them to the agents config but only the relevants and the rest is via skills and cli somehow.
> here is the said video (first of two at least):
> https://www.youtube.com/watch?v=nN5R9DFYsXY&list=PLm7xfhMOszqy3BElDBeGJ9RQbutJiVmoK&index=1
> that's the part 2: https://www.youtube.com/watch?v=NjOqPbUecC4&list=PLm7xfhMOszqy3BElDBeGJ9RQbutJiVmoK&index=2
>
> There is also a new concept of Design.md files that could be explored. as a broad topic to start injesting and exploring and retrieving informations
>
> There is also this one if we dont already have it:
> https://www.youtube.com/watch?v=fV17ZkPBlAc
>
> And this look interesting too:
> https://www.youtube.com/watch?v=TX91PdBn_IA
>
> also can you make things executable in sub-agents and everything doable with skills I guess ?

## Interpretation

### 1. MCP Cost Discovery (12x more expensive, less accurate)
Key insight the user had NOT previously considered: MCP is not just less token-efficient — it's 12x more costly with LOWER accuracy than CLI+Skills. This dramatically strengthens the existing wiki lesson "CLI Tools Beat MCP for Token Efficiency" and the decision page "MCP vs CLI for Tool Integration."

MCP's best use case: aggregated/grouped operations, not individual tool calls. Don't add all MCP servers to agent config — only the relevant ones. The rest should be skills+CLI.

### 2. New Sources to Ingest
- https://www.youtube.com/watch?v=D5bRTv6GhXk — MCP vs Skills cost analysis (12x finding)
- https://www.youtube.com/watch?v=nN5R9DFYsXY — Proof video part 1 (MCP cost demonstration)
- https://www.youtube.com/watch?v=NjOqPbUecC4 — Proof video part 2
- https://www.youtube.com/watch?v=fV17ZkPBlAc — Unknown topic (check if already ingested)
- https://www.youtube.com/watch?v=TX91PdBn_IA — Unknown topic (looks interesting)

### 3. Design.md Concept
New concept to explore: Design.md files as a pattern for project-level design documentation. Similar to CLAUDE.md but for design decisions and architecture. Broad topic — ingest and explore.

### 4. Sub-agent Executability + Skills
User wants the evolution pipeline and other operations to be executable via sub-agents and exposed as skills. Make the system self-operating.
