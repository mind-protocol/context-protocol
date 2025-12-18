# VIEW: Review

**You're reviewing changes made by another agent or human.**

---

## WHY THIS VIEW EXISTS

Review without context leads to:
- Approving changes that violate design principles
- Missing important behavior changes
- Failing to catch drift between docs and code

Your job is to verify the change fits the system.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before approving changes.** Reviews without context miss design violations. Do not skip this step.

### For Each Modified Module

- `docs/{area}/{module}/PATTERNS_*.md` — does change fit the design?
- `docs/{area}/{module}/BEHAVIORS_*.md` — are behaviors preserved or correctly updated?
- `docs/{area}/{module}/IMPLEMENTATION_*.md` — is code structure documented?
- `docs/{area}/{module}/SYNC_*.md` — was state updated?

### Project Level

- `.ngram/state/SYNC_Project_State.md` — is project state updated?

---

## WHAT TO CHECK

### Design Alignment

Does the implementation match PATTERNS? If it deviates:
- Is the deviation justified?
- Is PATTERNS updated with the new understanding?

### Behavior Correctness

Are documented behaviors preserved? If they changed:
- Is BEHAVIORS_*.md updated?
- Is the change intentional?

### State Updates

- Is module SYNC updated with what changed?
- Is project SYNC updated?
- Are handoffs clear?

### No Orphans

- All referenced files exist?
- New code has corresponding docs?

---

## HANDOFFS

**For next agent:** Review status, any concerns, what's approved vs needs work.

**For human:** Summary of what was reviewed, any significant findings.

---

## OBSERVATIONS (Living Documentation)

**At the end of your review, add observations to SYNC AND relevant docs.**

### Remarks
What did you notice? Design concerns, missing documentation, inconsistencies.
→ Add to SYNC and relevant docs

### Suggestions
What should be improved? Code quality, documentation, testing.
→ Add to SYNC with `[ ]` checkbox - these become actionable items

### Propositions
What follow-up work is needed? Related changes, cleanup, documentation.
→ Add to SYNC

**Format in SYNC:**
```markdown
## Review Observations

### Remarks
- [What you noticed]

### Suggestions
- [ ] [Actionable improvement] <!-- Repair will prompt user -->

### Propositions
- [Follow-up work]
```

---

## VERIFICATION

- Code aligns with PATTERNS (or PATTERNS updated)
- Behaviors preserved or correctly updated
- SYNC files updated
- No dead links or orphan files
- Tests pass
- Observations documented
