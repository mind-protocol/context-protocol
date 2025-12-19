# Repair Task

**Issue Type:** MONOLITH
**Severity:** critical
**Target:** ngram/tui/app.py

## Instructions
## Task: Split Monolith File

**Target:** `ngram/tui/app.py`
**Problem:** 829 lines (threshold: 800)
**Suggestion:** Split: class NgramApp() (915L, :42), async def _start_manager_with_overview() (192L, :239), async def on_mount() (69L, :125)

## Steps:

1. Read the VIEW and PRINCIPLES docs listed above
2. Read the target file to understand its structure
3. Find the IMPLEMENTATION doc for this module (check modules.yaml for docs path)
4. Identify the largest function/class mentioned in the suggestion
5. Create a new file for the extracted code (e.g., `app_utils.py`)
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

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Refactor_Improve_Code_Structure.md
- .ngram/PRINCIPLES.md
- modules.yaml
