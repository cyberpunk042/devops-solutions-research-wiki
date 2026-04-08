# Building Claude Code with Harness Engineering

Source: https://levelup.gitconnected.com/building-claude-code-with-harness-engineering-d2e8c0da85f0
Ingested: 2026-04-08
Type: article

---

Article by Fareed Khan on harness engineering patterns for Claude Code. Content combined with claude-code-harness GitHub project research.

## Key Concepts

### Harness Engineering
The practice of building structured control systems around an LLM coding agent. Not just prompt engineering — runtime guardrails, quality validation, and rerunnable verification that keep development on a defined path.

### Core Claude Code Harness Components (from Anthropic's engineering)
- Streaming agent loop: single-threaded master loop driving perception → reasoning → tool execution cycles
- Permission-governed tool dispatch: typed registry mapping tool names to handlers with strict input schemas  
- Context management layer: keeps model focused across arbitrarily long sessions
- Claude Code crossed $1B annualized revenue within 6 months of launch

### Claude Code Harness (Chachamaru127 project)
A community framework implementing harness engineering patterns:

**5-Verb Workflow:**
1. /harness-setup — initialize project with rules and command surfaces
2. /harness-plan — convert ideas to documented plans with acceptance criteria
3. /harness-work — implement via parallel workers with self-checks and review
4. /harness-review — 4-perspective analysis (security, performance, quality, accessibility)
5. /harness-release — package into CHANGELOG, version tags, GitHub Release

**TypeScript Guardrail Engine (13 rules R01-R13):**
- Denial rules: block sudo, .git/.env writes, force-push, protected-branch pushes
- Query rules: flag writes outside project scope, destructive operations
- Security rules: prevent --no-verify, direct main/master modifications
- Post-execution: warn against assertion tampering, it.skip patterns

**Advanced Execution:**
- Breezing (Agent Teams): automated multi-agent with Planner + Critic roles
- Codex Engine integration: parallel implementation alongside Claude Code
- /harness-work all: experimental full loop (plan → implement → review → commit)

**Key Insight — CLI over MCP:**
Article references trend of CLI+Skills over MCP for tool integration. CLI is more token-efficient (skills only load when relevant), produces fewer hallucinations, and costs less. Playwright CLI vs MCP comparison showed CLI was cheaper and more accurate.

**Knowledge Base Pattern:**
Using NotebookLM as external knowledge base instead of stuffing docs into context. Claude fetches from NotebookLM only when needed, keeping context clean. Sources grounded — only uses what you provided.
