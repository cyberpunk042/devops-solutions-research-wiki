# Decisions

Choice frameworks with alternatives, rationale, and reversibility assessment.

## Resolved Decisions

| Decision | Choice Made | Reversibility |
|----------|------------|--------------|
| [[Decision: MCP vs CLI for Tool Integration]] | CLI+Skills default, MCP for external services | Easy |
| [[Decision: Obsidian vs NotebookLM as Knowledge Interface]] | Both — complementary roles | Easy |
| [[Decision: Local Model vs Cloud API for Routine Operations]] | Route by complexity: local for simple, Claude for complex | Easy |
| [[Decision: Polling vs Event-Driven Change Detection]] | Polling on WSL2 (inotify unreliable on /mnt/c) | Easy |
| [[Decision: Wiki-First with LightRAG Upgrade Path]] | Wiki now, LightRAG additive at 200+ pages | Easy |

## Pages

- [Decision: Local Model vs Cloud API for Routine Operations](local-model-vs-cloud-api-for-routine-operations.md) — For routine wiki and devops operations, use local models (LocalAI/AICP) for mechanical, deterministic, and output-val...
- [Decision: MCP vs CLI for Tool Integration](mcp-vs-cli-for-tool-integration.md) — When integrating tools into LLM-powered workflows, CLI+Skills is the default preferred approach for operational tasks...
- [Decision: Obsidian vs NotebookLM as Knowledge Interface](obsidian-vs-notebooklm-as-knowledge-interface.md) — Obsidian and NotebookLM serve complementary roles as knowledge interfaces and should both be maintained rather than c...
- [Decision: Polling vs Event-Driven Change Detection](polling-vs-event-driven-change-detection.md) — On WSL2, polling is the correct change detection strategy for the wiki watcher daemon
- [Decision: Wiki-First with LightRAG Upgrade Path](wiki-first-with-lightrag-upgrade-path.md) — This wiki operates in wiki-first mode — pure structured markdown with index navigation — until it approaches 200 page...

## Tags

`aicp`, `localai`, `claude`, `routing`, `local-first`, `cost-optimization`, `backend-selection`, `complexity-scoring`, `wiki-pipeline`, `mcp`, `cli`, `skills`, `tool-integration`, `token-efficiency`, `claude-code`, `integration-pattern`, `context-management`, `obsidian`, `notebooklm`, `knowledge-interface`
