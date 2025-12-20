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

### Quick Overview

Run `ngram overview` to generate comprehensive maps of the project:
- File tree with sizes
- Bidirectional code↔docs links
- Function definitions and section headers
- Module dependencies

Output:
- `map.md` (project root) — scan this first to see what exists.
- `map_{folder}.md` (e.g., `map_src.md`, `map_app.md`) — specific maps for core directories.
- `docs/map.md` — a copy for the documentation directory.

### Start With State

```
.ngram/state/SYNC_Project_State.md
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

## CODE RESTRUCTURE ANALYSIS

If the codebase structure doesn't match the documentation areas/modules, consider restructuring:

### Identify Natural Boundaries

1. **Backend Areas** — API, services, data access, infrastructure
2. **Frontend Areas** — UI components, state management, routing, styles
3. **Shared Areas** — Types, utils, config, constants

### Typical Area Structure

```
src/
├── backend/           # or api/, server/
│   ├── auth/          # module: authentication
│   ├── users/         # module: user management
│   └── payments/      # module: billing/payments
├── frontend/          # or client/, web/, app/
│   ├── components/    # module: UI components
│   ├── pages/         # module: routes/views
│   ├── state/         # module: state management
│   └── styles/        # module: theming/CSS
├── shared/            # or common/, lib/
│   ├── types/         # module: shared types
│   └── utils/         # module: utilities
└── infra/             # module: deployment, CI/CD
```

### Frontend Considerations

- **Component library** — Shared UI primitives (buttons, inputs, modals)
- **Feature modules** — Self-contained features with their own state
- **Layout components** — Page shells, navigation, sidebars
- **Hooks/utilities** — Reusable logic (useAuth, useFetch, etc.)
- **Styles architecture** — Global vs scoped, theming, design tokens

### Module Mapping Checklist

For each code directory, answer:

1. **Is it a module?** — Does it have clear boundaries and purpose?
2. **Which area?** — Backend, frontend, shared, infra?
3. **What docs exist?** — PATTERNS, SYNC, BEHAVIORS?
4. **What's missing?** — Add to modules.yaml if unmapped

### Restructure Recommendations

After analysis, propose changes like:

```markdown
## Proposed Structure Changes

### Move
- `src/helpers/` → `src/shared/utils/` (generic utilities)
- `src/api/` → `src/backend/api/` (clearer area boundary)

### Split
- `src/components/` → `src/frontend/components/` + `src/frontend/pages/`

### Create
- `src/frontend/state/` — extract state management from components
- `docs/frontend/` — document frontend architecture

### Update modules.yaml
- Add frontend module mappings
- Add shared module mappings
```

---

## OUTPUT

After onboarding, you should be able to:
- Navigate to relevant code/docs without guessing
- Understand why things are structured as they are
- Know who to "ask" (which docs to consult) for different questions
- Identify where your work fits in the larger picture
- **Propose restructuring** if code doesn't match logical areas/modules

---

## HANDOFF

**For yourself:** Note what you learned, what's still unclear, what surprised you.

**For human:** If you found gaps in documentation or confusing areas, flag them.
