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
import re


def _truncate_thinking(text: str, max_lines: int = 3) -> str:
    """Truncate thinking text to approximately max_lines with ellipsis."""
    lines = text.split('\n')
    if len(lines) <= max_lines:
        return text
    truncated = '\n'.join(lines[:max_lines])
    return f"{truncated}..."


def _detect_commands(text: str) -> list[str]:
    """Detect runnable commands in text."""
    commands = []

    # ngram subcommands we know about
    ngram_subs = r'(?:doctor|repair|sync|init|validate|context|prompt)'
    # Other CLI tools
    other_cmds = r'(?:python|pip|npm|git|pytest|uv|make|cargo|go)'

    # Pattern 1: `ngram <subcommand> [args]` in backticks
    backtick_ngram = re.findall(rf'`(ngram\s+{ngram_subs}[^`]*)`', text)
    commands.extend(backtick_ngram)

    # Pattern 2: `other-command args` in backticks
    backtick_other = re.findall(rf'`({other_cmds}\s+[^`]+)`', text)
    commands.extend(backtick_other)

    # Pattern 3: **ngram subcommand [args]** in bold
    bold_ngram = re.findall(rf'\*\*(ngram\s+{ngram_subs}[^*]*)\*\*', text)
    commands.extend(bold_ngram)

    # Pattern 4: "Run/Try/Use ngram <subcommand>" in plain text
    # Stops at common prose words or punctuation
    action_words = r'(?:[Rr]un|[Tt]ry|[Uu]se|[Ee]xecute)'
    stop_words = r'(?:\s+targeting|\s+to\s+(?:fix|check|address|get|see)|\s+for\s+|\s+first|\s*[.!?\n]|$)'
    plain_ngram = re.findall(rf'{action_words}\s+(ngram\s+{ngram_subs}(?:\s+[^\s.!?]+)*?){stop_words}', text)
    commands.extend(plain_ngram)

    # Pattern 5: Code block commands
    code_block = re.findall(rf'```(?:bash|shell|sh)?\n(ngram\s+{ngram_subs}[^\n`]*)', text)
    commands.extend(code_block)

    # Pattern 6: $ shell prompt style
    shell_cmds = re.findall(r'^\$\s+(ngram\s+\S+.*)$', text, re.MULTILINE)
    commands.extend(shell_cmds)

    # Pattern 7: Standalone command on its own line (no prose around it)
    standalone = re.findall(rf'^(ngram\s+{ngram_subs}(?:\s+[^\n]*?)?)$', text, re.MULTILINE)
    commands.extend(standalone)

    # Deduplicate and clean
    seen = set()
    unique = []
    for cmd in commands:
        cmd = cmd.strip()
        if cmd and cmd not in seen and len(cmd) < 150:
            seen.add(cmd)
            unique.append(cmd)

    return unique

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


def _build_codex_history_prompt(app: "NgramApp", message: str) -> str:
    """Build a lightweight conversation prompt for non-interactive agents."""
    history = app.conversation.get_recent(limit=20)
    lines = []
    for msg in history:
        role = msg.role.upper()
        lines.append(f"{role}: {msg.content}")
    if not history or history[-1].content != message:
        lines.append(f"USER: {message}")
    lines.append("ASSISTANT:")
    return "\n\n".join(lines)


async def _run_agent_message(app: "NgramApp", message: str, response_widget, stop_animation: dict) -> None:
    """Run agent subprocess in background."""
    import asyncio
    import inspect
    import json
    import shutil
    from ..agent_cli import build_agent_command

    manager = app.query_one("#manager-panel")

    # Run manager from its own directory to avoid conversation conflicts with agents
    manager_dir = app.target_dir / ".ngram" / "agents" / "manager"
    manager_dir.mkdir(parents=True, exist_ok=True)

    # Copy CLAUDE.md to manager directory if not present
    claude_md_src = app.target_dir / ".ngram" / "CLAUDE.md"
    claude_md_dst = manager_dir / "CLAUDE.md"
    manager_agents_src = manager_dir / "AGENTS.md"
    agents_md_src = app.target_dir / "AGENTS.md"
    agents_md_dst = manager_dir / "AGENTS.md"
    if claude_md_src.exists() and not claude_md_dst.exists():
        shutil.copy(claude_md_src, claude_md_dst)
    if manager_agents_src.exists():
        agents_md_dst.write_text(manager_agents_src.read_text())
    elif agents_md_src.exists():
        agents_md_dst.write_text(agents_md_src.read_text())
    elif claude_md_src.exists():
        agents_md_dst.write_text(claude_md_src.read_text())

    cwd = manager_dir

    # Find GLOBAL_LEARNINGS.md (not the template)
    learnings_file = app.target_dir / ".ngram" / "views" / "GLOBAL_LEARNINGS.md"
    if not learnings_file.exists():
        learnings_file = None

    async def run_agent(response_widget) -> tuple[bool, str]:
        """Run agent and return (success, response). Updates response_widget as content arrives."""
        system_prompt = ""
        if learnings_file:
            if app.agent_provider == "claude":
                system_prompt = str(learnings_file)
            else:
                system_prompt = learnings_file.read_text()

        prompt_text = message
        if app.agent_provider != "claude":
            prompt_text = _build_codex_history_prompt(app, message)

        allowed_tools = "Bash(*) Read(*) Edit(*) Write(*) Glob(*) Grep(*) WebFetch(*) WebSearch(*) NotebookEdit(*) Task(*) TodoWrite(*)"
        agent_cmd = build_agent_command(
            app.agent_provider,
            prompt=prompt_text,
            system_prompt=system_prompt,
            stream_json=(app.agent_provider == "claude"),
            continue_session=not app._manager_force_new_session,
            add_dir=app.target_dir,
            allowed_tools=allowed_tools if app.agent_provider == "claude" else None,
        )
        app._manager_force_new_session = False

        process = await asyncio.create_subprocess_exec(
            *agent_cmd.cmd,
            cwd=cwd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            stdin=asyncio.subprocess.PIPE if agent_cmd.stdin else None,
        )
        app._running_process = process
        if agent_cmd.stdin and process.stdin:
            process.stdin.write((agent_cmd.stdin + "\n").encode())
            await process.stdin.drain()
            process.stdin.close()

        response_parts = []
        buffer = ""
        stderr_chunks = []
        last_update_time = [0.0]  # Use list for mutability in nested func

        def throttled_update():
            """Update widget, throttled to avoid Textual selection bugs."""
            import time
            now = time.time()
            # Only update every 50ms to avoid overwhelming Textual
            if now - last_update_time[0] > 0.05:
                content = "".join(response_parts)
                # Stop animation on first content update
                stop_animation["flag"] = True
                try:
                    result = response_widget.update(content)
                    if inspect.isawaitable(result):
                        asyncio.create_task(result)
                    response_widget.refresh()  # Force visual refresh
                    last_update_time[0] = now
                except Exception as e:
                    app.log_error(f"Widget update failed: {e}, content_len={len(content)}")

        # Drain stderr in background to prevent buffer deadlock
        async def drain_stderr():
            if process.stderr:
                while True:
                    chunk = await process.stderr.read(4096)
                    if not chunk:
                        break
                    stderr_chunks.append(chunk.decode(errors='replace'))

        stderr_task = asyncio.create_task(drain_stderr())

        # Read stdout in chunks and process complete JSON lines
        if process.stdout and app.agent_provider == "claude":
            while True:
                try:
                    # Use wait_for with timeout to prevent indefinite hanging
                    chunk = await asyncio.wait_for(
                        process.stdout.read(65536),  # 64KB chunks
                        timeout=300.0  # 5 minute timeout per chunk
                    )
                    if not chunk:
                        break
                    buffer += chunk.decode()

                    # Process complete lines from buffer
                    while '\n' in buffer:
                        line_str, buffer = buffer.split('\n', 1)
                        line_str = line_str.strip()
                        if not line_str:
                            continue
                        try:
                            data = json.loads(line_str)
                            msg_type = data.get("type", "unknown")
                            # Handle init message (start of conversation)
                            if msg_type == "init":
                                # Could extract session info if needed
                                pass
                            # Handle system messages
                            elif msg_type == "system":
                                pass
                            # Handle assistant message format
                            elif msg_type == "assistant":
                                msg_data = data.get("message", {})
                                for content in msg_data.get("content", []):
                                    if content.get("type") == "thinking":
                                        # Display thinking in collapsible dropdown (before response widget)
                                        thinking = content.get("thinking", "")
                                        if thinking:
                                            manager.add_thinking(thinking, before=response_widget)
                                            # Add linebreak between thinking and response
                                            manager.add_message("", before=response_widget)
                                    elif content.get("type") == "tool_use":
                                        # Display tool call
                                        tool_name = content.get("name", "unknown")
                                        tool_input = content.get("input", {})
                                        manager.add_tool_call(tool_name, tool_input, before=response_widget)
                                    elif content.get("type") == "text":
                                        response_parts.append(content.get("text", ""))
                                        throttled_update()
                            # Handle streaming content blocks
                            elif data.get("type") == "content_block_delta":
                                delta = data.get("delta", {})
                                delta_type = delta.get("type", "unknown")
                                if delta_type == "text_delta":
                                    text = delta.get("text", "")
                                    if text:
                                        response_parts.append(text)
                                        throttled_update()
                                elif delta_type == "thinking_delta":
                                    # Streaming thinking - could accumulate but skip for now
                                    pass
                                elif delta_type not in ("thinking_delta", "text_delta"):
                                    app.log_error(f"Unknown delta type: {delta_type}, keys: {list(delta.keys())}")
                            # Handle content block start/stop (streaming markers)
                            elif msg_type in ("content_block_start", "content_block_stop",
                                            "message_start", "message_stop", "user"):
                                pass  # Markers only, no content (user echoes input back)
                            # Handle result format (final answer)
                            elif msg_type == "result":
                                result = data.get("result", "")
                                if result:
                                    if not response_parts:
                                        response_parts.append(str(result))
                                    # Stop animation FIRST before updating
                                    stop_animation["flag"] = True
                                    # Small delay to let animation task exit
                                    await asyncio.sleep(0.05)
                                    # Force final update
                                    final_content = "".join(response_parts)
                                    try:
                                        result = response_widget.update(final_content)
                                        if inspect.isawaitable(result):
                                            await result
                                        response_widget.refresh()  # Force visual refresh
                                    except Exception as e:
                                        app.log_error(f"Result widget update failed: {e}")
                            # Log unknown types for debugging
                            else:
                                app.log_error(f"Unknown stream type: {msg_type}")
                        except json.JSONDecodeError:
                            continue
                except asyncio.TimeoutError:
                    process.kill()
                    break
                except Exception:
                    break
        elif process.stdout:
            while True:
                try:
                    chunk = await asyncio.wait_for(
                        process.stdout.read(65536),
                        timeout=300.0,
                    )
                    if not chunk:
                        break
                    text = chunk.decode(errors="replace")
                    if text:
                        response_parts.append(text)
                        throttled_update()
                except asyncio.TimeoutError:
                    process.kill()
                    break
                except Exception:
                    break

        # Wait for process and stderr drain to complete
        await process.wait()
        await stderr_task
        app._running_process = None  # Clear process reference

        # Log if process failed or no output
        if process.returncode != 0 or not response_parts:
            stderr_output = "".join(stderr_chunks)[:500] if stderr_chunks else ""
            if stderr_output:
                app.log_error(f"Agent stderr: {stderr_output}")
            elif process.returncode != 0:
                app.log_error(f"Agent process exited with code {process.returncode}")

        return process.returncode == 0, "".join(response_parts)

    try:
        success, response = await run_agent(response_widget=response_widget)

        # Always stop animation after agent completes
        stop_animation["flag"] = True

        if response:
            # Final update with full response
            result = response_widget.update(response)
            if inspect.isawaitable(result):
                await result
            response_widget.refresh()
            app.notify_manager_response()

            # Save assistant response to history (strip markup for storage)
            clean_response = response.replace("[dim italic]", "").replace("[/]", "")
            app.conversation.add_message("assistant", clean_response)

            # Detect commands and show as interactive options
            detected = _detect_commands(clean_response)
            if detected:
                app._pending_commands = detected
                manager.add_message("")
                manager.add_message("[bold]Suggested commands:[/]")
                for i, cmd in enumerate(detected[:5], 1):  # Max 5 commands
                    manager.add_message(f"  [cyan]{i}.[/] {cmd}")
                manager.add_message("[dim]Type a number to run, or continue chatting[/]")
        else:
            # No response received, remove the widget
            response_widget.remove()

    except Exception as e:
        stop_animation["flag"] = True  # Stop animation on error too
        response_widget.remove()
        app.log_error(f"LLM failed: {e}")


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
    # Show all issues
    from ..repair_core import AGENT_SYMBOLS
    for i, issue in enumerate(all_issues):
        symbol = AGENT_SYMBOLS[i % len(AGENT_SYMBOLS)]
        manager.add_message(f"[dim]{symbol} {issue.issue_type}: {issue.path}[/]")
    # Log repair start
    issue_list = "\n".join(f"  - {i.issue_type}: {i.path}" for i in all_issues[:10])
    app.conversation.add_message("system", f"/repair\nFound {len(all_issues)} issues:\n{issue_list}")

    # Switch to agents tab and clear existing agent panels
    agent_container.switch_to_tab("agents-tab")
    agent_container._agent_panels.clear()

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

    # Create agent panel
    agent_container.add_agent(agent)

    # Get instructions
    instructions = get_issue_instructions(issue, app.target_dir)

    # Create throttled output callback for this agent
    # Use default args to capture values (not references) in closure
    output_buffer = []
    last_update = [0.0]
    pending_update = [False]  # Flag to prevent stacking updates

    async def on_output(
        text: str,
        aid=agent_id,
        buf=output_buffer,
        upd=last_update,
        agent_ref=agent,
        pending=pending_update
    ) -> None:
        """Handle agent output with throttling to prevent UI blocking."""
        import time
        # Skip empty or whitespace-only deltas
        if not text or not text.strip():
            return
        buf.append(text)
        # Also store in agent handle for later retrieval
        agent_ref.append_output(text)
        now = time.time()
        # Only schedule UI update every 250ms and if no update pending
        if now - upd[0] > 0.25 and not pending[0]:
            upd[0] = now
            pending[0] = True
            combined = "".join(buf)
            # Schedule update on next event loop iteration (non-blocking)
            def do_update(content=combined, agent_id=aid):
                try:
                    agent_container.update_agent(agent_id, content)
                except Exception:
                    pass
                finally:
                    pending[0] = False
            app.call_later(do_update)

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

        # Update panel status
        agent_container.set_agent_status(agent.id, agent.status)

        # Supervisor check
        await app.supervisor.on_agent_complete(agent)

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
        agent_container.set_agent_status(agent.id, "failed")
        manager.add_message(f"[red]{agent.symbol} Error: {e}[/]")
        app.conversation.add_message("system", f"Repair {agent.symbol} error: {e}")

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


async def handle_doctor(app: "NgramApp", args: str) -> None:
    """Run health check."""
    await app._run_doctor()


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
    """Display completed agent logs in collapsible panels."""
    from textual.widgets import Static, Markdown, Collapsible

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

    # Switch to agents tab and use its columns container
    agent_container.switch_to_tab("agents-tab")

    try:
        from textual.containers import Horizontal
        columns = app.query_one("#agents-columns", Horizontal)
        # Clear existing content
        for child in list(columns.children):
            child.remove()
        agent_container._agent_panels.clear()

        # Add collapsible for each completed agent
        for agent in completed_agents:
            status_color = "green" if agent.status == "completed" else "red"
            title = f"{agent.symbol} [{status_color}]{agent.status.upper()}[/] - {agent.issue_type}: {agent.target_path}"

            # Get output (last 100 lines to avoid huge logs)
            output = agent.get_output()
            lines = output.split('\n')
            if len(lines) > 100:
                output = '\n'.join(lines[-100:])
                output = f"[dim]... ({len(lines) - 100} lines truncated) ...[/]\n\n{output}"

            # Create collapsible with markdown output
            collapsible = Collapsible(
                Markdown(output if output else "[dim](no output)[/]"),
                title=title,
                collapsed=True,
            )
            await columns.mount(collapsible)
    except Exception as e:
        manager.add_message(f"[red]Logs error: {e}[/]")


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
