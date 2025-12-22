# Schema — Link Axes: Nodes, Links, and Examples

```
STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against local tree
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Link_Axes_Not_Types.md
BEHAVIORS:       ./BEHAVIORS_Link_Axes.md
THIS:            SCHEMA_Link_Axes.md (you are here)
VALIDATION:      ./VALIDATION_Link_Axes.md
SYNC:            ./SYNC_Link_Axes.md
```

---

## OVERVIEW

This schema defines a compact link ontology with five link types and semantic
axes. It also provides 15 concrete instances and explicit links to illustrate
usage.

---

## NODE TYPES (V0)

- ACTOR
- NARRATIVE
- SPACE
- PLACE
- MOMENT
- THING

---

## UNIVERSAL FIELDS (ALL NODES)

Required on every node type:

```yaml
Node:
  required:
    - id: str
    - name: str
    - description: str
    - weight: float        # 0.0–1.0
    - energy: float        # 0.0–1.0 (or bounded by physics)
    - embedding: float[]   # vector
```

---

## LINK TYPES (V0)

- AT (localization/scope)
- CONTAINS (hierarchy)
- LEADS_TO (pointer/version/source)
- PRIMES (activation/priming)
- RELATES (generic semantic link with axes)

---

## UNIVERSAL FIELDS (ALL LINKS)

Required on every link type:

```yaml
Link:
  required:
    - id: str
    - name: str
    - description: str
    - weight: float        # 0.0–1.0
    - energy: float        # 0.0–1.0 (or bounded by physics)
    - embedding: float[]   # vector
```

---

## LINK AXES (REQUIRED FOR RELATES/PRIMES)

**Core axes:**
- `strength: 0..1`
- `confidence: 0..1`
- `polarity: -1..+1` (for RELATES; PRIMES uses 0)
- `role: normative | descriptive | procedural | evidential`
- `mode: structural | semantic | temporal | causal`
- `evidence: [id...]` (optional)

---

## INSTANCES (10) WITH NODE ATTRIBUTES

### ACTOR (3)

**A2 Player (ACTOR)**
- mood: {cold:0.7, impatient:0.2, amused:0.1}
- silence_seconds: 18
- attention_budget: 1.0
- history_count: {inputs:311, interrupts_seen:74}

**A3 Fox (ACTOR)**
- style: {subtle:0.7, disruptive:0.4, lyrical:0.5}
- guardrails: {facts:false, only_possibles:true}
- latency_s: {p50:1.2, p95:2.8}
- history_count: {possibles_created:512}

**A4 WorldBuilder (ACTOR)**
- dmz_hops: 2
- writes_allowed: {background:true, events:false, current_scene:false}
- latency_s: {p50:1.5, p95:4.0}
- quality: {coherence:0.8, novelty:0.6}

### SPACE / PLACE (3)

**P1 Inn:CommonRoom (PLACE)**
- tone: {warm:0.3, tense:0.4, sacred:0.1, dark:0.2}
- population: {visible:3, hidden:2}
- distance_class: narrative_local

**S1 engine/moment_graph (SPACE)**
- priority: 0.9
- status: stable
- risk: {latency:high, correctness:high}

**S3 knowledge_space:runner_tuning (SPACE)**
- priority: 0.8
- status: canonical
- tags: [retention, pacing, interrupts]

### NARRATIVE (2)

**N1 Aldric's Oath (NARRATIVE)**
- narrative_type: oath
- tone: {sacred:0.7, proud:0.4, fearful:0.2}
- truth: 0.8
- focus: 1.6
- emotions: {devotion:0.7, duty:0.6}

**N2 Membrane Modulation (NARRATIVE)**
- role: normative+procedural
- focus: 1.2
- quality: {stability:0.6, leverage:0.9}
- emotions: {resolve:0.4, caution:0.5}

### MOMENT (1)

**M1 "J'ai froid" (MOMENT)**
- status: possible/active/spoken (runtime)
- tone: {cold:0.9, needy:0.3}
- energy: 0.65
- weight: 0.55
- speaker: A2
- place: P1
- history_count: {appends:2}

### THING (1)

**T1 cli.ply (THING:file)**
- kind: code
- quality: {tests:0.6, complexity:0.7}
- history_count: {edits:53}

---

## LINK MATRIX (EXPLICIT LINKS)

### A2 Player → A3 Fox
- RELATES {role:descriptive, mode:semantic, strength:0.6, polarity:+0.1, confidence:0.7,
  emotions:{trust:0.4, annoyance:0.2}} : interaction relation

### A2 Player → P1
- AT {present:1.0, visible:1.0, strength:1.0, history:{seconds_here:420}} : player present

### A2 Player → S1
- AT {role:uses, strength:0.5, history:{sessions:6}} : dev usage scope

### A2 Player → S3
- AT {role:uses, strength:0.7, history:{sessions:9}} : task-space usage

### A2 Player → N1
- RELATES {role:evidential, mode:semantic, strength:0.9, polarity:+0.6, confidence:0.8,
  emotions:{duty:0.6}} : oath binds player

### A2 Player → N2
- PRIMES {strength:0.4, mode:causal, lag_ticks:1, intent_tags:[pacing]} : activates pattern

### A2 Player → M1
- LEADS_TO {role:origin, strength:1.0, history:{appends:2}} : input creates/feeds moment

### A3 Fox → A2 Player
- RELATES {role:descriptive, mode:semantic, strength:0.5, polarity:+0.1,
  emotions:{mischief:0.4, care:0.3}} : interaction stance

### A3 Fox → A4 WorldBuilder
- RELATES {role:descriptive, mode:semantic, strength:0.3, polarity:0.0, confidence:0.5} : coordination

### A3 Fox → P1
- AT {visible:0.1, strength:0.5} : soft presence in scene

### A3 Fox → S1
- AT {role:operates_in, strength:0.8, quality:{precision:0.7}} : operates in module

### A3 Fox → S3
- AT {role:uses, strength:0.6} : tuning space usage

### A3 Fox → N1
- PRIMES {strength:0.6, mode:causal, lag_ticks:1} : generates possibles around oath

### A3 Fox → N2
- PRIMES {strength:0.5, mode:causal, lag_ticks:1} : activates membrane usage

### A3 Fox → M1
- PRIMES {strength:0.8, mode:causal, lag_ticks:1, quality:{coherence:0.7, novelty:0.5}} : generates possibles

### A3 Fox → T1
- RELATES {role:evidential, mode:causal, strength:0.9, polarity:+0.2, confidence:0.85,
  history:{reads:5, last_s:120}, quality:{complexity:0.7}, emotions:{focus:0.7}} : read file

### A4 WorldBuilder → A2 Player
- RELATES {role:normative, mode:structural, strength:0.9, polarity:+0.2, confidence:0.85,
  rules:{dmz_hops:2, forbidden:mutate_view_neighborhood}} : DMZ rule

### A4 WorldBuilder → A3 Fox
- RELATES {role:descriptive, mode:semantic, strength:0.3, polarity:0.0} : interaction

### A4 WorldBuilder → P1
- AT {visible:0.0, strength:0.6, dmz_hops:2} : operates around scene

### A4 WorldBuilder → S1
- AT {role:uses, strength:0.4} : module awareness

### A4 WorldBuilder → S3
- AT {role:uses, strength:0.4} : tuning space awareness

### A4 WorldBuilder → N1
- PRIMES {strength:0.4, mode:causal, lag_ticks:2, intent_tags:[lore_fill]} : backstory enrichment

### A4 WorldBuilder → N2
- RELATES {role:procedural, mode:causal, strength:0.5, polarity:+0.1} : respects membrane

### A4 WorldBuilder → M1
- PRIMES {strength:0.3, mode:causal, lag_ticks:2} : background enrichment

### A4 WorldBuilder → T1
- LEADS_TO {role:source, strength:0.6, quality:{coherence:0.8}} : source writing (if allowed)

### P1 Inn → A2 Player
- RELATES {role:descriptive, mode:semantic, strength:0.4, polarity:+0.1,
  emotions:{warmth:0.3, tension:0.4}} : place affects player

### P1 Inn → A3 Fox
- RELATES {role:descriptive, mode:semantic, strength:0.3, polarity:+0.1} : place affects fox

### P1 Inn → A4 WorldBuilder
- RELATES {role:descriptive, mode:semantic, strength:0.2, polarity:0.0} : locality tie

### P1 Inn → N1
- RELATES {role:descriptive, mode:semantic, strength:0.4, polarity:+0.1, tags:[relevant_here]} : contextual relevance

### P1 Inn → N2
- PRIMES {strength:0.3, mode:causal, lag_ticks:1, intent_tags:[mood_local]} : mood local

### P1 Inn → M1
- AT {visible:1.0, strength:1.0} : moment located here

### S1 moment_graph → A2 Player
- RELATES {role:descriptive, mode:structural, strength:0.4} : usage relation

### S1 moment_graph → A3 Fox
- RELATES {role:descriptive, mode:structural, strength:0.6} : fox operates here

### S1 moment_graph → A4 WorldBuilder
- RELATES {role:descriptive, mode:structural, strength:0.3} : wb operates here

### S1 moment_graph → S3
- CONTAINS {scope:knowledge, strength:0.7} : tuning space attached

### S1 moment_graph → N1
- RELATES {role:descriptive, mode:structural, strength:0.4} : narrative relevance

### S1 moment_graph → N2
- RELATES {role:normative, mode:structural, strength:0.8, confidence:0.8} : pattern applies

### S1 moment_graph → T1
- AT {strength:1.0} : file location

### S3 runner_tuning → A2 Player
- RELATES {role:procedural, mode:causal, strength:0.5} : player uses tuning

### S3 runner_tuning → A3 Fox
- RELATES {role:procedural, mode:causal, strength:0.5} : fox uses tuning

### S3 runner_tuning → A4 WorldBuilder
- RELATES {role:procedural, mode:causal, strength:0.4} : wb uses tuning

### S3 runner_tuning → S1
- RELATES {role:structural, mode:structural, strength:0.6} : module linkage

### S3 runner_tuning → N1
- PRIMES {strength:0.2, mode:causal, lag_ticks:2, intent_tags:[interrupt_policy]} : rare influence

### S3 runner_tuning → N2
- RELATES {role:procedural, mode:causal, strength:0.7} : membrane integration

### S3 runner_tuning → M1
- PRIMES {strength:0.2, mode:causal, lag_ticks:1} : pacing influence

### S3 runner_tuning → T1
- RELATES {role:evidential, mode:structural, strength:0.5} : code linkage

### N1 Aldric's Oath → A2 Player
- RELATES {role:descriptive, mode:semantic, strength:0.9, polarity:+0.6, confidence:0.8,
  emotions:{duty:0.6}} : oath binds player

### N1 Aldric's Oath → A3 Fox
- RELATES {role:descriptive, mode:semantic, strength:0.5, polarity:+0.1} : oath considered

### N1 Aldric's Oath → A4 WorldBuilder
- RELATES {role:descriptive, mode:semantic, strength:0.4, polarity:+0.1} : lore relation

### N1 Aldric's Oath → P1
- RELATES {role:descriptive, mode:semantic, strength:0.4, polarity:+0.1} : place relevance

### N1 Aldric's Oath → S1
- AT {strength:0.5, role:belongs_to} : stored in module knowledge

### N1 Aldric's Oath → S3
- AT {strength:0.5, role:belongs_to} : stored in tuning space

### N1 Aldric's Oath → N2
- RELATES {role:normative, mode:semantic, strength:0.4, polarity:-0.2} : tension with membrane

### N1 Aldric's Oath → M1
- PRIMES {strength:0.6, mode:causal, lag_ticks:1} : influences interpretation

### N2 Membrane → A2 Player
- PRIMES {strength:0.5, mode:causal, lag_ticks:1, intent_tags:[field_shape]} : affects experience

### N2 Membrane → A3 Fox
- PRIMES {strength:0.4, mode:causal, lag_ticks:1} : guides fox

### N2 Membrane → A4 WorldBuilder
- RELATES {role:procedural, mode:causal, strength:0.5} : guides wb

### N2 Membrane → P1
- PRIMES {strength:0.4, mode:causal, lag_ticks:1, intent_tags:[mood_local]} : mood local

### N2 Membrane → S1
- RELATES {role:normative, mode:structural, strength:0.85, confidence:0.8} : applies to module

### N2 Membrane → S3
- RELATES {role:procedural, mode:causal, strength:0.75} : pacing rules

### N2 Membrane → N1
- RELATES {role:normative, mode:semantic, strength:0.3, polarity:-0.2} : tension with oath

### N2 Membrane → M1
- PRIMES {strength:0.5, mode:causal, lag_ticks:1} : modulates surfacing

### N2 Membrane → T1
- LEADS_TO {role:pointer, strength:0.6} : points to implementation file

### M1 \"J'ai froid\" → A2 Player
- RELATES {role:descriptive, mode:semantic, strength:0.7, polarity:+0.2, emotions:{need:0.6}} : concerns player

### M1 \"J'ai froid\" → A3 Fox
- PRIMES {strength:0.6, mode:causal, lag_ticks:1} : generates possibles

### M1 \"J'ai froid\" → A4 WorldBuilder
- RELATES {role:descriptive, mode:semantic, strength:0.3, polarity:+0.1} : background enrichment

### M1 \"J'ai froid\" → P1
- AT {visible:1.0, strength:1.0} : located in inn

### M1 \"J'ai froid\" → S1
- AT {role:logged_in, strength:0.4} : dev anchoring (optional)

### M1 \"J'ai froid\" → S3
- PRIMES {strength:0.3, mode:causal, lag_ticks:1} : pacing influence

### M1 \"J'ai froid\" → N1
- PRIMES {strength:0.5, mode:causal, lag_ticks:1} : activates oath themes

### M1 \"J'ai froid\" → N2
- PRIMES {strength:0.4, mode:causal, lag_ticks:1} : activates membrane

### M1 \"J'ai froid\" → T1
- LEADS_TO {role:pointer, strength:0.2} : log pointer (optional)

### T1 cli.ply → A3 Fox
- RELATES {role:evidential, mode:causal, strength:0.9, polarity:+0.2, confidence:0.85,
  history:{reads:5, last_s:120}, quality:{complexity:0.7}} : file read evidence

### T1 cli.ply → A4 WorldBuilder
- LEADS_TO {role:source, strength:0.5} : wb edits (if allowed)

### T1 cli.ply → S1
- AT {strength:1.0} : file in module

### T1 cli.ply → S3
- RELATES {role:evidential, mode:structural, strength:0.4} : tuning references

### T1 cli.ply → N1
- RELATES {role:evidential, mode:structural, strength:0.2} : rare link to oath logic

### T1 cli.ply → N2
- RELATES {role:evidential, mode:structural, strength:0.6} : membrane hooks

---

## ATTRIBUTE CATALOG (RICH)

### Common (all links)
- strength: 0..1
- confidence: 0..1
- polarity: -1..+1 (RELATES; PRIMES uses 0)
- role: normative | descriptive | procedural | evidential
- mode: structural | semantic | temporal | causal
- evidence: [id...] (optional)
- history: {count, last_tick, last_s, reinforced, decayed} (optional)
- quality: {clarity, coherence, novelty, stability, test_coverage} (optional)
- emotions: {label:0..1} (optional, focus modulator only)

### AT
- present: 0..1
- visible: 0..1
- recency_s
- duration_s
- dmz_hops (optional)

### CONTAINS
- order: int
- depth: int
- scope: module | place | topic

### LEADS_TO
- role: pointer | version | source
- hash_from, hash_to (versioning)
- format: md | code | yaml | url
- size_bytes, lines, word_count

### PRIMES
- lag_ticks: int
- budget_cost: 0..1
- decay_half_life_ticks
- activation_threshold_hint
- intent_tags: [..]

### RELATES
- polarity required
- role required
- mode required
- topics: [..]
- tags: [..]

---

## RULES

- Use RELATES + axes instead of new semantic link types.
- Encode contradiction as polarity < 0.
- Use PRIMES only for activation effects, not semantic claims.
- Context surfacing replaces AUTOLOAD semantics.

---

## OBSERVABLE BEHAVIORS (TARGET)

### B1: Player Input Coalescing
- Repeated inputs coalesce into a single moment with history.appends incremented.

### B2: Next Tick Salience
- A player input moment becomes active or eligible by next tick in the local neighborhood.

### B3: Focus Split Redistribution
- New sinks reallocate energy across neighborhood, changing dominant active moment.

### B4: Interrupt by Focus Reconfiguration
- Interrupt fires only when dominant active changes, deactivates, or a local moment is spoken.

### B5: Membrane Mood Local (Per Place)
- Same input in different places yields different timing/order without changing facts.

### B6: WorldBuilder DMZ
- No mutations inside player neighborhood; DMZ enforces local safety.

### B7: Fox Produces Possibles, CanonHolder Produces Facts
- Fox writes only possible moments; spoken only via canonization.

### B8: Relationship Narratives Shape Meaning
- Strong narratives bias which possibles emerge after input.

### B9: Evidenceful Links (No Absolutes)
- Normative/evidential links carry confidence/evidence and decay/reinforce over time.

### B10: File Read as Embodied Attention
- Agent read events strengthen evidential links and prime downstream behavior.
