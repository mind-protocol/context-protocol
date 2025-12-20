# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""
ngram TUI - manager startup helpers.
"""

from __future__ import annotations

import asyncio
import json
import shutil
from typing import TYPE_CHECKING

from ..agent_cli import build_agent_command
from .widgets.manager_panel import ManagerPanel

if TYPE_CHECKING:
    from .app import NgramApp


def build_manager_overview_prompt() -> str:
    """Build the initial prompt for manager to provide project overview."""
    # Simple overview prompt - init tasks are handled by `ngram init`, not TUI launch
    return """Please read the following files to understand the project:

1. Read `docs/SYNC_Project_Repository_Map.md` - the project structure map
2. Read `.ngram/state/SYNC_Project_State.md` - current project state

Then provide a brief overview:
- Where the project currently stands
- Any active work or issues
- Suggested next steps

Keep it concise and actionable (2-3 paragraphs max)."""


async def show_static_overview(app: "NgramApp", manager: ManagerPanel) -> None:
    """Show static overview when the manager agent is not available."""
    manager = app.query_one("#manager-panel")

    # Read SYNC file directly
    sync_file = app.target_dir / ".ngram" / "state" / "SYNC_Project_State.md"
    if sync_file.exists():
        content = sync_file.read_text()
        # Extract key sections
        lines = content.split("\n")
        summary_lines = []
        in_section = False
        for line in lines[:50]:  # First 50 lines
            if line.startswith("## CURRENT STATE") or line.startswith("## ACTIVE WORK"):
                in_section = True
            elif line.startswith("## ") and in_section:
                break
            elif in_section:
                summary_lines.append(line)

        if summary_lines:
            manager.add_message("Project State:")
            manager.add_message("\n".join(summary_lines[:15]))
        else:
            manager.add_message("No project state available. Run /doctor to check health.")
    else:
        manager.add_message("No SYNC file found. Initialize with `ngram init` or check .ngram/ directory.")


async def start_manager_with_overview(app: "NgramApp", manager: ManagerPanel) -> None:
    """Start manager and prompt for project overview."""
    manager = app.query_one("#manager-panel")
    initial_prompt = build_manager_overview_prompt()

    # Run manager from its own directory to avoid conversation conflicts
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

    # Find GLOBAL_LEARNINGS.md
    learnings_file = app.target_dir / ".ngram" / "views" / "GLOBAL_LEARNINGS.md"
    system_prompt = ""
    if learnings_file.exists():
        if app.agent_provider == "claude":
            system_prompt = str(learnings_file)
        else:
            system_prompt = learnings_file.read_text()

    allowed_tools = "Bash(*) Read(*) Edit(*) Write(*) Glob(*) Grep(*) WebFetch(*) WebSearch(*) NotebookEdit(*) Task(*) TodoWrite(*)"
    continue_session = not app._manager_force_new_session
    # If there's no conversation history, do not attempt to resume a session.
    if not app.conversation.messages:
        continue_session = False
    app._manager_force_new_session = False

    # Show loading indicator with animation
    thinking_msg = manager.add_message("[dim].[/]")
    animation_task = asyncio.create_task(app._animate_loading(thinking_msg))

    try:
        # Attempt to run with --resume first
        # If it fails, retry without --resume
        tried_with_resume = False
        while True:
            agent_cmd = build_agent_command(
                app.agent_provider,
                prompt=initial_prompt,
                system_prompt=system_prompt,
                stream_json=True,  # Always request stream-json
                continue_session=continue_session,
                add_dir=app.target_dir,
                allowed_tools=allowed_tools if app.agent_provider == "claude" else None,
            )

            process = await asyncio.create_subprocess_exec(
                *agent_cmd.cmd,
                cwd=cwd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                stdin=asyncio.subprocess.PIPE if agent_cmd.stdin else None,
            )
            app._running_process = process

            stdin_data = (agent_cmd.stdin + "\n").encode() if agent_cmd.stdin else None
            try:
                stdout_data, stderr_data = await asyncio.wait_for(
                    process.communicate(input=stdin_data),
                    timeout=180.0,
                )
                # If successful, break the loop
                break
            except asyncio.TimeoutError as timeout_exc:
                process.kill()
                await process.wait()
                app.log_error(
                    "Manager startup with --resume timed out. Retrying without --resume "
                    f"(Error: {timeout_exc})."
                )
                # Re-raise the timeout to be caught by the generic Exception handler for retry logic
                raise timeout_exc
            except Exception as e:
                # Capture stderr before logging/raising
                process.kill()  # Ensure process is terminated before trying to get output if it's still running
                await process.wait()
                _, stderr_data_on_exception = await process.communicate()  # Get remaining output if any
                stderr_output_on_exception = (
                    stderr_data_on_exception.decode(errors="replace").strip()
                    if stderr_data_on_exception
                    else "(empty stderr)"
                )

                # If it failed and we tried with resume, retry without it
                if continue_session and not tried_with_resume:
                    error_message = (
                        "Manager startup with --resume failed "
                        f"(Python Error: {e}, CLI stderr: {stderr_output_on_exception}). "
                        "Retrying without --resume."
                    )
                    app.log_error(error_message)
                    continue_session = False  # Disable resume for the next attempt
                    tried_with_resume = True
                    # Loop will continue to retry without resume
                else:
                    # If already tried without resume, or if continue_session was false, re-raise the exception
                    final_error_message = (
                        "Manager startup failed after retry "
                        f"(Python Error: {e}, CLI stderr: {stderr_output_on_exception}). "
                        "Final attempt failed."
                    )
                    app.log_error(final_error_message)
                    raise RuntimeError(final_error_message) from e
            finally:
                app._running_process = None

        # Stop animation and remove loading indicator
        animation_task.cancel()
        thinking_msg.remove()

        response_parts = []
        stdout_str = stdout_data.decode(errors="replace")

        for line_str in stdout_str.split("\n"):
            line_str = line_str.strip()
            if not line_str:
                continue
            try:
                data = json.loads(line_str)
                if not isinstance(data, dict):
                    continue
                if data.get("type") == "assistant":
                    msg_data = data.get("message", {})
                    if not isinstance(msg_data, dict):
                        continue
                    for content in msg_data.get("content", []):
                        if not isinstance(content, dict):
                            continue
                        if content.get("type") == "thinking":
                            thinking = content.get("thinking", "")
                            if thinking:
                                # Add thinking as collapsible
                                manager.add_thinking(thinking)
                        elif content.get("type") == "tool_use":
                            # Display tool call
                            tool_name = content.get("name", "unknown")
                            tool_input = content.get("input", {})
                            manager.add_tool_call(tool_name, tool_input)
                        elif content.get("type") == "text":
                            response_parts.append(content.get("text", ""))
                elif data.get("type") == "result":
                    result = data.get("result", "")
                    if result and not response_parts:
                        response_parts.append(result)
            except json.JSONDecodeError:
                # Not JSON, treat as plain text if it's the first part of output
                if not response_parts and not thinking_msg.is_visible:
                    response_parts.append(line_str)

        if stderr_data:
            stderr_text = stderr_data.decode(errors="replace").strip()
            if stderr_text:
                app.log_error(f"Manager stderr: {stderr_text[:500]}")

        if response_parts:
            full_response = "".join(response_parts)
            manager.add_message(full_response)
            app._llm_conversation_started = True
            app.notify_manager_response()

            # Detect commands and show interactive options
            from .commands_agent import _detect_commands
            detected = _detect_commands(full_response)
            if detected:
                app._pending_commands = detected
                manager.add_message("")
                manager.add_message("[bold]Suggested commands:[/]")
                for i, cmd in enumerate(detected[:5], 1):
                    manager.add_message(f"  [cyan]{i}.[/] {cmd}")
                manager.add_message("[dim]Type a number to run, or continue chatting[/]")
        else:
            await show_static_overview(app, manager)

    except Exception as e:
        animation_task.cancel()
        thinking_msg.remove()
        app.log_error(f"Manager startup failed: {e}")
        await show_static_overview(app, manager)
