---
title: "Decision: Polling vs Event-Driven Change Detection"
type: decision
domain: devops
layer: 6
status: synthesized
confidence: high
maturity: growing
derived_from:
  - "WSL2 Development Patterns"
  - "Wiki Event-Driven Automation"
  - "Research Pipeline Orchestration"
reversibility: easy
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
  - id: src-user-directive-ecosystem
    type: notes
    file: raw/notes/2026-04-08-user-directive-ecosystem-connections.md
    title: "User Directive — Ecosystem Connections & Automation Vision"
tags: [polling, inotify, fswatch, wsl2, change-detection, watcher, daemon, event-driven, filesystem, devops]
---

# Decision: Polling vs Event-Driven Change Detection

## Summary

On WSL2, polling is the correct change detection strategy for the wiki watcher daemon. The inotify kernel subsystem is unreliable across the /mnt/c boundary between WSL2's Linux filesystem and the Windows NTFS mount, making event-driven approaches fragile for the common case where source files originate on the Windows side. Polling the Linux-side wiki/ path at 5–10 second intervals is reliable, low-overhead, and sufficient for a personal wiki's edit-observe feedback loop. Event-driven (inotify or fswatch) becomes appropriate only when the wiki is deployed on native Linux or macOS where filesystem event delivery is reliable.

## Decision

**Use polling for change detection on WSL2. Use event-driven (inotify) on native Linux. Use fswatch on macOS.**

Concretely:

- **WSL2 (current environment)**: `tools/watcher.py --watch --interval 5` polls the Linux-side `wiki/` path every 5 seconds. This is the deployed default. The wiki lives on the ext4 WSL2 filesystem (`~/devops-solutions-research-wiki/wiki/`), not on `/mnt/c`. Polling on the ext4 path is reliable and fast — inotify works on ext4, but the polling implementation avoids complexity and handles edge cases (stale handles, WSL2 suspend/resume) more gracefully.

- **Native Linux**: `tools/watcher.py` can be extended with `inotifywait` or Python's `watchdog` library using the inotify backend for event-driven detection. Zero polling overhead, instant response to file changes. Appropriate when the wiki is deployed on a Linux server or in a CI environment.

- **macOS**: Use `fswatch` or `watchdog` with the kqueue/FSEvents backend. The `tools/sync.py --watch` daemon uses rsync polling today; a future upgrade to `watchdog` with FSEvents would reduce CPU overhead on Mac.

- **The /mnt/c boundary rule**: Never use inotify or fswatch to watch paths under `/mnt/c`. The WSL2 Development Patterns page documents this constraint explicitly: "inotify does not work reliably on /mnt/c — this matters for any daemon that watches files in Windows-accessible paths." Keep watchers on Linux-side paths and use the sync daemon for the Windows bridge.

## Alternatives

### Alternative 1: inotify on /mnt/c (Event-Driven Cross-Filesystem)

Use inotify to watch `/mnt/c` paths directly, eliminating the need for the two-daemon architecture (watcher + sync). **Rejected** because inotify is unreliable on the WSL2 /mnt/c boundary. The WSL2 Development Patterns page documents this as a first-class WSL2 constraint: "inotify does not work reliably on /mnt/c" — and the wiki's own architecture decision (keeping wiki on Linux filesystem, syncing to Windows) exists precisely because of this constraint. Attempting to watch the Windows-side vault path from the watcher daemon produces intermittent missed events, false positives, and stale file handles that are difficult to debug and unpredictable in production.

### Alternative 2: fswatch (macOS-Only Tool)

Use fswatch for cross-platform change detection. **Rejected as primary mechanism** because fswatch is macOS-specific (kqueue-based). It does not run on WSL2 Linux. For macOS deployments the tools could be extended to use fswatch, but it cannot be the default for the current WSL2 environment. Additionally, fswatch shares the same /mnt/c unreliability as inotify when run from macOS with cross-filesystem mounts.

### Alternative 3: Git Hooks (post-commit only)

Use git post-commit hooks to trigger the post-chain after every wiki commit. **Rejected as the sole mechanism** because git hooks only fire on git operations, not on raw file changes. The wiki's watcher is intended to detect mid-edit saves, partial writes, and operational tool outputs that may not be immediately committed. The `tools/watcher.py` pattern correctly uses filesystem-level detection rather than git-level detection. Git hooks are a useful supplementary trigger (e.g., for CI/CD validation on push) but cannot replace watcher-level change detection for the interactive edit-observe loop.

### Alternative 4: Kernel-Level inotify on Linux Filesystem with WSL2

Use inotify directly on the Linux-side ext4 paths (not /mnt/c). This would be event-driven without the /mnt/c reliability problem. **Not rejected — this is the upgrade path.** The current polling implementation is correct and adequate for the personal wiki use case. A future upgrade to `watchdog` with the inotify backend for Linux paths would reduce polling overhead from 5-second intervals to instant event delivery. The migration path is low-risk: swap the polling loop in `tools/watcher.py` for a `watchdog.observers.Observer` using the `InotifyObserver` backend. No change to the daemon deployment, no change to the sync architecture.

## Rationale

The WSL2 Development Patterns page documents the fundamental constraint driving this decision: "The fundamental WSL2 constraint: two filesystems. The Linux filesystem (ext4, inside the WSL2 VM) has full POSIX semantics. The Windows filesystem mounted at /mnt/c is NTFS with WSL interop shims. inotify does not work reliably on /mnt/c."

The decision to keep the wiki on the Linux filesystem (rather than on `/mnt/c` where Obsidian could read it directly) was made for performance and reliability reasons. This decision is upstream of the change detection decision: once the wiki lives on Linux ext4, the watcher operates on reliable POSIX filesystem semantics. Polling on ext4 at 5-second intervals is straightforward and correct.

The 5-second polling interval is well-calibrated for the personal wiki use case. The post-chain (validate → manifest → wikilinks → lint) takes several seconds to complete. A polling interval shorter than the post-chain duration would queue redundant triggers unnecessarily. The WSL2 Development Patterns page confirms: "a 5-second polling interval for watcher.py is the documented default, balancing sub-10-second responsiveness against CPU overhead." For the interactive edit-observe loop, sub-10-second latency is adequate — the human curator does not need instant feedback after saving a page.

The two-daemon architecture (watcher + sync) that results from this decision has a structural benefit: Obsidian always sees validated, post-processed wiki state rather than mid-edit intermediates. The watcher triggers the post-chain (validate, manifest, wikilinks, lint), then the sync daemon transfers the resulting clean state to the Windows-side Obsidian vault. Collapsing these into a single event-driven daemon would require careful ordering guarantees to prevent Obsidian from seeing a partially-validated state.

The Wiki Event-Driven Automation page maps the six wiki event hooks to existing Claude Code primitives. The watcher daemon is the "on new source" hook in production form — the foundation of the event-driven automation architecture. Polling is the implementation strategy; event-driven is the conceptual model. They are compatible: polling detects the event; the subsequent post-chain and skill triggers are event-driven responses.

## Reversibility

**Easy to reverse.** Switching from polling to inotify-based event detection requires only a modification to `tools/watcher.py`: replace the polling loop with a `watchdog.observers.Observer` using the `InotifyObserver` backend. The daemon deployment (systemd user service), the post-chain trigger, and the sync architecture are all unchanged. On WSL2, the constraint is permanent (inotify on /mnt/c will not be fixed by a Python library change), so "reversibility" applies specifically to: (a) upgrading from polling to inotify for Linux-side path watching, or (b) deploying on a different OS where the constraints differ.

The current polling implementation can run indefinitely without degradation — there is no forcing function to migrate. The upgrade to inotify becomes attractive primarily if CPU overhead from polling becomes measurable on constrained hardware, or if sub-second responsiveness becomes a requirement for an automated pipeline where latency matters.

## Dependencies

**Downstream effects of this decision:**

- **tools/watcher.py architecture**: The polling loop is the active implementation. Any change to event-driven detection requires updating this file and testing the failure modes (what happens on WSL2 resume, on /mnt/c path disappearing, on wiki path unmount).
- **wiki-watcher.service**: The systemd user service runs `tools/watcher.py --watch` as a daemon. The polling interval is configured via `--interval`. No changes needed when upgrading to inotify — the service invocation is identical.
- **Two-daemon dependency**: The decision to use polling reinforces the two-daemon architecture (watcher + sync). If inotify is adopted on native Linux, the watcher and sync daemons could potentially be merged — but the separation of concerns (change detection vs. file transfer) has value independent of polling vs. event-driven.
- **CI/CD pipelines**: If the wiki is ever deployed in a cloud CI context (GitHub Actions, etc.), the change detection mechanism must be adapted — polling is fine for CI batch runs, inotify is not available in most cloud CI environments. The post-chain (`python3 -m tools.pipeline post`) can be invoked directly without a watcher daemon in CI contexts.
- **Cross-platform tooling**: `tools/setup.py --services wiki-watcher` deploys the watcher as a systemd service. On macOS, a launchd plist would be the equivalent. The cross-platform Python tooling in the ecosystem handles OS detection, so the service deployment path is already abstracted.

## Relationships

- DERIVED FROM: [[WSL2 Development Patterns]]
- DERIVED FROM: [[Wiki Event-Driven Automation]]
- DERIVED FROM: [[Research Pipeline Orchestration]]
- RELATES TO: [[Infrastructure as Code Patterns]]
- RELATES TO: [[devops-control-plane]]
- ENABLES: [[Wiki Event-Driven Automation]]
- FEEDS INTO: [[Research Pipeline Orchestration]]
- RELATES TO: [[Obsidian Knowledge Vault]]

## Backlinks

[[WSL2 Development Patterns]]
[[Wiki Event-Driven Automation]]
[[Research Pipeline Orchestration]]
[[Infrastructure as Code Patterns]]
[[devops-control-plane]]
[[Obsidian Knowledge Vault]]
[[Model: Automation and Pipelines]]
