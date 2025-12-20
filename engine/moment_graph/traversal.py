"""
Blood Ledger — Moment Graph Traversal Engine

Handles click traversal, weight updates, and moment state transitions.
This is the hot path — must be <50ms for all operations.
"""

# DOCS: docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md

import logging
from typing import Dict, Any, Optional, List

from engine.physics.graph.graph_ops import GraphOps
from .queries import MomentQueries

logger = logging.getLogger(__name__)


class MomentTraversal:
    """
    Handles moment graph traversal.

    Core operations:
    - Click a word -> traverse to linked moment
    - Update weights on traversal
    - Mark moments as spoken
    - Create THEN links for history
    """

    def __init__(
        self,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379
    ):
        self.queries = MomentQueries(graph_name=graph_name, host=host, port=port)
        self.write = GraphOps(graph_name=graph_name, host=host, port=port)
        self.graph_name = graph_name

    def handle_click(
        self,
        moment_id: str,
        word: str,
        tick: int,
        player_id: str = "char_player"
    ) -> Optional[Dict]:
        """
        Handle player clicking a word in a moment.

        This is THE hot path. Must be <50ms total.

        Args:
            moment_id: Current active moment
            word: Word that was clicked
            tick: Current world tick
            player_id: Player character ID

        Returns:
            Target moment dict if found, None otherwise
        """
        # 1. Find matching target
        matches = self.queries.find_click_targets(moment_id, word)
        if not matches:
            logger.debug(f"[Traversal] No match for '{word}' from {moment_id}")
            return None

        # 2. Use first match (highest implicit priority)
        target = matches[0]
        target_id = target['id']

        # 3. Apply weight transfer
        weight_transfer = target.get('weight_transfer', 0.3)
        self._boost_weight(target_id, weight_transfer)

        # 4. Consume origin if configured
        if target.get('consumes_origin', True):
            self._update_status(moment_id, 'spoken', tick)

        # 5. Activate target
        self._update_status(target_id, 'active', tick)

        # 6. Create THEN link (history)
        self._create_then_link(moment_id, target_id, tick, player_caused=True)

        logger.info(f"[Traversal] Click: {moment_id} --[{word}]--> {target_id}")

        return target

    def activate_moment(
        self,
        moment_id: str,
        tick: int
    ) -> None:
        """Activate a moment (make it visible/triggerable)."""
        self._update_status(moment_id, 'active', tick)
        logger.debug(f"[Traversal] Activated: {moment_id}")

    def speak_moment(
        self,
        moment_id: str,
        tick: int,
        speaker_id: str = None
    ) -> None:
        """Mark moment as spoken and create SAID link if speaker."""
        self._update_status(moment_id, 'spoken', tick)
        if speaker_id:
            self.write.add_said(speaker_id, moment_id)
        logger.debug(f"[Traversal] Spoken: {moment_id} by {speaker_id}")

    def make_dormant(
        self,
        moment_id: str
    ) -> None:
        """Set moment to dormant (waiting for return)."""
        self._update_status(moment_id, 'dormant')
        logger.debug(f"[Traversal] Dormant: {moment_id}")

    def decay_moment(
        self,
        moment_id: str,
        tick: int
    ) -> None:
        """Mark moment as decayed (pruned)."""
        self._update_status(moment_id, 'decayed', tick)
        logger.debug(f"[Traversal] Decayed: {moment_id}")

    def reactivate_dormant(
        self,
        location_id: str,
        tick: int
    ) -> List[str]:
        """
        Reactivate dormant moments when player returns to location.

        Args:
            location_id: Place the player arrived at
            tick: Current tick

        Returns:
            List of moment IDs that were reactivated
        """
        dormant = self.queries.get_dormant_moments(location_id)
        reactivated = []

        for m in dormant:
            moment_id = m['id']
            self._update_status(moment_id, 'possible')
            # Restore some weight (at least 0.3)
            current_weight = m.get('weight', 0.3)
            self._set_weight(moment_id, max(0.3, current_weight))
            reactivated.append(moment_id)

        if reactivated:
            logger.info(f"[Traversal] Reactivated {len(reactivated)} dormant moments at {location_id}")
        return reactivated

    def process_wait_triggers(
        self,
        tick: int
    ) -> List[Dict]:
        """
        Process wait triggers that should auto-fire.

        Args:
            tick: Current world tick

        Returns:
            List of transitions that fired
        """
        triggers = self.queries.get_wait_triggers(tick)
        fired = []

        for t in triggers:
            from_id = t['from_id']
            to_id = t['to_id']

            # Apply weight transfer
            weight_transfer = t.get('weight_transfer', 0.3)
            self._boost_weight(to_id, weight_transfer)

            # Consume origin if configured
            if t.get('consumes_origin', True):
                self._update_status(from_id, 'spoken', tick)

            # Activate target
            self._update_status(to_id, 'active', tick)

            # Create THEN link
            self._create_then_link(from_id, to_id, tick, player_caused=False)

            fired.append(t)
            logger.info(f"[Traversal] Wait trigger: {from_id} --> {to_id}")

        return fired

    def _update_status(
        self,
        moment_id: str,
        status: str,
        tick: int = None
    ) -> None:
        """Update moment status and relevant tick."""
        props = {"status": status}

        if status == "spoken" and tick is not None:
            props["tick_spoken"] = tick
        elif status == "decayed" and tick is not None:
            props["tick_decayed"] = tick

        cypher = """
        MATCH (m:Moment {id: $moment_id})
        SET m += $props
        """
        self.write._query(cypher, {"moment_id": moment_id, "props": props})

    def _set_weight(
        self,
        moment_id: str,
        weight: float
    ) -> None:
        """Set moment weight to specific value."""
        weight = max(0.0, min(1.0, weight))
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        SET m.weight = $weight
        """
        self.write._query(cypher, {"moment_id": moment_id, "weight": weight})

    def _boost_weight(
        self,
        moment_id: str,
        boost: float
    ) -> None:
        """Add to moment weight (clamped to 0-1)."""
        cypher = """
        MATCH (m:Moment {id: $moment_id})
        SET m.weight = CASE
            WHEN m.weight + $boost > 1.0 THEN 1.0
            WHEN m.weight + $boost < 0.0 THEN 0.0
            ELSE m.weight + $boost
        END
        """
        self.write._query(cypher, {"moment_id": moment_id, "boost": boost})

    def _create_then_link(
        self,
        from_id: str,
        to_id: str,
        tick: int,
        player_caused: bool = False
    ) -> None:
        """Create THEN link with tick and causation info."""
        cypher = """
        MATCH (m1:Moment {id: $from_id})
        MATCH (m2:Moment {id: $to_id})
        MERGE (m1)-[r:THEN]->(m2)
        SET r.tick = $tick, r.player_caused = $player_caused
        """
        self.write._query(cypher, {
            "from_id": from_id,
            "to_id": to_id,
            "tick": tick,
            "player_caused": player_caused
        })
