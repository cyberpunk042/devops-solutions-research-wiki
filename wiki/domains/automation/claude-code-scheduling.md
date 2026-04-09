---
title: "Claude Code Scheduling"
type: concept
domain: automation
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
tags: [claude-code, scheduling, cron, remote-tasks, automation, anthropic-cloud]
---

# Claude Code Scheduling

## Summary

Claude Code supports scheduling recurring tasks through two mechanisms: local cron jobs that run on the user's machine, and remote tasks that run on Anthropic's cloud infrastructure. Local scheduling uses the schedule tab in Claude's sidebar to define tasks with a name, description, prompt, workspace, and time specification, which creates a cron schedule task on the local machine. Remote tasks, a newer feature from Anthropic, run on Anthropic Cloud and require a GitHub account with the workspace uploaded to GitHub. Additionally, Claude Code can configure scheduling programmatically based on the user's existing setup, such as writing to a cron registry JSON file.

## Key Insights

- **Two scheduling modes — local and remote**: Local tasks create cron jobs on the user's machine and only run when the device is powered on. Remote tasks run on Anthropic Cloud and execute regardless of whether the user's machine is on, but require a GitHub account and GitHub-hosted workspace.

- **GUI and conversational setup**: Users can set up scheduled tasks through the schedule tab in Claude's left sidebar (GUI approach) or by asking Claude Code directly to schedule something (conversational approach). Claude Code is flexible enough to determine the best scheduling method based on the user's existing setup.

- **Cron registry pattern**: The presenter's setup uses a cron registry text file (actually a JSON file) that lists all scheduled tasks with their cron timestamps. Claude Code can read this file, add new entries, and configure the timing — for example, setting "12:00 p.m. Sydney time" as a cron expression.

- **Permissions bypass for low-risk tasks**: When creating scheduled tasks, there is an option to set "bypass permissions mode" for tasks deemed low risk. The presenter enables this for the cybersecurity research daily task, allowing it to run without manual approval.

- **Task specification includes workspace context**: Each scheduled task is associated with a specific folder or workspace, ensuring Claude Code operates in the correct context when the task fires.

- **Integration with long-running sessions**: The presenter runs six long-running Claude Code sessions in an IDE terminal, each corresponding to a different agent workspace. Scheduled tasks feed into these sessions, and confirmations are sent via Telegram — creating an always-on assistant pattern.

- **Practical example — daily cybersecurity research**: The demonstrated use case is scheduling daily cybersecurity trend research at noon Sydney time, where Claude Code uses NotebookLM to research topics, load sources, and generate slides in a specified design, all without user intervention.

## Deep Analysis

Scheduling is the capability that transforms Claude Code from a reactive assistant (responds when prompted) into a proactive agent (acts on its own schedule). This is a significant architectural shift because it means the user does not need to be present or even aware when work is being done.

The local vs. remote distinction reflects a practical infrastructure trade-off. Local cron is simpler — no external dependencies, no GitHub requirement — but it depends on machine uptime. Remote tasks solve the availability problem but introduce dependencies on Anthropic's cloud infrastructure and GitHub for workspace access. For professional or production use cases where reliability matters, remote tasks are clearly preferable, but local cron is adequate for personal workflows where the user's machine is typically on during the scheduled hours.

The presenter's cron registry JSON pattern is interesting because it shows Claude Code adapting to an existing user setup rather than imposing its own scheduling mechanism. Rather than only supporting the built-in schedule tab, Claude Code recognized the existing JSON-based cron registry and wrote to it. This flexibility is a hallmark of the agent paradigm — the tool adapts to the user's infrastructure rather than requiring the user to adapt.

The Telegram notification integration mentioned in passing is significant because it closes the feedback loop for scheduled tasks. Without notifications, the user would need to check manually whether tasks completed. By routing confirmations through Telegram, the presenter has created a complete automation loop: schedule triggers execution triggers notification triggers human awareness.

The "bypass permissions mode" for low-risk tasks is a trust calibration mechanism. It acknowledges that not all automated actions carry the same risk, and that requiring manual approval for every scheduled action would defeat the purpose of scheduling. However, this raises questions about what constitutes "low risk" and whether there are guardrails to prevent a scheduled task from taking unexpected actions.

## Preferred Work Window / Off-Peak Usage

Anthropic offers usage multipliers based on time of day. From a scheduling perspective, this is critical for cost optimization:

- **Peak hours**: 8 AM – 2 PM ET / 5 – 11 AM PT / 12 – 6 PM GMT (weekdays) — standard usage limits
- **Off-peak hours**: outside the above window — 2x usage limits (during promotions, potentially permanent)

**Scheduling implication**: heavy automated workloads (batch evolution, ingestion pipelines, full health chains) should be scheduled for off-peak windows to maximize throughput within the same subscription tier. This applies across Claude Code, API, and all Claude surfaces.

**For this wiki**: `pipeline chain continue`, `pipeline evolve --auto`, and batch ingestion should be scheduled during off-peak hours when running as remote tasks.

## Open Questions

- How does the remote task feature handle secrets and authentication (e.g., the NotebookLM Google account login) when running on Anthropic Cloud? (Requires: Anthropic remote tasks documentation or direct testing; authentication in headless cloud environments is not covered by existing wiki pages)
- What are the cost implications of remote tasks on Anthropic Cloud? (Requires: Anthropic pricing documentation for remote task execution)
- What is the maximum frequency for scheduled tasks, and are there rate limits? (Requires: Anthropic documentation on scheduling constraints)
- Will the off-peak 2x usage become permanent or remain promotional? (Requires: Anthropic pricing updates)

## Answered Open Questions

### What happens when a scheduled task fails — is there retry logic, error reporting, or graceful degradation?

Cross-referencing `Research Pipeline Orchestration` and `Agent Orchestration Patterns`: the orchestration page documents that pipeline failure handling is a first-class concern — "How to handle pipeline failures mid-chain (e.g., one URL fails to fetch — skip or retry?)" is listed as an open design question, confirming retry logic is not yet built into the standard pipeline. The Agent Orchestration Patterns page documents OpenFleet's approach: the 12-step cycle includes a health check step that "detects stuck tasks, offline agents" and a 3-strike rule anomaly detection. Applying this to scheduling: the current Claude Code scheduling (local cron or remote tasks) does not have built-in retry logic for task-level failures. The Telegram notification integration mentioned in the Deep Analysis is the manual fallback — users observe failures via missing notifications and re-trigger manually. A more robust pattern from Agent Orchestration Patterns would be: health check after each scheduled run, alert on failure, bounded retry (max 3 attempts with backoff).

### Can scheduled tasks be chained or have dependencies (e.g., task B runs only after task A completes)?

Cross-referencing `Research Pipeline Orchestration`: the orchestration page documents three execution modes — Sequential (A → B → C, each step feeds the next), Group (A + B + C in parallel, results merged), and Tree (branch into parallel paths, merge at synthesis points). These compose to create complex workflows. However, this vision is for a Python pipeline engine, not for Claude Code's built-in scheduling mechanism. The current scheduling feature (local cron / remote tasks) does not natively support dependencies between tasks — each task fires independently at its scheduled time. Dependency chaining would need to be implemented either: (1) within the scheduled task's prompt/skill (task B's prompt checks for task A's output before proceeding), or (2) via the pipeline engine orchestrating the sequence within a single scheduled invocation. The Research Pipeline Orchestration vision of a Python orchestrator (`tools/pipeline.py`) that chains operations is the architectural answer to scheduled chaining.

### How does timezone handling work for remote tasks — is it tied to the user's configured timezone or the server's?

Cross-referencing `WSL2 Development Patterns`: the WSL2 page documents a known constraint: "Clock drift after resume — TLS errors, git timestamps wrong. WSL2 VM clock re-syncs on resume; rare in practice." For local cron on WSL2, the cron expression is evaluated against the Linux VM's system clock (which follows WSL2's timezone, typically set to UTC unless explicitly configured). The Deep Analysis on this page documents that the presenter sets "12:00 p.m. Sydney time" as a cron expression — this must be converted to the local VM's timezone for local scheduling. For remote tasks on Anthropic Cloud, the server timezone is unknown. The safe practice documented implicitly by the presenter's cron registry pattern: store the intended wall-clock time in the registry and let Claude Code generate the correct cron expression for the execution environment.

### How do the two scheduling modes map to the six Wiki Event-Driven Automation hooks? (Cross-source insight)

Cross-referencing `Wiki Event-Driven Automation`: that page explicitly resolves this: "On-schedule hooks map to Claude Code Scheduling (local cron or remote tasks)." The six hooks map to scheduling modes as follows: (1) **On new source** — triggered by file drop or CLI command, not by schedule; no scheduling mode required. (2) **On session start** — triggered by conversation start, not by schedule. (3) **On session end** — triggered by session close, not by schedule. (4) **On query** — triggered by query quality evaluation, not by schedule. (5) **On memory write** — triggered by wiki page writes, not by schedule. (6) **On schedule** (periodic lint, consolidation, retention decay) — this is the one hook that maps directly to scheduling. The on-schedule hook requires **always-on availability** because retention decay and consolidation are time-sensitive: a memory that should decay at day 30 produces incorrect confidence scores if the decay job only runs when the machine happens to be on. **Remote tasks** are therefore the correct mode for the on-schedule wiki automation hook. Local cron is acceptable for workflows (like the cybersecurity research pipeline) where missing a single daily run is tolerable.

## Relationships

- DERIVED FROM: src-claude-notebooklm-content-team
- BUILDS ON: Claude Code Skills
- ENABLES: AI-Driven Content Pipeline
- RELATES TO: NotebookLM
- ENABLES: Wiki Event-Driven Automation
- RELATES TO: LLM Knowledge Linting
- RELATES TO: Plane
- RELATES TO: OpenFleet

## Backlinks

[[src-claude-notebooklm-content-team]]
[[Claude Code Skills]]
[[AI-Driven Content Pipeline]]
[[NotebookLM]]
[[Wiki Event-Driven Automation]]
[[LLM Knowledge Linting]]
[[Plane]]
[[OpenFleet]]
[[Research Pipeline Orchestration]]
