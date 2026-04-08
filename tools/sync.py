"""Cross-platform sync daemon for the research wiki.

Keeps the wiki directory synced between WSL and Windows so that:
- Obsidian on Windows can open the vault directly
- WSL projects (openfleet, AICP) can read wiki at ~/... without /mnt/c fs bugs

Supports one-shot sync and watch mode (daemon).

Usage:
    python -m tools.sync                          # One-shot sync
    python -m tools.sync --watch                  # Watch for changes, auto-sync
    python -m tools.sync --watch --interval 10    # Custom interval (seconds)
    python -m tools.sync --reverse                # Sync from target back to source
    python -m tools.sync --status                 # Show sync config and last sync
    python -m tools.sync --target /path/to/vault  # Override target path

Environment:
    WIKI_SYNC_TARGET    Override default sync target path
    WIN_USER            Windows username (for WSL default target)
"""

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from tools.common import get_project_root


# ---------------------------------------------------------------------------
# Platform detection
# ---------------------------------------------------------------------------

def is_wsl() -> bool:
    try:
        return "microsoft" in Path("/proc/version").read_text().lower()
    except (FileNotFoundError, OSError):
        return False


def is_windows() -> bool:
    return platform.system() == "Windows"


def get_win_user() -> Optional[str]:
    """Get Windows username from WSL."""
    if not is_wsl():
        return None
    try:
        result = subprocess.run(
            ["cmd.exe", "/c", "echo", "%USERNAME%"],
            capture_output=True, text=True, timeout=5,
        )
        return result.stdout.strip().strip("\r\n")
    except (subprocess.TimeoutExpired, OSError, FileNotFoundError):
        return None


# ---------------------------------------------------------------------------
# Sync config
# ---------------------------------------------------------------------------

def get_sync_config(project_root: Path, target_override: str = None) -> Dict[str, Any]:
    """Determine sync source, target, and method based on platform."""
    # WIKI_SYNC_MODE: "vault" syncs wiki/ only, "repo" syncs entire project
    sync_mode = os.environ.get("WIKI_SYNC_MODE", "repo")
    source_dir = project_root if sync_mode == "repo" else project_root / "wiki"

    config = {
        "source": str(source_dir),
        "sync_mode": sync_mode,
        "target": None,
        "method": None,  # rsync, robocopy, or shutil
        "platform": platform.system(),
        "is_wsl": is_wsl(),
    }

    # Target from override, env var, or platform default
    if target_override:
        config["target"] = target_override
    elif os.environ.get("WIKI_SYNC_TARGET"):
        config["target"] = os.environ["WIKI_SYNC_TARGET"]
    elif is_wsl():
        win_user = get_win_user()
        if win_user:
            config["target"] = f"/mnt/c/Users/{win_user}/Documents/research-wiki-vault"
        else:
            config["target"] = None
    elif is_windows():
        # On Windows, sync to WSL home if accessible
        config["target"] = None  # User must set WIKI_SYNC_TARGET
    else:
        config["target"] = None

    # Select sync method
    if shutil.which("rsync"):
        config["method"] = "rsync"
    elif is_windows() and shutil.which("robocopy"):
        config["method"] = "robocopy"
    else:
        config["method"] = "shutil"

    return config


# ---------------------------------------------------------------------------
# Sync operations
# ---------------------------------------------------------------------------

def sync_rsync(source: str, target: str, reverse: bool = False,
               delete: bool = False, verbose: bool = True) -> Dict[str, Any]:
    """Sync using rsync. Uses --update (newer wins) by default, not --delete."""
    if reverse:
        source, target = target, source

    # Ensure trailing slash for rsync directory semantics
    src = source.rstrip("/") + "/"
    dst = target.rstrip("/") + "/"

    cmd = ["rsync", "-a", "--update"]
    if verbose:
        cmd.append("-v")
    if delete:
        cmd.append("--delete")
    cmd.extend([
        "--exclude", ".gitkeep",
        "--exclude", ".obsidian/workspace*.json",
        "--exclude", ".obsidian/workspace",
        "--exclude", ".venv/",
        "--exclude", "__pycache__/",
        "--exclude", "*.pyc",
        "--exclude", ".sync-state.json",
        "--exclude", ".watcher-state.json",
        "--exclude", ".evolve-queue/*.prompt.md",
        src, dst,
    ])

    os.makedirs(target, exist_ok=True)

    result = subprocess.run(cmd, capture_output=True, text=True)
    changed_files = [l for l in result.stdout.splitlines()
                     if l.strip() and not l.startswith("sending")
                     and not l.startswith("sent") and not l.startswith("total")]

    return {
        "ok": result.returncode == 0,
        "method": "rsync",
        "files_changed": len(changed_files),
        "direction": f"{'target → source' if reverse else 'source → target'}",
        "source": source,
        "target": target,
        "error": result.stderr.strip() if result.returncode != 0 else None,
    }


def sync_robocopy(source: str, target: str, reverse: bool = False,
                  verbose: bool = True) -> Dict[str, Any]:
    """Sync using robocopy (Windows)."""
    if reverse:
        source, target = target, source

    cmd = [
        "robocopy", source, target,
        "/MIR",  # Mirror (equivalent to rsync --delete)
        "/XF", ".gitkeep",  # Exclude
        "/XD", ".obsidian\\workspace",
    ]
    if not verbose:
        cmd.append("/NFL")  # No file list
        cmd.append("/NDL")  # No directory list

    result = subprocess.run(cmd, capture_output=True, text=True)
    # robocopy returns 0-7 for success, 8+ for errors
    ok = result.returncode < 8

    return {
        "ok": ok,
        "method": "robocopy",
        "direction": f"{'target → source' if reverse else 'source → target'}",
        "source": source,
        "target": target,
        "error": result.stderr.strip() if not ok else None,
    }


def sync_shutil(source: str, target: str, reverse: bool = False,
                verbose: bool = True) -> Dict[str, Any]:
    """Sync using Python shutil (fallback, no delete support)."""
    if reverse:
        source, target = target, source

    src_path = Path(source)
    dst_path = Path(target)
    dst_path.mkdir(parents=True, exist_ok=True)

    copied = 0
    for src_file in src_path.rglob("*"):
        if src_file.is_dir():
            continue
        if src_file.name == ".gitkeep":
            continue

        rel = src_file.relative_to(src_path)
        dst_file = dst_path / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        # Only copy if source is newer or target doesn't exist
        if not dst_file.exists() or src_file.stat().st_mtime > dst_file.stat().st_mtime:
            shutil.copy2(src_file, dst_file)
            copied += 1
            if verbose:
                print(f"  {rel}")

    return {
        "ok": True,
        "method": "shutil",
        "files_changed": copied,
        "direction": f"{'target → source' if reverse else 'source → target'}",
        "source": source,
        "target": target,
        "note": "shutil fallback: does not delete removed files",
    }


def run_sync(config: Dict[str, Any], reverse: bool = False,
             verbose: bool = True) -> Dict[str, Any]:
    """Run sync using the configured method."""
    source = config["source"]
    target = config["target"]
    method = config["method"]

    if not target:
        return {"ok": False, "error": "No sync target configured. Set WIKI_SYNC_TARGET or use --target."}

    if method == "rsync":
        return sync_rsync(source, target, reverse=reverse, verbose=verbose)
    elif method == "robocopy":
        return sync_robocopy(source, target, reverse=reverse, verbose=verbose)
    else:
        return sync_shutil(source, target, reverse=reverse, verbose=verbose)


# ---------------------------------------------------------------------------
# Directory fingerprint (for change detection)
# ---------------------------------------------------------------------------

def dir_fingerprint(path: str) -> str:
    """Quick hash of directory state (file paths + mtimes)."""
    entries = []
    for f in sorted(Path(path).rglob("*.md")):
        entries.append(f"{f.relative_to(path)}:{f.stat().st_mtime}")
    return hashlib.md5("\n".join(entries).encode()).hexdigest()


# ---------------------------------------------------------------------------
# Watch mode (daemon)
# ---------------------------------------------------------------------------

def watch_sync(config: Dict[str, Any], interval: int = 15,
               verbose: bool = True):
    """Watch for changes and auto-sync. Runs until interrupted."""
    source = config["source"]
    target = config["target"]

    if not target:
        print("ERROR: No sync target configured. Set WIKI_SYNC_TARGET or use --target.")
        sys.exit(1)

    print(f"Watching for changes (interval: {interval}s)")
    print(f"  Source: {source}")
    print(f"  Target: {target}")
    print(f"  Method: {config['method']}")
    print("  Press Ctrl+C to stop.\n")

    last_source_fp = None
    last_target_fp = None

    # Initial sync: reverse first (pick up Windows changes), then forward
    if Path(target).exists():
        ts = datetime.now().strftime("%H:%M:%S")
        print(f"  [{ts}] Initial reverse sync (target → source)...")
        result = run_sync(config, reverse=True, verbose=False)
        if result["ok"]:
            print(f"  [{ts}] Reverse synced ({result.get('files_changed', '?')} files)")
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [{ts}] Initial forward sync (source → target)...")
    result = run_sync(config, reverse=False, verbose=False)
    if result["ok"]:
        print(f"  [{ts}] Forward synced ({result.get('files_changed', '?')} files)")
    save_sync_state(Path(source).parent, result)

    last_source_fp = dir_fingerprint(source)
    last_target_fp = dir_fingerprint(target) if Path(target).exists() else None

    try:
        while True:
            source_fp = dir_fingerprint(source)
            target_fp = dir_fingerprint(target) if Path(target).exists() else None

            synced = False

            # Source changed → sync to target
            if source_fp != last_source_fp:
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"  [{ts}] Source changed — syncing to target...")
                result = run_sync(config, reverse=False, verbose=False)
                if result["ok"]:
                    print(f"  [{ts}] Synced ({result.get('files_changed', '?')} files)")
                else:
                    print(f"  [{ts}] Sync failed: {result.get('error', 'unknown')}")
                synced = True
                last_source_fp = source_fp

            # Target changed → sync back to source (bidirectional)
            if target_fp and target_fp != last_target_fp and not synced:
                ts = datetime.now().strftime("%H:%M:%S")
                print(f"  [{ts}] Target changed — syncing back to source...")
                result = run_sync(config, reverse=True, verbose=False)
                if result["ok"]:
                    print(f"  [{ts}] Reverse synced ({result.get('files_changed', '?')} files)")
                else:
                    print(f"  [{ts}] Reverse sync failed: {result.get('error', 'unknown')}")
                last_target_fp = target_fp
            elif target_fp:
                last_target_fp = target_fp

            time.sleep(interval)

    except KeyboardInterrupt:
        print("\nWatch stopped.")


# ---------------------------------------------------------------------------
# Sync state tracking
# ---------------------------------------------------------------------------

STATE_FILE = ".sync-state.json"


def save_sync_state(project_root: Path, result: Dict[str, Any]):
    """Save last sync result to state file."""
    state_path = project_root / STATE_FILE
    state = {
        "last_sync": datetime.now().isoformat(),
        "result": result,
    }
    state_path.write_text(json.dumps(state, indent=2, default=str))


def load_sync_state(project_root: Path) -> Optional[Dict[str, Any]]:
    """Load last sync state."""
    state_path = project_root / STATE_FILE
    if state_path.exists():
        return json.loads(state_path.read_text())
    return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Cross-platform sync daemon for the research wiki",
    )
    parser.add_argument("--watch", "-w", action="store_true",
                        help="Watch for changes and auto-sync")
    parser.add_argument("--interval", "-i", type=int, default=15,
                        help="Watch interval in seconds (default: 15)")
    parser.add_argument("--reverse", "-r", action="store_true",
                        help="Sync from target back to source")
    parser.add_argument("--target", "-t",
                        help="Override sync target path")
    parser.add_argument("--status", "-s", action="store_true",
                        help="Show sync configuration and last sync")
    parser.add_argument("--json", action="store_true",
                        help="JSON output")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="Minimal output")

    args = parser.parse_args()
    root = get_project_root()
    config = get_sync_config(root, target_override=args.target)
    verbose = not args.quiet

    if args.status:
        state = load_sync_state(root)
        if args.json:
            print(json.dumps({"config": config, "state": state}, indent=2, default=str))
        else:
            print(f"Platform:   {config['platform']}" +
                  (" (WSL)" if config["is_wsl"] else ""))
            print(f"Source:     {config['source']}")
            print(f"Target:     {config['target'] or 'NOT SET'}")
            print(f"Method:     {config['method']}")
            if state:
                print(f"Last sync:  {state['last_sync']}")
                r = state.get("result", {})
                print(f"  Status:   {'OK' if r.get('ok') else 'FAILED'}")
                print(f"  Files:    {r.get('files_changed', '?')}")
            else:
                print("Last sync:  never")
        sys.exit(0)

    if args.watch:
        watch_sync(config, interval=args.interval, verbose=verbose)
        sys.exit(0)

    # One-shot sync
    if verbose:
        direction = "target → source" if args.reverse else "source → target"
        print(f"Syncing ({direction})...")
        print(f"  Source: {config['source']}")
        print(f"  Target: {config['target'] or 'NOT SET'}")
        print(f"  Method: {config['method']}")

    result = run_sync(config, reverse=args.reverse, verbose=verbose)
    save_sync_state(root, result)

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    elif verbose:
        if result["ok"]:
            print(f"\nSync OK ({result.get('files_changed', '?')} files changed)")
        else:
            print(f"\nSync FAILED: {result.get('error', 'unknown')}")

    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()
