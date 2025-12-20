# Project — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
```

---

## CURRENT STATE

Imported the graph ownership docs from `~/the-blood-ledger` for all non-conflicting entries in `data/graph_scope_classification.yaml`, while explicitly skipping conflicting `.ngram/` and `AGENTS.md` paths. Four source paths were missing upstream and remain unimported. The source tree appears read-only, so I could not delete the originals to complete a true move.

---

## ACTIVE WORK

### Graph ownership intake

- **Area:** `docs/`
- **Status:** in progress
- **Owner:** agent
- **Context:** Copied non-conflicting graph docs and engine sources from `~/the-blood-ledger`; conflicts still need a merge decision.
- **Blocker:** Source tree is not writable (`Permission denied` on delete), so the move could not be completed.

---

## RECENT CHANGES

### 2025-12-20: Import graph ownership files

- **What:** Copied 157 non-conflicting files from `~/the-blood-ledger` based on `data/graph_scope_classification.yaml`; skipped 45 conflicts; 4 source paths were missing upstream.
- **Why:** Bring the graph schema/physics/engine materials into this repo without overwriting existing protocol assets.
- **Impact:** New docs and engine files now exist under `docs/` and `engine/`, with remaining conflicts awaiting a decision.

---

## KNOWN ISSUES

| Issue | Severity | Area | Notes |
|-------|----------|------|-------|
| Conflicting `.ngram/` + `AGENTS.md` paths in intake list | medium | `/.ngram` | Skipped; requires manual decision before importing. |
| Missing upstream paths in intake list | low | `engine/` | `engine/models/tensions.py`, `engine/db/graph_ops.py`, `engine/api/app.py`, `engine/infrastructure/memory/transcript.py` |
| Source tree is read-only | medium | `~/the-blood-ledger` | Unable to remove originals to complete the move. |

---

## HANDOFF: FOR AGENTS

**Likely VIEW for continuing:** `VIEW_Extend_Add_Features_To_Existing.md`

**Current focus:** Import the graph ownership docs listed in `data/graph_scope_classification.yaml`, resolving the 45 conflicts explicitly before copying.

**Key context:**
The repo already has `.ngram/` and `AGENTS.md` files; those paths are part of the intake list but were intentionally skipped.

**Watch out for:**
Do not overwrite `.ngram/` content or root `AGENTS.md` unless a human explicitly approves the merge strategy.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Imported 157 non-conflicting graph ownership files from `~/the-blood-ledger`. Conflicting `.ngram/` and `AGENTS.md` paths remain unresolved.

**Decisions made recently:**
Skipped all conflicting `.ngram/` and root-level paths to avoid overwriting existing protocol assets.

**Needs your input:**
How should we reconcile the 45 conflicting files in `.ngram/` and `AGENTS.md` when importing the graph docs?
Also, can you make `~/the-blood-ledger` writable or confirm a safe deletion method so we can complete the move?

**Concerns:**
If we copy the conflicting paths without a merge plan, the protocol bootstrap could be overwritten.

---

## TODO

### High Priority

- [ ] Decide how to merge or ignore conflicting `.ngram/` and `AGENTS.md` entries in the intake list.

### Backlog

- [ ] Import the non-conflicting graph docs into the newly created directories.
- IDEA: Use `ngram refactor` actions once files are in place to reconcile area/module layout changes cleanly.

---

## CONSCIOUSNESS TRACE

**Project momentum:**
Forward motion on intake preparation, but blocked by conflict resolution decisions.

**Architectural concerns:**
Overwriting `.ngram/` content would damage protocol continuity; conflicts must be resolved deliberately.

**Opportunities noticed:**
The refactor command can standardize doc moves once the import is staged.

---

## AREAS

| Area | Status | SYNC |
|------|--------|------|
| `docs/` | in progress | `docs/SYNC_Project_Repository_Map.md` |

---

## MODULE COVERAGE

Check `modules.yaml` (project root) for full manifest.

**Mapped modules:**
| Module | Code | Docs | Maturity |
|--------|------|------|----------|
| prompt | `ngram/prompt.py` | `docs/cli/prompt/` | DESIGNING |
| cli_core | `ngram/**` | `docs/cli/core/` | CANONICAL |
| llm_agents | `ngram/llms/**` | `docs/llm_agents/` | DESIGNING |
| tui | `ngram/tui/**` | `docs/tui/` | DESIGNING |

**Unmapped code:** (run `ngram validate` to check)
- `engine/` (incoming graph intake directories created; not yet mapped)

**Coverage notes:**
Graph ownership modules are staged as folders only; mapping will happen after files are imported.
