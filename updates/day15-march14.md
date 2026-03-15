# Day 15 Update — March 14, 2026

> 🌐 **EN** | [中文](../zh/updates/day15-march14.md)

**Status: UNSTABLE** | **Breaches: 3/5** | **λ median = 2.149**

---

## New Data

| Metric | Day 14 | Day 15 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 7 | **9** | **292** |
| BM Intercepted | 7 | 8 | 272 |
| Drones Detected | 27 | ~33 | ~1702 |
| Drones Intercepted | 21 | 27 | ~1604 |
| Cruise Missiles | 0 | 0 | 8 |
| BM Intercept Rate (cum) | — | — | 93.2% |
| Drone Stockpile | — | — | 14.9% (298/2000) |

**Key Events:**
- 9 BMs + 33 drones (@modgovae via Gulf News); cumulative 294 BMs, 15 cruise, ~1,700 drones
- Fujairah bunkering hub fire from drone interception debris; 1 Jordanian citizen injured
- Two killed in Oman by stray drones; several drones also fired at Saudi Arabia
- Cumulative: 6 dead, 141 injured (@modgovae)
- Brent closes above $100 for second consecutive day; WTI ~$99

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.170
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.149  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.149** |
| λ 95th percentile | **2.861** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.3%** |
| P(λ > 2.0) | **66.1%** |
| Verdict | **UNSTABLE** |
| Breaches | **3/5** (launcher, drone_stockpile, interception_day) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day15.png)

![Lambda Evolution](../charts/lambda_evolution_day15.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-15 20:11 |
