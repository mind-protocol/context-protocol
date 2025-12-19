# DOCS: docs/tui/IMPLEMENTATION_TUI_Code_Architecture.md
"""
Session state management for the TUI.

Centralized state avoids global variables and makes testing easier.
"""

from dataclasses import dataclass, field
from typing import Any, List, Optional
from pathlib import Path
import asyncio
import json
import time
from datetime import datetime


@dataclass
class ConversationMessage:
    """A single message in the conversation history."""
    role: str  # "user", "assistant", "system"
    content: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        timestamp = self.timestamp or datetime.now().isoformat()
        return {"role": self.role, "content": self.content, "timestamp": timestamp}

    @classmethod
    def from_dict(cls, data: dict) -> "ConversationMessage":
        return cls(
            role=data.get("role", "system"),
            content=data.get("content", ""),
            timestamp=data.get("timestamp", datetime.now().isoformat())
        )


class ConversationHistory:
    """Manages persistent conversation history."""

    def __init__(self, target_dir: Path):
        self.target_dir = target_dir
        self.history_file = target_dir / ".ngram" / "state" / "conversation_history.json"
        self.messages: List[ConversationMessage] = []
        self._load()

    def _load(self) -> None:
        """Load history from file."""
        if self.history_file.exists():
            try:
                data = json.loads(self.history_file.read_text())
                self.messages = [ConversationMessage.from_dict(m) for m in data.get("messages", [])]
            except (json.JSONDecodeError, KeyError):
                self.messages = []

    def _save(self) -> None:
        """Save history to file."""
        self.history_file.parent.mkdir(parents=True, exist_ok=True)
        data = {"messages": [m.to_dict() for m in self.messages]}
        self.history_file.write_text(json.dumps(data, indent=2))

    def add_message(self, role: str, content: str) -> None:
        """Add a message and persist."""
        # Skip empty or system status messages
        if not content.strip() or content in ["...", "[dim]...[/]"]:
            return
        # Skip duplicate consecutive messages
        if self.messages and self.messages[-1].content == content:
            return
        self.messages.append(ConversationMessage(role=role, content=content))
        self._save()

    def get_recent(self, limit: int = 50) -> List[ConversationMessage]:
        """Get most recent messages."""
        if limit is None:
            return list(self.messages)
        if limit <= 0:
            return []
        if limit >= len(self.messages):
            return list(self.messages)
        return self.messages[-limit:]

    def clear(self) -> None:
        """Clear all history."""
        if not self.messages and not self.history_file.exists():
            return
        self.messages = []
        self._save()

    def start_new_session(self) -> None:
        """Mark the start of a new session with a separator."""
        if self.messages:
            self.messages.append(ConversationMessage(
                role="system",
                content="--- New Session ---"
            ))
            self._save()


@dataclass
class AgentHandle:
    """Handle to a running or completed repair agent."""

    id: str
    issue_type: str
    target_path: str
    symbol: str
    status: str = "running"  # running, completed, failed, timeout
    output_buffer: List[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    process: Optional[asyncio.subprocess.Process] = None
    error: Optional[str] = None

    @property
    def duration(self) -> float:
        """Get duration in seconds."""
        return max(0.0, time.time() - self.start_time)

    @property
    def is_active(self) -> bool:
        """Check if agent is still running."""
        if self.status != "running":
            return False
        if self.process and self.process.returncode is not None:
            return False
        return True

    def append_output(self, text: str) -> None:
        """Append text to output buffer."""
        if not text:
            return
        self.output_buffer.append(text)

    def get_output(self) -> str:
        """Get full output as string."""
        if not self.output_buffer:
            return ""
        return "\n".join(self.output_buffer)


@dataclass
class SessionState:
    """
    Central state for the TUI session.

    Holds health score, active agents, and message history.
    Single source of truth for app state.
    """

    health_score: int = 0
    running: bool = True
    active_agents: List[AgentHandle] = field(default_factory=list)
    manager_messages: List[str] = field(default_factory=list)
    last_command: Optional[str] = None

    def add_agent(self, agent: AgentHandle) -> None:
        """Add an agent to active list."""
        for i, existing in enumerate(self.active_agents):
            if existing.id == agent.id:
                self.active_agents[i] = agent
                return
        self.active_agents.append(agent)

    def remove_agent(self, agent_id: str) -> Optional[AgentHandle]:
        """Remove and return an agent by ID."""
        for i, agent in enumerate(self.active_agents):
            if agent.id == agent_id:
                return self.active_agents.pop(i)
        return None

    def get_agent(self, agent_id: str) -> Optional[AgentHandle]:
        """Get an agent by ID."""
        for agent in self.active_agents:
            if agent.id == agent_id:
                return agent
        return None

    def add_manager_message(self, message: str) -> None:
        """Add a message to manager history."""
        if not message or not message.strip():
            return
        if self.manager_messages and self.manager_messages[-1] == message:
            return
        self.manager_messages.append(message)

    @property
    def active_count(self) -> int:
        """Count of currently running agents."""
        count = 0
        for agent in self.active_agents:
            if agent.is_active:
                count += 1
        return count

    def clear_completed(self) -> List[AgentHandle]:
        """Remove and return all completed agents."""
        completed = [a for a in self.active_agents if not a.is_active]
        self.active_agents = [a for a in self.active_agents if a.is_active]
        return completed
