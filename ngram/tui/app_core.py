# DOCS: docs/tui/PATTERNS_TUI_Modular_Interface_Design.md
"""
ngram TUI - Main Textual Application.

Agent-style persistent chat interface with:
- Manager panel (left column)
- Agent panels (right columns/tabs)
- Input bar (bottom)
- Status bar (top)
"""

import asyncio
from pathlib import Path
from typing import Optional

try:
    from textual.app import App, ComposeResult
    from textual.containers import Container, Horizontal, Vertical
    from textual.widgets import Footer, Static
    from textual.binding import Binding
    from textual.widget import Widget
    TEXTUAL_AVAILABLE = True
except ImportError:
    TEXTUAL_AVAILABLE = False
    # Stubs for type checking when textual not installed
    App = object
    ComposeResult = None

from .state import SessionState, ConversationHistory
from .manager import ManagerSupervisor, DriftWarning, ClaudePTY
from .widgets.manager_panel import ManagerPanel, ClickableStatic
from .app_manager import start_manager_with_overview


def check_textual() -> None:
    """Raise ImportError if textual is not available."""
    if not TEXTUAL_AVAILABLE:
        raise ImportError(
            "textual is required for the TUI. Install with: pip install ngram[tui]"
        )


class NgramApp(App if TEXTUAL_AVAILABLE else object):
    """
    ngram TUI Application.

    Layout:
    - Top: Status bar with health score
    - Left: Manager panel (~55% width)
    - Right: Agent container (columns or tabs)
    - Bottom: Input bar with /command support
    """

    CSS_PATH = "styles/theme_light.tcss"

    # Light mode for Wood & Paper theme (sunlit desk)
    dark = False

    BINDINGS = [
        Binding("ctrl+c", "interrupt_or_quit", "Interrupt/Quit", show=False),
        Binding("ctrl+d", "doctor", "Doctor", show=False),
        Binding("ctrl+r", "repair", "Repair", show=False),
        Binding("ctrl+p", "command_palette", show=False),
        # Tab switching: Ctrl+1-5 for direct access (order: CHANGES, SYNC, DOCTOR, MAP, AGENTS)
        Binding("ctrl+1", "tab_changes", "Changes", show=False),
        Binding("ctrl+2", "tab_sync", "Sync", show=False),
        Binding("ctrl+3", "tab_doctor", "Doctor", show=False),
        Binding("ctrl+4", "tab_map", "Map", show=False),
        Binding("ctrl+5", "tab_agents", "Agents", show=False),
        # Tab cycling - multiple key options
        Binding("tab", "next_tab", "Next Tab", show=False),
        Binding("shift+tab", "prev_tab", "Prev Tab", show=False),
        Binding("ctrl+tab", "next_tab", "Next Tab", show=False),
        Binding("ctrl+shift+tab", "prev_tab", "Prev Tab", show=False),
    ]

    def __init__(self, target_dir: Optional[Path] = None, agent_provider: str = "claude") -> None:
        """Initialize the TUI app."""
        from ..agent_cli import normalize_agent

        check_textual()
        super().__init__()
        self.target_dir = target_dir or Path.cwd()
        self.agent_provider = normalize_agent(agent_provider)
        self.state = SessionState()
        self.conversation = ConversationHistory(self.target_dir)
        self.supervisor = ManagerSupervisor(on_warning=self._handle_drift_warning)
        self._in_error_handler = False  # Prevent infinite loops
        self.claude_pty: Optional[ClaudePTY] = None
        self._ctrl_c_pending = False  # Track first Ctrl+C press
        self._running_process: Optional[asyncio.subprocess.Process] = None  # Track agent subprocess
        self._manager_wakeup_animation_task: Optional[asyncio.Task] = None
        self._manager_force_new_session: bool = False
        self._changes_last_refresh = 0.0
        self._changes_refresh_interval = 300.0
        self._changes_refresh_inflight = False
        self._sync_last_refresh = 0.0
        self._sync_refresh_interval = 120.0
        self._sync_refresh_inflight = False
        self._map_last_refresh = 0.0
        self._map_refresh_interval = 120.0
        self._map_refresh_inflight = False
        self._doctor_last_refresh = 0.0
        self._doctor_refresh_interval = 120.0
        self._doctor_refresh_inflight = False

    def compose(self) -> ComposeResult:
        """Compose the TUI layout."""
        from .widgets.status_bar import StatusBar
        from .widgets.manager_panel import ManagerPanel
        from .widgets.agent_container import AgentContainer
        from .widgets.input_bar import InputBar
        from .widgets.suggestions import SuggestionsBar

        yield StatusBar(folder_name=self.target_dir.name, id="status-bar")

        with Horizontal(id="main-container"):
            # Left column: manager panel + input
            with Vertical(id="manager-column"):
                yield ManagerPanel(id="manager-panel")
                yield SuggestionsBar(id="suggestions-bar")
                yield InputBar(id="input-bar")
            # Right column: agent container
            yield AgentContainer(id="agent-container")

    async def on_mount(self) -> None:
        """Run on app mount - initial setup."""
        # Ensure markdown bold styling uses orange without background.
        try:
            from rich.theme import Theme

            self.console.push_theme(
                Theme(
                    {
                        "bold": "bold #D2691E on #FAF6ED",
                        "markdown.strong": "bold #D2691E on #FAF6ED",
                        "markdown.h1": "bold #D2691E on #FAF6ED",
                        "markdown.h2": "bold #D2691E on #FAF6ED",
                        "markdown.h3": "bold #D2691E on #FAF6ED",
                        "markdown.h4": "bold #D2691E on #FAF6ED",
                        "markdown.h5": "bold #D2691E on #FAF6ED",
                        "markdown.h6": "bold #D2691E on #FAF6ED",
                        "markdown.h1.border": "#D2691E on #FAF6ED",
                    }
                ),
                inherit=True,
            )
        except Exception:
            pass

        # Focus input bar
        input_bar = self.query_one("#input-bar")
        input_bar.focus()

        manager = self.query_one("#manager-panel")

        # Load previous conversation history
        previous = self.conversation.get_recent(limit=20)
        if previous:
            from textual.widgets import Static
            # Add separator
            sep1 = Static("[dim]─── Previous Session ───[/]", classes="message")
            manager.mount(sep1)
            manager._messages.append(sep1)

            for msg in previous:
                if msg.role == "system" and "New Session" in msg.content:
                    widget = Static(f"[dim]{msg.content}[/]", classes="message")
                elif msg.role == "user":
                    widget = Static(f"[magenta]{msg.content}[/magenta]", classes="message")
                else:
                    # Truncate long assistant messages for history display
                    content = msg.content
                    if len(content) > 500:
                        content = content[:500] + "..."
                    widget = Static(f"[dim]{content}[/]", classes="message")
                manager.mount(widget)
                manager._messages.append(widget)

            sep2 = Static("[dim]─── Current Session ───[/]", classes="message")
            manager.mount(sep2)
            manager._messages.append(sep2)

        # Mark new session start
        self.conversation.start_new_session()

        # Add welcome messages in blue
        health_check_msg = manager.add_message("[blue]Running health check...[/]")
        manager_wakeup_msg = manager.add_message("[blue]Waking up ngram manager...[/]")
        self._manager_wakeup_animation_task = asyncio.create_task(self._animate_loading(manager_wakeup_msg))

        # Run startup tasks in background so UI appears immediately
        asyncio.create_task(self._startup_sequence(manager, health_check_msg, manager_wakeup_msg))

    async def _startup_sequence(self, manager: ManagerPanel, health_check_msg: ClickableStatic, manager_wakeup_msg: ClickableStatic) -> None:
        """Run startup tasks: doctor check then manager overview."""
        # Run initial health check and show issues
        await self._run_doctor_with_display(manager)

        manager = self.query_one("#manager-panel")
        manager_wakeup_msg = manager.add_message("[blue]Waking up ngram manager[/] [dim]...[/]")
        self._manager_wakeup_animation_task = asyncio.create_task(
            self._animate_loading(manager_wakeup_msg, prefix="[blue]Waking up ngram manager[/] ")
        )

        # Start manager session (also in this background task)
        await self._start_manager_with_overview(manager)

        if self._manager_wakeup_animation_task:
            self._manager_wakeup_animation_task.cancel()
        manager_wakeup_msg.remove()

    async def _start_claude_pty(self) -> None:
        """Start the interactive Claude PTY session."""
        if self.agent_provider != "claude":
            return
        manager = self.query_one("#manager-panel")

        # Load system prompt from .ngram/agents/manager/CLAUDE.md
        system_prompt = ""
        prompt_file = self.target_dir / ".ngram" / "agents" / "manager" / "CLAUDE.md"
        if prompt_file.exists():
            system_prompt = prompt_file.read_text()

        async def on_claude_output(text: str) -> None:
            """Handle output from Claude PTY."""
            if text.strip():
                manager.add_message(text)

        self.claude_pty = ClaudePTY(
            target_dir=self.target_dir,
            on_output=on_claude_output,
            system_prompt=system_prompt,
        )

        success = await self.claude_pty.start()
        if not success:
            manager.add_message("[dim]Manager agent not available - using fallback mode[/dim]")

    async def _start_manager_with_overview(self, manager: ManagerPanel) -> None:
        """Start manager and prompt for project overview."""
        await start_manager_with_overview(self, manager)

    async def _animate_loading(self, widget, prefix: str = "") -> None:
        """Animate the loading indicator until cancelled."""
        dots = [".", "..", "...", ".."]
        i = 0
        try:
            while True:
                await asyncio.sleep(0.3)
                if prefix:
                    await widget.update(f"{prefix}[dim]{dots[i % len(dots)]}[/]")
                else:
                    await widget.update(f"[dim]{dots[i % len(dots)]}[/]")
                i += 1
        except asyncio.CancelledError:
            pass  # Animation cancelled, exit cleanly
        except Exception:
            pass  # Widget removed or app closing

    def on_click(self) -> None:
        """Focus input bar on any click."""
        input_bar = self.query_one("#input-bar")
        input_bar.focus()

    async def on_input_bar_command_submitted(self, event) -> None:
        """Handle command submitted from input bar."""
        from .widgets.input_bar import InputBar

        try:
            await self.handle_command(event.command)
        except Exception as e:
            self.log_error(str(e))

    def on_input_bar_input_changed(self, event) -> None:
        """Scroll chat to bottom when user starts typing."""
        manager = self.query_one("#manager-panel")
        manager.scroll_end(animate=False)

    def on_input_bar_show_suggestions(self, event) -> None:
        """Show or hide command suggestions."""
        from .widgets.suggestions import SuggestionsBar
        suggestions_bar = self.query_one("#suggestions-bar", SuggestionsBar)
        suggestions_bar.show_suggestions(event.suggestions)

    async def _run_doctor(self) -> None:
        """Run doctor check and update health score."""
        manager = self.query_one("#manager-panel")
        manager.add_message("[blue]Running health check...[/]")

        try:
            result = await self._run_doctor_async()
            self.state.health_score = result.get("score", 0)
            status_bar = self.query_one("#status-bar")
            status_bar.update_health(self.state.health_score)
            manager.add_message(f"Health: {self.state.health_score}/100")
        except Exception as e:
            self.log_error(f"Health check failed: {e}")

    async def _run_doctor_with_display(self, manager: ManagerPanel) -> None:
        """Run doctor check and display issues in DOCTOR tab (parallelized)."""
        from .widgets.agent_container import AgentContainer
        import asyncio

        agent_container = self.query_one("#agent-container", AgentContainer)

        try:
            manager.add_message("[dim]Loading tabs...[/]")

            # Update tabs in background to avoid blocking startup
            asyncio.create_task(self._refresh_doctor_tab(force=True))
            asyncio.create_task(self._refresh_sync_tab(force=True))
            asyncio.create_task(self._refresh_map_tab(force=True))
            asyncio.create_task(self._refresh_changes_tab(force=True))

            # Default to CHANGES tab on startup
            agent_container.switch_to_tab("changes-tab")
            manager.add_message("[dim]Tabs loaded.[/]")

        except Exception as e:
            manager.add_message(f"[red]Startup error: {e}[/]")
            self.log_error(f"Health check failed: {e}")

    async def _load_doctor_data(self) -> tuple:
        """Load doctor data in executor."""
        from ..doctor import run_doctor
        from ..doctor_files import load_doctor_config
        import asyncio

        loop = asyncio.get_event_loop()
        config = load_doctor_config(self.target_dir)
        result = await loop.run_in_executor(
            None,
            lambda: run_doctor(self.target_dir, config)
        )

        score = result.get("score", 50) if isinstance(result, dict) else 50
        issues_dict = result.get("issues", {}) if isinstance(result, dict) else {}

        all_issues = []
        if isinstance(issues_dict, dict):
            for severity in ["critical", "warning", "info"]:
                all_issues.extend(issues_dict.get(severity, []))

        return score, all_issues

    async def _load_sync_data(self) -> str:
        """Load SYNC file in executor."""
        import asyncio

        sync_file = self.target_dir / ".ngram" / "state" / "SYNC_Project_State.md"
        if not sync_file.exists():
            return ""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, sync_file.read_text)

    async def _load_map_data(self) -> str:
        """Load map.md in executor."""
        import asyncio

        map_file = self.target_dir / "map.md"
        if not map_file.exists():
            return ""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, map_file.read_text)

    async def _load_git_data(self) -> tuple:
        """Load git status and log concurrently."""
        import asyncio
        from datetime import datetime

        updated_at = datetime.now().strftime("%H:%M")
        window_minutes = 60

        async def get_status():
            try:
                proc = await asyncio.create_subprocess_exec(
                    "git", "status", "--short",
                    cwd=self.target_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=3)
                return stdout.decode().strip() if proc.returncode == 0 else ""
            except Exception:
                return "(unable to get git status)"

        async def get_log():
            try:
                proc = await asyncio.create_subprocess_exec(
                    "git", "log", "--format=%h %s (%ar)", "-15",
                    cwd=self.target_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=3)
                return stdout.decode().strip() if proc.returncode == 0 else ""
            except Exception:
                return "(unable to get git log)"

        async def get_recent_commit_rate():
            try:
                proc = await asyncio.create_subprocess_exec(
                    "git", "log", f"--since={window_minutes}.minutes", "--pretty=oneline",
                    cwd=self.target_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=3)
                lines = stdout.decode().splitlines()
                count = len([line for line in lines if line.strip()])
                return count / window_minutes
            except Exception:
                return 0.0

        async def get_recent_change_rate():
            try:
                proc = await asyncio.create_subprocess_exec(
                    "git", "log", f"--since={window_minutes}.minutes", "--name-only", "--pretty=format:",
                    cwd=self.target_dir,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=3)
                files = {line for line in stdout.decode().splitlines() if line.strip()}
                return len(files) / window_minutes
            except Exception:
                return 0.0

        file_changes, commits, change_rate, commit_rate = await asyncio.gather(
            get_status(), get_log(), get_recent_change_rate(), get_recent_commit_rate()
        )
        return file_changes, commits, updated_at, change_rate, commit_rate

    async def _refresh_changes_tab(self, force: bool = False) -> None:
        """Refresh CHANGES tab data with a minimum interval."""
        import time
        from .widgets.agent_container import AgentContainer

        now = time.monotonic()
        if not force and (now - self._changes_last_refresh) < self._changes_refresh_interval:
            return
        if self._changes_refresh_inflight:
            return

        self._changes_refresh_inflight = True
        try:
            git_data = await self._load_git_data()
            agent_container = self.query_one("#agent-container", AgentContainer)
            file_changes, commits, updated_at, change_rate, commit_rate = git_data
            agent_container.update_changes_content(
                file_changes, commits, updated_at, change_rate, commit_rate
            )
            self._changes_last_refresh = time.monotonic()
        except Exception as e:
            manager = self.query_one("#manager-panel")
            manager.add_message(f"[red]CHANGES tab error: {e}[/]")
        finally:
            self._changes_refresh_inflight = False

    async def _refresh_sync_tab(self, force: bool = False) -> None:
        """Refresh SYNC tab data with a minimum interval."""
        import time
        from .widgets.agent_container import AgentContainer

        now = time.monotonic()
        if not force and (now - self._sync_last_refresh) < self._sync_refresh_interval:
            return
        if self._sync_refresh_inflight:
            return

        self._sync_refresh_inflight = True
        try:
            content = await self._load_sync_data()
            if content:
                agent_container = self.query_one("#agent-container", AgentContainer)
                agent_container.update_sync_content(content)
            self._sync_last_refresh = time.monotonic()
        except Exception as e:
            manager = self.query_one("#manager-panel")
            manager.add_message(f"[red]SYNC tab error: {e}[/]")
        finally:
            self._sync_refresh_inflight = False

    async def _refresh_map_tab(self, force: bool = False) -> None:
        """Refresh MAP tab data with a minimum interval."""
        import time
        from .widgets.agent_container import AgentContainer

        now = time.monotonic()
        if not force and (now - self._map_last_refresh) < self._map_refresh_interval:
            return
        if self._map_refresh_inflight:
            return

        self._map_refresh_inflight = True
        try:
            content = await self._load_map_data()
            if content:
                agent_container = self.query_one("#agent-container", AgentContainer)
                agent_container.update_map_content(content)
            self._map_last_refresh = time.monotonic()
        except Exception as e:
            manager = self.query_one("#manager-panel")
            manager.add_message(f"[red]MAP tab error: {e}[/]")
        finally:
            self._map_refresh_inflight = False

    async def _refresh_doctor_tab(self, force: bool = False) -> None:
        """Refresh DOCTOR tab data with a minimum interval."""
        import time
        from .widgets.agent_container import AgentContainer

        now = time.monotonic()
        if not force and (now - self._doctor_last_refresh) < self._doctor_refresh_interval:
            return
        if self._doctor_refresh_inflight:
            return

        self._doctor_refresh_inflight = True
        try:
            score, all_issues = await self._load_doctor_data()
            self.state.health_score = score
            status_bar = self.query_one("#status-bar")
            status_bar.update_health(score)
            repair_issues = [i for i in all_issues if i.severity in ("critical", "warning")]
            if repair_issues:
                status_bar.set_repair_progress(len(repair_issues), 0, 0)

            agent_container = self.query_one("#agent-container", AgentContainer)
            agent_container.update_doctor_content(all_issues, score)
            self._doctor_last_refresh = time.monotonic()
        except Exception as e:
            manager = self.query_one("#manager-panel")
            manager.add_message(f"[red]DOCTOR tab error: {e}[/]")
        finally:
            self._doctor_refresh_inflight = False

    async def _run_doctor_async(self) -> dict:
        """Run doctor check asynchronously."""
        import asyncio
        from ..doctor import run_doctor
        from ..doctor_files import load_doctor_config

        # Run doctor in executor to not block event loop
        loop = asyncio.get_event_loop()
        config = load_doctor_config(self.target_dir)
        result = await loop.run_in_executor(
            None,
            lambda: run_doctor(self.target_dir, config)
        )
        return {"score": result.get("score", 50) if isinstance(result, dict) else 50}

    async def _handle_drift_warning(self, warning: DriftWarning) -> None:
        """Handle drift warning from supervisor."""
        manager = self.query_one("#manager-panel")
        manager.add_message(
            f"[warning]{warning.agent_symbol} {warning.message}[/warning]"
        )
        manager.add_message(f"  -> {warning.suggestion}")

    async def handle_command(self, command: str) -> None:
        """Handle a slash command from input bar."""
        from .commands import handle_command

        self.state.last_command = command
        await handle_command(self, command)

    def log_error(self, error: str) -> None:
        """Log an error to the manager panel and .ngram/error-log."""
        if self._in_error_handler:
            return  # Prevent infinite loops

        self._in_error_handler = True
        try:
            # Log to file
            from datetime import datetime
            error_log = self.target_dir / ".ngram" / "error.log"
            error_log.parent.mkdir(parents=True, exist_ok=True)
            with open(error_log, "a") as f:
                timestamp = datetime.now().isoformat()
                f.write(f"[{timestamp}] {error}\n")

            # Show in manager panel
            manager = self.query_one("#manager-panel")
            manager.add_message(f"[red]Error: {error}[/red]")
        except Exception:
            pass  # Silently fail if we can't show the error
        finally:
            self._in_error_handler = False

    def on_exception(self, error: Exception) -> bool:
        """Handle uncaught exceptions by showing in manager panel."""
        import traceback
        # Suppress selection-related IndexErrors (Textual bug with dynamic content)
        if isinstance(error, IndexError):
            tb_str = "".join(traceback.format_tb(error.__traceback__))
            # Check for various selection-related paths in traceback
            if any(s in tb_str for s in ["selection", "get_copy_text", "extract", "Selection"]):
                return True  # Suppress silently - known Textual bug
        self.log_error(str(error))
        return True  # Return True to prevent crash, keep app running

    def notify_manager_response(self) -> None:
        """Emit an audible bell when the manager responds."""
        import sys

        try:
            sys.stdout.write("\a")
            sys.stdout.flush()
        except Exception:
            pass

    def reset_manager_session(self) -> None:
        """Force a fresh manager session on next message."""
        self._manager_force_new_session = True
        self._llm_conversation_started = False
        self._pending_commands = []

    async def action_interrupt_or_quit(self) -> None:
        """Handle Ctrl+C: first press interrupts, second press quits."""
        if self._ctrl_c_pending:
            # Second press - quit
            await self.action_quit()
            return

        manager = self.query_one("#manager-panel")

        # First press - interrupt agent subprocess if running
        if self._running_process and self._running_process.returncode is None:
            try:
                self._running_process.kill()
                manager.add_message("[dim]*Interrupted*[/]")
            except Exception:
                pass
            self._running_process = None
            self._ctrl_c_pending = True
            self.set_timer(2.0, self._reset_ctrl_c)
        elif self.claude_pty and self.claude_pty.is_running:
            await self.claude_pty.stop()
            manager.add_message("[dim]*Interrupted*[/]")
            self._ctrl_c_pending = True
            self.set_timer(2.0, self._reset_ctrl_c)
        else:
            # Nothing running - set pending for quit
            self._ctrl_c_pending = True
            manager.add_message("[dim]*Press Ctrl+C again to quit*[/]")
            self.set_timer(2.0, self._reset_ctrl_c)

    def _reset_ctrl_c(self) -> None:
        """Reset the Ctrl+C pending flag."""
        self._ctrl_c_pending = False

    async def action_quit(self) -> None:
        """Quit the application."""
        self.state.running = False
        # Stop PTY if running
        if self.claude_pty and self.claude_pty.is_running:
            await self.claude_pty.stop()
        self.exit()

    async def action_doctor(self) -> None:
        """Run doctor check."""
        await self._run_doctor()

    async def action_repair(self) -> None:
        """Start repair session."""
        await self.handle_command("/repair")

    # Tab switching actions
    def action_tab_agents(self) -> None:
        """Switch to AGENTS tab."""
        self._switch_tab("agents-tab")

    def action_tab_sync(self) -> None:
        """Switch to SYNC tab."""
        self._switch_tab("sync-tab")

    def action_tab_doctor(self) -> None:
        """Switch to DOCTOR tab."""
        self._switch_tab("doctor-tab")

    def action_tab_map(self) -> None:
        """Switch to MAP tab."""
        self._switch_tab("map-tab")

    def action_tab_changes(self) -> None:
        """Switch to CHANGES tab."""
        self._switch_tab("changes-tab")

    def action_next_tab(self) -> None:
        """Switch to next tab."""
        tabs = ["changes-tab", "sync-tab", "doctor-tab", "map-tab", "agents-tab"]
        self._cycle_tab(tabs, 1)

    def action_prev_tab(self) -> None:
        """Switch to previous tab."""
        tabs = ["changes-tab", "sync-tab", "doctor-tab", "map-tab", "agents-tab"]
        self._cycle_tab(tabs, -1)

    def _switch_tab(self, tab_id: str) -> None:
        """Switch to a specific tab."""
        from .widgets.agent_container import AgentContainer
        try:
            agent_container = self.query_one("#agent-container", AgentContainer)
            agent_container.switch_to_tab(tab_id)
        except Exception:
            pass

    def _cycle_tab(self, tabs: list, direction: int) -> None:
        """Cycle through tabs."""
        from .widgets.agent_container import AgentContainer
        try:
            agent_container = self.query_one("#agent-container", AgentContainer)
            tabbed = agent_container.query_one("#right-tabs")
            current = tabbed.active
            if current in tabs:
                idx = tabs.index(current)
                new_idx = (idx + direction) % len(tabs)
                agent_container.switch_to_tab(tabs[new_idx])
        except Exception:
            pass
