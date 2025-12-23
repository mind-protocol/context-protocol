"""
Connectome Session State

Tracks dialogue progress, collected answers, and accumulated context.
"""

import uuid
from enum import Enum
from datetime import datetime
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


class SessionStatus(Enum):
    """Session lifecycle states."""
    ACTIVE = "active"
    COMPLETE = "complete"
    ABORTED = "aborted"
    ERROR = "error"


@dataclass
class LoopState:
    """State for for_each loops."""
    step_id: str
    items: List[Any]
    index: int = 0
    results: List[Any] = field(default_factory=list)

    @property
    def current_item(self) -> Any:
        """Get current item in loop."""
        if self.index < len(self.items):
            return self.items[self.index]
        return None

    @property
    def is_complete(self) -> bool:
        """Check if loop is done."""
        return self.index >= len(self.items)

    def advance(self, result: Any = None) -> None:
        """Move to next item."""
        if result is not None:
            self.results.append(result)
        self.index += 1


@dataclass
class SessionState:
    """
    Complete state for a connectome dialogue session.

    Attributes:
        id: Unique session identifier
        connectome_name: Which connectome is running
        started_at: When session began
        current_step: Current step ID
        status: Session lifecycle status
        collected: Answers from ask steps (step_id -> value)
        context: Results from query steps (store_as -> data)
        loop_state: Current loop if in for_each
        created_nodes: Nodes created during session
        created_links: Links created during session
        error: Error message if status is ERROR
    """
    id: str
    connectome_name: str
    started_at: datetime
    current_step: str
    status: SessionStatus = SessionStatus.ACTIVE
    collected: Dict[str, Any] = field(default_factory=dict)
    context: Dict[str, Any] = field(default_factory=dict)
    loop_state: Optional[LoopState] = None
    created_nodes: List[Dict[str, Any]] = field(default_factory=list)
    created_links: List[Dict[str, Any]] = field(default_factory=list)
    error: Optional[str] = None

    @classmethod
    def create(cls, connectome_name: str, start_step: str) -> "SessionState":
        """Create a new session."""
        return cls(
            id=str(uuid.uuid4()),
            connectome_name=connectome_name,
            started_at=datetime.utcnow(),
            current_step=start_step,
        )

    def set_answer(self, step_id: str, value: Any) -> None:
        """Store answer from an ask step."""
        self.collected[step_id] = value

    def get_answer(self, step_id: str) -> Any:
        """Retrieve answer from a previous ask step."""
        return self.collected.get(step_id)

    def set_context(self, key: str, data: Any) -> None:
        """Store query results in context."""
        self.context[key] = data

    def get_context(self, key: str) -> Any:
        """Retrieve query results from context."""
        return self.context.get(key)

    def add_created_node(self, node: Dict[str, Any]) -> None:
        """Record a created node."""
        self.created_nodes.append(node)

    def add_created_link(self, link: Dict[str, Any]) -> None:
        """Record a created link."""
        self.created_links.append(link)

    def complete(self) -> None:
        """Mark session as complete."""
        self.status = SessionStatus.COMPLETE

    def abort(self) -> None:
        """Mark session as aborted."""
        self.status = SessionStatus.ABORTED

    def set_error(self, message: str) -> None:
        """Mark session as error with message."""
        self.status = SessionStatus.ERROR
        self.error = message

    def to_dict(self) -> Dict[str, Any]:
        """Serialize session state."""
        return {
            "id": self.id,
            "connectome_name": self.connectome_name,
            "started_at": self.started_at.isoformat(),
            "current_step": self.current_step,
            "status": self.status.value,
            "collected": self.collected,
            "context": self.context,
            "loop_state": {
                "step": self.loop_state.step_id,
                "items": self.loop_state.items,
                "index": self.loop_state.index,
                "results": self.loop_state.results,
            } if self.loop_state else None,
            "created_nodes": self.created_nodes,
            "created_links": self.created_links,
            "error": self.error,
        }
