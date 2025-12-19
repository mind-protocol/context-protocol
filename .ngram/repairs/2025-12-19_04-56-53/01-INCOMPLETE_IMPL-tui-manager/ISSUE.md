# Repair Task

**Issue Type:** INCOMPLETE_IMPL
**Severity:** warning
**Target:** ngram/tui/manager.py

## Instructions
## Task: Complete Empty Functions

**Target:** `ngram/tui/manager.py`
**Problem:** Contains 4 empty/incomplete function(s)
**Empty functions:** ['is_running', 'extract_changed_files', 'extract_doc_updates', 'on_agent_complete']

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


## Docs to Read
- .ngram/views/VIEW_Implement_Write_Or_Modify_Code.md
