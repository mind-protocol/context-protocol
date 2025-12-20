"""
Blood Ledger — Moment Graph Query Layer

Fast queries for the moment graph. All operations must be <50ms.
No LLM calls. Pure graph traversal.
"""

# DOCS: docs/engine/moment-graph-engine/PATTERNS_Instant_Traversal_Moment_Graph.md

import json
import logging
from typing import List, Dict, Any, Optional, Set

from engine.physics.graph.graph_queries import GraphQueries

logger = logging.getLogger(__name__)


class MomentQueries:
    """
    Query layer for moment graph operations.

    All methods must be fast (<50ms). No LLM calls.
    """

    def __init__(
        self,
        graph_name: str = "blood_ledger",
        host: str = "localhost",
        port: int = 6379
    ):
        self.read = GraphQueries(graph_name=graph_name, host=host, port=port)

    def get_current_view(
        self,
        player_id: str,
        location_id: str,
        present_chars: List[str],
        present_things: List[str] = None,
        limit: int = 20,
        history_limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get all visible moments for current scene, including history.

        Args:
            player_id: Player character ID
            location_id: Current place ID
            present_chars: Character IDs present
            present_things: Thing IDs present (optional)
            limit: Max possible/active moments to return
            history_limit: Max spoken moments to return

        Returns:
            {
                "location": {id, name, type, ...},
                "characters": [{id, name, ...}],
                "things": [{id, name, ...}],
                "moments": [moment dicts],
                "transitions": [transition dicts],
                "active_count": int
            }
        """
        present_things = present_things or []

        # Build presence set for gating
        present_set = set([player_id, location_id] + present_chars + present_things)

        # 1. Get metadata (location, characters, things)
        location = self.read.get_place(location_id)
        characters = [self.read.get_character(cid) for cid in present_chars]
        characters = [c for c in characters if c]
        things = [self.read.get_thing(tid) for tid in present_things]
        things = [t for t in things if t]

        # 2. Query: Get moments that pass presence gating
        # Statuses: 'active', 'possible' (live), 'spoken' (history)
        cypher = """
        MATCH (m:Moment)
        WHERE m.status IN ['possible', 'active', 'spoken']

        // Presence gating: Get all presence-required attachments
        OPTIONAL MATCH (m)-[r:ATTACHED_TO]->(target)
        WHERE r.presence_required = true
        WITH m, collect(target.id) AS required_targets

        // Location match for spoken moments
        OPTIONAL MATCH (m)-[:AT]->(at:Place {id: $location_id})
        WITH m, required_targets, at

        // Filter: all required must be in present set (or no requirements)
        // For 'spoken' moments, ensure they are at the current location
        WHERE (size(required_targets) = 0 OR ALL(req IN required_targets WHERE req IN $present_set))
          AND (m.status <> 'spoken' OR at IS NOT NULL)

        // Get speaker via SAID or CAN_SPEAK
        OPTIONAL MATCH (speaker:Character)-[:CAN_SPEAK]->(m)
        WHERE speaker.id IN $present_set
        OPTIONAL MATCH (said_by:Character)-[:SAID]->(m)

        RETURN m.id AS id,
               m.text AS text,
               m.type AS type,
               m.status AS status,
               m.weight AS weight,
               m.tone AS tone,
               m.tick_spoken AS tick_spoken,
               COALESCE(said_by.id, speaker.id) AS speaker

        ORDER BY 
            CASE m.status 
                WHEN 'active' THEN 1 
                WHEN 'possible' THEN 2 
                WHEN 'spoken' THEN 3 
                ELSE 4 
            END,
            m.tick_spoken DESC,
            m.weight DESC
        LIMIT $limit
        """

        try:
            results = self.read.query(cypher, {
                "present_set": list(present_set),
                "location_id": location_id,
                "limit": limit + history_limit
            })

            moments = []
            for row in results:
                if isinstance(row, dict):
                    moments.append({
                        'id': row.get('id'),
                        'text': row.get('text'),
                        'type': row.get('type'),
                        'status': row.get('status'),
                        'weight': row.get('weight'),
                        'tone': row.get('tone'),
                        'tick_spoken': row.get('tick_spoken'),
                        'speaker': row.get('speaker')
                    })
                else:
                    moments.append({
                        'id': row[0],
                        'text': row[1],
                        'type': row[2],
                        'status': row[3],
                        'weight': row[4],
                        'tone': row[5],
                        'tick_spoken': row[6],
                        'speaker': row[7]
                    })
        except Exception as e:
            logger.error(f"[MomentQueries] get_current_view failed: {e}")
            moments = []

        # 3. Get transitions for active moments
        active_ids = [m['id'] for m in moments if m.get('status') == 'active']
        transitions = self._get_transitions(active_ids) if active_ids else []

        return {
            "location": location,
            "characters": characters,
            "things": things,
            "moments": moments,
            "transitions": transitions,
            "active_count": len(active_ids)
        }

    def _get_transitions(self, moment_ids: List[str]) -> List[Dict]:
        """Get CAN_LEAD_TO links from given moments."""
        if not moment_ids:
            return []

        cypher = """
        MATCH (m:Moment)-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE m.id IN $ids
        AND next.status IN ['possible', 'active']
        RETURN m.id AS from_id,
               next.id AS to_id,
               r.trigger AS trigger,
               r.require_words AS require_words,
               r.weight_transfer AS weight_transfer,
               r.consumes_origin AS consumes_origin
        """

        try:
            results = self.read.query(cypher, {"ids": moment_ids})
            transitions = []
            for row in results:
                # Handle both dict and list results from FalkorDB
                if isinstance(row, dict):
                    require_words = row.get('require_words')
                    if isinstance(require_words, str):
                        require_words = json.loads(require_words)
                    transitions.append({
                        'from_id': row.get('from_id'),
                        'to_id': row.get('to_id'),
                        'trigger': row.get('trigger'),
                        'require_words': require_words or [],
                        'weight_transfer': row.get('weight_transfer'),
                        'consumes_origin': row.get('consumes_origin')
                    })
                else:
                    require_words = row[3]
                    if isinstance(require_words, str):
                        require_words = json.loads(require_words)
                    transitions.append({
                        'from_id': row[0],
                        'to_id': row[1],
                        'trigger': row[2],
                        'require_words': require_words or [],
                        'weight_transfer': row[4],
                        'consumes_origin': row[5]
                    })
            return transitions
        except Exception as e:
            logger.error(f"[MomentQueries] _get_transitions failed: {e}")
            return []

    def get_moment_by_id(self, moment_id: str) -> Optional[Dict]:
        """Get a single moment by ID."""
        cypher = """
        MATCH (m:Moment {id: $id})
        RETURN m.id, m.text, m.type, m.status, m.weight, m.tone,
               m.tick_created, m.tick_spoken
        """
        try:
            results = self.read.query(cypher, {"id": moment_id})
            if results:
                row = results[0]
                # Handle both dict and list results from FalkorDB
                if isinstance(row, dict):
                    return {
                        'id': row.get('m.id'),
                        'text': row.get('m.text'),
                        'type': row.get('m.type'),
                        'status': row.get('m.status'),
                        'weight': row.get('m.weight'),
                        'tone': row.get('m.tone'),
                        'tick_created': row.get('m.tick_created'),
                        'tick_spoken': row.get('m.tick_spoken')
                    }
                return {
                    'id': row[0],
                    'text': row[1],
                    'type': row[2],
                    'status': row[3],
                    'weight': row[4],
                    'tone': row[5],
                    'tick_created': row[6],
                    'tick_spoken': row[7]
                }
            return None
        except Exception as e:
            logger.error(f"[MomentQueries] get_moment_by_id failed: {e}")
            return None

    def find_click_targets(
        self,
        moment_id: str,
        word: str
    ) -> List[Dict]:
        """
        Find moments reachable by clicking a word.

        Args:
            moment_id: Current active moment
            word: Word that was clicked

        Returns:
            List of target moments that match the word
        """
        word_lower = word.lower()

        cypher = """
        MATCH (m:Moment {id: $moment_id})-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE r.trigger = 'click'
        AND next.status IN ['possible', 'active']
        RETURN next.id AS id,
               next.text AS text,
               next.type AS type,
               r.require_words AS require_words,
               r.weight_transfer AS weight_transfer,
               r.consumes_origin AS consumes_origin
        """

        try:
            results = self.read.query(cypher, {"moment_id": moment_id})

            candidates = []
            for row in results:
                # Handle both dict and list results from FalkorDB
                if isinstance(row, dict):
                    require_words = row.get('require_words')
                    if isinstance(require_words, str):
                        require_words = json.loads(require_words)
                    candidates.append({
                        'id': row.get('id'),
                        'text': row.get('text'),
                        'type': row.get('type'),
                        'require_words': require_words or [],
                        'weight_transfer': row.get('weight_transfer'),
                        'consumes_origin': row.get('consumes_origin')
                    })
                else:
                    require_words = row[3]
                    if isinstance(require_words, str):
                        require_words = json.loads(require_words)
                    candidates.append({
                        'id': row[0],
                        'text': row[1],
                        'type': row[2],
                        'require_words': require_words or [],
                        'weight_transfer': row[4],
                        'consumes_origin': row[5]
                    })
        except Exception as e:
            logger.error(f"[MomentQueries] find_click_targets failed: {e}")
            return []

        # Filter by word match
        matches = []
        for c in candidates:
            require_words = c.get('require_words', [])
            # Check if clicked word matches any required word
            for req in require_words:
                req_lower = req.lower()
                if req_lower in word_lower or word_lower in req_lower:
                    matches.append(c)
                    break

        return matches

    def get_speaker_for_moment(
        self,
        moment_id: str,
        present_chars: List[str]
    ) -> Optional[str]:
        """
        Determine who speaks a moment based on CAN_SPEAK weights.

        Args:
            moment_id: The moment to speak
            present_chars: Characters currently present

        Returns:
            Character ID of speaker, or None
        """
        cypher = """
        MATCH (c:Character)-[r:CAN_SPEAK]->(m:Moment {id: $moment_id})
        WHERE c.id IN $present
        RETURN c.id AS speaker_id, r.weight AS weight
        ORDER BY r.weight DESC
        LIMIT 1
        """

        try:
            results = self.read.query(cypher, {
                "moment_id": moment_id,
                "present": present_chars
            })
            return results[0][0] if results else None
        except Exception as e:
            logger.error(f"[MomentQueries] get_speaker_for_moment failed: {e}")
            return None

    def get_dormant_moments(
        self,
        location_id: str
    ) -> List[Dict]:
        """Get dormant moments attached to a location."""
        cypher = """
        MATCH (m:Moment {status: 'dormant'})-[:ATTACHED_TO]->(p:Place {id: $loc_id})
        RETURN m.id AS id, m.text AS text, m.weight AS weight
        """
        try:
            results = self.read.query(cypher, {"loc_id": location_id})
            dormant = []
            for row in results:
                if isinstance(row, dict):
                    dormant.append({
                        'id': row.get('id'),
                        'text': row.get('text'),
                        'weight': row.get('weight')
                    })
                else:
                    dormant.append({
                        'id': row[0],
                        'text': row[1],
                        'weight': row[2]
                    })
            return dormant
        except Exception as e:
            logger.error(f"[MomentQueries] get_dormant_moments failed: {e}")
            return []

    def get_wait_triggers(
        self,
        tick: int
    ) -> List[Dict]:
        """Get moments that should auto-fire based on wait time."""
        cypher = """
        MATCH (m:Moment {status: 'active'})-[r:CAN_LEAD_TO]->(next:Moment)
        WHERE r.trigger = 'wait'
        AND m.tick_spoken IS NOT NULL
        AND ($tick - m.tick_spoken) >= r.wait_ticks
        AND next.status IN ['possible', 'active']
        RETURN m.id AS from_id,
               next.id AS to_id,
               r.weight_transfer AS weight_transfer,
               r.consumes_origin AS consumes_origin
        """
        try:
            results = self.read.query(cypher, {"tick": tick})
            triggers = []
            for row in results:
                if isinstance(row, dict):
                    triggers.append({
                        'from_id': row.get('from_id'),
                        'to_id': row.get('to_id'),
                        'weight_transfer': row.get('weight_transfer'),
                        'consumes_origin': row.get('consumes_origin')
                    })
                else:
                    triggers.append({
                        'from_id': row[0],
                        'to_id': row[1],
                        'weight_transfer': row[2],
                        'consumes_origin': row[3]
                    })
            return triggers
        except Exception as e:
            logger.error(f"[MomentQueries] get_wait_triggers failed: {e}")
            return []
