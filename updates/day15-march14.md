# Day 15 Update — March 14, 2026

> 🌐 **EN** | [中文](../zh/updates/day15-march14.md)

**Status: UNSTABLE** | **Breaches: 2/5** | **λ median = 2.054**

---

## New Data

| Metric | Day 14 | Day 15 | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | 7 | **9** | **294** |
| BM Intercepted | ~7 | ~9 | ~294 (engaged) |
| Drones Detected | ~27 | **33** | **1,600** |
| Drones Intercepted | ~21 | ~26 | ~1,600 (engaged) |
| Cruise Missiles | 0 | 0 | 15 |
| BM Intercept Rate (cum) | ~93.3% | — | — (not broken out since Day 12) |
| Drone Stockpile | 16.9% (337/2000) | — | 20.0% (400/2000) |

**@modgovae official (14 March 2026):** "UAE air defences engage 9 ballistic missiles, 33 UAVs. The UAE air defence systems on 14th March engaged 9 ballistic missiles and 33 UAVs launched from Iran. Since the onsets of the blatant Iranian aggression, UAE air defences have engaged 294 ballistic missiles, 15 cruise missiles and 1600 UAVs."

**Key Events:**
- **US strikes 90+ military targets on Iran's Kharg Island** — Pentagon says oil infrastructure "preserved" but military facilities destroyed. Trump says US "totally obliterated every military target"
- **IRGC warns UAE** that US "hideouts" in the Emirates are "legitimate targets" following Kharg strikes — direct threat escalation
- Oil surges: **Brent closes at $103.14, WTI at $98.71** — second consecutive day above $100. Oil up ~44% since war began
- Dubai airport open for confirmed passengers only — Emirates at **~55% capacity**. BA, Air Canada, Finnair extend cancellations through late March/April
- Iraq US embassy helipad hit by missile — air defense system destroyed
- 12 medical workers killed in Israeli strike on Lebanon health center
- Iran's UN ambassador signals willingness to negotiate — contradicts Khamenei's hardline stance
- Trump says considering "taking over" Strait of Hormuz
- US gas prices average $3.68/gallon — up 23% since war began

---

## Lambda Recalculation

```
λ = 1.0
  + λ_launcher           = -0.544
  + λ_drone              = +0.200
  + λ_intercept          = -0.004
  + λ_hormuz             = +0.630
  + λ_proxy              = +0.500
  + λ_weapon             = +0.400
  + λ_bm_rebound         = +0.000
  + λ_naval              = -0.128
  ──────────────────────────────
  λ median           = 2.054  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **2.054** |
| λ 95th percentile | **2.750** |
| P(λ > 1.0) | **100.0%** |
| P(λ > 1.5) | **97.2%** |
| P(λ > 2.0) | **54.1%** |
| Verdict | **UNSTABLE** |
| Breaches | **2/5** (launcher, drone_stockpile) |

---

## What Changed Day 14 → Day 15

```
Day 14 → Day 15 Lambda Decomposition:

Component          Day 14           Day 15              Change
─────────────────────────────────────────────────────────────────
λ_launcher         -0.544           -0.544               0.000  (depletion maxed at 99%)
λ_drone            +0.168           +0.200              +0.032  (stockpile 16.9%→~20.0%, drone uptick)
λ_intercept        -0.004           -0.004               0.000  (rate stable — no breakdown reported)
λ_proxy            +0.500           +0.500               0.000  Iraq embassy helipad struck
λ_hormuz           +0.630           +0.630               0.000  Hormuz closed, Day 15
λ_weapon           +0.400           +0.400               0.000  No new weapon types
λ_bm_rebound       +0.000           +0.000               0.000  7→9 slight uptick but within range
λ_naval            -0.128           -0.128               0.000  2 carrier groups, unchanged
─────────────────────────────────────────────────────────────────
λ total (median)    2.080            2.054              -0.026
```

Key drivers of the Day 15 change:
1. **λ eases further (−0.026):** Fourth consecutive day of marginal easing (2.141 → 2.110 → 2.080 → 2.054). Attack volume remains low. However, the IRGC threat against UAE is a qualitative escalation not captured in the quantitative model.
2. **BMs uptick slightly (7→9):** After declining to 7, BMs tick up to 9. Still well below the 12-17/day range from Days 8-10. Five-day pattern: 6→10→7→**9** — stabilizing around single digits. Confirms launcher depletion thesis.
3. **Drones surge to 33:** Highest since Day 12 (39). After four consecutive days below 30 (35→26→27), this represents a notable uptick. May reflect new production batch or stockpile reallocation. Stockpile estimate needs upward revision if Iran is replenishing.
4. **Kharg Island strikes — major escalation:** US attacks on Iran's main oil export hub represent the most strategically significant US strike of the war. While oil infrastructure was spared, the signal is clear: Iran's economic lifeline is now a target. This could trigger Iranian retaliation escalation.
5. **IRGC direct threat to UAE:** The explicit warning that US "hideouts" in the UAE are "legitimate targets" is a qualitative escalation. This could indicate Iran is considering attacks on non-military targets in the UAE.

**Net assessment:** λ eases from 2.080 to 2.054 quantitatively, but the qualitative threat environment has worsened significantly. Kharg strikes + IRGC threat to UAE = strategic escalation that the model's lambda may understate. Oil above $100 for a second day. The narrow tactical window for evacuation remains open but the IRGC threat makes it more urgent.

---

## Defense Cost Update

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | ~176 | THAAD @ $12.7M | $2,239 | $4,478 |
| BM (PAC-3, 40%) | ~118 | PAC-3 @ $3.9M | $459 | $918 |
| Cruise Missiles | 15 | PAC-3 @ $3.9M | $59 | $117 |
| Drones | ~1,600 | SHORAD @ $0.7M | $1,120 | $2,240 |
| **TOTAL** | **~1,909** | | **$3,876** | **$7,753** |

### Oil Revenue Not Sold (Cumulative, 13 days Hormuz closure)

| Component | Volume | Revenue Loss |
|-----------|--------|-------------|
| Stranded oil (no Hormuz) | 1.7M bbl/d × 13 days × $103 | **$2,276M** |
| Voluntary production cuts | 0.5M bbl/d × 13 days × $103 | **$670M** |
| **TOTAL OIL LOSS** | | **$2,946M ($2.95B)** |

### Grand Total Cost to UAE (Day 15)

| Scenario | Defense | Oil Loss | **Grand Total** |
|----------|---------|----------|----------------|
| 1:1 | $3.88B | $2.95B | **$6.82B** |
| 1:2 | $7.75B | $2.95B | **$10.70B** |
| 1:3 | $11.63B | $2.95B | **$14.58B** |

*Note: Oil loss uses Day 15 Brent (~$103). Hormuz closure now in Day 13. Brent above $100 for second consecutive day despite IEA's 400M barrel reserve release. Defense costs surging as total intercepts approach 2,000. IRGC threat to attack US facilities in UAE could sharply increase future costs if attacks escalate.*

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day15.png)

![Lambda Evolution](../charts/lambda_evolution_day15.png)

---

## Recommendation

**EVACUATE IMMEDIATELY.** System remains in CASCADE territory (λ = 2.054, P(λ>1) = 100%).

**Day 15 key dynamics:**
- **Positive:** BMs remain in single digits (9), well below Day 8-10 peak of 12-17/day. Cumulative interception rate appears strong. Total daily projectiles (42) still far below peak. Dubai airport maintaining ~55% capacity. Diplomatic signals from Iran's UN ambassador suggest some internal debate on de-escalation. Fourth consecutive day of λ easing.
- **Negative:** **IRGC explicitly threatens US facilities in the UAE** — most direct threat to UAE sovereignty since the war began. US strikes on Kharg Island mark a major strategic escalation that could trigger disproportionate retaliation. Oil above $103 (Brent) for second day. Drone uptick to 33 breaks the four-day downtrend. Iraq embassy helipad destroyed — proxy attacks on US interests intensifying. Ceasefire odds declining (~15%).
- **CRITICAL — IRGC threat:** The IRGC's warning that US "hideouts" in the UAE are legitimate targets represents a potential phase change. If Iran shifts from indiscriminate ballistic/drone attacks to deliberately targeting US military facilities in the UAE, the conflict dynamic changes fundamentally. This could bring direct Iranian special operations or precision-guided munitions against specific UAE locations.
- **Kharg Island escalation dynamics:** US strikes on Iran's oil hub signal willingness to target Iran's economic lifeline. Iran's likely response options: (1) escalate attacks on Gulf shipping, (2) target US bases in UAE/Gulf, (3) attempt to reclose any Hormuz partial reopening. All three scenarios increase UAE risk.
- **Window:** Airport at ~55% but airlines extending cancellations (BA through end of March, Air Canada through May). Commercial exit options narrowing each day. The IRGC threat makes delay increasingly dangerous.

---

## Sources

| Source | Type |
|--------|------|
| [@modgovae](https://x.com/modgovae/status/2032777505250357734) | UAE MOD update (March 14) |
| [Al Jazeera — Day 15 live](https://www.aljazeera.com/news/liveblog/2026/3/14/iran-war-live-pentagon-vows-to-ramp-up-us-military-campaign-against-iran) | Regional situation |
| [Al Jazeera — Day 15 explainer](https://www.aljazeera.com/news/2026/3/14/iran-war-what-is-happening-on-day-15-of-us-israel-attacks) | What happened today |
| [CNN — Iran war live](https://www.cnn.com/world/live-news/iran-war-us-israel-trump-03-14-26) | US/Kharg strikes |
| [CNBC — Oil above $100](https://www.cnbc.com/2026/03/13/oil-100-price-brent-wti-trump-iran-war-surrender-khamenei.html) | Oil prices |
| [Gulf News — UAE flights Mar 14](https://gulfnews.com/business/aviation/uae-flight-status-march-14-updated-schedules-destinations-and-travel-advisory-1.500474091) | Airport status |
| [Bloomberg — Kharg strikes](https://www.bloomberg.com/news/articles/2026-03-14/iran-repeats-retaliation-threat-as-us-hits-kharg-island-military) | Kharg analysis |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | 2026-03-14 |
