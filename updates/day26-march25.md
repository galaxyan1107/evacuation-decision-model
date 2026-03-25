# Day 26 Update — March 25, 2026

> 🌐 **EN** | [中文](../zh/updates/day26-march25.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.171**

---

## New Data

| Metric | Day 25 | Day 26 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 5 | **0** | **356** |
| BM Intercepted | 5 | 0 | 335 |
| Drones Detected | 17 | ~9 | ~1921 |
| Drones Intercepted | 14 | 7 | ~1787 |
| Cruise Missiles | 0 | 0 | 8 |
| BM Intercept Rate (cum) | — | — | 94.1% |
| Drone Stockpile | — | — | 4.0% (79/2000) |

**Key Events:**
- FIRST DAY WITHOUT BALLISTIC MISSILES — 0 BMs detected since conflict began Feb 28 (@modgovae via Gulf News)
- Only 9 drones engaged; cumulative 357 BMs, 15 cruise, 1,815 drones (@modgovae)
- Trump claims US and Iran 'in negotiations now'; Iran denies: 'no talks or negotiations for 25 days'
- Iran formally requires crew/cargo manifests and IRGC approval for Hormuz transit; 6 vessels transited openly
- Oil crashes: WTI -5.1% to $87.63; Brent -5% to $99.30 on Trump diplomacy claims
- Air India resumes ad-hoc Dubai-Delhi flights (26 flights); Emirates limited schedule continues
- Iran says 'non-hostile' ships can pass Hormuz safely; formalizing selective blockade regime
- Iran won't accept ceasefire offer per state media (FARS); Trump's 15-point peace plan received by Iran (AP)

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.192
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.171  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.171** |
| λ 95th percentile | **2.884** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.6%** |
| P(λ > 2.0) | **68.3%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day26.png)

![Lambda Evolution](../charts/lambda_evolution_day26.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-25 23:09 |
