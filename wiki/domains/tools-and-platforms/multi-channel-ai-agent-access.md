---
title: "Multi-Channel AI Agent Access"
type: concept
domain: tools-and-platforms
status: synthesized
confidence: high
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-openarms-local
    type: documentation
    file: raw/articles/openarms-readme.md
    title: "OpenArms — Project Documentation"
    ingested: 2026-04-08
tags: [multi-channel, ai-assistant, messaging, openarms, gateway, telegram, discord, slack, signal, imessage, whatsapp, matrix, channel-routing, agent-access]
---

# Multi-Channel AI Agent Access

## Summary

Multi-channel AI agent access is the architectural pattern of making a single AI agent runtime reachable through multiple messaging platforms — Telegram, Discord, Slack, Signal, iMessage, WhatsApp, Matrix, IRC, and others — via a unified gateway that routes messages to a shared agent backend. OpenArms implements this pattern with 20+ channel integrations all routing through a single local WebSocket gateway. The key challenge is consistent agent behavior across channels with fundamentally different capability profiles, security models, and message formats. The solution is a channel-neutral runtime with per-channel adapters and a single access control layer at the gateway, not at each channel boundary.

## Key Insights

- **Gateway-centric routing is the enabling architecture**: All channels connect to a single gateway process rather than each channel having its own agent instance. This means one runtime, one configuration, one access control model, one set of tools. Without the gateway pattern, multi-channel access becomes N independent deployments, each with drift risk. The OpenArms gateway at `ws://127.0.0.1:18789` is the single control plane.

- **Channels have wildly different capability profiles**: Telegram supports rich media, inline keyboards, bot commands, file attachments, and group management. IRC is plain text with no file transfer. iMessage has end-to-end encryption but limited bot interaction surfaces. Signal has strong privacy guarantees but less API surface. A multi-channel agent must either reduce to the lowest common denominator or handle per-channel capability negotiation. OpenArms handles this through channel-specific adapters with per-channel allowlists and pairing models.

- **Security cannot be per-channel — it must be at the gateway**: Different messaging platforms have different authentication models (phone number, account, OAuth). Treating each as a trust boundary independently creates inconsistent security posture. The gateway-level DM pairing (unknown senders get a pairing code; the owner must approve) applies a consistent access control model regardless of which channel the message arrives on.

- **Session isolation enables safe multi-user access**: The `main` session (direct DMs from the owner) can run tools on the host. Non-main sessions (groups, channels, unknown contacts) are isolated in Docker sandboxes. This two-tier model — trusted sessions with full capability, untrusted sessions with sandboxed capability — enables the agent to be accessible on multiple channels without exposing host-level tools to arbitrary senders.

- **The agent must be channel-oblivious for portability**: Business logic (tool calls, planning, synthesis, responses) should not know or care which channel a message arrived from. The routing layer translates channel-specific message formats into a normalized internal event format before passing to the agent runtime. This enables the agent to be updated or replaced without touching channel adapters, and channel adapters to be added without touching agent logic.

- **20+ channels is not the goal — coverage is**: The goal is that the agent is reachable wherever the user is. Different users have different primary channels (Telegram in Europe, WhatsApp in South America, iMessage in iOS-heavy contexts, Slack in professional contexts, Discord in developer communities). A multi-channel agent reaches users without requiring them to change communication habits.

## Deep Analysis

### The Gateway Pattern

```
Channels (Telegram/Discord/Slack/WhatsApp/Signal/iMessage/Matrix/IRC/...)
               │
               ▼
┌──────────────────────────────────┐
│           Gateway                │   ← single WebSocket control plane
│      ws://127.0.0.1:18789        │   ← sessions, presence, config, cron
└──────────────┬───────────────────┘
               │
               ├─ Agent runtime (tools, reasoning, skills)
               ├─ CLI (openarms agent/send/gateway)
               ├─ WebChat UI
               ├─ macOS app (menu bar, voice wake)
               └─ iOS/Android nodes (device-local actions)
```

The gateway is the only component that touches channel-specific code. All other components (agent runtime, CLI, companion apps) communicate with the gateway via the internal WebSocket protocol. Adding a new channel means adding a new adapter to the gateway, not touching the agent logic.

### Channel Categories and Capability Tiers

| Tier | Channels | Characteristics |
|------|----------|----------------|
| Full-featured | Telegram, Discord, Slack | Rich media, bot APIs, group management, file transfer, inline UI elements |
| Privacy-first | Signal, iMessage (via BlueBubbles) | Strong encryption, limited bot API surface, owner-controlled allowlisting required |
| Enterprise | Microsoft Teams, Google Chat, Mattermost | Enterprise auth, org-scoped permissions, workspace context |
| Open/decentralized | Matrix, IRC, Nostr | Federation, open protocol, variable capability |
| Regional | WhatsApp (Baileys), WeChat (Tencent plugin), LINE, Feishu | Dominant in specific geographies; often require unofficial bridges |
| Web | WebChat | First-party channel served directly from gateway; no external dependency |

### Consistent Behavior Across Channels

The primary engineering challenge in multi-channel access is ensuring the agent behaves consistently when the same user contacts it via different channels. Failure modes include:
- Channel-specific tool availability (tools that work on Telegram may be blocked in a sandboxed Discord group)
- Context fragmentation (the agent has conversation history for Telegram but not Discord)
- Inconsistent access control (the user is trusted on iMessage but unknown on Discord)

OpenArms addresses these by:
1. **Per-session state persistence**: conversation history and session configuration are stored per session identifier, not per channel
2. **Allowlisting at the channel level**: each channel has an explicit allowlist defining which contacts receive non-sandboxed access
3. **Channel-transparent tool registry**: the agent's tool set is defined at runtime level, not per-channel; the gateway filters capabilities per session security tier

### Access Control Model

| Sender type | Default policy | Capability |
|-------------|---------------|------------|
| Owner DM (main session) | Auto-trusted | Full host tools, elevated bash |
| Allowlisted contact | Trusted after pairing | Standard tools, optionally sandboxed |
| Unknown sender | `dmPolicy=pairing` | Pairing code required; no tool access until approved |
| Group/channel | Sandbox mode | Isolated Docker container; bash/read/write/edit; no browser/canvas/cron |

The `openarms pairing approve` command is the explicit human step that promotes an unknown sender to trusted status. This prevents unsolicited contacts from accessing agent capabilities without owner knowledge.

### Remote Gateway and Distributed Access

The gateway can run on a small Linux box (Raspberry Pi, VPS, home server) and be accessed by device nodes (macOS, iOS, Android) over Tailscale or SSH tunnels. This means the AI agent is accessible across all channels without requiring a phone or laptop to be online — the gateway persists independently.

Device-local actions (camera, screen recording, system.run) stay on the device node. The gateway handles channel connections and agent execution. This separation keeps sensitive device capabilities local while centralizing routing and agent logic.

### Plugin SDK and Channel Extension

New channel integrations are developed as npm-distributed plugins via the OpenArms plugin SDK. The SDK enforces hard architectural boundaries: plugins access channel behavior only through `src/plugin-sdk/channel-contract.ts`, never through core `src/channels/**` internals. This plugin isolation means community-developed channel adapters cannot destabilize the core gateway or access data from other channels.

## Open Questions

- How should conversation context be shared or isolated when the same user contacts the agent via two channels in parallel?
- What is the canonical approach for per-channel capability negotiation when a tool is available in some sessions but not others?
- Should multi-channel access be designed for a single user (personal AI assistant) or for team-scale deployment (multiple owners, role-based access)?
- How does the agent communicate its capability limitations when asked to perform an action unavailable in the current channel context?
- What is the right architecture for bridging OpenArms channel access with OpenFleet agent tasking — can a Telegram message trigger a fleet task dispatch?

## Relationships

- ENABLES: OpenArms
- RELATES TO: MCP Integration Architecture
- RELATES TO: Claude Code Skills
- RELATES TO: OpenFleet
- RELATES TO: AICP
- BUILDS ON: Agent Orchestration Patterns
- RELATES TO: Research Pipeline Orchestration

## Backlinks

[[OpenArms]]
[[MCP Integration Architecture]]
[[Claude Code Skills]]
[[OpenFleet]]
[[AICP]]
[[Agent Orchestration Patterns]]
[[Research Pipeline Orchestration]]
