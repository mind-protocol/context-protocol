"""
Repair command for ADD Framework CLI.

Automatically fixes project health issues by spawning Claude Code agents.
Each agent follows the protocol: read docs, fix issue, update SYNC.
"""

import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any, Optional

from .doctor import run_doctor, load_doctor_config, DoctorIssue
from .repair_instructions import get_issue_instructions


# ANSI color codes
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


# Symbols and emojis per issue type
ISSUE_SYMBOLS = {
    "MONOLITH": ("🏔️", "▓"),
    "UNDOCUMENTED": ("📝", "□"),
    "STALE_SYNC": ("⏰", "◷"),
    "PLACEHOLDER": ("🔲", "▢"),
    "INCOMPLETE_CHAIN": ("🔗", "⛓"),
    "NO_DOCS_REF": ("📎", "⌘"),
    "BROKEN_IMPL_LINK": ("💔", "⚡"),
    "STUB_IMPL": ("🚧", "▲"),
    "INCOMPLETE_IMPL": ("🔧", "◐"),
    "UNDOC_IMPL": ("📋", "◎"),
    "LARGE_DOC_MODULE": ("📚", "▤"),
    "YAML_DRIFT": ("🗺️", "≋"),
    "MISSING_TESTS": ("🧪", "⚗"),
    "ORPHAN_DOCS": ("👻", "◌"),
    "STALE_IMPL": ("📉", "⇅"),
    "DOC_GAPS": ("🕳️", "○"),
    "ARBITRAGE": ("⚖️", "⚡"),
    "SUGGESTION": ("💡", "?"),
    "NEW_UNDOC_CODE": ("🆕", "+"),
    "COMPONENT_NO_STORIES": ("📖", "◇"),
    "HOOK_UNDOC": ("🪝", "⌒"),
    "DOC_DUPLICATION": ("📋", "≡"),
    "MAGIC_VALUES": ("🔢", "#"),
    "HARDCODED_CONFIG": ("⚙️", "∞"),
    "HARDCODED_SECRET": ("🔐", "!"),
    "LONG_PROMPT": ("📜", "¶"),
    "LONG_SQL": ("🗃️", "§"),
}

# Human-readable descriptions for issue types
ISSUE_DESCRIPTIONS = {
    "MONOLITH": ("split", "into smaller modules"),
    "UNDOCUMENTED": ("add module mapping + docs for", ""),
    "STALE_SYNC": ("update outdated SYNC for", ""),
    "PLACEHOLDER": ("fill in placeholders in", ""),
    "INCOMPLETE_CHAIN": ("add missing docs to", ""),
    "NO_DOCS_REF": ("add DOCS: comment to", ""),
    "BROKEN_IMPL_LINK": ("fix broken links in", ""),
    "STUB_IMPL": ("implement stubs in", ""),
    "INCOMPLETE_IMPL": ("complete functions in", ""),
    "UNDOC_IMPL": ("add to IMPLEMENTATION docs:", ""),
    "LARGE_DOC_MODULE": ("reduce size of", "docs"),
    "YAML_DRIFT": ("fix modules.yaml entry for", ""),
    "MISSING_TESTS": ("add tests for", ""),
    "ORPHAN_DOCS": ("link or remove orphan docs in", ""),
    "STALE_IMPL": ("update IMPLEMENTATION doc for", ""),
    "DOC_GAPS": ("complete gaps left in", ""),
    "ARBITRAGE": ("resolve conflict in", ""),
    "SUGGESTION": ("implement suggestion from", ""),
    "NEW_UNDOC_CODE": ("update docs for", ""),
    "COMPONENT_NO_STORIES": ("add stories for", ""),
    "HOOK_UNDOC": ("document hook", ""),
    "DOC_DUPLICATION": ("consolidate duplicate docs in", ""),
    "MAGIC_VALUES": ("extract magic numbers from", "to constants"),
    "HARDCODED_CONFIG": ("externalize config in", ""),
    "HARDCODED_SECRET": ("remove secret from", ""),
    "LONG_PROMPT": ("externalize prompts in", "to prompts/"),
    "LONG_SQL": ("externalize SQL in", "to .sql files"),
}


def get_learnings_content(target_dir: Path) -> str:
    """
    Load learnings from GLOBAL_LEARNINGS.md and return content to append.

    For repair agents, we use GLOBAL learnings since they're not VIEW-specific.
    """
    learnings_parts = []
    views_dir = target_dir / ".add-framework" / "views"

    # Load global learnings
    global_learnings = views_dir / "GLOBAL_LEARNINGS.md"
    if global_learnings.exists():
        content = global_learnings.read_text()
        # Only include if there are actual learnings (more than just the template)
        if "## Learnings" in content and content.count("\n") > 10:
            learnings_parts.append("# GLOBAL LEARNINGS (apply to ALL tasks)\n")
            learnings_parts.append(content)

    if learnings_parts:
        return "\n\n---\n\n" + "\n\n".join(learnings_parts)
    return ""


def get_issue_action_parts(issue_type: str) -> tuple:
    """Get action parts (prefix, suffix) for an issue type."""
    return ISSUE_DESCRIPTIONS.get(issue_type, ("fix", ""))


def get_issue_action(issue_type: str, path: str) -> str:
    """Get human-readable action for an issue (uncolored)."""
    prefix, suffix = get_issue_action_parts(issue_type)
    if suffix:
        return f"{prefix} {path} {suffix}"
    return f"{prefix} {path}"


def get_severity_color(severity: str) -> str:
    """Get color code for severity level."""
    return {
        "critical": Colors.FAILURE,
        "warning": Colors.WARNING,
        "info": Colors.DIM,
    }.get(severity, Colors.RESET)

# Agent symbols for parallel execution (memorable characters!)
AGENT_SYMBOLS = ["🥷", "🧚", "🤖", "🦊", "🐙", "🦄", "🧙", "🐲", "🦅", "🐺"]

# Issue priority (lower = fix first) - ordered by impact
ISSUE_PRIORITY = {
    # Foundation - fix manifest first
    "YAML_DRIFT": 1,          # Broken manifest breaks everything

    # Documentation creation - in dependency order
    "UNDOCUMENTED": 2,        # Create module + initial docs
    "INCOMPLETE_CHAIN": 3,    # Complete doc chain (needs UNDOCUMENTED first)
    "PLACEHOLDER": 4,         # Fill in content

    # Link fixes - need docs to exist first
    "BROKEN_IMPL_LINK": 5,    # Fix broken links (docs now exist)
    "NO_DOCS_REF": 6,         # Add DOCS: comments (docs now exist)

    # Staleness
    "STALE_SYNC": 7,          # Outdated state misleads
    "UNDOC_IMPL": 8,          # Add files to IMPLEMENTATION

    # Staleness and drift
    "STALE_IMPL": 9,          # IMPLEMENTATION doesn't match files

    # Code quality - more complex, do last
    "MONOLITH": 10,           # Large files harder to fix
    "STUB_IMPL": 11,          # Needs real implementation
    "INCOMPLETE_IMPL": 12,    # Needs code completion

    # Size and cleanup
    "LARGE_DOC_MODULE": 13,   # Docs too big
    "ORPHAN_DOCS": 14,        # Docs not linked from code
    "MISSING_TESTS": 15,      # No tests (lowest - tests are optional)

    # Handoff from previous agents
    "DOC_GAPS": 3,            # High priority - previous agent left work

    # Conflicts needing resolution
    "ARBITRAGE": 0,           # Highest priority - needs human decision first

    # User-requested actions
    "SUGGESTION": 1,          # User accepted - do after conflicts but before other work

    # Documentation drift
    "NEW_UNDOC_CODE": 8,      # Code changed but docs not updated
    "COMPONENT_NO_STORIES": 16,  # FE component without stories (low priority)
    "HOOK_UNDOC": 16,         # Hook without docs (low priority)
    "DOC_DUPLICATION": 6,     # Consolidate duplicate docs (after docs created)

    # Code quality issues
    "HARDCODED_SECRET": 0,    # CRITICAL: Security issue - fix immediately
    "HARDCODED_CONFIG": 12,   # Should externalize config
    "MAGIC_VALUES": 17,       # Low priority - code smell
    "LONG_PROMPT": 17,        # Low priority - refactoring opportunity
    "LONG_SQL": 17,           # Low priority - refactoring opportunity
}


def get_issue_symbol(issue_type: str) -> tuple:
    """Get emoji and symbol for an issue type."""
    return ISSUE_SYMBOLS.get(issue_type, ("🔹", "•"))


def get_agent_color(agent_id: int) -> str:
    """Get color code for an agent."""
    return Colors.AGENT_COLORS[agent_id % len(Colors.AGENT_COLORS)]


def get_agent_symbol(agent_id: int) -> str:
    """Get symbol for an agent."""
    return AGENT_SYMBOLS[agent_id % len(AGENT_SYMBOLS)]


def color(text: str, color_code: str) -> str:
    """Wrap text in ANSI color codes."""
    return f"{color_code}{text}{Colors.RESET}"


def load_github_issue_mapping(target_dir: Path) -> Dict[str, int]:
    """Load GitHub issue mapping from health report or tracking file."""
    mapping = {}

    # Try to load from a tracking file first
    tracking_path = target_dir / ".add-framework" / "state" / "github_issues.json"
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
    tracking_path = target_dir / ".add-framework" / "state" / "github_issues.json"
    if tracking_path.parent.exists():
        import json
        with open(tracking_path, "w") as f:
            json.dump(mapping, f, indent=2)


# Issue types categorized by repair depth
DEPTH_LINKS = {
    # Only fix references and links
    "NO_DOCS_REF",        # Add DOCS: reference to source file
    "BROKEN_IMPL_LINK",   # Fix broken file references in IMPLEMENTATION doc
    "YAML_DRIFT",         # Fix modules.yaml mappings
    "UNDOC_IMPL",         # Add file to IMPLEMENTATION doc
    "ORPHAN_DOCS",        # Link or remove orphan docs
}

DEPTH_DOCS = DEPTH_LINKS | {
    # Also create/update documentation content
    "UNDOCUMENTED",       # Create module docs
    "STALE_SYNC",         # Update stale SYNC files
    "PLACEHOLDER",        # Fill in placeholder content
    "INCOMPLETE_CHAIN",   # Create missing doc types
    "LARGE_DOC_MODULE",   # Reduce doc module size
    "STALE_IMPL",         # Update outdated IMPLEMENTATION doc
    "DOC_GAPS",           # Complete gaps from previous agent
    "ARBITRAGE",          # Resolve conflicts with human decision
    "DOC_DUPLICATION",    # Consolidate duplicate documentation
}

DEPTH_FULL = DEPTH_DOCS | {
    # Also make code changes
    "MONOLITH",           # Split large files
    "STUB_IMPL",          # Implement stub functions
    "INCOMPLETE_IMPL",    # Complete empty functions
    "MISSING_TESTS",      # Write tests for module
    # Code quality
    "HARDCODED_SECRET",   # Remove secrets from code
    "HARDCODED_CONFIG",   # Externalize configuration
    "MAGIC_VALUES",       # Extract to constants
    "LONG_PROMPT",        # Move to prompts directory
    "LONG_SQL",           # Move to .sql files
}


@dataclass
class RepairResult:
    """Result from a single repair agent."""
    issue_type: str
    target_path: str
    success: bool
    agent_output: str
    duration_seconds: float
    error: Optional[str] = None
    decisions_made: List[Dict[str, str]] = None  # [{name, conflict, resolution, reasoning}]


# Agent system prompt template
AGENT_SYSTEM_PROMPT = """You are a ADD Framework repair agent. Your job is to fix ONE specific issue in the project.

CRITICAL RULES:
1. FIRST: Read all documentation listed in "Docs to Read" before making changes
2. Follow the VIEW instructions exactly
3. After fixing, update the relevant SYNC file with what you changed
4. Keep changes minimal and focused on the specific issue
5. Do NOT make unrelated changes or "improvements"
6. Report completion status clearly at the end
7. NEVER create git branches - always work on the current branch
8. NEVER use git stash - other agents are working in parallel

CLI COMMANDS (use these!):
- `add-framework context {file}` - Get full doc chain for any source file
- `add-framework validate` - Check protocol invariants after changes
- `add-framework doctor --no-github` - Re-check project health

BIDIRECTIONAL LINKS:
- When creating new docs, add CHAIN section linking to related docs
- When modifying code, ensure DOCS: reference points to correct docs
- When creating module docs, add mapping to modules.yaml

AFTER CHANGES:
- Run `add-framework validate` to verify links are correct
- Update SYNC file with what changed
- Commit with descriptive message (include "Closes #NUMBER" if GitHub issue provided)

IF YOU CAN'T COMPLETE THE FULL FIX:
- Still report "REPAIR COMPLETE" for what you DID finish
- Add a "## GAPS" section to the relevant SYNC file listing:
  - What was completed
  - What remains to be done
  - Why you couldn't finish (missing info, too complex, needs human decision, etc.)
- Example SYNC addition:
  ```
  ## GAPS

  ### From repair session {date}
  - [x] Created PATTERNS doc
  - [ ] ALGORITHM doc needs: detailed flow for edge cases
  - [ ] Blocked: need clarification on error handling strategy
  ```
- This ensures the next agent knows exactly where to pick up

IF YOU FIND CONTRADICTIONS (docs vs code, or doc vs doc):
- Add a "## CONFLICTS" section to the relevant SYNC file
- **BE DECISIVE** - make the call yourself unless you truly cannot
- We can always improve later; progress > perfection

**Before making a DECISION:**
- If <70% confident, RE-READ the relevant docs first
- Check: PATTERNS (why), BEHAVIORS (what), ALGORITHM (how), VALIDATION (constraints)
- Often the answer is in the docs - you just need to look again

- For each conflict, categorize as DECISION or ARBITRAGE:
  - DECISION: You resolve it (this should be 90%+ of conflicts)
  - ARBITRAGE: Only when you truly cannot decide (missing critical info, major architectural choice)

- **DECISION format** (preferred - be decisive!):
  ```
  ### DECISION: {conflict name}
  - Conflict: {what contradicted what}
  - Resolution: {what you decided}
  - Reasoning: {why this choice}
  - Updated: {what files you changed}
  ```

- ARBITRAGE only when truly blocked - can be TWO types:

  **Type 1: Choice needed** - you understand but can't decide
  - Provide options in (A)/(B)/(C) format with pros/cons
  - Give recommendation with reasoning if you have one

  **Type 2: Context needed** - you lack information to proceed
  - Explain what you're trying to do
  - Explain what you need to know
  - Be specific about what context would unblock you

- Example SYNC addition:
  ```
  ## CONFLICTS

  ### DECISION: Auth timeout value
  - BEHAVIORS says 30 min, code uses 15 min
  - Resolved: Updated BEHAVIORS to match code (15 min is intentional per commit history)

  ### ARBITRAGE: Error handling strategy
  - PATTERNS says "fail fast", ALGORITHM says "retry 3 times"
  - Needs human: Which approach should we use?
  - (A) Fail fast everywhere
    - Pro: Simpler, surfaces bugs early, easier to debug
    - Con: Poor UX for transient network issues
  - (B) Retry for network errors only
    - Pro: Resilient to transient failures, better UX
    - Con: Can mask real issues, adds latency
  - (C) Configurable per-call
    - Pro: Maximum flexibility
    - Con: More complex API, decisions pushed to callers
  - **Recommendation:** (B) - Most codebases benefit from retry on network errors.
    The "fail fast" in PATTERNS likely refers to logic errors, not I/O.

  ### ARBITRAGE: Payment provider integration
  - Trying to: Document the payment flow in ALGORITHM
  - Need to know: Which payment provider is being used? (Stripe, PayPal, custom?)
  - Context needed: The code uses `PaymentClient` but I can't find its implementation
    or configuration. Is this an internal service or third-party API?
  - This would help me: Write accurate ALGORITHM docs and error handling guidance
  ```
- DECISION items: resolve and mark as resolved
- ARBITRAGE items: leave for human review, will be detected by doctor
- The `repair` command will prompt users interactively for ARBITRAGE items
"""


# NOTE: get_issue_instructions() moved to repair_instructions.py
# See import at top: from .repair_instructions import get_issue_instructions


def build_agent_prompt(
    issue: DoctorIssue,
    instructions: Dict[str, Any],
    target_dir: Path,
    github_issue_number: Optional[int] = None,
) -> str:
    """Build the full prompt for the repair agent."""
    docs_list = "\n".join(f"- {d}" for d in instructions["docs_to_read"])

    github_section = ""
    if github_issue_number:
        github_section = f"""
## GitHub Issue
This fix is tracked by GitHub issue #{github_issue_number}.
When committing, include "Closes #{github_issue_number}" in your commit message.
"""

    return f"""# ADD Framework Repair Task

## Issue Type: {issue.issue_type}
## Severity: {issue.severity}
{github_section}
## VIEW to Follow
Load and follow: `.add-framework/views/{instructions['view']}`

## Docs to Read FIRST (before any changes)
{docs_list}

{instructions['prompt']}

## After Completion
1. Commit your changes with a descriptive message{f' (include "Closes #{github_issue_number}")' if github_issue_number else ''}
2. Update `.add-framework/state/SYNC_Project_State.md` with:
   - What you fixed
   - Files created/modified
   - Any issues encountered
"""


def parse_decisions_from_output(output: str) -> List[Dict[str, str]]:
    """Parse DECISION items from agent output."""
    decisions = []
    lines = output.split('\n')

    current_decision = None
    for line in lines:
        stripped = line.strip()

        # Look for DECISION headers
        if '### DECISION:' in stripped or '### Decision:' in stripped:
            if current_decision and current_decision.get('name'):
                decisions.append(current_decision)
            name = stripped.split(':', 1)[1].strip() if ':' in stripped else ''
            current_decision = {'name': name, 'conflict': '', 'resolution': '', 'reasoning': ''}
        elif current_decision:
            lower = stripped.lower()
            if lower.startswith('- conflict:') or lower.startswith('conflict:'):
                current_decision['conflict'] = stripped.split(':', 1)[1].strip()
            elif lower.startswith('- resolution:') or lower.startswith('resolution:'):
                current_decision['resolution'] = stripped.split(':', 1)[1].strip()
            elif lower.startswith('- reasoning:') or lower.startswith('reasoning:'):
                current_decision['reasoning'] = stripped.split(':', 1)[1].strip()
            elif lower.startswith('- updated:') or lower.startswith('updated:'):
                current_decision['updated'] = stripped.split(':', 1)[1].strip()
            elif stripped.startswith('###') or stripped.startswith('## '):
                # New section, save current decision
                if current_decision.get('name'):
                    decisions.append(current_decision)
                current_decision = None

    # Don't forget last decision
    if current_decision and current_decision.get('name'):
        decisions.append(current_decision)

    return decisions


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


REPORT_PROMPT = """You are generating a repair report for a ADD Framework project.

Analyze the repair session data and write a detailed, insightful report. Be specific about:
1. What patterns you see in the repairs (common issue types, areas of the codebase)
2. Why certain repairs may have failed
3. Concrete next steps for the human or next agent
4. Any systemic issues the repairs reveal about the project

Write in a direct, professional tone. Use markdown formatting.

## Repair Session Data

**Project:** {project_name}
**Date:** {date}

### Health Score
- Before: {score_before}/100
- After: {score_after}/100
- Change: {score_change:+d}

### Issue Summary
- Critical before: {critical_before} → after: {critical_after}
- Warnings before: {warning_before} → after: {warning_after}

### Repairs Attempted ({total_repairs})
**Successful ({success_count}):**
{successful_list}

**Failed ({failed_count}):**
{failed_list}

**Total Duration:** {total_duration:.1f} seconds

### Decisions Made by Agents
{decisions_list}

### Remaining Issues
Critical: {remaining_critical}
Warnings: {remaining_warning}

---

Write the report now. Include:
1. Executive Summary (2-3 sentences)
2. What Was Fixed (with insights, not just a list)
3. Decisions Made (highlight key choices agents made and their reasoning)
4. What Failed and Why (analysis)
5. Patterns Observed (what do these issues say about the codebase?)
6. Recommended Next Steps (specific, actionable)
7. For Next Agent (handoff notes)
"""


def generate_llm_report(
    before_results: Dict[str, Any],
    after_results: Dict[str, Any],
    repair_results: List[RepairResult],
    target_dir: Path,
) -> Optional[str]:
    """Generate a detailed report using Claude."""

    successful = [r for r in repair_results if r.success]
    failed = [r for r in repair_results if not r.success]

    successful_list = "\n".join(
        f"- {r.issue_type}: `{r.target_path}` ({r.duration_seconds:.1f}s)"
        for r in successful
    ) or "None"

    failed_list = "\n".join(
        f"- {r.issue_type}: `{r.target_path}` — {r.error or 'unknown error'}"
        for r in failed
    ) or "None"

    # Collect all decisions made
    all_decisions = []
    for r in repair_results:
        if r.decisions_made:
            for d in r.decisions_made:
                all_decisions.append(f"- **{d.get('name', 'Unknown')}**: {d.get('resolution', 'No resolution')} (Reason: {d.get('reasoning', 'Not stated')})")
    decisions_list = "\n".join(all_decisions) or "None"

    prompt = REPORT_PROMPT.format(
        project_name=target_dir.name,
        date=datetime.now().strftime('%Y-%m-%d %H:%M'),
        score_before=before_results["score"],
        score_after=after_results["score"],
        score_change=after_results["score"] - before_results["score"],
        critical_before=before_results["summary"]["critical"],
        critical_after=after_results["summary"]["critical"],
        warning_before=before_results["summary"]["warning"],
        warning_after=after_results["summary"]["warning"],
        total_repairs=len(repair_results),
        success_count=len(successful),
        failed_count=len(failed),
        successful_list=successful_list,
        failed_list=failed_list,
        decisions_list=decisions_list,
        total_duration=sum(r.duration_seconds for r in repair_results),
        remaining_critical=after_results["summary"]["critical"],
        remaining_warning=after_results["summary"]["warning"],
    )

    try:
        cmd = [
            "claude",
            "-p", prompt,
            "--output-format", "text",
        ]

        result = subprocess.run(
            cmd,
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0 and result.stdout.strip():
            # Add header
            header = f"""# ADD Framework Repair Report

```
GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}
PROJECT: {target_dir.name}
GENERATED_BY: Claude
```

---

"""
            return header + result.stdout.strip()
    except Exception as e:
        print(f"  {Colors.DIM}(LLM report failed: {e}, using fallback){Colors.RESET}")

    return None


def generate_final_report(
    before_results: Dict[str, Any],
    after_results: Dict[str, Any],
    repair_results: List[RepairResult],
    target_dir: Path,
) -> str:
    """Generate a final report summarizing all repairs (fallback if LLM fails)."""

    # Calculate improvements
    score_before = before_results["score"]
    score_after = after_results["score"]
    score_change = score_after - score_before

    critical_before = before_results["summary"]["critical"]
    critical_after = after_results["summary"]["critical"]

    successful = [r for r in repair_results if r.success]
    failed = [r for r in repair_results if not r.success]

    total_duration = sum(r.duration_seconds for r in repair_results)

    lines = []
    lines.append("# ADD Framework Repair Report")
    lines.append("")
    lines.append("```")
    lines.append(f"GENERATED: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"PROJECT: {target_dir.name}")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")
    lines.append(f"| Metric | Before | After | Change |")
    lines.append(f"|--------|--------|-------|--------|")
    lines.append(f"| Health Score | {score_before}/100 | {score_after}/100 | {'+' if score_change >= 0 else ''}{score_change} |")
    lines.append(f"| Critical Issues | {critical_before} | {critical_after} | {critical_before - critical_after} fixed |")
    lines.append(f"| Warnings | {before_results['summary']['warning']} | {after_results['summary']['warning']} | - |")
    lines.append("")

    # Repairs attempted
    lines.append("## Repairs Attempted")
    lines.append("")
    lines.append(f"**Total:** {len(repair_results)} issues")
    lines.append(f"**Successful:** {len(successful)}")
    lines.append(f"**Failed:** {len(failed)}")
    lines.append(f"**Duration:** {total_duration:.1f} seconds")
    lines.append("")

    if successful:
        lines.append("### Successful Repairs")
        lines.append("")
        for r in successful:
            lines.append(f"- **{r.issue_type}**: `{r.target_path}` ({r.duration_seconds:.1f}s)")
        lines.append("")

    if failed:
        lines.append("### Failed Repairs")
        lines.append("")
        for r in failed:
            lines.append(f"- **{r.issue_type}**: `{r.target_path}`")
            if r.error:
                lines.append(f"  - Error: {r.error}")
        lines.append("")

    # Decisions made
    all_decisions = []
    for r in repair_results:
        if r.decisions_made:
            all_decisions.extend(r.decisions_made)

    if all_decisions:
        lines.append("## Decisions Made")
        lines.append("")
        lines.append("Agents made the following decisions to resolve conflicts:")
        lines.append("")
        for d in all_decisions:
            lines.append(f"### {d.get('name', 'Unknown')}")
            if d.get('conflict'):
                lines.append(f"- **Conflict:** {d['conflict']}")
            if d.get('resolution'):
                lines.append(f"- **Resolution:** {d['resolution']}")
            if d.get('reasoning'):
                lines.append(f"- **Reasoning:** {d['reasoning']}")
            if d.get('updated'):
                lines.append(f"- **Updated:** {d['updated']}")
            lines.append("")

    # Remaining issues
    if after_results["summary"]["critical"] > 0 or after_results["summary"]["warning"] > 0:
        lines.append("## Remaining Issues")
        lines.append("")
        lines.append("Run `add-framework doctor` for details on remaining issues.")
        lines.append("")

    # Recommendations
    lines.append("## Recommendations")
    lines.append("")

    if score_after >= 80:
        lines.append("Project health is good. Continue with normal development.")
    elif score_after >= 50:
        lines.append("Project health is improving. Consider running repair again to address remaining issues.")
    else:
        lines.append("Project still has critical issues. Manual intervention may be needed for complex cases.")
    lines.append("")

    if failed:
        lines.append("### Failed Repairs Need Attention")
        lines.append("")
        lines.append("The following issues could not be automatically repaired:")
        for r in failed:
            lines.append(f"- `{r.target_path}`: {r.error or 'Unknown error'}")
        lines.append("")
        lines.append("Consider fixing these manually using the appropriate VIEW.")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("*Generated by `add-framework repair`*")

    return "\n".join(lines)


def print_progress_bar(current: int, total: int, width: int = 40, status: str = "") -> None:
    """Print a progress bar."""
    percent = current / total if total > 0 else 0
    filled = int(width * percent)
    bar = "█" * filled + "░" * (width - filled)
    sys.stdout.write(f"\r  [{bar}] {current}/{total} {status}")
    sys.stdout.flush()


def get_depth_types(depth: str) -> set:
    """Get the set of issue types for a given depth level."""
    if depth == "links":
        return DEPTH_LINKS
    elif depth == "docs":
        return DEPTH_DOCS
    else:  # full
        return DEPTH_FULL


@dataclass
class ArbitrageDecision:
    """User's decision for an ARBITRAGE conflict."""
    conflict_title: str
    decision: str  # User's choice or "pass"
    passed: bool = False


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

    manager_dir = target_dir / ".add-framework" / "agents" / "manager"
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

    print(f"🔧 ADD Framework Repair")
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
            print(f"  {Colors.DIM}To check documentation issues: {Colors.RESET}{Colors.BOLD}add-framework repair --depth docs{Colors.RESET}")
            print(f"  {Colors.DIM}To check all issues:           {Colors.RESET}{Colors.BOLD}add-framework repair --depth full{Colors.RESET}")
        elif depth == "docs":
            print(f"  {Colors.DIM}All documentation issues are resolved.{Colors.RESET}")
            if has_other_issues:
                print(f"  {Colors.DIM}There are {total_critical} critical + {total_warnings} warning issues at 'full' depth.{Colors.RESET}")
            print(f"  {Colors.DIM}To check implementation issues: {Colors.RESET}{Colors.BOLD}add-framework repair --depth full{Colors.RESET}")
        else:  # full
            print(f"  {Colors.DIM}Project is healthy at all depths!{Colors.RESET}")
            print(f"  {Colors.DIM}Run {Colors.RESET}{Colors.BOLD}add-framework doctor{Colors.RESET}{Colors.DIM} to see the full health report.{Colors.RESET}")
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
    report_path = target_dir / ".add-framework" / "state" / "REPAIR_REPORT.md"
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
