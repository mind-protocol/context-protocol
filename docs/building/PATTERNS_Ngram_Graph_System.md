# ngram Graph System — Design Patterns

## Core Philosophy

**The graph runs the dev process.**

Docs dissolve into Narratives. Tasks emerge from energy. Agents differentiate through accumulated state. The world ticks continuously. Physics decides what's relevant.

## Key Decisions

### 1. Same Rules for All Actors

```
actor: human | agent
```

No special pump. Every actor:
- Exists in a Space
- Generates energy based on proximity
- Creates Moments
- Creates Narratives
- Accumulates beliefs/memories through links

Differentiation emerges from graph state, not hardcoded roles.

### 2. Docs Are Views, Graph Is Truth

```
markdown file → rendered from Narratives
change → creates Moment + updates Narrative
```

The doc chain (OBJECTIVES → PATTERNS → VALIDATION → etc.) becomes Narrative nodes linked by `relates`. Markdown files are regenerated views, not source of truth.

Ingest existing docs → atomic sections become Narratives → graph is canonical.

### 3. Space = Context Loader

```yaml
space:
  type: module | feature | focus
  contains: [narratives, moments, things, actors]
```

Actor enters Space → loads hot Narratives as context. Space determines what's relevant, not explicit instructions.

Actors can be in multiple Spaces. Energy flows through Space containment.

### 4. Narratives Mirror Doc Chain

```yaml
narrative:
  type: objectif | pattern | behavior | algorithm | validation | implementation | health | sync | goal | rationale | memory
```

**Doc chain types** (from ingested docs):

| Type | What It Captures |
|------|------------------|
| `objectif` | Primary objectives, non-objectives, tradeoffs |
| `pattern` | Design decisions, key patterns |
| `behavior` | Observable effects, what it should do |
| `algorithm` | Procedures, how it works |
| `validation` | Invariants, what must be true |
| `implementation` | Code architecture, docking points |
| `health` | Verification mechanics |
| `sync` | Current state, handoffs |

**Emergent types** (from work):

| Type | Created When | Example |
|------|--------------|---------|
| `goal` | Work needed | "Ship health checkers" |
| `rationale` | Work completed | "Simplified 14 link types to 9" |
| `memory` | Past event worth retaining | "We tried X, it failed" |

Narratives link via `relates` with direction: `supports | contradicts | elaborates | supersedes`.

### 5. Moments Are Ephemeral, Strength Is Memory

```
Moment: what happened (high energy, decays)
Link strength: what mattered (accumulates, persists)
```

Moments flow through, heat up links, then cool. Strength remains. Old work resurfaces when Space reactivated — not through Moment recall, but through high-strength links.

### 6. World Runs Continuously

```
tick_speed: x1 | x2 | x3
```

Not event-driven. World runner ticks at chosen speed. All actors generate energy each tick. Hot areas surface. Agents get triggered.

Human is an actor in the world, not the controller of it.

### 7. Many Agents, No Specialization

```
agent_count: 6+  # minimum
specialization: emergent from graph state
```

Agents start similar. Beliefs, memories, Space affinity accumulate through work. One agent gravitates toward physics, another toward docs. Not designed — discovered.

### 8. Energy Determines Activation

```python
if narrative.energy > ACTIVATION_THRESHOLD:
    trigger_linked_agents(narrative)
```

No task queues. No explicit assignment. Hot Narratives in an agent's Space = work surfaces. Agent works → creates Moments → energy flows → next hot thing emerges.

## What's NOT in This System

- **Explicit task lists** — Narratives with energy are implicit tasks
- **Agent instructions** — Context is the instruction
- **Doc versioning** — Moments track changes, not file versions
- **Coordination layer** — Physics handles it
- **External triggers** — GitHub/Slack etc. come later

## Invariants

- All actors generate energy (no passive observers)
- All Narratives can become goals (type is semantic, not behavioral)
- Spaces contain, not own (actors can be in multiple)
- Moments decay, strength accumulates
- World ticks whether or not human is active

## Open Patterns (Unresolved)

- **Space granularity** — per module? per objective? per feature? TBD through use.
- **Agent spawn** — fixed 6? dynamic based on load? Start fixed, evolve.
- **Narrative lifecycle** — when does goal become "done"? Physics (energy → 0) or explicit?

---

## MARKERS

<!-- @ngram:escalation Multiple agents triggered by same Moment — who goes first? Energy split? Sequential? Race condition risk? -->
<!-- @ngram:escalation Narrative in multiple Spaces via multiple contains links — does it appear in both contexts? Energy split between Spaces? -->
<!-- @ngram:escalation Bootstrap problem — first Moment creation before agents exist. Human seeds initial state, but how does first agent trigger happen? -->
<!-- @ngram:escalation Agent "leaving" a Space — explicit move action? Or just add to new Space? Can agent be in 0 Spaces? -->
<!-- @ngram:escalation Strength accumulation without bound — over years, does everything become max strength? Need soft cap or decay? -->

<!-- @ngram:proposition Use embeddings to auto-create relates links between semantically similar Narratives -->
<!-- @ngram:proposition Track agent "personality vector" derived from their accumulated beliefs/memories for observability -->
<!-- @ngram:proposition Explicit "focus" command where human enters Space (like cd) to concentrate energy injection -->
<!-- @ngram:proposition "Narrative merge" when two Narratives become redundant — physics-driven consolidation? -->
<!-- @ngram:proposition Agent can "flag" a Narrative for human attention by boosting its energy artificially -->
