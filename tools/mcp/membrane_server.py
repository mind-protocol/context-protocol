#!/usr/bin/env python3
"""
Membrane MCP Server

Exposes the connectome/membrane structured dialogue system as MCP tools.

Tools:
  - membrane_start: Start a new membrane dialogue
  - membrane_continue: Continue with an answer
  - membrane_abort: Abort a session

Usage:
  Run as MCP server (stdio):
    python tools/mcp/membrane_server.py

  Configure in Claude Code settings:
    {
      "mcpServers": {
        "membrane": {
          "command": "python",
          "args": ["tools/mcp/membrane_server.py"],
          "cwd": "/path/to/ngram"
        }
      }
    }
"""

import sys
import json
import logging
from pathlib import Path
from typing import Any, Dict, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from engine.connectome import ConnectomeRunner

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stderr
)
logger = logging.getLogger("membrane")

# =============================================================================
# MCP PROTOCOL IMPLEMENTATION
# =============================================================================

class MembraneServer:
    """MCP Server for Membrane tools."""

    def __init__(self, connectomes_dir: Optional[Path] = None):
        """Initialize server with optional connectomes directory."""
        self.connectomes_dir = connectomes_dir or (project_root / "tests" / "connectome_v0" / "connectomes")

        # Try to get graph connections if available
        try:
            from engine.physics.graph import GraphOps, GraphQueries
            self.graph_ops = GraphOps()
            self.graph_queries = GraphQueries()
            logger.info("Connected to graph database")
        except Exception as e:
            logger.warning(f"No graph connection: {e}")
            self.graph_ops = None
            self.graph_queries = None

        self.runner = ConnectomeRunner(
            graph_ops=self.graph_ops,
            graph_queries=self.graph_queries,
            connectomes_dir=self.connectomes_dir
        )

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a JSON-RPC request."""
        method = request.get("method", "")
        params = request.get("params", {})
        request_id = request.get("id")

        try:
            if method == "initialize":
                result = self._handle_initialize(params)
            elif method == "tools/list":
                result = self._handle_list_tools()
            elif method == "tools/call":
                result = self._handle_call_tool(params)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")

            return self._success_response(request_id, result)
        except Exception as e:
            logger.exception(f"Error handling {method}")
            return self._error_response(request_id, -32000, str(e))

    def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request."""
        return {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {}
            },
            "serverInfo": {
                "name": "membrane",
                "version": "0.1.0"
            }
        }

    def _handle_list_tools(self) -> Dict[str, Any]:
        """Return list of available tools."""
        return {
            "tools": [
                {
                    "name": "membrane_start",
                    "description": "Start a new membrane dialogue session. Returns the first step.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "membrane": {
                                "type": "string",
                                "description": "Name of the membrane/connectome to run (e.g., 'create_validation', 'document_progress')"
                            },
                            "context": {
                                "type": "object",
                                "description": "Optional initial context values (e.g., {\"actor_id\": \"actor_claude\"})"
                            }
                        },
                        "required": ["membrane"]
                    }
                },
                {
                    "name": "membrane_continue",
                    "description": "Continue a membrane session with an answer to the current step.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID from membrane_start"
                            },
                            "answer": {
                                "description": "Answer for the current step. Type depends on what the step expects."
                            }
                        },
                        "required": ["session_id", "answer"]
                    }
                },
                {
                    "name": "membrane_abort",
                    "description": "Abort a membrane session. No changes will be committed.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "session_id": {
                                "type": "string",
                                "description": "Session ID to abort"
                            }
                        },
                        "required": ["session_id"]
                    }
                },
                {
                    "name": "membrane_list",
                    "description": "List available membrane definitions.",
                    "inputSchema": {
                        "type": "object",
                        "properties": {}
                    }
                }
            ]
        }

    def _handle_call_tool(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a tool call."""
        tool_name = params.get("name", "")
        arguments = params.get("arguments", {})

        if tool_name == "membrane_start":
            return self._tool_start(arguments)
        elif tool_name == "membrane_continue":
            return self._tool_continue(arguments)
        elif tool_name == "membrane_abort":
            return self._tool_abort(arguments)
        elif tool_name == "membrane_list":
            return self._tool_list(arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

    def _tool_start(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Start a membrane session."""
        membrane_name = args.get("membrane")
        context = args.get("context", {})

        if not membrane_name:
            return {"content": [{"type": "text", "text": "Error: 'membrane' is required"}]}

        response = self.runner.start(membrane_name, initial_context=context)
        return self._format_response(response)

    def _tool_continue(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Continue a membrane session."""
        session_id = args.get("session_id")
        answer = args.get("answer")

        if not session_id:
            return {"content": [{"type": "text", "text": "Error: 'session_id' is required"}]}

        response = self.runner.continue_session(session_id, answer)
        return self._format_response(response)

    def _tool_abort(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Abort a membrane session."""
        session_id = args.get("session_id")

        if not session_id:
            return {"content": [{"type": "text", "text": "Error: 'session_id' is required"}]}

        response = self.runner.abort(session_id)
        return self._format_response(response)

    def _tool_list(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """List available membranes."""
        membranes = []
        if self.connectomes_dir and self.connectomes_dir.exists():
            for path in self.connectomes_dir.glob("*.yaml"):
                membranes.append(path.stem)

        text = "Available membranes:\n"
        for m in membranes:
            text += f"  - {m}\n"

        return {"content": [{"type": "text", "text": text}]}

    def _format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Format runner response as MCP tool result."""
        status = response.get("status", "unknown")

        lines = [f"Status: {status}"]

        if response.get("error"):
            lines.append(f"Error: {response['error']}")

        if response.get("session_id"):
            lines.append(f"Session: {response['session_id']}")

        step = response.get("step", {})
        if step:
            step_type = step.get("type", "")
            lines.append(f"Step Type: {step_type}")

            if step.get("question"):
                lines.append(f"\nQuestion: {step['question']}")

            if step.get("expects"):
                expects = step["expects"]
                lines.append(f"Expects: {expects.get('type', 'string')}")
                if expects.get("options"):
                    lines.append(f"Options: {expects['options']}")
                if expects.get("min_length"):
                    lines.append(f"Min Length: {expects['min_length']}")
                if expects.get("min") is not None:
                    lines.append(f"Min Items: {expects['min']}")

            if step.get("results"):
                lines.append(f"\nQuery Results: {len(step['results'])} items")
                for r in step["results"][:5]:
                    lines.append(f"  - {r}")

        if status == "complete":
            created = response.get("created", {})
            nodes = created.get("nodes", [])
            links = created.get("links", [])

            lines.append(f"\nCreated: {len(nodes)} nodes, {len(links)} links")

            if nodes:
                lines.append("\nNodes:")
                for n in nodes:
                    lines.append(f"  - [{n.get('type')}] {n.get('id')}")

            if links:
                lines.append("\nLinks:")
                for l in links:
                    lines.append(f"  - {l.get('type')}: {l.get('from')} -> {l.get('to')}")

        text = "\n".join(lines)
        return {"content": [{"type": "text", "text": text}]}

    def _success_response(self, request_id: Any, result: Any) -> Dict[str, Any]:
        """Build success response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": result
        }

    def _error_response(self, request_id: Any, code: int, message: str) -> Dict[str, Any]:
        """Build error response."""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }


def main():
    """Run the MCP server on stdio."""
    server = MembraneServer()
    logger.info("Membrane MCP server started")

    # Read JSON-RPC messages from stdin
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        try:
            request = json.loads(line)
            response = server.handle_request(request)
            print(json.dumps(response), flush=True)
        except json.JSONDecodeError as e:
            error_response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {
                    "code": -32700,
                    "message": f"Parse error: {e}"
                }
            }
            print(json.dumps(error_response), flush=True)


if __name__ == "__main__":
    main()
