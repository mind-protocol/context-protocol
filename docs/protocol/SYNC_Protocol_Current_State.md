# ngram Framework — Sync: Current State

```
LAST_UPDATED: 2025-12-19
UPDATED_BY: Codex (GPT-5)
STATUS: CANONICAL
```

---

## MATURITY

**What's canonical (v1):**
- 5 principles (architecture, verification, communication, quality, experience)
- 11 VIEWs covering full lifecycle
- CLI with init, validate, prompt, context
- Documentation process with maturity tracking

**What's still being designed:**
- Nothing currently

**What's proposed (v2+):**
- Drift detection (file watching)
- MCP tools
- PyPI publish

---

## CURRENT STATE

Protocol V1 complete and in use. Dogfooding on itself + Blood Ledger.

**What exists:**
- PROTOCOL.md — navigation (what to load, where to update, how to structure docs)
- PRINCIPLES.md — stance (5 principles: architecture, verification, communication, quality, experience)
- 11 VIEWs covering product development lifecycle
- 8 templates for documentation (including TEST)
- CLI package with `init`, `validate`, `prompt`, and `context` commands
- CLAUDE_ADDITION.md with motivation, principles summary, and lifecycle-ordered VIEWs
- Maturity tracking in SYNC (CANONICAL, DESIGNING, PROPOSED, DEPRECATED)
- Documentation process guidance (top-down/bottom-up, pruning cycle)
- Full documentation chain for protocol module (PATTERNS, BEHAVIORS, ALGORITHM, VALIDATION, IMPLEMENTATION, TEST, SYNC)

**Recent changes (2025-12-18):**
- Added protocol implementation documentation and corrected doc-link resolution issues.

**Recent changes (2025-12-19):**
- Split ALGORITHM and IMPLEMENTATION docs into folders for size control and clearer navigation.
- Compressed legacy sync details into archive notes for long-term reference.
- Added root overview stubs so validation still sees full chain files.
- Consolidated protocol ALGORITHM docs into a single overview and removed duplicate workflow/install files.

---

## HANDOFF: FOR AGENTS

**Your likely VIEW:** VIEW_Test_Write_Tests_And_Verify

**What needs testing:**
1. `pip install -e .` from repo root
2. `ngram init --dir /tmp/test-project`
3. Verify `.ngram/` created with:
   - PROTOCOL.md
   - PRINCIPLES.md (new!)
   - 9 VIEWs in views/
   - 7 templates in templates/
   - state/SYNC_Project_State.md
4. Verify .ngram/CLAUDE.md and AGENTS.md created with principles summary

**Key change since last handoff:**
PRINCIPLES.md now exists. Make sure it's copied during init.

---

## HANDOFF: FOR HUMAN

**Executive summary:**
Protocol V1 complete. Added PRINCIPLES.md capturing your working principles (architecture, verification, communication, quality). The protocol now has two core files: PROTOCOL.md for navigation, PRINCIPLES.md for stance.

**What changed:**
- PRINCIPLES.md created with four core stances from your document
- PROTOCOL.md updated to reference PRINCIPLES.md
- CLAUDE_ADDITION.md includes principles summary so agents see them immediately

**Ready for:**
- Testing the package installation
- Using on a real project (Blood Ledger?)

**Decisions made:**
- Principles in separate file (not embedded in PROTOCOL.md) — gives them space, follows "one solution per problem"
- Principles summary in CLAUDE_ADDITION.md — agents see them immediately without extra file load
- PROTOCOL.md references PRINCIPLES.md as "companion" — clear relationship

---

## STRUCTURE

```
.ngram/
├── PROTOCOL.md              # Navigation — what to load
├── PRINCIPLES.md            # Stance — how to work
├── views/                   # 9 task-specific VIEWs
├── templates/               # 7 doc templates
└── state/
    └── SYNC_Project_State.md
```

---

## POINTERS

| What | Where |
|------|-------|
| Protocol (navigation) | `templates/ngram/PROTOCOL.md` |
| Principles (stance) | `templates/ngram/PRINCIPLES.md` |
| CLI code | `ngram/cli.py` |
| CLAUDE addition | `templates/CLAUDE_ADDITION.md` |
| VIEWs | `templates/ngram/views/` |


---

## ARCHIVE

Older content archived to: `archive/SYNC_archive_2024-12.md`

---

## Agent Observations

### Remarks
- The protocol module docs were split to keep large files under the line threshold and improve navigation.

### Suggestions
- [ ] Re-run `ngram overview` to refresh `docs/map.md` after documentation reshuffles.

### Propositions
- Consider a short "Docs Index" note in `IMPLEMENTATION_Overview.md` if more splits happen.
