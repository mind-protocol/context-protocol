"""
Init command for ngram CLI.

Initializes the ngram in a project directory by:
- Copying protocol files to .ngram/
- Creating/updating .ngram/CLAUDE.md and root AGENTS.md with protocol bootstrap (inlined content)
"""
# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md

import shutil
import os
from pathlib import Path

from .utils import get_templates_path
from .repo_overview import generate_and_save


def _build_claude_addition(templates_path: Path) -> str:
    """Build CLAUDE.md content with inlined PRINCIPLES and PROTOCOL.

    Instead of using @ references (which Claude doesn't expand),
    we inline the actual content of the files.
    """
    principles_path = templates_path / "ngram" / "PRINCIPLES.md"
    protocol_path = templates_path / "ngram" / "PROTOCOL.md"

    principles_content = principles_path.read_text() if principles_path.exists() else ""
    protocol_content = protocol_path.read_text() if protocol_path.exists() else ""

    return f"""# ngram

{principles_content}

---

{protocol_content}

---

## Before Any Task

Check project state:
```
.ngram/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

## Choose Your VIEW

Based on your task, load ONE view from `.ngram/views/`:

| Task | VIEW |
|------|------|
| Processing raw data (chats, PDFs) | VIEW_Ingest_Process_Raw_Data_Sources.md |
| Getting oriented | VIEW_Onboard_Understand_Existing_Codebase.md |
| Analyzing structure | VIEW_Analyze_Structural_Analysis.md |
| Defining architecture | VIEW_Specify_Design_Vision_And_Architecture.md |
| Writing/modifying code | VIEW_Implement_Write_Or_Modify_Code.md |
| Adding features | VIEW_Extend_Add_Features_To_Existing.md |
| Pair programming | VIEW_Collaborate_Pair_Program_With_Human.md |
| Writing tests | VIEW_Test_Write_Tests_And_Verify.md |
| Debugging | VIEW_Debug_Investigate_And_Fix_Issues.md |
| Reviewing changes | VIEW_Review_Evaluate_Changes.md |
| Refactoring | VIEW_Refactor_Improve_Code_Structure.md |

## After Any Change

Update `.ngram/state/SYNC_Project_State.md` with what you did.
If you changed a module, update its `docs/{{area}}/{{module}}/SYNC_*.md` too.

## CLI Commands

The `ngram` command is available for project management:

```bash
ngram init [--force]    # Initialize/re-sync protocol files
ngram validate          # Check protocol invariants
ngram doctor            # Health checks (auto-archives large SYNCs)
ngram sync              # Show SYNC status (auto-archives large SYNCs)
ngram repair [--max N]  # Auto-fix issues using Claude Code agents
ngram context <file>    # Get doc context for a file
ngram prompt            # Generate bootstrap prompt for LLM
ngram overview          # Generate repo map with file tree, links, definitions
```

### Overview Command

`ngram overview` generates a comprehensive repository map:

- File tree with character counts (respecting .gitignore/.ngramignore)
- Bidirectional links: code→docs (DOCS: markers), docs→code (references)
- Section headers from markdown, function definitions from code
- Local imports (stdlib/npm filtered out)
- Module dependencies from modules.yaml
- Output: `docs/map.{{md|yaml|json}}`

Options: `--dir PATH`, `--format {{md,yaml,json}}`
"""


def _build_agents_addition(templates_path: Path) -> str:
    """Build AGENTS.md content by appending Codex-specific guidance."""
    claude_content = _build_claude_addition(templates_path)
    codex_addition_path = templates_path / "CODEX_SYSTEM_PROMPT_ADDITION.md"
    codex_addition = codex_addition_path.read_text() if codex_addition_path.exists() else ""
    if codex_addition:
        return f"{claude_content}\n\n{codex_addition}"
    return claude_content


def _build_manager_agents_addition(templates_path: Path) -> str:
    """Build manager AGENTS.md content from manager CLAUDE.md plus Codex guidance."""
    manager_claude_path = templates_path / "ngram" / "agents" / "manager" / "CLAUDE.md"
    manager_content = manager_claude_path.read_text() if manager_claude_path.exists() else ""
    codex_addition_path = templates_path / "CODEX_SYSTEM_PROMPT_ADDITION.md"
    codex_addition = codex_addition_path.read_text() if codex_addition_path.exists() else ""
    if codex_addition:
        return f"{manager_content}\n\n{codex_addition}"
    return manager_content


def init_protocol(target_dir: Path, force: bool = False) -> bool:
    """
    Initialize the ngram in a project directory.

    Copies protocol files and updates .ngram/CLAUDE.md and root AGENTS.md with inlined content.

    Args:
        target_dir: The project directory to initialize
        force: If True, overwrite existing .ngram/
    Returns:
        True if successful, False otherwise
    """
    try:
        templates_path = get_templates_path()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return False

    # Source paths
    protocol_source = templates_path / "ngram"
    modules_yaml_source = templates_path / "modules.yaml"
    ignore_source = templates_path / "ngramignore"

    # Destination paths
    protocol_dest = target_dir / ".ngram"
    modules_yaml_dest = target_dir / "modules.yaml"
    ignore_dest = target_dir / ".ngramignore"

    claude_md = protocol_dest / "CLAUDE.md"
    agents_md = target_dir / "AGENTS.md"
    manager_agents_md = protocol_dest / "agents" / "manager" / "AGENTS.md"

    # Check if already initialized
    if protocol_dest.exists() and not force:
        print(f"Error: {protocol_dest} already exists.")
        print("Use --force to overwrite.")
        return False

    # Preserve LEARNINGS files before reinitialization
    preserved_learnings = {}
    if protocol_dest.exists():
        views_dir = protocol_dest / "views"
        if views_dir.exists():
            for learnings_file in views_dir.glob("*_LEARNINGS.md"):
                content = learnings_file.read_text()
                # Only preserve if it has actual learnings (not just template)
                if "## Learnings" in content and content.count("\n") > 10:
                    preserved_learnings[learnings_file.name] = content
                    print(f"  ○ Preserving: {learnings_file.name}")
            # Also check GLOBAL_LEARNINGS.md
            global_learnings = views_dir / "GLOBAL_LEARNINGS.md"
            if global_learnings.exists():
                content = global_learnings.read_text()
                if "## Learnings" in content and content.count("\n") > 10:
                    preserved_learnings["GLOBAL_LEARNINGS.md"] = content
                    print(f"  ○ Preserving: GLOBAL_LEARNINGS.md")

    # Copy protocol files
    def copy_protocol_partial(src: Path, dst: Path) -> None:
        for root, dirs, files in os.walk(src):
            rel = Path(root).relative_to(src)
            target_root = dst / rel
            target_root.mkdir(parents=True, exist_ok=True)
            for dirname in dirs:
                (target_root / dirname).mkdir(parents=True, exist_ok=True)
            for filename in files:
                src_path = Path(root) / filename
                dst_path = target_root / filename
                try:
                    shutil.copy2(src_path, dst_path)
                except PermissionError:
                    print(f"  ○ Skipped (permission): {dst_path}")

    if protocol_dest.exists():
        try:
            shutil.rmtree(protocol_dest)
            shutil.copytree(protocol_source, protocol_dest)
            print(f"✓ Created: {protocol_dest}/")
        except PermissionError:
            print(f"  ○ Permission denied removing {protocol_dest}, attempting partial refresh")
            copy_protocol_partial(protocol_source, protocol_dest)
    else:
        shutil.copytree(protocol_source, protocol_dest)
        print(f"✓ Created: {protocol_dest}/")

    # Restore preserved LEARNINGS files
    if preserved_learnings:
        views_dir = protocol_dest / "views"
        for filename, content in preserved_learnings.items():
            learnings_path = views_dir / filename
            try:
                learnings_path.write_text(content)
                print(f"  ✓ Restored: {filename}")
            except PermissionError:
                print(f"  ○ Skipped (permission): {learnings_path}")

    # Copy modules.yaml to project root (if not exists or force)
    if not modules_yaml_dest.exists() or force:
        if modules_yaml_source.exists():
            try:
                shutil.copy2(modules_yaml_source, modules_yaml_dest)
                print(f"✓ Created: {modules_yaml_dest}")
            except PermissionError:
                print(f"  ○ Skipped (permission): {modules_yaml_dest}")
    else:
        print(f"○ {modules_yaml_dest} already exists")

    # Copy .ngramignore to project root (if not exists or force)
    if not ignore_dest.exists() or force:
        if ignore_source.exists():
            try:
                shutil.copy2(ignore_source, ignore_dest)
                print(f"✓ Created: {ignore_dest}")
            except PermissionError:
                print(f"  ○ Skipped (permission): {ignore_dest}")
    else:
        print(f"○ {ignore_dest} already exists")

    # Add agent working directories to .gitignore
    gitignore_path = target_dir / ".gitignore"
    ngram_gitignore_entries = [
        "# ngram agent working directories",
        ".ngram/agents/repair/",
        ".ngram/traces/",
    ]
    try:
        existing = gitignore_path.read_text() if gitignore_path.exists() else ""
        missing_entries = [e for e in ngram_gitignore_entries if e not in existing]
        if missing_entries:
            with open(gitignore_path, "a") as f:
                f.write("\n" + "\n".join(missing_entries) + "\n")
            print(f"✓ Updated: {gitignore_path}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {gitignore_path}")

    # Build CLAUDE.md content with inlined PRINCIPLES and PROTOCOL
    # (Claude doesn't expand @ references, so we inline the actual content)
    claude_content = _build_claude_addition(templates_path)
    agents_content = _build_agents_addition(templates_path)
    manager_agents_content = _build_manager_agents_addition(templates_path)

    gemini_addition_path = templates_path / "GEMINI_SYSTEM_PROMPT_ADDITION.md"
    gemini_addition = gemini_addition_path.read_text() if gemini_addition_path.exists() else ""
    gemini_content = f"{claude_content}\n\n---\n\n{gemini_addition}" if gemini_addition else claude_content

    # Always write/overwrite CLAUDE.md with fresh inlined content
    # This ensures the latest PRINCIPLES and PROTOCOL are always included
    try:
        if claude_md.exists():
            claude_md.write_text(claude_content)
            print(f"✓ Updated: {claude_md}")
        else:
            claude_md.write_text(claude_content)
            print(f"✓ Created: {claude_md}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {claude_md}")

    gemini_md = protocol_dest / "GEMINI.md"
    try:
        gemini_md.write_text(gemini_content)
        print(f"✓ Created: {gemini_md}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {gemini_md}")

    try:
        agents_md.write_text(agents_content)
        print(f"✓ Updated: {agents_md}")
    except PermissionError:
        print(f"  ○ Skipped (permission): {agents_md}")

    if manager_agents_content:
        try:
            manager_agents_md.parent.mkdir(parents=True, exist_ok=True)
            manager_agents_md.write_text(manager_agents_content)
            print(f"✓ Updated: {manager_agents_md}")
        except PermissionError:
            print(f"  ○ Skipped (permission): {manager_agents_md}")

    # Generate repository map
    print()
    print("Generating repository map...")
    try:
        output_path = generate_and_save(target_dir, output_format="md")
        print(f"✓ Created: {output_path}")
    except Exception as e:
        print(f"○ Map generation skipped: {e}")

    print()
    print("ngram initialized!")
    print()
    print("Next steps:")
    print("  1. Read .ngram/PROTOCOL.md")
    print("  2. Update .ngram/state/SYNC_Project_State.md")
    print("  3. Load the VIEW matching your task when working")
    print()
    print("To bootstrap an LLM, run:")
    print(f"  ngram prompt --dir {target_dir}")

    return True
