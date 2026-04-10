---
title: "OpenArms"
type: concept
layer: 2
maturity: growing
domain: tools-and-platforms
status: synthesized
confidence: authoritative
created: 2026-04-08
updated: 2026-04-10
sources:
  - id: src-openarms-local
    type: documentation
    file: raw/articles/openarms-readme.md
    title: "OpenArms — Project Documentation"
    ingested: 2026-04-08
tags: [openarms, ai-assistant, messaging, plugin-sdk, multi-channel, gateway, sandbox, media-pipeline]
---

# OpenArms

## Summary

OpenArms is a local-first personal AI assistant platform that runs a single Gateway daemon on your own devices and routes messages from 20+ messaging channels (Telegram, Discord, Slack, Signal, iMessage, WhatsApp, Matrix, and more) to a unified AI agent runtime. It provides a TypeScript plugin SDK, Docker-based session sandboxing, a media pipeline for images/audio/video, voice wake and talk mode, companion apps for macOS/iOS/Android, scheduled automation, and a skill registry (ClawHub). It is part of the user's 4-project devops ecosystem as the personal AI assistant layer.

## Key Insights

> [!info] Gateway as the single control plane
> All channels, sessions, tools, and events route through a local WebSocket gateway (`ws://127.0.0.1:18789`). The gateway runs as a daemon. All apps connect through it — none bypass it.

- **20+ messaging channel integrations**: WhatsApp (Baileys), Telegram (grammY), Slack (Bolt), Discord (discord.js), Google Chat, Signal (signal-cli), BlueBubbles/iMessage, IRC, Microsoft Teams, Matrix, Feishu, LINE, Mattermost, Nextcloud Talk, Nostr, Synology Chat, WeChat (via Tencent plugin), WebChat, and more. Each channel has its own allowlist and pairing model.

- **Plugin SDK with hard architecture boundaries**: Core stays lean. Optional capabilities ship as npm-distributed plugins. The `openarms/plugin-sdk/*` surface is the only public cross-package contract. Bundled plugins live in the workspace plugin tree and must not deep-import core `src/**`. Versioned, backwards-compatible contract evolution is required for third-party plugin compatibility.

- **Sandbox execution model**: Main sessions (direct DMs with the owner) run tools on the host. Non-main sessions (groups, channels) can be isolated in per-session Docker sandboxes via `agents.defaults.sandbox.mode: "non-main"`. Sandbox allows bash/process/read/write/edit/sessions tools; blocks browser/canvas/nodes/cron/gateway.

> [!warning] DM pairing security
> Unknown senders receive a pairing code by default (`dmPolicy="pairing"`). Gateway does not process their message until `openarms pairing approve`. Open DMs require explicit `dmPolicy="open"` opt-in. `openarms doctor` surfaces risky DM policies.

- **Voice and device nodes**: macOS/iOS offer Voice Wake (wake words) and Push-to-Talk overlays. Android node provides continuous voice mode, camera, screen recording, SMS/notifications/contacts/calendar/location commands. All device actions route via `node.invoke` over the Gateway WebSocket.

- **Session model with agent-to-agent coordination**: `main` session for direct chats; group isolation per channel. The `sessions_list`, `sessions_history`, and `sessions_send` tools allow agents to coordinate work across sessions without leaving the gateway. Reply-back ping-pong and announce steps (`REPLY_SKIP`, `ANNOUNCE_SKIP`) control cross-session communication patterns.

- **MCP via mcporter bridge**: MCP integration is deliberately kept out of core runtime. The `mcporter` bridge (`github.com/steipete/mcporter`) provides MCP server connectivity without restarting the gateway, keeping core lean and reducing MCP churn impact on stability.

- **ClawHub skill registry**: A minimal community skill registry at `clawhub.ai`. New skills should publish to ClawHub first, not be added to core. Core skills require a strong product or security justification. Skills are markdown instruction files injected into the agent workspace (`~/.openarms/workspace/skills/<skill>/SKILL.md`).

- **Remote gateway support**: The gateway runs cleanly on a small Linux box. macOS/iOS/Android clients connect over Tailscale Serve/Funnel (tailnet-only or public HTTPS) or SSH tunnels. Device-local actions (camera, screen recording, `system.run`) stay on the device node; the gateway runs channel connections and exec tools.

- **TypeScript orchestration-first design**: Chosen for hackability, fast iteration, and wide familiarity. OpenArms is primarily an orchestration system (prompts, tools, protocols, integrations) rather than a heavy compute layer. Node 24 recommended, Node 22.16+ required.

## Deep Analysis

### Architecture: Gateway-Centric Routing

```
Channels (Telegram/Discord/Slack/WhatsApp/Signal/iMessage/Matrix/...)
               │
               ▼
┌───────────────────────────────┐
│            Gateway            │   ← WebSocket control plane
│       ws://127.0.0.1:18789    │   ← sessions, presence, config, cron, webhooks
└──────────────┬────────────────┘
               │
               ├─ Pi agent runtime (RPC + tool streaming)
               ├─ CLI (openarms agent/send/gateway/onboard/doctor)
               ├─ WebChat UI (served from gateway)
               ├─ macOS app (menu bar + voice wake + PTT)
               └─ iOS / Android nodes (device-local actions)
```

The gateway protocol (`src/gateway/protocol/schema.ts`) is a typed WebSocket control-plane and node wire protocol. Protocol changes are contract changes — additive evolution is preferred; incompatible changes require explicit versioning and client follow-through.

### Plugin Architecture and Boundaries

Four hard boundaries govern plugin development:

1. **Plugin/channel boundary**: `src/channels/**` is core implementation detail. Plugin authors access it only through `src/plugin-sdk/channel-contract.ts` and `src/plugin-sdk/core.ts`.
2. **Provider/model boundary**: Core owns the generic inference loop. Providers own provider-specific behavior via typed registration hooks. Vendor tools and config belong in the owning plugin, not in core `tools.*`.
3. **Bundled plugin contract**: Manifest metadata, runtime registration, public SDK exports, and contract tests must stay aligned. No hidden bypass of declared plugin interfaces.
4. **Extension SDK self-import rule**: Inside an extension package, internal imports go through a local barrel (`./api.ts` or `./runtime-api.ts`), not `openarms/plugin-sdk/<self>`.

### Session and Security Model

Per-session toggles persist via `sessions.patch` WebSocket method: `thinkingLevel`, `verboseLevel`, `model`, `sendPolicy`, `groupActivation`, and per-session elevated access (`/elevated on|off`). Elevated bash is separate from macOS TCC permissions (camera, screen recording, notifications) — those are enforced via `node.invoke` + TCC permission status.

### Ecosystem Position

OpenArms is the personal AI assistant layer of the 4-project ecosystem:
- It provides the multi-channel interface and conversational surface
- Skills installed in `~/.openarms/workspace/skills/` can include Claude Code skills from the research wiki
- The OpenClaw architecture (long-running named agent sessions with Telegram-based status) is the inspiration for the user's multi-agent setup in Claude Code
- mcporter enables MCP tool exposure, including the research-wiki MCP server, to OpenArms agents

### Evolution Roadmap

Current priorities: security/safe defaults, bug fixes, setup reliability. Next: all major model providers, major messaging channel improvements, better computer-use/agent harness, companion apps (macOS/iOS/Android/Windows/Linux). Notable deferred items: first-class MCP runtime in core (mcporter preferred), agent-hierarchy frameworks, heavy orchestration layers that duplicate existing agent/tool infrastructure.

## Open Questions

- Is there a canonical approach for syncing OpenArms workspace skills with the AICP skills directory? (Requires: direct inspection of AICP's agent-tooling.yaml and OpenArms workspace structure; the AICP page documents 78 skills and 18 referenced in fleet's agent-tooling.yaml but does not document a sync mechanism with OpenArms's `~/.openarms/workspace/skills/` path)

### Answered Open Questions

**Q: How does OpenArms session memory integrate with the devops-solutions-research-wiki LightRAG knowledge graph?**

Cross-referencing `LightRAG` and `OpenFleet`: LightRAG runs as a REST API server at `localhost:9621` and exposes an MCP server (via `daniel-lightrag-mcp`, 22 tools). OpenArms supports MCP tool exposure via the `mcporter` bridge. The integration path is: (1) LightRAG server runs with the wiki's knowledge graph loaded (via `kb_sync.py` parsing the wiki's `## Relationships` sections), (2) mcporter bridges the LightRAG MCP server to the OpenArms gateway, (3) OpenArms agents can query the LightRAG graph in-session via the exposed MCP tools. The `LightRAG` page confirms the wiki's relationship format (`- VERB: Target Name`) is directly compatible with `kb_sync.py`'s regex parser, so the research wiki's own relationship structure is LightRAG-ingestible. OpenArms session memory (per-session conversation history) and the LightRAG knowledge graph are complementary — session memory is ephemeral per-conversation context; LightRAG provides persistent cross-session knowledge retrieval.

**Q: Can wiki MCP tools be exposed to OpenArms agents via mcporter for in-chat knowledge queries?**

Cross-referencing `OpenArms` and `AICP`: the OpenArms page documents that `mcporter` (`github.com/steipete/mcporter`) "provides MCP server connectivity without restarting the gateway, keeping core lean." AICP documents 11 MCP tools (including `kb search`) exposed as an MCP server for IDE clients and fleet agents. This wiki runs its own MCP server (`tools/mcp_server.py`) with 15 tools (`wiki_status`, `wiki_search`, `wiki_read_page`, etc.) registered in `.mcp.json`. The path to in-chat knowledge queries: connect the research-wiki MCP server to OpenArms via mcporter. The architecture is: `wiki MCP server → mcporter bridge → OpenArms gateway → agent session`. No new protocol is required; mcporter is the existing bridge for exactly this pattern. The feasibility is confirmed by AICP's documented pattern of exposing its own MCP tools to fleet agents.

**Q: What is the recommended skill structure for bridging OpenArms ↔ OpenFleet agent coordination?**

Cross-referencing `OpenArms` and `OpenFleet`: OpenArms skills are SKILL.md markdown files installed in `~/.openarms/workspace/skills/<skill>/SKILL.md`. OpenFleet agents have SOUL.md (identity) and HEARTBEAT.md (periodic checklist) files. The coordination surface is documented: OpenFleet exposes the Mission Control API (port 8000) and IRC channels (#fleet, #alerts, #reviews). An OpenArms bridge skill would contain: (1) instructions for invoking Mission Control API endpoints (task creation, status query), (2) IRC messaging patterns for the fleet channels, (3) the fleet's task state model (6-axis state, dispatch rules). The OpenArms `sessions_send` mechanism enables cross-session coordination internally, but for fleet dispatch, the skill would make direct HTTP calls to Mission Control API or messages to the fleet's IRC #fleet channel. The skill structure mirrors other OpenArms integration skills: one SKILL.md file per integration target, containing the relevant API surface and protocol notes.

**Q: How does the `sessions_send` cross-session mechanism compare to OpenFleet's agent messaging patterns?**

Cross-referencing `OpenFleet`: OpenArms's `sessions_send` is a synchronous within-gateway cross-session message: one agent session sends a message to another session over the same WebSocket gateway. This is primarily used for agent-to-agent coordination within a single OpenArms deployment. OpenFleet's messaging patterns are asynchronous and infrastructure-level: agents communicate via IRC channels (#fleet, #alerts, #reviews) on miniircd (port 6667), and the orchestrator dispatches tasks via the Mission Control API on a 30-second cycle. The key difference: `sessions_send` is ephemeral and session-scoped (no persistent task queue), while OpenFleet's IRC+orchestrator pattern is persistent (tasks survive agent restarts) and auditable (all channel messages are logged). For triggering fleet tasks from OpenArms, the correct approach is the Mission Control API (HTTP POST), not `sessions_send` — `sessions_send` is for coordinating within the OpenArms gateway, not for crossing into the OpenFleet boundary.

## Relationships

- RELATES TO: [[AICP]]
- RELATES TO: [[OpenFleet]]
- RELATES TO: [[devops-control-plane]]
- BUILDS ON: [[Claude Code Skills]]
- RELATES TO: [[MCP Integration Architecture]]
- ENABLES: [[Multi-Channel AI Agent Access]]
- RELATES TO: [[Claude Code]]
- FEEDS INTO: [[Research Pipeline Orchestration]]

## Backlinks

[[AICP]]
[[OpenFleet]]
[[devops-control-plane]]
[[Claude Code Skills]]
[[MCP Integration Architecture]]
[[Multi-Channel AI Agent Access]]
[[Claude Code]]
[[Research Pipeline Orchestration]]
[[Ecosystem Integration Interfaces]]
[[Four-Project Ecosystem]]
[[Gateway-Centric Routing]]
