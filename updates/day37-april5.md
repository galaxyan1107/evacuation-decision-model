# Day 37 Update — April 05, 2026

> 🌐 **EN** | [中文](../zh/updates/day37-april5.md)

**Status: UNSTABLE** | **Breaches: 4/5** | **λ median = 2.138**

---

## New Data

| Metric | Day 36 | Day 37 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 23 | **9** | **506** |
| BM Intercepted | 21 | 8 | 478 |
| Drones Detected | 56 | ~50 | ~2297 |
| Drones Intercepted | 48 | 42 | ~2112 |
| Cruise Missiles | 0 | 1 | 17 |
| BM Intercept Rate (cum) | — | — | 94.5% |
| Drone Stockpile | — | — | -14.8% (-297/2000) |

**Key Events:**
- @modgovae: 9 BMs engaged (~8 intercepted, 1 fell sea), 1 cruise missile, 50 drones detected (~42 intercepted, ~8 fell UAE); cumulative ~506 BMs, ~17 cruise, ~2,297 drones
- BOROUGE PETROCHEMICAL FIRES: Multiple fires at Borouge petrochemicals plant in Ruwais from interception debris; 3 separate fires confirmed; operations immediately suspended; no injuries reported (Gulf News, Bloomberg, Khaleej Times)
- US PILOT RESCUED: Missing F-15E weapons system officer rescued by US special forces from Iranian mountains after 36+ hours of evasion; 'seriously wounded' but walking; Trump confirms rescue of 'highly respected Colonel' (NPR, CBS, Axios)
- TRUMP DEADLINE T-24H: Trump's 48-hour ultimatum (issued Apr 4) expires April 6; Trump says US will target Iran's power grid, bridges, and oil infrastructure if Hormuz stays closed (Khaleej Times Day 37 live)
- IRAQ HORMUZ EXEMPTION: Iran grants Iraq special exemption for Hormuz transit; Suezmax Ocean Thunder (Iraqi cargo) seen transiting to Malaysia (Bloomberg)
- Oman and Iran hold talks on measures for smooth Hormuz transit (The National)
- Polymarket ceasefire-by-Apr-30 rises to ~60% on deadline pressure and pilot rescue as face-saving moment; ceasefire-by-Dec-31 at 71% (Polymarket)
- Oil markets closed (Easter Sunday); WTI ~$113.50, Brent ~$111.80 (Friday close carried forward)
- DXB operating at ~55% capacity (Easter Sunday); Emirates ~127 destinations; most European/North American carriers still suspended
- Hormuz expanding selective transits: ~15 vessels/day with Iraqi, French, Japanese, Philippine, Omani flagged vessels; Iran toll system active
- ~5 injuries estimated from debris; 0 fatalities; cumulative ~13 dead, ~222 injured
- Vatican issues statement on conflict; Pope calls for immediate ceasefire
- CENTCOM: US forces destroying Iranian attack drone launch sites targeting civilians in neighboring countries

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.230
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.200
  ──────────────────────────────
  λ median           = 2.138  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.138** |
| λ 95th percentile | **2.852** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.9%** |
| P(λ > 2.0) | **64.7%** |
| Verdict | **UNSTABLE** |
| Breaches | **4/5** (launcher, drone_stockpile, new_weapon, interception_day) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day37.png)

![Lambda Evolution](../charts/lambda_evolution_day37.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System is in CASCADE territory.

---

## Sources

| Source | Type |
|--------|------|
| @modgovae (X.com) | UAE MOD daily update |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-04-05 23:06 |
