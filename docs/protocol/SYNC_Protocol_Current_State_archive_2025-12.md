# Archived: SYNC_Protocol_Current_State.md

Archived on: 2025-12-18
Original file: SYNC_Protocol_Current_State.md

---

## RECENT CHANGES

### 2024-12-16: Added 5th principle "Experience: User Before Infrastructure"

**What:**
- Added new principle to PRINCIPLES.md
- Validates experience before building infrastructure
- "Fake it to learn it" — mock backends, LLM-simulated behavior
- Updated "How These Principles Integrate" section

**Why:**
Emerged from Blood Ledger planning. Building UI-first with LLM faking backend is better than architecting engine first. Usage reveals requirements imagination cannot.

### 2024-12-16: Added VIEW_Document_Create_Module_Documentation

**What:**
- New VIEW for documenting existing modules
- Guides through: understand → name descriptively → write with purpose → link chain
- Replaces the idea of a scaffolding command (which would create empty templates)

**Why:**
`ngram new-module` would create bad docs (generic names, empty content). A VIEW guides the thinking process instead.

### 2024-12-16: Added maturity tracking and documentation process

**What:**
- SYNC template now includes STATUS (CANONICAL, DESIGNING, PROPOSED, DEPRECATED)
- Added MATURITY section to SYNC template
- PROTOCOL.md new section: "THE DOCUMENTATION PROCESS"
  - When to create docs (decision/discovery trigger)
  - Top-down and bottom-up flows
  - Maturity tracking
  - The pruning cycle

**Why:**
Need to prevent scope creep and know what's stable vs experimental. Also clarified that docs can emerge bottom-up from code, not just top-down from design.

### 2024-12-16: Enhanced validate output with fix prompts

**What:**
- Validate now outputs detailed fix guidance when issues found
- For each issue: What's wrong, Why it matters, How to fix, References
- Designed to be fed to an LLM to guide fixing

### 2024-12-16: Added `ngram context` command

**What:**
- Added `context` command to get full documentation context for a file
- Follows DOCS: references in file headers
- Returns entire doc chain (PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, SYNC)

**Usage:**
```bash
ngram context src/module/file.py --dir /path/to/project
# Returns all linked docs for that file's module
```

### 2024-12-16: Added `ngram prompt` command

**What:**
- Added `prompt` command to generate bootstrap prompt for LLMs
- Guides LLM through: check state → choose mode → select VIEW → execute
- Includes autonomous vs collaborative mode choice
- `init` now hints about `prompt` command

**Usage:**
```bash
ngram prompt --dir /path/to/project
# Copy output to LLM to bootstrap it into using the protocol
```

### 2024-12-16: Added `ngram validate` command

**What:**
- Added validate command to CLI
- Implements checks: V2 (module docs minimum), V3 (CHAIN links), V6 (SYNC exists), V7 (VIEWs exist), NC (naming conventions)
- Reports gaps with actionable guidance

**Usage:**
```bash
ngram validate --dir /path/to/project
ngram validate --verbose  # show all details
```

### 2024-12-16: Added VIEW_Ingest

**What:**
- Created VIEW_Ingest_Process_Raw_Data_Sources.md
- Updated PROTOCOL.md and CLAUDE_ADDITION.md to include it

**Why:**
Projects start from raw data — chat logs, PDFs, research, specs dumped in `data/`. This VIEW handles processing that material into usable project context before implementation begins.

**The workflow:**
1. Survey: Scan and inventory `data/`
2. Extract: Pull decisions, constraints, requirements, concepts
3. Integrate: Transform into PATTERNS, BEHAVIORS, etc.
4. Triage: Note what wasn't processed and why

### 2024-12-15: Added PRINCIPLES.md

**What:**
- Created PRINCIPLES.md with four core stances
- Updated PROTOCOL.md to reference PRINCIPLES.md
- Updated CLAUDE_ADDITION.md with principles summary

**Why:**
Nicolas shared foundational working principles (architecture, verification, communication, quality). These aren't about WHAT to load — they're about HOW to work. Different layer, separate file.

**The four principles:**
1. Architecture: One solution per problem — verify before creating, fix don't circumvent
2. Verification: Test before claiming built — if not tested, not built
3. Communication: Depth over brevity — reasoning IS the work
4. Quality: Never degrade — stop and report rather than ship bad work

### 2024-12-15: V1 Package Implementation

**What:**
- Created `src/ngram/` package
- CLI with `init` command
- pyproject.toml for pip installation

### 2024-12-15: VIEW Restructuring

**What:**
- 9 VIEWs with descriptive names
- Ordered by development lifecycle
- New views: Onboard, Test, Refactor

---


## TODO

### Immediate

- [x] Test: `pip install -e .` and run init
- [x] Verify PRINCIPLES.md is copied correctly
- [x] Test on Blood Ledger or other real project
- [x] `ngram validate` command

### Later

- [ ] MCP tools for protocol navigation
- [ ] Publish to PyPI

### Ideas

- [ ] **Drift detection** — Warn when code changes but docs don't
  - Compare file timestamps: if code newer than linked docs, warn
  - Could use file watcher or validate-time check
  - No git required — just file modification times
  - Output: "src/engine/graph.py modified 10:30, docs last updated 09:00"
  - Optionally inject warnings into SYNC files when read

---

