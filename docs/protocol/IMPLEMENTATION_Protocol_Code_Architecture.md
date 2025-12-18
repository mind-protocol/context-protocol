# ADD Framework — Implementation: File Structure and Architecture

```
STATUS: STABLE
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ./BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ./ALGORITHM_Workflows_And_Procedures.md
VALIDATION:      ./VALIDATION_Protocol_Invariants.md
THIS:            IMPLEMENTATION_Protocol_Code_Architecture.md (you are here)
TEST:            ./TEST_Protocol_Test_Cases.md
SYNC:            ./SYNC_Protocol_Current_State.md
```

---

## OVERVIEW

The ADD Framework is implemented as a system of markdown files that guide AI agents. Unlike traditional code modules, the "implementation" here is the structure and content of template files that get copied to projects.

This document describes:
- Where protocol files live
- What each file does
- How agents traverse the system
- How the CLI installs and validates the protocol

---

## FILE STRUCTURE

### Template Directory (Source of Truth)

The source templates live in `templates/add-framework/`:

```
templates/add-framework/
├── PROTOCOL                       # Navigation rules for agents
├── PRINCIPLES                     # Working stance (how to think)
├── views/                         # Task-specific context instructions (11 VIEWs)
├── templates/                     # Doc templates for new modules (9 templates)
└── state/                         # State file templates
```

**Key files:**

| Category | Files |
|----------|-------|
| Core | `templates/add-framework/PROTOCOL.md`, `templates/add-framework/PRINCIPLES.md` |
| VIEWs | `templates/add-framework/views/VIEW_Implement_Write_Or_Modify_Code.md`, `templates/add-framework/views/VIEW_Debug_Investigate_And_Fix_Issues.md`, `templates/add-framework/views/VIEW_Review_Evaluate_Changes.md`, `templates/add-framework/views/VIEW_Extend_Add_Features_To_Existing.md`, `templates/add-framework/views/VIEW_Refactor_Improve_Code_Structure.md`, `templates/add-framework/views/VIEW_Test_Write_Tests_And_Verify.md`, `templates/add-framework/views/VIEW_Document_Create_Module_Documentation.md`, `templates/add-framework/views/VIEW_Onboard_Understand_Existing_Codebase.md`, `templates/add-framework/views/VIEW_Ingest_Process_Raw_Data_Sources.md`, `templates/add-framework/views/VIEW_Specify_Design_Vision_And_Architecture.md`, `templates/add-framework/views/VIEW_Collaborate_Pair_Program_With_Human.md` |
| Templates | `templates/add-framework/templates/PATTERNS_TEMPLATE.md`, `templates/add-framework/templates/BEHAVIORS_TEMPLATE.md`, `templates/add-framework/templates/ALGORITHM_TEMPLATE.md`, `templates/add-framework/templates/VALIDATION_TEMPLATE.md`, `templates/add-framework/templates/IMPLEMENTATION_TEMPLATE.md`, `templates/add-framework/templates/TEST_TEMPLATE.md`, `templates/add-framework/templates/SYNC_TEMPLATE.md`, `templates/add-framework/templates/CONCEPT_TEMPLATE.md`, `templates/add-framework/templates/TOUCHES_TEMPLATE.md` |
| State | `templates/add-framework/state/SYNC_Project_State.md` |

### Installed Directory (In Target Project)

When installed in a target project, files are copied to `.add-framework/`:

```
.add-framework/
├── PROTOCOL                       # Copied from templates
├── PRINCIPLES                     # Copied from templates
├── views/                         # Copied from templates
├── templates/                     # Copied from templates
├── modules.yaml                   # Project-specific module mapping
├── state/
│   ├── SYNC_Project_State         # Active project state
│   └── SYNC_Project_Health        # Doctor output (generated)
└── traces/                        # Agent activity logs (optional)
```

**Installed files in this project** (all under the hidden `.add-framework/` directory):

| Category | Location |
|----------|----------|
| Core | PROTOCOL, PRINCIPLES (at root) |
| State | state/SYNC_Project_State, state/SYNC_Project_Health |
| Mapping | modules.yaml |

### CLAUDE.md Bootstrap

The `CLAUDE.md` file includes protocol files via `@` directives:

```
CLAUDE.md
├── @templates/CLAUDE_ADDITION     # Include directive
├── @templates/add-framework/PRINCIPLES
└── @templates/add-framework/PROTOCOL
```

---

## FILE RESPONSIBILITIES

| File Pattern | Purpose | When Loaded |
|--------------|---------|-------------|
| PROTOCOL | Navigation — what to load, where to update | Every session start |
| PRINCIPLES | Stance — how to work (5 principles) | Every session start |
| VIEW_* (11 files) | Task instructions for specific work type | Based on task type |
| *_TEMPLATE (9 files) | Scaffolds for new documentation | When creating docs |
| SYNC_Project_State | Current project status and handoffs | Every session start |
| SYNC_Project_Health | Doctor output with health score | After `doctor` command |
| modules.yaml | Code → docs mapping | By CLI tools |

---

## SCHEMA

### modules.yaml

```yaml
modules:
  required:
    - {module_name}:
        code: str           # Glob pattern for source files
        docs: str           # Path to documentation directory
  optional:
    - maturity: enum        # DESIGNING | CANONICAL | PROPOSED | DEPRECATED
    - owner: str            # agent | human | team-name
    - entry_points: list    # Main files to start reading
    - internal: list        # Implementation details, not public API
    - depends_on: list      # Other modules this requires
    - patterns: list        # Design patterns used
    - notes: str            # Quick context
```

### SYNC File Structure

```yaml
SYNC:
  required:
    - LAST_UPDATED: date
    - STATUS: enum          # CANONICAL | DESIGNING | PROPOSED | DEPRECATED
  sections:
    - MATURITY:             # What's stable vs in progress
    - CURRENT STATE:        # What exists now
    - HANDOFF: FOR AGENTS:  # What next agent needs to know
    - HANDOFF: FOR HUMAN:   # Summary for human review
  optional:
    - CONSCIOUSNESS TRACE:  # Agent's mental state/insights
    - STRUCTURE:            # Directory layout
    - POINTERS:             # Quick reference links
```

### VIEW File Structure

```yaml
VIEW:
  required:
    - WHY THIS VIEW EXISTS: # Purpose of this view
    - CONTEXT TO LOAD:      # Specific files to read
    - THE WORK:             # What to do
    - AFTER:                # State updates required
  optional:
    - VERIFICATION:         # How to check work is complete
```

---

## ENTRY POINTS

| Entry Point | File | Triggered By |
|-------------|------|--------------|
| Bootstrap | CLAUDE.md | Agent session start |
| Navigation | .add-framework/PROTOCOL.md | After bootstrap |
| Task Selection | .add-framework/views/VIEW_*.md | Based on task type |
| State Check | .add-framework/state/SYNC_Project_State.md | Before any work |
| Module Context | docs/{area}/{module}/PATTERNS_*.md | When modifying code |

---

## DATA FLOW

### Agent Session Flow

```
┌─────────────────┐
│  Agent Starts   │
│   Session       │
└────────┬────────┘
         │ reads
         ▼
┌─────────────────┐
│   CLAUDE.md     │ ← Bootstrap with @includes
│  (with @refs)   │
└────────┬────────┘
         │ follows to
         ▼
┌─────────────────┐
│   PROTOCOL.md   │ ← Navigation rules
│  + PRINCIPLES   │   + Working stance
└────────┬────────┘
         │ directs to
         ▼
┌─────────────────┐
│  SYNC_Project_  │ ← Current state
│  State.md       │
└────────┬────────┘
         │ identifies
         ▼
┌─────────────────┐
│  VIEW_{Task}.md │ ← Task-specific instructions
└────────┬────────┘
         │ specifies
         ▼
┌─────────────────┐
│  Module Docs    │ ← PATTERNS, SYNC, etc.
│  (as needed)    │
└────────┬────────┘
         │ enables
         ▼
┌─────────────────┐
│  Implementation │
│     Work        │
└────────┬────────┘
         │ requires
         ▼
┌─────────────────┐
│  Update SYNC    │ ← State for next session
│     Files       │
└─────────────────┘
```

### Documentation Chain Flow

```
PATTERNS_*.md (WHY this design)
         │
         ▼
BEHAVIORS_*.md (WHAT it should do)
         │
         ▼
ALGORITHM_*.md (HOW it works)
         │
         ▼
VALIDATION_*.md (WHAT must be true)
         │
         ▼
IMPLEMENTATION_*.md (WHERE code lives)
         │
         ▼
TEST_*.md (WHAT's tested)
         │
         ▼
SYNC_*.md (WHERE we are now)
```

### CLI Installation Flow

```
┌─────────────────┐
│  context-proto- │
│  col init       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Find templates/ │ ← From package or repo
│ directory       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Copy to target  │ ← .add-framework/
│ .context-proto- │
│ col/            │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Create/update   │ ← Add @includes
│ CLAUDE.md       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Initialize      │ ← Empty modules.yaml
│ modules.yaml    │
└─────────────────┘
```

---

## LOGIC CHAINS

### LC1: Context Discovery

**Purpose:** Find documentation for a given source file

```
source_file
  → find DOCS: comment in file header
    → follow path to docs/{area}/{module}/
      → read PATTERNS_*.md for design context
        → read SYNC_*.md for current state
          → agent has full context
```

### LC2: State Propagation

**Purpose:** Ensure work is preserved across sessions

```
agent completes work
  → updates module SYNC_*.md
    → updates SYNC_Project_State.md
      → next agent reads SYNC files
        → understands current state
          → can continue without rediscovery
```

### LC3: VIEW Resolution

**Purpose:** Route agent to correct instructions

```
task description
  → agent reads PROTOCOL.md VIEW table
    → matches task to VIEW type
      → loads VIEW_{type}.md
        → follows VIEW instructions
          → loads only relevant context
```

---

## MODULE DEPENDENCIES

### Internal Dependencies (Protocol Files)

```
CLAUDE.md
    └── includes → PROTOCOL.md
    └── includes → PRINCIPLES.md

PROTOCOL.md
    └── references → views/VIEW_*.md
    └── references → templates/*_TEMPLATE.md

VIEW_*.md
    └── references → state/SYNC_Project_State.md
    └── references → docs/{area}/{module}/*.md

modules.yaml
    └── maps → code paths
    └── maps → docs paths
```

### External Dependencies (CLI)

The protocol files themselves have no external dependencies. The CLI that manages them uses:

| Package | Used For | Part Of |
|---------|----------|---------|
| pathlib | File path handling | CLI (init, validate) |
| shutil | File copying | CLI (init) |
| yaml | modules.yaml parsing | CLI (validate, doctor) |
| re | Pattern matching | CLI (validate) |

---

## STATE MANAGEMENT

### Where State Lives

| State | Location | Scope | Updated When |
|-------|----------|-------|--------------|
| Project state | .add-framework/state/SYNC_Project_State.md | Global | After any change |
| Module state | docs/{area}/{module}/SYNC_*.md | Module | After module change |
| Health state | .add-framework/state/SYNC_Project_Health.md | Global | After `doctor` run |
| Agent traces | .add-framework/traces/{date}.jsonl | Global | During agent execution |
| Module mapping | .add-framework/modules.yaml | Global | When modules added/changed |

### State Lifecycle

```
Project Created → init → Protocol Installed → work → State Updated → session end
                                                          ↓
                                         next session → State Read → work continues
```

---

## BIDIRECTIONAL LINKS

### Code → Docs

Source files reference documentation via header comment:

```python
# DOCS: docs/backend/auth/PATTERNS_Why_JWT_With_Refresh_Tokens.md
```

This enables `add-framework context {file}` to find the documentation chain.

### Docs → Code

Documentation references implementation:

| Doc Section | Points To |
|-------------|-----------|
| PATTERNS: Dependencies | Module imports |
| IMPLEMENTATION: Code Structure | File paths |
| VALIDATION: Invariants | Test files |
| SYNC: Pointers | Key file locations |

### CHAIN Sections

Every doc file includes a CHAIN block linking to siblings. Each entry maps a doc type to its relative file path (format: `TYPE: ./TYPE_Descriptive_Name`).

The doc types are: PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST, and SYNC. The current file is marked with `THIS:` instead of its type.

---

## CONFIGURATION

| Config | Location | Default | Description |
|--------|----------|---------|-------------|
| Ignore patterns | .add-framework/config.yaml | Common patterns | Paths to skip in doctor |
| Monolith threshold | .add-framework/config.yaml | 500 lines | SYNC archive trigger |
| Stale days | .add-framework/config.yaml | 14 days | When SYNC is stale |
| Disabled checks | .add-framework/config.yaml | [] | Doctor checks to skip |

---

## GAPS / IDEAS / QUESTIONS

- [ ] Consider adding VERSION file for protocol version tracking
- [ ] Document how to customize VIEW files for project-specific needs
- IDEA: Protocol migration tool for breaking changes
- IDEA: VIEW composition (inherit from base VIEW)
- QUESTION: Should trace files have retention policy?
