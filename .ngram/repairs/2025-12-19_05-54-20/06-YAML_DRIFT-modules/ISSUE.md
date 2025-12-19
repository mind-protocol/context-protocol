# Repair Task

**Issue Type:** YAML_DRIFT
**Severity:** critical
**Target:** modules.yaml#cli

## Instructions
## Task: Fix YAML Drift

**Target:** `modules.yaml#cli`
**Module:** cli
**Issues:** ["code path 'ngram.py' not found"]

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


## Docs to Read
- .ngram/views/VIEW_Document_Create_Module_Documentation.md
- modules.yaml
