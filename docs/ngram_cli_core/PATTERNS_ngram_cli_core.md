# ngram_cli_core — PATTERNS: Design and Implementation Conventions

## CHAIN
- Docs: `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`
- Code: `ngram/cli.py`
- Code: `ngram/agent_cli.py`
- Code: `ngram/doctor.py`
- Code: `ngram/repair.py`
- Code: `ngram/validate.py`
- Code: `ngram/context.py`
- Code: `ngram/prompt.py`

## PATTERNS

This module adheres to the following design and implementation patterns:

### 1. Command-Line Interface (CLI) Structure

*   **Click Framework:** All CLI commands are built using the `Click` library for robust, composable command definitions, argument parsing, and help generation.
*   **Subcommands:** Complex functionalities are organized into subcommands (e.g., `ngram doctor`, `ngram repair`) for clarity and modularity.
*   **Option and Argument Typing:** Type hints are used for CLI options and arguments to improve readability and enable static analysis.

### 2. Modular Design

*   **Separation of Concerns:** Core logic for distinct functionalities (e.g., `doctor`, `repair`, `validate`, `context`, `prompt`) resides in separate Python modules within the `ngram/` directory.
*   **Helper Functions/Classes:** Common utilities and reusable logic are encapsulated in helper functions or classes (e.g., `core_utils.py`, `doctor_checks.py`) to avoid duplication.

### 3. Context Management

*   **Global Context Object:** A central context object (`ngram/context.py`) is used to store and pass shared state, configuration, and services across different CLI commands and operations.
*   **Dependency Injection:** Dependencies are often passed explicitly or retrieved from the global context rather than relying on global state where possible.

### 4. Doc-Code Alignment

*   **`DOCS:` References:** Source files include `DOCS:` comments pointing to their primary documentation files.
*   **`CHAIN` Sections:** Documentation files include `CHAIN` sections linking to related code and other documentation.

### 5. Error Handling

*   **Graceful Degradation:** Commands aim to fail gracefully, providing informative error messages and suggestions for recovery.
*   **Specific Exceptions:** Custom exceptions are used for domain-specific errors to allow for precise error handling.

### 6. Testability

*   **Unit and Integration Tests:** Code is designed to be easily testable, with a clear separation between logic and I/O.
*   **Mocking:** Dependencies are often mocked in tests to isolate the unit under test.

## ANTI-PATTERNS TO AVOID

*   **Tight Coupling:** Avoid direct, rigid dependencies between unrelated modules; favor loose coupling through interfaces or explicit dependency passing.
*   **Magic Strings/Numbers:** Use constants or enums instead of hardcoded string or numeric literals for configuration and identifiers.
*   **Excessive Global State:** Minimize reliance on global variables; prefer passing state explicitly or through well-defined context objects.
*   **Undocumented Features:** All public CLI commands and core functionalities must be documented.
