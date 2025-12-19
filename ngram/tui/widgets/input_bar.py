# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""Input bar widget for user commands."""

from textual.widgets import TextArea
from textual.message import Message

# Command definitions with descriptions
COMMANDS = {
    "/help": "Show available commands",
    "/doctor": "Run project health check",
    "/repair": "Auto-fix project issues",
    "/issues": "Show current project issues",
    "/clear": "Clear chat history",
    "/logs": "Show agent logs",
    "/run": "Run a shell command",
    "/quit": "Exit the TUI",
}


class InputBar(TextArea):
    """
    Bottom input bar for slash commands and messages.

    Behavior:
    - Lines starting with / are commands
    - Other input is treated as chat
    - Enter submits, Shift+Enter for newline
    - Up/Down arrows navigate command history (preserves current draft)
    - Tab completes slash commands
    - Dynamically scales height for multiline input (max 10 lines)
    """

    DEFAULT_CSS = """
    InputBar {
        height: auto;
        min-height: 3;
        max-height: 12;
        width: 100%;
        padding: 0 1;
    }
    """

    class CommandSubmitted(Message):
        """Message emitted when a command is submitted."""

        def __init__(self, command: str) -> None:
            self.command = command
            super().__init__()

    class InputChanged(Message):
        """Message emitted when input text changes (for auto-scroll)."""
        pass

    class ShowSuggestions(Message):
        """Message emitted to show/hide command suggestions."""

        def __init__(self, suggestions: list[tuple[str, str]]) -> None:
            # List of (command, description) tuples, empty to hide
            self.suggestions = suggestions
            super().__init__()

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._history: list[str] = []
        self._history_index = -1
        self._current_draft = ""  # Preserve current input when navigating history
        # Tab completion state
        self._tab_candidates: list[str] = []
        self._tab_index = -1
        self._tab_original_value = ""

    def on_mount(self) -> None:
        """Set focus on mount."""
        self.focus()
        # Set placeholder text
        self.text = ""
        self._update_height()

    def _update_height(self) -> None:
        """Adjust height based on line count."""
        line_count = self.text.count('\n') + 1
        # Each line needs ~1 row, plus 2 for padding/border
        new_height = min(max(line_count + 2, 3), 12)
        self.styles.height = new_height

    def on_text_area_changed(self, event: TextArea.Changed) -> None:
        """Called when text changes - adjust height and notify for auto-scroll."""
        self._update_height()
        # Notify app to scroll chat to bottom when user starts typing
        self.post_message(self.InputChanged())

        # Show command suggestions when typing /
        current = self.text.strip()
        if current.startswith("/") and "\n" not in current:
            # Filter matching commands
            matches = [
                (cmd, desc) for cmd, desc in COMMANDS.items()
                if cmd.startswith(current)
            ]
            self.post_message(self.ShowSuggestions(matches))
        else:
            # Hide suggestions
            self.post_message(self.ShowSuggestions([]))

    @property
    def value(self) -> str:
        """Get the current text value."""
        return self.text

    @value.setter
    def value(self, new_value: str) -> None:
        """Set the text value."""
        self.text = new_value

    def _submit(self) -> None:
        """Submit the current input."""
        value = self.text.strip()
        if not value:
            return

        # Expand partial slash commands (e.g., /re -> /repair)
        if value.startswith("/") and " " not in value:
            # Find matching commands
            matches = [cmd for cmd in COMMANDS.keys() if cmd.startswith(value)]
            if len(matches) == 1:
                # Unique match - expand to full command
                value = matches[0]
            elif value in COMMANDS:
                # Exact match - use as is
                pass
            # If multiple matches or no match, let it through as-is

        # Add to history
        self._history.append(value)
        self._history_index = len(self._history)

        # Clear input and draft
        self.text = ""
        self._current_draft = ""

        # Hide suggestions
        self.post_message(self.ShowSuggestions([]))

        # Emit command (both / commands and regular messages)
        self.post_message(self.CommandSubmitted(value))

    def on_key(self, event) -> None:
        """Handle key events for submit, history navigation and tab completion."""
        # Enter submits, shift+enter adds newline
        if event.key == "enter":
            event.prevent_default()
            event.stop()
            self._submit()
            return
        # Allow shift+enter to pass through for newline
        if event.key == "shift+enter":
            return

        # Tab completion for slash commands
        if event.key == "tab":
            current_value = self.text

            # Only complete if input starts with /
            if not current_value.startswith("/"):
                return

            # First Tab press - build candidate list
            if current_value != self._tab_original_value:
                self._tab_original_value = current_value
                self._tab_candidates = [cmd for cmd in COMMANDS.keys() if cmd.startswith(current_value)]
                self._tab_index = -1

            # If we have candidates, cycle through them
            if self._tab_candidates:
                self._tab_index = (self._tab_index + 1) % len(self._tab_candidates)
                self.text = self._tab_candidates[self._tab_index]
                # Prevent default tab behavior
                event.prevent_default()
                event.stop()

            return

        # Reset tab completion on any other key
        self._tab_candidates = []
        self._tab_index = -1
        self._tab_original_value = ""

        # History navigation only when on single line or at start
        if event.key == "up" and self._history:
            # Only navigate history if cursor is on first line
            if self.text.count('\n') == 0 or self.cursor_location[0] == 0:
                # Save current draft when entering history for the first time
                if self._history_index == len(self._history):
                    self._current_draft = self.text

                # Navigate backward in history
                if self._history_index > 0:
                    self._history_index -= 1
                    self.text = self._history[self._history_index]
                    event.prevent_default()
                    event.stop()

        elif event.key == "down":
            # Only navigate history if cursor is on last line
            lines = self.text.split('\n')
            if len(lines) <= 1 or self.cursor_location[0] == len(lines) - 1:
                # Only navigate if we have history and are not already at present
                if not self._history:
                    return

                # Navigate forward in history
                if self._history_index < len(self._history) - 1:
                    self._history_index += 1
                    self.text = self._history[self._history_index]
                    event.prevent_default()
                    event.stop()
                # Return to present (restore draft)
                elif self._history_index < len(self._history):
                    self._history_index = len(self._history)
                    self.text = self._current_draft
                    event.prevent_default()
                    event.stop()
