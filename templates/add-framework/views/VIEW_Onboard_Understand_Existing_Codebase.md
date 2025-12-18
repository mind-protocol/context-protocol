# VIEW: Onboard — Understand Existing Codebase

**You're new to this codebase or area and need to get oriented before doing anything.**

---

## WHY THIS VIEW EXISTS

Jumping into unfamiliar code without orientation leads to:
- Misunderstanding design intent
- Breaking conventions you didn't know existed
- Duplicating solutions that already exist
- Wasting time reverse-engineering what docs could tell you

This view is about building mental models before building code.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before starting any work.** Orientation prevents wasted effort. Do not skip this step.

### Start With State

```
.add-framework/state/SYNC_Project_State.md
```

This tells you:
- What the project is doing right now
- Recent changes and their context
- Known issues
- Where attention is focused

### Then Patterns

Browse `docs/` to understand what areas exist. For each relevant area:

```
docs/{area}/SYNC_*.md           — current state of this area
docs/{area}/{module}/PATTERNS_*.md  — why modules are shaped this way
```

PATTERNS files are the most important. They explain design philosophy — the WHY behind the code.

### If Cross-Cutting Concepts Exist

```
docs/concepts/
```

These explain ideas that span multiple modules. Understanding concepts helps you see how pieces connect.

---

## WHAT TO BUILD

A mental model of:
- **What exists** — the major areas and modules
- **Why it's shaped this way** — the design philosophy
- **Where things are** — so you can find what you need
- **What's happening** — current focus and recent changes

---

## QUESTIONS TO ANSWER

- What problem does this project solve?
- Who is it for?
- What are the major architectural boundaries?
- What patterns/conventions are used?
- What's the current state of development?
- Where would my task fit?

---

## OUTPUT

After onboarding, you should be able to:
- Navigate to relevant code/docs without guessing
- Understand why things are structured as they are
- Know who to "ask" (which docs to consult) for different questions
- Identify where your work fits in the larger picture

---

## HANDOFF

**For yourself:** Note what you learned, what's still unclear, what surprised you.

**For human:** If you found gaps in documentation or confusing areas, flag them.
