# DOCS: docs/tui/BEHAVIORS_TUI_Interactions.md
"""
Slash command handlers for the TUI.

Commands:
- /help - Show available commands
- /repair - Start repair session
- /doctor - Run health check
- /issues - Display issues list
- /logs - View completed agent logs
- /quit - Exit TUI
"""

from typing import TYPE_CHECKING
import uuid

from .commands_agent import _run_agent_message


def _truncate_thinking(text: str, max_lines: int = 3) -> str:
    """Truncate thinking text to approximately max_lines with ellipsis."""
    lines = text.split('\n')
    if len(lines) <= max_lines:
        return text
    truncated = '\n'.join(lines[:max_lines])
    return f"{truncated}..."


if TYPE_CHECKING:
    from .app import NgramApp


async def handle_command(app: "NgramApp", command: str) -> None:
    """
    Route a slash command to its handler, or respond to messages.

    Pattern: Factory/Router
    """
    command = command.strip()

    # Check for numeric input to run pending commands
    if command.strip().isdigit():
        num = int(command.strip())
        pending = getattr(app, '_pending_commands', [])
        if 1 <= num <= len(pending):
            cmd_to_run = pending[num - 1]
            manager = app.query_one("#manager-panel")
            manager.add_message(f"[dim]Running: {cmd_to_run}[/]")
            app._pending_commands = []  # Clear pending
            await handle_run(app, cmd_to_run)
            return
        elif pending:
            manager = app.query_one("#manager-panel")
            manager.add_message(f"[red]Invalid option. Choose 1-{len(pending)}[/]")
            return

    # Handle slash commands
    if command.startswith("/"):
        parts = command.split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""

        handlers = {
            "/help": handle_help,
            "/repair": handle_repair,
            "/doctor": handle_doctor,
            "/quit": handle_quit,
            "/clear": handle_clear,
            "/issues": handle_issues,
            "/run": handle_run,
            "/logs": handle_logs,
            "/reset-manager": handle_reset_manager,
        }

        handler = handlers.get(cmd)
        if handler:
            try:
                await handler(app, args)
            except Exception as e:
                app.log_error(f"{cmd} failed: {e}")
        else:
            manager = app.query_one("#manager-panel")
            manager.add_message(f"Unknown command: {cmd}. Type /help for commands.")
    else:
        # Handle regular messages - manager responds
        await handle_message(app, command)


async def handle_message(app: "NgramApp", message: str) -> None:
    """Handle a non-command message - send to the agent via subprocess."""
    import asyncio
    import inspect

    manager = app.query_one("#manager-panel")

    # Show user input in violet with empty line before
    manager.add_message("")
    manager.add_message(f"[magenta]{message}[/magenta]")

    # Save user message to history
    app.conversation.add_message("user", message)

    # Create response widget with animated dots
    response_widget = manager.add_message("[dim].[/]")

    # Shared flag to signal animation to stop
    stop_animation = {"flag": False}

    # Run agent in background so UI stays responsive
    asyncio.create_task(_run_agent_message(app, message, response_widget, stop_animation))

    # Start animation task
    asyncio.create_task(_animate_loading(response_widget, stop_animation))


async def _animate_loading(widget, stop_flag: dict) -> None:
    """Animate the loading indicator until stop flag is set."""
    import asyncio
    import inspect
    dots = [".", "..", "..."]
    i = 0
    try:
        while not stop_flag.get("flag", False):
            result = widget.update(f"[dim]{dots[i % len(dots)]}[/]")
            if inspect.isawaitable(result):
                await result
            widget.refresh()
            i += 1
            await asyncio.sleep(0.3)
            # Check stop flag after sleep
            if stop_flag.get("flag", False):
                break
    except Exception:
        pass  # Widget removed or app closing




async def handle_help(app: "NgramApp", args: str) -> None:
    """Show available commands."""
    manager = app.query_one("#manager-panel")
    help_text = """Available commands:
  /help    - Show this help
  /run CMD - Run shell command with streaming output
  /repair  - Start repair session
  /doctor  - Run health check
  /issues  - Display issues list
  /logs    - View completed agent logs (collapsible)
  /reset-manager - Reset manager session (fresh system prompt)
  /clear   - Clear manager messages
  /quit    - Exit TUI

Keyboard shortcuts:
  Ctrl+C   - Interrupt (2x to quit)
  Ctrl+D   - Run doctor
  Ctrl+R   - Start repair"""
    manager.add_message(help_text)
    app.conversation.add_message("system", "/help\n" + help_text)


async def handle_run(app: "NgramApp", args: str) -> None:
    """Run a shell command with streaming output."""
    import asyncio

    manager = app.query_one("#manager-panel")

    if not args.strip():
        manager.add_message("[red]Usage: /run <command>[/]")
        return

    manager.add_message(f"[dim]$ {args}[/]")

    # Create output widget
    output_widget = manager.add_message("[dim]...[/]")

    # Run command in background
    asyncio.create_task(_run_shell_command(app, args, output_widget))


async def _run_shell_command(app: "NgramApp", command: str, output_widget) -> None:
    """Run shell command and stream output."""
    import asyncio

    try:
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
            cwd=app.target_dir,
        )

        output_lines = []
        buffer = ""

        if process.stdout:
            while True:
                # Use chunk-based reading to avoid line length limits
                chunk = await process.stdout.read(65536)
                if not chunk:
                    break
                buffer += chunk.decode(errors='replace')

                # Process complete lines
                while '\n' in buffer:
                    line_str, buffer = buffer.split('\n', 1)
                    output_lines.append(line_str.rstrip())
                    # Update widget with last 50 lines
                    output_widget.update("\n".join(output_lines[-50:]))

            # Handle any remaining buffer content
            if buffer.strip():
                output_lines.append(buffer.rstrip())

        await process.wait()

        # Final update
        final_output = "\n".join(output_lines[-100:]) if output_lines else "(no output)"
        if output_lines:
            output_widget.update(final_output)
        else:
            output_widget.update("[dim](no output)[/]")

        # Log to conversation history
        log_entry = f"$ {command}\n{final_output}"
        if process.returncode != 0:
            log_entry += f"\nExit code: {process.returncode}"
            manager = app.query_one("#manager-panel")
            manager.add_message(f"[red]Exit code: {process.returncode}[/]")
        app.conversation.add_message("system", log_entry)

    except Exception as e:
        output_widget.update(f"[red]Error: {e}[/]")
        app.conversation.add_message("system", f"$ {command}\nError: {e}")


async def handle_repair(app: "NgramApp", args: str) -> None:
    """Start a repair session."""
    import asyncio
    from datetime import datetime
    from ..doctor import run_doctor
    from ..doctor_files import load_doctor_config
    from ..repair_core import AGENT_SYMBOLS
    from .state import AgentHandle

    manager = app.query_one("#manager-panel")
    agent_container = app.query_one("#agent-container")

    manager.add_message("")
    manager.add_message("[bold]Starting repair session...[/]")

    # Create session folder with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_dir = app.target_dir / ".ngram" / "repairs" / timestamp
    session_dir.mkdir(parents=True, exist_ok=True)
    app._repair_session_dir = session_dir
    manager.add_message(f"[dim]Session: .ngram/repairs/{timestamp}/[/]")

    # Run doctor to find issues (load config from .ngramignore)
    try:
        loop = asyncio.get_event_loop()
        config = load_doctor_config(app.target_dir)
        result = await loop.run_in_executor(
            None,
            lambda: run_doctor(app.target_dir, config)
        )

        # Flatten issues from dict structure
        issues_dict = result.get("issues", {}) if isinstance(result, dict) else {}
        all_issues = []
        for severity in ["critical", "warning"]:  # Skip info for repair
            all_issues.extend(issues_dict.get(severity, []))

        # Deduplicate by (issue_type, path)
        seen = set()
        unique_issues = []
        for issue in all_issues:
            key = (issue.issue_type, issue.path)
            if key not in seen:
                seen.add(key)
                unique_issues.append(issue)
        all_issues = unique_issues

        # Sort by priority (lower = fix first)
        from ..repair_core import ISSUE_PRIORITY
        all_issues.sort(key=lambda i: ISSUE_PRIORITY.get(i.issue_type, 50))

    except Exception as e:
        manager.add_message(f"[red]Doctor failed: {e}[/]")
        return

    # Initialize status bar progress immediately after doctor
    status_bar = app.query_one("#status-bar")

    if not all_issues:
        manager.add_message("[green]No issues found. Project is healthy![/]")
        app.conversation.add_message("system", "/repair\nNo issues found. Project is healthy!")
        return

    # Show progress bar immediately with all issues as pending
    status_bar.set_repair_progress(len(all_issues), 0, 0)

    manager.add_message(f"Found {len(all_issues)} issues to repair.")
    # Show all issues in a single block to avoid extra spacing between items
    from ..repair_core import AGENT_SYMBOLS
    issue_lines = []
    for i, issue in enumerate(all_issues):
        symbol = AGENT_SYMBOLS[i % len(AGENT_SYMBOLS)]
        issue_lines.append(f"[dim]{symbol} {issue.issue_type}: {issue.path}[/]")
    manager.add_message("\n".join(issue_lines))
    # Log repair start
    issue_list = "\n".join(f"  - {i.issue_type}: {i.path}" for i in all_issues[:10])
    app.conversation.add_message("system", f"/repair\nFound {len(all_issues)} issues:\n{issue_list}")

    # Switch to agents tab and clear summary log
    agent_container.switch_to_tab("agents-tab")
    agent_container.clear_summary()
    agent_container.add_summary(f"[bold cyan]═══ REPAIR SESSION ═══[/]")
    agent_container.add_summary(f"[dim]Issues to fix:[/] [bold]{len(all_issues)}[/]")

    # Store issue queue on app for agent completion to pull from
    from ..repair_instructions import get_issue_instructions

    max_agents = 3
    app._repair_queue = list(all_issues[max_agents:])  # Remaining issues
    app._repair_total = len(all_issues)
    app._repair_agent_index = max_agents  # Next agent index for symbol

    running_count = min(len(all_issues), max_agents)
    status_bar.set_repair_progress(len(all_issues), 0, running_count)

    for i, issue in enumerate(all_issues[:max_agents]):
        await _spawn_agent(app, issue, i)

    # Start periodic summary updater (lightweight, no streaming)
    asyncio.create_task(_periodic_agent_summary(app))


def _get_last_messages(output: str, n: int = 5) -> str:
    """Get last N meaningful lines from agent output."""
    lines = [l.strip() for l in output.split('\n') if l.strip()]
    # Filter out noise (empty, just symbols, very short)
    meaningful = [l for l in lines if len(l) > 10]
    return "\n".join(meaningful[-n:])


async def _periodic_agent_summary(app: "NgramApp") -> None:
    """Periodically summarize agent progress and file changes to summary log."""
    import asyncio
    from datetime import datetime
    from .commands_agent import _run_agent_message

    agent_container = app.query_one("#agent-container")
    manager = app.query_one("#manager-panel")

    async def _run_git_command(args: list[str], timeout: float = 5.0) -> str:
        """Run a git command asynchronously with timeout."""
        try:
            proc = await asyncio.create_subprocess_exec(
                "git",
                *args,
                cwd=app.target_dir,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return stdout.decode().strip() if proc.returncode == 0 else ""
        except Exception:
            return ""

    while True:
        await asyncio.sleep(120)  # Update every 2 minutes

        # Check if any agents still running
        running = [a for a in app.state.active_agents if a.status == "running"]
        if not running:
            break

        timestamp = datetime.now().strftime("%H:%M:%S")

        agent_container.add_summary(f"[dim]───────── {timestamp} ─────────[/]")

        # Show uncommitted file changes inline: filepath +N -N
        try:
            output = await _run_git_command(["diff", "--numstat"])
            if output.strip():
                for line in output.strip().split('\n')[:5]:
                    parts = line.split('\t')
                    if len(parts) >= 3:
                        added, removed, filepath = parts[0], parts[1], parts[2]
                        if added.isdigit() and removed.isdigit():
                            agent_container.add_summary(
                                f"[dim]{filepath}[/] [green]+{added}[/] [red]-{removed}[/]"
                            )
        except Exception:
            pass

        # Show new commits as they appear (no header)
        try:
            output = await _run_git_command(["log", "--oneline", "-5", "--since=1.hour.ago"])
            if output.strip():
                for line in output.strip().split('\n'):
                    if line.strip():
                        agent_container.add_summary(f"[cyan]📦 {line[:60]}[/]")
        except Exception:
            pass

        # Build summary request for all running agents
        summaries = []
        for agent in running:
            output = agent.get_output()
            if output:
                last_msgs = _get_last_messages(output, 5)
                summaries.append(f"Agent {agent.symbol} ({agent.issue_type}):\n{last_msgs}")

        if not summaries:
            continue

        # Ask manager to summarize
        prompt = f"""Summarize each agent's current progress in ONE short line each (max 10 words per agent). Be concise. No markdown.

{chr(10).join(summaries)}

Format exactly: SYMBOL: summary"""

        # Create a response widget and run manager
        response_widget = manager.add_message("[dim]...[/]")
        stop_animation = {"flag": False}

        try:
            await _run_agent_message(app, prompt, response_widget, stop_animation)
        except Exception:
            response_widget.update("[dim]Summary unavailable[/]")


async def _spawn_agent(app: "NgramApp", issue, agent_index: int) -> None:
    """Spawn a single repair agent for an issue."""
    import asyncio
    import time
    from ..repair_instructions import get_issue_instructions
    from ..repair_core import AGENT_SYMBOLS, get_issue_folder_name
    from .state import AgentHandle

    manager = app.query_one("#manager-panel")
    agent_container = app.query_one("#agent-container")

    symbol = AGENT_SYMBOLS[agent_index % len(AGENT_SYMBOLS)]
    # Use issue reference for folder name (more useful than symbol)
    folder_name = get_issue_folder_name(issue.issue_type, issue.path, agent_index)
    agent_id = f"agent-{uuid.uuid4().hex[:8]}"

    # Get session dir if available
    session_dir = getattr(app, '_repair_session_dir', None)

    agent = AgentHandle(
        id=agent_id,
        issue_type=issue.issue_type,
        target_path=issue.path,
        symbol=symbol,
    )
    app.state.add_agent(agent)
    agent_container.add_agent(agent)

    # Log agent start to summary
    agent_container.add_summary(f"[yellow]▶[/] {symbol} [bold]{issue.issue_type}[/] [dim]{issue.path}[/]")

    # Get instructions
    instructions = get_issue_instructions(issue, app.target_dir)

    # Simple output callback - just buffer for summary mode
    async def on_output(text: str, agent_ref=agent) -> None:
        """Buffer agent output (summary mode - no UI updates)."""
        if text and text.strip():
            agent_ref.append_output(text)

    manager.add_message(f"{symbol} {issue.issue_type}: {issue.path}")

    # Spawn agent in background
    asyncio.create_task(
        _run_agent(app, agent, issue, instructions, on_output, session_dir, folder_name)
    )


async def _run_agent(app: "NgramApp", agent, issue, instructions: dict, on_output, session_dir=None, folder_name=None) -> None:
    """Run a single repair agent."""
    import asyncio
    from ..repair_core import spawn_repair_agent_async

    manager = app.query_one("#manager-panel")
    agent_container = app.query_one("#agent-container")
    status_bar = app.query_one("#status-bar")

    try:
        result = await spawn_repair_agent_async(
            issue=issue,
            target_dir=app.target_dir,
            on_output=on_output,
            instructions=instructions,
            agent_id=agent.id,
            session_dir=session_dir,
            agent_symbol=folder_name,  # Now uses issue-based folder name
            agent_provider=app.agent_provider,
        )

        agent.status = "completed" if result.success else "failed"
        agent.error = result.error

        # Check for rate limit errors - stop repair loop if detected
        rate_limit_markers = ["usage_limit_reached", "rate_limit", "429", "Too Many Requests", "quota exceeded"]
        output_lower = result.agent_output.lower() if result.agent_output else ""
        is_rate_limited = any(marker.lower() in output_lower for marker in rate_limit_markers)

        if is_rate_limited:
            agent_container.add_summary(f"[red]⛔ RATE LIMIT - stopping repair[/]")
            manager.add_message("[red]Rate limit hit - repair stopped. Wait or switch agents.[/]")
            # Clear the queue to stop further agents
            if hasattr(app, '_repair_queue'):
                app._repair_queue.clear()
            return

        # Log to summary
        if result.success:
            agent_container.add_summary(f"[green]✓[/] {agent.symbol} [green]Done[/] [dim]{agent.issue_type}[/]")
        else:
            agent_container.add_summary(f"[red]✗[/] {agent.symbol} [red]Failed[/] [dim]{result.error or 'unknown'}[/]")

        # Supervisor check
        await app.supervisor.on_agent_complete(agent)

        if result.decisions_made:
            lines = [f"### Decisions ({agent.symbol})"]
            for decision in result.decisions_made:
                if not isinstance(decision, dict):
                    continue
                name = decision.get("name", "Decision")
                conflict = decision.get("conflict", "")
                resolution = decision.get("resolution", "")
                reasoning = decision.get("reasoning", "")
                updated = decision.get("updated", "")
                lines.append(f"- **{name}**")
                if conflict:
                    lines.append(f"  - Conflict: {conflict}")
                if resolution:
                    lines.append(f"  - Resolution: {resolution}")
                if reasoning:
                    lines.append(f"  - Reasoning: {reasoning}")
                if updated:
                    lines.append(f"  - Updated: {updated}")
            manager.add_message("\n".join(lines), markdown=True)

        if result.success:
            manager.add_message(f"[green]{agent.symbol} Done: {agent.issue_type}[/]")
            app.conversation.add_message("system", f"Repair {agent.symbol} completed: {agent.issue_type} ({agent.target_path})")
            # Refresh map async after successful repair
            asyncio.create_task(_refresh_map(app))
        else:
            manager.add_message(f"[red]{agent.symbol} Failed: {result.error or 'unknown'}[/]")
            app.conversation.add_message("system", f"Repair {agent.symbol} failed: {agent.issue_type} - {result.error or 'unknown'}")

    except Exception as e:
        agent.status = "failed"
        agent.error = str(e)
        result = None  # No result on exception
        agent_container.add_summary(f"[red]✗[/] {agent.symbol} [red]Error[/] [dim]{e}[/]")
        manager.add_message(f"[red]{agent.symbol} Error: {e}[/]")
        app.conversation.add_message("system", f"Repair {agent.symbol} error: {e}")

    # Spawn background manager review (non-blocking)
    if result is not None:
        asyncio.create_task(_manager_review_agent(app, agent, result))

    # Spawn next agent from queue if available
    await _spawn_next_from_queue(app)


async def _spawn_next_from_queue(app: "NgramApp") -> None:
    """Spawn the next agent from the repair queue if available."""
    status_bar = app.query_one("#status-bar")

    # Check if there are queued issues
    if not hasattr(app, '_repair_queue') or not app._repair_queue:
        # No more queued issues - update progress and maybe clear
        completed = len([a for a in app.state.active_agents if a.status in ("completed", "failed")])
        running = len([a for a in app.state.active_agents if a.status == "running"])
        total = getattr(app, '_repair_total', 0)
        status_bar.set_repair_progress(total, completed, running)
        if total > 0 and completed >= total:
            status_bar.clear_repair_progress()
        return

    # Pop next issue from queue
    next_issue = app._repair_queue.pop(0)
    agent_index = getattr(app, '_repair_agent_index', 0)
    app._repair_agent_index = agent_index + 1

    # Update progress before spawning
    completed = len([a for a in app.state.active_agents if a.status in ("completed", "failed")])
    running = len([a for a in app.state.active_agents if a.status == "running"]) + 1  # +1 for new agent
    total = getattr(app, '_repair_total', 0)
    status_bar.set_repair_progress(total, completed, running)

    # Spawn the new agent
    await _spawn_agent(app, next_issue, agent_index)


async def _manager_review_agent(app: "NgramApp", agent, result) -> None:
    """Background task to have manager review agent completion."""
    from .commands_agent import _build_review_prompt, _run_manager_review

    try:
        # Get last 2000 chars of output
        full_output = agent.get_output()
        output_tail = full_output[-2000:] if len(full_output) > 2000 else full_output

        prompt = _build_review_prompt(agent, result, output_tail)
        agent_info = {
            "symbol": agent.symbol,
            "issue_type": agent.issue_type,
            "target": agent.target_path,
        }
        await _run_manager_review(app, prompt, agent_info)
    except Exception as e:
        app.log_error(f"Manager review failed: {e}")


async def handle_doctor(app: "NgramApp", args: str) -> None:
    """Run health check."""
    manager = app.query_one("#manager-panel")
    status_bar = app.query_one("#status-bar")

    manager.add_message("[blue]Running health check...[/]")

    try:
        result = await app._run_doctor_async()
        score = result.get("score", 0)
        app.state.health_score = score
        status_bar.update_health(score)
        manager.add_message(f"Health: {score}/100")
        app.conversation.add_message("system", f"/doctor\nHealth: {score}/100")
    except Exception as e:
        manager.add_message(f"[red]Health check failed: {e}[/]")
        app.log_error(f"Doctor command failed: {e}")


async def handle_quit(app: "NgramApp", args: str) -> None:
    """Exit the TUI."""
    manager = app.query_one("#manager-panel")
    manager.add_message("Goodbye!")
    app.action_quit()


async def handle_clear(app: "NgramApp", args: str) -> None:
    """Clear manager messages."""
    manager = app.query_one("#manager-panel")
    manager.clear()
    app.state.manager_messages.clear()


async def handle_issues(app: "NgramApp", args: str) -> None:
    """Display issues list in DOCTOR tab."""
    import asyncio
    from ..doctor import run_doctor
    from ..doctor_files import load_doctor_config

    manager = app.query_one("#manager-panel")
    agent_container = app.query_one("#agent-container")

    manager.add_message("")
    manager.add_message("Running health check...")

    try:
        # Run doctor to find issues (load config from .ngramignore)
        loop = asyncio.get_event_loop()
        config = load_doctor_config(app.target_dir)
        result = await loop.run_in_executor(
            None,
            lambda: run_doctor(app.target_dir, config)
        )

        # Update health score
        score = result.get("score", 50) if isinstance(result, dict) else 50
        issues_dict = result.get("issues", {}) if isinstance(result, dict) else {}
        app.state.health_score = score

        status_bar = app.query_one("#status-bar")
        status_bar.update_health(score)

        # Flatten issues from dict structure
        all_issues = []
        if isinstance(issues_dict, dict):
            for severity in ["critical", "warning", "info"]:
                all_issues.extend(issues_dict.get(severity, []))

        # Switch to doctor tab (it already has issues displayed)
        agent_container.switch_to_tab("doctor-tab")

        # Update doctor tab with issues
        agent_container.update_doctor_content(all_issues, score)

        # Display summary in manager panel
        if all_issues:
            manager.add_message(f"Found {len(all_issues)} issues. See DOCTOR tab.")
        else:
            manager.add_message("[green]No issues found. Project is healthy![/]")

    except Exception as e:
        manager.add_message(f"[red]Health check failed: {e}[/]")
        app.log_error(f"Issues command failed: {e}")


async def handle_logs(app: "NgramApp", args: str) -> None:
    """Display completed agent logs in summary."""
    manager = app.query_one("#manager-panel")
    agent_container = app.query_one("#agent-container")

    # Get all agents (including completed ones)
    all_agents = app.state.active_agents

    # Filter to completed/failed agents that have output
    completed_agents = [
        a for a in all_agents
        if a.status in ("completed", "failed") and a.output_buffer
    ]

    if not completed_agents:
        manager.add_message("[dim]No completed agent logs available.[/]")
        return

    manager.add_message(f"Showing logs for {len(completed_agents)} completed agents.")

    # Switch to agents tab
    agent_container.switch_to_tab("agents-tab")

    # Add log summaries to the summary log
    agent_container.add_summary("[dim]─────── Agent Logs ───────[/]")
    for agent in completed_agents:
        status_color = "green" if agent.status == "completed" else "red"
        agent_container.add_summary(
            f"{agent.symbol} [{status_color}]{agent.status.upper()}[/] {agent.issue_type}: [dim]{agent.target_path}[/]"
        )

        # Get output (last 20 lines to show in summary)
        output = agent.get_output()
        lines = output.split('\n')
        if len(lines) > 20:
            lines = lines[-20:]
        for line in lines[-10:]:
            if line.strip():
                agent_container.add_summary(f"  [dim]{line[:80]}[/]")
        agent_container.add_summary("")


async def handle_reset_manager(app: "NgramApp", args: str) -> None:
    """Reset the manager session to force a new system prompt load."""
    manager = app.query_one("#manager-panel")
    app.reset_manager_session()
    app.conversation.clear()
    manager.add_message("[dim]Manager session reset. Next message will start a fresh session.[/]")


async def _refresh_map(app: "NgramApp") -> None:
    """Refresh the repository map in background after changes."""
    import asyncio
    from ..repo_overview import generate_and_save

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: generate_and_save(app.target_dir, output_format="md")
        )
    except Exception:
        pass  # Silent failure - map refresh is non-critical
