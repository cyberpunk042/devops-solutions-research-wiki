# devops-control-plane — README.md

Source: /home/jfortin/devops-control-plane/README.md
Ingested: 2026-04-08
Type: documentation

---

# Solution Control Plane

> **A solution management platform for software projects.**

Point it at any project — mono-repo or single-stack — and get full visibility,
management, and evolution tools through a unified CLI, web dashboard, and
interactive terminal.

---

## What It Does

The control plane gives you **one place** to see, manage, and evolve your
software solution. It replaces scattered scripts, manual environment setup,
fragmented dashboards, and tool-specific knowledge with a unified platform
that understands your project.

### 🔍 Project Visibility & Observability

See your entire solution at a glance. The platform detects what technologies
are in your project, reports their status, and surfaces what needs attention.

- **Technology detection** — auto-scans for stacks (Python, Node, Go, Rust, Docker, Terraform, and 14 more)
- **Project status** — unified health view across all modules and environments
- **Audit trail** — append-only ledger of every operation performed

### 🔌 Integrations

First-class support for the tools your project depends on, with more added
over time.

- **Git** — status, commit, push, pull, branch management
- **GitHub** — secrets, environments, pull requests, Actions workflows, Releases
- **Docker** — container management (adapter ready)
- **Kubernetes** — orchestration (adapter ready)
- **CI/CD** — workflow triggering, status monitoring
- **Extensible** — pluggable adapter protocol for adding any tool

### 🔐 Vaults

Two vault systems for two different concerns:

- **Secret / Variable Vault** — AES-256-GCM encrypted `.env` files, environment-specific configs, key management, GitHub Secrets sync, auto-lock on inactivity
- **Content Vault** — per-file encryption for sensitive media and documents, binary envelope format, inline content preview

### � Project & Environment Management

Manage your project's lifecycle: its environments, its configuration, its
documentation, and its backups.

- **Environment management** — create, switch, compare `.env` configurations across dev/staging/production
- **Backup system** — create, restore, export, and archive project state
- **Documentation sites** — build and deploy with 6 SSG builders (Docusaurus, MkDocs, Hugo, Sphinx, Raw, Custom)
- **Content management** — file browser, media optimization (image compression, video transcoding), GitHub Release uploads

### � Solution Evolution & Augmentation

The platform doesn't just show you what's there — it helps you evolve your
solution by detecting what technologies you use and offering paths forward.

- **Stack detection** — 20 technology definitions with detection rules
- **Integration guidance** — identify what your project can integrate with
- **Solution analysis** — understand your project's structure, dependencies, and gaps

### 🧭 Setup Wizard

Guided setup with steps for configuring your project, its environments, its
secrets, and its integrations. Reduces onboarding from hours to minutes.

### � Debugging

Built-in debugging tools for diagnosing issues with your project, its
integrations, and its environment.

### 🔗 Resource Links

Quick access to your project's remote interfaces and resources — repositories,
dashboards, CI pipelines, deployed environments.

### 📊 Multi-Module & Multi-Stack

Handles mono-repos with multiple services and modules, multiple technology
stacks within a single solution, and complex project structures. Every
module gets detected, tracked, and managed.

---

## Three Interfaces, One Platform

Every capability is accessible from all three interfaces — they all drive the
same core:

| Interface | Usage | Best For |
|---|---|---|
| **`./manage.sh`** | Interactive terminal menu | Daily operations, guided workflows |
| **CLI** (`python -m src.main`) | Direct commands with flags | Scripting, automation, CI |
| **Web Dashboard** | Flask SPA at `localhost:8000` | Visual management, content browsing, setup wizard |

---

## Quick Start

```bash
# Clone and install
git clone https://github.com/cyberpunk042/devops-control-plane.git
cd devops-control-plane
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Discover your project
./manage.sh detect

# Check status
./manage.sh status

# Launch the web dashboard
./manage.sh web
```

See [docs/QUICKSTART.md](docs/QUICKSTART.md) for the full setup guide.

---

## CLI Commands

| Group | Commands |
|-------|----------|
| **Core** | `status`, `detect`, `config check`, `health`, `run`, `web` |
| **Vault** | `lock`, `unlock`, `status`, `export`, `detect`, `keys`, `templates`, `create`, `add-key`, `update-key`, `delete-key`, `activate` |
| **Content** | `encrypt`, `decrypt`, `optimize`, `upload`, `restore`, `list`, `preview`, `status` |
| **Pages** | `build`, `deploy`, `list`, `status`, `clean` |
| **Git** | `status`, `log`, `commit`, `pull`, `push`, `gh pulls`, `gh runs`, `gh dispatch`, `clone`, `branch` |
| **Backup** | `create`, `list`, `preview`, `delete`, `folders` |
| **Secrets** | `status`, `auto-detect`, `generate`, `set`, `remove`, `list`, `envs list`, `envs create`, `envs cleanup` |

Global flags: `--verbose`, `--quiet`, `--config <path>`, `--json`

---

## Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](docs/QUICKSTART.md) | Setup guide |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System architecture and file layout |
| [DESIGN.md](docs/DESIGN.md) | Design philosophy and principles |
| [WEB_ADMIN.md](docs/WEB_ADMIN.md) | Web dashboard guide |
| [PAGES.md](docs/PAGES.md) | Pages builder system |
| [VAULT.md](docs/VAULT.md) | Vault & secrets encryption |
| [CONTENT.md](docs/CONTENT.md) | Content management |
| [STACKS.md](docs/STACKS.md) | Stack definitions |
| [ADAPTERS.md](docs/ADAPTERS.md) | Adapter protocol |
| [DEVELOPMENT.md](docs/DEVELOPMENT.md) | Developer setup |

---

## Development

```bash
pip install -e ".[dev]"
make check    # lint + types + tests
make test     # pytest only
```

See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) for the full development guide.

---

## License

MIT
