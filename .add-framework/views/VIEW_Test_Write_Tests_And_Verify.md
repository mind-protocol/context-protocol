# VIEW: Test — Write Tests and Verify Correctness

**You're writing tests, improving test coverage, or verifying that code works correctly.**

---

## WHY THIS VIEW EXISTS

Code without tests is a promise without proof. Tests:
- Verify behavior matches intent
- Catch regressions before they ship
- Document expected behavior through examples
- Enable confident refactoring

This view is about turning VALIDATION specifications into executable verification.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before writing tests.** Tests verify intent, and you must understand intent first. Do not skip this step.

### For the Module You're Testing

```
docs/{area}/{module}/VALIDATION_*.md      — what invariants must hold
docs/{area}/{module}/BEHAVIORS_*.md       — what behaviors to test
docs/{area}/{module}/PATTERNS_*.md        — understand design to test meaningfully
docs/{area}/{module}/IMPLEMENTATION_*.md  — where is the code to test
```

VALIDATION is your primary source. It lists:
- Invariants (things that must always be true)
- Properties (things that should hold for all inputs)
- Error conditions (how failures should behave)
- What's tested vs what's not

### Existing Tests

```
tests/{area}/test_{module}.py
```

Understand what's already covered before adding more.

---

## WHAT TO TEST

### From VALIDATION

Each invariant (V1, V2, etc.) should have corresponding tests. If VALIDATION says "NOT YET TESTED," that's your target.

### From BEHAVIORS

Each behavior (B1, B2, etc.) describes a GIVEN/WHEN/THEN. These translate directly to test cases.

### Edge Cases

BEHAVIORS lists edge cases (E1, E2, etc.). These are often where bugs hide.

### Anti-Behaviors

BEHAVIORS lists what should NOT happen. Test that it doesn't.

---

## WRITING GOOD TESTS

**Test the contract, not the implementation.** If PATTERNS says "this module provides X," test that X works — not how X is achieved internally.

**Name tests after what they verify.** `test_V1_weight_never_negative` is better than `test_weight_1`.

**Reference the spec.** In test docstrings or comments, note which invariant/behavior you're testing.

---

## AFTER TESTING

### Update VALIDATION

Mark what's now tested:
```
V3: {invariant}
Tested by: test_xxx, test_yyy
```

### Update SYNC

Note what tests were added and what coverage changed.

### If You Found Bugs

Document in SYNC. Decide: fix now or file for later?

---

## HANDOFF

**For next agent:** What's tested now, what still needs tests, any tricky areas.

**For human:** Test coverage summary, any concerns about testability.
