# Continue — Resume the Research Wiki Mission

You are resuming work on the devops-solutions-research-wiki. This is a
research-grade knowledge synthesis system and second brain.

Read CLAUDE.md for conventions. Read the SESSION artifact for context.

## On Activation

Run these steps in order. Report results to the user after each.

### 1. Status Check

Run: `python3 -m tools.pipeline chain continue`

This executes: status → post-chain → evolve review → evolve score → gaps → crossref.
Report: page count, relationship count, validation errors, candidates, gaps.

### 2. Check Memory

Read `~/.claude/projects/-home-jfortin-devops-solutions-research-wiki/memory/MEMORY.md`
to recall user preferences, active projects, and pending work.

### 3. Check Unprocessed Raw Files

Run: `python3 -m tools.pipeline status`

If raw file count exceeds wiki page count significantly, there are unprocessed sources.

### 4. Present Mission State

Summarize in a table:
- Wiki stats (pages, relationships, layers, maturity distribution)
- Evolution candidates (top 5 from the score step)
- Gaps (orphans, weak domains, open question count)
- Pending work (from memory: hardware upgrade status, subsystem 3, etc.)
- Sync status: `python3 -m tools.setup --services`

### 5. Ask What's Next

Present actionable options:
- "Ingest new sources" → user provides URLs or topics
- "Evolve next batch" → scaffold + fill top candidates
- "Deepen weak domains" → focus on domains with few pages
- "Research gaps" → use web search to find sources for open questions
- "Review and promote" → check maturity promotions
- "Export to projects" → push to openfleet/AICP/OpenArms

## Available Tools

All wiki operations are available via:
- **CLI**: `python3 -m tools.pipeline <command>` (see CLAUDE.md for full list)
- **MCP**: 13 wiki tools registered in .mcp.json
- **Skills**: wiki-agent (ingest/query), evolve (evolution pipeline), continue (this)
- **Chains**: `pipeline chain --list` for all 13 named chains

## Key Chains

| Chain | Purpose |
|-------|---------|
| `continue` | Resume mission (this skill's backend) |
| `review` | Weekly health check |
| `health` | Post → gaps → crossref |
| `evolve` | Score → scaffold → post |
| `evolve-auto` | Score → scaffold → generate (local model) → post |
| `full` | Fetch → post → gaps → crossref → sync |
| `publish` | Post → sync to Windows |
