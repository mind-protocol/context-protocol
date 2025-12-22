# ngram_cli_core — SYNC: Project State and Recent Changes

## CHAIN
- Docs: `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`
- Docs: `docs/ngram_cli_core/PATTERNS_ngram_cli_core.md`
- Code: `ngram/cli.py`
- Code: `ngram/agent_cli.py`
- Code: `ngram/doctor.py`
- Code: `ngram/repair.py`
- Code: `ngram/validate.py`
- Code: `ngram/context.py`
- Code: `ngram/prompt.py`

## SYNC

This document tracks the current state and recent modifications within the `ngram_cli_core` module.

### Current Status

The `ngram_cli_core` module is the backbone of the `ngram` framework, providing all essential CLI functionalities. It is considered `CANONICAL` in its maturity, reflecting its central and stable role in the project. The module is actively maintained and evolved by the `agent`.

### Recent Changes

*   **2023-11-20: Initial Documentation:** This module's documentation was created to align `ngram/` core files with the `modules.yaml` mapping. Initial `OBJECTIFS`, `PATTERNS`, and `SYNC` documents were generated to describe the module's purpose, design principles, and current state. This addresses an `UNDOCUMENTED` issue.
    *   **Files Modified:** `modules.yaml`, `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md`, `docs/ngram_cli_core/PATTERNS_ngram_cli_core.md`, `docs/ngram_cli_core/SYNC_ngram_cli_core.md`, `...ngram/state/SYNC_Project_State.md`
    *   **Reasoning:** To formally document the core `ngram` CLI components, establish clear objectives, define design patterns, and ensure doc-code alignment as per the project protocol.

### Pending Work / Known Issues

*   **Granular Module Split:** Some sub-components within `ngram/` (e.g., `doctor_checks_*.py`, `repair_instructions_*.py`) could potentially be split into more granular modules in `modules.yaml` for finer-grained documentation and ownership tracking. This is a future enhancement to be considered.
*   **Missing `DOCS:` References:** Many individual files within `ngram/` currently lack explicit `DOCS:` references. These should be added to point to `docs/ngram_cli_core/OBJECTIFS_ngram_cli_core.md` or more specific future documentation.
