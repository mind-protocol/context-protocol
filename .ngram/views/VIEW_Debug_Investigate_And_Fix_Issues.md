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

### Before Testing: Doc Verification

**After implementing fix, before verifying it works:**

Compare your fix against the documentation chain:

| Doc Type | Verify |
|----------|--------|
| `PATTERNS_*.md` | Fix follows design philosophy, respects scope |
| `BEHAVIORS_*.md` | Fix restores documented behavior |
| `ALGORITHM_*.md` | Fix aligns with documented procedures |
| `VALIDATION_*.md` | Fix maintains all invariants |
| `IMPLEMENTATION_*.md` | Fix matches documented code structure |

**If fix differs from docs:**
1. Was doc wrong? → Update it, add DECISION to SYNC
2. Is fix wrong? → Revise before testing
3. Is it an improvement? → Update doc with reasoning

### After Fixing

- Verify the symptom is gone
- Verify existing tests pass
- Consider adding a test to prevent regression

---

## HANDOFFS

**For next agent:** Was the fix complete? Any remaining concerns?

**For human:** What was broken, what's fixed, any implications?

---

## OBSERVATIONS (Living Documentation)

**At the end of your work, add observations to SYNC AND relevant docs.**

### Remarks
What did you notice? Fragile areas, unclear logic, missing error handling.
→ Add to SYNC and relevant PATTERNS/IMPLEMENTATION docs

### Suggestions
What should be improved? Error handling, logging, defensive coding, test coverage.
→ Add to SYNC with `[ ]` checkbox - these become actionable items

### Propositions
What related issues might exist? Similar bugs, systemic problems, preventive measures.
→ Add to SYNC and relevant docs

**Format in SYNC:**
```markdown
## Agent Observations

### Remarks
- [What you noticed]

### Suggestions
- [ ] [Actionable improvement] <!-- Repair will prompt user -->

### Propositions
- [What future agents could investigate]
```

**IMPORTANT:** Suggestions with `[ ]` checkboxes will be offered interactively during `ngram repair`.

---

## VERIFICATION

- Does the fix address root cause (not just symptom)?
- Is the bug documented in SYNC?
- Is there a test preventing regression?
- Are observations documented?
