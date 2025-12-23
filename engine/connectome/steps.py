"""
Connectome Step Processors

Processes each step type: ask, query, create, update, branch.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass

from .session import SessionState, LoopState
from .loader import StepDefinition
from .validation import validate_input, coerce_value, ValidationError
from .templates import expand_template, expand_dict

logger = logging.getLogger(__name__)


@dataclass
class StepResult:
    """Result from processing a step."""
    success: bool
    next_step: Optional[str] = None
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    needs_input: bool = False


class StepProcessor:
    """
    Processes connectome steps.

    Requires graph_ops and graph_queries for graph operations.
    """

    # Preset queries for common patterns
    PRESET_QUERIES = {
        "all_spaces": "MATCH (n:Space) RETURN n.id, n.name, n.type ORDER BY n.name",
        "all_validations": "MATCH (n:Narrative) WHERE n.type = 'validation' RETURN n.id, n.name",
        "all_behaviors": "MATCH (n:Narrative) WHERE n.type = 'behavior' RETURN n.id, n.name",
        "all_goals": "MATCH (n:Narrative) WHERE n.type = 'goal' RETURN n.id, n.name, n.status",
        "all_narratives": "MATCH (n:Narrative) RETURN n.id, n.name, n.type ORDER BY n.type, n.name",
        "all_actors": "MATCH (n:Actor) RETURN n.id, n.name, n.type ORDER BY n.name",
    }

    def __init__(self, graph_ops=None, graph_queries=None):
        """
        Initialize processor.

        Args:
            graph_ops: GraphOps instance for mutations
            graph_queries: GraphQueries instance for queries
        """
        self.graph_ops = graph_ops
        self.graph_queries = graph_queries

    def process_step(
        self,
        step: StepDefinition,
        session: SessionState,
        answer: Any = None
    ) -> StepResult:
        """
        Process a single step.

        Args:
            step: The step definition
            session: Current session state
            answer: Answer if this is continuing an ask step

        Returns:
            StepResult
        """
        handlers = {
            "ask": self._process_ask,
            "query": self._process_query,
            "create": self._process_create,
            "update": self._process_update,
            "branch": self._process_branch,
        }

        handler = handlers.get(step.type)
        if not handler:
            return StepResult(
                success=False,
                error=f"Unknown step type: {step.type}"
            )

        try:
            return handler(step, session, answer)
        except Exception as e:
            logger.exception(f"Error processing step {step.id}")
            return StepResult(
                success=False,
                error=str(e)
            )

    def _process_ask(
        self,
        step: StepDefinition,
        session: SessionState,
        answer: Any = None
    ) -> StepResult:
        """Process an ask step."""
        config = step.config
        expects = config.get("expects", {"type": "string"})

        # Check for for_each loop
        for_each = config.get("for_each")
        if for_each and not session.loop_state:
            # Start loop
            items = session.get_answer(for_each) or session.get_context(for_each)
            if isinstance(items, list):
                session.loop_state = LoopState(step_id=step.id, items=items)

        # Get current loop item if in loop
        extra = {}
        if session.loop_state and session.loop_state.step_id == step.id:
            extra["item"] = session.loop_state.current_item

        # If no answer yet, return question
        if answer is None:
            question = expand_template(
                config.get("question", ""),
                session.collected,
                session.context,
                extra
            )
            return StepResult(
                success=True,
                needs_input=True,
                response={
                    "step_id": step.id,
                    "type": "ask",
                    "question": question,
                    "expects": expects,
                    "loop_index": session.loop_state.index if session.loop_state else None,
                    "loop_total": len(session.loop_state.items) if session.loop_state else None,
                }
            )

        # Validate and store answer
        answer = coerce_value(answer, expects)
        is_valid, error = validate_input(answer, expects)

        if not is_valid:
            return StepResult(
                success=False,
                needs_input=True,
                error=error,
                response={
                    "step_id": step.id,
                    "type": "ask",
                    "question": config.get("question"),
                    "expects": expects,
                    "validation_error": error,
                }
            )

        # Store answer
        if session.loop_state and session.loop_state.step_id == step.id:
            # In loop - advance and check if done
            session.loop_state.advance(answer)
            if not session.loop_state.is_complete:
                # Stay on same step for next item
                return StepResult(
                    success=True,
                    next_step=step.id,
                )
            else:
                # Loop complete - store all results and continue
                session.set_answer(step.id, session.loop_state.results)
                session.loop_state = None
        else:
            session.set_answer(step.id, answer)

        # Move to next step
        next_step = step.next
        if next_step == "$complete":
            next_step = None

        return StepResult(
            success=True,
            next_step=next_step,
        )

    def _process_query(
        self,
        step: StepDefinition,
        session: SessionState,
        answer: Any = None
    ) -> StepResult:
        """Process a query step."""
        config = step.config
        store_as = config.get("store_as", step.id)

        # Get query (preset or custom)
        preset = config.get("preset")
        if preset:
            # Handle parameterized presets like "space_contents:space_123"
            if ":" in preset:
                preset_name, param = preset.split(":", 1)
                param = expand_template(param, session.collected, session.context)
                query = self._get_preset_query(preset_name, param)
            else:
                query = self.PRESET_QUERIES.get(preset)
                if not query:
                    return StepResult(
                        success=False,
                        error=f"Unknown preset query: {preset}"
                    )
        else:
            query = config.get("query", "")
            query = expand_template(query, session.collected, session.context)

        # Execute query
        results = []
        if self.graph_queries:
            try:
                # Build params from session
                params = {
                    **session.collected,
                    **{f"ctx_{k}": v for k, v in session.context.items()},
                }
                # Add special params
                if "target_id" in session.context:
                    params["target_id"] = session.context["target_id"]

                raw_results = self.graph_queries.query(query, params=params)
                results = self._normalize_query_results(raw_results)
            except Exception as e:
                logger.warning(f"Query failed: {e}")
                results = []
        else:
            # No graph connection - return empty for testing
            logger.warning("No graph_queries configured, returning empty results")

        # Store results
        session.set_context(store_as, results)

        # Move to next
        next_step = step.next
        if next_step == "$complete":
            next_step = None

        return StepResult(
            success=True,
            next_step=next_step,
            response={
                "step_id": step.id,
                "type": "query",
                "store_as": store_as,
                "result_count": len(results),
                "results": results,
            }
        )

    def _process_create(
        self,
        step: StepDefinition,
        session: SessionState,
        answer: Any = None
    ) -> StepResult:
        """Process a create step."""
        config = step.config
        nodes_config = config.get("nodes", [])
        links_config = config.get("links", [])

        created_nodes = []
        created_links = []

        # Create nodes
        for node_config in nodes_config:
            # Check for for_each
            for_each = node_config.get("for_each")
            if for_each:
                items = session.get_answer(for_each) or session.get_context(for_each) or []
                for item in items:
                    extra = {"item": item}
                    node = self._create_node(node_config, session, extra)
                    if node:
                        created_nodes.append(node)
                        session.add_created_node(node)
            else:
                node = self._create_node(node_config, session)
                if node:
                    created_nodes.append(node)
                    session.add_created_node(node)

        # Create links
        for link_config in links_config:
            for_each = link_config.get("for_each")
            if for_each:
                items = session.get_answer(for_each) or session.get_context(for_each) or []
                for item in items:
                    extra = {"item": item}
                    link = self._create_link(link_config, session, extra)
                    if link:
                        created_links.append(link)
                        session.add_created_link(link)
            else:
                link = self._create_link(link_config, session)
                if link:
                    created_links.append(link)
                    session.add_created_link(link)

        # Move to next
        next_step = step.next
        if next_step == "$complete":
            next_step = None

        return StepResult(
            success=True,
            next_step=next_step,
            response={
                "step_id": step.id,
                "type": "create",
                "created_nodes": created_nodes,
                "created_links": created_links,
            }
        )

    def _process_update(
        self,
        step: StepDefinition,
        session: SessionState,
        answer: Any = None
    ) -> StepResult:
        """Process an update step."""
        config = step.config
        target = expand_template(
            config.get("target", ""),
            session.collected,
            session.context
        )
        set_values = config.get("set", {})

        # Expand set values
        expanded_values = expand_dict(set_values, session.collected, session.context)

        # Apply update
        if self.graph_ops and target:
            try:
                # Build cypher for update
                set_clauses = ", ".join(f"n.{k} = ${k}" for k in expanded_values.keys())
                cypher = f"""
                MATCH (n {{id: $target_id}})
                SET {set_clauses}
                RETURN n.id
                """
                params = {"target_id": target, **expanded_values}
                self.graph_ops._query(cypher, params)
            except Exception as e:
                logger.error(f"Update failed: {e}")
                return StepResult(success=False, error=str(e))

        # Move to next
        next_step = step.next
        if next_step == "$complete":
            next_step = None

        return StepResult(
            success=True,
            next_step=next_step,
            response={
                "step_id": step.id,
                "type": "update",
                "target": target,
                "set": expanded_values,
            }
        )

    def _process_branch(
        self,
        step: StepDefinition,
        session: SessionState,
        answer: Any = None
    ) -> StepResult:
        """Process a branch step."""
        config = step.config
        condition = config.get("condition", "")

        # Expand condition
        expanded = expand_template(condition, session.collected, session.context)

        # Evaluate condition
        # Simple evaluation - check for == comparisons
        result = self._evaluate_condition(expanded, session)

        # Handle cases or then/else
        cases = config.get("cases", {})
        if cases:
            # Look up value in cases
            value = session.get_answer(condition.strip("{}").split("|")[0])
            next_step = cases.get(value, config.get("default"))
        else:
            # then/else
            next_step = config.get("then") if result else config.get("else")

        if next_step == "$complete":
            next_step = None

        return StepResult(
            success=True,
            next_step=next_step,
            response={
                "step_id": step.id,
                "type": "branch",
                "condition_result": result,
                "next": next_step,
            }
        )

    def _create_node(
        self,
        node_config: Dict[str, Any],
        session: SessionState,
        extra: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a single node."""
        extra = extra or {}
        expanded = expand_dict(node_config, session.collected, session.context, extra)

        node_id = expanded.get("id")
        node_type = expanded.get("node_type", "narrative")

        if not node_id:
            return None

        # Map to engine methods
        if self.graph_ops:
            try:
                if node_type == "narrative":
                    self.graph_ops.add_narrative(
                        id=node_id,
                        name=expanded.get("name", node_id),
                        content=expanded.get("content", ""),
                        type=expanded.get("type", "memory"),
                        weight=float(expanded.get("weight", 0.5)),
                    )
                elif node_type == "space":
                    self.graph_ops.add_place(
                        id=node_id,
                        name=expanded.get("name", node_id),
                        type=expanded.get("type", "module"),
                        weight=float(expanded.get("weight", 0.5)),
                    )
                elif node_type == "thing":
                    self.graph_ops.add_thing(
                        id=node_id,
                        name=expanded.get("name", node_id),
                        type=expanded.get("type", "file"),
                    )
                elif node_type == "moment":
                    self.graph_ops.add_moment(
                        id=node_id,
                        text=expanded.get("prose", expanded.get("text", "")),
                        type=expanded.get("type", "narration"),
                        status=expanded.get("status", "completed"),
                    )
            except Exception as e:
                logger.error(f"Failed to create node {node_id}: {e}")
                return None

        return expanded

    def _create_link(
        self,
        link_config: Dict[str, Any],
        session: SessionState,
        extra: Optional[Dict[str, Any]] = None
    ) -> Optional[Dict[str, Any]]:
        """Create a single link."""
        extra = extra or {}
        expanded = expand_dict(link_config, session.collected, session.context, extra)

        link_type = expanded.get("type")
        from_id = expanded.get("from")
        to_id = expanded.get("to")

        if not all([link_type, from_id, to_id]):
            return None

        # Handle item being just an ID string
        if isinstance(extra.get("item"), str):
            if to_id == "{item}":
                to_id = extra["item"]
            if from_id == "{item}":
                from_id = extra["item"]

        properties = expanded.get("properties", {})

        if self.graph_ops:
            try:
                if link_type == "contains":
                    # Generic contains
                    cypher = """
                    MATCH (a {id: $from_id})
                    MATCH (b {id: $to_id})
                    MERGE (a)-[:CONTAINS]->(b)
                    """
                    self.graph_ops._query(cypher, {"from_id": from_id, "to_id": to_id})
                elif link_type == "relates":
                    self.graph_ops.add_narrative_link(
                        source_id=from_id,
                        target_id=to_id,
                        supports=float(properties.get("supports", 0)),
                        contradicts=float(properties.get("contradicts", 0)),
                        elaborates=float(properties.get("elaborates", 0)),
                    )
                elif link_type == "about":
                    self.graph_ops.add_about(
                        moment_id=from_id,
                        target_id=to_id,
                        weight=float(properties.get("weight", 0.5)),
                    )
                elif link_type == "expresses":
                    self.graph_ops.add_said(
                        character_id=from_id,
                        moment_id=to_id,
                    )
                else:
                    # Generic link creation
                    cypher = f"""
                    MATCH (a {{id: $from_id}})
                    MATCH (b {{id: $to_id}})
                    MERGE (a)-[r:{link_type.upper()}]->(b)
                    SET r += $props
                    """
                    self.graph_ops._query(cypher, {
                        "from_id": from_id,
                        "to_id": to_id,
                        "props": properties,
                    })
            except Exception as e:
                logger.error(f"Failed to create link {from_id}->{to_id}: {e}")
                return None

        return expanded

    def _get_preset_query(self, preset_name: str, param: str) -> str:
        """Get parameterized preset query."""
        presets = {
            "space_contents": f"""
                MATCH (s:Space {{id: '{param}'}})-[:CONTAINS]->(n)
                RETURN n.id, n.name, labels(n)[0] as type
            """,
            "node_links": f"""
                MATCH (n {{id: '{param}'}})-[r]-(m)
                RETURN type(r) as rel_type, m.id, m.name, labels(m)[0] as type
            """,
        }
        return presets.get(preset_name, "RETURN 1")

    def _normalize_query_results(self, raw_results: List) -> List[Dict[str, Any]]:
        """Normalize query results to list of dicts."""
        if not raw_results:
            return []

        normalized = []
        for row in raw_results:
            if isinstance(row, dict):
                normalized.append(row)
            elif isinstance(row, (list, tuple)):
                # Convert to dict with index keys
                normalized.append({f"col{i}": v for i, v in enumerate(row)})
            else:
                normalized.append({"value": row})

        return normalized

    def _evaluate_condition(self, condition: str, session: SessionState) -> bool:
        """Evaluate a simple condition string."""
        # Handle == comparison
        if "==" in condition:
            parts = condition.split("==")
            if len(parts) == 2:
                left = parts[0].strip().strip("'\"")
                right = parts[1].strip().strip("'\"")
                return left == right

        # Handle truthy check
        if condition.lower() in ("true", "1", "yes"):
            return True
        if condition.lower() in ("false", "0", "no", ""):
            return False

        # Check if it's a reference that's truthy
        return bool(condition)
