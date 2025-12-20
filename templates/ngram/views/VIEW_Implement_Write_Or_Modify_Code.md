# VIEW: Implement

**You're implementing new code or modifying existing modules.**

---

## WHY THIS VIEW EXISTS

Implementation without context leads to:
- Code that violates existing design patterns
- Duplication of solved problems
- Undocumented changes that confuse future agents

This view ensures you understand before you build.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before writing any code.** Understanding must precede implementation. Do not skip this step.

### Always

1. **Project state:** `.ngram/state/SYNC_Project_State.md`
   - What's happening in the project
   - Recent changes that might affect your work

2. **Module manifest:** `modules.yaml` (project root)
   - Find which module your code belongs to
   - Check dependencies, patterns, ownership

3. **Module docs (if module exists):**
   - `docs/{area}/{module}/PATTERNS_*.md` — understand the design
   - `docs/{area}/{module}/SYNC_*.md` — understand current state

### If Creating New Module

No existing docs? Create them first:
- PATTERNS: Why does this module exist? What's the design approach?
- SYNC: Current state (even if just "starting implementation")
- **modules.yaml**: Add mapping for the new code directory

Use templates from `.ngram/templates/`.

### If Unclear

- `BEHAVIORS_*.md` — what should this do?
- `ALGORITHM_*.md` — how does current logic work?
- `IMPLEMENTATION_*.md` — where is the code? how does data flow?
- `docs/concepts/` — if you're working with cross-cutting concepts

---

## THE WORK

Your implementation should reflect the PATTERNS. If you find yourself fighting the design:
- Either adjust your approach
- Or update PATTERNS with justification for the change

---

## BEFORE VERIFICATION: DOC VERIFICATION

**After implementing, before running tests, verify against docs:**

Compare your implementation to the documentation chain:

| Doc Type | Check |
|----------|-------|
| `PATTERNS_*.md` | Does code follow the design philosophy? Is this in scope? |
| `BEHAVIORS_*.md` | Does code produce the documented behaviors? |
| `ALGORITHM_*.md` | Does code follow the documented procedures? |
| `VALIDATION_*.md` | Are invariants maintained? |
| `IMPLEMENTATION_*.md` | Does code structure match what's documented? |

**If implementation differs from docs:**
1. Is the doc outdated? → Update the doc, add DECISION to SYNC
2. Is your code wrong? → Fix the code
3. Is it a design improvement? → Update doc with reasoning, add DECISION to SYNC

**This step prevents:**
- Implementing something that contradicts documented design
- Tests passing but behavior being wrong
- Silent drift between docs and code

---

## AFTER IMPLEMENTATION

### Update State

Update SYNC files with:
- What you implemented
- Why (briefly)
- What's working, what's not
- What's left to do

### Update Module Manifest

If you created new code directories or changed structure:

```yaml
# modules.yaml (project root)
modules:
  your_module:
    code: "src/path/to/code/**"
    docs: "docs/area/module/"
    maturity: DESIGNING
    # ... other fields as relevant
```

### Handoffs

**For next agent:** Which VIEW will they likely need? What do they need to know?

**For human:** Brief summary if significant decisions were made.

### If Behavior Changed

Update `BEHAVIORS_*.md` to reflect new observable behavior.

---

## OBSERVATIONS (Living Documentation)

**At the end of your work, add observations to SYNC AND relevant docs.**

Documentation is living - update it with what you learned.

### Remarks
What did you notice? Code smells, unclear areas, inconsistencies.
→ Add to SYNC and relevant PATTERNS/IMPLEMENTATION docs

### Suggestions
What should be improved? Technical debt, refactoring, missing tests.
→ Add to SYNC with `[ ]` checkbox - these become actionable items

### Propositions
What would you do next? Future features, optimizations, cleanups.
→ Add to SYNC and relevant PATTERNS docs (proposed section)

**Format in SYNC:**
```markdown
## Agent Observations

### Remarks
- [What you noticed]

### Suggestions
- [ ] [Actionable improvement] <!-- Repair will prompt user -->
- [ ] [Another suggestion]

### Propositions
- [What future agents could tackle]
```

**IMPORTANT:** Suggestions with `[ ]` checkboxes will be detected by `ngram repair` and offered to the user interactively. If accepted, an agent will be spawned to implement the suggestion.

---

## VERIFICATION

- Does code reflect PATTERNS?
- Do tests pass (if they exist)?
- Is SYNC updated?
- Are observations documented?
- Could another agent continue your work with what you've written?
