# VIEW: Ingest — Process Raw Data Sources

**You have raw data (chat logs, PDFs, research, specs) that needs to be understood and integrated into the project.**

---

## WHY THIS VIEW EXISTS

Projects don't start from nothing. They start from:
- Conversations (chat logs, meeting notes)
- Documents (PDFs, specs, research papers)
- Existing code or examples
- Ideas scattered across multiple sources

This raw material lives in `data/` but isn't yet usable. Without processing:
- Key insights get lost in noise
- Context isn't connected to where it's needed
- Implementation starts without full understanding
- Important constraints hide in unread documents

This view is about transforming raw data into actionable project context.

---

## CONTEXT TO LOAD

**FIRST: Read all documentation listed below before processing data.** Understanding existing structure prevents duplication. Do not skip this step.

### Then: Understand What Exists

```
data/                          — scan everything
.ngram/state/SYNC_Project_State.md  — current project context
```

### Then: Existing Docs (if any)

```
docs/                          — what's already documented
```

You need to know what exists so you don't duplicate or contradict.

---

## THE WORK

### Phase 0: Source Determination (Human-led)

Before ingestion begins, the human must determine which raw data sources are relevant to the project and place them in `data/`.

**The human identifies:**
- Which chat logs contain the most important decisions.
- Which research papers or articles define the domain constraints.
- Which existing specifications or legacy documentation should be integrated.
- Which URLs or external data sources are authoritative.

**Action:** The human populates the `data/` directory with these selected items.

### Phase 1: Survey

Scan `data/` and create an inventory:

| File/Folder | Type | Description | Priority |
|-------------|------|-------------|----------|
| `chat_log_2024-12-15.md` | Conversation | Initial design discussion | High |
| `research.pdf` | Document | Academic paper on X | Medium |
| `notes/` | Mixed | Scattered thoughts | Low |

**Classify by type:**
- Conversations (chats, meetings, discussions)
- Specifications (requirements, constraints, acceptance criteria)
- Research (papers, articles, reference material)
- Examples (code, implementations, inspiration)
- Raw ideas (brainstorms, possibilities, maybes)

### Phase 2: Extract

For each high-priority item, extract:

**Key decisions:** What was decided? By whom? Why?

**Constraints:** What must be true? What can't change?

**Requirements:** What needs to exist? What behavior is expected?

**Open questions:** What's unresolved? What needs clarification?

**Concepts:** What domain concepts appear? How are they defined?

### Phase 3: Integrate

Transform extracted information into project artifacts:

| Extracted | Becomes |
|-----------|---------|
| Design decisions | PATTERNS_*.md |
| Requirements | BEHAVIORS_*.md |
| Algorithms/procedures | ALGORITHM_*.md |
| Constraints/invariants | VALIDATION_*.md |
| Cross-cutting concepts | docs/concepts/CONCEPT_*.md |
| Current state | SYNC_*.md updates |

### Phase 4: Triage Remainder

For material you didn't fully process:
- Note what exists and why it wasn't prioritized
- Mark as "to process later" in SYNC
- Don't lose track of it

---

## OUTPUT

After ingestion, you should have:

1. **Inventory:** What's in `data/`, classified and prioritized
2. **Extracted insights:** Key decisions, constraints, requirements documented
3. **Updated docs:** New PATTERNS, BEHAVIORS, etc. as appropriate
4. **Updated SYNC:** What was processed, what remains, what's next
5. **Triage notes:** What was skipped and why

---

## HANDOFF

**For next agent:**
- Which data was processed vs skipped
- What docs were created/updated
- What questions emerged that need human input
- Recommended VIEW for continuing (likely Specify or Implement)

**For human:**
- Summary of what was extracted
- Key decisions found (verify these are correct)
- Open questions that need your input
- Anything surprising or contradictory

---

## VERIFICATION

- [ ] All files in `data/` accounted for (processed or triaged)
- [ ] High-priority items fully extracted
- [ ] New docs follow templates and conventions
- [ ] SYNC updated with ingestion results
- [ ] No key insights lost — everything important is now in docs

---

## TIPS

**Don't process everything.** Triage ruthlessly. Some data is reference material, not active input.

**Preserve provenance.** When creating docs from data, note the source: "Extracted from data/chat_2024-12-15.md"

**Flag contradictions.** If sources disagree, don't resolve silently. Document the conflict and flag for human.

**Conversations are gold.** Chat logs often contain decisions that never made it to formal docs. Extract them.

**PDFs lie.** Old documents may describe intent that never got implemented, or old designs that changed. Cross-reference with reality.

**Reference sources in PATTERNS.** Always list the processed data files, URLs, or other sources in the `# DATA` section of the relevant module's `PATTERNS_*.md` file. This maintains the provenance and allows future agents/humans to re-verify the design rationale.
