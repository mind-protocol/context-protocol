# ngram Framework CLI — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: codex (sync cli impl doc with code)
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

The CLI is stable and in active use. Core commands: `init`, `validate`, `doctor`, `repair`, plus supporting `sync/context/prompt/map/agents`.

---

## IN PROGRESS

No active development at this time.

---

## RECENT CHANGES

### 2025-12-19: Sync CLI implementation doc with code structure

- Added newly split doctor checks, repair helpers, and repo overview files
- Updated module dependencies and file responsibilities to match current layout

### 2025-12-19: Fixed broken implementation doc references

- Removed inline backtick references that were misclassified as files
- Updated SVG namespace note to reference `ngram/project_map_html.py`

### 2025-12-19: Externalized overview DOCS header scan length

- `repo_overview.py` now reads DOCS header scan length from DoctorConfig instead of a hardcoded value
- `doctor_files.py` loads `doctor.docs_ref_search_chars` from `.ngram/config.yaml` (default 2000)

### 2025-12-19: Externalized SVG namespace config

- `project_map_html.py` now reads SVG namespace from `NGRAM_SVG_NAMESPACE` with default fallback
- Documented env var in CLI implementation config table

### 2025-12-20: Multi-agent provider support

- `repair` accepts `--agents {claude,codex,gemini}` and `init` mirrors `.ngram/CLAUDE.md` into root `AGENTS.md`

### 2025-12-20: Doctor exits cleanly on findings

- `ngram doctor` returns exit code 0 when issues are found

### 2025-12-19: Documentation size reduction

- Reduced `docs/cli` module size by simplifying verbose sections

### 2025-12-19: INCOMPLETE_IMPL false positive review

- Confirmed `get_issue_symbol` and `get_issue_action_parts` already implement lookups
- No code changes required; this repair only updates SYNC to document the check

---

## KNOWN ISSUES

- Parallel agent output can intermix during `repair --parallel` (low severity)

---

## CONFLICTS

### DECISION: modules.yaml mapping mismatch
- Conflict: SYNC claims module mapping exists, but `modules.yaml` is template-only.
- Resolution: Keep this documented here; defer mapping to a dedicated task.
- Reasoning: Out of scope for CLI behavior changes.
- Updated: `docs/cli/SYNC_CLI_State.md`

---

## HANDOFF

- Agents: use `VIEW_Extend_Add_Features_To_Existing.md` (new commands) or `VIEW_Debug_Investigate_And_Fix_Issues.md` (bug fixes); no pending work.
- Human: CLI is stable and documented; no input needed.

---

## Agent Observations

### Remarks
- Confirmed INCOMPLETE_IMPL finding was a false positive due to short helper bodies.
- SVG namespace now configurable via `NGRAM_SVG_NAMESPACE` for project map HTML output.
- Overview DOCS header scan length now configurable via `doctor.docs_ref_search_chars` in `.ngram/config.yaml`.
- Implementation doc now avoids false broken-link hits from config key notation.

### Suggestions
- [ ] Reconcile `modules.yaml` with CLI module docs to remove mapping drift.

### Propositions
- No new propositions from this repair.

---

## ARCHIVE

Older content archived to: `SYNC_CLI_State_archive_2025-12.md`
