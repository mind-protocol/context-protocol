# Ngram CLI Core — Algorithm: Command Parsing and Execution Logic

```
STATUS: DRAFT
CREATED: 2023-12-19
VERIFIED: N/A against N/A
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_ngram_cli_core.md
BEHAVIORS:       ./BEHAVIORS_ngram_cli_core.md
PATTERNS:        ./PATTERNS_ngram_cli_core.md
THIS:            ALGORITHM_ngram_cli_core.md (you are here)
VALIDATION:      ./VALIDATION_ngram_cli_core.md
HEALTH:          ./HEALTH_ngram_cli_core.md
IMPLEMENTATION:  ./IMPLEMENTATION_ngram_cli_core.md
SYNC:            ./SYNC_ngram_cli_core.md

IMPL:            ngram/cli.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## OVERVIEW

This algorithm describes the high-level process by which the `ngram` CLI receives a command, parses it, determines the appropriate action, and executes it. It primarily involves argument parsing, command dispatching, and error handling.

---

## OBJECTIVES AND BEHAVIORS

| Objective | Behaviors Supported | Why This Algorithm Matters |
|-----------|---------------------|----------------------------|
| User Interaction | B1, B2 | Ensures user commands are correctly interpreted and executed. |
| Project Integrity | B3 | Facilitates the execution of validation and repair mechanisms. |

---

## DATA STRUCTURES

### `CommandArgs`

```
Represents the parsed command-line arguments.
Fields: command (str), sub_command (str, optional), flags (dict), positional_args (list)
```

---

## ALGORITHM: `execute_cli_command`

### Step 1: Parse Command-Line Arguments

Parses `sys.argv` into a structured `CommandArgs` object, identifying the main command, sub-command, flags, and positional arguments.

```pseudocode
args = parse_arguments(sys.argv)
```

### Step 2: Dispatch Command

Based on the `command` and `sub_command` in `CommandArgs`, identify the target function or module responsible for handling the command.

### Step 3: Execute Command Handler

Invoke the identified command handler function with the relevant arguments. This handler performs the core logic of the command (e.g., running `doctor`, `repair`).

### Step 4: Handle Execution Result

Process the return value or exceptions from the command handler to determine success/failure and format appropriate output.

---

## KEY DECISIONS

### D1: Command Mapping

```
IF command IS 'doctor':
    Call ngram.doctor.run_doctor()
ELSE IF command IS 'repair':
    Call ngram.repair.run_repair()
ELSE:
    Display error and exit
```

---

## DATA FLOW

```
sys.argv (raw CLI input)
    ↓
parse_arguments() (produces CommandArgs)
    ↓
dispatch_command() (selects handler)
    ↓
command_handler() (executes logic)
    ↓
stdout/stderr/exit_code (CLI output)
```

---

## COMPLEXITY

**Time:** O(N) for argument parsing (where N is number of args), O(1) for dispatch (lookup).

**Space:** O(N) for storing parsed arguments.

**Bottlenecks:**
- Complex argument structures could lead to more involved parsing logic.
- Long-running command handlers will dominate execution time.

---

## HELPER FUNCTIONS

### `parse_arguments()`

**Purpose:** Converts raw command-line arguments into a structured format.

**Logic:** Uses an argument parsing library (e.g., `argparse`) to define and parse expected CLI arguments and flags.

### `dispatch_command()`

**Purpose:** Maps a parsed command to its executable function.

**Logic:** Uses a dictionary or switch-like structure to look up the correct handler based on the command and sub-command names.

---

## INTERACTIONS

| Module | What We Call | What We Get |
|--------|--------------|-------------|
| `ngram.doctor` | `run_doctor()` | `health_report` |
| `ngram.repair` | `run_repair()` | `repair_status` |
| `ngram.validate` | `run_validate()` | `validation_results` |

---

## MARKERS

<!-- @ngram:todo
title: "Detail argument parsing library and configuration"
priority: low
context: |
  The current description is generic. It would be beneficial to specify which library is used for argument parsing and how it's configured.
task: |
  Add details about `argparse` or similar library, including key configurations like subcommands and argument definitions.
-->

<!-- @ngram:todo
title: "Expand on specific command handler algorithms"
priority: medium
context: |
  The algorithm focuses on the dispatcher. Each command (doctor, repair, etc.) has its own specific algorithm that could be documented.
task: |
  Add sub-sections or links to more detailed algorithms for each major CLI command within this module.
-->
