# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair agent (YAML_DRIFT fix)
```

---

## CURRENT STATE

The ADD Framework project is functional and in active use. The CLI provides commands for initializing, validating, diagnosing, and repairing protocol compliance in any project.

**NEW: TUI Feature in Progress**

A Claude Code-style TUI is being developed. Entry point: `ngram` (no subcommand). Features manager + worker agent columns, input bar, /commands, white theme.

- Documentation created: `docs/tui/PATTERNS_TUI_Design.md`, `docs/tui/SYNC_TUI_State.md`
- Module mapped: `ngram-tui` in `modules.yaml`
- Core extraction done: `repair_core.py` with shared logic for CLI and TUI

### Recent Changes

**2025-12-18:** Fixed INCOMPLETE_IMPL false positive in repair_core.py:
- Functions `get_issue_symbol`, `get_issue_action_parts` are intentionally simple one-liner dictionary lookup functions
- Added suppression entry to `.ngram/doctor-ignore.yaml` with detailed reason
- These functions return tuples from ISSUE_SYMBOLS and ISSUE_DESCRIPTIONS dictionaries with sensible defaults
- Used throughout repair.py for display formatting (imported and called at multiple locations)

**2025-12-18:** Fixed INCOMPLETE_IMPL false positive in repair.py:
- Functions `get_agent_color`, `get_agent_symbol`, `color` are intentionally simple one-line utility functions
- Added block comment explaining they're complete implementations, not stubs
- Added suppression entry to `.ngram/doctor-ignore.yaml` with detailed reason
- These functions provide semantic meaning to CLI operations (color cycling, symbol cycling, ANSI wrapping)

**2025-12-18:** Fixed YAML_DRIFT for ngram-tui module:
- Commented out `code: "src/ngram/tui/**"` in modules.yaml (path doesn't exist yet)
- Removed `entry_points:` section (no code to point to)
- Updated notes to clarify this is DOCS ONLY until implementation
- Module entry preserved for documentation tracking; code path will be uncommented when TUI is implemented

**2025-12-18:** TUI Feature Design and Core Extraction:
- Created `repair_core.py` with shared repair logic (dataclasses, constants, async spawn)
- Refactored `repair.py` to import from `repair_core.py` (1674 -> 1055 lines)
- Created TUI documentation: PATTERNS and SYNC docs
- Added `ngram-tui` module to `modules.yaml`
- Implementation pending: package structure, widgets, cli.py integration

**2025-12-18:** Fixed DOC_DUPLICATION false positive for archive files in doctor_checks.py:
- Added `_archive_` filename exclusion in Check 3 (doc type tracking by folder)
- Archive files created by auto-archiving system are now skipped before being added to `docs_by_topic`
- This prevents `SYNC_*.md` and `SYNC_*_archive_*.md` pairs from being flagged as duplicates
- Modified: `src/ngram/doctor_checks.py:1337-1341`

**2025-12-18:** Extracted check functions from doctor.py to doctor_checks.py:
- Created `doctor_checks.py` with all 23 `doctor_check_*()` functions (~1732 lines)
- `doctor.py` reduced from 1900 → 211 lines (now OK status)
- `doctor_checks.py` still needs further splitting by category (SPLIT status)
- Updated IMPLEMENTATION doc, modules.yaml, and SYNC_CLI_State.md

**2025-12-18:** Fixed BROKEN_IMPL_LINK in CLI IMPLEMENTATION doc:
- Fixed 22 broken file references in `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md`
- Root cause: File reference extraction pattern matched bare filenames (e.g., `cli.py`) that couldn't be resolved
- Flattened CODE STRUCTURE tree, updated tables to use module names without `.py` extension
- Clarified GAPS section to mark proposed files as "(planned)"

**2025-12-18:** Fixed DOC_DUPLICATION false positive bug in `doctor.py`:
- Fixed regex capture group bug in `doctor_check_documentation_duplication()` that was returning empty strings instead of file paths
- Changed file reference tracking from `List[str]` to `Set[str]` to avoid flagging the same doc that mentions a file multiple times
- The original issue was detecting "`\`\`` documented in 15 places" due to regex `(/?)` returning only the capture group contents

**2025-12-18:** Refactored `repair.py` to reduce monolith size:
- Created `repair_instructions.py` module with issue instruction dictionary (~885 lines)
- Moved: `get_issue_instructions()` function (725+ lines) containing all issue type prompts
- `repair.py` reduced from 1907 → 1613 lines (294 lines extracted, still above 800 threshold)
- Module hierarchy: `repair.py` → imports `get_issue_instructions` from `repair_instructions.py`

**2025-12-18 (earlier):** Refactored `doctor.py` to reduce monolith size:
- Created `doctor_files.py` module with file/path utilities (~280 lines extracted)
- Moved: `parse_gitignore`, `load_doctor_config`, `should_ignore_path`, `is_binary_file`, `find_source_files`, `find_code_directories`, `count_lines`, `find_long_sections`
- `doctor.py` reduced from 1337 → 1217 non-empty lines (still needs further splitting)
- Module hierarchy: `doctor.py` → imports from `doctor_types.py`, `doctor_report.py`, `doctor_files.py`

---

## ACTIVE WORK

**TUI Implementation** (Priority):
- ~~YAML_DRIFT: `ngram-tui` mapped but `src/ngram/tui/` doesn't exist yet~~ FIXED: Code path commented out
- INCOMPLETE_CHAIN: `docs/tui/` needs BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST
- Next steps: Create package structure, implement widgets, update cli.py, then uncomment code path in modules.yaml

**MONOLITH Cleanup** (Ongoing):
- `doctor_checks.py` (1411L) - needs splitting by category
- `repair.py` (1055L) - reduced from 1674L, still above threshold
- `repair_instructions.py` (1001L) - needs further splitting

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| ~~Circular import doctor/doctor_report~~ | ~~high~~ | ~~doctor.py~~ | **RESOLVED** - Moved DoctorIssue to doctor_types.py |
| Parallel output interleaving | low | repair.py | Agent outputs can mix when running parallel repairs |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Extend_Add_Features_To_Existing.md`

**Current focus:** Project health and documentation coverage

**Key context:**
The CLI is the main deliverable. Understanding `repair.py` is important for working on automated fixes. Each CLI command lives in its own file under `src/ngram/`.

**Watch out for:**
- Templates live in `templates/` at repo root (development) OR inside the package (installed)
- YAML is optional — code handles missing yaml library gracefully

---

## HANDOFF: FOR HUMAN

**Executive summary:**
The src/ directory is now documented. Created module mapping and minimum viable docs (PATTERNS + SYNC). CLI health issue resolved.

**Decisions made recently:**
- Named module `ngram-cli` in modules.yaml
- Put docs in flat `docs/cli/` structure (no area nesting)

**Needs your input:**
- None currently

**Concerns:**
- None

---

## TODO

### High Priority

- [x] Document src/ module (UNDOCUMENTED issue)
- [x] Complete CLI documentation chain (INCOMPLETE_CHAIN issue)

### Backlog

- [ ] Add automated tests for CLI (currently 0% coverage)
- [ ] Set up CI/CD test pipeline
- IDEA: Add watch mode for continuous health monitoring

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `docs/cli/` | documented | `docs/cli/SYNC_CLI_State.md` |
| `docs/protocol/` | documented | `docs/protocol/SYNC_Protocol_Current_State.md` |

---

## MODULE COVERAGE

Check `modules.yaml` for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| ngram-cli | `src/ngram/**` | `docs/cli/` | CANONICAL |
| ngram-tui | (not yet implemented) | `docs/tui/` | DESIGNING |

**Unmapped code:** None

**Coverage notes:**
The CLI module is the main code in this project. Templates are not mapped as they're static resources, not code.


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`
