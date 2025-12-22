# Schema — Validation: Link Axes Invariants

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
SCHEMA:          ./SCHEMA_Link_Axes.md
THIS:            VALIDATION_Link_Axes.md (you are here)
SYNC:            ./SYNC_Link_Axes.md
```

---

## BEHAVIORS GUARANTEED

| Behavior ID | Behavior | Why This Validation Matters |
|-------------|----------|-----------------------------|
| B1 | RELATES uses required axes | Prevents semantic ambiguity |
| B2 | PRIMES encodes activation only | Avoids semantic misuse |
| B3 | LEADS_TO role is explicit | Stabilizes pointers/versions |
| B4 | AT/CONTAINS define locality | Protects neighborhood logic |

---

## INVARIANTS

### V1: Allowed Link Types Only

```
Link types MUST be one of: AT, CONTAINS, LEADS_TO, PRIMES, RELATES.
```

### V1b: Universal Fields On Links

```
All links MUST include: id, name, description, weight, energy, embedding.
```

### V2: RELATES Requires Axes

```
RELATES links MUST include: strength, confidence, polarity, role, mode.
```

### V3: PRIMES Requires Activation Axes

```
PRIMES links MUST include: strength, mode=causal.
```

### V4: LEADS_TO Requires Role

```
LEADS_TO links MUST include role in {pointer, version, source}.
```

### V5: Axis Bounds

```
strength/confidence in [0,1], polarity in [-1,1].
```

### V6: Evidence Must Resolve

```
FORALL evidence ids: referenced nodes exist.
```

### V7: No AUTOLOAD Link Type

```
AUTOLOAD MUST NOT appear as a link type.
```

### V8: CONTRADICTS Encoded Via Polarity

```
CONTRADICTS MUST be represented by RELATES with polarity < 0.
```

### V9: Universal Fields On Nodes

```
All nodes MUST include: id, name, description, weight, energy, embedding.
```

---

## PROPERTIES

### P1: Schema Completeness

```
FORALL links:
  required axes exist for their type.
```

### P2: Deterministic Parsing

```
Given identical link data, normalization produces identical axes.
```

---

## ERROR CONDITIONS

### E1: Missing Axes

```
WHEN:   required axes are missing
THEN:   reject link or mark invalid
SYMPTOM: semantic ambiguity
```

### E2: Invalid Polarity

```
WHEN:   polarity outside [-1,1]
THEN:   error
SYMPTOM: contradict/support inversion
```

---

## VERIFICATION PROCEDURE

### Manual Checklist

```
[ ] RELATES has role/mode/polarity/strength/confidence
[ ] PRIMES has strength and causal mode
[ ] LEADS_TO has explicit role
```

### Automated

```bash
pytest tests/schema/test_link_axes.py
```

---

## SYNC STATUS

```
LAST_VERIFIED: 2025-12-20
VERIFIED_AGAINST:
  schema: docs/schema/link-axes/SCHEMA_Link_Axes.md @ local tree
VERIFIED_BY: manual review (doc-only)
RESULT:
  V1: NOT RUN
  V2: NOT RUN
  V3: NOT RUN
  V4: NOT RUN
  V5: NOT RUN
  V6: NOT RUN
  V7: NOT RUN
  V8: NOT RUN
```

---

## MARKERS

<!-- @ngram:todo Define how axes are enforced at write time. -->
<!-- @ngram:todo Add schema lint to reject missing axes. -->
