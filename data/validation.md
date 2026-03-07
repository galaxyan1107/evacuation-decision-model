# Validation Scorecard

> 🌐 **EN** | [中文](../zh/data/validation.md)


## Day 7 Live Validation (March 6, 2026)

| # | Check | Model Prediction | Observed | Result |
|---|-------|-----------------|----------|--------|
| 1 | Daily BM monotonic decay | Yes (β = 0.25/d) | 7→9 (broke monotonic) | **DIVERGENT** |
| 2 | Interception rate > 90% | 93.2% | 92.7% | **MATCH** |
| 3 | Drone rate stabilizing | ~130/day steady | 112/day (declining) | **CLOSE** |
| 4 | No new weapon types | No | No | **MATCH** |
| 5 | Ceasefire P by Mar 31 | 84% | 63% (Polymarket) | **DIVERGENT** |
| 6 | Airport ops recovering | 25% of normal | ~25% (GCAA) | **MATCH** |
| 7 | Drone stockpile > 30% | 40.8% | ~40% estimated | **CLOSE** |
| 8 | Total Day 30 departures | 5.04M | 5.55M (report) | **DIVERGENT** |

## Summary

**Rating: MODERATE** — 3 MATCH, 2 CLOSE, 3 DIVERGENT

## Analysis of Divergences

### 1. Ballistic Decay Rebound (Day 7: 7→9)
The model assumes monotonic exponential decay in ballistic launches. Day 7 saw a minor uptick from 7 to 9 BMs, breaking this pattern. This likely reflects residual mobile TEL activity rather than a fundamental model failure. The stochastic noise term in the simulation does allow for such fluctuations, but the deterministic trend line doesn't capture it.

**Impact on recommendation:** Strengthens evacuation case (higher residual threat than assumed).

### 2. Polymarket Ceasefire Gap (63% vs 84%)
The model's ceasefire probability by Day 31 (84%) significantly exceeds Polymarket's implied odds (~63%). This suggests the market prices in more escalation risk than the model's attrition-driven Bayesian update. Possible explanations include the market incorporating political/diplomatic factors the model doesn't capture, and thin market liquidity during active conflict.

**Impact on recommendation:** Strengthens evacuation case (conflict may last longer than model predicts).

### 3. Total Departures Gap (5.04M vs 5.55M)
The model underestimates total Day 30 departures by ~9%. The gap is concentrated in the Long-term Families segment (2.79M vs 3.29M), suggesting the model's duration stress calibration slightly underestimates the cumulative pressure on this segment.

**Impact on recommendation:** Neutral — directionally correct, magnitude acceptable for decision-making.

## Recommendation Impact

All three divergences either **strengthen** or are **neutral** to the evacuation recommendation. None suggest the model is overestimating risk. The core recommendation remains unchanged: **depart March 7**.
