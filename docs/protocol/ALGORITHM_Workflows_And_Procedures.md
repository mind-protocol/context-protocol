# ADD Framework — Algorithm: Workflows and Procedures

```
STATUS: STABLE
CREATED: 2024-12-15
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ./BEHAVIORS_Observable_Protocol_Effects.md
THIS:            ALGORITHM_Workflows_And_Procedures.md
VALIDATION:      ./VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ./IMPLEMENTATION_Protocol_Code_Architecture.md
TEST:            ./TEST_Protocol_Test_Cases.md
SYNC:            ./SYNC_Protocol_Current_State.md
```

---

## OVERVIEW

This document describes the step-by-step procedures for using the ADD Framework.
It covers installation, daily workflows, and maintenance.

---

## ALGORITHM: Install Protocol in Project

### Step 1: Copy Protocol Files

```
COPY: templates/ngram/ → {project}/.ngram/
```

Result:
```
{project}/
└── .ngram/
    ├── PROTOCOL.md
    ├── views/
    │   ├── VIEW_Implement.md
    │   ├── VIEW_Debug.md
    │   ├── VIEW_Review.md
    │   └── VIEW_Extend.md
    ├── templates/
    │   ├── PATTERNS_TEMPLATE.md
    │   ├── BEHAVIORS_TEMPLATE.md
    │   ├── ALGORITHM_TEMPLATE.md
    │   ├── VALIDATION_TEMPLATE.md
    │   ├── SYNC_TEMPLATE.md
    │   ├── CONCEPT_TEMPLATE.md
    │   └── TOUCHES_TEMPLATE.md
    └── state/
        └── SYNC_Project_State.md
```

### Step 2: Update CLAUDE.md

Append content from `templates/CLAUDE_ADDITION.md` to project's CLAUDE.md.

If CLAUDE.md doesn't exist, create it with the addition content.

### Step 3: Initialize Project SYNC

Edit `.ngram/state/SYNC_Project_State.md`:
- Fill in current project state
- Note what exists
- Note what's in progress

### Step 4: Create Initial Docs Structure (Optional)

```
CREATE: {project}/docs/
```

For existing modules, create docs using templates.

---

## ALGORITHM: Agent Starts Task

### Step 1: Read Bootstrap

```
READ: CLAUDE.md → find protocol section
READ: .ngram/PROTOCOL.md
```

### Step 2: Identify Task Type

```
IF task is implementing new code → VIEW_Implement.md
IF task is debugging → VIEW_Debug.md
IF task is reviewing → VIEW_Review.md
IF task is extending → VIEW_Extend.md
ELSE → Use closest VIEW or ask for clarification
```

### Step 3: Load View

```
READ: .ngram/views/VIEW_{TaskType}.md
FOLLOW: Instructions in the VIEW
```

### Step 4: Load Task-Specific Context

Follow the VIEW's instructions for what to load.
Typically:
```
READ: .ngram/state/SYNC_Project_State.md
READ: docs/{area}/{module}/PATTERNS_*.md (if working on specific module)
READ: docs/{area}/{module}/SYNC_*.md (if working on specific module)
```

### Step 5: Do the Work

Execute the task according to VIEW instructions.

### Step 6: Update State

```
UPDATE: .ngram/state/SYNC_Project_State.md
UPDATE: docs/{area}/{module}/SYNC_*.md (if module was changed)
UPDATE: Other docs as needed (if behavior/algorithm changed)
```

---

## ALGORITHM: Create New Module

### Step 1: Create Doc Folder

```
CREATE: docs/{area}/{module}/
```

### Step 2: Write PATTERNS First

```
COPY: .ngram/templates/PATTERNS_TEMPLATE.md
   → docs/{area}/{module}/PATTERNS_{Descriptive_Name}.md

FILL IN:
- The problem being solved
- The design pattern chosen
- Core principles
- Dependencies
```

### Step 3: Write SYNC

```
COPY: .ngram/templates/SYNC_TEMPLATE.md
   → docs/{area}/{module}/SYNC_{Module}_Current_State.md

FILL IN:
- Current state: "New module, not yet implemented"
- TODO: What needs to be built
```

### Step 4: Implement

Now write the code.

Reference docs in implementation header:
```python
"""
Module Name

DOCS: docs/{area}/{module}/
"""
```

### Step 5: Add Other Docs As Needed

After implementation, add:
- BEHAVIORS_*.md (if behaviors are non-trivial)
- ALGORITHM_*.md (if logic is complex)
- VALIDATION_*.md (if tests exist or invariants matter)

### Step 6: Update Project SYNC

```
UPDATE: .ngram/state/SYNC_Project_State.md
- Note new module created
- Note area affected
```

---

## ALGORITHM: Modify Existing Module

### Step 1: Load Module Docs

```
READ: docs/{area}/{module}/PATTERNS_*.md
READ: docs/{area}/{module}/SYNC_*.md
```

Understand:
- Why the module is shaped this way
- What the current state is
- Any known issues or constraints

### Step 2: Check If Change Fits Design

```
IF change fits PATTERNS → proceed
IF change conflicts with PATTERNS → either:
    - Adjust change to fit
    - Update PATTERNS with justification
```

### Step 3: Make Changes

Implement the modification.

### Step 4: Update Docs

```
IF behavior changed → UPDATE: BEHAVIORS_*.md
IF algorithm changed → UPDATE: ALGORITHM_*.md
IF new invariants → UPDATE: VALIDATION_*.md
ALWAYS → UPDATE: SYNC_*.md
```

### Step 5: Update Project SYNC

```
UPDATE: .ngram/state/SYNC_Project_State.md
- Note what was changed
- Note why
```

---

## ALGORITHM: Document Cross-Cutting Concept

### Step 1: Create Concept Folder

```
CREATE: docs/concepts/{concept}/
```

### Step 2: Write CONCEPT

```
COPY: .ngram/templates/CONCEPT_TEMPLATE.md
   → docs/concepts/{concept}/CONCEPT_{What_It_Is}.md

FILL IN:
- What the concept means
- Why it exists
- Key properties
- Relationships to other concepts
```

### Step 3: Write TOUCHES

```
COPY: .ngram/templates/TOUCHES_TEMPLATE.md
   → docs/concepts/{concept}/TOUCHES_{Where_It_Appears}.md

FILL IN:
- Which modules implement this concept
- What interfaces they provide
- How the concept flows between modules
```

### Step 4: Update Module Docs

In each module that uses this concept:
```
ADD reference to: docs/concepts/{concept}/CONCEPT_*.md
```

---

## DATA FLOW

```
Task Assigned
      ↓
CLAUDE.md (bootstrap)
      ↓
PROTOCOL.md (rules)
      ↓
VIEW_{Type}.md (specific instructions)
      ↓
Module Docs (PATTERNS, SYNC, etc.)
      ↓
Implementation Work
      ↓
Update SYNC files
      ↓
Update Docs (if needed)
      ↓
Task Complete
```

---

## COMPLEXITY

**Time to install:** O(1) — copy files, update CLAUDE.md
**Time to start task:** O(1) — read VIEW, load specified docs
**Time to maintain:** O(changes) — update SYNC proportional to changes

**Bottleneck:** Creating initial docs for undocumented codebase.
Solution: Do it incrementally. Document as you touch modules.

---

## GAPS / IDEAS / QUESTIONS

- [ ] Script to automate installation
- [ ] Script to scaffold new module with docs
- [ ] Procedure for handling very large existing codebases
- IDEA: VIEW for "understand unfamiliar codebase"
- QUESTION: How to handle documentation debt?
