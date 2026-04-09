---
title: "Gateway-Centric Routing"
type: pattern
domain: tools-and-platforms
layer: 5
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "OpenArms"
  - "OpenClaw"
  - "OpenFleet"
instances:
  - page: "OpenArms"
    context: "Single local gateway daemon (ws://127.0.0.1:18789) routes all 20+ messaging channels (Telegram, Discord, Slack, Signal, iMessage, WhatsApp, Matrix, etc.) through one control plane. Adding a new channel means configuring one gateway, not N consumer integrations."
  - page: "OpenClaw"
    context: "Multi-agent single gateway: all 10 OpenFleet agents connect through a single WebSocket gateway. Session management, heartbeat coordination, tool streaming, and agent identity are all handled centrally — agents are isolated but the routing infrastructure is shared."
  - page: "Research Pipeline Orchestration"
    context: "Wiki MCP server (tools/mcp_server.py, 15 tools) acts as a gateway: any Claude Code conversation or OpenArms agent connects once to the MCP server and gains access to all wiki operations. Tools are discoverable through the gateway without per-tool configuration."
  - page: "OpenFleet"
    context: "OpenFleet's deterministic orchestrator acts as the task routing gateway: all PO directives enter via the orchestrator, which evaluates readiness, security, budget, and agent availability before dispatching to the appropriate agent. No agent receives work except through the gateway."
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-openarms-local
    type: documentation
    file: raw/articles/openarms-readme.md
    title: "OpenArms — Project Documentation"
  - id: src-openfleet-local
    type: documentation
    file: ../openfleet/CLAUDE.md
    title: "OpenFleet — Local Project Documentation"
  - id: src-openclaw-docs
    type: documentation
    url: "https://github.com/anthropics/claude-code"
    title: "OpenClaw — Agent Framework Documentation"
tags: [gateway, routing, single-control-plane, multi-channel, orchestration, openarms, openclaw, openfleet, mcp, websocket, agent-dispatch]
---

# Gateway-Centric Routing

## Summary

Gateway-Centric Routing is the architectural pattern of channeling all traffic — messages, tasks, tool calls, or agent sessions — through a single control plane (the gateway) rather than establishing N direct point-to-point connections between producers and consumers. Changes to routing logic, authentication, security policy, or capability registry are made once in the gateway and propagate automatically to all consumers. The pattern trades the simplicity of direct connections for centralized control, observability, and uniform policy enforcement — a trade that becomes increasingly favorable as the number of consumers and channels grows.

## Pattern Description

Gateway-Centric Routing is recognizable by the gateway's role as the mandatory intermediary: no producer-to-consumer connection bypasses it. This is a structural property, not a convention — the gateway is typically the only entity with the credentials, connection state, or capability registry that enables the routing. Consumers cannot opt out of the gateway by design.

The pattern provides three structural benefits that direct-connection architectures cannot replicate:

**Single configuration point**: Adding a new channel, backend, or capability means configuring the gateway once. Without a gateway, each new integration requires updating every consumer that needs access to the new channel or capability. In OpenArms, adding a new messaging channel (e.g., a new Telegram bot configuration) requires updating the gateway's channel registry — not the 20+ other channels' handling logic. In AICP, adding a new LLM backend means updating the router's backend registry — not every tool or pipeline that uses the router.

**Uniform policy enforcement**: Security policies, rate limits, authentication, sandboxing, and budget gates are configured in the gateway and applied to all traffic. In OpenArms, the DM pairing security policy (unknown senders get a pairing code) applies to every channel without per-channel implementation. In OpenFleet, the behavioral security scan and budget gate apply to every dispatched task without per-agent implementation. Policy changes propagate by updating the gateway, not by updating N consumers.

**Observability and audit trail**: All traffic passes through one point, making comprehensive logging, metrics, and audit trails structurally easy. OpenArms provides gateway-level session management, heartbeat tracking, and event streams. OpenFleet's orchestrator provides a complete audit trail of every dispatch decision across all agents. The wiki MCP server enables observability over all wiki operations from any connected client.

The gateway's mandatory intermediary role introduces a single point of failure and a potential throughput bottleneck. The pattern's implementations address both concerns differently. OpenFleet's orchestrator fails gracefully — it is written as a stateless evaluator that reads current state and computes dispatch decisions, so it can be restarted without losing task state (state lives in Mission Control's PostgreSQL database). OpenArms runs as a persistent daemon with systemd/launchd lifecycle management and health monitoring via `openarms doctor`. The wiki MCP server is stateless per session — reconnecting restores full capability without session persistence.

The throughput bottleneck concern is addressed by bounded concurrency at the gateway. OpenFleet dispatches maximum 2 tasks per 30-second cycle — the throttle is a gateway-level enforcement, not a per-agent configuration. OpenClaw serializes execution per session — the gateway queues messages within each agent session. These are not limitations of the gateway pattern; they are deliberate throttles that the gateway's central position makes possible to enforce uniformly.

Gateway-Centric Routing is complementary to the Deterministic Shell, LLM Core pattern. The gateway is often the deterministic shell's outermost boundary — it receives requests, applies routing logic and policy, and routes to the appropriate LLM-powered backend. OpenFleet's orchestrator is simultaneously the gateway (routing PO directives to agents) and the deterministic shell (wrapping the LLM-powered agents). The patterns reinforce each other: the gateway's centralization makes the shell's policy enforcement uniform; the shell's determinism makes the gateway's routing reliable.

The pattern generalizes across abstraction levels: OpenArms's gateway routes messaging channel events; OpenFleet's orchestrator routes agent tasks; the wiki MCP server routes capability requests; AICP's router routes inference requests. Each operates at a different level of the ecosystem stack, but all implement the same structural principle: mandatory intermediary, single control plane, policy at the boundary.

## Instances

### OpenArms Gateway — Multi-Channel Messaging Control Plane

OpenArms's gateway is the ecosystem's most complete implementation of the pattern. A single daemon at `ws://127.0.0.1:18789` routes all traffic from 20+ messaging channels (WhatsApp, Telegram, Slack, Discord, Google Chat, Signal, iMessage, IRC, MS Teams, Matrix, and more) through a unified agent runtime. The gateway protocol (`src/gateway/protocol/schema.ts`) is a typed WebSocket wire protocol — all clients (CLI, macOS app, iOS/Android nodes, WebChat) connect via the same protocol, ensuring uniform behavior across device types.

The single-gateway architecture means: adding a new channel (e.g., Nostr, WeChat) requires implementing one channel plugin, not updating the iOS app, Android node, CLI, and WebChat separately. Security policy (DM pairing, sandbox mode for non-main sessions, elevated access controls) is configured once in the gateway and applies to all channels. The `openarms doctor` command audits gateway health including risky DM policies — a unified health check is possible because policy is centralized.

### OpenClaw/OpenFleet Gateway — Multi-Agent Session Management

OpenClaw's gateway serves as the routing layer for multi-agent deployments. OpenFleet deploys 10 specialized agents through a single gateway instance, each with its own identity, workspace, memory, and channel bindings. The gateway handles session serialization (one message at a time per session, queuing subsequent messages), agent isolation (no agent can access another agent's workspace), tool streaming, and compaction lifecycle.

The gateway-centric architecture enables OpenFleet's mission control observability: all agent activity is visible through one WebSocket connection. The orchestrator dispatches tasks to agents by sending messages through the gateway — there is no direct orchestrator-to-agent connection that bypasses it. This means the gateway's session model (max 2 dispatches per cycle, serialization per session) is enforced uniformly for all 10 agents without per-agent configuration.

### Wiki MCP Server — Tool Capability Gateway

The research wiki's MCP server (`tools/mcp_server.py`, 15 tools: `wiki_status`, `wiki_search`, `wiki_read_page`, `wiki_list_pages`, `wiki_post`, `wiki_fetch`, `wiki_fetch_topic`, `wiki_scan_project`, `wiki_gaps`, `wiki_crossref`, `wiki_sync`, `wiki_mirror_to_notebooklm`, `wiki_integrations`, `wiki_continue`, `wiki_evolve`) acts as a capability gateway. Any Claude Code conversation that discovers the MCP server via `.mcp.json` gains access to all 15 wiki tools through one registration. Any OpenArms agent connected via mcporter gains the same access.

The gateway's value is discoverability and uniformity: new tools added to the MCP server are automatically available to all connected clients without per-client configuration updates. The alternative — direct CLI invocations via Bash — requires each consumer to know the specific command syntax for each tool. The MCP server centralizes the tool registry.

### OpenFleet Orchestrator — Task Dispatch Gateway

OpenFleet's 9-step deterministic orchestrator operates as a task routing gateway. All work enters through one channel: PO directives on the board memory, or task creation through Mission Control API. The orchestrator processes all pending tasks on every 30-second cycle, evaluating readiness (6-axis state model), security (behavioral security scan), budget (cost gating), and agent availability before dispatching. No agent receives work directly — all dispatch goes through the orchestrator.

This gateway-centric dispatch architecture enables fleet-wide policy enforcement: when the fleet mode gate changes (paused, throttled, emergency stop), all dispatch stops immediately without per-agent configuration. When the budget gate closes, no new tasks dispatch regardless of which agent they target. The PO (Product Owner) sets direction through the orchestrator's board interface; the orchestrator propagates policy to all agents via the dispatch mechanism.

## When To Apply

Apply Gateway-Centric Routing when:

- **Multiple producers need access to multiple consumers**: the connection matrix grows as O(N×M) without a gateway and O(N+M) with one. For the research wiki's case: multiple consumers (Claude Code, OpenArms agents, CLI) accessing multiple wiki tools, one MCP gateway reduces configuration to one registration per consumer.
- **Uniform policy must be applied across all connections**: authentication, security policy, rate limiting, and sandboxing are most reliably enforced at a single control plane rather than distributed across N consumer implementations. If policy changes must propagate consistently across all connections, a gateway is the right architecture.
- **Observability of all traffic is required**: audit trails, metrics, and health monitoring become structurally simple when all traffic passes through one point. Systems where traffic bypasses the gateway create blind spots in observability.
- **Adding new channels or capabilities is a frequent operation**: the gateway's single-configuration-point benefit scales with the rate of channel/capability additions. If the integration surface is stable and rarely changes, the gateway overhead may not be justified.
- **Consumers cannot be trusted to implement policy correctly**: when policy correctness matters (security, compliance, cost control) and the consumer set is heterogeneous (different clients, agents, channels), centralizing policy in the gateway removes the requirement to verify policy implementation in each consumer.

## When Not To

Avoid Gateway-Centric Routing when:

- **The deployment has only 1-2 direct connections**: the gateway's centralization benefit appears when the connection matrix is large. For two components talking to each other, a direct connection is simpler and the gateway adds overhead without structural benefit. Apply the pattern when the connection count justifies the indirection.
- **Latency is the primary constraint**: every request passes through the gateway, adding one network hop (even if localhost) and gateway-side processing. For ultra-low-latency applications where microseconds matter, direct connections may be required. OpenArms's localhost WebSocket (`ws://127.0.0.1:18789`) minimizes this overhead, but it is non-zero.
- **The gateway becomes a centralization risk**: if the gateway is a single point of failure without adequate redundancy or restart mechanisms, it becomes a liability rather than an asset. Gateways must be deployed with health monitoring (`openarms doctor`), restart-on-failure (systemd/launchd), and graceful degradation (state persistence, session recovery).
- **Policy requirements differ fundamentally per channel**: if different channels require fundamentally incompatible policy implementations (not just different thresholds), forcing them through a single gateway may require per-channel special cases that negate the uniformity benefit. In this case, consider per-channel micro-gateways rather than a monolithic gateway.
- **Consumers need direct low-level access**: some integrations require low-level protocol access (raw WebSocket, direct socket) that a gateway abstraction layer cannot provide without significant complexity. In these cases, the gateway can serve as a control plane while allowing direct data-path connections for performance-critical traffic.

## Relationships

- DERIVED FROM: [[OpenArms]]
- DERIVED FROM: [[OpenClaw]]
- DERIVED FROM: [[OpenFleet]]
- RELATES TO: [[MCP Integration Architecture]]
- RELATES TO: [[Multi-Channel AI Agent Access]]
- RELATES TO: [[Deterministic Shell, LLM Core]]
- ENABLES: [[Multi-Channel AI Agent Access]]
- BUILDS ON: [[Infrastructure as Code Patterns]]
- RELATES TO: [[AICP]]
- FEEDS INTO: [[Research Pipeline Orchestration]]

## Backlinks

[[OpenArms]]
[[OpenClaw]]
[[OpenFleet]]
[[MCP Integration Architecture]]
[[Multi-Channel AI Agent Access]]
[[[[Deterministic Shell]]
[[LLM Core]]]]
[[Infrastructure as Code Patterns]]
[[AICP]]
[[Research Pipeline Orchestration]]
[[Deterministic Shell, LLM Core]]
[[Model: Ecosystem Architecture]]
[[Model: Local AI ($0 Target)]]
