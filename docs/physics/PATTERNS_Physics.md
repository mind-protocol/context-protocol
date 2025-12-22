# Physics — Patterns: Why This Shape

```
STATUS: CANONICAL
UPDATED: 2024-12-18
```

---

## CHAIN

```
THIS:           PATTERNS_Physics.md (you are here)
BEHAVIORS:      ./BEHAVIORS_Physics.md
ALGORITHMS:
  - ./ALGORITHM_Physics.md      (Consolidated: energy, tick, canon, handlers, input, actions, QA, speed)
SCHEMA:         ../schema/SCHEMA_Moments.md
API:            ./API_Physics.md
VALIDATION:     ./VALIDATION_Physics.md
IMPLEMENTATION: ./IMPLEMENTATION_Physics.md
HEALTH:         ./HEALTH_Physics.md
SYNC:           ./SYNC_Physics.md
```

---

## THE PROBLEM

We need a world simulation that produces believable drama without hand-coded
timelines or omniscient schedulers. The system must decide what happens next
from the living graph itself, keep state authoritative, and avoid separate,
contradictory sources of truth across subsystems.

---

## THE PATTERN

Treat physics as a graph-native scheduler: energy, weight, and link topology
drive what actualizes. Every subsystem reads from and writes to the same
graph, so causality and canon emerge from shared structure instead of
external orchestration rules.

---

## PRINCIPLES

### Principle 1: Single source of truth

Graph state is authoritative; handlers, tick loops, and canon logic are
purely readers and writers that do not maintain parallel state.

### Principle 2: Continuous propagation

Energy always flows and decays, so the system never waits for a "start" cue
and never suspends causality between ticks.

### Principle 3: Potential before canon

Potential moments compete by weight and energy until they actualize into
canon, keeping the system probabilistic without being arbitrary.

### Principle 4: Consequences emerge from links

Link topology determines transfer, proximity, and gating, so structure
drives behavior without ad hoc condition checks.

---

## DEPENDENCIES

| Module | Why We Depend On It |
|--------|---------------------|
| `engine/physics/graph/**` | Supplies graph reads/writes for energy flow and flip detection. |
| `docs/schema/SCHEMA_Moments.md` | Defines the moment and link fields that physics assumes. |
| `docs/infrastructure/api/` | Feeds player input and surfaces physics outputs to clients. |

---

## INSPIRATIONS

Systems-first narrative engines, emergent simulation design, and graph-based
knowledge models where structure, not scripts, produces behavior. The tone
leans toward "living world" sandboxes rather than deterministic story trees.

---

## SCOPE

### In Scope

- Energy propagation, decay, and flip detection in the living graph.
- Canon actualization of moments and sequencing through THEN links.
- Scheduler behavior derived from weights and proximity rules.

### Out of Scope

- LLM prompt design for narration or character voice (see narrator module).
- Visual presentation concerns (see frontend scene/map modules).
- World data ingestion or scraping pipelines (see world-scraping module).

---

## Core Principle

**The graph is the only truth.**

Everything else — handlers, ticks, canon — are processes that read from and write to the graph. No process owns state. No process is authoritative except through what it writes to the graph, so duplication is treated as a bug.

---

## P1: Potential vs Actual

Moments exist in two modes:

| Mode | Meaning | Graph State |
|------|---------|-------------|
| **Potential** | Could happen | Has weight, competes with other potentials |
| **Actual** | Did happen | Is canon, has THEN links to what came before |

No process decides what happens. Processes propose potentials. Physics determines what actualizes.

---

## P2: The Graph Is Alive

The graph is a mind. It doesn't stop thinking.

Energy always flows. Weights always decay. Propagation always happens. Player input is a perturbation, not an ignition.

**What we control:**
- Tick rate (speed setting)
- When we sample for display
- When we inject energy (input, world events, handler outputs)

**What we don't control:**
- "Starting" the cascade — it's always running
- "Stopping" the cascade — it doesn't stop

**Graph states:**

| State | Meaning |
|-------|---------|
| **Active** | High energy, many flips, drama unfolding |
| **Quiet** | Low energy, few flips, system settled |
| **Critical** | Energy building, thresholds approaching, tension rising |

But never **stopped**.

---

## P3: Everything Is Moments

There are no separate systems for dialogue, movement, actions, thoughts.

| What | How It's Represented |
|------|---------------------|
| Speech | Moment with type: dialogue |
| Thought | Moment with type: thought |
| Movement | Moment with type: action, action: travel |
| Combat | Moment with type: action, action: attack |
| Observation | Moment with type: narration |

The graph doesn't distinguish structurally — all are Moment nodes.
Physics doesn't distinguish — all propagate energy the same way.

**But:** Action Processing does distinguish. Moments with `action` field modify world state. Thoughts don't. The moment type determines *consequences*, not storage or propagation.

---

## P4: Moments Are Specific, Narratives Emerge

A moment: "That decision at the crossing cost us."
Another moment: "He's led us wrong before."
Another moment: "Someone else should lead."

These accumulate. Their links converge. A narrative emerges: "Leadership is contested."

**Moments are concrete.** They have text, speaker, time.
**Narratives are patterns.** They're recognized across moments, not authored directly.

---

## P5: Energy Must Land

When energy enters the system, it must go somewhere.

```
Player speaks
  → energy flows to all who heard
  → if no relevant moments exist → energy accumulates on characters
  → if no character flips → energy returns to player character
  → player character always has a handler → something always happens
```

There is no "nothing happens." There is "the silence stretches."

---

## P6: Sequential Actions, Parallel Potentials

**Parallel:** Many character handlers can generate potentials simultaneously.
**Sequential:** Actions that modify world state resolve one at a time.

Aldric and Mildred can both think at once.
Aldric and Mildred cannot both grab the sword at once.

---

## P7: The World Moves Without You

The system does not require player input to advance.

Player can press "Play" and observe.
Time passes. Pressure builds. Characters think. Events unfold.

The player is a participant, not a driver.

---

## P8: Time Is Elastic

The player controls the speed of time, not the content.

| Speed | Feel |
|-------|------|
| 1x | Every moment breathes |
| 2x | Time compresses but conversation persists |
| 3x | World rushes until drama demands attention |

The player is a viewer with a remote. Fast-forward through the boring parts. The system knows when to snap back.

**Speed changes rendering, not reality.** Canon is canon regardless of display speed.

---

## P9: Physics Is The Scheduler

No arbitrary triggers. No cooldowns. No caps.

Character important and close? More energy per tick → flips more often → handler runs more.
Character distant or minor? Less energy → flips rarely → handler runs rarely.

**Importance is derived, not assigned:**
```
importance = sum of weights of all moments ATTACHED_TO this character
```

Character with many high-weight potentials = important right now.
Character with few/low potentials = less important right now.

**Proximity is binary:**
```
proximity = 1.0 if character AT player_location else 0.0
```

Same location = full proximity. Different location = World Runner's domain.

---

## P10: Simultaneous Actions Are Drama

**Old thinking:** Aldric grabs sword + Mildred grabs sword = mutex = resolve conflict.

**New thinking:** Both actualize. Both canon.

```
"Aldric reaches for the sword."
"Mildred's hand closes on the hilt at the same moment."
```

That's not a problem. That's a scene. The consequences play out — struggle, tension, drama.

**Actual mutex (rare):** Same character, two incompatible actions, same tick.
- Aldric "walks east" AND Aldric "walks west"
- Resolution: Higher weight wins. Lower becomes potential for next tick.

Most "conflicts" are actually drama to embrace.

---

## What This Pattern Does NOT Solve

- Does not prevent bad drama (but makes state visible)
- Does not guarantee interesting content (handlers must produce it)
- Does not eliminate LLM latency (but pre-generation helps)
- Does not replace thinking (but structures it)

---

## The Philosophy

**Structure creates behavior.**

Moments don't have "speaker" because speakership is a relationship, not an attribute.
Conversations don't have "shape" because shape emerges from links.
Scenes don't exist because presence is computed, not declared.
Cascades don't have boundaries because the graph never stops.

**The graph is the single source of truth. No files. No trees. Just moments, links, and physics.**

---

*"The narrator weaves possibilities. Physics determines what actualizes. The graph remembers everything."*

---

## MARKERS

- How aggressively should energy decay when the world is in a "quiet" state?
- What is the right threshold for flipping from potential to canon in dense scenes?
- When do concurrent actions become mutually exclusive vs. staged drama?
