# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""
Container for right panel with tabbed interface.

Tabs:
- AGENTS: Shows running agent panels
- SYNC: Shows SYNC_Project_State.md
- DOCTOR: Shows health check results
"""

from typing import TYPE_CHECKING

from textual.containers import Container, VerticalScroll
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
    }

    AgentContainer VerticalScroll {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    """

    MAX_COLUMNS = 3

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._agent_panels: dict[str, any] = {}
        self._tabbed: TabbedContent | None = None

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
                VerticalScroll(Static("No agents running. Type /repair to start.", classes="placeholder"), id="agents-scroll"),
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
        """Add a panel for a new agent."""
        from .agent_panel import AgentPanel

        # Remove placeholder if present (any Static with placeholder class)
        try:
            agents_scroll = self.query_one("#agents-scroll")
            for child in list(agents_scroll.children):
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

        # Mount in agents scroll container
        agents_scroll = self.query_one("#agents-scroll")
        agents_scroll.mount(panel)
        self._agent_panels[agent.id] = panel

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

        # Show placeholder if empty
        if not self._agent_panels:
            agents_scroll = self.query_one("#agents-scroll")
            placeholder = Static(
                "No agents running. Type /repair to start.",
                classes="placeholder"
            )
            agents_scroll.mount(placeholder)

    def set_agent_status(self, agent_id: str, status: str) -> None:
        """Update an agent's status."""
        panel = self._agent_panels.get(agent_id)
        if panel:
            panel.set_status(status)

    def update_sync_content(self, content: str) -> None:
        """Update the SYNC tab content with Markdown."""
        try:
            # Query from app level to find nested widgets
            app = self.app
            scroll = app.query_one("#sync-scroll", VerticalScroll)
            # Remove old content
            for child in list(scroll.children):
                child.remove()
            # Add new Markdown content (no ID to avoid conflicts)
            scroll.mount(Markdown(content))
        except Exception as e:
            try:
                manager = self.app.query_one("#manager-panel")
                manager.add_message(f"[red]SYNC error: {e}[/]")
            except:
                pass
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
            for child in list(scroll.children):
                child.remove()
            scroll.mount(Markdown(content))
        except Exception as e:
            try:
                manager = self.app.query_one("#manager-panel")
                manager.add_message(f"[red]DOCTOR error: {e}[/]")
            except:
                pass

    def update_map_content(self, content: str) -> None:
        """Update the MAP tab content with Markdown."""
        try:
            scroll = self.app.query_one("#map-scroll", VerticalScroll)
            for child in list(scroll.children):
                child.remove()
            scroll.mount(Markdown(content))
        except Exception as e:
            try:
                manager = self.app.query_one("#manager-panel")
                manager.add_message(f"[red]MAP error: {e}[/]")
            except:
                pass

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
            for child in list(scroll.children):
                child.remove()
            scroll.mount(Markdown(content))
        except Exception as e:
            try:
                manager = self.app.query_one("#manager-panel")
                manager.add_message(f"[red]CHANGES error: {e}[/]")
            except:
                pass

    def switch_to_tab(self, tab_id: str) -> None:
        """Switch to a specific tab."""
        if self._tabbed:
            self._tabbed.active = tab_id
