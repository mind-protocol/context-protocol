# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent (doctor.py monolith extraction)
```

---

## CURRENT STATE

The ADD Framework project is functional and in active use. The CLI provides commands for initializing, validating, diagnosing, and repairing protocol compliance in any project.

Documentation coverage is complete. The `src/` directory containing the CLI implementation has proper module documentation mapped in `modules.yaml`.

### Recent Changes

**2025-12-18:** Extracted check functions from doctor.py to doctor_checks.py:
- Created `doctor_checks.py` with all 23 `doctor_check_*()` functions (~1732 lines)
- `doctor.py` reduced from 1900 → 211 lines (now OK status)
- `doctor_checks.py` still needs further splitting by category (SPLIT status)
- Updated IMPLEMENTATION doc, modules.yaml, and SYNC_CLI_State.md

**2025-12-18:** Fixed DOC_DUPLICATION false positive for archive files:
- Added `_archive_` filename exclusion in `doctor_check_doc_duplication()` (doctor.py:1320-1322)
- Archive files are intentionally created by the auto-archiving system and should not be flagged as duplicates
- Files like `SYNC_*_archive_2025-12.md` are now skipped during duplication checks

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

- MONOLITH issues remain: `doctor_checks.py` (1732L), `repair.py` (1384L), `repair_instructions.py` (1001L)
- `doctor.py` is now OK (211L) after extraction
- Next extraction candidates:
  - `doctor_checks.py`: Split by check category (doc checks, code checks, config checks)
  - `repair.py`: `spawn_repair_agent()`, agent streaming logic

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

**Unmapped code:** None after this repair

**Coverage notes:**
The CLI module is the main code in this project. Templates are not mapped as they're static resources, not code.


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`
