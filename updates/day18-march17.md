# Day 18 Update — March 17, 2026

> 🌐 **EN** | [中文](../zh/updates/day18-march17.md)

**Status: UNSTABLE** | **Breaches: 3/5** | **λ median = 2.157**

---

## New Data

| Metric | Day 17 | Day 18 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 7 | **10** | **313** |
| BM Intercepted | 6 | 10 | 292 |
| Drones Detected | 25 | ~45 | ~1778 |
| Drones Intercepted | 21 | 38 | ~1668 |
| Cruise Missiles | 0 | 0 | 8 |
| BM Intercept Rate (cum) | — | — | 93.3% |
| Drone Stockpile | — | — | 11.1% (222/2000) |

**Key Events:**
- @modgovae: 10 BMs intercepted, 45 drones detected; cumulative 314 BMs, 1,672 drones, 15 cruise
- Pakistani citizen killed by interception debris in Baniyas, Abu Dhabi (8th death total)
- UAE airspace closed early morning, reopened by 5am; flights gradually resumed
- Fujairah Oil Industry Zone fire from drone attack; no casualties
- HRW condemns Iran unlawful strikes across Gulf endangering civilians
- ~90 ships crossed Hormuz since war began; selective Iran-permitted transit emerging

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.178
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.157  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.157** |
| λ 95th percentile | **2.869** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.4%** |
| P(λ > 2.0) | **66.9%** |
| Verdict | **UNSTABLE** |
| Breaches | **3/5** (launcher, drone_stockpile, casualties) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day18.png)

![Lambda Evolution](../charts/lambda_evolution_day18.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-18 23:07 |
