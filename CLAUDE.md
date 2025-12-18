@templates/CLAUDE_ADDITION.md

---

@templates/context-protocol/PRINCIPLES.md

---

@templates/context-protocol/PROTOCOL.md

# Context Protocol

This project follows the Context Protocol — a system that ensures you load the right context for your task and leave useful state for the next agent.

---

## Why This Matters

You have a limited context window. You can't load everything. Without guidance, you'll either:
- Load too much and miss what matters
- Load too little and hallucinate structure
- Make changes without understanding design intent
- Leave no trace for the next session

The protocol solves this: **VIEWs tell you what to load. SYNC tells you where things stand. Documentation chains connect code to reasoning.**

Following it means your work compounds instead of getting lost.

---

## Before Any Task

**Understand the system:**
```
.context-protocol/PROTOCOL.md     # How to navigate — what to load, where to update
.context-protocol/PRINCIPLES.md   # How to work — the stance to hold
```

**Check project state:**
```
.context-protocol/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

---

## The Principles (Summary)

These are expanded in PRINCIPLES.md. Internalize them.

**Architecture: One Solution Per Problem**
Before creating, verify it doesn't exist. Fix broken systems, don't circumvent. Delete obsolete versions.

**Verification: Test Before Claiming Built**
If it's not tested, it's not built. Uncertainty is data. Only claim complete with proof.

**Communication: Depth Over Brevity**
Complex ideas need space. Make reasoning transparent. Explanation IS the work.

**Quality: Never Degrade**
Correctness > completeness > speed. If you can't meet the bar, stop and report why.

---

## Choose Your VIEW

VIEWs are ordered by the product development lifecycle. Pick the one that matches your current stage:

### Understanding & Planning

| Stage | VIEW |
|-------|------|
| Processing raw data (chats, PDFs, research) | `views/VIEW_Ingest_Process_Raw_Data_Sources.md` |
| Getting oriented in unfamiliar code | `views/VIEW_Onboard_Understand_Existing_Codebase.md` |
| Defining vision, audience, architecture | `views/VIEW_Specify_Design_Vision_And_Architecture.md` |

### Building

| Stage | VIEW |
|-------|------|
| Writing new code or modifying existing | `views/VIEW_Implement_Write_Or_Modify_Code.md` |
| Adding features to existing modules | `views/VIEW_Extend_Add_Features_To_Existing.md` |
| Working alongside human in real-time | `views/VIEW_Collaborate_Pair_Program_With_Human.md` |

### Verifying

| Stage | VIEW |
|-------|------|
| Writing tests, verifying correctness | `views/VIEW_Test_Write_Tests_And_Verify.md` |
| Investigating and fixing issues | `views/VIEW_Debug_Investigate_And_Fix_Issues.md` |
| Evaluating changes before merge | `views/VIEW_Review_Evaluate_Changes.md` |

### Maintaining

| Stage | VIEW |
|-------|------|
| Improving structure without changing behavior | `views/VIEW_Refactor_Improve_Code_Structure.md` |

**Read the VIEW for your stage.** It explains what context to load and why.

---

## After Any Change

Update state so the next agent (or your future self) knows what happened:
```
.context-protocol/state/SYNC_Project_State.md
```

If you changed a specific module, also update its SYNC:
```
docs/{area}/{module}/SYNC_*.md
```

**Remember:** If it's not in SYNC, it didn't happen. The next agent won't know.

---

## Documentation Structure

```
docs/
├── concepts/                    # Cross-cutting ideas
│   └── {concept}/
│       ├── CONCEPT_*.md         # What it means
│       └── TOUCHES_*.md         # Where it appears in code
│
└── {area}/
    ├── SYNC_{Area}_State.md     # Area status
    └── {module}/
        ├── PATTERNS_*.md        # Why this design
        ├── BEHAVIORS_*.md       # What it should do
        ├── ALGORITHM_*.md       # How it works
        ├── VALIDATION_*.md      # How to verify
        └── SYNC_*.md            # Current state
```

---

## Templates

When creating new documentation, use templates from:
```
.context-protocol/templates/
```

**Remember the architecture principle:** Before creating, check if it already exists.


# Context Protocol

@.context-protocol/PRINCIPLES.md

---

@.context-protocol/PROTOCOL.md

---

## Before Any Task

Check project state:
```
.context-protocol/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

## Choose Your VIEW

Based on your task, load ONE view from `.context-protocol/views/`:

| Task | VIEW |
|------|------|
| Processing raw data (chats, PDFs) | VIEW_Ingest_Process_Raw_Data_Sources.md |
| Getting oriented | VIEW_Onboard_Understand_Existing_Codebase.md |
| Defining architecture | VIEW_Specify_Design_Vision_And_Architecture.md |
| Writing/modifying code | VIEW_Implement_Write_Or_Modify_Code.md |
| Adding features | VIEW_Extend_Add_Features_To_Existing.md |
| Pair programming | VIEW_Collaborate_Pair_Program_With_Human.md |
| Writing tests | VIEW_Test_Write_Tests_And_Verify.md |
| Debugging | VIEW_Debug_Investigate_And_Fix_Issues.md |
| Reviewing changes | VIEW_Review_Evaluate_Changes.md |
| Refactoring | VIEW_Refactor_Improve_Code_Structure.md |

## After Any Change

Update `.context-protocol/state/SYNC_Project_State.md` with what you did.
If you changed a module, update its `docs/{area}/{module}/SYNC_*.md` too.
