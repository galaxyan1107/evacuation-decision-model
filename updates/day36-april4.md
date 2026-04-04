# Day 36 Update — April 04, 2026

> 🌐 **EN** | [中文](../zh/updates/day36-april4.md)

**Status: UNSTABLE** | **Breaches: 3/5** | **λ median = 2.133**

---

## New Data

| Metric | Day 35 | Day 36 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 18 | **23** | **497** |
| BM Intercepted | 16 | 21 | 470 |
| Drones Detected | 47 | ~56 | ~2247 |
| Drones Intercepted | 40 | 48 | ~2070 |
| Cruise Missiles | 4 | 0 | 16 |
| BM Intercept Rate (cum) | — | — | 94.6% |
| Drone Stockpile | — | — | -12.3% (-247/2000) |

**Key Events:**
- @modgovae: 23 BMs engaged (~21 intercepted, 1 fell sea, 1 fell land), 0 cruise missiles, 56 drones detected (~48 intercepted, ~8 fell UAE); cumulative 498 BMs, 23 cruise, 2,141 drones
- TRUMP 48-HOUR ULTIMATUM: Trump warns Iran to open Strait of Hormuz or make a deal within 48 hours or face 'all hell' -- reinforcing April 6 deadline; posts on Truth Social
- BUSHEHR NUCLEAR PLANT TARGETED: US-Israeli strike hits grounds near Bushehr nuclear facility -- 1 person killed, auxiliary buildings damaged; raises nuclear escalation fears
- US AIRCRAFT SHOT DOWN: Iran shoots down US military aircraft in Gulf operations; at least one crew member missing -- search and rescue ongoing (CBS News live coverage)
- US STRIKES IRAN B1 BRIDGE: US strikes Iran's B1 bridge during Iran's Nature Day holiday gatherings -- 8 killed, 95 wounded; major civilian outcry
- UN Security Council votes on Bahrain Hormuz proposal -- Russia and China signal likely veto citing escalation risk
- Polymarket ceasefire-by-Apr-30 surges to ~57% (from 22% Day 35) on Trump renewed diplomatic pressure and Iran receiving US message via mediators
- Oil prices elevated: WTI ~13.50 (continues WTI>Brent inversion); Brent ~11.80 on Bushehr strike and ultimatum
- 11 injuries reported (debris/shrapnel) -- no fatalities; cumulative 13 dead, ~217 injured
- DXB operating at ~55% capacity (Easter Saturday); Emirates serving ~127 destinations; most European/North American carriers still suspended
- Hormuz selective transits ~12/day; Philippines-flagged vessels now permitted; France and Japan-flagged vessels transiting; Iran toll booth system active
- Cumulative: ~13 dead, ~217 injured

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.225
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.200
  ──────────────────────────────
  λ median           = 2.133  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.133** |
| λ 95th percentile | **2.846** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.8%** |
| P(λ > 2.0) | **64.1%** |
| Verdict | **UNSTABLE** |
| Breaches | **3/5** (launcher, drone_stockpile, casualties) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day36.png)

![Lambda Evolution](../charts/lambda_evolution_day36.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-04-04 23:23 |
