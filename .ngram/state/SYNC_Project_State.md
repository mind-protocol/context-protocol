# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent
```

---

## CURRENT STATE

ngram CLI project with doctor/repair functionality for maintaining project health.

---

## ACTIVE WORK

### Monolith Refactoring

- **Area:** `src/ngram/`
- **Status:** completed
- **Owner:** repair-agent
- **Context:** Reducing file sizes to meet 800-line threshold

---

## RECENT CHANGES

### 2025-12-18: Split doctor_checks.py monolith

- **What:** Extracted 7 functions from doctor_checks.py into 2 new files:
  - `doctor_checks_quality.py` (172L): doctor_check_magic_values, doctor_check_hardcoded_secrets
  - `doctor_checks_docs.py` (316L): doctor_check_placeholder_docs, doctor_check_orphan_docs, doctor_check_stale_impl, doctor_check_large_doc_module, doctor_check_incomplete_chain
- **Why:** MONOLITH issue - file was 1155 lines (threshold: 800)
- **Impact:** doctor_checks.py reduced from 1155 lines to 733 lines (now under threshold). Functions are re-exported for backwards compatibility.
- **Doc updates:** modules.yaml updated with cli module mapping including new files.

### 2025-12-18: Split repair_instructions.py monolith

- **What:** Removed duplicate doc-related instructions from repair_instructions.py that were already extracted to repair_instructions_docs.py. Updated get_issue_instructions() to delegate to get_doc_instructions() for doc-related issues.
- **Why:** MONOLITH issue - file was 1226 lines (threshold: 800)
- **Impact:** repair_instructions.py reduced from 1226 lines to 765 lines (WATCH status). repair_instructions_docs.py remains at 492 lines. Total 1257 lines split across 2 files.
- **Doc updates:** IMPLEMENTATION_CLI_Code_Architecture.md updated with new file structure, file responsibilities, and dependency diagram.

### 2025-12-18: Remove duplicate code from repair.py

- **What:** Removed ~270 lines of duplicate code from repair.py that was already defined in repair_interactive.py. Functions removed: print_progress_bar, input_listener_thread, spawn_manager_agent, check_for_manager_input, resolve_arbitrage_interactive, and associated global state variables.
- **Why:** MONOLITH issue - file was 983 lines (threshold: 800)
- **Impact:** repair.py reduced from 983 lines to 712 lines. Code now properly uses imports from repair_interactive.py instead of shadowing them with local duplicates.

### 2025-12-18: Verified repair_core.py functions as complete (false positive)

- **What:** Verified that `get_issue_symbol` and `get_issue_action_parts` in `repair_core.py` are already implemented correctly.
- **Why:** INCOMPLETE_IMPL issue flagged these as empty, but they are complete one-liner dictionary lookups with sensible defaults.
- **Impact:** No code changes needed. Functions return correct tuples used throughout the codebase.
- **Note:** Doctor's empty function detection may flag single-line implementations as incomplete.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| {description} | {level} | `{area}/` | {context} |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** {which VIEW}

**Current focus:** {what the project is working toward right now}

**Key context:**
{The things an agent needs to know that aren't obvious from the code/docs}

**Watch out for:**
{Project-level gotchas}

---

## HANDOFF: FOR HUMAN

**Executive summary:**
{2-3 sentences on project state}

**Decisions made recently:**
{Key choices with rationale}

**Needs your input:**
{Blocked items, strategic questions}

**Concerns:**
{Things that might be problems, flagged for awareness}

---

## TODO

### High Priority

- [ ] {Must do}

### Backlog

- [ ] {Should do}
- IDEA: {Possibility}

---

## CONSCIOUSNESS TRACE

**Project momentum:**
{Is the project moving well? Stuck? What's the energy like?}

**Architectural concerns:**
{Things that feel like they might become problems}

**Opportunities noticed:**
{Ideas that came up during work}

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `{area}/` | {status} | `docs/{area}/SYNC_*.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| {module} | `{code_path}` | `{docs_path}` | {status} |

**Unmapped code:** (run `ngram validate` to check)
- {List any code directories without module mappings}

**Coverage notes:**
{Any notes about why certain code isn't mapped, or plans to add mappings}
