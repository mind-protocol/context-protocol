# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: repair-agent
```

---

## CURRENT STATE

ngram CLI project with doctor/repair functionality for maintaining project health.

---

## ACTIVE WORK

### Monolith Refactoring

- **Area:** `ngram/`
- **Status:** completed
- **Owner:** repair-agent
- **Context:** Reducing file sizes to meet 800-line threshold

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| INCOMPLETE_IMPL false positives | info | `ngram/` | Doctor flags one-liner functions as "empty". Files have explanatory comments. Consider improving empty function detection heuristics. |
| HARDCODED_CONFIG false positives | info | `ngram/` | Doctor flags W3C namespace URIs as "hardcoded URLs". Added ignore for SVG namespace in project_map_html.py. |

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


---

## ARCHIVE

Older content archived to: `SYNC_Project_State_archive_2025-12.md`
