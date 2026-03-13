# Day 13 Update — March 12, 2026

> 🌐 **EN** | [中文](../zh/updates/day13-march12.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.110**

---

## New Data

| Metric | Day 12 | Day 13 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 6 | **10** | **275** |
| BM Intercepted | 6 | 10 | 256 |
| Drones Detected | 39 | ~26 | ~1636 |
| Drones Intercepted | ~32 | ~20 | ~1556 |
| Cruise Missiles | 7 | 0 | 15 |
| BM Intercept Rate (cum) | — | — | 93.1% |
| Drone Stockpile | — | — | 18.2% (364/2000) |

**@modgovae official (12 March 2026):** "UAE air defences intercept 10 ballistic missiles and 26 UAVs." Cumulative: 278 BM, 15 cruise missiles, 1540 UAVs.

**Key Events:**
- BM uptick: 6→10, reversing three-day decline (12→9→6→**10**)
- Drone record low: only 26 UAVs — lowest daily count since conflict began
- No cruise missiles (Day 12 had 7, first since Day 3)
- Total daily projectiles: 36 — lowest since Day 1
- Two UAE military helicopter crash deaths: Captain Pilot Saeed Rashid Al Balushi and First Lieutenant Ali Saleh Al Taniji — technical malfunction, operational accidents
- No new combat fatalities; 5 injuries (cumulative: 6 dead, 131 injured)
- Iran's missile fire rate described as having "collapsed by 92%" (JPost)

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.165
  + λ_intercept          = -0.002
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.110  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.110** |
| λ 95th percentile | **2.810** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **98.1%** |
| P(λ > 2.0) | **63.2%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## What Changed Day 12 → Day 13

```
Day 12 → Day 13 Lambda Decomposition:

Component          Day 12           Day 13              Change
─────────────────────────────────────────────────────────────────
λ_launcher         -0.544           -0.544               0.000  (depletion maxed at 99%)
λ_drone            +0.162           +0.165              +0.003  (stockpile 19.5%→18.2%)
λ_intercept        +0.000           -0.002              -0.002  (cum rate improves 92.8%→93.1%)
λ_proxy            +0.500           +0.500               0.000  Still active
λ_hormuz           +0.630           +0.630               0.000  Still closed (Day 11)
λ_weapon           +0.400           +0.400               0.000  No new weapon types
λ_bm_rebound       +0.000           +0.000               0.000  6→10 treated as noise, not structural rebound
λ_naval            -0.128           -0.128               0.000  2 carrier groups, unchanged
─────────────────────────────────────────────────────────────────
λ total (median)    2.141            2.110              -0.031
```

Key drivers of the Day 13 change:
1. **λ eases slightly (−0.031):** No new escalation events. Improved interception rate (93.1%) provides small negative contribution. Drone stockpile decline provides tiny positive contribution. Net effect is marginal easing.
2. **BM uptick (6→10) not reactivating λ_bm_rebound:** While BMs reversed the three-day decline, the 10-BM count is well below the Day 8-9 peak (16-17). Treated as tactical variation, not structural rebound. If BMs sustain >10/day for 2+ consecutive days, λ_bm_rebound would reactivate.
3. **Drone collapse deepens:** 26 drones is the lowest single-day count since the conflict began. Three consecutive days below 40 (35→39→26). Stockpile at 18.2% — on track for exhaustion in ~12 days at current rate.

**Net assessment:** λ eases marginally from 2.141 to 2.110. The system remains in cascade territory. The dramatic reduction in attack volume (36 total, lowest since Day 1) provides a brief tactical window, but structural instability factors (Hormuz, proxy, drone depletion) continue dominating. Iran is clearly in stockpile conservation mode — fewer drones, sustained BM capability.

---

## Defense Cost Update

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | 154 | THAAD @ $12.7M | $1,956 | $3,911 |
| BM (PAC-3, 40%) | 102 | PAC-3 @ $3.9M | $398 | $796 |
| Cruise Missiles | 15 | PAC-3 @ $3.9M | $59 | $117 |
| Drones | ~1,556 | SHORAD @ $0.7M | $1,089 | $2,178 |
| **TOTAL** | **~1,827** | | **$3,501** | **$7,002** |

### Oil Revenue Not Sold (Cumulative, 11 days Hormuz closure)

| Component | Volume | Revenue Loss |
|-----------|--------|-------------|
| Stranded oil (no Hormuz) | 1.7M bbl/d × 11 days × $88 | **$1,646M** |
| Voluntary production cuts | 0.5M bbl/d × 11 days × $88 | **$484M** |
| **TOTAL OIL LOSS** | | **$2,130M ($2.13B)** |

### Grand Total Cost to UAE (Day 13)

| Scenario | Defense | Oil Loss | **Grand Total** |
|----------|---------|----------|----------------|
| 1:1 | $3.50B | $2.13B | **$5.63B** |
| 1:2 | $7.00B | $2.13B | **$9.13B** |
| 1:3 | $10.50B | $2.13B | **$12.63B** |

*Note: Oil loss uses Day 13 WTI (~$88), slightly recovered from Day 12's $86 post-IEA release. Ruwais refinery remains shut (922K bbl/d). Cumulative defense costs rising despite lower daily attack volume, as BMs (the most expensive to intercept) increased.*

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day13.png)

![Lambda Evolution](../charts/lambda_evolution_day13.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System remains in CASCADE territory (λ = 2.110, P(λ>1) = 100%).

**Day 13 key dynamics:**
- **Positive:** All 10 BMs intercepted (100%), cumulative rate improves to 93.1% — best since Day 5. Total attack volume at record low (36 projectiles). Zero combat fatalities. Drone conservation mode suggests Iran's stockpile is critically depleted. Oil stabilizes around $88 post-IEA intervention.
- **Negative:** BMs reverse three-day decline (6→10), proving Iran retains ballistic missile capability. Two UAE military deaths from helicopter crash (operational). Ceasefire odds continue declining (~19%). Hormuz remains closed. Drone stockpile at 18.2% — approaching exhaustion territory.
- **Tactical window:** The dramatic drop in attack volume creates a brief **relative calm window** for evacuation. Use it. BM capability persists and Iran could surge attacks at any time. Airport at ~55% capacity — still viable for departure.
- **Two military helicopter crash deaths** (Captain Al Balushi, 1st Lt. Al Taniji) from technical malfunction highlight the strain on UAE military operations even without direct combat engagement. Operational tempo is taking a toll.
- **Drone exhaustion approaching:** At ~26/day, remaining ~364 drones last ~14 days (exhaustion ~Day 27, March 25). Iran may be forced to shift entirely to BMs or seek resupply. This could trigger a new phase of the conflict.

---

## Sources

| Source | Type |
|--------|------|
| [@modgovae](https://x.com/modgovae) | UAE MOD daily update (March 12) |
| [@modgovae — helicopter crash condolences](https://x.com/modgovae) | Military operational casualties |
| [Gulf News — Day 13 liveblog](https://gulfnews.com/uae/us-israel-war-on-iran-day-13-iran-hits-gulf-countries-minor-drone-incidents-in-dubai-1.500471643) | Daily situation |
| [JPost — Iran missile fire rate collapsed 92%](https://www.jpost.com/defense-and-tech/article-889435) | Military analysis |
| [Al Jazeera — Iran targets Gulf nations](https://www.aljazeera.com/news/2026/3/12/iran-targets-gulf-nations-with-missiles-drones-as-oil-prices-soar) | Regional context |
| [Breaking Defense — GCC nightmare scenario](https://breakingdefense.com/2026/03/iran-attacks-uae-saudi-missiles-drones-gcc-air-defense/) | Defense analysis |
| [Polymarket](https://polymarket.com/event/us-x-iran-ceasefire-by) | Ceasefire odds |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-13 |
