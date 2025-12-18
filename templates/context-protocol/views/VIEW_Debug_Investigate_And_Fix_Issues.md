# VIEW: Debug

**You're debugging an issue or investigating unexpected behavior.**

---

## WHY THIS VIEW EXISTS

Debugging without context leads to:
- Fixing symptoms instead of root causes
- Breaking other things while fixing one thing
- Repeated debugging of the same issue

This view ensures you understand the system before changing it.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before attempting fixes.** Understanding the system prevents fixing symptoms instead of causes. Do not skip this step.

### Then: Understand Expected Behavior

Before assuming something is broken, confirm what should happen:
- `docs/{area}/{module}/BEHAVIORS_*.md` — expected behaviors
- `docs/{area}/{module}/SYNC_*.md` — known issues, recent changes

Often "bugs" are misunderstandings of intended behavior.

### Second: Understand the Logic

If behavior is genuinely wrong:
- `docs/{area}/{module}/ALGORITHM_*.md` — how it's supposed to work
- `docs/{area}/{module}/VALIDATION_*.md` — what invariants should hold
- `docs/{area}/{module}/IMPLEMENTATION_*.md` — where is the code, how data flows

### Third: Check Cross-Module Issues

If the bug involves interactions:
- `docs/concepts/{concept}/TOUCHES_*.md` — see all modules involved
- The bug might be in the interaction, not any single module

---

## THE WORK

Narrow the scope:
- Reproduce reliably
- Find minimal case
- Identify which invariant is violated

---

## WHEN YOU FIND IT

### Document Before Fixing

Add to SYNC:
- Symptom (what was observed)
- Root cause (what was actually wrong)
- Fix (what you're doing)

This helps if the fix doesn't work or creates new issues.

### After Fixing

- Verify the symptom is gone
- Verify existing tests pass
- Consider adding a test to prevent regression

---

## HANDOFFS

**For next agent:** Was the fix complete? Any remaining concerns?

**For human:** What was broken, what's fixed, any implications?

---

## VERIFICATION

- Does the fix address root cause (not just symptom)?
- Is the bug documented in SYNC?
- Is there a test preventing regression?
