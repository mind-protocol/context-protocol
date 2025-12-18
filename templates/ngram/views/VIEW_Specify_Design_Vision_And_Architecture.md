# VIEW: Specify

**You're specifying or designing — defining what should exist before it's built.**

---

## WHY THIS VIEW EXISTS

Building without specification leads to:
- Solving the wrong problem
- Missing the target audience's needs
- Architectural decisions made ad-hoc under pressure
- Scope creep and unclear boundaries

This view is for thinking before building. It's about defining the "what" and "why" before the "how."

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before designing.** Specification requires understanding what already exists. Do not skip this step.

### Project Level

- `.ngram/state/SYNC_Project_State.md` — what exists now
- Existing `PATTERNS_*.md` files — understand current design philosophy

### If Specifying New Area

- Related areas' PATTERNS — maintain consistency
- `docs/concepts/` — existing concepts you might use or extend

### If Refining Existing Area

- Full documentation chain for that area
- Dependencies and dependents

---

## WHAT TO SPECIFY

### Vision

What is this trying to achieve? Not features — outcomes.
- What problem does this solve?
- For whom?
- What does success look like?

### Audience

Who will use this? What do they need?
- User types and their goals
- Technical vs non-technical
- Constraints they operate under

### UX / Interface

How will users interact with this?
- Key workflows
- What should feel easy?
- What complexity is acceptable?

### Boundaries

What is explicitly OUT of scope?
- What this is NOT
- What it won't handle
- Adjacent problems that are separate

### Technical Approach

High-level architecture:
- Key components and their responsibilities
- How they interact
- Critical constraints (performance, scale, compatibility)

---

## OUTPUT

Specification should produce:
- PATTERNS_*.md for the area/module being specified
- Clear scope and boundaries
- Enough detail for implementation to begin

---

## HANDOFFS

**For implementing agent:** What needs to be built, what's the priority, what questions remain.

**For human:** Vision summary, key decisions made, decisions that need human input.

---

## VERIFICATION

- Is the problem clearly stated?
- Is the audience defined?
- Are boundaries explicit?
- Is there enough detail to implement?
- Are open questions documented?
