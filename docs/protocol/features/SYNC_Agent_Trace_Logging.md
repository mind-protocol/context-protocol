# Agent Trace Logging — Sync: Current State

```
LAST_UPDATED: 2025-12-16
UPDATED_BY: Claude (Opus 4.5)
STATUS: DESIGNING
```

---

## MATURITY

**What's canonical (v1):**
- Nothing yet — feature is being designed

**What's still being designed:**
- Trace file format
- CLI commands (trace, trace --detail, trace clear)
- Integration with context command
- Analysis/summary output

**What's proposed (v2+):**
- File watcher for automatic tracing
- SYNC injection of usage stats
- Cross-session analysis

---

## CURRENT STATE

Documentation complete. Ready for implementation.

Docs created:
- PATTERNS: Design decisions and rationale
- BEHAVIORS: Observable effects and command interface

---

## IMPLEMENTATION PLAN

### Phase 1: Basic tracing (MVP)

1. Add trace logging to `ngram context` command
2. Create `.ngram/traces/` directory on first trace
3. Write JSONL trace entries
4. Add `ngram trace` command for basic summary

### Phase 2: Analysis

5. Add `--detail` flag for raw trace output
6. Add summary statistics (most loaded, least loaded)
7. Add `--clear` command for cleanup

### Phase 3: Integration

8. Integrate with validate (stale doc detection)
9. Add `trace log <file>` for agent self-reporting
10. Optional: file watcher mode

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Implement

**Start here:**
1. Read BEHAVIORS to understand the interface
2. Implement Phase 1 in cli.py
3. Test with `ngram context` on a file
4. Verify trace file created

**Key files:**
- `src/ngram/cli.py` — add trace functions
- `.ngram/traces/` — output location

---

## TODO

### Immediate

- [ ] Implement `log_trace()` function
- [ ] Add tracing to `context` command
- [ ] Implement `trace` command (basic summary)

### Later

- [ ] `trace --detail` flag
- [ ] `trace clear` command
- [ ] Navigation pattern detection
- [ ] Stale doc detection integration

---

## OPEN QUESTIONS

- Should we trace validate runs? (might be noisy)
- Session ID: auto-generate or let agent provide?
- Retention policy: auto-delete after N days?
