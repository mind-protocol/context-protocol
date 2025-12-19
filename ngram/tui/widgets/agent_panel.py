# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""Single agent panel widget for agent output display."""

from textual.widgets import Static, Markdown, Input
from textual.containers import Vertical, VerticalScroll


class AgentPanel(Vertical):
    """
    Panel displaying a single agent's output.

    Shows:
    - Agent symbol and issue type (fixed header, always visible)
    - Real-time streamed output (scrollable, hidden when collapsed)
    - Status indicator (running/completed/failed)

    Completed/failed agents collapse to just header, click to expand.
    """

    DEFAULT_CSS = """
    /* ─── Base Layout (theme-independent) ─── */
    AgentPanel {
        width: 1fr;
        height: 100%;
        padding: 0;
        overflow: hidden;
    }

    AgentPanel.collapsed {
        height: auto;
        max-height: 3;
        width: auto;
        min-width: 20;
    }

    AgentPanel.collapsed .output-scroll {
        display: none;
    }

    AgentPanel.collapsed .agent-input {
        display: none;
    }

    AgentPanel .header {
        padding: 0 1;
        dock: top;
        height: auto;
        text-style: bold;
    }

    AgentPanel .output-scroll {
        height: 1fr;
        overflow-x: hidden;
        padding: 1;
    }

    AgentPanel .output {
        width: 100%;
        overflow: hidden;
    }

    AgentPanel MarkdownFence {
        overflow: hidden;
        max-width: 100%;
    }

    AgentPanel .agent-input {
        height: 3;
        margin-top: 1;
    }

    /* ─── Light Theme (default) ─── */
    AgentPanel {
        border-left: solid #C4B49A;
        background: #FAF6ED;
    }

    AgentPanel .header {
        background: #E8DFD0;
        color: #2C1810;
    }

    AgentPanel .header:hover {
        background: #D4C4A8;
    }

    AgentPanel .output {
        color: #2C1810;
    }

    AgentPanel MarkdownFence {
        background: #2F3542;
    }

    AgentPanel .agent-input {
        border: solid #C4B49A;
        background: #F5F0E6;
        color: #2C1810;
    }

    AgentPanel .agent-input:focus {
        border: solid #A0522D;
    }

    AgentPanel.running .header {
        background: #E8DFD0;
        color: #B87333;
    }

    AgentPanel.completed .header {
        background: #D4E5C8;
        color: #5F7A4A;
    }

    AgentPanel.failed .header {
        background: #E8D0C8;
        color: #A0522D;
    }

    /* ─── Dark Theme (when app.dark = True) ─── */
    App.-dark-mode AgentPanel {
        border-left: solid #6B5D4D;
        background: #4A3F35;
    }

    App.-dark-mode AgentPanel .header {
        background: #5C4D3D;
        color: #F5F0E6;
    }

    App.-dark-mode AgentPanel .header:hover {
        background: #6B5D4D;
    }

    App.-dark-mode AgentPanel .output {
        color: #F5F0E6;
    }

    App.-dark-mode AgentPanel MarkdownFence {
        background: #3D3229;
    }

    App.-dark-mode AgentPanel .agent-input {
        border: solid #6B5D4D;
        background: #5C4D3D;
        color: #F5F0E6;
    }

    App.-dark-mode AgentPanel .agent-input:focus {
        border: solid #D4A574;
    }

    App.-dark-mode AgentPanel.running .header {
        background: #5C4D3D;
        color: #D4A574;
    }

    App.-dark-mode AgentPanel.completed .header {
        background: #4A5A4A;
        color: #A8C99B;
    }

    App.-dark-mode AgentPanel.failed .header {
        background: #5A4A42;
        color: #C97B5D;
    }
    """

    # Render throttling - 100ms minimum between updates
    RENDER_INTERVAL = 0.1

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
        self._header: Static | None = None
        self._collapsed: bool = False
        self._status: str = "running"
        self._stick_to_bottom: bool = True
        self._user_scrolled: bool = False
        # Render throttling
        self._last_render: float = 0.0
        self._pending_render: bool = False

    def on_mount(self) -> None:
        """Initialize on mount."""
        # Header with agent symbol, issue type and target path (fixed, always visible)
        self._header = Static(
            f"{self.symbol} {self.issue_type}: {self.target_path}",
            classes="header"
        )
        self.mount(self._header)

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


    def on_scroll(self, event) -> None:
        """Track whether the user is at the bottom of the output."""
        if event.sender is self._output_scroll:
            if self._output_scroll:
                at_bottom = self._output_scroll.scroll_y >= self._output_scroll.max_scroll_y - 2
                self._stick_to_bottom = at_bottom
                self._user_scrolled = not at_bottom

    def toggle_collapse(self) -> None:
        """Toggle between collapsed and expanded state."""
        self._collapsed = not self._collapsed
        if self._collapsed:
            self.add_class("collapsed")
            self._update_header_text()
        else:
            self.remove_class("collapsed")
            self._update_header_text()

    def collapse(self) -> None:
        """Collapse the panel."""
        if not self._collapsed:
            self._collapsed = True
            self.add_class("collapsed")
            self._update_header_text()

    def expand(self) -> None:
        """Expand the panel."""
        if self._collapsed:
            self._collapsed = False
            self.remove_class("collapsed")
            self._update_header_text()

    def _update_header_text(self) -> None:
        """Update header text with collapse indicator."""
        if self._header:
            indicator = "▶" if self._collapsed else "▼" if self._status != "running" else ""
            status_icon = "✓" if self._status == "completed" else "✗" if self._status == "failed" else "⋯"
            if self._status == "running":
                self._header.update(f"{self.symbol} {self.issue_type}: {self.target_path}")
            else:
                self._header.update(f"{indicator} {status_icon} {self.symbol} {self.issue_type}: {self.target_path}")

    def set_output(self, text: str) -> None:
        """Set/replace the output area content (throttled)."""
        import time
        self._output_content = text
        self._maybe_render()

    def append_output(self, text: str) -> None:
        """Append text to the output area (throttled)."""
        if self._output_content:
            self._output_content += "\n\n" + text
        else:
            self._output_content = text
        self._maybe_render()

    def _maybe_render(self) -> None:
        """Render if enough time has passed, otherwise schedule."""
        import time
        now = time.time()
        if now - self._last_render >= self.RENDER_INTERVAL:
            self._do_render()
            self._last_render = now
            self._pending_render = False
        elif not self._pending_render:
            # Schedule a render for later
            self._pending_render = True
            self.set_timer(self.RENDER_INTERVAL, self._flush_render)

    def _flush_render(self) -> None:
        """Flush any pending render."""
        if self._pending_render:
            self._do_render()
            self._pending_render = False
            import time
            self._last_render = time.time()

    def _do_render(self) -> None:
        """Actually render the output (expensive)."""
        if self._output_widget and self._output_content:
            at_bottom = False
            if self._output_scroll:
                at_bottom = self._output_scroll.scroll_y >= self._output_scroll.max_scroll_y - 2
                if at_bottom:
                    self._user_scrolled = False
            # Show last 50 lines to prevent slowdown
            lines = self._output_content.split('\n')
            display = '\n'.join(lines[-50:])
            self._output_widget.update(display)
            if self._output_scroll and (self._stick_to_bottom or not self._user_scrolled):
                self._output_scroll.scroll_end(animate=False)

    def set_status(self, status: str) -> None:
        """Update the status (running/completed/failed)."""
        self.remove_class("running")
        self.remove_class("completed")
        self.remove_class("failed")
        self.add_class(status)
        self._status = status

        # Flush any pending output before status change
        if status in ("completed", "failed"):
            self._do_render()
            self._pending_render = False
            self.collapse()

        self._update_header_text()
