---
title: "Plane"
type: concept
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-plane-docs
    type: documentation
    url: "https://plane.so"
    title: "Plane — Open-Source Project Management"
    ingested: 2026-04-08
  - id: src-dspd-local
    type: documentation
    file: ../devops-solution-product-development/CLAUDE.md
    title: "DSPD — Plane Fleet Integration"
    ingested: 2026-04-08
tags: [plane, project-management, sprints, kanban, rest-api, webhooks, self-hosted, docker, fleet-integration, pm-agent]
---

# Plane

## Summary

Plane is the #1 open-source project management platform (AGPL-3.0, 47.4k+ stars, 1M+ Docker pulls) positioned as an alternative to Jira, Linear, and ClickUp. It provides work items, cycles (sprints), modules (epics), 5 view layouts (Kanban, List, Gantt, Calendar, Spreadsheet), pages/wiki, intake/triage, analytics dashboards, and AI capabilities (semantic search, duplicate detection). Self-hosted via Docker Compose (12 services) or Kubernetes with Helm charts. In the ecosystem, Plane serves as the PM surface for the OpenClaw Fleet via DSPD (devops-solution-product-development), where the PM agent bridges human planning in Plane with agent execution in Mission Control. 4 projects tracked: AICP, Fleet, DSPD, NNRT.

## Key Insights

- **Full REST API**: Base URL `/api/v1/workspaces/{slug}/`, X-API-Key auth, 60 req/min rate limit, cursor-based pagination. Full CRUD on projects, work items, cycles, modules, pages, states, labels, comments, attachments, estimates, time tracking, epics.

- **Webhook system**: Events for project, issue, cycle, module, comment. Triggers HTTP POST on create/update/delete. DSPD uses HMAC-SHA256 signed webhooks for fleet integration.

- **Three-surface model in DSPD**: Plane (planning: sprints, epics, analytics, wiki) → OCMC (execution: task dispatch, heartbeat, board memory) → GitHub (code: PRs, CI, releases). PM agent bridges the first two.

- **PM agent as sole writer**: Non-negotiable architecture rule — the PM agent is the only entity that writes to Plane. Other fleet agents route through PM. This prevents race conditions and maintains audit trail coherence.

- **Bidirectional sync**: Plane → OCMC (PM reads Plane, dispatches to MC), OCMC → Plane (PM detects completion, updates Plane + adds PR link). plane_sync.py handles the logic, plane_client.py is the sole API caller.

- **Self-hosted with operational independence**: Separate Docker Compose from OCMC, separate PostgreSQL instance (plane-db on port 5433), own nginx proxy on port 8080. No shared infrastructure with Mission Control.

- **5 Fibonacci estimate scale**: 1/2/3/5/8/13 story points. Labels: `agent:<name>`, `project:<name>`, `blocked`, `spec-required`. Custom states per project (backlog → todo → dispatched → in-review → done).

- **AI capabilities**: Natural language chat, duplicate detection, semantic search across items/pages/projects. Requires OpenSearch 2.19+ and LLM provider API key.

- **Community vs Commercial**: Free tier has unlimited projects/items/cycles/users. Commercial ($7/seat/month) adds SSO, RBAC, audit logs, workflows, epics/initiatives, GitHub/GitLab/Slack integrations.

## Deep Analysis

### Fleet Integration Architecture (DSPD)

The data flow in 5 steps:
1. **PLAN**: Humans create work items in Plane (sprints, epics, stories)
2. **DISPATCH**: PM agent reads Plane via MCP tools, creates OCMC tasks
3. **EXECUTE**: Fleet agents work in OCMC
4. **CLOSE**: PM detects OCMC completion, updates Plane + adds PR link
5. **REVIEW**: Humans see burn-down in Plane, merge PRs

PM agent MCP tools: `plane_list_projects`, `plane_list_cycles`, `plane_list_issues`, `plane_create_issue`, `plane_update_issue`, `plane_add_to_cycle`, `plane_create_comment`.

DSPD development phases: Phase 0 (architecture docs) ✅, Phase 1 (Plane deployed) IaC built, Phase 2 (fleet CLI) code done, Phase 3 (MCP + webhooks) code done, Phase 4 (analytics) not started.

### Why Plane Over Alternatives

For the ecosystem, Plane's advantages:
- Self-hosted (data sovereignty, no SaaS dependency)
- Open-source (customizable, forkable)
- REST API (programmatic access for agents)
- Webhooks (real-time event integration)
- Docker Compose deployment (consistent with OCMC, LightRAG, LocalAI)
- Free unlimited tier (cost control for multi-project fleet)

## Open Questions

- Can Plane's AI capabilities (semantic search) be integrated with the research wiki for cross-system queries?
- What is the performance profile under heavy API usage from automated fleet sync (60 req/min limit)?
- Can Plane's pages/wiki feature replace or complement the research wiki for operational documentation?
- How does Plane handle sprint-level analytics when tasks are dispatched to agents (velocity tracking per agent)?

## Relationships

- USED BY: OpenFleet
- RELATES TO: AICP
- RELATES TO: OpenClaw
- RELATES TO: devops-control-plane
- ENABLES: Claude Code Scheduling

## Backlinks

[[OpenFleet]]
[[AICP]]
[[OpenClaw]]
[[devops-control-plane]]
[[Claude Code Scheduling]]
