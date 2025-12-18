"""
Repair command for Context Protocol CLI.

Automatically fixes project health issues by spawning Claude Code agents.
Each agent follows the protocol: read docs, fix issue, update SYNC.
"""

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from .doctor import run_doctor, load_doctor_config, DoctorIssue


def load_github_issue_mapping(target_dir: Path) -> Dict[str, int]:
    """Load GitHub issue mapping from health report or tracking file."""
    mapping = {}

    # Try to load from a tracking file first
    tracking_path = target_dir / ".context-protocol" / "state" / "github_issues.json"
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
    tracking_path = target_dir / ".context-protocol" / "state" / "github_issues.json"
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
}

DEPTH_DOCS = DEPTH_LINKS | {
    # Also create/update documentation content
    "UNDOCUMENTED",       # Create module docs
    "STALE_SYNC",         # Update stale SYNC files
    "PLACEHOLDER",        # Fill in placeholder content
    "INCOMPLETE_CHAIN",   # Create missing doc types
    "LARGE_DOC_MODULE",   # Reduce doc module size
}

DEPTH_FULL = DEPTH_DOCS | {
    # Also make code changes
    "MONOLITH",           # Split large files
    "STUB_IMPL",          # Implement stub functions
    "INCOMPLETE_IMPL",    # Complete empty functions
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


# Agent system prompt template
AGENT_SYSTEM_PROMPT = """You are a Context Protocol repair agent. Your job is to fix ONE specific issue in the project.

CRITICAL RULES:
1. FIRST: Read all documentation listed in "Docs to Read" before making changes
2. Follow the VIEW instructions exactly
3. After fixing, update the relevant SYNC file with what you changed
4. Keep changes minimal and focused on the specific issue
5. Do NOT make unrelated changes or "improvements"
6. Report completion status clearly at the end

BIDIRECTIONAL LINKS:
- When creating new docs, add CHAIN section linking to related docs
- When modifying code, ensure DOCS: reference points to correct docs
- When creating module docs, add mapping to .context-protocol/modules.yaml

GIT COMMITS:
- After making changes, commit with a descriptive message
- If a GitHub issue number is provided, include "Closes #NUMBER" in the commit message
- Use conventional commit format when appropriate (fix:, feat:, docs:, refactor:)
"""


def get_issue_instructions(issue: DoctorIssue, target_dir: Path) -> Dict[str, Any]:
    """Generate specific instructions for each issue type."""

    instructions = {
        "MONOLITH": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Split a monolith file into smaller modules",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Refactor_Improve_Code_Structure.md",
                ".context-protocol/PRINCIPLES.md",
            ],
            "prompt": f"""## Task: Split Monolith File

**Target:** `{issue.path}`
**Problem:** {issue.message}
{f"**Suggestion:** {issue.suggestion}" if issue.suggestion else ""}

## Steps:

1. Read the VIEW and PRINCIPLES docs listed above
2. Read the target file to understand its structure
3. Identify the largest function/class mentioned in the suggestion
4. Create a new file for the extracted code (e.g., `{Path(issue.path).stem}_utils.py`)
5. Move the function/class to the new file
6. Update imports in the original file
7. Run any existing tests to verify nothing broke
8. Update SYNC with what you changed

## Success Criteria:
- Original file is shorter
- Code still works (tests pass if they exist)
- Imports are correct
- SYNC is updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [".context-protocol/state/SYNC_Project_State.md"],
        },

        "UNDOCUMENTED": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Create documentation for undocumented code",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
                ".context-protocol/templates/PATTERNS_TEMPLATE.md",
                ".context-protocol/templates/SYNC_TEMPLATE.md",
            ],
            "prompt": f"""## Task: Document Module

**Target:** `{issue.path}`
**Problem:** {issue.message}

## Steps:

1. Read the VIEW and template docs listed above
2. Read the code in `{issue.path}` to understand what it does
3. Add mapping to `.context-protocol/modules.yaml`:
   ```yaml
   modules:
     {Path(issue.path).name}:
       code: "{issue.path}/**"
       docs: "docs/{issue.path}/"
       maturity: DESIGNING
   ```
4. Create minimum viable docs:
   - `docs/{issue.path}/PATTERNS_*.md` - why this module exists, design approach
   - `docs/{issue.path}/SYNC_*.md` - current state
5. Add DOCS: reference to main source file
6. Update SYNC_Project_State.md with what you created

## Success Criteria:
- modules.yaml has mapping
- PATTERNS doc exists with actual content (not placeholders)
- SYNC doc exists
- Main source file has DOCS: reference

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [
                ".context-protocol/modules.yaml",
                ".context-protocol/state/SYNC_Project_State.md",
            ],
        },

        "STALE_SYNC": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Update stale SYNC file",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Implement_Write_Or_Modify_Code.md",
                issue.path,  # The stale SYNC file itself
            ],
            "prompt": f"""## Task: Update Stale SYNC File

**Target:** `{issue.path}`
**Problem:** {issue.message}

## Steps:

1. Read the VIEW doc and the current SYNC file
2. Read the code/docs that this SYNC file describes
3. Compare current state with what SYNC says
4. Update SYNC to reflect reality:
   - Update LAST_UPDATED to today's date
   - Update STATUS if needed
   - Update CURRENT STATE section
   - Remove outdated information
   - Add any new developments
5. If the SYNC is for a module, also check if the module's code has changed

## Success Criteria:
- LAST_UPDATED is today's date
- Content reflects current reality
- No outdated information

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "PLACEHOLDER": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Fill in placeholder content",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
                issue.path,
            ],
            "prompt": f"""## Task: Fill In Placeholders

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Placeholders found:** {issue.details.get('placeholders', [])}

## Steps:

1. Read the VIEW doc and the file with placeholders
2. Identify each placeholder (like {{MODULE_NAME}}, {{DESCRIPTION}}, etc.)
3. Read related code/docs to understand what should replace each placeholder
4. Replace all placeholders with actual content
5. Ensure the document makes sense and is complete

## Success Criteria:
- No {{PLACEHOLDER}} patterns remain
- Content is meaningful, not generic
- Document is useful for agents

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "INCOMPLETE_CHAIN": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Complete documentation chain",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
            ],
            "prompt": f"""## Task: Complete Documentation Chain

**Target:** `{issue.path}`
**Missing docs:** {issue.details.get('missing', [])}
**Existing docs:** {issue.details.get('present', [])}

## Steps:

1. Read the VIEW doc
2. Read existing docs in `{issue.path}` to understand the module
3. For EACH missing doc type, create the file:
   - Use templates from `.context-protocol/templates/`
   - Fill with actual content based on the code
4. Ensure CHAIN sections link all docs together
5. Update SYNC with what you created

## Priority order for creation:
1. PATTERNS (if missing) - most important
2. IMPLEMENTATION (if missing) - code structure
3. SYNC (if missing) - current state
4. Others as needed

## Success Criteria:
- Missing doc types are created
- Content is real, not placeholders
- CHAIN sections link correctly

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "NO_DOCS_REF": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Add DOCS: reference to source file",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
            ],
            "prompt": f"""## Task: Add DOCS Reference

**Target:** `{issue.path}`
**Problem:** {issue.message}

## Steps:

1. Find the documentation for this code (check docs/ and .context-protocol/modules.yaml)
2. Add a DOCS: reference near the top of the file:
   - Python: `# DOCS: docs/path/to/PATTERNS_*.md`
   - JS/TS: `// DOCS: docs/path/to/PATTERNS_*.md`
3. If no docs exist, create minimum PATTERNS + SYNC docs first

## Success Criteria:
- Source file has DOCS: reference in header
- Reference points to existing doc file

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "BROKEN_IMPL_LINK": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Fix broken file references in IMPLEMENTATION doc",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
                issue.path,
            ],
            "prompt": f"""## Task: Fix Broken Implementation Links

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Missing files:** {issue.details.get('missing_files', [])}

## Steps:

1. Read the IMPLEMENTATION doc
2. For each missing file reference:
   - Search the codebase for the actual file location
   - If file was moved: update the path in the doc
   - If file was renamed: update the reference
   - If file was deleted: remove the reference or note it's deprecated
3. Verify all remaining file references point to existing files
4. Update SYNC with what you fixed

## Success Criteria:
- All file references in IMPLEMENTATION doc point to existing files
- No broken links remain
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "STUB_IMPL": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Implement stub functions",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Implement_Write_Or_Modify_Code.md",
                ".context-protocol/PRINCIPLES.md",
            ],
            "prompt": f"""## Task: Implement Stub Functions

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Stub indicators:** {issue.details.get('stubs', [])}

## Steps:

1. Read the file and identify all stub patterns (TODO, NotImplementedError, pass, etc.)
2. For each stub function:
   - Understand what it should do from context (docstring, function name, callers)
   - Implement the actual logic
   - Remove the stub marker
3. If you cannot implement (missing requirements), document why in SYNC
4. Run any existing tests to verify implementations work

## Success Criteria:
- Stub functions have real implementations
- No NotImplementedError, TODO in function bodies
- Tests pass (if they exist)
- SYNC updated with what was implemented

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [".context-protocol/state/SYNC_Project_State.md"],
        },

        "INCOMPLETE_IMPL": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Complete empty functions",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Implement_Write_Or_Modify_Code.md",
            ],
            "prompt": f"""## Task: Complete Empty Functions

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Empty functions:** {[f['name'] for f in issue.details.get('empty_functions', [])]}

## Steps:

1. Read the file and find empty functions (only have pass, docstring, or trivial body)
2. For each empty function:
   - Understand its purpose from name, docstring, and how it's called
   - Implement the logic
3. If a function should remain empty (abstract base, protocol), add a comment explaining why
4. Update SYNC with implementations added

## Success Criteria:
- Empty functions have real implementations
- Or have comments explaining why they're intentionally empty
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [".context-protocol/state/SYNC_Project_State.md"],
        },

        "UNDOC_IMPL": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Document implementation file",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
            ],
            "prompt": f"""## Task: Document Implementation File

**Target:** `{issue.path}`
**Problem:** {issue.message}

## Steps:

1. Read the source file to understand what it does
2. Find the relevant IMPLEMENTATION_*.md doc (or create one if none exists)
3. Add the file to the IMPLEMENTATION doc with:
   - File path
   - Brief description of what it does
   - Key functions/classes it contains
   - How it fits in the data flow
4. Update the CHAIN section if needed
5. Update SYNC

## Success Criteria:
- File is referenced in an IMPLEMENTATION doc
- Description is accurate and helpful
- Bidirectional link established

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "LARGE_DOC_MODULE": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Reduce documentation module size",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Refactor_Improve_Code_Structure.md",
                issue.path,
            ],
            "prompt": f"""## Task: Reduce Documentation Size

**Target:** `{issue.path}`
**Problem:** {issue.message}
**File sizes:** {[(f['file'], f'{f["chars"]//1000}K') for f in issue.details.get('file_sizes', [])[:5]]}

## Steps:

1. Read the docs in the module folder
2. Identify content that can be reduced:
   - Old/archived sections -> move to dated archive file
   - Duplicate information -> consolidate
   - Verbose explanations -> make concise
   - Implementation details that changed -> update or remove
3. For large individual files, consider splitting into focused sub-docs
4. Update CHAIN sections after any splits
5. Update SYNC with what was reorganized

## Archiving pattern:
- Create `{issue.path}/archive/SYNC_archive_2024-12.md` for old content
- Keep only current state in main docs

## Success Criteria:
- Total chars under 50K
- Content is current and relevant
- No duplicate information
- CHAIN links still work

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "YAML_DRIFT": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Fix modules.yaml drift",
            "docs_to_read": [
                ".context-protocol/views/VIEW_Document_Create_Module_Documentation.md",
                ".context-protocol/modules.yaml",
            ],
            "prompt": f"""## Task: Fix YAML Drift

**Target:** `{issue.path}`
**Module:** {issue.details.get('module', 'unknown')}
**Issues:** {issue.details.get('issues', [])}

## Steps:

1. Read modules.yaml and find the module entry
2. For each drift issue:
   - **Path not found**: Search for where the code/docs actually are, update the path
   - **Dependency not defined**: Either add the missing module or remove the dependency
3. If the module was completely removed, delete its entry from modules.yaml
4. Verify all paths now exist
5. Update SYNC with what was fixed

## Success Criteria:
- All code/docs/tests paths in the module entry point to existing directories
- All dependencies reference defined modules
- modules.yaml reflects reality

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [".context-protocol/modules.yaml"],
        },
    }

    return instructions.get(issue.issue_type, {
        "view": "VIEW_Implement_Write_Or_Modify_Code.md",
        "description": f"Fix {issue.issue_type} issue",
        "docs_to_read": [".context-protocol/PROTOCOL.md"],
        "prompt": f"""## Task: Fix Issue

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Suggestion:** {issue.suggestion}

Review and fix this issue following the Context Protocol.

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
        "docs_to_update": [],
    })


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

    return f"""# Context Protocol Repair Task

## Issue Type: {issue.issue_type}
## Severity: {issue.severity}
{github_section}
## VIEW to Follow
Load and follow: `.context-protocol/views/{instructions['view']}`

## Docs to Read FIRST (before any changes)
{docs_list}

{instructions['prompt']}

## After Completion
1. Commit your changes with a descriptive message{f' (include "Closes #{github_issue_number}")' if github_issue_number else ''}
2. Update `.context-protocol/state/SYNC_Project_State.md` with:
   - What you fixed
   - Files created/modified
   - Any issues encountered
"""


def spawn_repair_agent(
    issue: DoctorIssue,
    target_dir: Path,
    dry_run: bool = False,
    github_issue_number: Optional[int] = None,
) -> RepairResult:
    """Spawn a Claude Code agent to fix a single issue."""

    instructions = get_issue_instructions(issue, target_dir)
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

    # Build the claude command
    cmd = [
        "claude",
        "-p", prompt,
        "--dangerously-skip-permissions",
        "--append-system-prompt", AGENT_SYSTEM_PROMPT,
        "--verbose",
        "--output-format", "stream-json",
    ]

    start_time = time.time()
    output_lines = []

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

        # Stream output in real-time
        print()  # Newline before agent output
        for line in process.stdout:
            output_lines.append(line)
            # Print streamed output with indent
            sys.stdout.write(f"    {line}")
            sys.stdout.flush()

        process.wait(timeout=600)
        duration = time.time() - start_time
        output = "".join(output_lines)

        # Check for success markers in output
        success = "REPAIR COMPLETE" in output and "REPAIR FAILED" not in output

        return RepairResult(
            issue_type=issue.issue_type,
            target_path=issue.path,
            success=success,
            agent_output=output,
            duration_seconds=duration,
            error=None if process.returncode == 0 else f"Exit code: {process.returncode}",
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


def generate_final_report(
    before_results: Dict[str, Any],
    after_results: Dict[str, Any],
    repair_results: List[RepairResult],
    target_dir: Path,
) -> str:
    """Generate a final report summarizing all repairs."""

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
    lines.append("# Context Protocol Repair Report")
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

    # Remaining issues
    if after_results["summary"]["critical"] > 0 or after_results["summary"]["warning"] > 0:
        lines.append("## Remaining Issues")
        lines.append("")
        lines.append("Run `context-protocol doctor` for details on remaining issues.")
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
    lines.append("*Generated by `context-protocol repair`*")

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


def repair_command(
    target_dir: Path,
    max_issues: Optional[int] = None,
    issue_types: Optional[List[str]] = None,
    depth: str = "docs",
    dry_run: bool = False,
) -> int:
    """Run the repair command."""

    depth_labels = {
        "links": "Links only (refs, mappings)",
        "docs": "Links + Documentation",
        "full": "Full (links + docs + code)",
    }

    print(f"🔧 Context Protocol Repair")
    print(f"{'='*60}")
    print(f"  Depth: {depth_labels.get(depth, depth)}")
    print()

    # Step 1: Run doctor to get issues
    print("📋 Step 1: Analyzing project health...")
    print()
    config = load_doctor_config(target_dir)
    before_results = run_doctor(target_dir, config)

    print(f"  Health Score: {before_results['score']}/100")
    print(f"  Critical: {before_results['summary']['critical']}")
    print(f"  Warnings: {before_results['summary']['warning']}")
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

    if not all_issues:
        print(f"✅ No issues to repair at depth '{depth}'!")
        return 0

    # Limit number of issues if specified
    if max_issues is not None:
        issues_to_fix = all_issues[:max_issues]
    else:
        issues_to_fix = all_issues

    # Step 2: Show the repair plan
    print(f"📝 Step 2: Repair Plan")
    print()

    # Group by type for display
    from collections import Counter
    type_counts = Counter(i.issue_type for i in issues_to_fix)

    print(f"  Issues to fix: {len(issues_to_fix)}")
    if max_issues is not None and len(all_issues) > max_issues:
        print(f"  (Limited to {max_issues}, {len(all_issues) - max_issues} remaining)")
    print()
    print("  By type:")
    for issue_type, count in sorted(type_counts.items()):
        print(f"    • {issue_type}: {count}")
    print()
    print("  Files:")
    # Show first 10 files
    for i, issue in enumerate(issues_to_fix[:10]):
        print(f"    {i+1}. [{issue.issue_type}] {issue.path}")
    if len(issues_to_fix) > 10:
        print(f"    ... and {len(issues_to_fix) - 10} more")
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

    # Step 3: Execute repairs with progress bar
    print(f"🔨 Step 3: Executing repairs...")
    print()

    repair_results: List[RepairResult] = []

    for i, issue in enumerate(issues_to_fix, 1):
        # Update progress bar
        print_progress_bar(i - 1, len(issues_to_fix), status=f"Starting {issue.issue_type}...")
        print()  # Newline after progress bar

        # Get GitHub issue number if one exists for this path
        github_issue_num = github_mapping.get(issue.path)
        github_info = f" (#{github_issue_num})" if github_issue_num else ""
        print(f"\n  [{i}/{len(issues_to_fix)}] {issue.issue_type}: {issue.path}{github_info}")

        result = spawn_repair_agent(
            issue,
            target_dir,
            dry_run=False,
            github_issue_number=github_issue_num,
        )
        repair_results.append(result)

        if result.success:
            print(f"\n  ✓ Complete ({result.duration_seconds:.1f}s)")
        else:
            print(f"\n  ✗ Failed: {result.error or 'Unknown error'}")

    # Final progress bar
    print_progress_bar(len(issues_to_fix), len(issues_to_fix), status="Done!")
    print("\n")

    # Step 4: Run doctor again
    print("📊 Step 4: Running final health check...")
    after_results = run_doctor(target_dir, config)

    print(f"  Health Score: {after_results['score']}/100")
    print(f"  Critical: {after_results['summary']['critical']}")
    print(f"  Warnings: {after_results['summary']['warning']}")
    print()

    # Step 5: Generate report
    print("📄 Step 5: Generating report...")
    report = generate_final_report(before_results, after_results, repair_results, target_dir)

    # Save report
    report_path = target_dir / ".context-protocol" / "state" / "REPAIR_REPORT.md"
    if report_path.parent.exists():
        report_path.write_text(report)
        print(f"  Saved to {report_path.relative_to(target_dir)}")

    print()

    # Summary
    successful = len([r for r in repair_results if r.success])
    print(f"{'='*60}")
    print(f"✅ Repair Complete: {successful}/{len(repair_results)} successful")
    print(f"📈 Health Score: {before_results['score']} → {after_results['score']}")
    print(f"{'='*60}")

    # Return exit code
    return 0 if successful == len(repair_results) else 1
