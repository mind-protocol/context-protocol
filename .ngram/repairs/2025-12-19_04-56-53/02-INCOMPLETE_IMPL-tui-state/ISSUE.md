# Repair Task

**Issue Type:** INCOMPLETE_IMPL
**Severity:** warning
**Target:** ngram/tui/state.py

## Instructions
## Task: Complete Empty Functions

**Target:** `ngram/tui/state.py`
**Problem:** Contains 10 empty/incomplete function(s)
**Empty functions:** ['to_dict', 'get_recent', 'clear', 'duration', 'is_active', 'append_output', 'get_output', 'add_agent', 'add_manager_message', 'active_count']

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
