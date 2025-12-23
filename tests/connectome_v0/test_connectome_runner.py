"""
Tests for Connectome v0 Runner

Tests the connectome dialogue system without requiring graph connection.
"""

import pytest
from pathlib import Path

from engine.connectome import ConnectomeRunner, SessionStatus
from engine.connectome.loader import load_connectome, load_connectome_from_string
from engine.connectome.session import SessionState
from engine.connectome.validation import validate_input, coerce_value
from engine.connectome.templates import expand_template, slugify


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def connectomes_dir():
    """Path to test connectomes."""
    return Path(__file__).parent / "connectomes"


@pytest.fixture
def runner(connectomes_dir):
    """Runner without graph connection (for testing)."""
    return ConnectomeRunner(connectomes_dir=connectomes_dir)


@pytest.fixture
def simple_connectome_yaml():
    """A minimal connectome for testing."""
    return """
connectome: simple_test
version: "1.0"
description: Simple test connectome

steps:
  ask_name:
    type: ask
    question: "What is your name?"
    expects:
      type: string
      min_length: 1
    next: ask_priority

  ask_priority:
    type: ask
    question: "Priority?"
    expects:
      type: enum
      options: [HIGH, LOW]
    next: do_create

  do_create:
    type: create
    nodes:
      - id: "test_{ask_name|slugify}"
        node_type: narrative
        type: test
        name: "{ask_name}"
        priority: "{ask_priority}"
    next: $complete
"""


# =============================================================================
# LOADER TESTS
# =============================================================================

class TestLoader:
    """Tests for connectome loading."""

    def test_load_from_string(self, simple_connectome_yaml):
        """Load connectome from YAML string."""
        connectome = load_connectome_from_string(simple_connectome_yaml)

        assert connectome.name == "simple_test"
        assert connectome.version == "1.0"
        assert len(connectome.steps) == 3
        assert connectome.start_step == "ask_name"

    def test_load_from_file(self, connectomes_dir):
        """Load connectome from file."""
        connectome = load_connectome(connectomes_dir / "create_validation.yaml")

        assert connectome.name == "create_validation"
        assert "ask_name" in connectome.steps
        assert "do_create" in connectome.steps

    def test_step_types(self, connectomes_dir):
        """Verify step types are parsed correctly."""
        connectome = load_connectome(connectomes_dir / "create_validation.yaml")

        assert connectome.steps["get_spaces"].type == "query"
        assert connectome.steps["ask_name"].type == "ask"
        assert connectome.steps["do_create"].type == "create"


# =============================================================================
# VALIDATION TESTS
# =============================================================================

class TestValidation:
    """Tests for input validation."""

    def test_string_validation(self):
        """Validate string inputs."""
        expects = {"type": "string", "min_length": 5}

        is_valid, error = validate_input("hello", expects)
        assert is_valid

        is_valid, error = validate_input("hi", expects)
        assert not is_valid
        assert "too short" in error.lower()

    def test_string_pattern(self):
        """Validate string pattern."""
        expects = {"type": "string", "pattern": "^V-[A-Z]+-[A-Z-]+$"}

        is_valid, _ = validate_input("V-TEST-INVARIANT", expects)
        assert is_valid

        is_valid, _ = validate_input("invalid", expects)
        assert not is_valid

    def test_enum_validation(self):
        """Validate enum inputs."""
        expects = {"type": "enum", "options": ["HIGH", "MED", "LOW"]}

        is_valid, _ = validate_input("HIGH", expects)
        assert is_valid

        is_valid, _ = validate_input("INVALID", expects)
        assert not is_valid

    def test_number_validation(self):
        """Validate number inputs."""
        expects = {"type": "number", "min": 0, "max": 1}

        is_valid, _ = validate_input(0.5, expects)
        assert is_valid

        is_valid, _ = validate_input(2, expects)
        assert not is_valid

    def test_id_list_validation(self):
        """Validate ID list inputs."""
        expects = {"type": "id_list", "min": 1, "max": 3}

        is_valid, _ = validate_input(["id1", "id2"], expects)
        assert is_valid

        is_valid, _ = validate_input([], expects)
        assert not is_valid  # min 1

        # Single string becomes list of one
        is_valid, _ = validate_input("single_id", expects)
        assert is_valid

    def test_empty_list_allowed(self):
        """Empty list allowed when min is 0."""
        expects = {"type": "id_list", "min": 0}

        is_valid, _ = validate_input([], expects)
        assert is_valid

    def test_coerce_boolean(self):
        """Coerce string to boolean."""
        expects = {"type": "boolean"}

        assert coerce_value("true", expects) is True
        assert coerce_value("false", expects) is False
        assert coerce_value("yes", expects) is True


# =============================================================================
# TEMPLATE TESTS
# =============================================================================

class TestTemplates:
    """Tests for template expansion."""

    def test_simple_expansion(self):
        """Expand simple references."""
        collected = {"name": "Test Name", "priority": "HIGH"}
        context = {}

        result = expand_template("Hello {name}", collected, context)
        assert result == "Hello Test Name"

    def test_filter_slugify(self):
        """Apply slugify filter."""
        collected = {"name": "Test Name Here"}
        context = {}

        result = expand_template("{name|slugify}", collected, context)
        assert result == "test_name_here"

    def test_nested_context(self):
        """Access nested context values."""
        collected = {}
        context = {
            "spaces": [{"id": "space_1", "name": "First Space"}]
        }

        result = expand_template("{spaces.0.name}", collected, context)
        assert result == "First Space"

    def test_timestamp(self):
        """Timestamp expansion."""
        result = expand_template("{timestamp}", {}, {})
        assert len(result) == 15  # YYYYMMDD_HHMMSS

    def test_missing_reference(self):
        """Missing reference returns empty string."""
        result = expand_template("Hello {missing}", {}, {})
        assert result == "Hello "

    def test_slugify_function(self):
        """Test slugify helper."""
        assert slugify("Hello World") == "hello_world"
        assert slugify("V-TEST-INVARIANT") == "v_test_invariant"
        assert slugify("  spaces  ") == "spaces"


# =============================================================================
# SESSION TESTS
# =============================================================================

class TestSession:
    """Tests for session state."""

    def test_create_session(self):
        """Create new session."""
        session = SessionState.create("test_connectome", "start_step")

        assert session.id
        assert session.connectome_name == "test_connectome"
        assert session.current_step == "start_step"
        assert session.status == SessionStatus.ACTIVE

    def test_collect_answers(self):
        """Store and retrieve answers."""
        session = SessionState.create("test", "start")

        session.set_answer("step1", "value1")
        assert session.get_answer("step1") == "value1"
        assert session.get_answer("missing") is None

    def test_context(self):
        """Store and retrieve context."""
        session = SessionState.create("test", "start")

        session.set_context("query_results", [{"id": "1"}])
        assert session.get_context("query_results") == [{"id": "1"}]

    def test_session_lifecycle(self):
        """Test session status transitions."""
        session = SessionState.create("test", "start")
        assert session.status == SessionStatus.ACTIVE

        session.complete()
        assert session.status == SessionStatus.COMPLETE

    def test_abort(self):
        """Test session abort."""
        session = SessionState.create("test", "start")
        session.abort()
        assert session.status == SessionStatus.ABORTED


# =============================================================================
# RUNNER TESTS
# =============================================================================

class TestRunner:
    """Tests for connectome runner."""

    def test_start_session(self, runner):
        """Start a new session."""
        response = runner.start("create_validation")

        assert response["status"] == "active"
        assert response["session_id"]
        assert response.get("needs_input") or response.get("step")

    def test_continue_with_answer(self, runner):
        """Continue session with valid answer."""
        response = runner.start("create_validation")
        session_id = response["session_id"]

        # Skip query steps (they auto-advance)
        # Should be at ask_name
        while response.get("step", {}).get("type") == "query":
            response = runner.continue_session(session_id)

        # Now at ask step
        assert response.get("step", {}).get("type") == "ask"

        # Provide valid answer
        response = runner.continue_session(session_id, "V-TEST-INVARIANT")
        assert response["status"] == "active"

    def test_validation_error_retry(self, runner):
        """Invalid input returns error and allows retry."""
        response = runner.start("create_validation")
        session_id = response["session_id"]

        # Skip to ask step
        while response.get("step", {}).get("type") == "query":
            response = runner.continue_session(session_id)

        # Provide invalid answer (doesn't match pattern)
        response = runner.continue_session(session_id, "invalid-name")

        assert response.get("error")
        assert response["status"] == "active"  # Can retry

    def test_abort_session(self, runner):
        """Abort mid-flow."""
        response = runner.start("create_validation")
        session_id = response["session_id"]

        response = runner.abort(session_id)
        assert response["status"] == "aborted"

    def test_complete_simple_flow(self, runner, simple_connectome_yaml):
        """Complete a simple connectome flow."""
        runner.register_connectome_yaml(simple_connectome_yaml)
        response = runner.start("simple_test")
        session_id = response["session_id"]

        # Answer name
        response = runner.continue_session(session_id, "TestUser")
        assert response["status"] == "active"

        # Answer priority
        response = runner.continue_session(session_id, "HIGH")

        # Should be complete (create step auto-executes)
        assert response["status"] == "complete"
        assert response.get("created")
        assert len(response["created"]["nodes"]) == 1
        assert response["created"]["nodes"][0]["name"] == "TestUser"

    def test_session_not_found(self, runner):
        """Error on invalid session ID."""
        response = runner.continue_session("invalid-id", "answer")
        assert response["status"] == "error"
        assert "not found" in response["error"].lower()

    def test_connectome_not_found(self, runner):
        """Error on invalid connectome name."""
        response = runner.start("nonexistent_connectome")
        assert response["status"] == "error"
        assert "not found" in response["error"].lower()


# =============================================================================
# INTEGRATION TESTS
# =============================================================================

class TestIntegration:
    """Integration tests for full flows."""

    def test_create_validation_flow(self, runner):
        """Test create_validation connectome end-to-end (without graph)."""
        response = runner.start("create_validation")
        session_id = response["session_id"]

        answers = {
            "ask_name": "V-TEST-EXAMPLE",
            "ask_criteria": "This must always be true for the test",
            "ask_priority": "HIGH",
            "ask_space": "space_building",
            "ask_behaviors": [],  # Empty list allowed
            "ask_failure_mode": "Test fails if this invariant is violated",
        }

        # Process through all steps
        while response["status"] == "active":
            step = response.get("step", {})
            step_id = step.get("step_id")

            if response.get("needs_input") and step_id in answers:
                response = runner.continue_session(session_id, answers[step_id])
            else:
                response = runner.continue_session(session_id)

        # Should complete
        assert response["status"] == "complete"

        # Check created nodes
        nodes = response["created"]["nodes"]
        assert len(nodes) >= 1

        validation_node = nodes[0]
        assert validation_node["type"] == "validation"
        assert validation_node["name"] == "V-TEST-EXAMPLE"
        assert validation_node["priority"] == "HIGH"

    def test_document_progress_flow(self, runner):
        """Test document_progress connectome."""
        response = runner.start(
            "document_progress",
            initial_context={"actor_id": "actor_test"}
        )
        session_id = response["session_id"]

        answers = {
            "ask_summary": "Implemented the connectome v0 system",
            "ask_affected": ["narrative_1", "narrative_2"],
            "ask_todos": ["Write more tests", "Add documentation"],
        }

        while response["status"] == "active":
            step = response.get("step", {})
            step_id = step.get("step_id")

            if response.get("needs_input") and step_id in answers:
                response = runner.continue_session(session_id, answers[step_id])
            else:
                response = runner.continue_session(session_id)

        assert response["status"] == "complete"

        # Should have created moment + 2 goal narratives
        nodes = response["created"]["nodes"]
        assert len(nodes) >= 3

        # Check goals were created
        goals = [n for n in nodes if n.get("type") == "goal"]
        assert len(goals) == 2


# =============================================================================
# RUN TESTS
# =============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
