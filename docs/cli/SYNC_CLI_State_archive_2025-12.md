# Archived: SYNC_CLI_State.md

Archived on: 2025-12-18
Original file: SYNC_CLI_State.md

---

## MATURITY

**What's canonical (v1):**
- `init` command — copies protocol files to target project
- `validate` command — checks protocol invariants
- `doctor` command — identifies health issues (monoliths, stale SYNCs, etc.)
- `repair` command — spawns Claude Code agents to fix issues
- `sync` command — manages SYNC files
- `context` command — navigates from code to docs
- `prompt` command — generates LLM bootstrap prompts
- `map` command — visual project mapping

**What's still being designed:**
- Parallel agent coordination in `repair` (works but output can be interleaved)
- GitHub issue integration depth (currently creates issues, could do more)
- Config.yaml structure for project-specific settings

**What's proposed (v2+):**
- Watch mode for continuous health monitoring
- MCP server integration for repairs
- IDE extension/plugin support

---


## RECENT CHANGES

### 2025-12-18: Fixed BROKEN_IMPL_LINK in IMPLEMENTATION Doc

- **What:** Fixed 22 broken file references in IMPLEMENTATION_CLI_Code_Architecture.md
- **Why:** BROKEN_IMPL_LINK issue — doctor detected non-existent file references
- **Root cause:** File references were extracted as bare filenames (e.g., `cli.py`) instead of full paths
- **Changes:**
  - Flattened CODE STRUCTURE tree to avoid nested `│ ├──` pattern extracting bare filenames
  - Updated File Responsibilities table to use module names without `.py` extension
  - Updated Code Patterns, Anti-Patterns, Boundaries tables to use module names
  - Updated External Dependencies table to use module names
  - Clarified GAPS section to mark proposed files as "(planned)"
- **Result:** All file references now resolve to existing files in `src/ngram/`

### 2025-12-18: Full Documentation Chain Complete

- **What:** Completed full documentation chain for CLI module
- **Why:** INCOMPLETE_CHAIN issue — module had only PATTERNS + SYNC, missing 5 doc types
- **Files created:**
  - `docs/cli/BEHAVIORS_CLI_Command_Effects.md` — observable command effects
  - `docs/cli/ALGORITHM_CLI_Logic.md` — command processing logic
  - `docs/cli/VALIDATION_CLI_Invariants.md` — invariants and checks
  - `docs/cli/IMPLEMENTATION_CLI_Code_Architecture.md` — code structure
  - `docs/cli/TEST_CLI_Coverage.md` — test coverage (currently 0%)
- **Files updated:**
  - `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` — updated CHAIN section
  - `docs/cli/SYNC_CLI_State.md` — added CHAIN section, updated status to CANONICAL
- **Insights:** CLI module is now fully documented. All 7 doc types in chain.

### 2025-12-18: Initial Documentation

- **What:** Created module documentation (PATTERNS + SYNC)
- **Why:** The `src/` directory had 12 files with no documentation mapping
- **Files:**
  - `modules.yaml` — added mapping
  - `docs/cli/PATTERNS_Why_CLI_Over_Copy.md` — design rationale
  - `docs/cli/SYNC_CLI_State.md` — current state (this file)
- **Insights:** The CLI is mature enough for stable documentation. Core patterns are clear.

### Previous: Parallel Agent Execution

- **What:** Added `--parallel` flag to repair command
- **Why:** Sequential repairs were slow; parallel speeds up batch fixes
- **Files:** `repair.py`

### Previous: GitHub Integration

- **What:** Doctor command can create GitHub issues for findings
- **Why:** Track issues in the repo's native issue tracker
- **Files:** `github.py`, `doctor.py`

---


## TODO

### Completed

- [x] Add modules.yaml mapping
- [x] Create PATTERNS doc
- [x] Create SYNC doc (this file)
- [x] Create IMPLEMENTATION doc detailing file structure and data flows
- [x] Create BEHAVIORS doc for command specifications
- [x] Create ALGORITHM doc for command logic
- [x] Create VALIDATION doc for invariants
- [x] Create TEST doc for coverage tracking

### Later

- [ ] Add automated tests (currently 0% coverage)
- [ ] Set up CI/CD test pipeline
- IDEA: Document the repair agent prompt templates in external files

---

