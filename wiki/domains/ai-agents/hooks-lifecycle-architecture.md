---
title: "Hooks Lifecycle Architecture"
type: concept
domain: ai-agents
status: synthesized
confidence: high
created: 2026-04-09
updated: 2026-04-10
layer: 2
maturity: growing
sources:
  - id: src-claude-code-hooks-reference
    type: documentation
    url: "https://code.claude.com/docs/en/hooks"
    file: raw/articles/claude-code-hooks-reference.md
    title: "Claude Code Hooks Reference — Full Research"
    ingested: 2026-04-09
tags: [hooks, lifecycle, claude-code, pre-tool-use, post-tool-use, session-hooks, composition, stage-gating, context-injection, blocking-pattern, reverse-hook, subagent, compaction, harness-engineering]
---

# Hooks Lifecycle Architecture

## Summary

Claude Code's hook system exposes 26 lifecycle events across 7 categories — session, tool, permission, subagent, task, system, and compaction — with 4 handler types (command, http, prompt, agent). Hooks are the structural enforcement mechanism of the agent harness: they operate at execution time and can block, modify, or inject context at every major boundary in the agent loop. The blocking pattern on PreToolUse (deny/allow/ask/defer) and the reverse-hook pattern on Stop and TeammateIdle establish two complementary control axes — gating initiation and preventing premature completion. This architecture makes hooks the correct implementation substrate for stage-gate enforcement, runtime safety rules, and session continuity systems like context-mode.

## Key Insights

- **26 events, 7 categories**: The full event surface spans session lifecycle (SessionStart, SessionEnd, InstructionsLoaded, ConfigChange, CwdChanged), tool execution (PreToolUse, PostToolUse, PostToolUseFailure), permissions (PermissionRequest, PermissionDenied), subagents (SubagentStart, SubagentStop), tasks (TaskCreated, TaskCompleted), system/environment (Notification, FileChanged, WorktreeCreate, WorktreeRemove, Elicitation, ElicitationResult), and compaction (PreCompact, PostCompact). Plus Stop, StopFailure, TeammateIdle, and UserPromptSubmit. No agent boundary is left uncovered.

> [!info] Handler types reference card
>
> | Handler | How It Works | Cost/Capability |
> |---------|-------------|----------------|
> | `command` | Shell script receiving JSON on stdin | Low cost, supports `async: true` fire-and-forget |
> | `http` | POST to an endpoint | External integration, decoupled |
> | `prompt` | Single-turn LLM evaluation | Lightweight AI reasoning at hook boundaries |
> | `agent` | Full subagent with tool access | Highest capability, highest cost |

> [!warning] PreToolUse is the primary enforcement surface
> A hook can block all `Write`/`Edit` calls to `src/` during documentation phase — enforcing "no implementation in document stage" at the infrastructure level. Impossible to violate, not merely discouraged. This closes the compliance gap: instruction files ~60% → programmatic hooks ~98%.
>
> Four decision gradations: **block** (hard denial), **allow** (unconditional pass), **ask** (escalate to user), **defer** (pass to next hook in chain).

- **The blocking pattern**: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, TaskCreated, TaskCompleted, ConfigChange all support blocking. Exit code 2 or `{"decision": "block"}` halts the operation.

- **The reverse hook concept**: Stop and TeammateIdle invert PreToolUse. PreToolUse gates initiation; Stop can block completion (forcing the agent to continue). Bidirectional control across the full agent loop.

- **Context injection**: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart accept `additionalContext` — structured info injected into the conversation without user intervention. This is how context-mode restores state after compaction.

- **Scope hierarchy**: user settings → project settings → local settings → plugins → policies. Lower scopes add but cannot remove higher-scope hooks. Matchers compose via exact string, pipe-separated list, regex, and `if` filters.

## Deep Analysis

### The 7 Event Categories as a Control Plane Map

The 26 events are not arbitrary — they map to every meaningful boundary in the agent execution model:

| Category | Events | Control Use Case |
|---|---|---|
| Session | SessionStart, SessionEnd, InstructionsLoaded, ConfigChange, CwdChanged | Context restoration, environment setup, config validation |
| Tool | PreToolUse, PostToolUse, PostToolUseFailure | Block dangerous ops, modify inputs, validate outputs, enforce stage gates |
| Permission | PermissionRequest, PermissionDenied | Custom permission logic, override default ask behavior |
| Subagent | SubagentStart, SubagentStop | Inject subagent context, aggregate subagent results |
| Task | TaskCreated, TaskCompleted | Readiness validation, downstream triggers |
| System | Notification, FileChanged, WorktreeCreate, WorktreeRemove, Elicitation, ElicitationResult, UserPromptSubmit | Environment reactions, user-input preprocessing |
| Compaction | PreCompact, PostCompact | State snapshot before compaction, restoration after |

The `Stop` and `TeammateIdle` events sit outside this taxonomy as meta-control hooks — they govern whether the agent loop itself terminates.

### PreToolUse as the Primary Enforcement Surface

PreToolUse is the highest-leverage hook for runtime safety. Its decision model has four gradations:

- **block**: Hard denial. Logs reason. Operation aborted.
- **allow**: Unconditional pass-through. Skips Claude's built-in permission checks.
- **ask**: Escalate to user approval. Pauses execution with structured question.
- **defer**: Pass to the next matching hook. Enables hook composition chains.

The `updatedInput` capability means PreToolUse can also *sanitize* inputs before execution — not just block them. A hook could strip dangerous flags from a `git push` command, rewrite a destructive `rm` to a safer alternative, or inject required arguments. This is qualitatively more powerful than binary block/pass: the agent keeps working, but within safe parameters.

For stage-gate enforcement, the correct pattern is:
```
PreToolUse matcher: Write, Edit
if filter: path matches src/**
decision: block (with reason: "document stage — no implementation writes")
```
This enforces the OpenArms "Document stage: MUST NOT write code" constraint at the infrastructure level with no LLM compliance required.

### The Reverse Hook Axis

The Stop/TeammateIdle hooks address a failure mode that PreToolUse cannot: premature task completion. An agent that has not finished a required step may still signal Stop. A PreToolUse hook cannot catch this — the agent never attempted a tool call to block. The Stop hook fires after the response and can return `{"decision": "block", "reason": "validation checks not run"}` to force continuation. This is the mechanism for post-completion quality gates: run validation, check required outputs, and only allow Stop when the task meets exit criteria.

TeammateIdle serves a parallel role in multi-agent setups: when an agent in a fleet goes idle before its assigned work window closes, TeammateIdle can push a new task assignment rather than allowing idle waste.

Together, Stop (prevent premature completion) and PreToolUse (prevent forbidden initiation) bracket the task execution window from both ends.

### Connection to Context-Mode: 5 Hooks for Session Continuity

Context-mode's session continuity system uses exactly 5 of the 26 hooks:

| Hook | Role in Context-Mode |
|---|---|
| PreToolUse | Enforce sandbox routing — block direct data-processing tool chains |
| PostToolUse | Capture file edits, git ops, errors, tasks, env changes as SQLite events |
| UserPromptSubmit | Capture user decisions, corrections, intent, data references |
| PreCompact | Build priority-tiered XML snapshot (≤2 KB) before compaction fires |
| SessionStart | Restore session state — inject Session Guide into context |

The compliance gap between hooks and instruction files (98% vs 60% context savings) is entirely explained by PreToolUse: instruction files can be ignored under load; PreToolUse blocking cannot. The hook selection is not arbitrary — these 5 hooks correspond exactly to the 5 distinct session-continuity failure modes: routing failures, state loss, decision loss, compaction amnesia, and resume blindness.

### Handler Type Selection

| Handler | When to Use | Tradeoff |
|---|---|---|
| `command` | Shell-level validation, file operations, external process invocation | Fastest; supports `async: true`; full OS access |
| `http` | Remote validation services, logging to centralized audit trail | Network latency; requires running service |
| `prompt` | Lightweight AI judgment at boundaries ("is this commit message safe?") | Token cost per hook fire; only single-turn |
| `agent` | Complex multi-step validation requiring tool access | Highest power; highest cost; creates subagent overhead |

For runtime safety rules (the harness engineering use case), `command` is correct: Python script, zero latency, full filesystem access, exit code 2 to block. For plan annotation (the Plannotator use case), `prompt` or `agent` is appropriate — the validation itself requires reasoning. For async audit logging, `http` with `async: true` is the correct pattern.

### Scope Hierarchy Implications

The 5-layer scope hierarchy (user → project → local → plugins → policies) has a critical operational implication: hooks at the `policies` layer are organization-enforced and cannot be overridden by lower scopes. This is the correct substrate for shared guardrail rules across a multi-project ecosystem: define safety rules at policy scope, allow individual projects to add project-specific rules at project scope, and reserve local scope for developer-specific preferences. The ecosystem (openfleet, AICP, DSPD, devops-control-plane) could share a common policy-scope hook set for cross-project safety invariants.

## Open Questions

- Can a single PreToolUse hook read the current stage from an external state file to make dynamic blocking decisions (e.g., block writes when `stage == "document"` and allow them when `stage == "implement"`)? This would require hooks to have read access to the filesystem — command handlers do, but is it within the documented pattern?
- How do hooks interact with Claude Code's built-in `--dangerously-skip-permissions` flag? Can policy-scope hooks block this override, or does the flag bypass the entire hook system?
- What is the hook invocation latency budget for command handlers in a fast-paced development session? If PreToolUse fires on every Bash call and each handler takes 100ms, a session with 500 tool calls adds ~50 seconds of overhead.
- Can `agent`-type hook handlers themselves trigger further hooks (recursive hook chains)? What is the depth limit?
- Is there a hook for plan generation specifically (before the agent commits to an execution strategy)? Plannotator suggests this exists but the 26-event list does not explicitly name a "PlanGenerated" event — is this handled via a `prompt` handler on UserPromptSubmit?

## Relationships

- EXTENDS: [[Harness Engineering]]
- IMPLEMENTS: [[Task Lifecycle Stage-Gating]]
- ENABLES: [[Context-Aware Tool Loading]]
- RELATES TO: [[Synthesis: Context Mode — MCP Sandbox for Context Saving]]
- RELATES TO: [[Claude Code Best Practices]]
- RELATES TO: [[Claude Code]]
- RELATES TO: [[Plannotator — Interactive Plan & Code Review for AI Agents]]
- FEEDS INTO: [[Per-Role Command Architecture]]
- FEEDS INTO: [[Design.md Pattern]]
- BUILDS ON: [[Agent Orchestration Patterns]]

## Backlinks

[[Harness Engineering]]
[[Task Lifecycle Stage-Gating]]
[[Context-Aware Tool Loading]]
[[Synthesis: Context Mode — MCP Sandbox for Context Saving]]
[[Claude Code Best Practices]]
[[Claude Code]]
[[Plannotator — Interactive Plan & Code Review for AI Agents]]
[[Per-Role Command Architecture]]
[[Design.md Pattern]]
[[Agent Orchestration Patterns]]
[[Claude Code Standards — What Good Agent Configuration Looks Like]]
[[Model: Claude Code]]
[[Model: Skills, Commands, and Hooks]]
