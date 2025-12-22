# OBJECTIFS: Text User Interface (TUI) Module

## Objective

The primary objective of the `ngram/tui` module is to provide a robust, interactive, and user-friendly Text User Interface (TUI) for the Ngram project. It enables agents and human users to:

1.  **Interact with the Ngram system:** Execute commands, provide input, and receive feedback directly within a terminal environment.
2.  **Monitor project state:** Display real-time information about the project's progress, agent activities, and codebase status.
3.  **Visualize agent operations:** Offer a clear visual representation of ongoing tasks, system outputs, and critical events.
4.  **Enhance developer experience:** Provide an efficient and accessible interface for debugging, testing, and managing the Ngram project without relying solely on web-based or traditional CLI tools.

## Scope

This module encompasses:
-   The main TUI application (`app.py`, `app_core.py`, `app_manager.py`).
-   Command processing and execution (`commands.py`, `commands_agent.py`).
-   Application state management (`state.py`).
-   Custom TUI widgets (`widgets/`).
-   Styling definitions (`styles/`).

## Non-Objectives

-   Replacing the web-based UI for complex data visualizations or rich media interactions.
-   Providing a full-fledged IDE experience within the terminal.

## CHAIN
- [PROTOCOL.md](../../PROTOCOL.md)
- [modules.yaml](../../modules.yaml)
