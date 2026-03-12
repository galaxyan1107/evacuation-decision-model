# Day 13 Update — March 12, 2026

> 🌐 **EN** | [中文](../zh/updates/day13-march12.md)

**Status: UNSTABLE** | **Breaches: 3/5** | **λ median = 2.329**

---

## New Data

| Metric | Day 12 | Day 13 | Cumulative |
|--------|--------|--------|------------|
| Ballistic Missiles | 7 | **6** | **272** |
| BM Intercepted | 7 | 6 | 253 |
| Drones Detected | ~45 | ~42 | ~1,658 |
| Drones Intercepted | 38 | 39 | ~1,575 |
| Cruise Missiles | 0 | **7** | **15** |
| BM Intercept Rate (cum) | 92.9% | — | 93.0% |
| Drone Stockpile | 19.2% (384/2000) | — | 17.1% (342/2000) |

**Key Events:**
- **⚠️ CRUISE MISSILE ESCALATION:** 7 cruise missiles in a single day — first significant use since Day 3. Total cruise missiles nearly doubles (8→15). Signals shift to higher-value, harder-to-intercept munitions
- **Dubai Creek Harbour drone strike** — Iranian drone hits Address Creek Harbour 2 residential tower; fire contained to 1-2 apartments; all residents evacuated; no injuries
- BMs continue declining for 4th consecutive day (17→12→9→7→6), approaching pre-rebound levels
- US "most intense day of strikes" on Iran (Hegseth/Pentagon), targeting drone-manufacturing infrastructure — 90% reduction in Iranian missile launches claimed
- Oil: WTI ~$86, Brent ~$91; prices stabilizing post-IEA reserve release; Goldman Sachs raises Q4 Brent forecast
- Polymarket ceasefire by Mar 31: ~18% (↓ from 20%, 9th consecutive decline)
- 5 additional injuries (cumulative: 6 killed, ~131 injured across 27+ nationalities)

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.172
  + λ_intercept          = +0.000
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_cruise             = +0.200
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.150
  ──────────────────────────────
  λ median           = 2.329  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.329** |
| λ 95th percentile | **3.039** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **99.1%** |
| P(λ > 2.0) | **72.6%** |
| Verdict | **UNSTABLE** |
| Breaches | **3/5** (launcher, drone_stockpile, new_weapon) |

---

## What Changed Day 12 → Day 13

```
Day 12 → Day 13 Lambda Decomposition:

Component          Day 12           Day 13              Change
─────────────────────────────────────────────────────────────────
λ_launcher         -0.544           -0.544               0.000  (depletion maxed at 99%)
λ_drone            +0.162           +0.172              +0.010  (stockpile 19.2%→17.1%)
λ_intercept        +0.000           +0.000               0.000  (cum rate stable 92.9%→93.0%)
λ_proxy            +0.500           +0.500               0.000  Still active
λ_hormuz           +0.630           +0.630               0.000  Still closed
λ_weapon           +0.400           +0.400               0.000  DXB + Creek Harbour targeting
λ_cruise           +0.000           +0.200              +0.200  ⚠️ 7 cruise missiles (NEW vector)
λ_bm_rebound       +0.000           +0.000               0.000  Still broken (9→7→6)
λ_naval            -0.128           -0.150              -0.022  US "most intense" strikes improve deterrence
─────────────────────────────────────────────────────────────────
λ total (median)    2.141            2.329              +0.188
```

Key drivers of the Day 13 change:
1. **Cruise missile escalation** (+0.200): 7 cruise missiles in a single day is a qualitative shift. Cruise missiles are harder to intercept than ballistic missiles (lower radar cross-section, terrain-following flight), signaling Iran is deploying higher-capability weapons as drone stockpile depletes. This is a new λ component introduced on Day 13
2. **Drone stockpile continues declining** (+0.010): Remaining drones drop from 19.2% to 17.1% (342 of 2,000 estimated). At 42/day, exhaustion in ~8 days (Day 21, ~March 20). But if rate rebounds, exhaustion in 3-4 days
3. **Naval deterrence marginally improves** (−0.022): US "most intense day of strikes" on Iran claims 90% reduction in Iranian missile launches, targeting drone-manufacturing facilities. Marginal improvement but Hormuz still closed

**Net assessment:** λ jumps from 2.141 to 2.329 — the largest single-day increase since Day 8 (+0.868). The cruise missile escalation is the dominant driver. Iran appears to be shifting from drone saturation (exhausting) to cruise missile strikes (higher penetration, harder to intercept). This is precisely the "cost cascade" scenario predicted when drone stockpile breached 30% on Day 9.

---

## Defense Cost Update

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | 152 | THAAD @ $12.7M | $1,930 | $3,861 |
| BM (PAC-3, 40%) | 101 | PAC-3 @ $3.9M | $394 | $788 |
| Cruise Missiles | 15 | PAC-3 @ $3.9M | $59 | $117 |
| Drones | 1,575 | SHORAD @ $0.7M | $1,103 | $2,205 |
| **TOTAL** | **1,843** | | **$3,485** | **$6,971** |

### Oil Revenue Not Sold (Cumulative, 11 days Hormuz closure)

| Component | Volume | Revenue Loss |
|-----------|--------|-------------|
| Stranded oil (no Hormuz) | 1.7M bbl/d × 11 days × $88 | **$1,646M** |
| Voluntary production cuts | 0.5M bbl/d × 11 days × $88 | **$484M** |
| **TOTAL OIL LOSS** | | **$2,130M ($2.13B)** |

### Grand Total Cost to UAE (Day 13)

| Scenario | Defense | Oil Loss | **Grand Total** |
|----------|---------|----------|----------------|
| 1:1 | $3.49B | $2.13B | **$5.61B** |
| 1:2 | $6.97B | $2.13B | **$9.10B** |
| 1:3 | $10.46B | $2.13B | **$12.58B** |

*Note: Oil loss uses blended average price ($88) — WTI crashed from $100 to $86 on Day 12 (IEA reserve release), recovering slightly to ~$88 average by Day 13. Ruwais refinery (922K bbl/d) remains shut — domestic refining losses not captured above. Cruise missile interceptor cost (PAC-3 at $3.9M each) significantly higher than drone SHORAD at $0.7M — confirms cost cascade as Iran shifts to cruise missiles.*

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day13.png)

![Lambda Evolution](../charts/lambda_evolution_day13.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** λ jumps to 2.329 on cruise missile escalation — system moves deeper into CASCADE territory.

**Day 13 key dynamics:**
- **Positive:** BMs continue declining (7→6, 4th consecutive day, all intercepted 100%). US claims "most intense day of strikes" targeting Iranian drone/missile factories — potential to degrade Iran's production capacity. Oil prices stabilizing ~$86-91 post-IEA intervention
- **Negative:** **⚠️ CRUISE MISSILE ESCALATION** — 7 cruise missiles in one day (total conflict: 15, nearly all in Days 2-3 and now Day 13). This is the predicted "cost cascade": as drone stockpile depletes (17.1%), Iran shifts to cruise missiles which are harder to intercept and cost $3.9M/each to counter (vs $0.7M for drones). Dubai Creek Harbour residential tower hit by drone — fire contained but demonstrates continued precision targeting of civilian infrastructure. Polymarket ceasefire drops to ~18% (9th consecutive decline). Drone stockpile at 17.1% (342 of est. 2,000 remaining)
- **Critical assessment:** The cruise missile vector fundamentally changes the defense economics. At 7 cruise/day × $3.9M = $27.3M/day in interceptor cost alone — 4× the cost of intercepting 42 drones ($29.4M at 1:1). If Iran sustains or increases cruise missile volume while drone stockpile approaches exhaustion, defense cost per day rises sharply even as total projectile count falls
- **Window:** Airport capacity ~55%, still operational but further reduced. Creek Harbour strike demonstrates willingness to target residential areas near aviation hubs. **Use this window now — cruise missile escalation makes subsequent windows less predictable**

---

## Sources

| Source | Type |
|--------|------|
| [@modgovae](https://x.com/modgovae) | UAE MOD daily update (March 12) |
| [Sharjah24 — UAE intercepts 6 BM, 7 cruise, 39 UAVs](https://sharjah24.ae/en/Articles/2026/03/12/UAE-air-defences-intercept-missiles-drones-from-Iran) | MOD data |
| [Gulf Business — Creek Harbour drone fire](https://gulfbusiness.com/dubai-fire-brought-under-control-amid-drone-incident-near-creek-harbour/) | Creek Harbour strike |
| [NBC News — "Most intense" US strikes on Iran](https://www.nbcnews.com/world/iran/live-blog/live-updates-iran-war-oil-prices-trump-hormuz-israel-rcna262670) | US military |
| [Goldman Sachs — Q4 Brent forecast raised](https://money.usnews.com/investing/news/articles/2026-03-11/goldman-sachs-raises-q4-brent-wti-crude-price-forecast-amid-longer-hormuz-disruption) | Oil market |
| [Polymarket](https://polymarket.com/event/us-x-iran-ceasefire-by) | Ceasefire odds |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-12 |
