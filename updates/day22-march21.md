# Day 22 Update — March 21, 2026

> 🌐 **EN** | [中文](../zh/updates/day22-march21.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.164**

---

## New Data

| Metric | Day 21 | Day 22 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 4 | **3** | **340** |
| BM Intercepted | 4 | 3 | 319 |
| Drones Detected | 26 | ~8 | ~1854 |
| Drones Intercepted | 22 | 6 | ~1731 |
| Cruise Missiles | 0 | 0 | 8 |
| BM Intercept Rate (cum) | — | — | 93.8% |
| Drone Stockpile | — | — | 7.3% (146/2000) |

**Key Events:**
- @modgovae: 3 BMs intercepted, 8 drones detected; cumulative 341 BMs, 15 cruise, 1,748 drones
- US strikes Natanz uranium enrichment facility with bunker busters — second attack on nuclear site; IAEA reports no radiation leak
- Iran offers Japan safe passage through Hormuz — selective blockade expanding to China, India, Pakistan, and now Japan
- Iran fires 2 BMs at Diego Garcia (UK-US base in Indian Ocean) — unsuccessful per UK officials
- Trump says mulling 'winding down' the Iran war despite continued strikes
- Brent ~$107 (down from $113 peak); WTI ~$95; VLCC rates declining as tankers flee Gulf
- Cumulative: 8 dead, ~160 injured (@modgovae); no new casualties today

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.185
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.164  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.164** |
| λ 95th percentile | **2.877** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.5%** |
| P(λ > 2.0) | **67.7%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day22.png)

![Lambda Evolution](../charts/lambda_evolution_day22.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-21 23:07 |
