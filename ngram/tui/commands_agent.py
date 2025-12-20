# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""
Helpers for running manager-agent messages in the TUI.
"""

from typing import TYPE_CHECKING
import re

if TYPE_CHECKING:
    from .app import NgramApp


def _detect_commands(text: str) -> list[str]:
    """Detect runnable commands in text."""
    commands = []

    # Detect ngram subcommands
    ngram_subs = r'(?:doctor|repair|sync|init|validate|context|prompt|solve-markers)'
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
            """Update widget, throttled to avoid overwhelming UI."""
            import time
            now = time.time()
            # Only update every 200ms to keep UI responsive
            if now - last_update_time[0] > 0.2:
                content = "".join(response_parts)
                # Stop animation on first content update
                stop_animation["flag"] = True
                try:
                    result = response_widget.update(content)
                    if inspect.isawaitable(result):
                        asyncio.create_task(result)
                    last_update_time[0] = now
                except Exception as e:
                    app.log_error(f"Widget update failed: {e}")

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


def _build_review_prompt(agent, result, output_tail: str) -> str:
    """Build prompt for manager to review completed agent."""
    status = "SUCCESS" if result.success else f"FAILED: {result.error or 'unknown'}"
    return f"""Agent {agent.symbol} completed repair task.

Issue: {agent.issue_type}
Target: {agent.target_path}
Duration: {result.duration_seconds:.1f}s
Status: {status}

Please review this repair:
1. Identify commits made by this agent - check `git log --oneline -10` and look for recent commits related to {agent.issue_type} or {agent.target_path}
2. For each relevant commit, run `git show <commit> --stat` to see the changes
3. If no commits were made, check `git diff` for uncommitted changes
4. Summarize what was changed and why
5. Assess the quality of the fix

Agent output (last 2000 chars):
```
{output_tail}
```"""


async def _run_manager_review(app: "NgramApp", prompt: str, agent_info: dict = None) -> None:
    """Run manager review in background, display result and save to log."""
    from datetime import datetime

    manager = app.query_one("#manager-panel")

    # Add separator and review header
    manager.add_message("")
    manager.add_message("[dim]--- Agent Review ---[/]")

    # Create response widget for streaming
    response_widget = manager.add_message("[dim]Reviewing...[/]")
    stop_animation = {"flag": False}

    # Run with --continue to maintain session
    await _run_agent_message(app, prompt, response_widget, stop_animation)

    # Save review to repair log
    try:
        review_content = response_widget.renderable if hasattr(response_widget, 'renderable') else str(response_widget)
        # Clean up rich markup for plain text
        clean_review = str(review_content).replace("[dim italic]", "").replace("[/]", "").replace("[dim]", "")

        log_dir = app.target_dir / ".ngram" / "repairs"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Use session date for log file
        today = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"reviews_{today}.md"

        timestamp = datetime.now().strftime("%H:%M:%S")
        agent_symbol = agent_info.get("symbol", "?") if agent_info else "?"
        issue_type = agent_info.get("issue_type", "unknown") if agent_info else "unknown"
        target = agent_info.get("target", "") if agent_info else ""

        entry = f"\n## {timestamp} - {agent_symbol} {issue_type}\n\n**Target:** {target}\n\n{clean_review}\n\n---\n"

        with open(log_file, "a") as f:
            f.write(entry)
    except Exception:
        pass  # Don't fail on logging errors
