# VIEW: Refactor — Improve Code Structure Without Changing Behavior

**You're improving code quality, cleaning up technical debt, or restructuring without adding features.**

---

## WHY THIS VIEW EXISTS

Refactoring is high-risk if done without understanding. You're changing HOW without changing WHAT — but you need to deeply understand WHAT to not accidentally break it.

Bad refactoring:
- Breaks behavior that tests don't cover
- Violates design patterns without realizing
- Creates inconsistency with related modules
- Loses important context embedded in "ugly" code

Good refactoring makes the code clearer while preserving all contracts.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before making any changes.** Refactoring without full context causes breakage. Do not skip this step.

### Full Documentation Chain

```
docs/{area}/{module}/PATTERNS_*.md        — what design must be preserved
docs/{area}/{module}/BEHAVIORS_*.md       — what behaviors must not change
docs/{area}/{module}/VALIDATION_*.md      — what invariants must hold
docs/{area}/{module}/IMPLEMENTATION_*.md  — code structure, data flows
docs/{area}/{module}/SYNC_*.md            — any context about why code is shaped this way
```

**Load all of them.** Refactoring requires full understanding.

### Tests

```
tests/{area}/test_{module}.py
```

Tests are your safety net. Know what's covered and what isn't.

### Related Modules

If your refactoring touches interfaces:
```
docs/{area}/{related}/PATTERNS_*.md
```

Understand who depends on you.

---

## BEFORE REFACTORING

**Run tests.** Establish baseline. Everything should pass before you start.

**Identify contracts.** What are the public interfaces? What do other modules depend on? These must not change (unless intentionally, with updates to dependents).

**Check for hidden context.** Sometimes ugly code exists for a reason. Comments, SYNC notes, git history might explain why something is shaped oddly.

---

## WHILE REFACTORING

**Small steps.** Refactor incrementally. Run tests frequently.

**Preserve behavior.** If a test fails, you probably broke something — unless you're intentionally changing behavior (which is feature work, not refactoring).

**Improve clarity.** Refactoring should make the code more obviously correct. If it's getting more complex, reconsider.

---

## AFTER REFACTORING

### Verify

Run all tests. They should pass without changes (if you only refactored).

### Update Docs If Needed

- If algorithm changed: update ALGORITHM_*.md
- If internal structure changed: update IMPLEMENTATION_*.md
- If internal structure changed significantly: note in SYNC
- PATTERNS and BEHAVIORS should NOT change (behavior didn't change)

### Update SYNC

What you refactored, why, what's cleaner now.

---

## HANDOFF

**For next agent:** What was restructured, what's cleaner, any areas that still need work.

**For human:** Summary of improvements, any risks or areas to watch.
