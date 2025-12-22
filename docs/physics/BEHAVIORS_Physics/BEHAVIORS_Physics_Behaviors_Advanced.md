# Physics — Behaviors: Extended Interactions

```
STATUS: CANONICAL
UPDATED: 2024-12-18
```

---

## CHAIN

```
PATTERNS:       ../PATTERNS_Physics.md
BEHAVIORS:      ../BEHAVIORS_Physics.md
THIS:           BEHAVIORS_Physics_Behaviors_Advanced.md (you are here)
ALGORITHMS:
  - ../ALGORITHM_Physics.md      (Consolidated: energy, tick, canon, handlers, input, actions, QA, speed)
SCHEMA:         ../../schema/SCHEMA_Moments.md
API:            ../API_Physics.md
VALIDATION:     ../VALIDATION_Physics.md
IMPLEMENTATION: ../IMPLEMENTATION_Physics.md
HEALTH:         ../HEALTH_Physics.md
SYNC:           ../SYNC_Physics.md
```

---

## Extended Behaviors

Details below continue from the overview doc.

## B7: Actions Have Consequences

A moment with an `action` field doesn't just display.
It changes the graph.

| Action | What It Modifies |
|--------|------------------|
| travel | Character AT links |
| take | Thing AT/CARRIES links |
| attack | Health, relationships, tension |
| give | Possession links |
| speak | (no state change, just moment) |

Actions are processed sequentially to prevent conflicts.

### Action Queue

```
Moment with action: travel actualizes
  → enters action queue
  → processed: character AT link updated
  → consequences generated (arrival moment, witness reactions)
  → consequences enter graph with energy
```

---

## B8: Cascades Create Drama

One actualization triggers another.

### Example

```
Aldric confesses (weight crosses threshold)
  → energy propagates to witnesses
  → Mildred's "shock" potential crosses threshold
  → Mildred reacts
  → energy propagates
  → Godwin's "intervention" potential crosses threshold
  → Godwin intervenes
  → tension escalates
```

Player watches dominoes fall.
Player can intervene (inject energy via input) or observe (let physics continue).

### The "Next" Button

Player can press "Next" to advance to next canon moment.
If queue empty, triggers physics tick.
If still empty after tick, shows "waiting" state or player character observation.

---

## B9: Characters Have Opinions About Each Other

Character handlers observe other characters' moments.
They form opinions (new potentials linking to those characters).

### Examples

- "Aldric speaks well" — positive potential linking to Aldric
- "Mildred is hiding something" — suspicious potential linking to Mildred
- "I don't trust Godwin" — distrust potential linking to Godwin

These accumulate into relationships.

### How It Works

```
Aldric speaks (moment actualizes)
  → Mildred witnesses (energy propagates)
  → Mildred's handler runs
  → Handler has context: "Aldric just said X"
  → Handler generates opinion potential: "He's right about the Normans"
  → Opinion enters graph, linked to Aldric
```

Over time, these opinions form the relationship graph.

---

## B10: The World Continues Elsewhere

While player is at the camp, York still exists.
World Runner handles other locations.
Characters there have their own physics.
News can arrive.

### Example

```
Player at camp.
York under siege (World Runner processing).
Tension in York crosses threshold.
"City falls" moment actualizes in York.
News moment generated: "A rider from York. The city has fallen."
News travels to player's location.
Player learns of event.
```

The player's location is not the only location.

### Isolation

World Runner and player's location are isolated.
No concurrent writes to same nodes.
News travels through moments, not shared state.

---

## B11: The Snap

Player is skipping through time at 3x.
Blur, motion, streaming text.
Suddenly: an interrupt.
The world freezes. A beat of silence.
Then: clarity. A moment demands attention.

### The Three Phases

**Phase 1: Running (3x)**
- Motion blur effect
- Muted colors
- Text small, streaming upward, fading fast

**Phase 2: The Beat**
- Screen sharpens (freeze)
- Silence — 300-500ms pause
- Nothing displays
- Tension in the gap

**Phase 3: Arrival (1x)**
- Crystal clear, full color
- Interrupt moment appears
- Large, centered, deliberate

The pause is where dread lives. "Something's happening."

### Interrupt Conditions

| Interrupt Type | Definition |
|----------------|------------|
| Direct address | Player character's name in REFERENCES |
| Combat | Moment with action: attack becomes canon |
| Major arrival | Character with importance > 0.7 enters scene |
| Tension boils | Detected tension pressure > 0.9 (computed from structure) |
| Decision point | Moment with multiple CAN_LEAD_TO from player |
| Discovery | Narrative node created with player in WITNESSED_BY |
| Danger | Moment with THREATENS → player or companion |

All weight-based or link-based. No magic.

---

## B12: Journey Conversations

At 2x, time compresses but emotional beats survive.

### Example

```
The road stretches. (montage, muted)
"I never told you about my brother." (conversation, vivid)
The sun sets. (montage, muted)
"What happened?" (conversation, vivid)
You make camp. (montage, muted)
"The Normans." (conversation, vivid)
```

Two things at once: travel and intimacy. Like film. A day passes in minutes, but the conversation is whole.

### Display Distinction at 2x

| Type | Visual Style |
|------|--------------|
| World/montage | Muted color, smaller, italic, flows upward |
| Conversation | Full color, larger, centered, pauses for reading |

### How It Works

Same handlers, different framing.

At 2x, character handlers still run on flip. They're prompted differently:

```
Context: You're on a journey.
Generate brief atmospheric moments, not full dialogue.
Unless something important needs to be said.
```

No separate "montage system." Same handlers, context-aware output.

---

## INPUTS / OUTPUTS

**Inputs:** player input text, current graph state (moments, links, weights),
tick cadence (speed 1x/2x/3x), and handler output moments generated on flips.

**Outputs:** updated graph weights/energies, new or actualized moments,
queued actions (travel, take, attack), and frontend-visible moments/events
produced by the canon and display pipeline.

---

## EDGE CASES

- **No relevant potentials:** energy returns to the player character and the
  handler produces a narrated silence instead of dropping the input.
- **Simultaneous incompatible actions by same character:** higher weight wins
  this tick; the lower-weight action remains potential for later ticks.
- **Empty action queue after a tick:** the UI shows waiting state or narrates
  the absence of response rather than faking progress.

---

## ANTI-BEHAVIORS

- **No "nothing happens":** inputs must always land in a narrated response or
  a visible lack-of-response moment, never a silent UI stall.
- **No single-speaker monopoly:** multi-participant replies should surface by
  weight order instead of forcing one NPC to respond exclusively.
- **No parallel world-state writes:** concurrent location physics must not
  mutate the same nodes; remote updates arrive via news moments.

---

## MARKERS

<!-- @ngram:escalation How should energy routing behave when a named character is present -->
  but asleep or otherwise unavailable to respond?
<!-- @ngram:escalation Should action queue pacing slow under 1x to keep responses legible -->
  while still honoring sequential action resolution?
<!-- @ngram:proposition Add a visible "waiting" affordance that explains when no potentials -->
  are above threshold, instead of relying solely on narrated silence.

---

## Summary: What To Expect

| Behavior | Observable |
|----------|------------|
| B1 | Response is instant; depth comes later |
| B2 | Multiple voices respond, not just one NPC |
| B3 | Characters speak unprompted when pressure builds |
| B4 | Silence is narrated, not ignored |
| B5 | Naming someone directs energy to them |
| B6 | "What happened?" is a graph query |
| B7 | Actions modify world state |
| B8 | Confessions cascade into confrontations |
| B9 | Characters form opinions over time |
| B10 | News arrives from places you're not |
| B11 | Speed 3x snaps to 1x when drama demands |
| B12 | Travel compresses but conversation persists |

---

*"The conversation is a graph you walk, not a tree you descend."*
