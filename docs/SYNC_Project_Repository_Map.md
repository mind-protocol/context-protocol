# Project Repository Map - Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex (doc template drift repair)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- The repository map format and file tree are stable enough for daily navigation and review.

**What's still being designed:**
- How much derived metadata (sections, refs, definitions) to embed versus link elsewhere.

**What's proposed (v2+):**
- Auto-refresh cadence tracking and diff summaries baked into the map output.

---

## CURRENT STATE

This file is a generated snapshot of the repository structure and doc/code link inventory, last produced by `ngram overview`, and it serves as a single place to scan tree layout, doc sections, and reference mappings. It is accurate for the timestamp noted below but must be regenerated after material changes.

---

## IN PROGRESS

### Repository map template alignment

- **Started:** 2025-12-20
- **By:** codex
- **Status:** completed
- **Context:** The map file needed the standard SYNC sections so downstream tools and reviews can read state consistently; the content now captures drift status and handoff notes for future refresh work.

---

## RECENT CHANGES

### 2025-12-20: Restore missing SYNC sections

- **What:** Added the standard SYNC template sections to the repository map sync file and documented current expectations for refresh behavior.
- **Why:** The doctor flagged missing template fields, so the map needed consistent metadata for handoffs and status tracking.
- **Files:** `docs/SYNC_Project_Repository_Map.md`
- **Struggles/Insights:** The map content is auto-generated, so keeping a lightweight, human-authored preface is the least invasive fix.

---

## KNOWN ISSUES

### Map snapshot may be stale after repo changes

- **Severity:** medium
- **Symptom:** The tree and doc refs may not reflect new files or doc fixes until `ngram overview` is rerun.
- **Suspected cause:** The map is generated on demand and not auto-refreshed in the repair pipeline.
- **Attempted:** No automation changes made; documented the expected refresh step here instead.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** `VIEW_Implement_Write_Or_Modify_Code.md`

**Where I stopped:** The SYNC sections are restored; the generated map body remains untouched.

**What you need to understand:**
This file is primarily generated output, so any future updates should preserve the map body and only adjust the SYNC preface or rerun `ngram overview` if the tree or refs need refresh.

**Watch out for:**
Re-running the overview may overwrite this preface unless the generator preserves it; verify before regenerating.

**Open questions I had:**
Should the generator be updated to include these SYNC sections automatically, or should this file remain a hand-maintained wrapper?

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Repaired `docs/SYNC_Project_Repository_Map.md` to include the required SYNC sections without altering the generated map content. The file now documents refresh expectations and the current status of the map snapshot.

**Decisions made:**
Chose to add a minimal, human-authored preface rather than regenerate or reformat the map body.

**Needs your input:**
Confirm whether you want the `ngram overview` generator to emit SYNC sections automatically in the future.

---

## CONSCIOUSNESS TRACE

The main tension here is between preserving generated output and satisfying the SYNC template requirements, so I opted for a minimal preface that documents intent without touching the map body. I am confident the fix aligns with the template drift check, but I am unsure whether the map generator should be updated to avoid future drift.

---

## MATURITY

STATUS: DESIGNING

The repository map is generated output and still being tuned for completeness,
so the doc is treated as designing while coverage and format stabilize.

## CURRENT STATE

This file captures the latest generated map snapshot and embedded references
from `ngram overview`, serving as the canonical repository map for the project.

## IN PROGRESS

No active regeneration is running right now, but the map will need refreshes as
files move, new modules appear, or doc chains are reorganized.

## RECENT CHANGES

Filled the missing sync template sections so this map doc matches the required
SYNC structure and passes template drift checks.

## KNOWN ISSUES

The map may be stale relative to the live repo if new files were added after
the last overview run; regenerate when accuracy matters.

## HANDOFF: FOR AGENTS

Use `VIEW_Implement_Write_Or_Modify_Code.md` and rerun `ngram overview` after
significant repo changes to keep this map aligned with current structure.

## HANDOFF: FOR HUMAN

Decide whether the map should be refreshed on a cadence or only after major
structural changes; that choice affects how often this file is updated.

## TODO

- [ ] Re-run `ngram overview` after the next major doc or code reorganization.
- [ ] Confirm whether the map should include repo root artifacts like logs.

## CONSCIOUSNESS TRACE

Focus remains on keeping a reliable map as navigation; the missing sections
were drift, not conceptual uncertainty about the map's role.

## POINTERS

- `docs/map.md` contains the overview output in a shorter top-level file.
- `ngram/repo_overview.py` defines how the map is generated and serialized.


---

## ARCHIVE

Older content archived to: `SYNC_Project_Repository_Map_archive_2025-12.md`
