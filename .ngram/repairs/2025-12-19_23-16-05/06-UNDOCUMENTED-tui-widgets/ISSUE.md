# Repair Task

**Issue Type:** UNDOCUMENTED
**Severity:** critical
**Target:** ngram/tui/widgets

## Instructions
## Task: Document Module

**Target:** `ngram/tui/widgets`
**Problem:** No documentation mapping (7 files)

## CRITICAL: Check for existing docs first

Before creating anything, search for existing documentation:
- `grep -r "ngram/tui/widgets" docs/` - check if this path is mentioned in existing docs
- Search `docs/**/IMPLEMENTATION_*.md` for references to this code
- Check `modules.yaml` for existing mappings that might cover this code
- If docs exist elsewhere, UPDATE the mapping instead of creating duplicates

## Steps:

1. Read the VIEW, PROTOCOL.md, and template docs listed above
2. Search for existing docs that might cover this code
3. If found: update `modules.yaml` mapping to link existing docs
4. If not found:
   a. Check `modules.yaml` and `docs/` to see existing naming patterns
   b. Read the code in `ngram/tui/widgets` to understand what it does
   c. Choose a descriptive module name (e.g., `cli`, `auth`) not the code path
   d. Follow the pattern: `docs/{module}/` or `docs/{area}/{module}/`
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

MANDATORY FINAL LINE:
- End your response with a standalone line: `REPAIR COMPLETE`
- If you fail, end with: `REPAIR FAILED: <reason>`



## Docs to Read
- .ngram/views/VIEW_Document_Create_Module_Documentation.md
- .ngram/PROTOCOL.md
- .ngram/templates/PATTERNS_TEMPLATE.md
- .ngram/templates/SYNC_TEMPLATE.md
- modules.yaml
