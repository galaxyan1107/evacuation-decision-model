# Day 21 Update — March 20, 2026

> 🌐 **EN** | [中文](../zh/updates/day21-march20.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.163**

---

## New Data

| Metric | Day 20 | Day 21 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 7 | **4** | **337** |
| BM Intercepted | 7 | 4 | 316 |
| Drones Detected | 15 | ~26 | ~1846 |
| Drones Intercepted | 13 | 22 | ~1725 |
| Cruise Missiles | 0 | 0 | 8 |
| BM Intercept Rate (cum) | — | — | 93.8% |
| Drone Stockpile | — | — | 7.7% (154/2000) |

**Key Events:**
- @modgovae: 4 BMs intercepted, 26 drones detected (~22 intercepted); cumulative 338 BMs, 15 cruise, 1,740 drones
- Eid al-Fitr — conflict continues through holiday; no ceasefire despite diplomatic hopes
- Foreign airlines remain banned from DXB since Mar 17; only Emirates and flydubai operating (~40% capacity)
- US weighs releasing sanctioned Iranian crude to ease oil prices (CNBC)
- Brent drops to ~$107 (from $113 close); WTI ~$97; Citi raises forecast to $120 near-term
- Polymarket ceasefire-by-Mar-31 odds collapse to 8% (from 10%)
- Hormuz selective transits continue expanding; ~15 vessels through today; IMO emergency talks ongoing
- Cumulative: 8 dead, ~161 injured (@modgovae)

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
  λ median           = 2.163  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.163** |
| λ 95th percentile | **2.876** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.5%** |
| P(λ > 2.0) | **67.6%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day21.png)

![Lambda Evolution](../charts/lambda_evolution_day21.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-20 23:06 |
