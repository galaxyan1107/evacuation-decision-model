# Daily Tracker — Day-by-Day Change Log

> 🌐 **EN** | [中文](../zh/updates/daily-tracker.md)

**Last Updated: March 9, 2026 (Day 10)**

This page tracks daily changes across all model inputs, compares model predictions against observed data, and flags breaches as they occur.

---

## Model vs Actual — Divergence Summary

### Divergence Heatmap

Day-by-day percentage deviation across all 6 tracked metrics. Red = actual exceeds model, blue = actual below model. Lambda divergence dominates from Day 3 onward (+240% → +447%).

![Divergence Heatmap](../charts/divergence_heatmap.png)

### 6-Panel Comparison

Side-by-side model (blue) vs actual (red) with ribbon fill showing the gap. Airport (green) is the only positive divergence. Lambda (bottom-right) shows deep cascade zone. Drone stockpile (bottom-center) breaches 30% threshold on Day 9.

![Model vs Actual](../charts/model_vs_actual_bars.png)

### Scorecard & Verdict Timeline

Stacked divergence shows lambda (purple) dominating total model error. Verdict timeline: model predicted METASTABLE for all 9 days — reality crossed to UNSTABLE on Day 3 and never returned.

![Divergence Scorecard](../charts/divergence_scorecard.png)

### Lambda Evolution

λ jumped from 0.47 → 1.70 on Day 3 (Hormuz closure) and reached 2.71 on Day 9 (drone stockpile breach + sustained BM rebound), then eased to 2.06 on Day 10 (BM rebound breaks, naval deterrence increases). P(λ>1) has been 100% since Day 3.

![Lambda Evolution](../charts/lambda_evolution_day10.png)

### Ballistic Missile Trajectory

The model's exponential decay assumption (β=0.25/day) broke down from Day 5 onward. Days 5→9: 3→7→9→16→17 showed an accelerating rebound. Day 10 (12 BMs) breaks the monotonic trend — first decline in 5 days — though volume remains elevated well above model predictions.

![BM Trajectory](../charts/bm_trajectory.png)

---

## Attack Volume Tracker

### Daily New Attacks

| Day | Date | BM (New) | Model BM | Drones | Model Drones | Cruise | Total | Trend |
|-----|------|----------|----------|--------|-------------|--------|-------|-------|
| 1 | Feb 28 | **137** | — | 209 | — | 0 | 346 | Opening salvo |
| 2 | Mar 1 | **28** | — | 332 | — | 2 | 362 | Peak drone day |
| 3 | Mar 2 | **9** | ~19 | 148 | ~130 | 6 | 163 | BM faster than model decay |
| 4 | Mar 3 | **12** | ~14 | 123 | ~130 | 0 | 135 | BM uptick (noise?) |
| 5 | Mar 4 | **3** | ~10 | 129 | ~130 | 0 | 132 | BM near-zero |
| 6 | Mar 5 | **7** | ~8 | 131 | ~130 | 0 | 138 | BM rebound |
| 7 | Mar 6 | **9** | ~6 | 112 | ~130 | 0 | 121 | ⚠️ BM broke monotonic decay |
| 8 | Mar 7 | **16** | ~4 | ~125 | ~130 | 0 | 141 | ⚠️⚠️ BM REBOUND — highest since Day 2 |
| **9** | **Mar 8** | **17** | ~3 | 117 | ~130 | 0 | **134** | ⚠️⚠️ BM sustained high — 16→17 |
| **10** | **Mar 9** | **12** | ~2 | 110 | ~130 | 0 | **122** | BM drops 17→12: rebound breaks |

### Cumulative Totals

| Day | Date | Cum. BM | Cum. Drones | Cum. Cruise | Cum. Total |
|-----|------|---------|-------------|-------------|------------|
| 1 | Feb 28 | 137 | 209 | 0 | 346 |
| 2 | Mar 1 | 165 | 541 | 2 | 708 |
| 3 | Mar 2 | 174 | 689 | 8 | 871 |
| 4 | Mar 3 | 186 | 812 | 8 | 1,006 |
| 5 | Mar 4 | 189 | 941 | 8 | 1,138 |
| 6 | Mar 5 | 196 | 1,072 | 8 | 1,276 |
| 7 | Mar 6 | 205 | 1,184 | 8 | 1,397 |
| 8 | Mar 7 | 221 | ~1,309 | 8 | ~1,538 |
| **9** | **Mar 8** | **238** | **~1,422** | **8** | **~1,668** |
| **10** | **Mar 9** | **250** | **~1,536** | **8** | **~1,794** |

---

## Interception Rate Tracker

| Day | Date | BM Detected | BM Intercepted | Day Rate | Cum. Rate | Threshold (<90%) | Status |
|-----|------|-------------|----------------|----------|-----------|-------------------|--------|
| 1 | Feb 28 | 137 | 132 | 96.4% | 96.4% | OK | OK |
| 2 | Mar 1 | 28 | 20 | 71.4% | 92.1% | ⚠️ Day breach | Cum OK |
| 3 | Mar 2 | 9 | 9 | 100% | 93.6% | OK | OK |
| 4 | Mar 3 | 12 | 11 | 91.7% | 93.0% | OK | OK |
| 5 | Mar 4 | 3 | 3 | 100% | 93.1% | OK | OK |
| 6 | Mar 5 | 7 | 6 | **85.7%** | 93.4% | ⚠️ Day breach, 1 landed | **ALERT** |
| 7 | Mar 6 | 9 | 9 | 100% | 92.7% | OK | OK |
| 8 | Mar 7 | 16 | 15 | 93.8% | 92.8% | OK | ⚠️ BM rebound to 16 |
| **9** | **Mar 8** | **17** | **16** | **94.1%** | **92.9%** | OK | ⚠️ BM sustained high: 16→17 |
| **10** | **Mar 9** | **12** | **11** | **91.7%** | **92.8%** | OK | BM drops 17→12: rebound breaks |

**Day 6 breach note:** 1 ballistic missile landed inside UAE territory on March 5 — first confirmed BM ground impact.

**Day 8 critical note:** 16 BMs detected — highest since Day 2 (28). Days 5→8 show **accelerating** trend: 3→7→9→16. This contradicts the exponential decay model and suggests either hidden TELs activated or resupply from deeper storage. Launcher depletion estimate revised from 85.7% to **~73%**.

**Day 9 critical note:** 17 BMs detected — surpasses Day 8. Consecutive high-volume days (16→17) confirm the rebound is structural, not a single-day anomaly. Launcher depletion estimate revised further to **~67%**. Drone stockpile breaches 30% threshold for the first time (28.9%).

**Day 10 note:** 12 BMs detected — first daily decline in 5 days, breaking the 3→7→9→16→17 accelerating trend. However, volume remains elevated well above model predictions (~2 BMs/day at this point in the decay curve). Launcher depletion estimate revised up to **~99%** — cumulative 250 BMs against 40 TELs suggests near-exhaustion.

---

## Drone Stockpile Tracker

| Day | Date | Daily Launched | Cum. Launched | Est. Remaining | % Remaining | Threshold (<30%) |
|-----|------|---------------|---------------|----------------|-------------|-------------------|
| 1 | Feb 28 | 209 | 209 | 1,791 | 89.6% | OK |
| 2 | Mar 1 | 332 | 541 | 1,459 | 73.0% | OK |
| 3 | Mar 2 | 148 | 689 | 1,311 | 65.6% | OK |
| 4 | Mar 3 | 123 | 812 | 1,188 | 59.4% | OK |
| 5 | Mar 4 | 129 | 941 | 1,059 | 53.0% | OK |
| 6 | Mar 5 | 131 | 1,072 | 928 | 46.4% | OK |
| 7 | Mar 6 | 112 | 1,184 | 816 | 40.8% | OK |
| 8 | Mar 7 | ~125 | ~1,309 | ~691 | 34.5% | Approaching |
| **9** | **Mar 8** | **117** | **~1,422** | **~578** | **28.9%** | **⚠️ BREACHED** |
| **10** | **Mar 9** | **110** | **~1536** | **~464** | **23.2%** | **⚠️ BREACHED** |

~~At current rate (~120/day), stockpile hits 30% threshold around Day 11 (March 10).~~ **BREACHED on Day 9** — 2 days earlier than predicted. At current burn rate (~110/day), full exhaustion estimated Day 14 (~March 13). Drone rate declining (117→110) but stockpile erosion continues relentlessly.

---

## Cascade Threshold Tracker

| Metric | Day 1 | Day 3 | Day 5 | Day 7 | Day 8 | Day 9 | Day 10 | Threshold |
|--------|-------|-------|-------|-------|-------|-------|--------|-----------|
| Launcher Depletion | ~39% | ~50% | ~54% | 85.7% | ~73% | ~67% | **~99%** | > 85% |
| Drone Stockpile | 89.6% | 65.6% | 53.0% | 40.8% | 34.5% | 28.9% | **23.2%** | < 30% |
| Interception Rate (cum) | 96.4% | 93.6% | 93.1% | 92.7% | 92.8% | 92.9% | 92.8% | < 90% |
| Daily Casualties | ~22/d | ~18/d | ~15/d | ~16/d | ~14/d | ~15/d | **2/d** | > 10 |
| New Weapon Type | No | No | No | No | Air base | Air base | Air base | Yes |

*Launcher depletion **revised downward** from 85.7% to ~73% (Day 8) and further to **~67%** (Day 9) due to consecutive high-volume BM days (16→17). The accelerating trend 3→7→9→16→17 confirms more TELs remain operational than previously estimated. Drone stockpile has **breached** the 30% threshold on Day 9 — 2 days earlier than forecast.

| Day | Breaches | Verdict |
|-----|----------|---------|
| 1 | 1/5 (casualties) | METASTABLE |
| 3 | 1/5 | METASTABLE |
| 5 | 1/5 | METASTABLE |
| 7 | 2/5 (launcher + casualties) | METASTABLE |
| 8 | 4/5 (launcher + interception day + casualties + air base) | UNSTABLE |
| 9 | 3/5 (casualties + new_weapon + drone_stockpile) | UNSTABLE |
| **10** | **2/5** (launcher + **drone_stockpile**) | **UNSTABLE** |

---

## Lambda (λ) Evolution

| Day | λ Median | P(λ > 1) | 95th Pctl | Verdict | Key Change |
|-----|----------|----------|-----------|---------|------------|
| 1 | ~0.75 | ~12% | ~1.52 | METASTABLE | Initial assessment |
| 7 (2 CSGs) | 0.739 | 12.2% | 1.523 | METASTABLE | Baseline model |
| 7 (3 CSGs) | 0.496 | 5.8% | 1.063 | METASTABLE | CVN-77 deploying, proxy/Hormuz lowered |
| 8 (corrected) | 2.589 | 100% | 3.304 | UNSTABLE | Hormuz + proxy + air base + BM rebound |
| 9 | 2.712 | 100% | 3.481 | UNSTABLE | Drone stockpile breach + BM sustained |
| **10** | **2.061** | **100%** | **2.770** | **UNSTABLE** | BM rebound breaks (17→12), λ eases but still CASCADE |

### What Changed on Day 8

```
Day 7 → Day 8 Lambda Decomposition:

Component          Day 7 (3 CSG)    Day 8 (corrected)   Change
─────────────────────────────────────────────────────────────────
λ_launcher         -0.471           -0.401              +0.070  (depletion 85.7%→~73%)
λ_drone            +0.148           +0.164              +0.016  (stockpile lower)
λ_intercept        +0.020           +0.020               0.000
λ_proxy             0.000*          +0.500              +0.500  ⚠️ Hezbollah partial
λ_hormuz            0.000*          +0.630              +0.630  ⚠️ REALIZED
λ_weapon            0.000*          +0.400              +0.400  ⚠️ Air base strike
λ_bm_rebound        0.000           +0.300              +0.300  ⚠️ 16 BM (accelerating)
λ_naval            -0.240           -0.184              +0.056  (CVN-77 not yet arrived)
─────────────────────────────────────────────────────────────────
λ total (median)    0.496            2.589              +2.093

* Stochastic tail risks, expected value ~0 at P=2-4%
```

---

## Scenario Probability Tracker

### Model Bayesian Posteriors (calibrated)

| Scenario | Day 6 | Day 14 | Day 30 | Day 9 Assessment |
|----------|-------|--------|--------|------------------|
| Ceasefire | 3.3% | 7.8% | 12.8% | ↓ Polymarket 59% (still declining) |
| Baseline | 64.9% | 71.2% | 75.4% | ↓↓ Hormuz + stockpile depletion challenges baseline |
| Escalation | 31.4% | 20.1% | 11.7% | ↑↑ Multiple escalation events realized |
| Regime War | 0.4% | 0.9% | 0.1% | ↑ Air base strike + sustained BM raises floor |

### Polymarket Ceasefire Odds

| Date | By Mar 31 | Direction |
|------|-----------|-----------|
| Mar 5 (Day 6) | 67% | — |
| Mar 6 (Day 7) | 63% | ↓ |
| Mar 7 (Day 8) | 61% | ↓ |
| Mar 8 (Day 9) | 59% | ↓ |
| **Mar 9 (Day 10)** | **24%** | **↓↓↓** |

Ceasefire odds **collapsed** — from 59% to 24% in a single day. Six consecutive days of decline (67%→24%). Markets now pricing extended, entrenched conflict with no near-term resolution.

---

## Airport & Flight Tracker

| Day | Date | Airport Capacity | Model Predicted | Flights/Day | Status |
|-----|------|-----------------|-----------------|-------------|--------|
| 1 | Feb 28 | 30% (pre-strike) | 30% | Normal ops | OK |
| 2 | Mar 1 | **0%** (closed) | 0% | All suspended | MATCH |
| 3 | Mar 2 | ~2% | 2% | Exceptional only | MATCH |
| 4 | Mar 3 | ~5% | 3% | Partial Abu Dhabi | CLOSE |
| 5 | Mar 4 | ~8% | 8% | Limited routes | MATCH |
| 6 | Mar 5 | ~15% | 12% | Etihad resumes | CLOSE |
| 7 | Mar 6 | ~25% | 15% | Emirates 40% network | **AHEAD** |
| 8 | Mar 7 | ~55% | 35% | Emirates 60%, Etihad ~25 dest | WELL AHEAD |
| 9 | Mar 8 | ~60% | 40% | Emirates targeting 100%; Air Arabia Mar 9 | **WELL AHEAD** |
| **10** | **Mar 9** | **~65%** | **45%** | Air Arabia resumes; Emirates nearing 100% | **WELL AHEAD** |

**Positive divergence:** Airport recovery is 1.6× faster than model predicted. Emirates targeting 100% capacity "in coming days," operating 106+ flights/day to 83+ destinations. Etihad serving ~25 key destinations. Air Arabia resumes March 9. ~250K passenger backlog being cleared.

---

## Casualty Tracker

| Day | Date | Daily Killed | Daily Injured | Cum. Killed | Cum. Injured | Daily Total | Threshold (>10) |
|-----|------|-------------|-------------- |-------------|-------------|-------------|-----------------|
| 1 | Feb 28 | 0 | 15 | 0 | 15 | 15 | **BREACHED** |
| 2 | Mar 1 | 1 | 22 | 1 | 37 | 23 | **BREACHED** |
| 3 | Mar 2 | 0 | 12 | 1 | 49 | 12 | **BREACHED** |
| 4 | Mar 3 | 1 | 10 | 2 | 59 | 11 | **BREACHED** |
| 5 | Mar 4 | 0 | 8 | 2 | 67 | 8 | OK |
| 6 | Mar 5 | 1 | 11 | 3 | 78 | 12 | **BREACHED** |
| 7 | Mar 6 | 0 | 15 | 3 | 93 | 15 | **BREACHED** |
| 8 | Mar 7 | 0 | ~19 | 3 | ~112 | ~19 | **BREACHED** |
| 9 | Mar 8 | 1 | 0 | 4 | 112 | 1 | OK |
| **10** | **Mar 9** | **0** | **2** | **4** | **114** | **2** | OK |

**Note:** Casualty figures from WAM (Emirates News Agency) and Reuters. Remarkably low given attack volume, attributable to >92% interception rates and effective civil defense.

**Day 9 note:** 4th fatality — Pakistani driver killed in Al Barsha, Dubai, when interception debris struck his vehicle. Total injuries now ~130 across 17+ nationalities.

---

## Economic Impact Tracker

| Day | Date | Oil (WTI) | Weekly Δ | Hormuz Status | VLCC Rate | Key Event |
|-----|------|----------|----------|---------------|-----------|-----------|
| 1 | Feb 28 | $72 | — | Open | $218K/d | US-Israel strikes Iran |
| 2 | Mar 1 | $78 | +8.3% | Open | $245K/d | Iran retaliates |
| 3 | Mar 2 | $82 | +13.9% | **CLOSED** | $310K/d | IRGC closes Hormuz |
| 4 | Mar 3 | $86 | +19.4% | Closed | $380K/d | Container ship hit |
| 5 | Mar 4 | $90 | +25.0% | Near-zero traffic | $400K/d | 5 crossings only |
| 6 | Mar 5 | $93 | +29.2% | Zero traffic | $410K/d | Maersk suspends Gulf |
| 7 | Mar 6 | $95 | +31.9% | Zero traffic | $420K/d | 150 vessels trapped |
| 8 | Mar 7 | $97 | +35.6% | Zero traffic | $424K/d | Record VLCC rate |
| 9 | Mar 8 | ~$100 | +38.9% | Zero traffic | ~$430K/d | Brent hits $100; Morgan Stanley raises forecast |
| **10** | **Mar 9** | **$103** | **+43.1%** | **Zero traffic** | **~$435K/d** | **WTI $103; Brent touches $119 intraday** |

---

## Key Events Timeline

| Day | Date | Category | Event | Model Impact |
|-----|------|----------|-------|--------------|
| 1 | Feb 28 | ATTACK | Iran launches 137 BM + 209 drones at UAE | Opening parameters set |
| 1 | Feb 28 | MILITARY | US Operation Epic Fury commences | — |
| 2 | Mar 1 | ATTACK | Peak drone day: 332 launched | Drone rate calibrated |
| 2 | Mar 1 | CASUALTY | First fatality (Pakistani national) | Casualties > 10/day |
| 3 | Mar 2 | **HORMUZ** | **IRGC declares Strait closed** | **λ_hormuz: 0→+0.63** |
| 3 | Mar 2 | PROXY | Hezbollah launches rockets at Israel | λ_proxy partial |
| 4 | Mar 3 | MARITIME | Container ship hit in Strait of Hormuz | Hormuz confirmed |
| 4 | Mar 3 | CASUALTY | Second fatality (Bangladeshi national) | — |
| 5 | Mar 4 | BM | BM drops to 3 — near-zero | Supports decay model |
| 5 | Mar 4 | MARITIME | Only 5 vessels transit Hormuz | Near-total blockade |
| 6 | Mar 5 | **BM BREACH** | **1 BM lands inside UAE** (Day int. rate 85.7%) | Interception threshold |
| 6 | Mar 5 | AVIATION | Etihad resumes limited flights | Airport ahead of model |
| 6 | Mar 5 | CASUALTY | Third fatality | — |
| 7 | Mar 6 | BM | 9 BM — breaks monotonic decay (up from 7) | Model divergence |
| 7 | Mar 6 | AVIATION | Emirates at 40% network | Airport well ahead |
| 7 | Mar 6 | NAVAL | CVN-77 Bush completes COMPTUEX, returns Norfolk | 3rd CSG confirmed |
| **8** | **Mar 7** | **ESCALATION** | **IRGC claims strike on Al Dhafra air base** | **λ_weapon: 0→+0.40** |
| 8 | Mar 7 | AVIATION | Emirates 60% network, 106 flights/day | Airport 1.5× model |
| 8 | Mar 7 | CIVIL | Dubai shelter-in-place alert | Escalation signal |
| 8 | Mar 7 | BM | 16 BMs detected — highest since Day 2 | BM rebound confirmed |
| **9** | **Mar 8** | **BM** | **17 BMs — back-to-back high (16→17)** | **Rebound is structural** |
| 9 | Mar 8 | **DRONE** | **Drone stockpile breaches 30% (28.9%)** | **λ_drone: +0.079** |
| 9 | Mar 8 | CASUALTY | 4th killed — Pakistani driver, Al Barsha Dubai | Debris from interception |
| 9 | Mar 8 | OIL | Brent approaches $100; +39% since Feb 28 | Record weekly gain |
| 9 | Mar 8 | AVIATION | Emirates targeting 100%; Air Arabia resumes Mar 9 | Airport 1.6× model |
| **10** | **Mar 9** | **BM** | **12 BMs — first daily decline in 5 days (17→12)** | **BM rebound breaks; λ_bm_rebound → 0** |
| 10 | Mar 9 | OIL | WTI $103, Brent intraday $119 | Record prices |
| 10 | Mar 9 | MARKET | Polymarket ceasefire crashes to 24% (from 59%) | Market sees no resolution |
| 10 | Mar 9 | CASUALTY | 2 injured in Abu Dhabi from interception debris | — |
| 10 | Mar 9 | AVIATION | Air Arabia resumes; Emirates nearing 100% | Airport 1.4× model |

---

## Model vs Reality Scorecard (Running)

| # | Check | Model | Day 9 Observed | Day 10 Observed | Status |
|---|-------|-------|----------------|-----------------|--------|
| 1 | BM monotonic decay | Yes | 16→17 (sustained) | 17→12 (breaks rebound) | **DIVERGENT** (easing) |
| 2 | Interception > 90% (cum) | 93.2% | 92.9% | 92.8% | **MATCH** |
| 3 | Drone rate ~130/day | ~130/day | 117/day | 110/day | **CLOSE** (declining) |
| 4 | No new weapon types | No | Air base (cont.) | Air base (cont.) | **DIVERGENT** |
| 5 | Ceasefire P (Polymarket) | 84% | 59% | **24%** | **DIVERGENT** (collapsed) |
| 6 | Airport recovery | 45% (D10) | ~60% | **~65%** | **DIVERGENT** (positive) |
| 7 | Drone stockpile > 30% | 28.9% | 28.9% | **23.2%** | **⚠️ CRITICAL** |
| 8 | Hormuz open | P=98% open | CLOSED | **CLOSED** | **DIVERGENT** |
| 9 | No proxy activation | P=96% none | Houthis threatening | Houthis threatening | **DIVERGENT** |
| 10 | Verdict | METASTABLE | UNSTABLE | **UNSTABLE** | **DIVERGENT** |

**Day 10 Rating: 1 MATCH, 1 CLOSE, 8 DIVERGENT**

Mixed signals: BM volume dropped for the first time in 5 days (positive), but Polymarket ceasefire odds collapsed from 59% to 24% (extremely negative), and drone stockpile continues eroding (23.2%). **Net assessment: tactical improvement (BM decline) but strategic deterioration (market pricing extended war).**

---

## Recommendation History

| Day | Risk Score | λ Median | Verdict | Recommendation |
|-----|-----------|----------|---------|---------------|
| 1 | ~100 | — | — | **LEAVE IMMEDIATELY** |
| 3 | ~80 | — | METASTABLE | **LEAVE — good window** |
| 5 | ~65 | — | METASTABLE | **LEAVE — window closing** |
| 7 | ~55 | 0.496 | METASTABLE | **LEAVE — depart today** |
| 8 | ~50 | 2.589 | UNSTABLE | EVACUATE IMMEDIATELY |
| 9 | ~48 | 2.712 | UNSTABLE | EVACUATE IMMEDIATELY |
| **10** | **~45** | **2.061** | **UNSTABLE** | **EVACUATE IMMEDIATELY** |

Despite λ easing from 2.712 to 2.061 (driven by BM rebound breaking and increased naval deterrence), the system remains **firmly in cascade territory**. The structural destabilizers — Hormuz closure, proxy activation, air base vulnerability — persist unchanged.

**Day 10 key dynamics:**
- **Positive:** BM drops 17→12, breaking the 5-day accelerating trend. Launcher depletion revised up (~99%), suggesting attrition is working
- **Negative:** Polymarket ceasefire odds collapse to 24% (from 59%) — market sees no near-term resolution. Drone stockpile at 23.2% continues eroding (~4 days to exhaustion at current burn rate). Oil surges past $103 WTI / $119 Brent intraday
- **Window:** Airport capacity ~65% provides a **usable but narrowing evacuation window**. Emirates targeting 100% imminently. Use it before drone exhaustion forces a BM-only phase.
