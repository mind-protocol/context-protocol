"""
Core repair logic shared between CLI and TUI.

This module contains:
- Data structures (RepairResult, EscalationDecision)
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

from .agent_cli import build_agent_command, normalize_agent
from .doctor_types import DoctorConfig
from .doctor_files import save_doctor_config


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
    "ESCALATION": ("⚖️", "⚡"),
    "PROPOSITION": ("💡", "✨"), # New: Agent proposals for improvement/refactor/features
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
    "LOG_ERROR": ("🧯", "×"),
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
    "ESCALATION": ("resolve conflict in", ""),
    "PROPOSITION": ("review agent proposition in", ""), # New: Agent proposals for improvement/refactor/features
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
    "LOG_ERROR": ("review log errors in", ""),
}

# Agent symbols for parallel execution (20 symbols for variety)
AGENT_SYMBOLS = [
    "🥷", "🧚", "🤖", "🦊", "🐙", "🦄", "🧙", "🐲", "🦅", "🐺",
    "🦝", "🦉", "🐢", "🦎", "🐝", "🦋", "🐬", "🦈", "🦁", "🐯",
]

# Symbol to folder name mapping
AGENT_SYMBOL_NAMES = {
    "🥷": "ninja",
    "🧚": "fairy",
    "🤖": "robot",
    "🦊": "fox",
    "🐙": "octopus",
    "🦄": "unicorn",
    "🧙": "wizard",
    "🐲": "dragon",
    "🦅": "eagle",
    "🐺": "wolf",
    "🦝": "raccoon",
    "🦉": "owl",
    "🐢": "turtle",
    "🦎": "lizard",
    "🐝": "bee",
    "🦋": "butterfly",
    "🐬": "dolphin",
    "🦈": "shark",
    "🦁": "lion",
    "🐯": "tiger",
}


def get_symbol_name(symbol: str, index: int = 0) -> str:
    """Get folder-safe name for an agent symbol with optional index for duplicates.

    Args:
        symbol: The emoji symbol
        index: The agent index (0-based), used for numbering when > 10 agents

    Returns:
        Folder name like "ninja" for first 10, "ninja-2" for 11th ninja, etc.
    """
    base_name = AGENT_SYMBOL_NAMES.get(symbol, f"agent-{ord(symbol) if len(symbol) == 1 else hash(symbol) % 10000}")
    cycle = index // len(AGENT_SYMBOLS)
    if cycle > 0:
        return f"{base_name}-{cycle + 1}"
    return base_name


def get_issue_folder_name(issue_type: str, path: str, index: int = 0) -> str:
    """Get folder-safe name from issue type and path.

    Args:
        issue_type: e.g., "MONOLITH", "STALE_SYNC"
        path: e.g., "docs/physics/SYNC_Physics.md"
        index: Agent index for uniqueness

    Returns:
        Folder name like "STALE_SYNC-physics-SYNC_Physics" (sanitized)
    """
    import re
    # Extract meaningful parts from path
    path_parts = path.replace("\\", "/").split("/")
    # Take last 2 meaningful parts (skip extension)
    meaningful = []
    for part in reversed(path_parts):
        if part and part not in (".", ".."):
            # Remove extension
            name = re.sub(r'\.[^.]+$', '', part)
            if name:
                meaningful.insert(0, name)
            if len(meaningful) >= 2:
                break

    # Build folder name: TYPE-path_part1-path_part2
    path_str = "-".join(meaningful) if meaningful else "unknown"
    # Sanitize: only alphanumeric, dash, underscore
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', f"{issue_type}-{path_str}")
    # Add index if needed for uniqueness
    if index > 0:
        sanitized = f"{index:02d}-{sanitized}"
    else:
        sanitized = f"{index:02d}-{sanitized}"
    return sanitized[:60]  # Limit length

# Issue priority (lower = fix first)
# Order: MONOLITH (blocks all) → INCOMPLETE_IMPL (code first) → DOC_DUPLICATION →
#        INCOMPLETE_CHAIN (structural) → LARGE_DOC_MODULE (info) → HARDCODED_CONFIG (often false positive)
ISSUE_PRIORITY = {
    "HARDCODED_SECRET": 0,   # Security first
    "ESCALATION": 1,          # Conflicts block progress
    "MONOLITH": 2,           # Blocks everything
    "INCOMPLETE_IMPL": 3,    # Code before docs
    "STUB_IMPL": 4,          # Also code
    "DOC_DUPLICATION": 5,    # Fix content
    "INCOMPLETE_CHAIN": 6,   # Structural docs
    "YAML_DRIFT": 7,         # Config alignment
    "UNDOCUMENTED": 8,       # New docs needed
    "PLACEHOLDER": 9,        # Fill in gaps
    "BROKEN_IMPL_LINK": 10,  # Fix links
    "NO_DOCS_REF": 11,       # Add refs
    "STALE_SYNC": 12,        # Update state
    "UNDOC_IMPL": 13,        # Doc existing code
    "STALE_IMPL": 14,        # Update impl docs
    "DOC_GAPS": 15,          # Fill gaps
    "NEW_UNDOC_CODE": 16,    # New code docs
    "PROPOSITION": 16,        # New: Agent proposals, high priority for human review
    "SUGGESTION": 17,        # Nice to have
    "ORPHAN_DOCS": 18,       # Cleanup
    "MISSING_TESTS": 19,     # Tests last
    "LARGE_DOC_MODULE": 20,  # Info only
    "COMPONENT_NO_STORIES": 21,
    "HOOK_UNDOC": 22,
    "MAGIC_VALUES": 23,
    "LONG_PROMPT": 24,
    "LONG_SQL": 25,
    "LOG_ERROR": 90,
    "HARDCODED_CONFIG": 99,  # Often false positive, last
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
    "ESCALATION",
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
class EscalationDecision:
    """User's decision for an ESCALATION conflict."""
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
- `ngram doctor` - Re-check project health

BIDIRECTIONAL LINKS:
- When creating new docs, add CHAIN section linking to related docs
- When modifying code, ensure DOCS: reference points to correct docs
- When creating module docs, add mapping to modules.yaml

AFTER CHANGES:
- Run `ngram validate` to verify links are correct
- Update SYNC file with what changed
- Commit with descriptive message using a type prefix (e.g., "fix:", "docs:", "refactor:") and include the issue reference ("Closes #NUMBER" if provided or inferred from recent commits)

IF YOU CAN'T COMPLETE THE FULL FIX:
- Add a "## GAPS" section to the relevant SYNC file listing:
  - What was completed
  - What remains to be done
  - Why you couldn't finish (missing info, too complex, needs human decision, etc.)
Do NOT claim completion without a git commit.

IF YOU FIND CONTRADICTIONS (docs vs code, or doc vs doc):
- Add a "## CONFLICTS" section to the relevant SYNC file
- **BE DECISIVE** - make the call yourself unless you truly cannot

**Before making a DECISION:**
- If <70% confident, RE-READ the relevant docs first
- Check: PATTERNS (why), BEHAVIORS (what), ALGORITHM (how), VALIDATION (constraints)

- For each conflict, categorize as DECISION or ESCALATION:
  - DECISION: You resolve it (this should be 90%+ of conflicts)
  - ESCALATION: Only when you truly cannot decide

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


def _get_git_head(target_dir: Path) -> Optional[str]:
    """Return current git HEAD hash, or None if unavailable."""
    import subprocess

    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip() or None
    except Exception:
        return None


# NOTE: These lookup functions are intentionally simple one-line implementations.
# They provide semantic meaning for dictionary lookups with sensible defaults.
# Short body does not mean incomplete - these are complete implementations.

def get_issue_symbol(issue_type: str) -> tuple:
    """Get emoji and symbol for an issue type."""
    default = ("🔹", "•")
    if not issue_type:
        return default
    symbol = ISSUE_SYMBOLS.get(issue_type)
    if symbol:
        return symbol
    return ISSUE_SYMBOLS.get(issue_type.upper(), default)


def get_issue_action_parts(issue_type: str) -> tuple:
    """Get action parts (prefix, suffix) for an issue type."""
    default = ("fix", "")
    if not issue_type:
        return default
    parts = ISSUE_DESCRIPTIONS.get(issue_type)
    if parts:
        return parts
    return ISSUE_DESCRIPTIONS.get(issue_type.upper(), default)


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


def split_docs_to_read(docs_to_read: List[str], target_dir: Path) -> tuple[List[str], List[str]]:
    """Split docs into existing and missing paths relative to target_dir."""
    existing = []
    missing = []
    for doc in docs_to_read:
        if not doc:
            continue
        doc_path = Path(doc)
        candidate = doc_path if doc_path.is_absolute() else (target_dir / doc_path)
        if candidate.exists():
            existing.append(doc)
        else:
            missing.append(doc)
    return existing, missing


def _detect_recent_issue_number(target_dir: Path, max_commits: int = 5) -> Optional[int]:
    """Detect a recent issue number from the last few commit messages."""
    import subprocess
    import re

    try:
        result = subprocess.run(
            ["git", "log", f"-{max_commits}", "--pretty=%s"],
            cwd=target_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return None
        for line in result.stdout.splitlines():
            match = re.search(r"#(\d+)", line)
            if match:
                return int(match.group(1))
    except Exception:
        return None
    return None


def build_agent_prompt(
    issue: Any,  # DoctorIssue
    instructions: Dict[str, Any],
    target_dir: Path,
    github_issue_number: Optional[int] = None,
) -> str:
    """Build the full prompt for the repair agent."""
    existing_docs, missing_docs = split_docs_to_read(instructions["docs_to_read"], target_dir)
    docs_list = "\n".join(f"- {d}" for d in existing_docs) or "- (no docs found)"
    missing_section = ""
    if missing_docs:
        missing_list = "\n".join(f"- {d}" for d in missing_docs)
        missing_section = f"""
## Missing Docs at Prompt Time
{missing_list}

If any missing docs should exist, locate the correct paths before proceeding.
"""

    if github_issue_number is None:
        github_issue_number = _detect_recent_issue_number(target_dir)

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
{missing_section}

{instructions['prompt']}

## After Completion
1. Commit your changes with a descriptive message using a type prefix (e.g., "fix:", "docs:", "refactor:"){f' and include "Closes #{github_issue_number}"' if github_issue_number else ''}
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
                tool_input = content.get("input", {})
                if tool_input:
                    # Show key params briefly
                    params = []
                    for k, v in list(tool_input.items())[:2]:
                        val = str(v)[:40] + "..." if len(str(v)) > 40 else str(v)
                        params.append(f"{k}={val}")
                    param_str = ", ".join(params)
                    return f"\n**🔧 {tool_name}**(`{param_str}`)\n"
                return f"\n**🔧 {tool_name}**\n"

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
    config: DoctorConfig, # New: DoctorConfig to manage fallback status
    github_issue_number: Optional[int] = None,
    escalation_decisions: Optional[List[EscalationDecision]] = None,
    agent_id: Optional[str] = None,
    session_dir: Optional[Path] = None,
    agent_symbol: Optional[str] = None,
    agent_provider: str = "claude",
) -> RepairResult:
    """
    Async version of spawn_repair_agent for TUI integration.

    Args:
        issue: The DoctorIssue to fix
        target_dir: Project directory
        on_output: Async callback for each output line
        instructions: Instructions from get_issue_instructions()
        github_issue_number: Optional GitHub issue number
        escalation_decisions: Optional user decisions for ESCALATION issues
        agent_id: Unique identifier for this agent
        session_dir: Repair session directory (e.g., .ngram/repairs/2024-01-15_14-30-00/)
        agent_symbol: Symbol for this agent (e.g., "ninja" for 🥷)
        agent_provider: Agent provider name (claude or codex)

    Returns:
        RepairResult with success status and output
    """
    # Handle ESCALATION decisions
    if issue.issue_type == "ESCALATION" and escalation_decisions:
        decisions_text = "\n".join(
            f"- **{d.conflict_title}**: {d.decision}"
            for d in escalation_decisions if not d.passed
        )
        instructions["prompt"] = instructions["prompt"].replace(
            "{escalation_decisions}",
            decisions_text or "(No decisions provided)"
        )
    elif issue.issue_type == "ESCALATION":
        instructions["prompt"] = instructions["prompt"].replace(
            "{escalation_decisions}",
            "(No decisions provided - skip this issue)"
        )

    agent_provider = normalize_agent(agent_provider)
    prompt = build_agent_prompt(issue, instructions, target_dir, github_issue_number)
    system_prompt = AGENT_SYSTEM_PROMPT + get_learnings_content(target_dir)

    GEMINI_PRIMARY_MODEL = "gemini-3-flash-preview"
    GEMINI_FALLBACK_MODEL = "gemini-2.5-flash"

    # Determine Gemini model, with fallback logic
    current_gemini_model = config.gemini_model_fallback_status.get(agent_id or "default_repair", GEMINI_PRIMARY_MODEL)
    current_attempt = 0
    max_attempts = 2 if agent_provider == "gemini" else 1
    text_output = []
    start_time = time.time()

    # Outer loop for model fallback retry
    try:
        while True:
            try:
                agent_cmd = build_agent_command(
                    agent_provider,
                    prompt=prompt,
                    system_prompt=system_prompt,
                    stream_json=(agent_provider == "claude"),
                    continue_session=False,
                    model_name=current_gemini_model if agent_provider == "gemini" else None, # Pass model name
                )

                start_time = time.time()
                text_output = []  # Reset text_output for each attempt

                import shutil

            except Exception as e:
                logger.error(f"Error during agent command build or execution: {e}")
                current_attempt += 1
                if agent_provider == "gemini" and current_gemini_model != GEMINI_FALLBACK_MODEL:
                    current_gemini_model = GEMINI_FALLBACK_MODEL
                    config.gemini_model_fallback_status[agent_id or "default_repair"] = current_gemini_model
                if current_attempt >= max_attempts:
                    logger.error(f"Max attempts ({max_attempts}) reached for {issue.path}. Giving up.")
                    raise
                continue  # Retry outer while loop

            # Create agent directory within session folder
            # Structure: .ngram/repairs/{timestamp}/{agent_symbol}/
            if session_dir and agent_symbol:
                # Use symbol name as folder (e.g., "ninja" for 🥷)
                agent_dir = session_dir / agent_symbol
            elif session_dir and agent_id:
                agent_dir = session_dir / agent_id
            elif agent_id:
                # Fallback to old structure
                agent_dir = target_dir / ".ngram" / "agents" / "repair" / agent_id
            else:
                import uuid
                agent_dir = target_dir / ".ngram" / "agents" / "repair" / f"agent-{uuid.uuid4().hex[:8]}"

            agent_dir.mkdir(parents=True, exist_ok=True)

            # Copy CLAUDE.md so agent has context
            claude_md_src = target_dir / ".ngram" / "CLAUDE.md"
            claude_md_dst = agent_dir / "CLAUDE.md"
            agents_md_src = target_dir / "AGENTS.md"
            agents_md_dst = agent_dir / "AGENTS.md"
            if claude_md_src.exists() and not claude_md_dst.exists():
                shutil.copy(claude_md_src, claude_md_dst)
            if agents_md_src.exists():
                agents_md_dst.write_text(agents_md_src.read_text())
            elif claude_md_src.exists():
                agents_md_dst.write_text(claude_md_src.read_text())

            # Write issue info to agent folder for reference
            issue_info = agent_dir / "ISSUE.md"
            issue_info.write_text(f"""# Repair Task

**Issue Type:** {issue.issue_type}
**Severity:** {issue.severity}
**Target:** {issue.path}

## Instructions
{instructions.get('prompt', 'No instructions provided')}

## Docs to Read
{chr(10).join('- ' + d for d in instructions.get('docs_to_read', []))}
""")

            head_before = _get_git_head(target_dir)

            # Run subprocess in thread pool to keep UI responsive
            import subprocess as sync_subprocess
            import concurrent.futures

            def run_agent_sync():
                """Run agent synchronously in thread, return output lines."""
                output_lines = []
                try:
                    proc = sync_subprocess.Popen(
                        agent_cmd.cmd,
                        cwd=agent_dir,
                        stdout=sync_subprocess.PIPE,
                        stderr=sync_subprocess.STDOUT,
                        stdin=sync_subprocess.PIPE if agent_cmd.stdin else None,
                        text=False,
                    )
                    if agent_cmd.stdin:
                        proc.stdin.write((agent_cmd.stdin + "\n").encode())
                        proc.stdin.close()

                    for line in proc.stdout:
                        line_str = line.decode(errors='replace').strip()
                        if not line_str:
                            continue
                        parsed = parse_stream_json_line(line_str)
                        if parsed:
                            output_lines.append(parsed)
                        elif not line_str.startswith("{"):
                            output_lines.append(line_str)

                    proc.wait()
                    return output_lines, proc.returncode
                except Exception as e:
                    output_lines.append(f"ERROR: {e}")
                    return output_lines, -1

            loop = asyncio.get_event_loop()
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = loop.run_in_executor(pool, run_agent_sync)
                last_callback = time.time()
                while not future.done():
                    await asyncio.sleep(0.5)  # Yield to UI every 500ms
                    now = time.time()
                    if (now - last_callback) > 5.0:
                        await on_output("")  # Heartbeat
                        last_callback = now

                text_output, returncode = await asyncio.wrap_future(future)
            duration = time.time() - start_time

            head_after = _get_git_head(target_dir)
            readable_output = "\n".join(text_output)
            success = bool(head_before and head_after and head_before != head_after)
            decisions = parse_decisions_from_output(readable_output)

            # Workaround: Delete GEMINI.md created by gemini CLI in agent's directory
            if agent_provider == "gemini":
                gemini_md_path = agent_dir / "GEMINI.md"
                if gemini_md_path.exists():
                    gemini_md_path.unlink()
                    print(f"Cleaned up: Deleted {gemini_md_path}")

            error = None
            if returncode != 0:
                error = f"Exit code: {returncode}"
            elif not success:
                error = "No git commit detected"

            return RepairResult(
                issue_type=issue.issue_type,
                target_path=issue.path,
                success=success,
                agent_output=readable_output,
                duration_seconds=duration,
                error=error,
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
