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

    /* Completed agents list (stacked above active columns) */
    AgentContainer #agents-stack {
        width: 100%;
        height: 100%;
    }

    AgentContainer #agents-completed {
        width: 100%;
        height: auto;
        max-height: 40%;
        padding: 1;
    }

    /* Agent columns container */
    AgentContainer #agents-columns {
        width: 100%;
        height: 100%;
        padding: 0;
    }

    /* Each agent panel takes equal width */
    AgentContainer #agents-columns > AgentPanel {
        width: 1fr;
        height: 100%;
    }
    """

    MAX_COLUMNS = 3

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._agent_panels: dict[str, any] = {}
        self._tabbed: TabbedContent | None = None
        self._completed_ids: set[str] = set()

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
                Container(
                    Container(
                        VerticalScroll(Static("No completed agents yet.", classes="placeholder"), id="agents-completed"),
                        Horizontal(Static("No agents running. Type /repair to start.", classes="placeholder"), id="agents-columns"),
                        id="agents-stack",
                    ),
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
        """Add a panel for a new agent as a column."""
        from .agent_panel import AgentPanel

        # Remove placeholder if present (any Static with placeholder class)
        try:
            agents_columns = self.app.query_one("#agents-columns", Horizontal)
            for child in list(agents_columns.children):
                if hasattr(child, 'has_class') and child.has_class("placeholder"):
                    child.remove()
        except Exception:
            pass

        panel = AgentPanel(
            agent_id=agent.id,
            symbol=agent.symbol,
            issue_type=agent.issue_type,
            target_path=agent.target_path,
            id=f"agent-panel-{agent.id}",
        )

        # Mount in agents columns container (horizontal layout)
        agents_columns = self.app.query_one("#agents-columns", Horizontal)
        agents_columns.mount(panel)
        self._agent_panels[agent.id] = panel
        self._completed_ids.discard(agent.id)

        # Switch to agents tab when agent starts
        if self._tabbed:
            self._tabbed.active = "agents-tab"

    def update_agent(self, agent_id: str, text: str) -> None:
        """Update an agent's output (replaces content)."""
        panel = self._agent_panels.get(agent_id)
        if panel:
            panel.set_output(text)

    def remove_agent(self, agent_id: str) -> None:
        """Remove an agent's panel."""
        panel = self._agent_panels.pop(agent_id, None)
        if panel:
            panel.remove()
        was_completed = agent_id in self._completed_ids
        self._completed_ids.discard(agent_id)

        if was_completed:
            try:
                completed_list = self.app.query_one("#agents-completed", VerticalScroll)
                has_completed = any(
                    child.id and str(child.id).startswith("agent-panel-")
                    for child in completed_list.children
                )
                if not has_completed:
                    completed_list.mount(
                        Static("No completed agents yet.", classes="placeholder")
                    )
            except Exception:
                pass

        # Show placeholder if empty
        if not self._agent_panels:
            try:
                agents_columns = self.app.query_one("#agents-columns", Horizontal)
                placeholder = Static(
                    "No agents running. Type /repair to start.",
                    classes="placeholder"
                )
                agents_columns.mount(placeholder)
            except Exception:
                pass

    def set_agent_status(self, agent_id: str, status: str) -> None:
        """Update an agent's status."""
        panel = self._agent_panels.get(agent_id)
        if panel:
            panel.set_status(status)
            if status in ("completed", "failed"):
                self._move_to_completed(agent_id, panel)

    def _move_to_completed(self, agent_id: str, panel) -> None:
        """Move completed/failed agent panel above active columns."""
        if agent_id in self._completed_ids:
            return
        try:
            completed_list = self.app.query_one("#agents-completed", VerticalScroll)
            # Remove placeholder if present
            for child in list(completed_list.children):
                if hasattr(child, 'has_class') and child.has_class("placeholder"):
                    child.remove()
            panel.remove()
            completed_list.mount(panel)
            self._completed_ids.add(agent_id)
        except Exception:
            return

        # Show placeholder if no active agents remain in columns
        try:
            agents_columns = self.app.query_one("#agents-columns", Horizontal)
            active_panels = [child for child in agents_columns.children if child.id and str(child.id).startswith("agent-panel-")]
            if not active_panels:
                agents_columns.mount(
                    Static("No agents running. Type /repair to start.", classes="placeholder")
                )
        except Exception:
            pass

    def update_sync_content(self, content: str) -> None:
        """Update the SYNC tab content with Markdown."""
        try:
            app = self.app
            scroll = app.query_one("#sync-scroll", VerticalScroll)
            # Try to update existing Markdown, or create if none
            md_widgets = list(scroll.query(Markdown))
            if md_widgets:
                md_widgets[0].update(content)
            else:
                # Remove any non-Markdown children first
                for child in list(scroll.children):
                    child.remove()
                scroll.mount(Markdown(content))
        except Exception as e:
            self.log.error(f"update_sync_content failed: {e}")

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

                if critical:
                    lines.append(f"\n### Critical ({len(critical)})\n")
                    for issue in critical:
                        lines.append(f"- **{issue.issue_type}**: `{issue.path}`")

                if warnings:
                    lines.append(f"\n### Warnings ({len(warnings)})\n")
                    for issue in warnings:
                        lines.append(f"- **{issue.issue_type}**: `{issue.path}`")

                if info:
                    lines.append(f"\n### Info ({len(info)})\n")
                    for issue in info[:10]:
                        lines.append(f"- {issue.issue_type}: `{issue.path}`")
                    if len(info) > 10:
                        lines.append(f"- ... and {len(info) - 10} more")

            content = "\n".join(lines)
            scroll = self.app.query_one("#doctor-scroll", VerticalScroll)
            md_widgets = list(scroll.query(Markdown))
            if md_widgets:
                md_widgets[0].update(content)
            else:
                for child in list(scroll.children):
                    child.remove()
                scroll.mount(Markdown(content))
        except Exception as e:
            self.log.error(f"update_doctor_content failed: {e}")

    def update_map_content(self, content: str) -> None:
        """Update the MAP tab content with Markdown."""
        try:
            scroll = self.app.query_one("#map-scroll", VerticalScroll)
            md_widgets = list(scroll.query(Markdown))
            if md_widgets:
                md_widgets[0].update(content)
            else:
                for child in list(scroll.children):
                    child.remove()
                scroll.mount(Markdown(content))
        except Exception as e:
            self.log.error(f"update_map_content failed: {e}")

    def update_changes_content(self, file_changes: str, commits: str, updated_at: str = "") -> None:
        """Update the CHANGES tab with Markdown."""
        try:
            # Build markdown content
            header = "## File Changes"
            if updated_at:
                header += f" *(updated {updated_at})*"
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
            scroll = self.app.query_one("#changes-scroll", VerticalScroll)
            md_widgets = list(scroll.query(Markdown))
            if md_widgets:
                md_widgets[0].update(content)
            else:
                for child in list(scroll.children):
                    child.remove()
                scroll.mount(Markdown(content))
        except Exception as e:
            self.log.error(f"update_changes_content failed: {e}")

    def switch_to_tab(self, tab_id: str) -> None:
        """Switch to a specific tab."""
        if self._tabbed:
            self._tabbed.active = tab_id
