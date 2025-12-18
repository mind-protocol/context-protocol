# ADD Framework CLI — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent (BROKEN_IMPL_LINK fix)
STATUS: CANONICAL
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Why_CLI_Over_Copy.md
BEHAVIORS:       ./BEHAVIORS_CLI_Command_Effects.md
ALGORITHM:       ./ALGORITHM_CLI_Logic.md
VALIDATION:      ./VALIDATION_CLI_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_CLI_Code_Architecture.md
TEST:            ./TEST_CLI_Coverage.md
THIS:            SYNC_CLI_State.md (you are here)
```

---

## CURRENT STATE

The CLI is functional and in active use. All core commands work:

**init**: Copies `.ngram/` directory and updates CLAUDE.md. Supports `--force` for re-initialization.

**validate**: Runs 8 validation checks including protocol installation, VIEW existence, module docs minimum, chain completeness, naming conventions, CHAIN link validity, and module manifest configuration.

**doctor**: Comprehensive health checks for 12 issue types (MONOLITH, UNDOCUMENTED, STALE_SYNC, PLACEHOLDER, INCOMPLETE_CHAIN, NO_DOCS_REF, BROKEN_IMPL_LINK, STUB_IMPL, INCOMPLETE_IMPL, UNDOC_IMPL, LARGE_DOC_MODULE, YAML_DRIFT). Generates SYNC-formatted health report. Supports GitHub issue creation.

**repair**: The most sophisticated command. Spawns Claude Code agents in parallel (default 5) to fix issues. Each agent follows a VIEW, reads required docs, makes focused changes, and updates SYNC. Supports depth levels (links, docs, full) and issue type filtering.

**sync**: Shows SYNC file status and auto-archives large files.

**context**: Given a file path, finds related documentation through modules.yaml mapping and DOCS: references.

**prompt**: Generates bootstrap prompt for LLMs working on the project.

**map**: Generates visual HTML map of modules and dependencies.

---

## IN PROGRESS

No active development at this time.

---

## RECENT CHANGES

### 2025-12-18: Fixed BROKEN_IMPL_LINK for ALGORITHM reference

**What changed:**
- Updated `IMPLEMENTATION_CLI_Code_Architecture.md` line 181 reference from `` `ALGORITHM_CLI_Logic.md` `` to `` `docs/cli/ALGORITHM_CLI_Logic.md` ``
- The doctor check extracts backtick references and looks in `target_dir/`, `src/`, etc. but not relative to the doc file
- Using the full path from project root resolves the broken link check

**Files modified:**
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md`

### 2025-12-18: Added DOCS reference to context.py

**What changed:**
- Added `DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` reference to `src/ngram/context.py` header
- Enables `ngram context` to properly trace documentation chain for this file

**Files modified:**
- `src/ngram/context.py`

### 2025-12-18: Reduced documentation size (LARGE_DOC_MODULE fix)

**What changed:**
- Removed duplicate data structures from ALGORITHM (now references IMPLEMENTATION#SCHEMA)
- Removed duplicate check reference tables from VALIDATION (now references ALGORITHM)
- Simplified verbose DATA FLOW diagrams in IMPLEMENTATION (now references ALGORITHM)
- Consolidated TEST_CLI_Coverage.md verbose "NOT TESTED" tables

**Result:** Total module size reduced from 53K to 48K chars (threshold: 50K)

### 2025-12-18: Fixed DOC_DUPLICATION false positive for archive files

**What changed:**
- Added `_archive_` filename exclusion in `doctor_check_doc_duplication()` Check 3
- Archive files are now skipped before being added to `docs_by_topic` tracking
- This prevents SYNC archive files from being flagged as duplicates of main SYNC files

**Files modified:**
- `src/ngram/doctor_checks.py:1337-1341`

### 2025-12-18: Extracted doctor_checks.py

**What changed:**
- Extracted all 23 `doctor_check_*()` functions from `doctor.py` to new `doctor_checks.py`
- `doctor.py`: 1900L → 211L (now OK status)
- `doctor_checks.py`: New file, 1732L (SPLIT status - needs further splitting)

**Files created:**
- `src/ngram/doctor_checks.py`

**Files modified:**
- `src/ngram/doctor.py`
- `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md`
- `modules.yaml`

**What still needs extraction:**
- `doctor_checks.py` needs splitting by check category (doc checks, code checks, config checks)
- `repair.py` and `repair_instructions.py` also still need extraction

---

## KNOWN ISSUES

### Parallel Output Interleaving

- **Severity:** low
- **Symptom:** When running `repair --parallel`, agent outputs can intermix
- **Suspected cause:** Multiple agents writing to stdout simultaneously
- **Attempted:** Added per-agent colors and symbols for visual distinction

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Extend_Add_Features_To_Existing.md` (for new commands) or `VIEW_Debug_Investigate_And_Fix_Issues.md` (for bug fixes)

**Where I stopped:** Documentation complete. No pending work.

**What you need to understand:**
- Each command is in its own file under `src/ngram/`
- `cli.py` is the entry point that wires up argparse
- `utils.py` has shared utilities (template paths, module discovery)
- The repair system spawns `claude` subprocess with specific prompts

**Watch out for:**
- `repair.py` is complex — understand DEPTH_LINKS/DOCS/FULL before modifying
- YAML is optional dependency — code handles missing yaml gracefully
- Template files live in `templates/` at repo root (for dev) or in package (installed)

**Open questions I had:**
- Should repair depth default to "links" instead of "docs" for safer defaults?
- Is there value in a `ngram status` that combines doctor + sync output?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
CLI module now has documentation. All 8 commands work and are documented. Module mapping added to `modules.yaml`. The codebase health issue (UNDOCUMENTED for src/) is resolved.

**Decisions made:**
- Named module `ngram-cli` in modules.yaml (vs just `cli`)
- Put docs in `docs/cli/` (flat, not nested under an area)
- PATTERNS focuses on "why CLI over copy" as the core design question

**Needs your input:**
- None at this time

---

## POINTERS

| What | Where |
|------|-------|
| CLI entry point | `src/ngram/cli.py` |
| Validation logic | `src/ngram/validate.py` |
| Health check orchestration | `src/ngram/doctor.py` |
| Health check functions | `src/ngram/doctor_checks.py` |
| Repair agents | `src/ngram/repair.py` |
| Module manifest | `modules.yaml` |
| Design rationale | `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` |


---

## ARCHIVE

Older content archived to: `SYNC_CLI_State_archive_2025-12.md`
