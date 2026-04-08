# User Directive — 2026-04-08 — Every Interface, Every Level

## Verbatim

> should it not also be a command so I can use "/" in the conversation ? or a skills ? or both ?
> and how not everything be documented properly to every level and every interfaces ?

## Interpretation

Every operation should be accessible from EVERY interface:
1. CLI: `python3 -m tools.pipeline chain continue`
2. Skill: Claude Code reads the skill and knows how to resume
3. Slash command: `/continue` in a conversation triggers the resume flow
4. MCP: wiki_continue tool callable from any MCP client

And every operation must be DOCUMENTED at every level:
- CLAUDE.md for the agent
- Skills for the conversation
- CLI help for the terminal
- MCP tool descriptions for external clients
- SESSION artifact for cross-session resume

Nothing should exist at one interface level but not the others.
