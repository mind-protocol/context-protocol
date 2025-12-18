"""
Init command for ngram CLI.

Initializes the ngram in a project directory by:
- Copying protocol files to .ngram/
- Creating/updating CLAUDE.md with protocol bootstrap
"""

import shutil
from pathlib import Path

from .utils import get_templates_path


def init_protocol(target_dir: Path, force: bool = False, claude_md_dir: Path = None) -> bool:
    """
    Initialize the ngram in a project directory.

    Copies protocol files and updates CLAUDE.md.

    Args:
        target_dir: The project directory to initialize
        force: If True, overwrite existing .ngram/
        claude_md_dir: Directory for CLAUDE.md (default: target_dir)

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
    claude_addition = templates_path / "CLAUDE_ADDITION.md"
    modules_yaml_source = templates_path / "modules.yaml"
    ignore_source = templates_path / "ngramignore"

    # Destination paths
    protocol_dest = target_dir / ".ngram"
    modules_yaml_dest = target_dir / "modules.yaml"
    ignore_dest = target_dir / ".ngramignore"

    # CLAUDE.md location - can be customized
    if claude_md_dir:
        claude_md_dir = Path(claude_md_dir)
        claude_md_dir.mkdir(parents=True, exist_ok=True)
        claude_md = claude_md_dir / "CLAUDE.md"
    else:
        claude_md = target_dir / "CLAUDE.md"

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
    if protocol_dest.exists():
        shutil.rmtree(protocol_dest)

    shutil.copytree(protocol_source, protocol_dest)
    print(f"✓ Created: {protocol_dest}/")

    # Restore preserved LEARNINGS files
    if preserved_learnings:
        views_dir = protocol_dest / "views"
        for filename, content in preserved_learnings.items():
            learnings_path = views_dir / filename
            learnings_path.write_text(content)
            print(f"  ✓ Restored: {filename}")

    # Copy modules.yaml to project root (if not exists or force)
    if not modules_yaml_dest.exists() or force:
        if modules_yaml_source.exists():
            shutil.copy2(modules_yaml_source, modules_yaml_dest)
            print(f"✓ Created: {modules_yaml_dest}")
    else:
        print(f"○ {modules_yaml_dest} already exists")

    # Copy .ngramignore to project root (if not exists or force)
    if not ignore_dest.exists() or force:
        if ignore_source.exists():
            shutil.copy2(ignore_source, ignore_dest)
            print(f"✓ Created: {ignore_dest}")
    else:
        print(f"○ {ignore_dest} already exists")

    # Create/update CLAUDE.md with @ includes for system prompt
    # This loads PRINCIPLES and PROTOCOL directly into context
    claude_includes = """# ngram

@.ngram/PRINCIPLES.md

---

@.ngram/PROTOCOL.md

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
If you changed a module, update its `docs/{area}/{module}/SYNC_*.md` too.
"""

    if claude_md.exists():
        existing_content = claude_md.read_text()
        if "@.ngram/PRINCIPLES.md" in existing_content or "## ngram" in existing_content:
            print(f"○ {claude_md} already has ngram section")
        else:
            with open(claude_md, "a") as f:
                f.write("\n\n")
                f.write(claude_includes)
            print(f"✓ Updated: {claude_md}")
    else:
        claude_md.write_text(claude_includes)
        print(f"✓ Created: {claude_md}")

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
