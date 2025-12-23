# Connectome v0 Tests

Tests for the Connectome structured dialogue system.

## What is Connectome?

Connectome provides structured dialogues for graph interactions:
- Agent calls connectome tool
- Tool returns step (ask/query/create/update)
- Agent responds
- Tool validates/executes
- Next step or completion

## Running Tests

```bash
# From repo root
pytest tests/connectome_v0/ -v

# Specific test
pytest tests/connectome_v0/test_connectome_runner.py::TestRunner::test_complete_simple_flow -v
```

## Example Connectomes

### create_validation.yaml
Creates a validation invariant with:
- Query available spaces and behaviors
- Ask for name, criteria, priority
- Create narrative node
- Create links to space and behaviors

### explore_escalation.yaml
Load and resolve an escalation:
- Query escalation details
- Query related nodes
- Ask for action (resolve/defer/escalate/needs_info)
- Branch to appropriate handler
- Update escalation status

### document_progress.yaml
Record work progress:
- Query recent moments
- Ask for summary, affected nodes, TODOs
- Create progress moment
- Create goal narratives for TODOs
- Create links

## Test Categories

- **Loader**: YAML parsing, step extraction
- **Validation**: Input validation (string, enum, id_list, etc.)
- **Templates**: Reference expansion, filters
- **Session**: State management, lifecycle
- **Runner**: Step processing, flow control
- **Integration**: End-to-end flows

## Without Graph

Tests run without FalkorDB connection. Query steps return empty results,
create/update steps record what would be created but don't persist.

For live tests with graph, see `tools/test_connectome_live.py`.
