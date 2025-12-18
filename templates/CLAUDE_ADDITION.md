# ADD Framework

This project follows the ADD Framework — a system that ensures you load the right context for your task and leave useful state for the next agent.

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

**Check project state:**
```
.ngram/state/SYNC_Project_State.md
```

What's happening? What changed recently? Any handoffs for you?

(PROTOCOL.md and PRINCIPLES.md are already loaded in your system prompt above.)

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
| Documenting an existing module | `views/VIEW_Document_Create_Module_Documentation.md` |

**Read the VIEW for your stage.** It explains what context to load and why.

---

## After Any Change

Update state so the next agent (or your future self) knows what happened:
```
.ngram/state/SYNC_Project_State.md
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
        ├── IMPLEMENTATION_*.md  # Code architecture
        ├── TEST_*.md            # Test cases
        └── SYNC_*.md            # Current state
```

---

## Templates

When creating new documentation, use templates from:
```
.ngram/templates/
```

**Remember the architecture principle:** Before creating, check if it already exists.

---

## CLI Commands

The `ngram` command is available for project management:

```bash
ngram init [--force]    # Initialize/re-sync protocol files
ngram validate          # Check protocol invariants
ngram doctor            # Health checks (auto-archives large SYNCs)
ngram sync              # Show SYNC status (auto-archives large SYNCs)
ngram repair [--max N]  # Auto-fix issues using Claude Code agents
ngram context <file>    # Get doc context for a file
ngram prompt            # Generate bootstrap prompt for LLM
```

### Repair Command

The `repair` command automatically fixes project health issues:

```bash
ngram repair              # Fix all issues
ngram repair --max 5      # Limit to 5 issues
ngram repair --type MONOLITH --type STALE_SYNC  # Fix specific types
ngram repair --dry-run    # Preview what would be fixed
```

Each repair spawns a Claude Code agent that:
1. Reads the appropriate VIEW and documentation
2. Fixes the specific issue (output streamed to terminal)
3. Updates SYNC with what changed
