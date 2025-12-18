# Context Protocol

**A context management protocol for AI agents working on code.**

---

## The Problem

AI agents have limited context windows. They can't load everything. They need:
- The RIGHT context for THIS task
- To know what to update after changes  
- To not lose information across sessions
- To navigate codebases without hallucinating structure

## The Solution

A protocol that tells agents:
1. **What to load** for their current task
2. **What to focus on** vs ignore
3. **What to update** when done
4. **Where to find things** they need

---

## Quick Start

```bash
# Install
pip install context-protocol

# Initialize in your project
context-protocol init

# Check protocol health
context-protocol validate

# Check project health (monoliths, stale docs, etc.)
context-protocol doctor

# Get documentation context for a file
context-protocol context src/your_file.py

# Generate bootstrap prompt for LLM
context-protocol prompt
```

After installation, your project will have:

```
your-project/
├── CLAUDE.md                    # Updated with protocol bootstrap
└── .context-protocol/
    ├── PROTOCOL.md              # Core rules (agents read this)
    ├── PRINCIPLES.md            # Working principles (how to work well)
    ├── views/                   # Task-specific context instructions (11 VIEWs)
    ├── templates/               # Templates for documentation
    └── state/
        └── SYNC_Project_State.md  # Current project state
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `context-protocol init` | Initialize protocol in project |
| `context-protocol validate` | Check protocol invariants |
| `context-protocol doctor` | Project health check (monoliths, stale docs) |
| `context-protocol context <file>` | Get doc context for a file |
| `context-protocol prompt` | Generate LLM bootstrap prompt |

### Doctor Command

The doctor command checks project health:

```bash
context-protocol doctor              # Full report
context-protocol doctor --level critical  # Only critical issues
context-protocol doctor --format json     # JSON output
```

Checks for:
- **Monolith files** (>500 lines code, >1000 lines docs)
- **Undocumented code** directories
- **Stale SYNC files** (>14 days old)
- **Placeholder docs** (unfilled templates)
- **Incomplete doc chains**
- **Missing DOCS: references**

---

## How It Works

### 1. Bootstrap (CLAUDE.md)

Your CLAUDE.md points agents to the protocol:

```markdown
## Context Protocol

Before any task, read: .context-protocol/PROTOCOL.md
For task-specific context: .context-protocol/views/
```

### 2. Protocol (PROTOCOL.md)

Tiny set of rules every agent follows:
- Load the right VIEW for your task
- Read relevant docs before changing code
- Update SYNC.md after changes
- Create docs if they don't exist

### 3. Views (Task Instructions)

Each VIEW tells the agent exactly what to load:

```markdown
# VIEW: Implement

## LOAD FIRST
1. .context-protocol/state/SYNC.md
2. docs/{area}/{module}/PATTERNS_*.md
3. docs/{area}/{module}/SYNC_*.md

## AFTER CHANGES
Update: docs/{area}/{module}/SYNC_*.md
```

### 4. State (SYNC.md)

Living document tracking current state:
- What's working
- What's in progress
- Handoffs for next session
- TODOs

---

## Documentation Chain

The protocol encourages a documentation chain for each module:

```
docs/{area}/{module}/
├── PATTERNS_{Design_Philosophy}.md      # WHY this shape
├── BEHAVIORS_{Observable_Effects}.md    # WHAT it should do
├── ALGORITHM_{Procedures_Logic}.md      # HOW it works
├── VALIDATION_{Invariants_Tests}.md     # HOW to verify
└── SYNC_{Current_State}.md              # WHERE we are now
```

Agents navigate: Code ↔ Docs bidirectionally.

---

## Key Concepts

### Module
A coherent responsibility with clear interface. May be one file or several.

### Area  
A cluster of related modules. Organizational grouping.

### View
Task-specific context loading instructions. Agent loads ONE view for their task.

### Sync
Current state document. Updated after every change. Enables handoffs.

### Concept
Cross-cutting idea that spans modules. Documented separately with TOUCHES index.

---

## Design Principles

1. **Agents don't load everything** — They load ONE view for their task
2. **Docs before code** — Understand before changing
3. **State is explicit** — SYNC.md tracks what's happening
4. **Names are descriptive** — File names tell agents what's inside
5. **Protocol is substrate-agnostic** — Works with Claude, Cursor, Aider, any agent

---

## Full Documentation

See `docs/` for:
- Protocol specification (using the protocol itself)
- Templates for all file types
- Concepts explained

---

## License

MIT

---

## Contributing

This protocol is being developed by Mind Protocol as part of AI-human symbiosis infrastructure.

Issues and PRs welcome.
