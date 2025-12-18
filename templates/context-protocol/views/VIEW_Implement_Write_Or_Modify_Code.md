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

1. **Project state:** `.context-protocol/state/SYNC_Project_State.md`
   - What's happening in the project
   - Recent changes that might affect your work

2. **Module manifest:** `.context-protocol/modules.yaml`
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

Use templates from `.context-protocol/templates/`.

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
# .context-protocol/modules.yaml
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

## VERIFICATION

- Does code reflect PATTERNS?
- Do tests pass (if they exist)?
- Is SYNC updated?
- Could another agent continue your work with what you've written?
