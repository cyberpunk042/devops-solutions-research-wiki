---
title: "WSL2 Development Patterns"
type: concept
domain: devops
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-08
sources:
  - id: src-user-directive-ecosystem
    type: notes
    file: raw/notes/2026-04-08-user-directive-ecosystem-connections.md
    title: "User Directive — Ecosystem Connections & Automation Vision"
    ingested: 2026-04-08
  - id: src-devops-control-plane-local
    type: documentation
    file: ../devops-control-plane/README.md
    title: "devops-control-plane — Local Project Documentation"
    ingested: 2026-04-08
tags: [devops, wsl2, windows-subsystem-linux, obsidian-sync, systemd, daemon, cross-platform, inotify, sync, filesystem]
---

# WSL2 Development Patterns

## Summary

WSL2 (Windows Subsystem for Linux 2) enables running a full Linux development ecosystem alongside Windows tools, but the bridged architecture introduces constraints that standard Linux devops documentation does not cover. The four-project ecosystem runs entirely in WSL2, using Windows-side tools (Obsidian, Claude Desktop) for UI access and Linux-side tooling (Python, systemd, git) for computation. Key patterns: sync daemons for WSL-to-Windows file bridging, systemd user services for daemon lifecycle, /mnt/c filesystem limitations for inotify, and cross-platform Python setup scripts that abstract OS differences. Understanding where WSL2 differs from native Linux is prerequisite knowledge for operating and extending the ecosystem.

## Key Insights

- **The fundamental WSL2 constraint: two filesystems**: The Linux filesystem (ext4, inside the WSL2 VM) has full POSIX semantics. The Windows filesystem mounted at /mnt/c is NTFS with WSL interop shims. inotify does not work reliably on /mnt/c — this matters for any daemon that watches files in Windows-accessible paths.

- **Obsidian sync requires an explicit bridge**: Obsidian runs on Windows and reads from a Windows filesystem path. The wiki lives in WSL2 (~/devops-solutions-research-wiki/wiki/). A sync daemon (tools/sync.py) bridges them by copying wiki/ to a Windows path (/mnt/c/Users/.../Obsidian vault). Without this bridge, Obsidian cannot see wiki edits made in WSL2.

- **Polling vs inotify for the watcher daemon**: tools/watcher.py monitors wiki/ for changes. In native Linux, inotify is the correct mechanism — instant, event-driven, efficient. In WSL2, inotify on /mnt/c paths is unreliable. The watcher therefore polls the Linux-side wiki/ path (reliable inotify) and the sync daemon separately bridges to Windows. Two daemons, clean separation of concerns.

- **Systemd user services on WSL2**: Modern WSL2 (WSL 1.4+, systemd enabled) supports systemd user services (systemctl --user). The watcher and sync daemons are deployed as systemd user services via tools/setup.py --services. This gives them proper lifecycle management (restart on failure, start on login) without requiring root or manual process management.

- **Cross-platform Python tooling abstracts the gap**: tools/setup.py, tools/sync.py, and tools/watcher.py are designed to run on Linux (WSL2), macOS, and Windows with consistent behavior. On WSL2, the setup script auto-detects the Windows username (WIN_USER env var or heuristic) and constructs the correct /mnt/c sync target path.

- **The /mnt/c performance trade-off**: File operations on /mnt/c are significantly slower than on the Linux filesystem due to the NTFS translation layer. This is why the wiki lives on the Linux filesystem and is synced to Windows, rather than living on /mnt/c directly. The performance cost of a copy-on-change sync is lower than the performance cost of running all tooling against an /mnt/c path.

- **Bidirectional sync requires conflict resolution**: tools/sync.py supports --reverse for syncing Windows changes back to WSL2, used when Obsidian edits are made directly (e.g., adding notes via Obsidian interface). The --update flag passes rsync's --update option to resolve conflicts by keeping the newer file. True bidirectional merge (like Syncthing) is outside scope — the workflow assumes WSL2 is the source of truth for wiki writes.

- **Service deployment is reproducible IaC**: Running python -m tools.setup --services wiki-sync deploys the sync daemon as a systemd user service, writing the service file to ~/.config/systemd/user/ and enabling it. This is the ecosystem's IaC pattern applied to daemon lifecycle management — no manual systemctl commands documented anywhere in CLAUDE.md.

## Deep Analysis

### WSL2 Architecture for the Ecosystem

```
Windows (Host)
├── Obsidian Desktop App
│   └── reads from C:\Users\<user>\<obsidian-vault>\
├── Claude Desktop
│   └── connects to MCP servers over localhost
└── /mnt/c/ (NTFS via WSL interop, slow, no reliable inotify)

WSL2 VM (Linux)
├── ~/devops-solutions-research-wiki/    ← ext4, fast, inotify works
│   ├── wiki/                           ← source of truth
│   ├── tools/sync.py                   ← sync daemon
│   └── tools/watcher.py                ← change detector
├── ~/openfleet/                        ← fleet project
├── ~/devops-expert-local-ai/           ← AICP project
└── Daemons (systemd user services)
    ├── wiki-sync.service               → copies wiki/ → /mnt/c/.../vault/
    └── wiki-watcher.service            → detects changes, runs post-chain
```

### Daemon Architecture: Two Services, One Problem

The wiki uses two daemons with distinct responsibilities:

| Daemon | Tool | Watches | Action |
|--------|------|---------|--------|
| wiki-watcher | tools/watcher.py | wiki/ (Linux fs) | Detects edits, runs post-chain |
| wiki-sync | tools/sync.py | wiki/ (after post-chain) | rsync to Windows /mnt/c path |

The watcher triggers the post-chain (validate, manifest, wikilinks, lint). The sync daemon transfers the resulting clean state to Windows. Separating them means Obsidian always sees validated, post-processed wiki state — not mid-edit intermediates.

### Known WSL2 Constraints and Workarounds

| Constraint | Impact | Workaround |
|-----------|--------|-----------|
| inotify unreliable on /mnt/c | Can't watch Windows paths | Keep wiki on Linux fs, sync to Windows |
| NTFS performance on /mnt/c | Slow tooling if wiki on Windows path | Wiki on Linux fs, sync is one-way copy |
| No systemd by default (older WSL) | Daemons need manual start | Enable systemd in /etc/wsl.conf; use setup --services |
| Networking is NAT by default | Services on Linux not reachable from Windows by hostname | Use localhost (127.0.0.1) which WSL2 mirrors |
| Windows line endings (CRLF) | Git and Python tools see dirty files | .gitattributes: text=auto eol=lf enforces LF on checkout |
| Clock drift after resume | TLS errors, git timestamps wrong | WSL2 VM clock re-syncs on resume; rare in practice |

### Enabling systemd in WSL2

For tools/setup.py --services to work, systemd must be enabled. Add to /etc/wsl.conf:

```ini
[boot]
systemd=true
```

Then restart WSL (`wsl --shutdown` from PowerShell). This is a one-time setup step that unlocks proper daemon lifecycle management.

### Cross-Platform Considerations

The ecosystem's Python tooling is designed to degrade gracefully when not on WSL2:
- On macOS: sync.py uses rsync to a local path; no Windows interop needed
- On native Linux: inotify is fully reliable; watcher.py can use event mode
- On WSL2: polling mode for watcher, /mnt/c path detection for sync

The WIKI_SYNC_TARGET environment variable overrides the auto-detected Windows path, providing explicit control for non-standard setups.

## Open Questions

- What is the optimal polling interval for tools/watcher.py on WSL2 to balance responsiveness and CPU overhead?
- Can WSL2's newer mirrored networking mode (WSL 2.0+) simplify the localhost-to-Windows service access pattern?
- Should tools/sync.py support Syncthing as a backend for true bidirectional sync without --reverse?
- Is there a way to reliably use inotify across WSL2 for paths on the Linux filesystem that are accessed from Windows?
- What happens to systemd user services when the WSL2 instance is terminated and restarted — do they auto-restart?

## Relationships

- RELATES TO: Research Pipeline Orchestration
- RELATES TO: MCP Integration Architecture
- RELATES TO: devops-control-plane
- ENABLES: Infrastructure as Code Patterns
- RELATES TO: Obsidian CLI
- RELATES TO: Wiki Ingestion Pipeline

## Backlinks

[[Research Pipeline Orchestration]]
[[MCP Integration Architecture]]
[[devops-control-plane]]
[[Infrastructure as Code Patterns]]
[[Obsidian CLI]]
[[Wiki Ingestion Pipeline]]
[[Four-Project Ecosystem]]
