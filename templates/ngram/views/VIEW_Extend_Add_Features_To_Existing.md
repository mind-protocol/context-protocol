# VIEW: Extend

**You're extending existing functionality or adding features to existing modules.**

---

## WHY THIS VIEW EXISTS

Extension without deep understanding leads to:
- Features that fight the existing design
- Breaking existing behavior while adding new
- Inconsistent patterns within the same module

Extensions require more context than new implementations because you're working within existing constraints.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before adding features.** Extensions require deep understanding of existing design. Do not skip this step.

### Module Manifest First

Check `modules.yaml` (project root):
- Find the target module's mapping
- Check its dependencies (what else to load?)
- Check its patterns (conventions to follow)
- Check its maturity (CANONICAL = be careful, DESIGNING = more flexible)

### Deep Load the Target Module

You need full understanding:
- `docs/{area}/{module}/PATTERNS_*.md` — design philosophy
- `docs/{area}/{module}/BEHAVIORS_*.md` — current behaviors (don't break these)
- `docs/{area}/{module}/ALGORITHM_*.md` — how it works (extend coherently)
- `docs/{area}/{module}/VALIDATION_*.md` — what must remain true
- `docs/{area}/{module}/IMPLEMENTATION_*.md` — code structure, data flows
- `docs/{area}/{module}/SYNC_*.md` — current state

### Cross-Cutting Concepts

If your extension involves system-wide concepts:
- `docs/concepts/{concept}/CONCEPT_*.md` — understand the concept
- `docs/concepts/{concept}/TOUCHES_*.md` — see where else it's used

### Dependencies

What depends on this module? Your extension might affect them.

---

## PLANNING

Before implementing, answer:
1. Does this fit existing PATTERNS?
2. Will existing BEHAVIORS continue to work?
3. What new VALIDATION invariants does this create?
4. Is this module the right place for this extension?

Write your plan in SYNC before starting.

---

## THE WORK

- Preserve existing invariants
- Maintain pattern consistency
- Add, don't corrupt

---

## BEFORE VERIFICATION: DOC VERIFICATION

**After implementing your extension, before running tests:**

Re-read the documentation chain and verify:

| Doc Type | Verify |
|----------|--------|
| `PATTERNS_*.md` | Extension follows design philosophy, is in scope |
| `BEHAVIORS_*.md` | Existing behaviors still work, new ones match intent |
| `ALGORITHM_*.md` | New logic integrates with existing procedures |
| `VALIDATION_*.md` | All invariants (old and new) are maintained |
| `IMPLEMENTATION_*.md` | Code structure matches documented architecture |

**If your extension differs from docs:**
1. Doc outdated? → Update it, add DECISION to SYNC
2. Extension wrong? → Fix it before testing
3. Design improvement? → Update doc with reasoning, add DECISION to SYNC

**This prevents:**
- Extensions that silently break documented contracts
- Tests passing but behavior contradicting docs
- Future agents confused by doc/code mismatch

---

## AFTER EXTENDING

### Update All Affected Docs

- BEHAVIORS — add new behaviors
- ALGORITHM — add new logic (if significant)
- VALIDATION — add new invariants
- IMPLEMENTATION — update code structure, data flows
- SYNC — document the extension

### Update Module Manifest

If your extension adds new code directories or changes dependencies:

```yaml
# modules.yaml (project root)
modules:
  your_module:
    depends_on:
      - existing_dep
      - new_dep        # Added by your extension
```

### Update TOUCHES

If your extension expands how a concept is used, update the TOUCHES index.

### Add Tests

New behavior needs tests. Reference VALIDATION.

---

## HANDOFFS

**For next agent:** What was extended, any concerns, what's left to do.

**For human:** Summary of new capability, any design decisions made.

---

## OBSERVATIONS (Living Documentation)

**At the end of your work, add observations to SYNC AND relevant docs.**

### Remarks
What did you notice? Design tensions, integration challenges, unclear boundaries.
→ Add to SYNC and relevant PATTERNS/IMPLEMENTATION docs

### Suggestions
What should be improved? Refactoring, abstraction needs, documentation gaps.
→ Add to SYNC with `[ ]` checkbox - these become actionable items

### Propositions
What would you do next? Related extensions, optimizations, architectural improvements.
→ Add to SYNC and relevant PATTERNS docs (proposed section)

**Format in SYNC:**
```markdown
## Agent Observations

### Remarks
- [What you noticed]

### Suggestions
- [ ] [Actionable improvement] <!-- Repair will prompt user -->

### Propositions
- [What future agents could tackle]
```

**IMPORTANT:** Suggestions with `[ ]` checkboxes will be offered interactively during `ngram repair`.

---

## VERIFICATION

- Extension fits existing PATTERNS
- Existing behaviors preserved
- New behaviors documented
- New invariants documented
- Tests added
- SYNC updated
- Observations documented
