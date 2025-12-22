# Schema — Behaviors: Link Axes Semantics

```
STATUS: DRAFT
CREATED: 2025-12-20
VERIFIED: 2025-12-20 against local tree
```

---

## CHAIN

```
PATTERNS:        ./PATTERNS_Link_Axes_Not_Types.md
THIS:            BEHAVIORS_Link_Axes.md (you are here)
SCHEMA:          ./SCHEMA_Link_Axes.md
VALIDATION:      ./VALIDATION_Link_Axes.md
SYNC:            ./SYNC_Link_Axes.md
```

---

## BEHAVIORS

### B1: RELATES Uses Required Axes

```
GIVEN:  a RELATES link is created
WHEN:   it is stored
THEN:   role, mode, polarity, strength, and confidence are present
```

### B2: PRIMES Encodes Activation, Not Semantics

```
GIVEN:  PRIMES links exist
WHEN:   energy/attention is propagated
THEN:   PRIMES affects activation, not semantic truth
```

### B3: LEADS_TO Encodes Pointer/Version/Source

```
GIVEN:  a LEADS_TO link exists
WHEN:   it is interpreted
THEN:   role identifies pointer vs version vs source
```

### B4: AT and CONTAINS Define Locality

```
GIVEN:  AT/CONTAINS links exist
WHEN:   neighborhood or scope is computed
THEN:   locality derives from these links, not hidden config
```

---

## INPUTS / OUTPUTS

### Primary Function: `validate_link_axes()` (planned)

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| link | dict | link properties and type |

**Outputs:**

| Return | Type | Description |
|--------|------|-------------|
| valid | bool | whether required axes are present |

**Side Effects:**

- None (validation only)

---

## EDGE CASES

### E1: Missing Axes

```
GIVEN:  RELATES link missing role or mode
THEN:   validation fails
```

---

## ANTI-BEHAVIORS

### A1: New Link Types for Semantics

```
GIVEN:   a new semantic link type is proposed
WHEN:    modeling relations
MUST NOT: create new link types
INSTEAD: use RELATES with axes
```

---

## MARKERS

<!-- @ngram:todo Define schema-level enforcement for required axes. -->
