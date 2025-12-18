"""
Issue instructions for ngram repair agents.

This module contains the large instruction dictionary that maps issue types
to specific repair instructions. Extracted from repair.py to reduce file size.
"""

from pathlib import Path
from typing import Any, Dict

# Import DoctorIssue type for type hints
from .doctor import DoctorIssue


def get_issue_instructions(issue: DoctorIssue, target_dir: Path) -> Dict[str, Any]:
    """Generate specific instructions for each issue type."""

    instructions = {
        "MONOLITH": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Split a monolith file into smaller modules",
            "docs_to_read": [
                ".ngram/views/VIEW_Refactor_Improve_Code_Structure.md",
                ".ngram/PRINCIPLES.md",
                "modules.yaml",
            ],
            "prompt": f"""## Task: Split Monolith File

**Target:** `{issue.path}`
**Problem:** {issue.message}
{f"**Suggestion:** {issue.suggestion}" if issue.suggestion else ""}

## Steps:

1. Read the VIEW and PRINCIPLES docs listed above
2. Read the target file to understand its structure
3. Find the IMPLEMENTATION doc for this module (check modules.yaml for docs path)
4. Identify the largest function/class mentioned in the suggestion
5. Create a new file for the extracted code (e.g., `{Path(issue.path).stem}_utils.py`)
6. Move the function/class to the new file
7. Update imports in the original file
8. Run any existing tests to verify nothing broke

## MANDATORY: Update Documentation

**Refactoring is NOT complete without documentation updates.**

9. Update IMPLEMENTATION doc:
   - Add new file to CODE STRUCTURE tree
   - Add new file to File Responsibilities table
   - Count lines: `wc -l` for both original and new file
   - Update Status column (OK/WATCH/SPLIT) for both files
   - Update internal dependencies diagram

10. Update modules.yaml:
    - Add new file to appropriate section (subsystems or internal)
    - Add note about extraction if file still needs splitting

11. Update SYNC with:
    - Files extracted and their new names
    - Line counts before/after
    - What still needs extraction (if any)

## Success Criteria:
- Original file is shorter
- New file created with extracted code
- Code still works (tests pass if they exist)
- Imports are correct
- **IMPLEMENTATION doc updated with new file**
- **modules.yaml updated with new file**
- **Line counts recorded in File Responsibilities**
- SYNC updated with extraction summary

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [".ngram/state/SYNC_Project_State.md"],
        },

        "UNDOCUMENTED": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Create documentation for undocumented code",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                ".ngram/PROTOCOL.md",
                ".ngram/templates/PATTERNS_TEMPLATE.md",
                ".ngram/templates/SYNC_TEMPLATE.md",
                "modules.yaml",
            ],
            "prompt": f"""## Task: Document Module

**Target:** `{issue.path}`
**Problem:** {issue.message}

## CRITICAL: Check for existing docs first

Before creating anything, search for existing documentation:
- `grep -r "{issue.path}" docs/` - check if this path is mentioned in existing docs
- Search `docs/**/IMPLEMENTATION_*.md` for references to this code
- Check `modules.yaml` for existing mappings that might cover this code
- If docs exist elsewhere, UPDATE the mapping instead of creating duplicates

## Steps:

1. Read the VIEW, PROTOCOL.md, and template docs listed above
2. Search for existing docs that might cover this code
3. If found: update `modules.yaml` mapping to link existing docs
4. If not found:
   a. Check `modules.yaml` and `docs/` to see existing naming patterns
   b. Read the code in `{issue.path}` to understand what it does
   c. Choose a descriptive module name (e.g., `cli`, `auth`) not the code path
   d. Follow the pattern: `docs/{{module}}/` or `docs/{{area}}/{{module}}/`
   e. Add mapping to `modules.yaml`
   f. Create minimum viable docs: PATTERNS_*.md + SYNC_*.md
5. Add DOCS: reference to main source file
6. Update SYNC_Project_State.md

## Success Criteria:
- modules.yaml has mapping (new or updated)
- PATTERNS doc exists with actual content
- SYNC doc exists
- NO duplicate documentation created

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [
                "modules.yaml",
                ".ngram/state/SYNC_Project_State.md",
            ],
        },

        "STALE_SYNC": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Update stale SYNC file",
            "docs_to_read": [
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
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
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
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
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                "modules.yaml",
            ],
            "prompt": f"""## Task: Complete Documentation Chain

**Target:** `{issue.path}`
**Missing docs:** {issue.details.get('missing', [])}
**Existing docs:** {issue.details.get('present', [])}

## CRITICAL: Check for existing docs first

Before creating any missing doc type:
- Search `docs/` for existing docs of that type that might cover this module
- Check if the missing doc exists in a different location or with different name
- If found elsewhere, link to it instead of creating a duplicate

## IMPLEMENTATION doc guidance

One IMPLEMENTATION doc per module that documents ALL files in that module.

**File Responsibilities table MUST include:**
- Line count for each file (approximate)
- Status: OK (<400L), WATCH (400-700L), or SPLIT (>700L)
- Any WATCH/SPLIT files need extraction candidates in GAPS section

**DESIGN PATTERNS section MUST include:**
- Architecture pattern (MVC, Layered, Pipeline, etc.) and WHY
- Code patterns in use (Factory, Strategy, etc.) and WHERE
- Anti-patterns to avoid in this module
- Boundary definitions (what's inside vs outside)

**Structure:**
- List all files in CODE STRUCTURE section
- Document each file's purpose in File Responsibilities table
- Define design patterns and boundaries
- Show data flows between files

If the IMPLEMENTATION doc exceeds ~300 lines, split into folder:
```
IMPLEMENTATION/
├── IMPLEMENTATION_Overview.md      # Entry point, high-level structure
├── IMPLEMENTATION_DataFlow.md      # How data moves
├── IMPLEMENTATION_Components.md    # Individual file details
```

## Steps:

1. Read the VIEW doc and modules.yaml
2. Read existing docs in `{issue.path}` to understand the module
3. For EACH missing doc type:
   a. Search for existing docs: `grep -r "PATTERN_TYPE" docs/`
   b. If found: update CHAIN to link to existing doc
   c. If not found: create using templates from `.ngram/templates/`
4. Ensure CHAIN sections link all docs together
5. Update SYNC with what you created/linked

## Success Criteria:
- Missing doc types are present (created or linked)
- NO duplicate documentation created
- CHAIN sections link correctly

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "NO_DOCS_REF": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Add DOCS: reference to source file",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
            ],
            "prompt": f"""## Task: Add DOCS Reference

**Target:** `{issue.path}`
**Problem:** {issue.message}

## Steps:

1. Find the documentation for this code (check docs/ and modules.yaml)
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
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
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
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
                ".ngram/PRINCIPLES.md",
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
            "docs_to_update": [".ngram/state/SYNC_Project_State.md"],
        },

        "INCOMPLETE_IMPL": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Complete empty functions",
            "docs_to_read": [
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
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
            "docs_to_update": [".ngram/state/SYNC_Project_State.md"],
        },

        "UNDOC_IMPL": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Document implementation file",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                "modules.yaml",
            ],
            "prompt": f"""## Task: Document Implementation File

**Target:** `{issue.path}`
**Problem:** {issue.message}

## CRITICAL: Find existing docs first

Before creating anything:
- `grep -r "{issue.path}" docs/` - check if already documented
- Search `docs/**/IMPLEMENTATION_*.md` for references to this file
- Check `modules.yaml` for module that should contain this file
- If documented elsewhere, update that doc instead of creating new

## IMPLEMENTATION doc structure

One IMPLEMENTATION doc per module documents ALL files in that module.
- Add this file to the existing module's IMPLEMENTATION doc
- Do NOT create a separate IMPLEMENTATION doc per file

**When adding a file, include:**
- Line count (approximate) - use `wc -l` to check
- Status: OK (<400L), WATCH (400-700L), or SPLIT (>700L)
- If WATCH/SPLIT: add extraction candidates to GAPS section

**Also update DESIGN PATTERNS if needed:**
- Does this file introduce new patterns?
- Does it affect module boundaries?

If adding makes the doc exceed ~300 lines, consider splitting into folder:
```
IMPLEMENTATION/
├── IMPLEMENTATION_Overview.md
├── IMPLEMENTATION_DataFlow.md
├── IMPLEMENTATION_Components.md
```

## Steps:

1. Search for existing documentation of this file
2. Find which module owns this code (check modules.yaml)
3. Count the file's lines: `wc -l {issue.path}`
4. Find that module's IMPLEMENTATION doc
5. Add the file with:
   - File path and brief description
   - Key functions/classes it contains
   - Line count and OK/WATCH/SPLIT status
6. If file is WATCH/SPLIT: add extraction candidates to GAPS
7. Update SYNC

## Success Criteria:
- File is referenced in the module's IMPLEMENTATION doc
- NO separate IMPLEMENTATION doc created for single file
- Bidirectional link established

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "LARGE_DOC_MODULE": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Reduce documentation module size",
            "docs_to_read": [
                ".ngram/views/VIEW_Refactor_Improve_Code_Structure.md",
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
3. For large individual files (~300+ lines), split into a folder:
   - Any doc type can become a folder when too large
   - Example: `ALGORITHM.md` -> `ALGORITHM/ALGORITHM_Overview.md`, `ALGORITHM_Details.md`
   - Keep an overview file as entry point
4. Update CHAIN sections after any splits
5. Update SYNC with what was reorganized

## Splitting pattern for any doc type:
```
DOC_TYPE.md (too large) -> DOC_TYPE/
├── DOC_TYPE_Overview.md      # Entry point, high-level
├── DOC_TYPE_Part1.md         # Focused section
├── DOC_TYPE_Part2.md         # Another section
```

## Archiving pattern:
- Create `{issue.path}/archive/SYNC_archive_2024-12.md` for old content
- Keep only current state in main docs

## Success Criteria:
- Total chars under 50K
- Individual files under ~300 lines
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
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                "modules.yaml",
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
            "docs_to_update": ["modules.yaml"],
        },

        "MISSING_TESTS": {
            "view": "VIEW_Test_Write_Tests_And_Verify.md",
            "description": "Add tests for module",
            "docs_to_read": [
                ".ngram/views/VIEW_Test_Write_Tests_And_Verify.md",
                "modules.yaml",
            ],
            "prompt": f"""## Task: Add Tests for Module

**Target:** `{issue.path}`
**Problem:** {issue.message}

## Steps:

1. Read modules.yaml to understand the module structure
2. Read the source code to understand what needs testing
3. Check for existing test patterns in the project (pytest, unittest, etc.)
4. Create test file(s) following existing conventions:
   - If `tests/` exists, put tests there
   - Mirror the source structure (e.g., `src/foo/bar.py` → `tests/foo/test_bar.py`)
5. Write tests for key functions/classes
6. Run tests to verify they pass
7. Update modules.yaml with tests path if needed
8. Update SYNC

## Success Criteria:
- Test file(s) created following project conventions
- Tests pass when run
- Key functionality is covered
- modules.yaml updated with tests path

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": ["modules.yaml"],
        },

        "ORPHAN_DOCS": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Fix orphan documentation",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                "modules.yaml",
            ],
            "prompt": f"""## Task: Fix Orphan Documentation

**Target:** `{issue.path}`
**Problem:** {issue.message}

Orphan docs are documentation files not linked from any code or modules.yaml.

## Steps:

1. Read the orphan doc to understand what it documents
2. Search for related code: `grep -r "keyword" src/`
3. Decide:
   a. If code exists: add DOCS: reference to code, add to modules.yaml
   b. If code was deleted: delete the orphan doc
   c. If doc is for a concept: move to `docs/concepts/`
4. Update SYNC

## Success Criteria:
- Doc is linked from code OR modules.yaml OR moved to concepts OR deleted
- No orphan docs remain

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "STALE_IMPL": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Update stale IMPLEMENTATION doc",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                issue.path,
            ],
            "prompt": f"""## Task: Update Stale IMPLEMENTATION Doc

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Missing files:** {issue.details.get('missing_files', [])}
**New files:** {issue.details.get('new_files', [])}

The IMPLEMENTATION doc doesn't match the actual files in the codebase.

## Steps:

1. Read the current IMPLEMENTATION doc
2. Compare against actual files in the module
3. For missing files (referenced but don't exist):
   - If renamed: update the path
   - If deleted: remove from doc
4. For new files (exist but not documented):
   - Add to CODE STRUCTURE section
   - Add to File Responsibilities table
5. Update data flow diagrams if needed
6. Update SYNC

## Success Criteria:
- All files in doc exist in codebase
- All files in codebase are in doc
- File descriptions are accurate

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "ARBITRAGE": {
            "view": "VIEW_Specify_Design_Vision_And_Architecture.md",
            "description": "Resolve conflict with human decision",
            "docs_to_read": [
                ".ngram/views/VIEW_Specify_Design_Vision_And_Architecture.md",
                issue.path,
            ],
            "prompt": f"""## Task: Implement Conflict Resolution

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Conflicts:** {issue.details.get('conflicts', [])}

The human has made decisions about these conflicts. Implement them.

## Human Decisions:
{{arbitrage_decisions}}

## Steps:

1. Read the SYNC file to understand each conflict
2. For each decision:
   - Update the conflicting docs/code to match the decision
   - Change ARBITRAGE to DECISION in the CONFLICTS section
   - Add "Resolved:" note explaining what was changed
3. Verify consistency - both sources should now agree
4. If CONFLICTS section is now all DECISION items, consider removing it
5. Update SYNC

## Success Criteria:
- All decided conflicts are resolved (docs/code updated)
- ARBITRAGE items converted to DECISION items
- No contradictions remain for resolved items

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "DOC_GAPS": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Complete gaps from previous agent",
            "docs_to_read": [
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
                issue.path,
            ],
            "prompt": f"""## Task: Complete Gaps From Previous Agent

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Gaps to complete:**
{chr(10).join(f"- [ ] {g}" for g in issue.details.get('gaps', []))}

A previous repair agent couldn't complete all work and left these tasks in a GAPS section.

## Steps:

1. Read the SYNC file to understand context
2. For each gap item:
   - Understand what was intended
   - Complete the task (create doc, implement feature, fix issue, etc.)
   - Mark it [x] done in the GAPS section
3. If you complete ALL gaps:
   - Remove the ## GAPS section entirely
   - Update SYNC with summary of what was completed
4. If you can't complete some gaps:
   - Mark completed ones [x]
   - Leave incomplete ones [ ] with updated notes on blockers
   - Add your own notes about why you couldn't complete

## Success Criteria:
- All completable gaps are done and marked [x]
- Incomplete gaps have clear notes about blockers
- GAPS section removed if all done
- SYNC updated with completion summary

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "SUGGESTION": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Implement agent suggestion",
            "docs_to_read": [
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
                issue.path,
            ],
            "prompt": f"""## Task: Implement Agent Suggestion

**Source:** `{issue.path}`
**Suggestion:** {issue.details.get('suggestion', issue.message)}

A previous agent made this suggestion for improvement. The user has accepted it.

## Steps:

1. Read the source SYNC file to understand context
2. Understand what the suggestion is asking for
3. Implement the improvement:
   - If it's a code change: modify the code
   - If it's a refactoring: restructure as suggested
   - If it's adding something: create it
4. Mark the suggestion as done in the SYNC file:
   - Change `[ ]` to `[x]` for this suggestion
5. Update SYNC with what you implemented
6. If implementation reveals more work needed, add new suggestions

## Success Criteria:
- Suggestion is implemented
- Suggestion marked [x] in source SYNC
- SYNC updated with implementation notes
- Any follow-up suggestions added

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "NEW_UNDOC_CODE": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Update documentation for changed code",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                issue.details.get('impl_doc', issue.path),
            ],
            "prompt": f"""## Task: Update Documentation for Changed Code

**Source file:** `{issue.path}`
**Problem:** {issue.message}
**IMPLEMENTATION doc:** `{issue.details.get('impl_doc', 'unknown')}`

The source code has been modified more recently than its documentation.

## Steps:

1. Read the source file to understand what changed
2. Count lines: `wc -l {issue.path}` - check if size status changed
3. Read the IMPLEMENTATION doc to see what's documented
4. Compare and identify gaps:
   - New functions/classes not documented
   - Changed signatures not reflected
   - Removed code still documented
   - File size changed (update Lines/Status columns)
5. Update the IMPLEMENTATION doc:
   - Add new code to FILE RESPONSIBILITIES
   - Update function signatures
   - Update line count and OK/WATCH/SPLIT status
   - Remove references to deleted code
   - Update data flow if changed
6. If file is now WATCH/SPLIT: add extraction candidates to GAPS
7. Update SYNC with what was updated

## Success Criteria:
- IMPLEMENTATION doc reflects current code
- New functions/classes are documented
- Line count and status are current
- No stale references to deleted code
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.details.get('impl_doc', '')],
        },

        "COMPONENT_NO_STORIES": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Add Storybook stories for component",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
            ],
            "prompt": f"""## Task: Add Storybook Stories for Component

**Component:** `{issue.path}`
**Problem:** {issue.message}

Frontend components should have Storybook stories for visual documentation and testing.

## Steps:

1. Read the component file to understand:
   - What props it accepts
   - What variants/states it has
   - What it renders
2. Create a stories file (e.g., `{Path(issue.path).stem}.stories.tsx`)
3. Add stories covering:
   - Default state
   - Key prop variations
   - Edge cases (loading, error, empty states)
   - Interactive states if applicable
4. Test stories render correctly in Storybook
5. Update SYNC

## Story Template:
```tsx
import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {Path(issue.path).stem} }} from './{Path(issue.path).stem}';

const meta: Meta<typeof {Path(issue.path).stem}> = {{
  component: {Path(issue.path).stem},
  title: 'Components/{Path(issue.path).stem}',
}};
export default meta;

type Story = StoryObj<typeof {Path(issue.path).stem}>;

export const Default: Story = {{
  args: {{}},
}};
```

## Success Criteria:
- Stories file exists next to component
- Default story renders component
- Key variants are covered
- Stories work in Storybook

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "HOOK_UNDOC": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Document custom React hook",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
            ],
            "prompt": f"""## Task: Document Custom Hook

**Hook:** `{issue.path}`
**Problem:** {issue.message}

Custom React hooks should have JSDoc documentation explaining their purpose and usage.

## Steps:

1. Read the hook file to understand:
   - What it does
   - What parameters it takes
   - What it returns
   - Any side effects
2. Add JSDoc comment above the hook:
```tsx
/**
 * Brief description of what this hook does.
 *
 * @param param1 - Description of first parameter
 * @param param2 - Description of second parameter
 * @returns Description of return value
 *
 * @example
 * ```tsx
 * const {{ data, loading }} = useMyHook(arg1, arg2);
 * ```
 */
```
3. Add `// DOCS:` reference if module docs exist
4. Update SYNC

## Success Criteria:
- Hook has JSDoc with description
- Parameters documented with @param
- Return value documented with @returns
- Usage example provided
- DOCS: reference if applicable

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "DOC_DUPLICATION": {
            "view": "VIEW_Document_Create_Module_Documentation.md",
            "description": "Consolidate duplicate documentation",
            "docs_to_read": [
                ".ngram/views/VIEW_Document_Create_Module_Documentation.md",
                issue.path,
            ],
            "prompt": f"""## Task: Consolidate Duplicate Documentation

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Details:** {issue.details}

Documentation duplication wastes context and creates inconsistency risk.

## Duplication Types

1. **Same file in multiple IMPLEMENTATION docs**
   - One file should be documented in exactly one IMPLEMENTATION doc
   - Remove references from all but the primary module's doc

2. **Multiple docs of same type in same folder**
   - Merge into single doc (e.g., two PATTERNS files → one)
   - Or split into subfolders if genuinely different modules

3. **Similar content across docs**
   - If >60% similar, one is probably redundant
   - Consolidate into the canonical location
   - Remove or replace the duplicate with a reference

## Steps:

1. Read the flagged doc and its "similar" doc
2. Determine which is the canonical source:
   - More complete? More recently updated? In better location?
3. For file references: keep in the owning module's IMPLEMENTATION only
4. For content duplication:
   - Merge unique content into canonical doc
   - Replace duplicate with: `See [Doc Name](path/to/canonical.md)`
   - Or delete if truly redundant
5. Update CHAIN sections to reflect new structure
6. Update SYNC with consolidation done

## Success Criteria:
- No duplicate file references
- No redundant content
- Clear canonical location for each topic
- CHAIN links updated
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [issue.path],
        },

        "HARDCODED_SECRET": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Remove hardcoded secret from code",
            "docs_to_read": [
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
                ".ngram/PRINCIPLES.md",
            ],
            "prompt": f"""## Task: Remove Hardcoded Secret (SECURITY CRITICAL)

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Details:** {issue.details}

This is a CRITICAL security issue. Secrets must never be in source code.

## Steps:

1. Read the file and locate the secret
2. Determine where the secret should come from:
   - Environment variable (most common)
   - Secrets manager (AWS Secrets Manager, Vault, etc.)
   - Config file that's in .gitignore
3. Replace the hardcoded value with environment variable lookup:
   - Python: `os.environ.get('SECRET_NAME')` or `os.getenv('SECRET_NAME')`
   - Node.js: `process.env.SECRET_NAME`
4. Add the secret name to a `.env.example` file with placeholder value
5. Ensure `.env` is in `.gitignore`
6. Update any documentation about required environment variables
7. Update SYNC with security fix

## Success Criteria:
- No hardcoded secret in code
- Secret loaded from environment variable
- `.env.example` updated
- `.gitignore` includes `.env`
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [".ngram/state/SYNC_Project_State.md"],
        },

        "HARDCODED_CONFIG": {
            "view": "VIEW_Implement_Write_Or_Modify_Code.md",
            "description": "Externalize hardcoded configuration",
            "docs_to_read": [
                ".ngram/views/VIEW_Implement_Write_Or_Modify_Code.md",
            ],
            "prompt": f"""## Task: Externalize Hardcoded Configuration

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Details:** {issue.details}

Configuration values like URLs, ports, and IPs should not be hardcoded.

## Steps:

1. Read the file and identify the hardcoded config value
2. Determine the appropriate configuration method:
   - Environment variable for runtime config
   - Config file (config.yaml, settings.py) for app config
   - Constants file for truly static values
3. Extract the value:
   - Create or update config file if needed
   - Replace hardcoded value with config lookup
4. Add default value handling for development
5. Update SYNC with changes

## Success Criteria:
- Hardcoded value replaced with config lookup
- Config file or env var documented
- Default values for development
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "MAGIC_VALUES": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Extract magic numbers to constants",
            "docs_to_read": [
                ".ngram/views/VIEW_Refactor_Improve_Code_Structure.md",
            ],
            "prompt": f"""## Task: Extract Magic Numbers to Constants

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Examples:** {issue.details.get('examples', [])}

Magic numbers make code hard to understand and maintain.

## Steps:

1. Read the file and identify magic numbers
2. For each magic number:
   - Determine what it represents
   - Create a named constant with descriptive name
   - Replace the number with the constant
3. Place constants appropriately:
   - Module-level constants at top of file
   - Or in a dedicated constants.py if shared across files
4. Use UPPER_CASE naming convention
5. Add brief comment explaining each constant if not obvious

## Example:
```python
# Before
if timeout > 300:
    raise TimeoutError()

# After
REQUEST_TIMEOUT_SECONDS = 300  # Maximum time to wait for API response

if timeout > REQUEST_TIMEOUT_SECONDS:
    raise TimeoutError()
```

## Success Criteria:
- Magic numbers replaced with named constants
- Constants have descriptive names
- Code behavior unchanged
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "LONG_PROMPT": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Move prompts to prompts/ directory",
            "docs_to_read": [
                ".ngram/views/VIEW_Refactor_Improve_Code_Structure.md",
            ],
            "prompt": f"""## Task: Externalize Long Prompts

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Details:** {issue.details}

Long prompt strings embedded in code are hard to edit and review.

## Steps:

1. Read the file and identify the long prompt string(s)
2. Create prompts/ directory if it doesn't exist
3. For each prompt:
   - Create a new file: `prompts/{{purpose}}.md` or `prompts/{{purpose}}.txt`
   - Move the prompt content to the file
   - Replace inline string with file read:
     ```python
     from pathlib import Path
     prompt = (Path(__file__).parent / "prompts" / "my_prompt.md").read_text()
     ```
4. If prompt has variables, use string formatting or templating
5. Update SYNC with what was externalized

## Benefits:
- Easier to edit prompts in markdown
- Better version control diffs
- Can review prompts separately from code

## Success Criteria:
- Prompts moved to prompts/ directory
- Code loads prompts from files
- Functionality unchanged
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },

        "LONG_SQL": {
            "view": "VIEW_Refactor_Improve_Code_Structure.md",
            "description": "Move SQL queries to .sql files",
            "docs_to_read": [
                ".ngram/views/VIEW_Refactor_Improve_Code_Structure.md",
            ],
            "prompt": f"""## Task: Externalize Long SQL Queries

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Details:** {issue.details}

Long SQL queries embedded in code are hard to maintain and test.

## Steps:

1. Read the file and identify the long SQL query/queries
2. Create sql/ directory if it doesn't exist
3. For each query:
   - Create a new file: `sql/{{purpose}}.sql`
   - Move the SQL to the file
   - Replace inline string with file read
4. For queries with parameters, use SQL placeholders
5. Update SYNC with what was externalized

## Example:
```python
# Before
query = \"\"\"
SELECT u.id, u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
WHERE u.status = 'active'
GROUP BY u.id, u.name
HAVING COUNT(o.id) > 5
\"\"\"

# After
# sql/active_users_with_orders.sql contains the query
query = (Path(__file__).parent / "sql" / "active_users_with_orders.sql").read_text()
```

## Success Criteria:
- SQL queries moved to .sql files
- Code loads SQL from files
- Parameters handled correctly
- SYNC updated

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
            "docs_to_update": [],
        },
    }

    return instructions.get(issue.issue_type, {
        "view": "VIEW_Implement_Write_Or_Modify_Code.md",
        "description": f"Fix {issue.issue_type} issue",
        "docs_to_read": [".ngram/PROTOCOL.md"],
        "prompt": f"""## Task: Fix Issue

**Target:** `{issue.path}`
**Problem:** {issue.message}
**Suggestion:** {issue.suggestion}

Review and fix this issue following the ngram.

Report "REPAIR COMPLETE" when done, or "REPAIR FAILED: <reason>" if you cannot complete.
""",
        "docs_to_update": [],
    })
