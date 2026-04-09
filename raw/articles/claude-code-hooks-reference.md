# Claude Code Hooks Reference — Full Research

Source: https://code.claude.com/docs/en/hooks
Compiled: 2026-04-09

## 26 Lifecycle Events

SessionStart, UserPromptSubmit, InstructionsLoaded, PreToolUse, PermissionRequest,
PostToolUse, PostToolUseFailure, PermissionDenied, Notification, SubagentStart,
SubagentStop, TaskCreated, TaskCompleted, Stop, StopFailure, TeammateIdle,
ConfigChange, CwdChanged, FileChanged, WorktreeCreate, WorktreeRemove,
PreCompact, PostCompact, Elicitation, ElicitationResult, SessionEnd

## 4 Handler Types
- command: shell script receives JSON on stdin
- http: POST to endpoint
- prompt: single-turn LLM evaluation
- agent: subagent with tool access

## Key Capabilities
- Block actions: PreToolUse, PermissionRequest, UserPromptSubmit, Stop, TaskCreated, TaskCompleted, ConfigChange (exit 2 or JSON decision:block)
- Modify tool input: PreToolUse, PermissionRequest (updatedInput)
- Inject context: SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, SubagentStart (additionalContext)
- Control MCP: Elicitation, ElicitationResult
- Set env vars: SessionStart, CwdChanged, FileChanged (CLAUDE_ENV_FILE)
- Async execution: command hooks only (async: true)

## Reverse Hook Pattern
- Stop hook: fires when Claude finishes responding. Can BLOCK the stop — forcing continuation.
- TeammateIdle: fires when agent teammate is idle. Can prevent idle (keep working).
- These are "reverse" because they PREVENT completion rather than GATE initiation.

## Composition
- Matchers: exact string, pipe-separated list, or JavaScript regex
- MCP tool matching: mcp__server__tool pattern
- Per-event matchers: SessionStart matches startup|resume|clear|compact
- if filters: permission rule syntax Bash(rm *), Edit(*.ts)
- Hook deduplication: identical handlers run only once
- Scope hierarchy: user settings → project settings → local settings → plugins → policies
