# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""Manager panel widget for orchestration output."""

from textual.widgets import Static, Markdown, Collapsible
from textual.containers import VerticalScroll
from textual.widget import Widget


class ClickableStatic(Static):
    """Static widget that copies content on click."""

    def __init__(self, content: str, **kwargs) -> None:
        super().__init__(content, **kwargs)
        self._raw_content = content

    def on_click(self) -> None:
        """Copy content to clipboard on click."""
        self.app.copy_to_clipboard(self._raw_content)
        self.notify("Copied!", timeout=1)

    def update(self, content: str):
        """Update content and raw content."""
        import inspect
        import asyncio

        self._raw_content = content
        result = super().update(content)
        if inspect.isawaitable(result):
            try:
                loop = asyncio.get_running_loop()
                task = loop.create_task(result)
                return task
            except RuntimeError:
                return result
        return result


class ClickableMarkdown(Markdown):
    """Markdown widget that copies content on click."""

    def __init__(self, content: str, **kwargs) -> None:
        super().__init__(content, **kwargs)
        self._raw_content = content

    def on_click(self) -> None:
        """Copy content to clipboard on click."""
        self.app.copy_to_clipboard(self._raw_content)
        self.notify("Copied!", timeout=1)

    def update(self, content: str):
        """Update content and raw content."""
        import inspect
        import asyncio

        self._raw_content = content
        result = super().update(content)
        if inspect.isawaitable(result):
            try:
                loop = asyncio.get_running_loop()
                task = loop.create_task(result)
                return task
            except RuntimeError:
                return result
        return result


class ManagerPanel(VerticalScroll):
    """
    Left panel displaying manager/orchestration messages.

    Shows:
    - Status updates
    - Agent spawn notifications
    - Drift warnings
    - User guidance
    """

    DEFAULT_CSS = """
    ManagerPanel {
        width: 100%;
        height: 1fr;
        padding: 0 1;
    }

    ManagerPanel .message {
        margin-bottom: 1;
    }

    ManagerPanel .markdown-message {
        margin-bottom: 1;
    }

    ManagerPanel .warning {
        color: $warning;
    }

    ManagerPanel .thinking-collapsible {
        margin-bottom: 1;
        padding: 0;
    }

    ManagerPanel .thinking-collapsible CollapsibleTitle {
        color: #8B7355;  /* Oak - muted */
        text-style: italic;
        padding: 0;
    }

    ManagerPanel .thinking-content {
        color: #8B7355;  /* Oak - muted */
        text-style: italic;
        padding-left: 2;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._messages: list[Widget] = []

    def on_mount(self) -> None:
        """Initialize on mount."""
        # No header - clean look
        pass

    def _is_at_bottom(self) -> bool:
        """Check if scrolled to bottom (or close enough)."""
        # Allow small tolerance for floating point
        return self.scroll_y >= self.max_scroll_y - 2

    def _auto_scroll(self) -> None:
        """Scroll to end only if already at bottom."""
        if self._is_at_bottom():
            self.scroll_end(animate=False)

    def add_message(self, message: str, markdown: bool = False, before: Widget = None) -> Widget:
        """Add a message to the panel and return the widget.

        Args:
            message: The message text
            markdown: If True, render as markdown
            before: If provided, insert before this widget
        """
        # Auto-detect markdown if not explicitly set
        if not markdown:
            # Check for common markdown patterns (but not Rich markup like [blue])
            # Rich markup: [color]...[/] or [bold]...[/]
            import re
            has_rich_markup = re.search(r'\[(?:blue|red|green|dim|bold|italic|cyan|magenta|yellow|white|#[0-9A-Fa-f]+)[^\]]*\]', message)
            has_markdown_link = re.search(r'\[[^\]]+\]\([^)]+\)', message)  # [text](url)
            markdown = any(pattern in message for pattern in [
                '```', '**', '__', '##', '- ', '* ', '1. '
            ]) or has_markdown_link
            # Don't use markdown if it's just Rich markup
            if has_rich_markup and not any(p in message for p in ['```', '**', '__', '##']):
                markdown = False

        if markdown:
            widget = ClickableMarkdown(message, classes="markdown-message")
        else:
            widget = ClickableStatic(message, classes="message")

        if before:
            self.mount(widget, before=before)
        else:
            self.mount(widget)
        self._messages.append(widget)
        self._auto_scroll()
        return widget

    def add_thinking(self, thinking: str, max_preview_lines: int = 3, before: Widget = None) -> Widget:
        """Add a collapsible thinking block.

        Args:
            thinking: The full thinking text
            max_preview_lines: Number of lines to show as preview
            before: If provided, insert before this widget (keeps it at bottom)
        """
        from textual.containers import Vertical

        lines = thinking.split('\n')

        if len(lines) <= max_preview_lines:
            # Short thinking - just show it all
            widget = Static(f"[dim italic]💭 {thinking}[/]", classes="thinking-content")
            if before:
                self.mount(widget, before=before)
            else:
                self.mount(widget)
            self._messages.append(widget)
            self._auto_scroll()
            return widget

        # Show first 3 lines as preview, rest in collapsible
        preview = '\n'.join(lines[:max_preview_lines])
        rest = '\n'.join(lines[max_preview_lines:])

        container = Vertical(classes="thinking-block")

        # Preview text (always visible)
        preview_widget = Static(f"[dim italic]💭 {preview}...[/]", classes="thinking-preview")

        # Collapsible for the rest
        collapsible = Collapsible(
            Static(rest, classes="thinking-content"),
            title="Show more",
            collapsed=True,
            classes="thinking-collapsible"
        )

        if before:
            self.mount(container, before=before)
        else:
            self.mount(container)
        container.mount(preview_widget)
        container.mount(collapsible)
        self._messages.append(container)
        self._auto_scroll()
        return container

    def add_tool_call(self, tool_name: str, tool_input: dict = None, before: Widget = None) -> Widget:
        """Add a tool call indicator.

        Args:
            tool_name: Name of the tool being called
            tool_input: Optional input parameters
            before: If provided, insert before this widget
        """
        def escape_markup(s: str) -> str:
            """Escape Rich markup characters."""
            return s.replace("[", "[[").replace("]", "]]")

        # Format tool call compactly in blue
        if tool_input:
            # Show key params briefly
            params = []
            for k, v in list(tool_input.items())[:3]:
                val = str(v)[:30] + "..." if len(str(v)) > 30 else str(v)
                params.append(f"{k}={escape_markup(val)}")
            param_str = ", ".join(params)
            text = f"[blue]🔧 {escape_markup(tool_name)}({param_str})[/]"
            # Plain text for clipboard
            copy_text = f"{tool_name}({param_str})"
        else:
            text = f"[blue]🔧 {escape_markup(tool_name)}[/]"
            copy_text = tool_name

        inner_widget = Static(text, classes="tool-call")
        widget = CopyableMessage(content=copy_text, widget=inner_widget)
        if before:
            self.mount(widget, before=before)
        else:
            self.mount(widget)
        self._messages.append(widget)
        self._auto_scroll()
        return widget

    def clear(self) -> None:
        """Clear all messages."""
        for msg in self._messages:
            msg.remove()
        self._messages.clear()
