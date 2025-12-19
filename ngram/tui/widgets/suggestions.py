# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""Command suggestions widget."""

from textual.widgets import Static


class SuggestionsBar(Static):
    """Shows command suggestions above the input bar."""

    DEFAULT_CSS = """
    SuggestionsBar {
        height: auto;
        max-height: 6;
        width: 100%;
        padding: 0 1;
        background: $surface;
        color: $text-muted;
        display: none;
    }

    SuggestionsBar.visible {
        display: block;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__("", **kwargs)

    def show_suggestions(self, suggestions: list[tuple[str, str]]) -> None:
        """Show or hide suggestions.

        Args:
            suggestions: List of (command, description) tuples
        """
        if not suggestions:
            self.remove_class("visible")
            self.update("")
            return

        # Format suggestions
        lines = []
        for cmd, desc in suggestions[:5]:  # Max 5 suggestions
            lines.append(f"[bold cyan]{cmd}[/] [dim]{desc}[/]")

        self.update("\n".join(lines))
        self.add_class("visible")
