# DOCS: docs/tui/PATTERNS_TUI_Design.md
"""
Manager supervisor logic for the TUI.

The manager monitors running agents and detects drift:
- Tracks which files agents modify
- Checks if docs are updated when code changes
- Presents warnings to user (doesn't auto-fix)

Also provides interactive Claude session via PTY.
"""

from dataclasses import dataclass
from typing import Callable, List, Optional, Awaitable
from pathlib import Path
import asyncio
import json
import os
import pty
import re


from .state import AgentHandle


@dataclass
class DriftWarning:
    """Warning when agent changes code without updating docs."""

    agent_id: str
    agent_symbol: str
    message: str
    suggestion: str
    files_changed: List[str]
    docs_updated: List[str]


class ClaudePTY:
    """Interactive Claude session using PTY."""

    def __init__(
        self,
        target_dir: Path,
        on_output: Callable[[str], Awaitable[None]],
        system_prompt: str = "",
    ):
        self.target_dir = target_dir
        self.on_output = on_output
        self.system_prompt = system_prompt
        self._master_fd: Optional[int] = None
        self._slave_fd: Optional[int] = None
        self._process: Optional[asyncio.subprocess.Process] = None
        self._reader_task: Optional[asyncio.Task] = None
        self._running = False
        self._buffer = ""

    async def start(self) -> bool:
        """Start the Claude PTY session."""
        try:
            # Create pseudo-terminal
            self._master_fd, self._slave_fd = pty.openpty()

            # Build command
            cmd = ["claude"]
            if self.system_prompt:
                cmd.extend(["--append-system-prompt", self.system_prompt])

            # Spawn Claude with PTY
            self._process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=self._slave_fd,
                stdout=self._slave_fd,
                stderr=self._slave_fd,
                cwd=self.target_dir,
            )

            # Close slave in parent
            os.close(self._slave_fd)
            self._slave_fd = None

            self._running = True

            # Start reader task
            self._reader_task = asyncio.create_task(self._read_output())

            return True

        except Exception as e:
            await self.on_output(f"[Error starting Claude: {e}]")
            return False

    async def _read_output(self) -> None:
        """Read output from Claude PTY."""
        loop = asyncio.get_event_loop()

        while self._running and self._master_fd is not None:
            try:
                # Read from master fd (non-blocking via executor)
                data = await loop.run_in_executor(
                    None,
                    lambda: os.read(self._master_fd, 4096)
                )

                if data:
                    text = data.decode('utf-8', errors='replace')
                    # Filter out control sequences and clean up
                    clean_text = self._clean_output(text)
                    if clean_text:
                        await self.on_output(clean_text)
                else:
                    await asyncio.sleep(0.1)

            except OSError:
                break
            except Exception as e:
                await self.on_output(f"[Read error: {e}]")
                break

    def _clean_output(self, text: str) -> str:
        """Clean ANSI codes and control chars from output."""
        # Remove ANSI escape sequences
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        text = ansi_escape.sub('', text)
        # Remove other control chars except newline
        text = ''.join(c for c in text if c == '\n' or (ord(c) >= 32 and ord(c) < 127))
        return text.strip()

    async def send(self, message: str) -> None:
        """Send a message to Claude."""
        if self._master_fd is not None and self._running:
            try:
                # Write to master fd
                os.write(self._master_fd, (message + "\n").encode())
            except OSError as e:
                await self.on_output(f"[Send error: {e}]")

    async def stop(self) -> None:
        """Stop the Claude session."""
        self._running = False

        if self._reader_task:
            self._reader_task.cancel()
            try:
                await self._reader_task
            except asyncio.CancelledError:
                pass

        if self._master_fd is not None:
            try:
                os.close(self._master_fd)
            except OSError:
                pass
            self._master_fd = None

        if self._process:
            try:
                self._process.terminate()
                await asyncio.wait_for(self._process.wait(), timeout=2.0)
            except asyncio.TimeoutError:
                self._process.kill()
            except Exception:
                pass

    @property
    def is_running(self) -> bool:
        if not self._running:
            return False
        if self._process and self._process.returncode is not None:
            self._running = False
            return False
        return self._master_fd is not None


class ManagerSupervisor:
    """
    Supervisor that monitors agents and catches drift.

    Pattern: Observer
    - Monitors agent output streams
    - Detects concerning patterns (code change without doc update)
    - Reports to TUI (doesn't auto-fix)
    """

    def __init__(self, on_warning: Callable[[DriftWarning], Awaitable[None]]) -> None:
        """
        Initialize supervisor.

        Args:
            on_warning: Async callback to report warnings to TUI
        """
        self.on_warning = on_warning
        self._change_patterns = re.compile(
            r'(?:Created|Modified|Edited|Updated|Wrote|Deleted)\s+[`"]?([^`"\n]+)[`"]?',
            re.IGNORECASE
        )
        self._file_patterns = re.compile(
            r'(?:Created|Modified|Edited|Updated|Wrote|Deleted)\s+[`"]?([^`"\n]+\.py)[`"]?',
            re.IGNORECASE
        )
        self._doc_patterns = re.compile(
            r'(?:Created|Modified|Edited|Updated|Wrote)\s+[`"]?([^`"\n]+\.md)[`"]?',
            re.IGNORECASE
        )

    @staticmethod
    def _normalize_path(raw_path: str) -> str:
        """Normalize extracted paths for comparison."""
        cleaned = raw_path.strip().strip("`'\"")
        return cleaned.rstrip(".,;:")

    def extract_changed_files(self, output: str) -> List[str]:
        """Extract Python files mentioned as changed in output."""
        matches = {self._normalize_path(p) for p in self._file_patterns.findall(output)}
        for path in self._change_patterns.findall(output):
            cleaned = self._normalize_path(path)
            if not cleaned:
                continue
            suffix = Path(cleaned).suffix.lower()
            if suffix and suffix not in {".md", ".mdx", ".rst", ".txt"}:
                matches.add(cleaned)
        return sorted(p for p in matches if p)

    def extract_doc_updates(self, output: str) -> List[str]:
        """Extract markdown files mentioned as updated in output."""
        matches = {self._normalize_path(p) for p in self._doc_patterns.findall(output)}
        for path in self._change_patterns.findall(output):
            cleaned = self._normalize_path(path)
            if not cleaned:
                continue
            if Path(cleaned).suffix.lower() in {".md", ".mdx"}:
                matches.add(cleaned)
        return sorted(p for p in matches if p)

    async def check_agent_output(self, agent: AgentHandle) -> Optional[DriftWarning]:
        """
        Check agent output for potential drift.

        Returns DriftWarning if code was changed but no docs updated.
        """
        output = agent.get_output()

        code_files = self.extract_changed_files(output)
        doc_files = self.extract_doc_updates(output)

        # Skip check if agent explicitly mentioned SYNC updates
        if "SYNC" in output and any("SYNC" in d for d in doc_files):
            return None

        # Warning if code changed but no docs updated
        if code_files and not doc_files:
            return DriftWarning(
                agent_id=agent.id,
                agent_symbol=agent.symbol,
                message=f"Changed {', '.join(code_files)} but no doc updates detected",
                suggestion="Consider updating IMPLEMENTATION or SYNC docs",
                files_changed=code_files,
                docs_updated=doc_files,
            )

        return None

    async def monitor_agent(self, agent: AgentHandle) -> None:
        """
        Monitor an agent and report any drift warnings.

        Called periodically or when agent completes.
        """
        warning = await self.check_agent_output(agent)
        if warning:
            await self.on_warning(warning)

    async def on_agent_complete(self, agent: AgentHandle) -> None:
        """Handle agent completion - final drift check."""
        output = agent.get_output()
        if not output.strip():
            return

        warning = await self.check_agent_output(agent)
        if warning:
            await self.on_warning(warning)


# Guidance injection for PostToolUse hook pattern
MANAGER_GUIDANCE_FILE = ".ngram/manager-guidance.json"


def write_guidance(guidance: str) -> None:
    """
    Write guidance for PostToolUse hook to inject.

    The hook reads this and injects as user message.
    Used by TUI to steer agents mid-work.
    """
    import json
    from pathlib import Path

    path = Path(MANAGER_GUIDANCE_FILE)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"guidance": guidance}))


def clear_guidance() -> None:
    """Clear any pending guidance."""
    from pathlib import Path

    path = Path(MANAGER_GUIDANCE_FILE)
    if path.exists():
        path.unlink()
