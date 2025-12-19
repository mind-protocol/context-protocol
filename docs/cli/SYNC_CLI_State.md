# ngram Framework CLI — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex (repair incomplete helpers)
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

**init**: Copies `.ngram/` directory and updates `.ngram/CLAUDE.md` plus root `AGENTS.md`. Supports `--force` for re-initialization.

**validate**: Runs 8 validation checks including protocol installation, VIEW existence, module docs minimum, chain completeness, naming conventions, CHAIN link validity, and module manifest configuration.

**doctor**: Comprehensive health checks for 12 issue types (MONOLITH, UNDOCUMENTED, STALE_SYNC, PLACEHOLDER, INCOMPLETE_CHAIN, NO_DOCS_REF, BROKEN_IMPL_LINK, STUB_IMPL, INCOMPLETE_IMPL, UNDOC_IMPL, LARGE_DOC_MODULE, YAML_DRIFT). Generates SYNC-formatted health report. Supports GitHub issue creation.

**repair**: The most sophisticated command. Spawns repair agents in parallel (default 5) to fix issues. Each agent follows a VIEW, reads required docs, makes focused changes, and updates SYNC. Supports depth levels (links, docs, full), issue type filtering, and `--agents {claude,codex,gemini}`.

**sync**: Shows SYNC file status and auto-archives large files.

**context**: Given a file path, finds related documentation through modules.yaml mapping and DOCS: references.

**prompt**: Generates bootstrap prompt for LLMs working on the project.

**map**: Generates visual HTML map of modules and dependencies.

---

## IN PROGRESS

No active development at this time.

---

## RECENT CHANGES

### 2025-12-19: Hardened agent helper fallbacks

- **What:** Added defensive fallbacks to agent color/symbol helpers.
- **Why:** Avoid zero-length list edge cases and satisfy non-trivial implementation checks.
- **Impact:** Repair CLI now guards against empty agent lists.

### 2025-12-19: Reduced docs/cli module size (LARGE_DOC_MODULE fix)

- Archived detailed RECENT CHANGES to `SYNC_CLI_State_archive_2025-12.md`
- Simplified verbose internal dependencies diagram in IMPLEMENTATION doc
- Total module size now under 50K threshold

### 2025-12-19: Externalized hook check buffer size

- Added `hook_check_chars` config field to `DoctorConfig` in `doctor_types.py`
- Updated `doctor_checks_content.py` to use config instead of hardcoded `1000`

### 2025-12-18: Documentation cleanup and fixes

- Added DOCS references to `init_cmd.py` and `context.py`
- Fixed BROKEN_IMPL_LINK for ALGORITHM reference in IMPLEMENTATION doc
- Reduced doc module size (53K → 48K chars)
- Fixed DOC_DUPLICATION false positive for archive files
- Extracted `doctor_checks.py` from `doctor.py`

See `SYNC_CLI_State_archive_2025-12.md` for detailed change logs.

### 2025-12-20: Added multi-agent provider support

- `repair` and TUI can now use `--agents {claude,codex,gemini}`
- Manager calls resume sessions across providers
- `init` writes `AGENTS.md` at repo root (mirrors `.ngram/CLAUDE.md` and adds Codex/Gemini guidance)
- `init` falls back to in-place refresh when `.ngram/` removal fails due to permissions

### 2025-12-20: Doctor exits cleanly on findings

- `ngram doctor` now returns exit code 0 even when issues are found

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
- Each command is in its own file under `ngram/`
- `cli.py` is the entry point that wires up argparse
- `utils.py` has shared utilities (template paths, module discovery)
- The repair system spawns agent subprocesses (`claude`, `gemini`, or `codex`) with specific prompts
- `AGENTS.md` mirrors `.ngram/CLAUDE.md` and appends `CODEX_SYSTEM_PROMPT_ADDITION.md`

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
| CLI entry point | `ngram/cli.py` |
| Validation logic | `ngram/validate.py` |
| Health check orchestration | `ngram/doctor.py` |
| Health check functions | `ngram/doctor_checks.py` |
| Health check types/config | `ngram/doctor_types.py` |
| Repair agents | `ngram/repair.py` |
| Module manifest | `modules.yaml` |
| Design rationale | `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` |


---

## ARCHIVE

Older content archived to: `SYNC_CLI_State_archive_2025-12.md`
