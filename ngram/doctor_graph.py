"""
Doctor Graph Operations — Issue and Task Narrative Node Management

Creates, updates, and traverses issue/task narrative nodes in the graph.
Follows canonical schema v1.2:
- Issues, Objectives, Tasks are Narrative nodes with type attribute
- Modules are Space nodes
- Files are Thing nodes
- Links use relates with direction/role properties

Flow:
1. Surface issues from checks → create Narrative nodes (type: issue)
2. Traverse up from issues → find Narrative nodes (type: objective)
3. Create Narrative nodes (type: task) grouping issues

DOCS: docs/protocol/doctor/ALGORITHM_Project_Health_Doctor.md
"""

import hashlib
import time
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Set, Tuple


# =============================================================================
# SCHEMA-ALIGNED ENUMS
# =============================================================================

class NodeType(Enum):
    """Canonical node types from schema v1.2."""
    ACTOR = "actor"
    SPACE = "space"
    THING = "thing"
    NARRATIVE = "narrative"
    MOMENT = "moment"


class NarrativeSubtype(Enum):
    """Narrative type values for doctor system."""
    ISSUE = "issue"
    OBJECTIVE = "objective"
    TASK = "task"
    PATTERN = "pattern"
    VALIDATION = "validation"


class LinkType(Enum):
    """Canonical link types from schema v1.2."""
    CONTAINS = "contains"       # Space → Space/Actor/Thing
    LEADS_TO = "leads_to"       # Space → Space
    EXPRESSES = "expresses"     # Actor → Moment
    SEQUENCE = "sequence"       # Moment → Moment
    PRIMES = "primes"           # Moment → Moment
    CAN_BECOME = "can_become"   # Thing → Thing
    RELATES = "relates"         # Any → Any (energy carrier)
    ABOUT = "about"             # Moment → Any
    ATTACHED_TO = "attached_to" # Thing → Actor/Space


class RelatesDirection(Enum):
    """Direction values for relates links."""
    SUPPORT = "support"
    OPPOSE = "oppose"
    ELABORATE = "elaborate"
    SUBSUME = "subsume"
    SUPERSEDE = "supersede"


class TraversalOutcome(Enum):
    """Result of traversing from issue up to objective."""
    SERVE = "serve"              # Found objective → normal task
    RECONSTRUCT = "reconstruct"  # Missing nodes in chain → rebuild
    TRIAGE = "triage"            # No objective defined → evaluate usefulness


# =============================================================================
# SCHEMA-ALIGNED NODE STRUCTURES
# =============================================================================

@dataclass
class GraphNode:
    """Base node following schema v1.2 NodeBase."""
    id: str
    name: str
    node_type: str              # actor, space, thing, narrative, moment
    type: str                   # Subtype within node_type (free string)
    description: str = ""
    weight: float = 1.0         # Importance/inertia (unbounded)
    energy: float = 0.0         # Instantaneous activation (unbounded)
    created_at_s: int = 0
    updated_at_s: int = 0

    # Extended fields (stored in properties for flexibility)
    properties: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        now = int(time.time())
        if not self.created_at_s:
            self.created_at_s = now
        if not self.updated_at_s:
            self.updated_at_s = now


@dataclass
class NarrativeNode(GraphNode):
    """Narrative node with content field."""
    content: str = ""

    def __post_init__(self):
        self.node_type = NodeType.NARRATIVE.value
        super().__post_init__()


@dataclass
class SpaceNode(GraphNode):
    """Space node for modules/containers."""

    def __post_init__(self):
        self.node_type = NodeType.SPACE.value
        super().__post_init__()


@dataclass
class ThingNode(GraphNode):
    """Thing node for files/artifacts."""
    uri: str = ""  # File path, URL, etc.

    def __post_init__(self):
        self.node_type = NodeType.THING.value
        super().__post_init__()


@dataclass
class GraphLink:
    """Link following schema v1.2 LinkBase."""
    id: str
    node_a: str                 # First endpoint
    node_b: str                 # Second endpoint
    type: str                   # Link type from LinkType enum

    # Physics properties
    conductivity: float = 0.5
    weight: float = 1.0
    energy: float = 0.0
    strength: float = 0.0

    # Semantic properties
    name: str = ""
    role: Optional[str] = None  # originator, believer, witness, subject, creditor, debtor
    direction: Optional[str] = None  # support, oppose, elaborate, subsume, supersede
    description: str = ""
    created_at_s: int = 0

    def __post_init__(self):
        if not self.created_at_s:
            self.created_at_s = int(time.time())
        if not self.id:
            self.id = f"link_{self.node_a}_{self.node_b}_{self.type}"


# =============================================================================
# ISSUE NARRATIVE NODE
# =============================================================================

@dataclass
class IssueNarrative(NarrativeNode):
    """
    Narrative node with type='issue'.

    Represents an atomic problem detected by doctor.
    """
    issue_type: str = ""          # MONOLITH, STALE_SYNC, etc.
    severity: str = "warning"     # critical, warning, info
    status: str = "open"          # open, resolved, in_progress
    module: str = ""              # Module ID (Space it belongs to)
    path: str = ""                # File/dir path
    message: str = ""             # Human description
    detected_at: str = ""
    resolved_at: Optional[str] = None

    def __post_init__(self):
        self.type = NarrativeSubtype.ISSUE.value
        if not self.detected_at:
            self.detected_at = datetime.now().isoformat()
        super().__post_init__()
        # Map severity to energy (higher severity = more energy)
        self.energy = {"critical": 1.0, "warning": 0.5, "info": 0.2}.get(self.severity, 0.3)


@dataclass
class ObjectiveNarrative(NarrativeNode):
    """
    Narrative node with type='objective'.

    Represents a goal for a module.
    """
    objective_type: str = ""      # documented, maintainable, tested, etc.
    module: str = ""              # Module ID (Space it belongs to)
    status: str = "open"          # open, achieved, deferred, deprecated
    criteria: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = NarrativeSubtype.OBJECTIVE.value
        super().__post_init__()


@dataclass
class TaskNarrative(NarrativeNode):
    """
    Narrative node with type='task'.

    Groups issues serving an objective.
    """
    task_type: str = "serve"      # serve, reconstruct, triage
    objective_id: Optional[str] = None
    module: str = ""
    skill: str = ""               # Skill to resolve this task
    status: str = "open"          # open, in_progress, completed
    issue_ids: List[str] = field(default_factory=list)
    missing_nodes: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.type = NarrativeSubtype.TASK.value
        super().__post_init__()


@dataclass
class TraversalResult:
    """Result of traversing from issue to objective."""
    outcome: TraversalOutcome
    objective: Optional[ObjectiveNarrative] = None
    space_id: Optional[str] = None
    missing_nodes: List[str] = field(default_factory=list)
    path: List[str] = field(default_factory=list)


# =============================================================================
# ID GENERATION
# =============================================================================
#
# Convention:
#   {node-type}_{SUBTYPE}_{instance-context}_{disambiguator}
#
# - node-type: lowercase (low info, you already know it)
# - SUBTYPE: ALLCAPS (high info, what you scan for)
# - instance-context: lowercase, `-` between words (which one)
# - disambiguator: lowercase 2-char hash or index (collision safety)
#
# Examples:
#   narrative_ISSUE_monolith-engine-physics-graph-ops_a7
#   narrative_TASK_serve-engine-physics-documented_01
#   narrative_OBJECTIVE_engine-physics-documented
#   space_MODULE_engine-physics
#   thing_FILE_engine-physics-graph-ops_a7
#   moment_TICK_1000_a7
#


def _clean_for_id(s: str) -> str:
    """Clean string for use in ID: lowercase, replace _ and / with -."""
    return s.lower().replace("_", "-").replace("/", "-").replace(" ", "-")


def generate_space_id(module: str, space_type: str = "MODULE") -> str:
    """Generate space ID.

    Format: space_{SUBTYPE}_{instance}
    Example: space_MODULE_engine-physics
    """
    clean_module = _clean_for_id(module)
    return f"space_{space_type.upper()}_{clean_module}"


def generate_thing_id(path: str, thing_type: str = "FILE") -> str:
    """Generate thing ID for a file/artifact.

    Format: thing_{SUBTYPE}_{instance}_{hash}
    Example: thing_FILE_engine-physics-graph-ops_a7
    """
    # Convert path to dashed format
    clean_path = _clean_for_id(Path(path).stem)
    # Add parent dir for context if available
    parent = Path(path).parent.name
    if parent and parent != ".":
        clean_path = f"{_clean_for_id(parent)}-{clean_path}"
    short_hash = hashlib.md5(path.encode()).hexdigest()[:2]
    return f"thing_{thing_type.upper()}_{clean_path}_{short_hash}"


def generate_actor_id(name: str, actor_type: str = "AGENT") -> str:
    """Generate actor ID.

    Format: actor_{SUBTYPE}_{instance}
    Example: actor_AGENT_claude
    """
    clean_name = _clean_for_id(name)
    return f"actor_{actor_type.upper()}_{clean_name}"


def generate_issue_id(issue_type: str, module: str, path: str) -> str:
    """Generate issue narrative ID.

    Format: narrative_ISSUE_{issue-type}-{module}-{file}_{hash}
    Example: narrative_ISSUE_monolith-engine-physics-graph-ops_a7
    """
    file_stem = Path(path).stem if path else "root"
    clean_type = _clean_for_id(issue_type)
    clean_module = _clean_for_id(module)
    clean_file = _clean_for_id(file_stem)

    # Build context: type-module-file
    context = f"{clean_type}-{clean_module}-{clean_file}"

    hash_input = f"{issue_type}:{module}:{path}"
    short_hash = hashlib.md5(hash_input.encode()).hexdigest()[:2]

    return f"narrative_ISSUE_{context}_{short_hash}"


def generate_objective_id(objective_type: str, module: str) -> str:
    """Generate objective narrative ID.

    Format: narrative_OBJECTIVE_{module}-{type}
    Example: narrative_OBJECTIVE_engine-physics-documented
    """
    clean_module = _clean_for_id(module)
    clean_type = _clean_for_id(objective_type)
    return f"narrative_OBJECTIVE_{clean_module}-{clean_type}"


def generate_task_id(task_type: str, module: str, objective_type: str = "", index: int = 1) -> str:
    """Generate task narrative ID.

    Format: narrative_TASK_{task-type}-{module}-{objective}_{index}
    Example: narrative_TASK_serve-engine-physics-documented_01
    """
    clean_task = _clean_for_id(task_type)
    clean_module = _clean_for_id(module)

    if objective_type:
        clean_obj = _clean_for_id(objective_type)
        context = f"{clean_task}-{clean_module}-{clean_obj}"
    else:
        context = f"{clean_task}-{clean_module}"

    return f"narrative_TASK_{context}_{index:02d}"


def generate_moment_id(moment_type: str, context: str, tick: int = 0) -> str:
    """Generate moment ID.

    Format: moment_{SUBTYPE}_{context}_{hash}
    Example: moment_TICK_1000_a7
             moment_EXPLORATION_physics-state_x8
    """
    if tick > 0:
        return f"moment_{moment_type.upper()}_{tick}_{hashlib.md5(context.encode()).hexdigest()[:2]}"

    clean_context = _clean_for_id(context)
    short_hash = hashlib.md5(f"{moment_type}:{context}".encode()).hexdigest()[:2]
    return f"moment_{moment_type.upper()}_{clean_context}_{short_hash}"


def generate_link_id(link_type: str, from_id: str, to_id: str, semantic_name: str = "") -> str:
    """Generate link ID.

    Format: {link-type}_{SEMANTIC}_{from-short}_TO_{to-short}
    Example: relates_BLOCKS_narrative-issue-a7_TO_narrative-objective-b3
    """
    # Extract short form from node IDs (last two parts)
    from_parts = from_id.split("_")
    to_parts = to_id.split("_")
    from_short = "-".join(from_parts[-2:]) if len(from_parts) >= 2 else from_id
    to_short = "-".join(to_parts[-2:]) if len(to_parts) >= 2 else to_id

    if semantic_name:
        return f"{link_type.lower()}_{semantic_name.upper()}_{from_short}_TO_{to_short}"
    return f"{link_type.lower()}_{from_short}_TO_{to_short}"


# =============================================================================
# ISSUE TYPE → OBJECTIVE TYPE MAPPING
# =============================================================================

ISSUE_BLOCKS_OBJECTIVE: Dict[str, List[str]] = {
    # Documentation issues → documented
    "UNDOCUMENTED": ["documented"],
    "INCOMPLETE_CHAIN": ["documented"],
    "PLACEHOLDER": ["documented"],
    "DOC_TEMPLATE_DRIFT": ["documented"],
    "NO_DOCS_REF": ["documented"],
    "BROKEN_IMPL_LINK": ["documented"],
    "ORPHAN_DOCS": ["documented"],
    "NON_STANDARD_DOC_TYPE": ["documented"],
    "DOC_DUPLICATION": ["documented"],
    "UNDOC_IMPL": ["documented"],
    "NEW_UNDOC_CODE": ["documented"],
    "HOOK_UNDOC": ["documented"],
    "DOC_LINK_INTEGRITY": ["documented"],

    # Sync issues → synced
    "STALE_SYNC": ["synced"],
    "STALE_IMPL": ["synced"],
    "CODE_DOC_DELTA_COUPLING": ["synced"],
    "DOC_GAPS": ["synced"],

    # Code quality issues → maintainable
    "MONOLITH": ["maintainable"],
    "STUB_IMPL": ["maintainable"],
    "INCOMPLETE_IMPL": ["maintainable"],
    "NAMING_CONVENTION": ["maintainable"],
    "MAGIC_VALUES": ["maintainable"],
    "HARDCODED_CONFIG": ["maintainable"],
    "LONG_PROMPT": ["maintainable"],
    "LONG_SQL": ["maintainable"],
    "LEGACY_MARKER": ["maintainable"],
    "PROMPT_DOC_REFERENCE": ["maintainable"],
    "PROMPT_VIEW_TABLE": ["maintainable"],
    "PROMPT_CHECKLIST": ["maintainable"],

    # Test issues → tested
    "MISSING_TESTS": ["tested"],
    "TEST_FAILED": ["tested"],
    "TEST_ERROR": ["tested"],
    "TEST_TIMEOUT": ["tested"],
    "INVARIANT_UNTESTED": ["tested"],
    "TEST_NO_VALIDATES": ["tested"],

    # Health issues → healthy
    "HEALTH_FAILED": ["healthy"],
    "INVARIANT_VIOLATED": ["healthy"],
    "INVARIANT_NO_TEST": ["healthy"],
    "VALIDATION_BEHAVIORS_MISSING": ["healthy"],
    "CONFIG_MISSING": ["healthy"],
    "LOG_ERROR": ["healthy"],
    "MEMBRANE_NO_PROTOCOLS": ["healthy"],
    "MEMBRANE_IMPORT_ERROR": ["healthy"],
    "MEMBRANE_SESSION_INVALID": ["healthy"],
    "MEMBRANE_STEP_ORDERING": ["healthy"],
    "MEMBRANE_EMPTY_PROTOCOL": ["healthy"],
    "MEMBRANE_MISSING_FIELDS": ["healthy"],
    "MEMBRANE_INVALID_STEP": ["healthy"],
    "MEMBRANE_BRANCH_NO_CHECKS": ["healthy"],
    "MEMBRANE_YAML_ERROR": ["healthy"],
    "MEMBRANE_PARSE_ERROR": ["healthy"],

    # Review issues → resolved
    "ESCALATION": ["resolved"],
    "SUGGESTION": ["resolved"],
    "UNRESOLVED_QUESTION": ["resolved"],

    # Security issues → secure
    "HARDCODED_SECRET": ["secure"],

    # Module status
    "MODULE_INCOMPLETE": ["documented", "tested"],
    "MODULE_BLOCKED": ["resolved"],
    "YAML_DRIFT": ["documented"],
    "COMPONENT_NO_STORIES": ["documented"],
}


OBJECTIVE_TO_SKILL: Dict[str, str] = {
    "documented": "create_module_documentation",
    "synced": "update_module_sync_state",
    "maintainable": "implement_write_or_modify_code",
    "tested": "test_integrate_and_gate",
    "healthy": "health_define_and_verify",
    "resolved": "review_evaluate_changes",
    "secure": "implement_write_or_modify_code",
}


STANDARD_OBJECTIVE_TYPES = ["documented", "synced", "maintainable", "tested", "healthy", "secure", "resolved"]


# =============================================================================
# GRAPH STORE (Schema-aligned)
# =============================================================================

class DoctorGraphStore:
    """
    Graph store for doctor nodes and links.

    Follows schema v1.2:
    - Nodes have node_type (actor/space/thing/narrative/moment) and type (subtype)
    - Links use canonical types with semantic properties (role, direction)
    """

    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.links: List[GraphLink] = []
        self._links_by_from: Dict[str, List[GraphLink]] = {}
        self._links_by_to: Dict[str, List[GraphLink]] = {}

    def upsert_node(self, node: GraphNode) -> bool:
        """Create or update a node. Returns True if created, False if updated."""
        is_new = node.id not in self.nodes
        node.updated_at_s = int(time.time())
        self.nodes[node.id] = node
        return is_new

    def get_node(self, node_id: str) -> Optional[GraphNode]:
        """Get node by ID."""
        return self.nodes.get(node_id)

    def query_nodes(
        self,
        node_type: Optional[str] = None,
        subtype: Optional[str] = None,
        **kwargs
    ) -> List[GraphNode]:
        """Query nodes by node_type and subtype (type field)."""
        results = []
        for node in self.nodes.values():
            if node_type and node.node_type != node_type:
                continue
            if subtype and node.type != subtype:
                continue
            # Additional property filters
            match = True
            for k, v in kwargs.items():
                if hasattr(node, k) and getattr(node, k) != v:
                    match = False
                    break
            if match:
                results.append(node)
        return results

    def create_link(self, link: GraphLink) -> None:
        """Create a link between nodes."""
        # Avoid duplicates (same endpoints + type)
        for existing in self.links:
            if (existing.node_a == link.node_a and
                existing.node_b == link.node_b and
                existing.type == link.type):
                return

        self.links.append(link)
        self._links_by_from.setdefault(link.node_a, []).append(link)
        self._links_by_to.setdefault(link.node_b, []).append(link)

    def get_links_from(self, node_id: str, link_type: Optional[str] = None) -> List[GraphLink]:
        """Get outgoing links from a node (node_a = node_id)."""
        links = self._links_by_from.get(node_id, [])
        if link_type:
            links = [l for l in links if l.type == link_type]
        return links

    def get_links_to(self, node_id: str, link_type: Optional[str] = None) -> List[GraphLink]:
        """Get incoming links to a node (node_b = node_id)."""
        links = self._links_by_to.get(node_id, [])
        if link_type:
            links = [l for l in links if l.type == link_type]
        return links

    def delete_node(self, node_id: str) -> bool:
        """Delete a node and its links."""
        if node_id not in self.nodes:
            return False

        del self.nodes[node_id]

        # Remove links
        self.links = [l for l in self.links
                      if l.node_a != node_id and l.node_b != node_id]
        self._links_by_from.pop(node_id, None)
        self._links_by_to.pop(node_id, None)

        return True


# =============================================================================
# NODE CREATION HELPERS
# =============================================================================

def create_issue_node(
    issue_type: str,
    severity: str,
    path: str,
    message: str,
    module: str,
    details: Optional[Dict[str, Any]] = None,
) -> IssueNarrative:
    """Create an issue narrative node with full content.

    ID format: narrative_ISSUE_{type}-{module}-{file}_{hash}
    Example: narrative_ISSUE_monolith-engine-physics-graph-ops_a7
    """
    issue_id = generate_issue_id(issue_type, module, path)
    file_stem = Path(path).stem if path else "root"

    # Build rich content
    content_lines = [
        f"## {issue_type}",
        f"",
        f"**Module:** {module}",
        f"**File:** {path}" if path else "**Scope:** module-level",
        f"**Severity:** {severity}",
        f"",
        f"### Description",
        message,
    ]

    if details:
        content_lines.extend([
            "",
            "### Details",
            "```yaml",
        ])
        for k, v in details.items():
            content_lines.append(f"{k}: {v}")
        content_lines.append("```")

    content = "\n".join(content_lines)

    return IssueNarrative(
        id=issue_id,
        name=f"{issue_type} in {module}/{file_stem}",
        content=content,
        description=message,
        issue_type=issue_type,
        severity=severity,
        module=module,
        path=path,
        message=message,
        properties={"details": details or {}}
    )


def create_objective_node(objective_type: str, module: str) -> ObjectiveNarrative:
    """Create an objective narrative node with full content.

    ID format: narrative_OBJECTIVE_{module}-{type}
    Example: narrative_OBJECTIVE_engine-physics-documented
    """
    obj_id = generate_objective_id(objective_type, module)

    # Build rich content describing the objective
    criteria = {
        "documented": [
            "Module is mapped in modules.yaml",
            "Doc chain exists: PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, HEALTH, SYNC",
            "All code files have DOCS: references",
            "No placeholder content in docs",
        ],
        "synced": [
            "SYNC file updated within 14 days",
            "IMPLEMENTATION doc reflects current code",
            "No code changes without doc updates",
        ],
        "maintainable": [
            "No files over 800 lines",
            "No functions over 100 lines",
            "Naming conventions followed",
            "No magic values or hardcoded config",
        ],
        "tested": [
            "Test coverage exists",
            "All tests passing",
            "Invariants have test coverage",
        ],
        "healthy": [
            "Health signals defined and passing",
            "No errors in logs",
            "Invariants not violated",
        ],
        "secure": [
            "No hardcoded secrets",
            "No exposed credentials",
        ],
        "resolved": [
            "No open escalations",
            "No unresolved questions",
            "No pending suggestions",
        ],
    }

    obj_criteria = criteria.get(objective_type, [f"All {objective_type} issues resolved"])

    content_lines = [
        f"## Objective: {module} is {objective_type}",
        "",
        "### Criteria",
    ]
    for c in obj_criteria:
        content_lines.append(f"- [ ] {c}")

    content = "\n".join(content_lines)

    return ObjectiveNarrative(
        id=obj_id,
        name=f"{module} is {objective_type}",
        content=content,
        description=f"Objective: module {module} achieves {objective_type} status",
        objective_type=objective_type,
        module=module,
        criteria=obj_criteria
    )


def create_task_node(
    task_type: str,
    module: str,
    skill: str,
    issue_ids: List[str],
    objective_id: Optional[str] = None,
    objective_type: str = "",
    index: int = 1,
    missing_nodes: Optional[List[str]] = None
) -> TaskNarrative:
    """Create a task narrative node with full content.

    ID format: narrative_TASK_{type}-{module}-{objective}_{index}
    Example: narrative_TASK_serve-engine-physics-documented_01
    """
    task_id = generate_task_id(task_type, module, objective_type, index)

    # Build rich content based on task type
    if task_type == "serve":
        name = f"Serve {objective_type} for {module}"
        content_lines = [
            f"## Task: {name}",
            "",
            f"**Type:** serve",
            f"**Module:** {module}",
            f"**Objective:** {objective_id or objective_type}",
            f"**Skill:** {skill}",
            "",
            f"### Issues ({len(issue_ids)})",
        ]
        for iid in issue_ids:
            content_lines.append(f"- [ ] `{iid}`")

    elif task_type == "reconstruct":
        name = f"Reconstruct chain for {module}"
        content_lines = [
            f"## Task: {name}",
            "",
            f"**Type:** reconstruct",
            f"**Module:** {module}",
            f"**Skill:** {skill}",
            "",
            "### Missing Nodes",
        ]
        for node in (missing_nodes or []):
            content_lines.append(f"- {node}")
        content_lines.extend([
            "",
            "### Steps",
            "1. Create missing Space/docs nodes",
            "2. Establish links",
            "3. Re-run doctor to verify",
            "",
            f"### Related Issues ({len(issue_ids)})",
        ])
        for iid in issue_ids:
            content_lines.append(f"- `{iid}`")

    else:  # triage
        name = f"Triage orphan code: {module}"
        content_lines = [
            f"## Task: {name}",
            "",
            f"**Type:** triage",
            f"**Module:** {module}",
            f"**Skill:** {skill}",
            "",
            "### Decision Required",
            "No objective defined for this code. Evaluate:",
            "- **integrate**: Move to existing module",
            "- **create_module**: Define new module with objectives",
            "- **deprecate**: Archive for reference",
            "- **delete**: Remove if unused",
            "",
            "### Investigation",
            "- [ ] Check if code is imported elsewhere",
            "- [ ] Check git history for recent activity",
            "- [ ] Check for existing tests",
            "",
            f"### Related Issues ({len(issue_ids)})",
        ]
        for iid in issue_ids:
            content_lines.append(f"- `{iid}`")

    content = "\n".join(content_lines)

    return TaskNarrative(
        id=task_id,
        name=name,
        content=content,
        description=content_lines[0].replace("## Task: ", ""),
        task_type=task_type,
        objective_id=objective_id,
        module=module,
        skill=skill,
        issue_ids=issue_ids,
        missing_nodes=missing_nodes or []
    )


def create_space_node(module: str, space_type: str = "MODULE", description: str = "") -> SpaceNode:
    """Create a space node for a module.

    ID format: space_{SUBTYPE}_{instance}
    Example: space_MODULE_engine-physics
    """
    space_id = generate_space_id(module, space_type)

    return SpaceNode(
        id=space_id,
        name=module,
        node_type=NodeType.SPACE.value,  # Will be set by __post_init__ but needed for dataclass
        type=space_type.lower(),
        description=description or f"Module: {module}"
    )


def create_thing_node(path: str, thing_type: str = "FILE", description: str = "") -> ThingNode:
    """Create a thing node for a file.

    ID format: thing_{SUBTYPE}_{instance}_{hash}
    Example: thing_FILE_engine-physics-graph-ops_a7
    """
    thing_id = generate_thing_id(path, thing_type)

    return ThingNode(
        id=thing_id,
        name=Path(path).name,
        node_type=NodeType.THING.value,  # Will be set by __post_init__ but needed for dataclass
        type=thing_type.lower(),
        uri=path,
        description=description or f"File: {path}"
    )


# =============================================================================
# LINK CREATION HELPERS
# =============================================================================

def link_space_contains(space_id: str, node_id: str) -> GraphLink:
    """Create contains link: Space → Node.

    Example ID: contains_space-module-engine-physics_TO_narrative-issue-a7
    """
    link_id = generate_link_id(LinkType.CONTAINS.value, space_id, node_id)
    return GraphLink(
        id=link_id,
        node_a=space_id,
        node_b=node_id,
        type=LinkType.CONTAINS.value,
        name="contains",
        description=f"Space contains {node_id.split('_')[1] if '_' in node_id else 'node'}"
    )


def link_issue_blocks_objective(issue_id: str, objective_id: str) -> GraphLink:
    """Create relates link with direction=oppose: Issue blocks Objective.

    Example ID: relates_BLOCKS_narrative-issue-a7_TO_narrative-objective-b3
    """
    link_id = generate_link_id(LinkType.RELATES.value, issue_id, objective_id, "BLOCKS")
    return GraphLink(
        id=link_id,
        node_a=issue_id,
        node_b=objective_id,
        type=LinkType.RELATES.value,
        name="blocks",
        direction=RelatesDirection.OPPOSE.value,
        description="Issue blocking objective achievement"
    )


def link_task_serves_objective(task_id: str, objective_id: str) -> GraphLink:
    """Create relates link with direction=support: Task serves Objective.

    Example ID: relates_SERVES_narrative-task-01_TO_narrative-objective-b3
    """
    link_id = generate_link_id(LinkType.RELATES.value, task_id, objective_id, "SERVES")
    return GraphLink(
        id=link_id,
        node_a=task_id,
        node_b=objective_id,
        type=LinkType.RELATES.value,
        name="serves",
        direction=RelatesDirection.SUPPORT.value,
        description="Task working toward objective"
    )


def link_task_includes_issue(task_id: str, issue_id: str) -> GraphLink:
    """Create relates link: Task includes Issue.

    Example ID: relates_INCLUDES_narrative-task-01_TO_narrative-issue-a7
    """
    link_id = generate_link_id(LinkType.RELATES.value, task_id, issue_id, "INCLUDES")
    return GraphLink(
        id=link_id,
        node_a=task_id,
        node_b=issue_id,
        type=LinkType.RELATES.value,
        name="includes",
        direction=RelatesDirection.SUBSUME.value,
        description="Task includes this issue"
    )


def link_issue_about_thing(issue_id: str, thing_id: str) -> GraphLink:
    """Create relates link: Issue is about Thing.

    Example ID: relates_ABOUT_narrative-issue-a7_TO_thing-file-b3
    """
    link_id = generate_link_id(LinkType.RELATES.value, issue_id, thing_id, "ABOUT")
    return GraphLink(
        id=link_id,
        node_a=issue_id,
        node_b=thing_id,
        type=LinkType.RELATES.value,
        name="about",
        description="Issue concerns this file/artifact"
    )


# =============================================================================
# GRAPH OPERATIONS
# =============================================================================

def upsert_issue(
    issue_type: str,
    severity: str,
    path: str,
    message: str,
    module: str,
    store: DoctorGraphStore,
    details: Optional[Dict[str, Any]] = None,
) -> IssueNarrative:
    """
    Create or update an issue narrative node.

    If exists: update severity, message, detected_at
    If new: create with links to space and thing
    """
    issue_id = generate_issue_id(issue_type, module, path)
    existing = store.get_node(issue_id)

    if existing and isinstance(existing, IssueNarrative):
        # Update existing - rebuild full content
        existing.severity = severity
        existing.message = message
        existing.detected_at = datetime.now().isoformat()
        existing.status = "open"
        existing.properties["details"] = details or {}
        existing.energy = {"critical": 1.0, "warning": 0.5, "info": 0.2}.get(severity, 0.3)

        # Rebuild rich content
        content_lines = [
            f"## {issue_type}",
            "",
            f"**Module:** {module}",
            f"**File:** {path}" if path else "**Scope:** module-level",
            f"**Severity:** {severity}",
            "",
            "### Description",
            message,
        ]
        if details:
            content_lines.extend(["", "### Details", "```yaml"])
            for k, v in details.items():
                content_lines.append(f"{k}: {v}")
            content_lines.append("```")
        existing.content = "\n".join(content_lines)

        store.upsert_node(existing)
        return existing

    # Create new
    issue = create_issue_node(issue_type, severity, path, message, module, details)
    store.upsert_node(issue)

    # Ensure space exists
    space_id = generate_space_id(module)
    if not store.get_node(space_id):
        space = create_space_node(module)
        store.upsert_node(space)

    # Link space contains issue
    store.create_link(link_space_contains(space_id, issue.id))

    # Link issue about thing (file)
    if path:
        thing_id = generate_thing_id(path)
        if not store.get_node(thing_id):
            thing = create_thing_node(path)
            store.upsert_node(thing)
        store.create_link(link_issue_about_thing(issue.id, thing_id))

    return issue


def resolve_issue(issue_id: str, store: DoctorGraphStore) -> bool:
    """Mark an issue as resolved."""
    issue = store.get_node(issue_id)
    if issue and isinstance(issue, IssueNarrative):
        issue.status = "resolved"
        issue.resolved_at = datetime.now().isoformat()
        issue.energy = 0.0  # No longer active
        store.upsert_node(issue)
        return True
    return False


def ensure_module_objectives(module: str, store: DoctorGraphStore) -> List[ObjectiveNarrative]:
    """Ensure standard objectives exist for a module."""
    objectives = []
    space_id = generate_space_id(module)

    # Ensure space exists
    if not store.get_node(space_id):
        space = create_space_node(module)
        store.upsert_node(space)

    for obj_type in STANDARD_OBJECTIVE_TYPES:
        obj_id = generate_objective_id(obj_type, module)
        existing = store.get_node(obj_id)

        if existing and isinstance(existing, ObjectiveNarrative):
            objectives.append(existing)
        else:
            obj = create_objective_node(obj_type, module)
            store.upsert_node(obj)
            store.create_link(link_space_contains(space_id, obj.id))
            objectives.append(obj)

    return objectives


def fetch_objectives(store: DoctorGraphStore, module: Optional[str] = None) -> List[ObjectiveNarrative]:
    """Fetch objective narrative nodes from graph."""
    nodes = store.query_nodes(
        node_type=NodeType.NARRATIVE.value,
        subtype=NarrativeSubtype.OBJECTIVE.value
    )
    objectives = [n for n in nodes if isinstance(n, ObjectiveNarrative)]

    if module:
        objectives = [o for o in objectives if o.module == module]

    return objectives


# =============================================================================
# TRAVERSAL: Issue → Objective
# =============================================================================

def traverse_to_objective(
    issue: IssueNarrative,
    store: DoctorGraphStore,
    modules: Dict[str, Any]
) -> TraversalResult:
    """
    Traverse from issue up to objective.

    Returns TraversalResult with outcome:
    - SERVE: Found objective
    - RECONSTRUCT: Missing nodes in chain
    - TRIAGE: No objective defined
    """
    path = [issue.id]
    missing_nodes = []

    # Step 1: Find space for this module
    space_id = generate_space_id(issue.module)
    space = store.get_node(space_id)

    if not space:
        missing_nodes.append(f"Space:{issue.module}")
    else:
        path.append(space_id)

    # Step 2: Check for documentation chain in module config
    module_info = modules.get(issue.module, {})
    docs_path = module_info.get("docs") if isinstance(module_info, dict) else None

    if docs_path:
        # Check for required doc narrative nodes (PATTERNS, SYNC at minimum)
        for doc_type in ["patterns", "sync"]:
            doc_id = f"narrative_{doc_type}_{issue.module}"
            doc_node = store.get_node(doc_id)
            if not doc_node:
                missing_nodes.append(f"{doc_type.upper()}:{issue.module}")

    # Step 3: Find objective
    objective_types = ISSUE_BLOCKS_OBJECTIVE.get(issue.issue_type, ["documented"])

    objective = None
    for obj_type in objective_types:
        obj_id = generate_objective_id(obj_type, issue.module)
        obj_node = store.get_node(obj_id)
        if obj_node and isinstance(obj_node, ObjectiveNarrative):
            objective = obj_node
            path.append(obj_id)
            break

    # Determine outcome
    if missing_nodes:
        return TraversalResult(
            outcome=TraversalOutcome.RECONSTRUCT,
            space_id=space_id if space else None,
            missing_nodes=missing_nodes,
            path=path
        )
    elif objective:
        return TraversalResult(
            outcome=TraversalOutcome.SERVE,
            objective=objective,
            space_id=space_id,
            path=path
        )
    else:
        return TraversalResult(
            outcome=TraversalOutcome.TRIAGE,
            space_id=space_id if space else None,
            path=path
        )


# =============================================================================
# TASK CREATION FROM ISSUES
# =============================================================================

MAX_ISSUES_PER_TASK = 5


def group_issues_by_outcome(
    issues: List[IssueNarrative],
    store: DoctorGraphStore,
    modules: Dict[str, Any]
) -> Dict[TraversalOutcome, Dict[str, List[Tuple[IssueNarrative, TraversalResult]]]]:
    """Group issues by traversal outcome and module."""
    grouped: Dict[TraversalOutcome, Dict[str, List[Tuple[IssueNarrative, TraversalResult]]]] = {
        TraversalOutcome.SERVE: {},
        TraversalOutcome.RECONSTRUCT: {},
        TraversalOutcome.TRIAGE: {},
    }

    for issue in issues:
        result = traverse_to_objective(issue, store, modules)
        key = issue.module or "orphan"

        if key not in grouped[result.outcome]:
            grouped[result.outcome][key] = []
        grouped[result.outcome][key].append((issue, result))

    return grouped


def create_tasks_from_issues(
    issues: List[IssueNarrative],
    store: DoctorGraphStore,
    modules: Dict[str, Any]
) -> List[TaskNarrative]:
    """
    Create task narrative nodes from issues.

    1. Traverse each issue to objective
    2. Group by outcome and module
    3. Split if too many issues
    4. Create task narrative nodes with proper links
    """
    grouped = group_issues_by_outcome(issues, store, modules)
    tasks: List[TaskNarrative] = []

    # SERVE tasks - group by objective
    for module, issue_results in grouped[TraversalOutcome.SERVE].items():
        by_objective: Dict[str, List[IssueNarrative]] = {}
        for issue, result in issue_results:
            if result.objective:
                obj_id = result.objective.id
                by_objective.setdefault(obj_id, []).append(issue)

        for obj_id, obj_issues in by_objective.items():
            objective = store.get_node(obj_id)
            if not objective or not isinstance(objective, ObjectiveNarrative):
                continue

            skill = OBJECTIVE_TO_SKILL.get(objective.objective_type, "implement_write_or_modify_code")

            # Split if too many
            chunks = [obj_issues[i:i + MAX_ISSUES_PER_TASK]
                      for i in range(0, len(obj_issues), MAX_ISSUES_PER_TASK)]

            for idx, chunk in enumerate(chunks, 1):
                task = create_task_node(
                    task_type="serve",
                    module=module,
                    skill=skill,
                    issue_ids=[i.id for i in chunk],
                    objective_id=obj_id,
                    objective_type=objective.objective_type,
                    index=idx
                )
                store.upsert_node(task)
                tasks.append(task)

                # Links
                store.create_link(link_task_serves_objective(task.id, obj_id))
                for issue in chunk:
                    store.create_link(link_task_includes_issue(task.id, issue.id))
                    store.create_link(link_issue_blocks_objective(issue.id, obj_id))

    # RECONSTRUCT tasks
    for module, issue_results in grouped[TraversalOutcome.RECONSTRUCT].items():
        all_missing: Set[str] = set()
        all_issues: List[IssueNarrative] = []
        for issue, result in issue_results:
            all_missing.update(result.missing_nodes)
            all_issues.append(issue)

        task = create_task_node(
            task_type="reconstruct",
            module=module,
            skill="create_module_documentation",
            issue_ids=[i.id for i in all_issues],
            missing_nodes=list(all_missing)
        )
        store.upsert_node(task)
        tasks.append(task)

        for issue in all_issues:
            store.create_link(link_task_includes_issue(task.id, issue.id))

    # TRIAGE tasks
    for module, issue_results in grouped[TraversalOutcome.TRIAGE].items():
        all_issues = [issue for issue, _ in issue_results]

        task = create_task_node(
            task_type="triage",
            module=module,
            skill="triage_unmapped_code",
            issue_ids=[i.id for i in all_issues]
        )
        store.upsert_node(task)
        tasks.append(task)

        for issue in all_issues:
            store.create_link(link_task_includes_issue(task.id, issue.id))

    return tasks


def update_objective_status(objective_id: str, store: DoctorGraphStore) -> str:
    """Update objective status based on blocking issues."""
    objective = store.get_node(objective_id)
    if not objective or not isinstance(objective, ObjectiveNarrative):
        return "unknown"

    # Find issues blocking this objective via relates links with direction=oppose
    blocking_links = store.get_links_to(objective_id, LinkType.RELATES.value)
    blocking_links = [l for l in blocking_links if l.direction == RelatesDirection.OPPOSE.value]

    open_blockers = 0
    for link in blocking_links:
        issue = store.get_node(link.node_a)
        if issue and isinstance(issue, IssueNarrative) and issue.status == "open":
            open_blockers += 1

    if open_blockers == 0:
        objective.status = "achieved"
    else:
        objective.status = "open"

    store.upsert_node(objective)
    return objective.status


# =============================================================================
# FILE THING NODE OPERATIONS
# =============================================================================

def upsert_file_thing(
    path: str,
    module: str,
    store: DoctorGraphStore,
    file_type: str = "FILE",
) -> ThingNode:
    """
    Create or update a Thing node for a file.

    Creates the Thing node and links it to its containing Space (module).

    Args:
        path: File path relative to project root
        module: Module name (for Space linkage)
        store: Graph store instance
        file_type: Thing subtype (default: FILE)

    Returns:
        The created/updated ThingNode
    """
    thing_id = generate_thing_id(path, file_type)
    existing = store.get_node(thing_id)

    if existing and isinstance(existing, ThingNode):
        # Update existing
        existing.updated_at_s = int(time.time())
        store.upsert_node(existing)
        return existing

    # Create new Thing node
    thing = create_thing_node(path, file_type)
    store.upsert_node(thing)

    # Ensure Space exists and link
    space_id = generate_space_id(module)
    if not store.get_node(space_id):
        space = create_space_node(module)
        store.upsert_node(space)

    # Create contains link: Space → Thing
    store.create_link(link_space_contains(space_id, thing.id))

    return thing


def upsert_all_file_things(
    target_dir: Path,
    store: DoctorGraphStore,
    ignore_patterns: List[str],
    modules_config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Scan all files in target_dir and create Thing nodes for each.

    Respects .gitignore and .ngramignore patterns.
    Creates Space nodes for modules and links files to them.

    Args:
        target_dir: Project root directory
        store: Graph store instance
        ignore_patterns: List of ignore patterns from config
        modules_config: Optional modules.yaml config for module mapping

    Returns:
        Dict with stats: {files_scanned, things_created, things_updated, spaces_created}
    """
    from .doctor_files import should_ignore_path, is_binary_file
    from .core_utils import IGNORED_EXTENSIONS

    stats = {
        "files_scanned": 0,
        "things_created": 0,
        "things_updated": 0,
        "spaces_created": 0,
        "modules": set(),
    }

    # Skip directories that should never be scanned
    skip_dirs = {
        '.git', '.ngram', '__pycache__', '.venv', 'venv',
        'node_modules', '.next', 'dist', 'build', '.cache',
        '.pytest_cache', '.mypy_cache', 'coverage', '.tox',
    }

    def get_module_for_path(file_path: Path) -> str:
        """Determine module name for a file path."""
        try:
            rel_path = file_path.relative_to(target_dir)
        except ValueError:
            return "root"

        parts = rel_path.parts

        # Check modules_config for explicit mapping
        if modules_config:
            for module_name, module_info in modules_config.items():
                if isinstance(module_info, dict):
                    module_path = module_info.get("path", "")
                    if module_path and str(rel_path).startswith(module_path):
                        return module_name

        # Default: use first directory component
        if len(parts) > 1:
            return parts[0]
        return "root"

    def scan_directory(directory: Path, depth: int = 0) -> None:
        """Recursively scan directory for files."""
        if depth > 10:  # Prevent too deep recursion
            return

        try:
            items = list(directory.iterdir())
        except PermissionError:
            return

        for item in items:
            # Skip hidden files/dirs
            if item.name.startswith('.'):
                continue

            # Skip known skip directories
            if item.is_dir() and item.name in skip_dirs:
                continue

            # Check ignore patterns
            if should_ignore_path(item, ignore_patterns, target_dir):
                continue

            if item.is_dir():
                scan_directory(item, depth + 1)
            elif item.is_file():
                # Skip binary files
                if is_binary_file(item):
                    continue

                # Skip ignored extensions
                if item.suffix.lower() in IGNORED_EXTENSIONS:
                    continue

                stats["files_scanned"] += 1

                # Get relative path for storage
                try:
                    rel_path = str(item.relative_to(target_dir))
                except ValueError:
                    rel_path = str(item)

                # Determine module
                module = get_module_for_path(item)
                stats["modules"].add(module)

                # Check if Thing already exists
                thing_id = generate_thing_id(rel_path)
                existing = store.get_node(thing_id)

                if existing:
                    stats["things_updated"] += 1
                else:
                    stats["things_created"] += 1

                # Upsert the file Thing
                upsert_file_thing(rel_path, module, store)

    # Start scan from target_dir
    scan_directory(target_dir)

    # Count spaces created
    for module in stats["modules"]:
        space_id = generate_space_id(module)
        space = store.get_node(space_id)
        if space and space.created_at_s == space.updated_at_s:
            # Newly created (timestamps match)
            stats["spaces_created"] += 1

    # Convert set to count for return
    stats["modules_count"] = len(stats["modules"])
    del stats["modules"]

    return stats


def sync_file_things_to_graph(
    target_dir: Path,
    store: DoctorGraphStore,
    ignore_patterns: List[str],
    graph_ops: Optional[Any] = None,
) -> Dict[str, Any]:
    """
    Sync file Thing nodes to external graph database.

    First builds local store with upsert_all_file_things,
    then syncs to external graph if graph_ops provided.

    Args:
        target_dir: Project root directory
        store: Local graph store instance
        ignore_patterns: List of ignore patterns
        graph_ops: Optional external graph operations instance

    Returns:
        Dict with sync stats
    """
    # Build local store
    stats = upsert_all_file_things(target_dir, store, ignore_patterns)

    if not graph_ops:
        return stats

    # Sync to external graph
    sync_stats = {"nodes_synced": 0, "links_synced": 0}

    try:
        # Sync Thing nodes (FalkorDB-compatible: no ON CREATE SET)
        for node_id, node in store.nodes.items():
            if isinstance(node, ThingNode):
                # Use MERGE with all properties set unconditionally
                cypher = """
                MERGE (t:Thing {id: $id})
                SET t.node_type = $node_type,
                    t.type = $type,
                    t.name = $name,
                    t.uri = $uri,
                    t.description = $description,
                    t.weight = $weight,
                    t.energy = $energy,
                    t.created_at_s = $created_at_s,
                    t.updated_at_s = $updated_at_s
                """
                graph_ops._query(cypher, {
                    "id": node.id,
                    "node_type": node.node_type,
                    "type": node.type,
                    "name": node.name,
                    "uri": node.uri,
                    "description": node.description,
                    "weight": node.weight,
                    "energy": node.energy,
                    "created_at_s": node.created_at_s,
                    "updated_at_s": node.updated_at_s,
                })
                sync_stats["nodes_synced"] += 1

            elif isinstance(node, SpaceNode):
                cypher = """
                MERGE (s:Space {id: $id})
                SET s.node_type = $node_type,
                    s.type = $type,
                    s.name = $name,
                    s.description = $description,
                    s.weight = $weight,
                    s.energy = $energy,
                    s.created_at_s = $created_at_s,
                    s.updated_at_s = $updated_at_s
                """
                graph_ops._query(cypher, {
                    "id": node.id,
                    "node_type": node.node_type,
                    "type": node.type,
                    "name": node.name,
                    "description": node.description,
                    "weight": node.weight,
                    "energy": node.energy,
                    "created_at_s": node.created_at_s,
                    "updated_at_s": node.updated_at_s,
                })
                sync_stats["nodes_synced"] += 1

        # Sync contains links (Space → Thing)
        for link in store.links:
            if link.type == LinkType.CONTAINS.value:
                cypher = """
                MATCH (a {id: $from_id})
                MATCH (b {id: $to_id})
                MERGE (a)-[r:contains]->(b)
                SET r.created_at_s = $created_at_s
                """
                graph_ops._query(cypher, {
                    "from_id": link.node_a,
                    "to_id": link.node_b,
                    "created_at_s": link.created_at_s,
                })
                sync_stats["links_synced"] += 1

    except Exception as e:
        sync_stats["error"] = str(e)

    stats.update(sync_stats)
    return stats


# =============================================================================
# FUNCTION ALIAS
# =============================================================================

# doctor_tasks.py imports use this name
upsert_issue_from_check = upsert_issue
