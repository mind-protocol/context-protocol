# Link Axes — Sync: Current State

```
LAST_UPDATED: 2025-12-20
UPDATED_BY: codex
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Link types limited to AT/CONTAINS/LEADS_TO/PRIMES/RELATES.

**What's still being designed:**
- Enforcement of required axes at write time.

**What's proposed (v2+):**
- Auto-linting for missing axes in graph writes.

---

## CURRENT STATE

Link-axes schema docs are defined with 15 concrete instances, a link matrix,
and a rich attribute catalog. Runtime enforcement is not implemented yet.

---

## IN PROGRESS

### Link axes module scaffolding

- **Started:** 2025-12-20
- **By:** codex
- **Status:** in progress
- **Context:** Establish schema and validation before runtime enforcement.

---

## RECENT CHANGES

### 2025-12-20: Added link axes module

- **What:** Created PATTERNS/BEHAVIORS/SCHEMA/VALIDATION/SYNC docs.
- **Why:** Encode semantic links via axes instead of proliferating link types.
- **Files:** docs/schema/link-axes/*
- **Struggles/Insights:** Kept link types minimal and attributes explicit.

---

## KNOWN ISSUES

### No enforcement yet

- **Severity:** medium
- **Symptom:** links may exist without required axes.
- **Suspected cause:** no write-time validation.
- **Attempted:** doc-only.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement_Write_Or_Modify_Code

**Where I stopped:** Docs complete; enforcement not implemented.

**What you need to understand:**
RELATES and PRIMES require axes. CONTRADICTS is encoded as polarity < 0.

**Watch out for:**
Do not reintroduce specialized link types.

**Open questions I had:**
Where to enforce axes (GraphOps vs schema layer).

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Link axes schema is documented and ready for enforcement.

**Decisions made:**
Five link types only; semantic meaning via axes.

**Needs your input:**
Where to enforce validation (write-time vs lint-only).

---

## TODO

### Doc/Impl Drift

<!-- @ngram:todo DOCS→IMPL: Add write-time validation for required axes. -->

### Tests to Run

```bash
ngram validate
```

### Immediate

<!-- @ngram:todo Decide enforcement location. -->
<!-- @ngram:todo Add schema lint for axes. -->

### Later

<!-- @ngram:todo Consider migration script for legacy link types. -->

---

## CONSCIOUSNESS TRACE

**Mental state when stopping:**
Clear and confident; waiting on enforcement decisions.

**Threads I was holding:**
Write-time validation and migration of existing data.

**Intuitions:**
Axes are more stable than proliferating link types.

**What I wish I'd known at the start:**
How strict the enforcement should be during migration.

---

## POINTERS

| What | Where |
|------|-------|
| Schema | `docs/schema/link-axes/SCHEMA_Link_Axes.md` |
| Patterns | `docs/schema/link-axes/PATTERNS_Link_Axes_Not_Types.md` |
| Validation | `docs/schema/link-axes/VALIDATION_Link_Axes.md` |
