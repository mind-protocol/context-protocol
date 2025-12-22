# Ngram CLI Core — Behaviors: Observable Effects of CLI Commands

```
STATUS: DRAFT
CREATED: 2023-12-19
VERIFIED: N/A against N/A
```

---

## CHAIN

```
OBJECTIFS:      ./OBJECTIFS_ngram_cli_core.md
THIS:            BEHAVIORS_ngram_cli_core.md (you are here)
PATTERNS:        ./PATTERNS_ngram_cli_core.md
ALGORITHM:       ./ALGORITHM_ngram_cli_core.md
VALIDATION:      ./VALIDATION_ngram_cli_core.md
HEALTH:          ./HEALTH_ngram_cli_core.md
IMPLEMENTATION:  ./IMPLEMENTATION_ngram_cli_core.md
SYNC:            ./SYNC_ngram_cli_core.md

IMPL:            ngram/cli.py
```

> **Contract:** Read docs before modifying. After changes: update IMPL or add TODO to SYNC. Run tests.

---

## BEHAVIORS

### B1: Execute CLI Command

```
GIVEN:  A valid ngram CLI command (e.g., 'ngram doctor') and arguments.
WHEN:   The command is executed.
THEN:   The corresponding action is performed and output is displayed to the user.
AND:    Project state or files might be modified based on the command.
```

### B2: Display Help Information

```
GIVEN:  A user requests help for a command (e.g., 'ngram --help').
WHEN:   The help command is executed.
THEN:   Usage instructions and available commands/arguments are displayed.
```

### B3: Validate Project Health

```
GIVEN:  A 'ngram doctor' command is executed.
WHEN:   The project health check runs.
THEN:   A report on the project's adherence to documentation and code standards is generated.
```

---

## OBJECTIVES SERVED

| Behavior ID | Objective | Why It Matters |
|-------------|-----------|----------------|
| B1 | User Interaction | Enables users to control the ngram agent and project. |
| B2 | Usability | Provides clear guidance for using the CLI. |
| B3 | Project Integrity | Ensures the project follows defined protocols and standards. |

---

## INPUTS / OUTPUTS

### Primary Function: `ngram_cli_core` (various commands)

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `command` | `str` | The primary command to execute. |
| `args`    | `list` | Additional arguments and flags for the command. |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| `stdout` | `str` | Textual output from command execution. |
| `stderr` | `str` | Error messages or warnings. |
| `exit_code` | `int` | Standard process exit code (0 for success, non-zero for failure). |

**Side Effects:**

- Modification of project files (e.g., during `ngram repair`).
- Generation of reports or logs.
- Interaction with external tools (e.g., git, python interpreters).

---

## EDGE CASES

### E1: Invalid Command

```
GIVEN:  A non-existent or malformed CLI command is provided.
THEN:   An error message is displayed, and the program exits with a non-zero code.
```

### E2: Missing Arguments

```
GIVEN:  A command requiring arguments is called without them.
THEN:   An error message is displayed, typically with usage help, and the program exits with a non-zero code.
```

---

## ANTI-BEHAVIORS

What should NOT happen:

### A1: Silent Failure

```
GIVEN:   A critical operation fails (e.g., file write error).
WHEN:    The command is executed.
MUST NOT: The program exits silently or indicates success.
INSTEAD:  An informative error message is displayed, and the program exits with an appropriate error code.
```

---

## MARKERS

<!-- @ngram:todo
title: "Document specific command behaviors"
priority: medium
context: |
  The current behaviors are very high-level. More specific behaviors for each core command (doctor, repair, validate, etc.) should be detailed.
task: |
  Add Bx entries for key commands like 'doctor', 'repair', 'validate', ' 'context', 'prompt' with GIVEN/WHEN/THEN.
-->
