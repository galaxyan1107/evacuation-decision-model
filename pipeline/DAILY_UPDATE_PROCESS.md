# Daily Update Process — Claude Operator Guide

> This document is the **single source of truth** for performing a daily GitBook update.
> Follow every step in order. Do not skip steps.

---

## Overview

Each day, update the evacuation model with new data from @modgovae and regenerate all outputs. The process has **5 phases**:

1. **Data Collection** — Search web for today's numbers
2. **Data Entry** — Add new day to `pipeline/daily_data.json`
3. **Pipeline Execution** — Run `daily_update.py` to generate day page + 2 charts
4. **Tracker Charts** — Run `regen_tracker_charts.py` to regenerate all 4 tracker charts
5. **Manual Enrichment** — Add change analysis, defense costs, sources to EN/ZH pages + update daily tracker

---

## Phase 1: Data Collection

### Required Data Points

Search the web for ALL of the following. Primary source: **@modgovae** on X (Twitter).

| Field | Source | Search Query |
|-------|--------|--------------|
| `bm_detected` | @modgovae | `modgovae [DATE] ballistic missiles detected` |
| `bm_intercepted` | @modgovae | (same tweet, "intercepted and destroyed") |
| `bm_fell_sea` | @modgovae | (same tweet, "fell into the sea") |
| `bm_fell_land` | @modgovae | (same tweet, "fell within the country") |
| `drones_detected` | @modgovae | (same tweet) |
| `drones_intercepted` | @modgovae | (same tweet) |
| `drones_fell_uae` | Derived: detected - intercepted |
| `cruise_missiles` | @modgovae | Usually 0 after Day 3 |
| `deaths` | WAM, Gulf News, The National | `UAE casualties deaths [DATE]` |
| `injuries` | WAM, Gulf News, The National | `UAE injuries debris [DATE]` |
| `airport_capacity_pct` | Gulf News, Emirates press | `Emirates flights capacity [DATE]` |
| `oil_wti` | CNBC, Bloomberg | `WTI oil price [DATE]` |
| `vlcc_rate` | Bloomberg, shipping news | `VLCC tanker rate [DATE]` |
| `hormuz_status` | Maritime trackers | `Strait of Hormuz [DATE] status` |
| `hormuz_crossings` | Maritime trackers | 0 if closed |
| `polymarket_ceasefire_mar31` | Polymarket, news | `Polymarket ceasefire Iran [DATE]` |
| `carrier_count` | USNI News | `US carrier strike group [DATE]` |
| `carrier_effective` | Model estimate | Based on readiness (0.8 per deployed CSG) |
| `new_weapon_event` | News | Any new escalation type (null if none) |
| `key_events` | All sources | 3-5 most significant events of the day |
| `realized_tail_risks` | Analysis | Update hormuz_closed, proxy_activated, air_base_strike booleans |

### Search Strategy

Run these web searches in parallel:

```
1. "UAE MOD @modgovae [month] [day] 2026 ballistic missiles drones intercepted"
2. "modgovae [DATE] missiles drones detected intercepted"
3. "UAE defense [DATE] casualties injuries debris airport"
4. "Polymarket ceasefire Iran [DATE] oil price WTI Brent"
```

### Cross-Validation

- **Cumulative check**: Verify today's cumulative BM total = yesterday's cum + today's daily
- **Interception rate**: Should be ~92-93% cumulative; flag if daily rate < 90%
- **Drone stockpile**: Compute (2000 - cum_drones_detected) / 2000 × 100

---

## Phase 2: Data Entry

### Add new day to `pipeline/daily_data.json`

Open the file and append a new entry to the `"days"` array. Use the Edit tool to insert before the closing `]`:

```json
{
  "day": N,
  "date": "2026-MM-DD",
  "bm_detected": X,
  "bm_intercepted": X,
  "bm_fell_sea": X,
  "bm_fell_land": X,
  "drones_detected": X,
  "drones_intercepted": X,
  "drones_fell_uae": X,
  "cruise_missiles": X,
  "deaths": X,
  "injuries": X,
  "airport_capacity_pct": X,
  "oil_wti": X,
  "vlcc_rate": X,
  "hormuz_status": "open|closed",
  "hormuz_crossings": X,
  "proxy_active": true|false,
  "new_weapon_event": "description"|null,
  "polymarket_ceasefire_mar31": X|null,
  "carrier_count": X,
  "carrier_effective": X.X,
  "key_events": [
    "Event 1",
    "Event 2"
  ],
  "realized_tail_risks": {
    "hormuz_closed": true|false,
    "proxy_activated": true|false,
    "air_base_strike": true|false
  },
  "notes": "Brief summary"
}
```

### Day Number Convention

- Day 1 = Feb 28, 2026 (conflict start)
- Day N = Feb 28 + (N-1) days
- Verify: `day 10 = March 9`, `day 11 = March 10`, etc.

---

## Phase 3: Pipeline Execution

### Prerequisites

```bash
pip install matplotlib numpy --break-system-packages -q
```

### Run the pipeline

```bash
cd /sessions/great-lucid-cori/mnt/flea/gitbook-evacuation-model/pipeline
python daily_update.py --day N
```

This generates:
- `charts/model_vs_actual_dayN.png` (6-panel comparison)
- `charts/lambda_evolution_dayN.png` (λ time series)
- `updates/dayN-monthDD.md` (English day page — **skeleton only**)
- `zh/updates/dayN-monthDD.md` (Chinese day page — **skeleton only**)
- Updates `SUMMARY.md` navigation
- Appends to `pipeline/run_log.json`

### Verify pipeline output

Check the printed output for:
- λ median value
- P(λ>1) percentage
- Verdict (STABLE/METASTABLE/UNSTABLE)
- Breach count and list

---

## Phase 4: Tracker Charts Regeneration

**CRITICAL: The pipeline only generates 2 charts. The daily tracker references 4 additional charts that must be regenerated separately.**

### Run tracker chart regeneration

```bash
python /sessions/great-lucid-cori/regen_tracker_charts.py
```

Or if that script doesn't exist, create it. It must regenerate these 4 charts with ALL days' data:

| Chart | File | Description |
|-------|------|-------------|
| Divergence Heatmap | `charts/divergence_heatmap.png` | Day-by-day % deviation across 6 metrics |
| Model vs Actual Bars | `charts/model_vs_actual_bars.png` | 6-panel bar comparison |
| Divergence Scorecard | `charts/divergence_scorecard.png` | Stacked divergence + verdict timeline |
| BM Trajectory | `charts/bm_trajectory.png` | Daily + cumulative BM vs model decay |

### Verify all 6 charts

Read each PNG to visually confirm Day N appears:

```
charts/model_vs_actual_dayN.png    ← from pipeline
charts/lambda_evolution_dayN.png   ← from pipeline
charts/divergence_heatmap.png      ← from tracker regen
charts/model_vs_actual_bars.png    ← from tracker regen
charts/divergence_scorecard.png    ← from tracker regen
charts/bm_trajectory.png           ← from tracker regen
```

---

## Phase 5: Manual Enrichment

The pipeline generates skeleton pages. Enrich them with analysis.

### 5A. English Day Page (`updates/dayN-monthDD.md`)

Add these sections between "Key Events" and "Charts":

#### Day N-1 → Day N Change Analysis

```markdown
## What Changed Day N-1 → Day N

\```
Day N-1 → Day N Lambda Decomposition:

Component          Day N-1          Day N               Change
─────────────────────────────────────────────────────────────────
λ_launcher         X.XXX            X.XXX               X.XXX
λ_drone            X.XXX            X.XXX               X.XXX
λ_intercept        X.XXX            X.XXX               X.XXX
λ_proxy            X.XXX            X.XXX               X.XXX
λ_hormuz           X.XXX            X.XXX               X.XXX
λ_weapon           X.XXX            X.XXX               X.XXX
λ_bm_rebound       X.XXX            X.XXX               X.XXX
λ_naval            X.XXX            X.XXX               X.XXX
─────────────────────────────────────────────────────────────────
λ total (median)    X.XXX            X.XXX               X.XXX
\```

Key drivers of the Day N change:
1. **Driver 1** (±X.XXX): Explanation
2. **Driver 2** (±X.XXX): Explanation
3. **Driver 3** (±X.XXX): Explanation
```

To compute previous day's decomposition, look at the previous day's page or run the pipeline for day N-1 to get its decomposition values.

#### Defense Cost Update

Add after the recommendation section:

```markdown
## Defense Cost Update

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | X | THAAD @ $12.7M | X | X |
| BM (PAC-3, 40%) | X | PAC-3 @ $3.9M | X | X |
| Cruise Missiles | X | PAC-3 @ $3.9M | X | X |
| Drones | X | SHORAD @ $0.7M | X | X |
| **TOTAL** | **X** | | **$X** | **$X** |
```

**Formulas:**
- BM THAAD count = cum_bm_intercepted × 0.6
- BM PAC-3 count = cum_bm_intercepted × 0.4
- THAAD cost = count × $12.7M
- PAC-3 cost = count × $3.9M
- Drone cost = cum_drones_intercepted × $0.7M
- Oil loss = 1.7M bbl/d × days_hormuz_closed × WTI_price (for stranded)
- Production cuts = 0.5M bbl/d × days_hormuz_closed × WTI_price

#### Enhanced Recommendation

Replace the generic recommendation with a specific one referencing:
- Current λ value and trend direction
- Which structural destabilizers persist
- Drone stockpile days remaining
- Ceasefire odds
- Airport window viability

#### Sources Table

Replace generic sources with actual URLs from web searches:

```markdown
## Sources

| Source | Type |
|--------|------|
| [@modgovae](https://x.com/modgovae) | UAE MOD daily update (Month Day) |
| [Gulf News](URL) | Specific article |
| [CNBC](URL) | Oil price article |
| [Polymarket](URL) | Ceasefire odds |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | YYYY-MM-DD |
```

### 5B. Chinese Day Page (`zh/updates/dayN-monthDD.md`)

Mirror all enrichments from the English page:
- Translate key_events to Chinese
- Add 第N-1天→第N天变化分析 section (same decomposition table with Chinese labels)
- Add 防御成本更新 section
- Enhanced 建议 section
- Real source URLs with Chinese descriptions

**Chinese label map for lambda components:**
```
λ_launcher    → λ_发射装置
λ_drone       → λ_无人机
λ_intercept   → λ_拦截
λ_hormuz      → λ_霍尔木兹
λ_proxy       → λ_代理人
λ_weapon      → λ_武器
λ_bm_rebound  → λ_弹道反弹
λ_naval       → λ_海军威慑
```

### 5C. Daily Tracker (`updates/daily-tracker.md`)

Update **ALL** of the following sections with Day N data:

| Section | What to Update |
|---------|---------------|
| Header | `Last Updated: [Date] (Day N)` |
| Lambda Evolution text | Add Day N λ value and trend note |
| BM Trajectory text | Note if rebound continues/breaks |
| **Attack Volume — Daily** | Add Day N row |
| **Attack Volume — Cumulative** | Add Day N row |
| **Interception Rate** | Add Day N row + notes |
| **Drone Stockpile** | Add Day N row + update exhaustion estimate |
| **Cascade Thresholds** | Add Day N column |
| **Breaches/Verdict** | Add Day N row |
| **Lambda Evolution table** | Add Day N row |
| **Polymarket** | Add Day N row + trend note |
| **Airport & Flight** | Add Day N row |
| **Casualty Tracker** | Add Day N row |
| **Economic Impact** | Add Day N row |
| **Key Events Timeline** | Add Day N events (3-5 rows) |
| **Scorecard** | Update Day N-1 → Day N comparison |
| **Recommendation History** | Add Day N row + analysis |

### 5D. Chinese Tracker (`zh/updates/daily-tracker.md`)

Update at minimum:
- Header date
- (Ideally mirror all English tracker changes, but at minimum update the date)

### 5E. Fix SUMMARY.md Ordering

The pipeline appends new entries at the end. Verify that Day N appears **before** Day N-1 in both EN and ZH sections:

```markdown
## Daily Updates
* [📊 Day-by-Day Tracker](updates/daily-tracker.md)
* [Day N — Month DD ⚠️ UNSTABLE](updates/dayN-monthDD.md)      ← newest first
* [Day N-1 — Month DD ⚠️ UNSTABLE](updates/dayN-1-monthDD.md)
```

---

## Checklist

Before declaring "done", verify:

- [ ] `pipeline/daily_data.json` has Day N entry with all fields
- [ ] `charts/model_vs_actual_dayN.png` exists and shows Day N
- [ ] `charts/lambda_evolution_dayN.png` exists and shows Day N
- [ ] `charts/divergence_heatmap.png` includes Day N column
- [ ] `charts/model_vs_actual_bars.png` includes Day N bars
- [ ] `charts/divergence_scorecard.png` includes Day N
- [ ] `charts/bm_trajectory.png` includes Day N
- [ ] `updates/dayN-monthDD.md` has change analysis + defense costs + real sources
- [ ] `zh/updates/dayN-monthDD.md` has Chinese translations of all enrichments
- [ ] `updates/daily-tracker.md` has Day N in ALL tables (15+ tables/sections)
- [ ] `zh/updates/daily-tracker.md` header date updated
- [ ] `SUMMARY.md` has Day N links in correct order (newest first) for both EN and ZH

---

## Key Formulas Reference

### Lambda Decomposition (from pipeline code)

```python
λ_launcher    = -0.55 × launcher_depletion
λ_drone       = 0.50 × (1 - drone_remaining_pct/100) × 0.4   # only if remaining < 50%
λ_intercept   = 0.30 × max(0, 0.93 - cum_intercept_rate) × 1.0
λ_hormuz      = 0.63 if hormuz_closed else 0.0
λ_proxy       = 0.50 if proxy_activated else 0.0
λ_weapon      = 0.40 if air_base_strike else 0.0
λ_bm_rebound  = 0.30 if last-4-days BMs monotonically increasing and latest ≥ 10
λ_naval       = -0.08 × carrier_effective
```

### Launcher Depletion

```python
tels_used = cum_bm_detected / 6.0
depletion = min(tels_used / 40, 0.99)
# If last 4 days BMs monotonically increasing with latest > 10: cap at 0.75
```

### Drone Stockpile

```python
remaining = 2000 - cum_drones_detected
pct = remaining / 2000 × 100
```

### BM Rebound Signal

```python
# Active if last 4 days of BM detections are monotonically increasing AND latest ≥ 10
recent_bm = [bm_detected for last 4 days]
bm_rebound = all(recent_bm[i] <= recent_bm[i+1]) and recent_bm[-1] >= 10
```

### Defense Cost

```python
# BM interception (60% THAAD @ $12.7M, 40% PAC-3 @ $3.9M)
thaad_cost = cum_bm_intercepted × 0.6 × 12.7  # $M
pac3_bm_cost = cum_bm_intercepted × 0.4 × 3.9  # $M

# Cruise missile interception (PAC-3 @ $3.9M)
pac3_cm_cost = cum_cruise_intercepted × 3.9  # $M

# Drone interception (SHORAD @ $0.7M)
shorad_cost = cum_drones_intercepted × 0.7  # $M

# Oil revenue loss
stranded_oil = 1.7 × days_hormuz_closed × wti_price  # $M
production_cuts = 0.5 × days_hormuz_closed × wti_price  # $M
```

---

## Tracker Chart Regeneration Script

If `/sessions/great-lucid-cori/regen_tracker_charts.py` doesn't exist, create it with the code that was used for the Day 10 update. It reads `pipeline/daily_data.json`, computes all series (BM actual/model, drones, intercept rate, drone stockpile, airport, lambda for each day), and generates:

1. **divergence_heatmap.png** — `imshow` heatmap of % divergence, 6 metrics × N days
2. **model_vs_actual_bars.png** — 6-panel bar chart, model (blue) vs actual (red)
3. **divergence_scorecard.png** — Top: stacked absolute divergence. Bottom: verdict timeline bars
4. **bm_trajectory.png** — Top: daily BMs with model decay curve. Bottom: cumulative BMs with TEL capacity lines

---

## Timing

Typical session: ~15-20 minutes total
- Phase 1 (data collection): 3-5 min
- Phase 2 (data entry): 1 min
- Phase 3 (pipeline): 2 min
- Phase 4 (tracker charts): 1 min
- Phase 5 (enrichment): 8-12 min
