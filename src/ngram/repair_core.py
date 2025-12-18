"""
Core repair logic shared between CLI and TUI.

This module contains:
- Data structures (RepairResult, ArbitrageDecision)
- Constants (issue symbols, priorities, depth filters)
- Pure functions for building prompts and parsing output
- Async agent spawning for TUI integration

DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md
"""

import asyncio
import json
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional


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

# Agent symbols for parallel execution
AGENT_SYMBOLS = ["🥷", "🧚", "🤖", "🦊", "🐙", "🦄", "🧙", "🐲", "🦅", "🐺"]

# Issue priority (lower = fix first)
ISSUE_PRIORITY = {
    "YAML_DRIFT": 1,
    "UNDOCUMENTED": 2,
    "INCOMPLETE_CHAIN": 3,
    "PLACEHOLDER": 4,
    "BROKEN_IMPL_LINK": 5,
    "NO_DOCS_REF": 6,
    "STALE_SYNC": 7,
    "UNDOC_IMPL": 8,
    "STALE_IMPL": 9,
    "MONOLITH": 10,
    "STUB_IMPL": 11,
    "INCOMPLETE_IMPL": 12,
    "LARGE_DOC_MODULE": 13,
    "ORPHAN_DOCS": 14,
    "MISSING_TESTS": 15,
    "DOC_GAPS": 3,
    "ARBITRAGE": 0,
    "SUGGESTION": 1,
    "NEW_UNDOC_CODE": 8,
    "COMPONENT_NO_STORIES": 16,
    "HOOK_UNDOC": 16,
    "DOC_DUPLICATION": 6,
    "HARDCODED_SECRET": 0,
    "HARDCODED_CONFIG": 12,
    "MAGIC_VALUES": 17,
    "LONG_PROMPT": 17,
    "LONG_SQL": 17,
}

# Issue types categorized by repair depth
DEPTH_LINKS = {
    "NO_DOCS_REF",
    "BROKEN_IMPL_LINK",
    "YAML_DRIFT",
    "UNDOC_IMPL",
    "ORPHAN_DOCS",
}

DEPTH_DOCS = DEPTH_LINKS | {
    "UNDOCUMENTED",
    "STALE_SYNC",
    "PLACEHOLDER",
    "INCOMPLETE_CHAIN",
    "LARGE_DOC_MODULE",
    "STALE_IMPL",
    "DOC_GAPS",
    "ARBITRAGE",
    "DOC_DUPLICATION",
}

DEPTH_FULL = DEPTH_DOCS | {
    "MONOLITH",
    "STUB_IMPL",
    "INCOMPLETE_IMPL",
    "MISSING_TESTS",
    "HARDCODED_SECRET",
    "HARDCODED_CONFIG",
    "MAGIC_VALUES",
    "LONG_PROMPT",
    "LONG_SQL",
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
    decisions_made: Optional[List[Dict[str, str]]] = None


@dataclass
class ArbitrageDecision:
    """User's decision for an ARBITRAGE conflict."""
    conflict_title: str
    decision: str
    passed: bool = False


# Agent system prompt template
AGENT_SYSTEM_PROMPT = """You are an ngram repair agent. Your job is to fix ONE specific issue in the project.

CRITICAL RULES:
1. FIRST: Read all documentation listed in "Docs to Read" before making changes
2. Follow the VIEW instructions exactly
3. After fixing, update the relevant SYNC file with what you changed
4. Keep changes minimal and focused on the specific issue
5. Do NOT make unrelated changes or "improvements"
6. Report completion status clearly at the end
7. NEVER create git branches - always work on the current branch
8. NEVER use git stash - other agents are working in parallel

PIPELINE AWARENESS:
You are part of a development pipeline. When making changes, keep docs in sync:
- Code changes → Update ALGORITHM and/or IMPLEMENTATION docs
- Behavior changes → Update BEHAVIORS doc
- Design changes → Update PATTERNS doc
- Test changes → Update TEST doc
- ANY changes → Update SYNC with what changed and why

The doctor checks for drift (STALE_SYNC, NEW_UNDOC_CODE, STALE_IMPL).
The manager monitors your work for doc/code alignment.
Don't leave upstream docs stale when you change downstream artifacts.

CLI COMMANDS (use these!):
- `ngram context {file}` - Get full doc chain for any source file
- `ngram validate` - Check protocol invariants after changes
- `ngram doctor --no-github` - Re-check project health

BIDIRECTIONAL LINKS:
- When creating new docs, add CHAIN section linking to related docs
- When modifying code, ensure DOCS: reference points to correct docs
- When creating module docs, add mapping to modules.yaml

AFTER CHANGES:
- Run `ngram validate` to verify links are correct
- Update SYNC file with what changed
- Commit with descriptive message (include "Closes #NUMBER" if GitHub issue provided)

IF YOU CAN'T COMPLETE THE FULL FIX:
- Still report "REPAIR COMPLETE" for what you DID finish
- Add a "## GAPS" section to the relevant SYNC file listing:
  - What was completed
  - What remains to be done
  - Why you couldn't finish (missing info, too complex, needs human decision, etc.)

IF YOU FIND CONTRADICTIONS (docs vs code, or doc vs doc):
- Add a "## CONFLICTS" section to the relevant SYNC file
- **BE DECISIVE** - make the call yourself unless you truly cannot

**Before making a DECISION:**
- If <70% confident, RE-READ the relevant docs first
- Check: PATTERNS (why), BEHAVIORS (what), ALGORITHM (how), VALIDATION (constraints)

- For each conflict, categorize as DECISION or ARBITRAGE:
  - DECISION: You resolve it (this should be 90%+ of conflicts)
  - ARBITRAGE: Only when you truly cannot decide

- **DECISION format** (preferred - be decisive!):
  ```
  ### DECISION: {conflict name}
  - Conflict: {what contradicted what}
  - Resolution: {what you decided}
  - Reasoning: {why this choice}
  - Updated: {what files you changed}
  ```
"""


def get_learnings_content(target_dir: Path) -> str:
    """Load learnings from GLOBAL_LEARNINGS.md."""
    views_dir = target_dir / ".ngram" / "views"
    global_learnings = views_dir / "GLOBAL_LEARNINGS.md"

    if global_learnings.exists():
        content = global_learnings.read_text()
        if "## Learnings" in content and content.count("\n") > 10:
            return "\n\n---\n\n# GLOBAL LEARNINGS (apply to ALL tasks)\n" + content
    return ""


# NOTE: These lookup functions are intentionally simple one-line implementations.
# They provide semantic meaning for dictionary lookups with sensible defaults.
# Short body does not mean incomplete - these are complete implementations.

def get_issue_symbol(issue_type: str) -> tuple:
    """Get emoji and symbol for an issue type."""
    return ISSUE_SYMBOLS.get(issue_type, ("🔹", "•"))


def get_issue_action_parts(issue_type: str) -> tuple:
    """Get action parts (prefix, suffix) for an issue type."""
    return ISSUE_DESCRIPTIONS.get(issue_type, ("fix", ""))


def get_issue_action(issue_type: str, path: str) -> str:
    """Get human-readable action for an issue."""
    prefix, suffix = get_issue_action_parts(issue_type)
    if suffix:
        return f"{prefix} {path} {suffix}"
    return f"{prefix} {path}"


def get_depth_types(depth: str) -> set:
    """Get the set of issue types for a given depth level."""
    if depth == "links":
        return DEPTH_LINKS
    elif depth == "docs":
        return DEPTH_DOCS
    else:
        return DEPTH_FULL


def build_agent_prompt(
    issue: Any,  # DoctorIssue
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

    return f"""# ngram Repair Task

## Issue Type: {issue.issue_type}
## Severity: {issue.severity}
{github_section}
## VIEW to Follow
Load and follow: `.ngram/views/{instructions['view']}`

## Docs to Read FIRST (before any changes)
{docs_list}

{instructions['prompt']}

## After Completion
1. Commit your changes with a descriptive message{f' (include "Closes #{github_issue_number}")' if github_issue_number else ''}
2. Update `.ngram/state/SYNC_Project_State.md` with:
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
                if current_decision.get('name'):
                    decisions.append(current_decision)
                current_decision = None

    if current_decision and current_decision.get('name'):
        decisions.append(current_decision)

    return decisions


def parse_stream_json_line(line: str) -> Optional[str]:
    """Parse a single JSON line from Claude stream output, return readable text."""
    try:
        data = json.loads(line)
        msg_type = data.get("type", "")

        # Handle streaming content deltas (main streaming output)
        if msg_type == "content_block_delta":
            delta = data.get("delta", {})
            if delta.get("type") == "text_delta":
                return delta.get("text", "")

        # Handle tool use results
        elif msg_type == "content_block_start":
            content = data.get("content_block", {})
            if content.get("type") == "tool_use":
                tool_name = content.get("name", "")
                return f"[Using: {tool_name}]"

        # Handle final assistant message (fallback)
        elif msg_type == "assistant":
            message = data.get("message", {})
            for content in message.get("content", []):
                if content.get("type") == "text":
                    return content.get("text", "")

        # Handle result messages
        elif msg_type == "result":
            result = data.get("result", "")
            if result:
                return f"[Result: {result[:100]}...]" if len(result) > 100 else f"[Result: {result}]"

    except json.JSONDecodeError:
        pass
    return None


async def spawn_repair_agent_async(
    issue: Any,  # DoctorIssue
    target_dir: Path,
    on_output: Callable[[str], Awaitable[None]],
    instructions: Dict[str, Any],
    github_issue_number: Optional[int] = None,
    arbitrage_decisions: Optional[List[ArbitrageDecision]] = None,
) -> RepairResult:
    """
    Async version of spawn_repair_agent for TUI integration.

    Args:
        issue: The DoctorIssue to fix
        target_dir: Project directory
        on_output: Async callback for each output line
        instructions: Instructions from get_issue_instructions()
        github_issue_number: Optional GitHub issue number
        arbitrage_decisions: Optional user decisions for ARBITRAGE issues

    Returns:
        RepairResult with success status and output
    """
    # Handle ARBITRAGE decisions
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
    system_prompt = AGENT_SYSTEM_PROMPT + get_learnings_content(target_dir)

    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--append-system-prompt", system_prompt,
        "--verbose",
        "--output-format", "stream-json",
    ]

    start_time = time.time()
    text_output = []

    try:
        process = await asyncio.create_subprocess_exec(
            *cmd,
            cwd=target_dir,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        async for line in process.stdout:
            line_str = line.decode().strip()
            if not line_str:
                continue

            # Parse JSON and extract text
            parsed = parse_stream_json_line(line_str)
            if parsed:
                text_output.append(parsed)
                await on_output(parsed)

        await process.wait()
        duration = time.time() - start_time

        readable_output = "\n".join(text_output)
        success = "REPAIR COMPLETE" in readable_output and "REPAIR FAILED" not in readable_output
        decisions = parse_decisions_from_output(readable_output)

        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=success,
            agent_output=readable_output,
            duration_seconds=duration,
            error=None if process.returncode == 0 else f"Exit code: {process.returncode}",
            decisions_made=decisions if decisions else None,
        )

    except asyncio.TimeoutError:
        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=False,
            agent_output="\n".join(text_output),
            duration_seconds=600,
            error="Agent timed out after 10 minutes",
        )
    except Exception as e:
        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=False,
            agent_output="\n".join(text_output),
            duration_seconds=time.time() - start_time,
            error=str(e),
        )
