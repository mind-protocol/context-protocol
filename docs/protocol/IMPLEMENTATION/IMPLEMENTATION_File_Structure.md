# ngram Framework — Implementation: File Structure

```
STATUS: STABLE
CREATED: 2025-12-18
```

---

## CHAIN

```
PATTERNS:        ../PATTERNS_Bidirectional_Documentation_Chain_For_AI_Agents.md
BEHAVIORS:       ../BEHAVIORS_Observable_Protocol_Effects.md
ALGORITHM:       ../ALGORITHM_Overview.md
VALIDATION:      ../VALIDATION_Protocol_Invariants.md
IMPLEMENTATION:  ../IMPLEMENTATION_Overview.md
THIS:            ./IMPLEMENTATION_File_Structure.md
TEST:            ../TEST_Protocol_Test_Cases.md
SYNC:            ../SYNC_Protocol_Current_State.md
```

---

## TEMPLATE DIRECTORY (SOURCE OF TRUTH)

```
templates/ngram/
├── PROTOCOL.md
├── PRINCIPLES.md
├── views/                 # 11 VIEW files
├── templates/             # 9 doc templates
└── state/
    └── SYNC_Project_State.md
```

---

## INSTALLED DIRECTORY (TARGET PROJECT)

```
.ngram/
├── PROTOCOL.md
├── PRINCIPLES.md
├── views/
├── templates/
├── modules.yaml
├── state/
│   ├── SYNC_Project_State.md
│   └── SYNC_Project_Health.md
└── traces/                # Optional agent logs
```

---

## FILE RESPONSIBILITIES

| File Pattern | Purpose | When Loaded |
|--------------|---------|-------------|
| PROTOCOL.md | Navigation rules | Session start |
| PRINCIPLES.md | Working stance | Session start |
| VIEW_*.md | Task instructions | Based on task |
| *_TEMPLATE.md | Doc scaffolding | When creating docs |
| SYNC_Project_State.md | Project state and handoff | Session start |
| SYNC_Project_Health.md | Doctor output | After `doctor` |
| modules.yaml | Code ↔ docs mapping | CLI and tooling |

---

## BOOTSTRAP FILES

The protocol is surfaced through:
- `.ngram/CLAUDE.md` (includes templates/CLAUDE_ADDITION.md, PRINCIPLES.md, PROTOCOL.md)
- Root `AGENTS.md` mirroring `.ngram/CLAUDE.md` plus `templates/CODEX_SYSTEM_PROMPT_ADDITION.md`
- `.ngram/agents/manager/AGENTS.md` for manager role
