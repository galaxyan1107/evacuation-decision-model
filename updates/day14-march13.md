# Day 14 Update — March 13, 2026

> 🌐 **EN** | [中文](../zh/updates/day14-march13.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.080**

---

## New Data

| Metric | Day 13 | Day 14 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 10 | **7** | **282** |
| BM Intercepted | 10 | ~7 | ~263 |
| Drones Detected | ~26 | ~27 | ~1663 |
| Drones Intercepted | ~20 | ~21 | ~1577 |
| Cruise Missiles | 0 | 0 | 15 |
| BM Intercept Rate (cum) | — | — | 93.3% |
| Drone Stockpile | — | — | 16.9% (337/2000) |

**@modgovae official (13 March 2026, 8:51 PM):** "UAE Air Defences engaged Iranian Ballistic and Cruise Missiles and UAVs Attacks." Cumulative per Gulf News Day 14 liveblog: 285 BM, 15 cruise missiles, 1,567 UAVs.

**Key Events:**
- BMs decline: 10→7, resuming three-day decline trend (12→9→6→10→**7**)
- Drones stable at record low: ~27 UAVs — near yesterday's record low of 26
- No cruise missiles (2nd consecutive day without cruise; Day 12 had 7)
- Total daily projectiles: 34 — **new record low**, surpassing Day 13's 36
- Debris from intercepted attack hits DIFC Innovation Hub building in central Dubai — **no injuries** per Dubai Media Office
- Mojtaba Khamenei (new supreme leader) first public statement: vows Strait of Hormuz will remain closed as "tool of pressure"
- Iranian ambassador to UN contradicts Khamenei on Hormuz hours later — mixed signals
- US KC-135 refueling tanker crashes in western Iraq during Operation Epic Fury — 4 of 6 crew killed; Islamic Resistance in Iraq claims responsibility (CENTCOM says not hostile fire)
- Oil rebounds: Brent ~$99/bbl, WTI ~$95 — erasing most of IEA reserve release gains
- Saudi Arabia downs 10+ drones targeting Eastern and Central Provinces
- Israel launches new wide-scale wave of strikes across Tehran
- UAE Energy Minister confirms energy supplies stable, national energy system operating normally

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.168
  + λ_intercept          = -0.004
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.080  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.080** |
| λ 95th percentile | **2.780** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.5%** |
| P(λ > 2.0) | **56.8%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## What Changed Day 13 → Day 14

```
Day 13 → Day 14 Lambda Decomposition:

Component          Day 13           Day 14              Change
─────────────────────────────────────────────────────────────────
λ_launcher         -0.544           -0.544               0.000  (depletion maxed at 99%)
λ_drone            +0.165           +0.168              +0.003  (stockpile 18.2%→16.9%)
λ_intercept        -0.002           -0.004              -0.002  (cum rate improves 93.1%→93.3%)
λ_proxy            +0.500           +0.500               0.000  Still active (Iraq proxy claims KC-135)
λ_hormuz           +0.630           +0.630               0.000  Khamenei explicitly confirms closure
λ_weapon           +0.400           +0.400               0.000  No new weapon types
λ_bm_rebound       +0.000           +0.000               0.000  10→7 continues decline
λ_naval            -0.128           -0.128               0.000  2 carrier groups, unchanged
─────────────────────────────────────────────────────────────────
λ total (median)    2.110            2.080              -0.030
```

Key drivers of the Day 14 change:
1. **λ eases further (−0.030):** Continues the marginal easing trend from Day 13 (−0.031). No new escalation events. BMs decline (10→7), interception rate improves (93.3%), drone stockpile decline adds tiny positive contribution. Net effect is continued marginal easing.
2. **BMs resume decline (10→7):** After Day 13's uptick (6→10), BMs drop back to 7. The five-day pattern is now 12→9→6→10→7 — trending downward with one-day noise. This further confirms Iran's ballistic launcher depletion.
3. **Drone stabilization at record lows:** 27 drones (vs 26 yesterday) — virtually unchanged at historically low levels. Four consecutive days below 40 (35→39→26→27). Stockpile at 16.9% — on track for exhaustion in ~12 days at current rate.
4. **Khamenei statement locks in Hormuz closure:** New supreme leader's first public act is to confirm Hormuz stays closed, removing any ambiguity about near-term reopening. This keeps λ_hormuz firmly at +0.630.

**Net assessment:** λ eases from 2.110 to 2.080. The system remains in cascade territory but the trend is marginally improving for the third consecutive day (2.141 → 2.110 → 2.080). Attack volume at new record low (34 total). However, Khamenei's explicit Hormuz statement and oil rebound to $99 show that the structural instability factors dominating λ remain firmly in place.

---

## Defense Cost Update

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | 158 | THAAD @ $12.7M | $2,007 | $4,013 |
| BM (PAC-3, 40%) | 105 | PAC-3 @ $3.9M | $410 | $819 |
| Cruise Missiles | 15 | PAC-3 @ $3.9M | $59 | $117 |
| Drones | ~1,577 | SHORAD @ $0.7M | $1,104 | $2,208 |
| **TOTAL** | **~1,855** | | **$3,579** | **$7,157** |

### Oil Revenue Not Sold (Cumulative, 12 days Hormuz closure)

| Component | Volume | Revenue Loss |
|-----------|--------|-------------|
| Stranded oil (no Hormuz) | 1.7M bbl/d × 12 days × $95 | **$1,938M** |
| Voluntary production cuts | 0.5M bbl/d × 12 days × $95 | **$570M** |
| **TOTAL OIL LOSS** | | **$2,508M ($2.51B)** |

### Grand Total Cost to UAE (Day 14)

| Scenario | Defense | Oil Loss | **Grand Total** |
|----------|---------|----------|----------------|
| 1:1 | $3.58B | $2.51B | **$6.09B** |
| 1:2 | $7.16B | $2.51B | **$9.67B** |
| 1:3 | $10.74B | $2.51B | **$13.25B** |

*Note: Oil loss uses Day 14 WTI (~$95), significantly higher than Day 12-13's $86-$88 following IEA reserve release. Brent approaching $100 again as Khamenei confirms Hormuz closure. Oil rebound erases ~75% of IEA intervention gains. Ruwais refinery remains shut (922K bbl/d). Defense costs rising steadily as BMs (most expensive to intercept) continue at 7/day.*

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day14.png)

![Lambda Evolution](../charts/lambda_evolution_day14.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System remains in CASCADE territory (λ = 2.080, P(λ>1) = 100%).

**Day 14 key dynamics:**
- **Positive:** BMs resume decline (10→7), confirming Day 13's uptick was noise. Cumulative interception rate improves to 93.3% — best since Day 4. Total attack volume at **new record low** (34 projectiles). Zero combat fatalities. DIFC debris incident caused no injuries. UAE Energy Minister confirms energy supplies stable. Attack volume has collapsed ~90% from peak.
- **Negative:** Mojtaba Khamenei's first public statement as new supreme leader **explicitly confirms Hormuz stays closed** — removing any ambiguity about near-term reopening. Oil rebounds to ~$99/bbl, erasing IEA intervention gains. KC-135 tanker crash in Iraq kills 4 US crew (Operation Epic Fury). Islamic Resistance in Iraq claims responsibility. Ceasefire odds continue declining (~17%).
- **DIFC debris incident:** Intercepted attack showers debris on DIFC Innovation Hub in central Dubai — no injuries, but demonstrates that even successful interceptions pose risk to urban areas. This is the second consecutive day of debris/drone incidents in central Dubai.
- **Oil rebound:** Brent back near $100 after Khamenei's Hormuz statement. The IEA's record 400M barrel reserve release (Day 12) has lost ~75% of its price impact in just 2 days. Markets pricing in extended Hormuz closure.
- **Drone exhaustion accelerating:** At ~27/day, remaining ~337 drones last ~12 days (exhaustion ~Day 26, March 25). Four consecutive days below 40 drones. Iran may be forced to shift entirely to BMs or seek resupply — either outcome could trigger a new conflict phase.
- **Window:** Airport capacity ~50%. The continued low attack volume maintains the **tactical calm window** for evacuation. Khamenei's Hormuz statement signals no near-term de-escalation. Leave while volume is low.

---

## Sources

| Source | Type |
|--------|------|
| [@modgovae](https://x.com/modgovae/status/2032439385149604064) | UAE MOD update (March 13, 8:51 PM) |
| [Gulf News — Day 14 liveblog](https://gulfnews.com/uae/us-israel-war-on-iran-day-14-us-refuelling-aircraft-crashes-in-iraq-iran-threatens-gulf-energy-sites-1.500472879) | Daily situation |
| [Al Jazeera — Day 14](https://www.aljazeera.com/news/2026/3/13/iran-war-what-is-happening-on-day-14-of-us-israel-attacks) | Regional context |
| [The National — DIFC debris](https://www.thenationalnews.com/news/uae/2026/03/13/debris-hits-dubai-building-after-air-strike-intercepted-as-more-alerts-issued/) | Dubai debris incident |
| [NBC News — Khamenei Hormuz](https://www.nbcnews.com/world/iran/live-blog/live-updates-iran-war-oil-ship-attacks-hormuz-trump-israel-lebanon-rcna263101) | Khamenei statement |
| [CNBC — KC-135 crash](https://www.cnbc.com/2026/03/13/us-kc135-crash-iraq-iran-threats-shipping-attacks.html) | US military crash |
| [CBS News — Iran war paralyzes oil](https://www.cbsnews.com/live-updates/iran-war-us-israel-gulf-allies-strait-of-hormuz-attacks-oil-prices-stocks/) | Oil prices & conflict |
| [Polymarket](https://polymarket.com/event/us-x-iran-ceasefire-by) | Ceasefire odds |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-14 |
