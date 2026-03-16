# Day 16 Update — March 15, 2026

> 🌐 **EN** | [中文](../zh/updates/day16-march15.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.150**

---

## New Data

| Metric | Day 15 | Day 16 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 9 | **4** | **296** |
| BM Intercepted | 8 | 4 | 276 |
| Drones Detected | 33 | ~6 | ~1708 |
| Drones Intercepted | 27 | 5 | ~1609 |
| Cruise Missiles | 0 | 0 | 8 |
| BM Intercept Rate (cum) | — | — | 93.2% |
| Drone Stockpile | — | — | 14.6% (292/2000) |

**Key Events:**
- @modgovae: 4 BMs intercepted, 6 drones detected (confirmed by Gulf News, CGTN, Khaleej Times, Peninsula Qatar)
- Cumulative: 298 BMs, 15 cruise, 1,606 drones (@modgovae official)
- Lowest daily volume since conflict began (10 total projectiles)
- Heavy US-Israeli strikes on Isfahan, Shiraz, Tehran, Dezful, Khomein, Hamedan
- Brent ~$103; WTI ~$99

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.171
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.150  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.150** |
| λ 95th percentile | **2.862** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.3%** |
| P(λ > 2.0) | **66.2%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day16.png)

![Lambda Evolution](../charts/lambda_evolution_day16.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-16 23:29 |
