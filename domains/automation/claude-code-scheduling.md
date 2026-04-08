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

## Open Questions

- What happens when a scheduled task fails — is there retry logic, error reporting, or graceful degradation?
- How does the remote task feature handle secrets and authentication (e.g., the NotebookLM Google account login) when running on Anthropic Cloud?
- What are the cost implications of remote tasks on Anthropic Cloud?
- Can scheduled tasks be chained or have dependencies (e.g., task B runs only after task A completes)?
- How does timezone handling work for remote tasks — is it tied to the user's configured timezone or the server's?
- What is the maximum frequency for scheduled tasks, and are there rate limits?
- Cross-source insight: Scheduling is the implementation mechanism for the "on-schedule" hook in Wiki Event-Driven Automation (periodic lint, consolidation, retention decay). How do the two scheduling modes (local cron vs. remote tasks) map to the six event hooks -- which hooks require always-on availability (remote) vs. which can tolerate machine-off gaps (local)?

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
