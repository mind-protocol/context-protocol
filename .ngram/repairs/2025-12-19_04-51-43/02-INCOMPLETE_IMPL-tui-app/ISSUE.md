# Repair Task

**Issue Type:** INCOMPLETE_IMPL
**Severity:** warning
**Target:** ngram/tui/app.py

## Instructions
## Task: Complete Empty Functions

**Target:** `ngram/tui/app.py`
**Problem:** Contains 10 empty/incomplete function(s)
**Empty functions:** ['on_claude_output', '_build_manager_overview_prompt', 'on_click', 'on_input_bar_input_changed', '_reset_ctrl_c', 'action_doctor', 'action_repair', 'action_tab_agents', 'action_tab_sync', 'action_tab_doctor']

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
