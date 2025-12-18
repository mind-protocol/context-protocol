# ngram

**Memory for AI agents.** Protocol for context, state, and handoffs across sessions.

---

## The Problem

AI agents are stateless. Every session starts from zero. They:
- Can't load everything (limited context window)
- Lose state between sessions
- Hallucinate structure they haven't seen
- Can't hand off to the next agent

## The Solution

A protocol that makes sessions compound instead of restart:
1. **VIEWs** tell agents what to load for their current task
2. **SYNC** files track state so agents remember
3. **Handoffs** let agents communicate across sessions

---

## Quick Start

```bash
# Install
pip install ngram

# Initialize in your project
ngram init

# Check protocol health
ngram validate

# Check project health (monoliths, stale docs, etc.)
ngram doctor

# Auto-fix issues with agents
ngram repair

# Get documentation context for a file
ngram context src/your_file.py

# Generate bootstrap prompt for LLM
ngram prompt
```

After initialization:

```
your-project/
├── CLAUDE.md                    # Updated with protocol bootstrap
└── .ngram/
    ├── PROTOCOL.md              # Core rules (agents read this)
    ├── PRINCIPLES.md            # Working principles
    ├── views/                   # Task-specific context instructions
    ├── templates/               # Templates for documentation
    └── state/
        └── SYNC_Project_State.md  # Current project state
```

---

## CLI Commands

| Command | Description |
|---------|-------------|
| `ngram init` | Initialize protocol in project |
| `ngram validate` | Check protocol invariants |
| `ngram doctor` | Project health check |
| `ngram repair` | Auto-fix issues with agents |
| `ngram context <file>` | Get doc context for a file |
| `ngram sync` | Show SYNC file status |
| `ngram prompt` | Generate LLM bootstrap prompt |

### Doctor Command

```bash
ngram doctor              # Full report
ngram doctor --level critical  # Only critical issues
ngram doctor --format json     # JSON output
```

Checks for:
- **Monolith files** (>500 lines code, >1000 lines docs)
- **Undocumented code** directories
- **Stale SYNC files** (>14 days old)
- **Placeholder docs** (unfilled templates)
- **Incomplete doc chains**

### Repair Command

```bash
ngram repair              # Fix all issues
ngram repair --max 3      # Limit to 3 agents
ngram repair --dry-run    # Preview what would be fixed
```

Spawns Claude Code agents to autonomously fix issues found by doctor.

---

## How It Works

### 1. Bootstrap (CLAUDE.md)

Points agents to the protocol:

```markdown
# ngram

Before any task, read: .ngram/PROTOCOL.md
For task-specific context: .ngram/views/
```

### 2. Views (Task Instructions)

Each VIEW tells agents what to load for a specific task type:

```markdown
# VIEW: Implement

## LOAD FIRST
1. .ngram/state/SYNC_Project_State.md
2. docs/{area}/{module}/PATTERNS_*.md
3. docs/{area}/{module}/SYNC_*.md

## AFTER CHANGES
Update: docs/{area}/{module}/SYNC_*.md
```

Available views: Implement, Debug, Test, Review, Refactor, Document, Onboard, and more.

### 3. State (SYNC files)

Living documents tracking current state:
- What's working
- What's in progress
- Handoffs for next session

This is how agents "remember" across sessions.

---

## Documentation Chain

For each module:

```
docs/{area}/{module}/
├── PATTERNS_*.md    # WHY this design
├── BEHAVIORS_*.md   # WHAT it should do
├── ALGORITHM_*.md   # HOW it works
├── VALIDATION_*.md  # HOW to verify
└── SYNC_*.md        # WHERE we are now
```

Agents navigate: Code ↔ Docs bidirectionally.

---

## Key Concepts

| Concept | Description |
|---------|-------------|
| **View** | Task-specific context loading instructions |
| **Sync** | State document updated after every change |
| **Module** | Coherent responsibility with clear interface |
| **Area** | Cluster of related modules |
| **Concept** | Cross-cutting idea spanning modules |

---

## Design Principles

1. **Agents don't load everything** — They load ONE view for their task
2. **State is explicit** — SYNC files track what's happening
3. **Sessions compound** — Work accumulates instead of restarting
4. **Protocol over intelligence** — Structure enables capability

---

## License

MIT

---

## Contributing

Developed by Mind Protocol. Issues and PRs welcome.
