# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""
Container for right panel with tabbed interface.

Tabs:
- AGENTS: Shows running agent panels
- SYNC: Shows SYNC_Project_State.md
- DOCTOR: Shows health check results
"""

from typing import TYPE_CHECKING

from textual.containers import Container, VerticalScroll, Horizontal, ScrollableContainer
from textual.widgets import Static, TabbedContent, TabPane, Markdown


class ClickableStatic(Static):
    """Static widget that copies stored content on click."""

    def __init__(self, content, raw_content: str = "", **kwargs) -> None:
        super().__init__(content, **kwargs)
        self._raw_content = raw_content

    def on_click(self) -> None:
        """Copy content to clipboard on click."""
        if self._raw_content:
            self.app.copy_to_clipboard(self._raw_content)
            self.notify("Copied!", timeout=1)

if TYPE_CHECKING:
    from ..state import AgentHandle


class AgentContainer(Container):
    """
    Tabbed container for the right panel.

    Tabs:
    - AGENTS: Running repair agents (columns or nested tabs for 4+)
    - SYNC: Project state from SYNC_Project_State.md
    - DOCTOR: Health check results
    """

    DEFAULT_CSS = """
    AgentContainer {
        width: 1fr;
        height: 100%;
    }

    AgentContainer > TabbedContent {
        width: 100%;
        height: 100%;
    }

    AgentContainer ContentSwitcher {
        width: 100%;
        height: 100%;
    }

    AgentContainer TabPane {
        width: 100%;
        height: 100%;
        padding: 0;
    }

    AgentContainer .placeholder {
        text-align: center;
        color: $text-muted;
        padding: 2;
        width: 100%;
    }

    AgentContainer VerticalScroll {
        width: 100%;
        height: 100%;
        padding: 1;
    }

    /* Summary log container */
    AgentContainer #summary-log {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._agent_panels: dict[str, any] = {}
        self._tabbed: TabbedContent | None = None
        self._completed_ids: set[str] = set()
        self._max_markdown_chars = 20000
        self._markdown_cache: dict[str, tuple[str, object]] = {}

    def _prepare_markdown(self, content: str, label: str) -> str:
        """Truncate large markdown content to keep tab rendering responsive."""
        if len(content) <= self._max_markdown_chars:
            return content
        tail = content[-self._max_markdown_chars:]
        notice = f"**{label} truncated to last {self._max_markdown_chars} chars.**\n\n"
        return notice + tail

    def _set_markdown_content(self, scroll_id: str, content: str, label: str) -> None:
        """Render markdown once and reuse cached renderable."""
        try:
            from rich.markdown import Markdown as RichMarkdown

            scroll = self.app.query_one(f"#{scroll_id}", VerticalScroll)
            content = self._prepare_markdown(content, label)
            cache_key = f"{scroll_id}:{label}"
            cached = self._markdown_cache.get(cache_key)
            if cached and cached[0] == content:
                return
            renderable = RichMarkdown(content)
            for child in list(scroll.children):
                child.remove()
            scroll.mount(ClickableStatic(renderable, raw_content=content))
            self._markdown_cache[cache_key] = (content, renderable)
        except Exception as e:
            self.log.error(f"_set_markdown_content failed ({label}): {e}")

    def compose(self):
        """Compose the tabbed interface. Order: CHANGES, SYNC, DOCTOR, MAP, AGENTS."""
        with TabbedContent(id="right-tabs"):
            yield TabPane(
                "CHANGES",
                VerticalScroll(Static("Loading changes..."), id="changes-scroll"),
                id="changes-tab"
            )
            yield TabPane(
                "SYNC",
                VerticalScroll(Static("Loading SYNC..."), id="sync-scroll"),
                id="sync-tab"
            )
            yield TabPane(
                "DOCTOR",
                VerticalScroll(Static("Run /doctor to check health"), id="doctor-scroll"),
                id="doctor-tab"
            )
            yield TabPane(
                "MAP",
                VerticalScroll(Static("Loading MAP..."), id="map-scroll"),
                id="map-tab"
            )
            yield TabPane(
                "AGENTS",
                VerticalScroll(
                    Static("Agent summaries will appear here during /repair", classes="placeholder"),
                    id="summary-log"
                ),
                id="agents-tab"
            )

    def on_mount(self) -> None:
        """Store reference to tabbed content."""
        try:
            self._tabbed = self.query_one("#right-tabs", TabbedContent)
            self.log.info(f"on_mount: found TabbedContent, active={self._tabbed.active}")
        except Exception as e:
            self.log.error(f"on_mount: failed to find TabbedContent: {e}")

    def add_agent(self, agent: "AgentHandle") -> None:
        """Track a new agent (summary log mode - no panels)."""
        self._agent_panels[agent.id] = agent
        self._completed_ids.discard(agent.id)

        # Switch to agents tab when agent starts
        if self._tabbed:
            self._tabbed.active = "agents-tab"

    def update_agent(self, agent_id: str, text: str) -> None:
        """Update an agent's output (no-op in summary mode)."""
        pass

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent from tracking."""
        self._agent_panels.pop(agent_id, None)
        self._completed_ids.discard(agent_id)

    def set_agent_status(self, agent_id: str, status: str) -> None:
        """Update an agent's status."""
        if status in ("completed", "failed"):
            self._completed_ids.add(agent_id)

    def update_sync_content(self, content: str) -> None:
        """Update the SYNC tab content with Markdown."""
        self._set_markdown_content("sync-scroll", content, "SYNC")

    def update_doctor_content(self, issues: list, score: int) -> None:
        """Update the DOCTOR tab content with Markdown."""
        try:
            # Build markdown content
            lines = [f"## Health Score: {score}/100\n"]

            if not issues:
                lines.append("✓ No issues found")
            else:
                critical = [i for i in issues if i.severity == "critical"]
                warnings = [i for i in issues if i.severity == "warning"]
                info = [i for i in issues if i.severity == "info"]

                def get_path(issue):
                    """Safely get issue path as string."""
                    p = issue.path
                    if isinstance(p, list):
                        return p[0] if p else ""
                    return str(p)

                if critical:
                    lines.append(f"\n### Critical ({len(critical)})\n")
                    for issue in critical:
                        lines.append(f"- **{issue.issue_type}**: `{get_path(issue)}`")

                if warnings:
                    lines.append(f"\n### Warnings ({len(warnings)})\n")
                    for issue in warnings:
                        lines.append(f"- **{issue.issue_type}**: `{get_path(issue)}`")

                if info:
                    lines.append(f"\n### Info ({len(info)})\n")
                    for issue in info[:10]:
                        lines.append(f"- {issue.issue_type}: `{get_path(issue)}`")
                    if len(info) > 10:
                        lines.append(f"- ... and {len(info) - 10} more")

            content = "\n".join(lines)
        except Exception as e:
            self.log.error(f"update_doctor_content failed: {e}")
            return
        self._set_markdown_content("doctor-scroll", content, "DOCTOR")

    def update_map_content(self, content: str) -> None:
        """Update the MAP tab content with Markdown."""
        self._set_markdown_content("map-scroll", content, "MAP")

    def update_changes_content(
        self,
        file_changes: str,
        commits: str,
        updated_at: str = "",
        change_rate: float = 0.0,
        commit_rate: float = 0.0,
    ) -> None:
        """Update the CHANGES tab with Markdown."""
        try:
            # Build markdown content
            header = "## File Changes"
            if updated_at:
                header += f" *(updated {updated_at})*"
            header += f" — {change_rate:.1f} changes/min, {commit_rate:.1f} commits/min"
            lines = [header + "\n"]
            if file_changes.strip():
                lines.append(f"```\n{file_changes}\n```")
            else:
                lines.append("*No uncommitted changes*")

            lines.append("\n---\n")
            lines.append("## Recent Commits\n")
            if commits.strip():
                lines.append(f"```\n{commits}\n```")
            else:
                lines.append("*No commits yet*")

            content = "\n".join(lines)
        except Exception as e:
            self.log.error(f"update_changes_content failed: {e}")
            return
        self._set_markdown_content("changes-scroll", content, "CHANGES")

    def switch_to_tab(self, tab_id: str) -> None:
        """Switch to a specific tab."""
        if self._tabbed:
            self._tabbed.active = tab_id

    def add_summary(self, text: str) -> None:
        """Add a summary entry to the AGENTS summary log."""
        try:
            scroll = self.app.query_one("#summary-log", VerticalScroll)
            # Remove placeholder if present
            for child in list(scroll.children):
                if hasattr(child, 'has_class') and child.has_class("placeholder"):
                    child.remove()
            scroll.mount(Static(text, markup=True))
            scroll.scroll_end(animate=False)
        except Exception as e:
            self.log.error(f"add_summary failed: {e}")

    def clear_summary(self) -> None:
        """Clear the summary log."""
        try:
            scroll = self.app.query_one("#summary-log", VerticalScroll)
            for child in list(scroll.children):
                child.remove()
            scroll.mount(Static("Agent summaries will appear here during /repair", classes="placeholder"))
        except Exception as e:
            self.log.error(f"clear_summary failed: {e}")
