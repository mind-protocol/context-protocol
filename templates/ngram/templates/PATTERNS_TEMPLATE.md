# {Module Name} — Patterns: {Brief Design Philosophy Description}

```
STATUS: DRAFT | REVIEW | STABLE
CREATED: {DATE}
VERIFIED: {DATE} against {COMMIT}
```

---

## CHAIN

```
THIS:            PATTERNS_*.md (you are here)
BEHAVIORS:       ./BEHAVIORS_*.md
ALGORITHM:       ./ALGORITHM_*.md
VALIDATION:      ./VALIDATION_*.md
IMPLEMENTATION:  ./IMPLEMENTATION_*.md
TEST:            ./TEST_*.md
SYNC:            ./SYNC_*.md

IMPL:            {path/to/main/source/file.py}
```

### Bidirectional Contract

**Before modifying this doc or the code:**
1. Read ALL docs in this chain first
2. Read the linked IMPL source file

**After modifying this doc:**
1. Update the IMPL source file to match, OR
2. Add a TODO in SYNC_*.md: "Docs updated, implementation needs: {what}"
3. Run tests: `{test command}`

**After modifying the code:**
1. Update this doc chain to match, OR
2. Add a TODO in SYNC_*.md: "Implementation changed, docs need: {what}"
3. Run tests: `{test command}`

---

## THE PROBLEM

{What problem does this module solve?}
{What's wrong with NOT having this?}
{What pain does this address?}

---

## THE PATTERN

{What is the core design approach?}
{What shape does the solution take?}
{What's the key insight that makes this work?}

---

## PRINCIPLES

### Principle 1: {Name}

{Description of principle}
{Why this matters}

### Principle 2: {Name}

{Description of principle}
{Why this matters}

### Principle 3: {Name}

{Description of principle}
{Why this matters}

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| {path} | {reason} |
| {path} | {reason} |

---

## INSPIRATIONS

{What prior art informed this design?}
{What patterns from other systems?}
{What literature or theory applies?}

---

## WHAT THIS DOES NOT SOLVE

{What is explicitly out of scope?}
{What might someone expect that this doesn't do?}
{What limitations are inherent?}

---

## GAPS / IDEAS / QUESTIONS

- [ ] {Open question or todo}
- [ ] {Another item}
- IDEA: {Future possibility}
- QUESTION: {Unresolved uncertainty}
