"""Integration wrappers for external tools: Obsidian CLI and notebooklm-py.

Provides graceful-degradation wrappers that:
- Check tool availability before calling
- Timeout on hung commands (e.g., Obsidian without display)
- Fall back to direct file operations when CLI is unavailable
- Return structured results for pipeline composition

Usage from pipeline:
    from tools.integrations import obsidian, notebooklm

    # Obsidian
    result = obsidian.search("LLM wiki")
    result = obsidian.backlinks("llm-wiki-pattern.md")
    result = obsidian.is_available()

    # NotebookLM
    result = notebooklm.is_available()
    result = notebooklm.create_notebook("Research Wiki")
    result = notebooklm.add_source(notebook_id, url)
    result = notebooklm.ask(notebook_id, "question")
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from tools.common import get_project_root

# CLI timeout for commands that might hang (Obsidian without display)
CLI_TIMEOUT = 10


# ===========================================================================
# Obsidian CLI wrapper
# ===========================================================================

class ObsidianCLI:
    """Wrapper for the Obsidian CLI (v1.12.7+).

    Requires the Obsidian desktop app to be running.
    On WSL2 without a display server, commands will timeout gracefully.
    Falls back to direct file operations where possible.
    """

    def __init__(self, vault_path: Optional[Path] = None):
        self._binary = shutil.which("obsidian")
        self._vault_path = vault_path or (get_project_root() / "wiki")
        self._available: Optional[bool] = None

    def is_available(self) -> bool:
        """Check if Obsidian CLI is responsive (app running with display)."""
        if self._available is not None:
            return self._available

        if not self._binary:
            self._available = False
            return False

        try:
            result = subprocess.run(
                [self._binary, "version"],
                capture_output=True, text=True, timeout=CLI_TIMEOUT,
            )
            self._available = result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            self._available = False

        return self._available

    def _run(self, *args: str, timeout: int = CLI_TIMEOUT) -> Dict[str, Any]:
        """Run an obsidian CLI command. Returns {ok, stdout, stderr, error}."""
        if not self._binary:
            return {"ok": False, "error": "obsidian not found in PATH"}

        cmd = [self._binary] + list(args)
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
            )
            return {
                "ok": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": f"Command timed out after {timeout}s (Obsidian app not running?)"}
        except OSError as e:
            return {"ok": False, "error": str(e)}

    def search(self, query: str, limit: int = 20, fmt: str = "json") -> Dict[str, Any]:
        """Search vault content. Falls back to grep if CLI unavailable."""
        if self.is_available():
            return self._run("search", f"query={query}", f"limit={limit}", f"format={fmt}")

        # Fallback: grep wiki files
        from tools.common import find_wiki_pages
        results = []
        for page in find_wiki_pages(self._vault_path):
            text = page.read_text(encoding="utf-8", errors="ignore")
            if query.lower() in text.lower():
                results.append(str(page.relative_to(self._vault_path)))
        return {"ok": True, "stdout": json.dumps(results), "fallback": True}

    def backlinks(self, file: str, fmt: str = "json") -> Dict[str, Any]:
        """Get backlinks for a file. Falls back to manifest if CLI unavailable."""
        if self.is_available():
            return self._run("backlinks", f"file={file}", f"format={fmt}")

        # Fallback: parse manifest for incoming relationships
        manifest_path = self._vault_path / "manifest.json"
        if manifest_path.exists():
            manifest = json.loads(manifest_path.read_text())
            target_title = Path(file).stem.replace("-", " ").title()
            incoming = []
            for page in manifest.get("pages", []):
                for rel in page.get("relationships", []):
                    if target_title in rel.get("targets", []):
                        incoming.append(page["title"])
            return {"ok": True, "stdout": json.dumps(incoming), "fallback": True}

        return {"ok": False, "error": "No manifest.json and Obsidian CLI unavailable"}

    def orphans(self) -> Dict[str, Any]:
        """Find orphan pages (no incoming links)."""
        if self.is_available():
            return self._run("orphans")

        # Fallback: use lint
        from tools.lint import lint_wiki, LintConfig
        config = LintConfig(30, 30, 100, 1, 3, 2, 0.70)
        report = lint_wiki(self._vault_path, config)
        orphans = report.get("orphan_pages", [])
        return {"ok": True, "stdout": json.dumps(orphans), "fallback": True}

    def properties(self, file: str, fmt: str = "json") -> Dict[str, Any]:
        """Read file properties (frontmatter)."""
        if self.is_available():
            return self._run("properties", f"file={file}", f"format={fmt}")

        # Fallback: parse frontmatter directly
        from tools.common import parse_frontmatter
        full_path = self._vault_path / file
        if full_path.exists():
            text = full_path.read_text(encoding="utf-8")
            meta, _ = parse_frontmatter(text)
            return {"ok": True, "stdout": json.dumps(meta, default=str), "fallback": True}

        return {"ok": False, "error": f"File not found: {file}"}

    def vault_info(self) -> Dict[str, Any]:
        """Get vault information."""
        if self.is_available():
            return self._run("vault")

        # Fallback: count files
        from tools.common import find_wiki_pages
        pages = find_wiki_pages(self._vault_path)
        return {
            "ok": True,
            "stdout": json.dumps({
                "path": str(self._vault_path),
                "files": len(pages),
            }),
            "fallback": True,
        }


# ===========================================================================
# NotebookLM CLI wrapper
# ===========================================================================

class NotebookLMCLI:
    """Wrapper for notebooklm-py CLI.

    Requires:
    - notebooklm-py package installed (pip install notebooklm-py[browser])
    - Browser auth completed (notebooklm login)
    - Python 3.10+ (use project venv)
    """

    def __init__(self):
        # Try venv binary first, then system
        project_root = get_project_root()
        # Cross-platform: Linux/macOS use .venv/bin/, Windows uses .venv/Scripts/
        for venv_subdir in ["bin", "Scripts"]:
            venv_bin = project_root / ".venv" / venv_subdir / "notebooklm"
            if venv_bin.exists():
                self._binary = str(venv_bin)
                break
            # Windows may add .exe
            venv_bin_exe = venv_bin.with_suffix(".exe")
            if venv_bin_exe.exists():
                self._binary = str(venv_bin_exe)
                break
        else:
            self._binary = shutil.which("notebooklm")
        self._available: Optional[bool] = None

    def is_available(self) -> bool:
        """Check if notebooklm CLI is installed and authenticated."""
        if self._available is not None:
            return self._available

        if not self._binary:
            self._available = False
            return False

        try:
            result = subprocess.run(
                [self._binary, "--version"],
                capture_output=True, text=True, timeout=10,
            )
            self._available = result.returncode == 0
        except (subprocess.TimeoutExpired, OSError):
            self._available = False

        return self._available

    def _run(self, *args: str, timeout: int = 60) -> Dict[str, Any]:
        """Run a notebooklm CLI command."""
        if not self._binary:
            return {"ok": False, "error": "notebooklm not found (install: uv pip install notebooklm-py[browser])"}

        cmd = [self._binary] + list(args)
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
            )
            return {
                "ok": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": f"Command timed out after {timeout}s"}
        except OSError as e:
            return {"ok": False, "error": str(e)}

    def auth_status(self) -> Dict[str, Any]:
        """Check authentication status."""
        return self._run("auth", "check", "--test", timeout=15)

    def list_notebooks(self) -> Dict[str, Any]:
        """List all notebooks."""
        return self._run("list")

    def create_notebook(self, title: str) -> Dict[str, Any]:
        """Create a new notebook."""
        return self._run("create", title)

    def use_notebook(self, notebook_id: str) -> Dict[str, Any]:
        """Set active notebook."""
        return self._run("use", notebook_id)

    def add_source(self, source: str) -> Dict[str, Any]:
        """Add a source (URL, file path, or text) to active notebook."""
        return self._run("source", "add", source, timeout=120)

    def ask(self, question: str, json_output: bool = False) -> Dict[str, Any]:
        """Ask a question against the active notebook's sources."""
        args = ["ask", question]
        if json_output:
            args.append("--json")
        return self._run(*args, timeout=60)

    def generate(self, artifact_type: str, wait: bool = True) -> Dict[str, Any]:
        """Generate an artifact (audio, video, quiz, etc.)."""
        args = ["generate", artifact_type]
        if wait:
            args.append("--wait")
        return self._run(*args, timeout=300)

    def download(self, artifact_type: str, output_path: str,
                 fmt: str = None) -> Dict[str, Any]:
        """Download a generated artifact."""
        args = ["download", artifact_type, output_path]
        if fmt:
            args.extend(["--format", fmt])
        return self._run(*args, timeout=120)

    def add_research(self, query: str) -> Dict[str, Any]:
        """Start web research and auto-import sources."""
        return self._run("source", "add-research", query, timeout=180)


# ===========================================================================
# Module-level instances
# ===========================================================================

obsidian = ObsidianCLI()
notebooklm = NotebookLMCLI()


def status_report() -> Dict[str, Any]:
    """Report availability of all integrations."""
    return {
        "obsidian": {
            "installed": obsidian._binary is not None,
            "responsive": obsidian.is_available(),
            "note": "Requires Obsidian app running with display" if not obsidian.is_available() else "OK",
        },
        "notebooklm": {
            "installed": notebooklm._binary is not None,
            "responsive": notebooklm.is_available(),
            "note": "Run: notebooklm login" if notebooklm._binary and not notebooklm.is_available() else
                    "Install: uv pip install notebooklm-py[browser]" if not notebooklm._binary else "OK",
        },
    }
