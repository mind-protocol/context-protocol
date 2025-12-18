# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-18
UPDATED_BY: repair-agent (NO_DOCS_REF fix for validate.py)
```

---

## CURRENT STATE

{Narrative of the project's current state. Not a feature list — the story of where things are.}

---

## ACTIVE WORK

### {Work Stream}

- **Area:** `{area}/`
- **Status:** {in progress / blocked}
- **Owner:** {agent/human}
- **Context:** {what's happening, why it matters}

---

## RECENT CHANGES

### 2025-12-18: Added DOCS reference to validate.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/validate.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for validate.py

### 2025-12-18: Added DOCS reference to sync.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/sync.py`; added sync.py to modules.yaml internal list
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for sync.py

### 2025-12-18: Added DOCS reference to utils.py

- **What:** Added `DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to docstring of `src/ngram/utils.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for utils.py

### 2025-12-18: Added DOCS reference to repair_report.py

- **What:** Added `DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to docstring of `src/ngram/repair_report.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for repair_report.py

### 2025-12-18: Added DOCS reference to repair_instructions.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/repair_instructions.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for repair_instructions.py

### 2025-12-18: Added DOCS reference to repair.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/repair.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for repair.py

### 2025-12-18: Added DOCS reference to repair_core.py

- **What:** Added `DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to docstring of `src/ngram/repair_core.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for repair_core.py

### 2025-12-18: Added DOCS reference to init_cmd.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/init_cmd.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for init_cmd.py

### 2025-12-18: Added DOCS reference to prompt.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/prompt.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for prompt.py

### 2025-12-18: Added DOCS reference to project_map.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/project_map.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for project_map.py

### 2025-12-18: Fixed BROKEN_IMPL_LINK in CLI docs

- **What:** Updated `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` line 181 reference from `ALGORITHM_CLI_Logic.md` to `docs/cli/ALGORITHM_CLI_Logic.md`
- **Why:** Doctor check extracts backtick refs and searches from project root, not relative to doc file
- **Impact:** CLI module no longer has BROKEN_IMPL_LINK issue

### 2025-12-18: Added DOCS reference to doctor_files.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/doctor_files.py`
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for this file

### 2025-12-18: Added DOCS reference to github.py

- **What:** Added `# DOCS: docs/cli/PATTERNS_Why_CLI_Over_Copy.md` to `src/ngram/github.py`; added github.py to modules.yaml internal list
- **Why:** NO_DOCS_REF issue - file lacked bidirectional link to documentation
- **Impact:** Enables `ngram context` to find doc chain for github.py

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
