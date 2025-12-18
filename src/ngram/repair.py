"""
Repair command for ngram CLI.

Automatically fixes project health issues by spawning Claude Code agents.
Each agent follows the protocol: read docs, fix issue, update SYNC.
"""

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any, Optional

from .doctor import run_doctor, load_doctor_config, DoctorIssue
from .repair_instructions import get_issue_instructions
from .repair_report import generate_llm_report, generate_final_report
from .repair_core import (
    ISSUE_SYMBOLS,
    ISSUE_DESCRIPTIONS,
    ISSUE_PRIORITY,
    AGENT_SYMBOLS,
    DEPTH_LINKS,
    DEPTH_DOCS,
    DEPTH_FULL,
    AGENT_SYSTEM_PROMPT,
    RepairResult,
    ArbitrageDecision,
    get_learnings_content,
    get_issue_symbol,
    get_issue_action_parts,
    get_issue_action,
    get_depth_types,
    build_agent_prompt,
    parse_decisions_from_output,
)


# ANSI color codes (CLI-specific)
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    GRAY = "\033[38;5;245m"

    # Agent colors (cycle through for parallel agents)
    AGENT_COLORS = [
        "\033[38;5;39m",   # Blue
        "\033[38;5;208m",  # Orange
        "\033[38;5;42m",   # Green
        "\033[38;5;201m",  # Pink
        "\033[38;5;226m",  # Yellow
        "\033[38;5;51m",   # Cyan
        "\033[38;5;196m",  # Red
        "\033[38;5;141m",  # Purple
    ]

    # Status colors
    SUCCESS = "\033[38;5;42m"   # Green
    FAILURE = "\033[38;5;196m"  # Red
    WARNING = "\033[38;5;208m"  # Orange
    INFO = "\033[38;5;39m"      # Blue

    # Special colors
    VIOLET = "\033[38;5;183m"   # Light violet for user messages
    HEALTH = "\033[38;5;87m"    # Cyan for health score
    CRITICAL = "\033[38;5;196m" # Red for critical count
    WARN_COUNT = "\033[38;5;214m"  # Orange-yellow for warning count


# CLI-specific helper functions (using imported constants from repair_core)
# NOTE: These are intentionally simple one-line utility functions.
# They provide semantic meaning to common operations (color lookup, symbol lookup, text wrapping).
# Short body does not mean incomplete - these are complete implementations.

def get_severity_color(severity: str) -> str:
    """Get color code for severity level."""
    return {
        "critical": Colors.FAILURE,
        "warning": Colors.WARNING,
        "info": Colors.DIM,
    }.get(severity, Colors.RESET)


def get_agent_color(agent_id: int) -> str:
    """Get color code for an agent by cycling through available colors."""
    return Colors.AGENT_COLORS[agent_id % len(Colors.AGENT_COLORS)]


def get_agent_symbol(agent_id: int) -> str:
    """Get visual symbol for an agent by cycling through available symbols."""
    return AGENT_SYMBOLS[agent_id % len(AGENT_SYMBOLS)]


def color(text: str, color_code: str) -> str:
    """Wrap text in ANSI color codes with automatic reset."""
    return f"{color_code}{text}{Colors.RESET}"


def load_github_issue_mapping(target_dir: Path) -> Dict[str, int]:
    """Load GitHub issue mapping from health report or tracking file."""
    mapping = {}

    # Try to load from a tracking file first
    tracking_path = target_dir / ".ngram" / "state" / "github_issues.json"
    if tracking_path.exists():
        try:
            import json
            with open(tracking_path) as f:
                data = json.load(f)
                return {k: v["number"] for k, v in data.items()}
        except Exception:
            pass

    return mapping


def save_github_issue_mapping(target_dir: Path, mapping: Dict[str, Dict[str, Any]]) -> None:
    """Save GitHub issue mapping to tracking file."""
    tracking_path = target_dir / ".ngram" / "state" / "github_issues.json"
    if tracking_path.parent.exists():
        import json
        with open(tracking_path, "w") as f:
            json.dump(mapping, f, indent=2)


# Core repair logic (DEPTH_*, RepairResult, ArbitrageDecision, AGENT_SYSTEM_PROMPT,
# build_agent_prompt, parse_decisions_from_output, etc.) imported from repair_core.py


def spawn_repair_agent(
    issue: DoctorIssue,
    target_dir: Path,
    dry_run: bool = False,
    github_issue_number: Optional[int] = None,
    arbitrage_decisions: Optional[List['ArbitrageDecision']] = None,
    agent_symbol: str = "→",
) -> RepairResult:
    """Spawn a Claude Code agent to fix a single issue."""

    instructions = get_issue_instructions(issue, target_dir)

    # For ARBITRAGE issues, inject the human decisions into the prompt
    if issue.issue_type == "ARBITRAGE" and arbitrage_decisions:
        decisions_text = "\n".join(
            f"- **{d.conflict_title}**: {d.decision}"
            for d in arbitrage_decisions if not d.passed
        )
        instructions["prompt"] = instructions["prompt"].replace(
            "{arbitrage_decisions}",
            decisions_text or "(No decisions provided)"
        )
    elif issue.issue_type == "ARBITRAGE":
        instructions["prompt"] = instructions["prompt"].replace(
            "{arbitrage_decisions}",
            "(No decisions provided - skip this issue)"
        )

    prompt = build_agent_prompt(issue, instructions, target_dir, github_issue_number)

    if dry_run:
        print(f"\n{'='*60}")
        print(f"DRY RUN: Would spawn agent for {issue.issue_type}")
        print(f"Target: {issue.path}")
        print(f"VIEW: {instructions['view']}")
        if github_issue_number:
            print(f"GitHub Issue: #{github_issue_number}")
        print(f"{'='*60}")
        print(prompt)
        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=True,
            agent_output="[DRY RUN]",
            duration_seconds=0,
        )

    # Build system prompt with learnings
    system_prompt = AGENT_SYSTEM_PROMPT + get_learnings_content(target_dir)

    # Build the claude command
    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--append-system-prompt", system_prompt,
        "--verbose",
        "--output-format", "stream-json",
    ]

    start_time = time.time()
    output_lines = []
    text_output = []  # Human-readable text only

    try:
        # Run claude with streaming output
        process = subprocess.Popen(
            cmd,
            cwd=target_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,  # Line buffered
        )

        # Stream output - parse JSON and extract text
        for line in process.stdout:
            output_lines.append(line)
            line = line.strip()
            if not line:
                continue

            # Try to parse JSON and extract readable content
            try:
                data = json.loads(line)
                msg_type = data.get("type", "")

                # Extract assistant text messages
                if msg_type == "assistant":
                    message = data.get("message", {})
                    for content in message.get("content", []):
                        if content.get("type") == "text":
                            text = content.get("text", "")
                            if text:
                                text_output.append(text)
                                # Show full text output, indented
                                for line in text.split('\n'):
                                    stripped = line.strip()
                                    if stripped:
                                        # Highlight DECISION items
                                        if '### DECISION:' in stripped or '### Decision:' in stripped:
                                            decision_name = stripped.split(':', 1)[1].strip() if ':' in stripped else ''
                                            sys.stdout.write(f"    {Colors.BOLD}{agent_symbol} ⚡ DECISION: {decision_name}{Colors.RESET}\n")
                                        elif stripped.lower().startswith('- resolution:') or stripped.lower().startswith('resolution:'):
                                            resolution = stripped.split(':', 1)[1].strip()
                                            sys.stdout.write(f"    {agent_symbol} {Colors.SUCCESS}→ {resolution}{Colors.RESET}\n")
                                        else:
                                            sys.stdout.write(f"    {agent_symbol} {line}\n")
                                        sys.stdout.flush()
                        elif content.get("type") == "tool_use":
                            tool = content.get("name", "unknown")
                            tool_input = content.get("input", {})
                            # Extract file path for file operations
                            file_path = tool_input.get("file_path") or tool_input.get("path") or ""
                            if file_path and tool in ("Read", "Write", "Edit", "Glob", "Grep"):
                                # Shorten path for display
                                short_path = file_path.split("/")[-2:] if "/" in file_path else [file_path]
                                path_display = "/".join(short_path)
                                sys.stdout.write(f"    {agent_symbol} {Colors.DIM}{Colors.ITALIC}📎 {tool} {path_display}{Colors.RESET}\n")
                            else:
                                sys.stdout.write(f"    {agent_symbol} {Colors.DIM}{Colors.ITALIC}📎 {tool}{Colors.RESET}\n")
                            sys.stdout.flush()

            except json.JSONDecodeError:
                # Not JSON, might be plain text
                if line and not line.startswith("{"):
                    sys.stdout.write(f"    {agent_symbol} {line}\n")
                    sys.stdout.flush()

        process.wait(timeout=600)
        duration = time.time() - start_time
        output = "".join(output_lines)
        readable_output = "\n".join(text_output)

        # Check for success markers in readable text output (not raw JSON)
        success = "REPAIR COMPLETE" in readable_output and "REPAIR FAILED" not in readable_output

        # Parse decisions made by the agent
        decisions = parse_decisions_from_output(readable_output)

        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=success,
            agent_output=output,
            duration_seconds=duration,
            error=None if process.returncode == 0 else f"Exit code: {process.returncode}",
            decisions_made=decisions if decisions else None,
        )

    except subprocess.TimeoutExpired:
        process.kill()
        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=False,
            agent_output="".join(output_lines),
            duration_seconds=600,
            error="Agent timed out after 10 minutes",
        )
    except Exception as e:
        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=False,
            agent_output="".join(output_lines),
            duration_seconds=time.time() - start_time,
            error=str(e),
        )


def print_progress_bar(current: int, total: int, width: int = 40, status: str = "") -> None:
    """Print a progress bar."""
    percent = current / total if total > 0 else 0
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    sys.stdout.write(f"\r  [{bar}] {current}/{total} {status}")
    sys.stdout.flush()


# get_depth_types and ArbitrageDecision imported from repair_core.py

# Global state for manager input
manager_input_queue = []
manager_input_lock = Lock()
stop_input_listener = False


def input_listener_thread():
    """Background thread that listens for user input during repairs."""
    global stop_input_listener
    import select
    import sys

    while not stop_input_listener:
        try:
            # Check if input is available (non-blocking on Unix)
            if sys.platform != 'win32':
                readable, _, _ = select.select([sys.stdin], [], [], 0.5)
                if readable:
                    line = sys.stdin.readline().strip()
                    if line:
                        with manager_input_lock:
                            manager_input_queue.append(line)
            else:
                # Windows fallback - just sleep
                time.sleep(0.5)
        except Exception:
            break


def spawn_manager_agent(
    user_input: str,
    recent_logs: List[str],
    target_dir: Path,
) -> Optional[str]:
    """Spawn the manager agent with user input and recent logs."""

    manager_dir = target_dir / ".ngram" / "agents" / "manager"
    if not manager_dir.exists():
        print(f"  {Colors.DIM}(Manager agent not found at {manager_dir}){Colors.RESET}")
        return None

    # Build context with recent logs
    logs_context = "\n".join(recent_logs[-50:]) if recent_logs else "(No recent logs)"

    prompt = f"""## Human Input During Repair

The human has provided input during an active repair session:

**Human says:** {user_input}

## Recent Repair Logs

```
{logs_context}
```

## Your Task

Respond to the human's input. If they're:
- Asking a question → Answer it
- Providing context → Acknowledge and explain how it helps
- Making a decision → Record it as a DECISION
- Redirecting → Acknowledge the new direction

Keep your response concise - repairs are in progress.
"""

    try:
        cmd = [
            "claude",
            "--continue",
            "-p", prompt,
            "--output-format", "text",
        ]

        print()
        print(f"{Colors.BOLD}🎛️  Manager Agent{Colors.RESET}")
        print(f"{'─'*40}")

        # Stream output instead of capturing (faster feedback)
        process = subprocess.Popen(
            cmd,
            cwd=manager_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        response_lines = []
        try:
            # Read output line by line with timeout
            import select
            while True:
                # Check if process finished
                if process.poll() is not None:
                    break

                # Check for output with short timeout
                readable, _, _ = select.select([process.stdout], [], [], 0.1)
                if readable:
                    line = process.stdout.readline()
                    if line:
                        print(line, end='', flush=True)
                        response_lines.append(line)

            # Get any remaining output
            remaining = process.stdout.read()
            if remaining:
                print(remaining, end='', flush=True)
                response_lines.append(remaining)

            process.wait(timeout=30)  # Wait for process to finish

        except subprocess.TimeoutExpired:
            process.kill()
            print(f"  {Colors.DIM}(Manager timed out){Colors.RESET}")

        print(f"{'─'*40}")
        return ''.join(response_lines).strip() if response_lines else None

    except Exception as e:
        print(f"  {Colors.DIM}(Manager error: {e}){Colors.RESET}")

    return None


def check_for_manager_input(recent_logs: List[str], target_dir: Path) -> Optional[str]:
    """Check if user has provided input, spawn manager if so."""
    global manager_input_queue

    with manager_input_lock:
        if manager_input_queue:
            user_input = manager_input_queue.pop(0)
            # Echo user input in violet
            print(f"\n{Colors.VIOLET}💬 You: {user_input}{Colors.RESET}")
            return spawn_manager_agent(user_input, recent_logs, target_dir)

    return None


def resolve_arbitrage_interactive(issue: DoctorIssue) -> List[ArbitrageDecision]:
    """Interactively resolve ARBITRAGE conflicts with user input."""
    decisions = []
    items = issue.details.get("items", [])

    print()
    print(f"{Colors.BOLD}⚖️  ARBITRAGE: Conflicts need your decision{Colors.RESET}")
    print(f"   File: {issue.path}")
    print(f"{'─'*60}")

    for i, item in enumerate(items, 1):
        title = item.get("title", "Unknown conflict")
        details = item.get("details", [])

        print()
        print(f"{Colors.BOLD}Conflict {i}/{len(items)}: {title}{Colors.RESET}")
        print()

        # Parse details into context, options, pros/cons, recommendation, and context-needed fields
        options = []
        recommendation = None
        context_lines = []
        trying_to = None
        need_to_know = None
        context_needed = None
        would_help = None

        for detail in details:
            stripped = detail.strip()
            if stripped.startswith("(") and ")" in stripped[:4]:
                # Option: (A) text or (1) text
                options.append(stripped)
            elif stripped.lower().startswith("pro:"):
                # Pro for previous option
                if options:
                    options[-1] += f"\n      {Colors.SUCCESS}✓ {stripped[4:].strip()}{Colors.RESET}"
            elif stripped.lower().startswith("con:"):
                # Con for previous option
                if options:
                    options[-1] += f"\n      {Colors.FAILURE}✗ {stripped[4:].strip()}{Colors.RESET}"
            elif "**recommendation" in stripped.lower() or stripped.lower().startswith("recommendation:"):
                # Agent's recommendation
                recommendation = stripped.replace("**Recommendation:**", "").replace("**recommendation:**", "").strip()
            elif stripped.lower().startswith("trying to:"):
                trying_to = stripped.split(":", 1)[1].strip()
            elif stripped.lower().startswith("need to know:"):
                need_to_know = stripped.split(":", 1)[1].strip()
            elif stripped.lower().startswith("context needed:"):
                context_needed = stripped.split(":", 1)[1].strip()
            elif stripped.lower().startswith("this would help"):
                would_help = stripped.split(":", 1)[1].strip() if ":" in stripped else stripped
            else:
                context_lines.append(stripped)

        # Determine if this is a "context needed" type ARBITRAGE
        is_context_type = trying_to or need_to_know or context_needed

        if is_context_type:
            # Show context-needed format
            if trying_to:
                print(f"  {Colors.BOLD}🎯 Trying to:{Colors.RESET} {trying_to}")
            if need_to_know:
                print(f"  {Colors.BOLD}❓ Need to know:{Colors.RESET} {need_to_know}")
            if context_needed:
                print(f"  {Colors.DIM}   {context_needed}{Colors.RESET}")
            if would_help:
                print(f"  {Colors.BOLD}💡 This would help:{Colors.RESET} {would_help}")
            # Show any additional context
            for line in context_lines:
                print(f"  {Colors.DIM}{line}{Colors.RESET}")
        else:
            # Show choice-type format - context first
            for line in context_lines:
                print(f"  {Colors.DIM}{line}{Colors.RESET}")

        # Show options with pros/cons
        if options:
            print()
            print(f"  {Colors.BOLD}Options:{Colors.RESET}")
            for opt in options:
                for line in opt.split('\n'):
                    print(f"    {line}")

        # Show recommendation
        if recommendation:
            print()
            print(f"  {Colors.BOLD}💡 Agent recommends:{Colors.RESET} {recommendation}")

        print()
        print(f"  Enter your decision (or 'pass' to skip):")
        print(f"  > ", end="")

        try:
            user_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            user_input = "pass"

        if user_input.lower() == "pass" or not user_input:
            decisions.append(ArbitrageDecision(
                conflict_title=title,
                decision="",
                passed=True
            ))
            print(f"  {Colors.DIM}Skipped{Colors.RESET}")
        else:
            decisions.append(ArbitrageDecision(
                conflict_title=title,
                decision=user_input,
                passed=False
            ))
            print(f"  {Colors.SUCCESS}Decision recorded{Colors.RESET}")

    print(f"{'─'*60}")
    resolved = len([d for d in decisions if not d.passed])
    print(f"  {resolved}/{len(decisions)} conflicts decided")
    print()

    return decisions


def repair_command(
    target_dir: Path,
    max_issues: Optional[int] = None,
    issue_types: Optional[List[str]] = None,
    depth: str = "docs",
    dry_run: bool = False,
    parallel: int = 5,
) -> int:
    """Run the repair command."""

    depth_labels = {
        "links": "Links only (refs, mappings)",
        "docs": "Links + Documentation",
        "full": "Full (links + docs + code)",
    }

    print(f"🔧 ngram Repair")
    print(f"{'='*60}")
    print(f"  Depth: {depth_labels.get(depth, depth)}")
    print(f"  Parallel agents: {parallel}")
    print()

    # Step 1: Run doctor to get issues
    print(f"{Colors.BOLD}📋 Step 1: Analyzing project health...{Colors.RESET}")
    print()
    config = load_doctor_config(target_dir)
    before_results = run_doctor(target_dir, config)

    print(f"  {Colors.HEALTH}Health Score: {before_results['score']}/100{Colors.RESET}")
    print(f"  {Colors.CRITICAL}Critical: {before_results['summary']['critical']}{Colors.RESET}")
    print(f"  {Colors.WARN_COUNT}Warnings: {before_results['summary']['warning']}{Colors.RESET}")
    print()

    # Collect issues to fix
    all_issues: List[DoctorIssue] = []
    all_issues.extend(before_results["issues"]["critical"])
    all_issues.extend(before_results["issues"]["warning"])
    # Include info-level issues for links depth (safe fixes)
    if depth == "links":
        all_issues.extend(before_results["issues"]["info"])

    # Filter by depth level
    allowed_types = get_depth_types(depth)
    all_issues = [i for i in all_issues if i.issue_type in allowed_types]

    # Filter by explicit type if specified
    if issue_types:
        all_issues = [i for i in all_issues if i.issue_type in issue_types]

    # Sort by priority (foundation issues first, then by impact)
    all_issues.sort(key=lambda i: ISSUE_PRIORITY.get(i.issue_type, 99))

    if not all_issues:
        print(f"✅ No issues to repair at depth '{depth}'!")
        print()

        # Count total issues at all depths for context
        total_critical = before_results['summary']['critical']
        total_warnings = before_results['summary']['warning']
        has_other_issues = total_critical > 0 or total_warnings > 0

        # Provide guidance based on current depth
        if depth == "links":
            print(f"  {Colors.DIM}All link/reference issues are resolved.{Colors.RESET}")
            if has_other_issues:
                print(f"  {Colors.DIM}There are {total_critical} critical + {total_warnings} warning issues at deeper depths.{Colors.RESET}")
            print(f"  {Colors.DIM}To check documentation issues: {Colors.RESET}{Colors.BOLD}ngram repair --depth docs{Colors.RESET}")
            print(f"  {Colors.DIM}To check all issues:           {Colors.RESET}{Colors.BOLD}ngram repair --depth full{Colors.RESET}")
        elif depth == "docs":
            print(f"  {Colors.DIM}All documentation issues are resolved.{Colors.RESET}")
            if has_other_issues:
                print(f"  {Colors.DIM}There are {total_critical} critical + {total_warnings} warning issues at 'full' depth.{Colors.RESET}")
            print(f"  {Colors.DIM}To check implementation issues: {Colors.RESET}{Colors.BOLD}ngram repair --depth full{Colors.RESET}")
        else:  # full
            print(f"  {Colors.DIM}Project is healthy at all depths!{Colors.RESET}")
            print(f"  {Colors.DIM}Run {Colors.RESET}{Colors.BOLD}ngram doctor{Colors.RESET}{Colors.DIM} to see the full health report.{Colors.RESET}")
        print()
        return 0

    # Limit number of issues if specified
    if max_issues is not None:
        issues_to_fix = all_issues[:max_issues]
    else:
        issues_to_fix = all_issues

    # Step 2: Show the repair plan
    print(f"{Colors.BOLD}📝 Step 2: Repair Plan{Colors.RESET}")
    print()

    print(f"  {color(str(len(issues_to_fix)), Colors.BOLD)} issues to fix:")
    if max_issues is not None and len(all_issues) > max_issues:
        print(f"  {color(f'(showing first {max_issues} of {len(all_issues)})', Colors.DIM)}")
    print()

    # Show each issue with problem description and action
    for i, issue in enumerate(issues_to_fix[:15]):
        agent_sym = get_agent_symbol(i)
        agent_clr = get_agent_color(i)
        prefix, suffix = get_issue_action_parts(issue.issue_type)
        sev_color = get_severity_color(issue.severity)

        # Format: "No documentation mapping (red): 🥷 will add docs for `path`"
        msg = color(issue.message, sev_color)
        action = f"{Colors.GRAY}{Colors.ITALIC}{prefix}{Colors.RESET}"
        path_fmt = f"`{issue.path}`"
        suffix_fmt = f" {Colors.GRAY}{Colors.ITALIC}{suffix}{Colors.RESET}" if suffix else ""

        print(f"    {i+1}. {msg}: {color(agent_sym, agent_clr)} {action} {path_fmt}{suffix_fmt}")

    if len(issues_to_fix) > 15:
        print(f"    {color(f'   ... and {len(issues_to_fix) - 15} more', Colors.DIM)}")
    print()

    if dry_run:
        print("  [DRY RUN] Would spawn Claude Code agents for each issue above.")
        print()
        return 0

    print(f"{'='*60}")
    print()

    # Load GitHub issue mapping (if exists)
    github_mapping = load_github_issue_mapping(target_dir)
    if github_mapping:
        print(f"  GitHub issues found: {len(github_mapping)}")
        print()

    # Step 3: Execute repairs
    print(f"{Colors.BOLD}🔨 Step 3: Executing repairs...{Colors.RESET}")
    print(f"  {Colors.DIM}(Type anytime to invoke manager agent){Colors.RESET}")
    print(f"  {Colors.DIM}{'─' * 50}{Colors.RESET}")
    print()

    # Start input listener for manager agent
    global stop_input_listener, manager_input_queue
    stop_input_listener = False
    manager_input_queue = []
    recent_logs: List[str] = []

    import threading
    listener = threading.Thread(target=input_listener_thread, daemon=True)
    listener.start()

    repair_results: List[RepairResult] = []
    print_lock = Lock()
    completed_count = [0]  # Use list to allow modification in nested function
    manager_responses: List[str] = []  # Track manager responses for report

    def run_repair(issue_tuple, arbitrage_decisions=None):
        """Run a single repair in a thread."""
        idx, issue = issue_tuple
        github_issue_num = github_mapping.get(issue.path)

        # Get agent and issue visual identifiers
        agent_clr = get_agent_color(idx - 1)
        agent_sym = get_agent_symbol(idx - 1)
        prefix, suffix = get_issue_action_parts(issue.issue_type)
        sev_color = get_severity_color(issue.severity)

        with print_lock:
            agent_tag = color(agent_sym, agent_clr)
            msg = color(issue.message, sev_color)
            action = f"{Colors.GRAY}{Colors.ITALIC}{prefix}{Colors.RESET}"
            path_fmt = f"`{issue.path}`"
            suffix_fmt = f" {Colors.GRAY}{Colors.ITALIC}{suffix}{Colors.RESET}" if suffix else ""
            print(f"  {msg}: {agent_tag} {action} {path_fmt}{suffix_fmt}")

        result = spawn_repair_agent(
            issue,
            target_dir,
            dry_run=False,
            github_issue_number=github_issue_num,
            arbitrage_decisions=arbitrage_decisions,
            agent_symbol=agent_sym,
        )

        with print_lock:
            completed_count[0] += 1
            agent_tag = color(agent_sym, agent_clr)
            if result.success:
                print(f"  {agent_tag} {color('✓', Colors.SUCCESS)} finished {issue.path} ({result.duration_seconds:.0f}s)")
            else:
                print(f"  {agent_tag} {color('✗', Colors.FAILURE)} failed on {issue.path}: {result.error or 'unknown'}")

        return result

    # Separate special issues (need interactive input) from others
    arbitrage_issues = [(i, iss) for i, iss in enumerate(issues_to_fix, 1) if iss.issue_type == "ARBITRAGE"]
    suggestion_issues = [(i, iss) for i, iss in enumerate(issues_to_fix, 1) if iss.issue_type == "SUGGESTION"]
    other_issues = [(i, iss) for i, iss in enumerate(issues_to_fix, 1)
                    if iss.issue_type not in ("ARBITRAGE", "SUGGESTION")]

    # Handle ARBITRAGE issues first (interactive, sequential)
    if arbitrage_issues:
        print(f"  {Colors.BOLD}⚖️ Resolving {len(arbitrage_issues)} conflict(s) first...{Colors.RESET}")
        print()

        for idx, issue in arbitrage_issues:
            # Interactive prompt
            decisions = resolve_arbitrage_interactive(issue)

            # Check if any decisions were made (not all passed)
            has_decisions = any(not d.passed for d in decisions)

            if has_decisions:
                issue_emoji, _ = get_issue_symbol(issue.issue_type)
                github_issue_num = github_mapping.get(issue.path)
                print(f"  {issue_emoji} Spawning agent to implement decisions...")

                result = spawn_repair_agent(
                    issue,
                    target_dir,
                    dry_run=False,
                    github_issue_number=github_issue_num,
                    arbitrage_decisions=decisions,
                )
                repair_results.append(result)

                if result.success:
                    print(f"\n  {color('✓ Complete', Colors.SUCCESS)} ({result.duration_seconds:.1f}s)")
                else:
                    print(f"\n  {color('✗ Failed', Colors.FAILURE)}: {result.error or 'Unknown error'}")
            else:
                print(f"  {Colors.DIM}All conflicts skipped, no agent spawned{Colors.RESET}")
                repair_results.append(RepairResult(
                    issue_type=issue.issue_type,
                    target_path=issue.path,
                    success=True,
                    agent_output="User passed all conflicts",
                    duration_seconds=0,
                ))

        print()

    # Handle SUGGESTION issues (interactive, ask user before spawning)
    accepted_suggestions = []
    if suggestion_issues:
        print(f"  {Colors.BOLD}💡 {len(suggestion_issues)} agent suggestion(s) found:{Colors.RESET}")
        print()

        for idx, issue in suggestion_issues:
            suggestion_text = issue.details.get("suggestion", issue.message)
            source_file = issue.details.get("source_file", issue.path)

            print(f"    {Colors.DIM}From: {source_file}{Colors.RESET}")
            print(f"    💡 {suggestion_text}")
            print()

            try:
                response = input(f"    {Colors.BOLD}Implement this? (y/n/q to quit): {Colors.RESET}").strip().lower()
            except (EOFError, KeyboardInterrupt):
                print("\n    Skipping remaining suggestions...")
                break

            if response == 'q':
                print("    Skipping remaining suggestions...")
                break
            elif response in ('y', 'yes'):
                accepted_suggestions.append((idx, issue))
                print(f"    {Colors.SUCCESS}✓ Accepted{Colors.RESET}")
            else:
                print(f"    {Colors.DIM}Skipped{Colors.RESET}")
            print()

        # Spawn agents for accepted suggestions
        if accepted_suggestions:
            print(f"  {Colors.BOLD}Implementing {len(accepted_suggestions)} accepted suggestion(s)...{Colors.RESET}")
            print()

            for idx, issue in accepted_suggestions:
                agent_sym = get_agent_symbol(idx - 1)
                agent_clr = get_agent_color(idx - 1)
                agent_tag = color(agent_sym, agent_clr)

                suggestion_text = issue.details.get("suggestion", issue.message)
                print(f"  {agent_tag} Implementing: {suggestion_text[:50]}...")

                github_issue_num = github_mapping.get(issue.path)
                result = spawn_repair_agent(
                    issue,
                    target_dir,
                    dry_run=False,
                    github_issue_number=github_issue_num,
                    agent_symbol=agent_sym,
                )
                repair_results.append(result)

                if result.success:
                    print(f"\n  {agent_tag} {color('✓ Complete', Colors.SUCCESS)} ({result.duration_seconds:.1f}s)")
                else:
                    print(f"\n  {agent_tag} {color('✗ Failed', Colors.FAILURE)}: {result.error or 'Unknown error'}")
                print()
        else:
            print(f"  {Colors.DIM}No suggestions accepted{Colors.RESET}")
            print()

    # Run remaining agents in parallel or sequentially
    if not other_issues:
        pass  # Only had ARBITRAGE issues
    elif parallel > 1:
        active_workers = min(parallel, len(other_issues))
        print(f"  Running {len(other_issues)} repairs with {active_workers} parallel agents...")
        print()

        with ThreadPoolExecutor(max_workers=parallel) as executor:
            futures = {
                executor.submit(run_repair, issue_tuple): issue_tuple[1]
                for issue_tuple in other_issues
            }

            for future in as_completed(futures):
                result = future.result()
                repair_results.append(result)

                # Log for manager context
                log_entry = f"[{result.issue_type}] {result.target_path}: {'SUCCESS' if result.success else 'FAILED'}"
                recent_logs.append(log_entry)

                # Check for manager input periodically
                manager_response = check_for_manager_input(recent_logs, target_dir)
                if manager_response:
                    manager_responses.append(manager_response)
    else:
        # Sequential execution with more verbose output
        for i, issue in other_issues:
            # Check for manager input between repairs
            manager_response = check_for_manager_input(recent_logs, target_dir)
            if manager_response:
                manager_responses.append(manager_response)
                if "STOP REPAIRS" in manager_response:
                    print(f"\n  {Colors.BOLD}Manager requested stop. Halting repairs.{Colors.RESET}")
                    break

            issue_emoji, issue_sym = get_issue_symbol(issue.issue_type)
            print_progress_bar(i - 1, len(issues_to_fix), status=f"Starting {issue.issue_type}...")
            print()

            github_issue_num = github_mapping.get(issue.path)
            github_info = f" (#{github_issue_num})" if github_issue_num else ""
            prefix, suffix = get_issue_action_parts(issue.issue_type)
            sev_color = get_severity_color(issue.severity)
            msg = color(issue.message, sev_color)
            action = f"{Colors.GRAY}{Colors.ITALIC}{prefix}{Colors.RESET}"
            path_fmt = f"`{issue.path}`"
            suffix_fmt = f" {Colors.GRAY}{Colors.ITALIC}{suffix}{Colors.RESET}" if suffix else ""
            print(f"\n  {issue_emoji} [{i}/{len(issues_to_fix)}] {msg}: {action} {path_fmt}{suffix_fmt}{github_info}")

            result = spawn_repair_agent(
                issue,
                target_dir,
                dry_run=False,
                github_issue_number=github_issue_num,
            )
            repair_results.append(result)

            # Log for manager context
            log_entry = f"[{issue.issue_type}] {issue.path}: {'SUCCESS' if result.success else 'FAILED'}"
            recent_logs.append(log_entry)

            if result.success:
                print(f"\n  {color('✓ Complete', Colors.SUCCESS)} ({result.duration_seconds:.1f}s)")
            else:
                print(f"\n  {color('✗ Failed', Colors.FAILURE)}: {result.error or 'Unknown error'}")

        print_progress_bar(len(issues_to_fix), len(issues_to_fix), status="Done!")

    # Stop the input listener
    stop_input_listener = True

    # Final check for manager input
    manager_response = check_for_manager_input(recent_logs, target_dir)
    if manager_response:
        manager_responses.append(manager_response)

    print("\n")

    # Step 4: Run doctor again
    print(f"{Colors.BOLD}📊 Step 4: Running final health check...{Colors.RESET}")
    after_results = run_doctor(target_dir, config)

    # Calculate and format score change
    score_change = after_results['score'] - before_results['score']
    if score_change > 0:
        change_str = f" {Colors.SUCCESS}(+{score_change}){Colors.RESET}"
    elif score_change < 0:
        change_str = f" {Colors.FAILURE}({score_change}){Colors.RESET}"
    else:
        change_str = f" {Colors.DIM}(±0){Colors.RESET}"

    print(f"  {Colors.HEALTH}Health Score: {after_results['score']}/100{Colors.RESET}{change_str}")
    print(f"  {Colors.CRITICAL}Critical: {after_results['summary']['critical']}{Colors.RESET}")
    print(f"  {Colors.WARN_COUNT}Warnings: {after_results['summary']['warning']}{Colors.RESET}")
    print()

    # Step 5: Generate report
    print(f"{Colors.BOLD}📄 Step 5: Generating report...{Colors.RESET}")

    # Try LLM-generated report first, fall back to template
    report = generate_llm_report(before_results, after_results, repair_results, target_dir)
    if report:
        print(f"  {Colors.DIM}(Generated by Claude){Colors.RESET}")
    else:
        report = generate_final_report(before_results, after_results, repair_results, target_dir)
        print(f"  {Colors.DIM}(Using template report){Colors.RESET}")

    # Save report
    report_path = target_dir / ".ngram" / "state" / "REPAIR_REPORT.md"
    if report_path.parent.exists():
        report_path.write_text(report)
        print(f"  Saved to {report_path.relative_to(target_dir)}")

    print()

    # Display report to CLI
    print(f"{'─'*60}")
    print(report)
    print(f"{'─'*60}")
    print()

    # Summary
    successful = len([r for r in repair_results if r.success])
    score_before = before_results['score']
    score_after = after_results['score']
    score_diff = score_after - score_before
    if score_diff > 0:
        score_change_fmt = f"{Colors.SUCCESS}(+{score_diff}){Colors.RESET}"
    elif score_diff < 0:
        score_change_fmt = f"{Colors.FAILURE}({score_diff}){Colors.RESET}"
    else:
        score_change_fmt = f"{Colors.DIM}(±0){Colors.RESET}"

    print(f"{'='*60}")
    print(f"✅ Repair Complete: {successful}/{len(repair_results)} successful")
    print(f"📈 {Colors.HEALTH}Health Score: {score_before} → {score_after}{Colors.RESET} {score_change_fmt}")
    print(f"{'='*60}")

    # Return exit code
    return 0 if successful == len(repair_results) else 1
