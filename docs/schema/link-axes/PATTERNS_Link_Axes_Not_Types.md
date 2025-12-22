# Schema — Patterns: Link Axes, Not Link Types

```
STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against local tree
```

---

## CHAIN

```
THIS:            PATTERNS_Link_Axes_Not_Types.md (you are here)
BEHAVIORS:       ./BEHAVIORS_Link_Axes.md
SCHEMA:          ./SCHEMA_Link_Axes.md
VALIDATION:      ./VALIDATION_Link_Axes.md
SYNC:            ./SYNC_Link_Axes.md
```

---

## THE PROBLEM

A large number of specialized link types (GOVERNS, IMPLEMENTS, GUARANTEES,
CONTRADICTS, etc.) makes the graph hard to reason about and impossible to keep
consistent. A single RELATES type without structure is equally bad: everything
becomes indistinguishable and loses meaning.

---

## THE PATTERN

Use a **small fixed set of link types** and encode semantics using **axes**
(attributes) on links. The core link types are:

- AT (localization/scope)
- CONTAINS (hierarchy)
- LEADS_TO (pointers/version/derivation)
- PRIMES (activation/priming)
- RELATES (generic semantics with required axes)

Semantics that used to require distinct link types are expressed via axes like
`role`, `mode`, `polarity`, `strength`, and `confidence`.

---

## PRINCIPLES

### Principle 1: Small Link Type Set

Use the five link types only. Everything else is expressed via axes.

### Principle 2: Mandatory Axes

RELATES and PRIMES must carry required axes; without them they are invalid.

### Principle 3: Semantics Are Axes

Support/contradict, govern/implement, and evidential vs normative are captured
via `polarity`, `role`, and `mode`, not new link types.

---

## DATA

| Source | Type | Purpose / Description |
|--------|------|-----------------------|
| `SCHEMA_Link_Axes.md` | FILE | Canonical node/link axes and required fields |
| Graph state | OTHER | Runtime storage of axes on link properties |

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `docs/schema/SCHEMA/SCHEMA_Links.md` | Base graph link schema constraints |
| `docs/physics/PATTERNS_Physics.md` | Semantics for polarity and strength |
| `docs/engine/moments/PATTERNS_Moments.md` | Moment visibility rules |

---

## INSPIRATIONS

- Typed edges with semantic axes in knowledge graphs.
- Physics-style parameters instead of enumerated types.

---

## SCOPE

### In Scope

- Define link axes and required fields.
- Specify how to encode semantic meaning via axes.

### Out of Scope

- Defining runtime propagation formulas (belongs in physics).
- Introducing new link types beyond the core five.

---

## MARKERS

<!-- @ngram:todo Define strict validation rules for missing axes. -->
<!-- @ngram:todo Decide when RELATES vs PRIMES is required. -->
