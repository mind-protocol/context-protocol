# Repair Task

**Issue Type:** HARDCODED_CONFIG
**Severity:** warning
**Target:** ngram/project_map_html.py

## Instructions
## Task: Externalize Hardcoded Configuration

**Target:** `ngram/project_map_html.py`
**Problem:** Contains hardcoded configuration values
**Details:** {'values': [(258, 'hardcoded URL')]}

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


## Docs to Read
- .ngram/views/VIEW_Implement_Write_Or_Modify_Code.md
