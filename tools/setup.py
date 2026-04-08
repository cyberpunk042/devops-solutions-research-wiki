"""Cross-platform setup for the DevOps Solutions Research Wiki.

Replaces bash scripts for environments where bash isn't available (Windows).
Works on Linux, macOS, and Windows.

Usage:
    python3 -m tools.setup                    # Full setup
    python3 -m tools.setup --deps             # Install dependencies only
    python3 -m tools.setup --check            # Check environment only
    python3 -m tools.setup --obsidian-config  # Configure Obsidian vault
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

from tools.common import get_project_root


def is_windows() -> bool:
    return platform.system() == "Windows"


def is_wsl() -> bool:
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except (FileNotFoundError, OSError):
        return False


def log_info(msg: str):
    print(f"\033[0;32m[INFO]\033[0m {msg}")


def log_warn(msg: str):
    print(f"\033[0;33m[WARN]\033[0m {msg}")


def log_error(msg: str):
    print(f"\033[0;31m[ERROR]\033[0m {msg}", file=sys.stderr)


def venv_python(project_root: Path) -> Path:
    """Get the venv Python path (cross-platform)."""
    if is_windows():
        return project_root / ".venv" / "Scripts" / "python.exe"
    return project_root / ".venv" / "bin" / "python"


def venv_bin(project_root: Path, name: str) -> Path:
    """Get a venv binary path (cross-platform)."""
    if is_windows():
        p = project_root / ".venv" / "Scripts" / f"{name}.exe"
        if p.exists():
            return p
        return project_root / ".venv" / "Scripts" / name
    return project_root / ".venv" / "bin" / name


# ---------------------------------------------------------------------------
# Check environment
# ---------------------------------------------------------------------------

def check_environment(project_root: Path) -> dict:
    """Check what's available in the environment."""
    report = {
        "platform": platform.system(),
        "python_version": platform.python_version(),
        "is_wsl": is_wsl(),
        "uv": shutil.which("uv") is not None,
        "git": shutil.which("git") is not None,
        "obsidian_cli": shutil.which("obsidian") is not None,
        "venv_exists": (project_root / ".venv").exists(),
        "venv_python": venv_python(project_root).exists(),
    }

    # Check notebooklm in venv
    nlm_path = venv_bin(project_root, "notebooklm")
    report["notebooklm"] = nlm_path.exists()

    return report


def print_check(project_root: Path):
    """Print environment check report."""
    report = check_environment(project_root)

    log_info(f"Platform:       {report['platform']}" +
             (" (WSL)" if report["is_wsl"] else ""))
    log_info(f"Python:         {report['python_version']}")

    for key in ["uv", "git", "obsidian_cli", "venv_exists", "venv_python", "notebooklm"]:
        status = "YES" if report[key] else "NO"
        color = "\033[0;32m" if report[key] else "\033[0;33m"
        print(f"  {color}{key:20s}{status}\033[0m")

    if not report["uv"]:
        log_warn("uv not found. Install: https://docs.astral.sh/uv/getting-started/installation/")
    if not report["venv_exists"]:
        log_warn("No .venv — run: python -m tools.setup --deps")


# ---------------------------------------------------------------------------
# Install dependencies
# ---------------------------------------------------------------------------

def install_deps(project_root: Path):
    """Install dependencies via uv into .venv."""
    uv = shutil.which("uv")
    if not uv:
        log_error("uv not found. Install: https://docs.astral.sh/uv/getting-started/installation/")
        sys.exit(1)

    venv_dir = project_root / ".venv"

    # Create venv if needed
    if not venv_dir.exists():
        log_info("Creating Python 3.11 venv...")
        subprocess.run([uv, "venv", "--python", "3.11", str(venv_dir)], check=True)
    else:
        log_info(f"Venv exists at {venv_dir}")

    # Install packages
    log_info("Installing Python packages...")
    req_file = project_root / "requirements.txt"
    subprocess.run([uv, "pip", "install", "-r", str(req_file)], check=True)

    # Install Playwright chromium
    playwright = venv_bin(project_root, "playwright")
    if playwright.exists():
        log_info("Installing Playwright chromium...")
        subprocess.run([str(playwright), "install", "chromium"],
                       capture_output=True)
    else:
        log_warn("Playwright not found in venv — notebooklm login may not work")

    # Verify
    log_info("Verifying installations...")
    py = venv_python(project_root)
    subprocess.run([str(py), "-c", "import yaml; print(f'  PyYAML {yaml.__version__}')"])
    subprocess.run([str(py), "-c", "import youtube_transcript_api; print('  youtube-transcript-api OK')"])

    nlm = venv_bin(project_root, "notebooklm")
    if nlm.exists():
        result = subprocess.run([str(nlm), "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            log_info(f"notebooklm-py: {result.stdout.strip()}")
        else:
            log_warn("notebooklm-py installed but not responding")

    # Integration check
    log_info("Integration status:")
    subprocess.run([str(py), "-m", "tools.pipeline", "integrations"])

    log_info("Done.")


# ---------------------------------------------------------------------------
# Configure Obsidian vault
# ---------------------------------------------------------------------------

def configure_obsidian(project_root: Path):
    """Set up Obsidian vault configuration in wiki/.obsidian/."""
    obsidian_dir = project_root / "wiki" / ".obsidian"
    obsidian_dir.mkdir(parents=True, exist_ok=True)

    # app.json — basic settings
    app_config = {
        "livePreview": True,
        "readableLineLength": True,
        "showLineNumber": True,
        "strictLineBreaks": False,
    }
    (obsidian_dir / "app.json").write_text(json.dumps(app_config, indent=2))

    # core-plugins.json — enable graph, backlinks, search
    core_plugins = [
        "file-explorer", "global-search", "graph", "backlink",
        "tag-pane", "page-preview", "templates", "command-palette",
        "markdown-importer", "outline",
    ]
    (obsidian_dir / "core-plugins.json").write_text(json.dumps(core_plugins, indent=2))

    # graph.json — color groups per domain
    graph_config = {
        "collapse-filter": False,
        "search": "",
        "showTags": False,
        "showAttachments": False,
        "hideUnresolved": False,
        "showOrphans": True,
        "collapse-color-groups": False,
        "colorGroups": [
            {"query": "path:domains/ai-agents", "color": {"a": 1, "rgb": 14701138}},
            {"query": "path:domains/knowledge-systems", "color": {"a": 1, "rgb": 5431378}},
            {"query": "path:domains/automation", "color": {"a": 1, "rgb": 16098048}},
            {"query": "path:domains/tools-and-platforms", "color": {"a": 1, "rgb": 8564738}},
            {"query": "path:domains/devops", "color": {"a": 1, "rgb": 16750848}},
            {"query": "path:sources", "color": {"a": 1, "rgb": 11184810}},
            {"query": "path:comparisons", "color": {"a": 1, "rgb": 16777045}},
        ],
        "collapse-display": False,
        "lineSizeMultiplier": 1,
        "nodeSizeMultiplier": 1,
        "textFadeMultiplier": 0,
        "collapse-forces": False,
        "centerStrength": 0.518713248970312,
        "repelStrength": 10,
        "linkStrength": 1,
        "linkDistance": 250,
    }
    (obsidian_dir / "graph.json").write_text(json.dumps(graph_config, indent=2))

    log_info(f"Obsidian vault configured at {obsidian_dir}")

    # Run manifest + obsidian wikilinks
    py = venv_python(project_root)
    if py.exists():
        log_info("Regenerating manifest and wikilinks...")
        subprocess.run([str(py), "-m", "tools.pipeline", "post"])
    else:
        log_warn("Venv not found — run tools.setup --deps first, then tools.pipeline post")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Cross-platform setup for the research wiki")
    parser.add_argument("--deps", action="store_true", help="Install dependencies only")
    parser.add_argument("--check", action="store_true", help="Check environment only")
    parser.add_argument("--obsidian-config", action="store_true", help="Configure Obsidian vault")
    args = parser.parse_args()

    root = get_project_root()

    if args.check:
        print_check(root)
    elif args.deps:
        install_deps(root)
    elif args.obsidian_config:
        configure_obsidian(root)
    else:
        # Full setup
        log_info("=== Research Wiki Setup ===")
        print_check(root)
        print()
        install_deps(root)
        print()
        configure_obsidian(root)
        log_info("=== Setup complete ===")


if __name__ == "__main__":
    main()
