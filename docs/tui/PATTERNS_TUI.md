# PATTERNS: Text User Interface (TUI) Module

## Core Technologies

-   **Textual Framework:** The TUI is built extensively using the [Textual](https://textual.textualize.io/) framework for Python. All UI components (widgets, screens) adhere to Textual's API and conventions.

## Architectural Patterns

1.  **Component-Based UI:** The TUI is structured around a component-based architecture, where the interface is composed of modular and reusable `Textual.widgets.Widget` instances. Each widget is responsible for rendering a specific part of the UI and managing its internal state.

2.  **Centralized State Management:** The application's global state is managed centrally (e.g., within `state.py` or similar constructs) and updated through explicit actions or commands. Widgets react to changes in this central state, ensuring a single source of truth and predictable UI updates.

3.  **Command Pattern for Interactions:** User inputs (keystrokes, command line entries) are translated into discrete commands. These commands are processed by a command handler (e.g., `commands.py`, `commands_agent.py`), which then executes the corresponding logic, potentially modifying the application state or triggering external actions.

4.  **Event-Driven Communication:** Widgets and other TUI components communicate primarily through Textual's event system. Custom events are defined and emitted to notify other parts of the application about changes or user interactions, promoting loose coupling.

5.  **Reactive UI Updates:** The UI is designed to be reactive to state changes. When the application state is updated, relevant widgets automatically re-render or update their display to reflect the new state, minimizing manual UI refresh logic.

## Styling Conventions

-   **Textual CSS:** Styling for the TUI components is managed primarily through Textual's CSS-like syntax, defined in files within `ngram/tui/styles/`. Consistent class names and IDs should be used across widgets for unified theming.
-   **Minimalist Design:** The overall design aims for clarity and minimalism, prioritizing information density and readability within a terminal environment.

## File Structure

-   `ngram/tui/app.py`: Main application entry point and root screen.
-   `ngram/tui/app_core.py`: Core application logic and setup.
-   `ngram/tui/app_manager.py`: Manages the overall TUI application lifecycle.
-   `ngram/tui/commands.py`: Defines general TUI commands.
-   `ngram/tui/commands_agent.py`: Defines agent-specific commands.
-   `ngram/tui/manager.py`: TUI-specific manager components.
-   `ngram/tui/state.py`: Manages the application's global state.
-   `ngram/tui/styles/`: Contains Textual CSS files.
-   `ngram/tui/widgets/`: Directory for custom Textual widgets.

## CHAIN
- [PROTOCOL.md](../../PROTOCOL.md)
- [modules.yaml](../../modules.yaml)
- [OBJECTIFS_TUI.md](OBJECTIFS_TUI.md)
