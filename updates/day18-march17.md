# Day 18 Update — March 17, 2026

> 🌐 **EN** | [中文](../zh/updates/day18-march17.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.155**

---

## New Data

| Metric | Day 17 | Day 18 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 7 | **10** | **314** |
| BM Intercepted | 6 | ~9 | ~291 |
| Drones Detected | ~25 | **45** | **~1,672** |
| Drones Intercepted | 21 | ~38 | ~1,570 |
| Cruise Missiles | 0 | 0 | 15 |
| BM Intercept Rate (cum) | — | — | ~92.7% |
| Drone Stockpile | — | — | ~16.4% (328/2000) |

**Key Events:**
- @modgovae: UAE air defences engaged 10 ballistic missiles and 45 drones on 17th March 2026. Cumulative: 314 BMs, 15 cruise, 1,672 UAVs
- **GCAA closes UAE airspace** — "exceptional precautionary measure" amid active missile/drone threats; first full airspace closure since Day 2
- Airspace reopened by 5:05 AM local time after situation stabilized
- Abu Dhabi emergency alert: MOI urged public to remain in safe places
- Loud explosions heard across Dubai from successful aerial interceptions
- Fujairah oil port hit again by drone
- Trump pressures allies to help open Strait of Hormuz; muted international response
- UK begins "defensive air sorties" in UAE
- US troops wounded in war reaches ~200 (180 returned to duty)
- Brent $103.65 (+4%); WTI $97.08 (+4.2%)

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.164
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.155  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.155** |
| λ 95th percentile | **2.875** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.5%** |
| P(λ > 2.0) | **67.2%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day18.png)

![Lambda Evolution](../charts/lambda_evolution_day18.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System remains in CASCADE territory. First full airspace closure since Day 2 signals intensifying threat level. Attack volume rebounds sharply (32→55) with drone numbers tripling (25→45). Evacuation windows narrowing as airport capacity remains degraded.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update: 314 BMs, 15 cruise, 1,672 UAVs cumulative |
| GCAA (via WAM) | Airspace closure and reopening |
| CNBC | Oil: Brent $103.65, WTI $97.08 |
| Polymarket | Ceasefire by Mar 31: 8% |
| Euronews, Gulf News | Day 18 events |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-17 23:30 |
