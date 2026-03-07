# 4. Population Flight Model

The population flight module adapts the **Brock & Hommes (1998) Heterogeneous Agent Model** for evacuation dynamics. Six agent types represent distinct civilian population segments, each with unique risk thresholds, departure speeds, and sensitivity profiles.

## Agent Types

| Agent | Pop Share | Size | Risk Threshold | Departure Speed | Attack Sensitivity | Social Contagion | Infrastructure |
|-------|-----------|------|---------------|-----------------|-------------------|-----------------|---------------|
| Transit/Stranded | 2% | 200K | 0.01 | 0.99 | 1.0 | 0.0 | 0.0 |
| Tourists | 5% | 500K | 0.05 | 0.85 | 2.5 | 1.5 | 0.5 |
| Short-term Expats | 15% | 1.5M | 0.15 | 0.30 | 1.5 | 1.2 | 1.0 |
| Long-term Families | 45% | 4.5M | 0.28 | 0.12 | 0.9 | 1.0 | 2.5 |
| HNW / Business | 5% | 500K | 0.38 | 0.08 | 0.6 | 0.8 | 2.0 |
| Nationals | 12% | 1.2M | 0.75 | 0.015 | 0.3 | 0.2 | 0.5 |

**Design rationale:** Transit passengers leave immediately regardless of conditions. Tourists have low thresholds and high speed. Long-term families are the largest segment but require sustained pressure (high infrastructure sensitivity reflects school closures, service disruption). Nationals have the highest threshold — deep roots, property, extended family networks.

## Perceived Risk Function

The Brock-Hommes adapted perceived risk function has six components:

```
R_a(d) = 0.25 · M(d) · α_atk     // memory-weighted attack intensity
       + 0.15 · SC(d) · α_soc     // social contagion (herding)
       + 0.10 · ID(d) · α_inf     // infrastructure degradation
       + 0.30 · DS(d)             // duration stress
       + 0.10 · U(d)              // uncertainty premium
       + 0.10 · SD(d) · α_inf     // service disruption
```

### Memory-Weighted Attack Intensity

Uses exponential decay over a 7-day lookback window:

```
M(d) = Σ_{k=0..6} AI(d-k) · 0.7^k / Σ_{k=0..6} 0.7^k
```

This captures the psychological reality that recent attacks weigh more heavily than older ones, but the memory doesn't reset instantly.

### Social Contagion (Herding)

```
SC(d) = (total_departed_fraction)^0.5
```

Non-linear: accelerates once departures cross ~5% threshold. This is the core Brock-Hommes insight — agents observe other agents' decisions and incorporate them into their own risk assessment.

### Duration Stress

```
DS(d) = 1 - exp(-0.10 · d)
```

Captures the "even patient families eventually crack" dynamic. Reaches 0.63 by Day 10 and 0.95 by Day 30. This was the key calibration fix — without duration stress, long-term families and nationals never reached their departure thresholds.

### Infrastructure Degradation

```
ID(d) = 1 / (1 + exp(10 · (EA(d) - 0.50)))
```

A sigmoid function of economic activity remaining. Triggers sharply when economic activity drops below 50%.

## Departure Decision Rule

```python
if R_a(d) > θ_a:
    excess = (R_a(d) - θ_a) / (1 - θ_a)
    new_wanting = remaining_a · speed_a · excess^1.3
```

The 1.3 exponent creates a convex response — small risk exceedances produce modest departures, but large exceedances trigger rapid flight.

## Airport Capacity Constraint

Actual departures are capped by GCAA airport capacity recovery curve:

```python
AIRPORT_CAPACITY = {
    "normal_daily": 310_000,
    "recovery": {
        0: 0.30, 1: 0.00, 2: 0.02, 3: 0.03, 4: 0.08,
        5: 0.12, 6: 0.15, 7: 0.25, 8: 0.35, 9: 0.45,
        10: 0.50, 14: 0.65, 20: 0.80, 29: 0.90,
    }
}
```

This creates a bottleneck early in the conflict (Day 1: airport closed, Day 2-3: minimal capacity) that generates large queues of people wanting to leave but unable to fly.

![Population Departure Curves by Agent Type](../assets/population_flight.png)

## Day 30 Model Output

| Agent | Departed (%) | Departed (Count) |
|-------|-------------|-------------------|
| Transit/Stranded | ~93% | ~186K |
| Tourists | ~92% | ~460K |
| Short-term Expats | ~87% | ~1.31M |
| Long-term Families | ~62% | ~2.79M |
| HNW / Business | ~50% | ~250K |
| Nationals | ~4.6% | ~55K |
| **Total** | — | **~5.04M** |

Report target: 5.55M (~91% match).
