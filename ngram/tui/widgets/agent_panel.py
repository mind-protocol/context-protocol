# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""Single agent panel widget for agent output display."""

from textual.widgets import Static, Markdown, Input
from textual.containers import Vertical, VerticalScroll


class AgentPanel(Vertical):
    """
    Panel displaying a single agent's output.

    Shows:
    - Agent symbol and issue type (fixed header, always visible)
    - Real-time streamed output (scrollable)
    - Status indicator (running/completed/failed)
    """

    DEFAULT_CSS = """
    AgentPanel {
        width: 1fr;
        border-left: solid $primary;
        padding: 0 1;
        overflow: hidden;
    }

    AgentPanel .header {
        background: $surface;
        padding: 0 1;
        dock: top;
        height: auto;
    }

    AgentPanel .output-scroll {
        height: 1fr;
        overflow-x: hidden;
    }

    AgentPanel .output {
        width: 100%;
        overflow: hidden;
    }

    AgentPanel MarkdownFence {
        overflow: hidden;
        max-width: 100%;
    }

    AgentPanel .output-line {
        margin: 0;
    }

    AgentPanel .agent-input {
        height: 3;
        border: solid $border;
        background: $surface;
        margin-top: 1;
    }

    AgentPanel .agent-input:focus {
        border: solid $accent;
    }

    AgentPanel.running .header {
        color: $primary;
    }

    AgentPanel.completed .header {
        color: green;
    }

    AgentPanel.failed .header {
        color: red;
    }
    """

    def __init__(
        self,
        agent_id: str,
        symbol: str,
        issue_type: str,
        target_path: str,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.agent_id = agent_id
        self.symbol = symbol
        self.issue_type = issue_type
        self.target_path = target_path
        self._output_widget: Static | None = None
        self._output_scroll: VerticalScroll | None = None
        self._output_content: str = ""

    def on_mount(self) -> None:
        """Initialize on mount."""
        # Header with agent symbol, issue type and target path (fixed, always visible)
        header = Static(
            f"{self.symbol} {self.issue_type}: {self.target_path}",
            classes="header"
        )
        self.mount(header)

        # Scrollable output area with markdown support
        self._output_scroll = VerticalScroll(classes="output-scroll")
        self.mount(self._output_scroll)

        self._output_widget = Markdown("*...*", classes="output")
        self._output_scroll.mount(self._output_widget)

        # Input field for agent interaction (non-functional for now)
        self._input = Input(
            placeholder=f"> Message {self.symbol}...",
            classes="agent-input"
        )
        self.mount(self._input)

        self.add_class("running")

    def set_output(self, text: str) -> None:
        """Set/replace the output area content."""
        if self._output_widget:
            self._output_content = text
            # Show last 50 lines to prevent slowdown
            lines = text.split('\n')
            display = '\n'.join(lines[-50:])
            self._output_widget.update(display)
            if self._output_scroll:
                self._output_scroll.scroll_end(animate=False)

    def append_output(self, text: str) -> None:
        """Append text to the output area."""
        if self._output_widget:
            if self._output_content:
                # Add line break between messages
                self._output_content += "\n\n" + text
            else:
                self._output_content = text
            # Show last 50 lines to prevent slowdown
            lines = self._output_content.split('\n')
            display = '\n'.join(lines[-50:])
            self._output_widget.update(display)
            if self._output_scroll:
                self._output_scroll.scroll_end(animate=False)

    def set_status(self, status: str) -> None:
        """Update the status (running/completed/failed)."""
        self.remove_class("running")
        self.remove_class("completed")
        self.remove_class("failed")
        self.add_class(status)
