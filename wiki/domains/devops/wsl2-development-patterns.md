---
title: "WSL2 Development Patterns"
type: concept
layer: 2
maturity: growing
domain: devops
status: synthesized
confidence: medium
created: 2026-04-08
updated: 2026-04-10
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

> [!warning] The fundamental WSL2 constraint: two filesystems
>
> | Filesystem | Location | Characteristics |
> |-----------|----------|----------------|
> | **Linux (ext4)** | Inside WSL2 VM | Full POSIX, fast, inotify works |
> | **Windows (NTFS)** | /mnt/c/ | Interop shims, slow, inotify unreliable |
>
> This is why the wiki lives on ext4 and is synced to Windows, not the other way around. The performance cost of copy-on-change sync is lower than running all tooling against /mnt/c.

**Obsidian sync requires an explicit bridge.** Obsidian reads Windows paths; wiki lives in WSL2. `tools/sync.py` copies wiki/ to /mnt/c/.../vault/. Without the bridge, Obsidian can't see WSL2 edits.

**Two daemons, clean separation.** `tools/watcher.py` polls Linux-side wiki/ (reliable inotify). `tools/sync.py` separately bridges to Windows. The watcher detects changes; the sync daemon pushes them across the boundary.

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

- Can WSL2's newer mirrored networking mode (WSL 2.0+) simplify the localhost-to-Windows service access pattern? (Requires: external research on WSL 2.0 mirrored networking specifics and its inotify/socket behavior changes; not covered in existing wiki pages)
- Should tools/sync.py support Syncthing as a backend for true bidirectional sync without --reverse? (Requires: external research on Syncthing API integration and conflict resolution semantics; not covered in existing wiki pages)
- Is there a way to reliably use inotify across WSL2 for paths on the Linux filesystem that are accessed from Windows? (Requires: external research on WSL2 kernel updates to inotify across the interop boundary; the current wiki consensus is that inotify works on the Linux-side ext4 paths and the workaround — keeping wiki on Linux fs, syncing to Windows — remains the recommended approach)

### Answered Open Questions

**Q: What is the optimal polling interval for tools/watcher.py on WSL2 to balance responsiveness and CPU overhead?**

Cross-referencing `Infrastructure as Code Patterns` and `Research Pipeline Orchestration`: The CLAUDE.md documentation lists `--interval 5` (5 seconds) as the example custom poll interval for the watcher and `--interval 10` (10 seconds) for the sync daemon. The `Research Pipeline Orchestration` page establishes that the watcher's purpose is to detect wiki edits and trigger the post-chain (validate → manifest → lint → index). The post-chain itself takes several seconds to run, so a polling interval shorter than the post-chain duration would queue multiple triggers unnecessarily. The `Infrastructure as Code Patterns` page notes that the watcher and sync daemons have distinct responsibilities and run independently. Combining these: a 5-second polling interval for `watcher.py` is the documented default, balancing sub-10-second responsiveness (adequate for an edit-observe loop) against CPU overhead from inotify polling on the ext4 Linux filesystem. For machines under memory pressure, 10 seconds is acceptable — the post-chain always processes the latest wiki state regardless of how many edits occurred between polls.

**Q: What happens to systemd user services when the WSL2 instance is terminated and restarted — do they auto-restart?**

Cross-referencing `Infrastructure as Code Patterns`: The `Infrastructure as Code Patterns` page documents the service deployment pattern: "Writing the service file to ~/.config/systemd/user/ and running `systemctl enable` is reproducible infrastructure deployment." The `systemctl enable` command configures a service to start automatically at login — in systemd terminology, this is `WantedBy=default.target` for user services. When a WSL2 instance is shut down (`wsl --shutdown`) and restarted, systemd initializes the user session fresh, which activates all `enabled` user services. The WSL2 page itself states these services get "restart on failure, start on login" lifecycle management. The practical answer: yes, enabled systemd user services (`wiki-sync.service`, `wiki-watcher.service`) auto-restart when the WSL2 instance starts, because WSL2 restart = new systemd user session = all `enabled` services are activated. No manual `systemctl --user start` is required after a WSL2 reboot, provided systemd is enabled in `/etc/wsl.conf`.

## Relationships

- RELATES TO: [[Research Pipeline Orchestration]]
- RELATES TO: [[MCP Integration Architecture]]
- RELATES TO: [[devops-control-plane]]
- ENABLES: [[Infrastructure as Code Patterns]]
- RELATES TO: [[Obsidian CLI]]
- RELATES TO: [[Wiki Ingestion Pipeline]]

## Backlinks

[[Research Pipeline Orchestration]]
[[MCP Integration Architecture]]
[[devops-control-plane]]
[[Infrastructure as Code Patterns]]
[[Obsidian CLI]]
[[Wiki Ingestion Pipeline]]
[[Decision: Obsidian vs NotebookLM as Knowledge Interface]]
[[Decision: Polling vs Event-Driven Change Detection]]
[[Four-Project Ecosystem]]
