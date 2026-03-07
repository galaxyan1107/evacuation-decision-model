# 5. Evacuation Risk Scoring

> 🌐 **EN** | [中文](../zh/method/evacuation-scoring.md)


The final module produces a **composite evacuation risk score (0–100)** that synthesizes all model outputs into a single actionable metric.

## Composite Score Formula

```
S(d) = min(decay_envelope(d),
        w_atk · ATK(d) + w_casc · CASC(d) + w_queue · QUEUE(d)
      + w_oman · OMAN(d) + w_flight · FLIGHT(d))
```

### Component Weights (Default)

| Component | Weight | Description |
|-----------|--------|-------------|
| Attack Intensity | 0.25 | Normalized daily attack threat level |
| Cascade Probability | 0.20 | HAM λ > 1 cumulative probability |
| Airport Queue | 0.20 | Normalized departure queue pressure |
| Oman Spillover | 0.15 | Regional contagion risk |
| Flight Urgency | 0.05 | Logarithmic time pressure |

### Decay Envelope

The composite score is constrained by an exponential decay envelope calibrated to match the report's risk trajectory:

```
decay_envelope(d) = 95 · exp(-0.13 · d) + 25
```

This ensures the score follows the report's 95 → 27 trajectory over 10 days, reflecting the diminishing urgency as the initial attack intensity subsides and airport capacity recovers.

## Recommendation Bands

| Score Range | Recommendation |
|-------------|---------------|
| ≥ 80 | **LEAVE IMMEDIATELY** |
| ≥ 60 | **LEAVE — good window** |
| ≥ 40 | **ACCEPTABLE — queue building** |
| ≥ 30 | **LATE — risky** |
| < 30 | **LOW RISK — but monitor** |

![Composite Evacuation Risk Score](../assets/risk_score.png)

## Optimal Departure Window

Based on Day 7 data, the optimal departure window is **Days 1-3** (score > 60). By Day 10, the score drops below 40 and the window narrows significantly due to airport congestion and reduced flight availability.

**Current recommendation (March 7, Day 8):** LEAVE — depart today. Score remains above 60 but declining. Airport capacity at ~25% of normal and recovering.
