# Daily Update Process — Claude Operator Guide

> This document is the **single source of truth** for performing a daily GitBook update.
> Follow every step in order. Do not skip steps.
> Last revised: Day 11 (March 10, 2026)

---

## Overview

Each day, update the evacuation model with new data from @modgovae and regenerate all outputs. The process has **5 phases**:

1. **Data Collection** — Search web for today's numbers
2. **Data Entry** — Add new day to `pipeline/daily_data.json`
3. **Pipeline Execution** — Run `daily_update.py` to generate day page + 2 charts
4. **Tracker Charts** — Update `regen_tracker_charts.py` with new lambda values, then run it to regenerate all 5 tracker charts (including the corrected lambda evolution chart that overwrites the pipeline's version)
5. **Manual Enrichment** — Add change analysis, defense costs, sources to EN/ZH pages + update daily tracker (ALL 16+ tables/sections)

### Files Modified Per Day

| File | Modified By |
|------|------------|
| `pipeline/daily_data.json` | Phase 2 (manual) |
| `charts/model_vs_actual_dayN.png` | Phase 3 (pipeline) |
| `charts/lambda_evolution_dayN.png` | Phase 3 (pipeline) → **overwritten by Phase 4 (regen)** with official values |
| `charts/divergence_heatmap.png` | Phase 4 (regen) |
| `charts/model_vs_actual_lines.png` | Phase 4 (regen) — **line plot, not bars** |
| `charts/divergence_scorecard.png` | Phase 4 (regen) |
| `charts/bm_trajectory.png` | Phase 4 (regen) |
| `updates/dayN-monthDD.md` | Phase 3 (skeleton) → Phase 5A (enriched) |
| `zh/updates/dayN-monthDD.md` | Phase 3 (skeleton) → Phase 5B (enriched) |
| `updates/daily-tracker.md` | Phase 5C (16+ tables) |
| `zh/updates/daily-tracker.md` | Phase 5D (ALL 21 sections — full Chinese mirror of English tracker) |
| `SUMMARY.md` | Phase 3 (pipeline) → Phase 5E (fix ordering) |
| `regen_tracker_charts.py` | Phase 4 (update LAMBDA_OFFICIAL + P_LAMBDA_GT1 dicts) |

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
1. "Iran UAE attack [month] [day] 2026 missiles drones latest"
2. "UAE air defences intercept [month] [day] 2026 ballistic missiles drones"
3. "WTI oil price [month] [day] 2026 crude today"
4. "UAE Strait of Hormuz [month] [day] 2026 shipping tanker"
```

### Cross-Validation

- **Cumulative check**: Verify today's cumulative BM total = yesterday's cum + today's daily
- **Interception rate**: Should be ~92-93% cumulative; flag if daily rate < 90%
- **Drone stockpile**: Compute (2000 - cum_drones_detected) / 2000 × 100
- **Casualty cumulative**: Verify cum deaths + today's deaths = new cum total (check against Gulf News cumulative figures)

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
- Verify: `day 10 = March 9`, `day 11 = March 10`, `day 12 = March 11`, etc.

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
- `charts/lambda_evolution_dayN.png` (λ time series — **will be overwritten in Phase 4 with official values**)
- `updates/dayN-monthDD.md` (English day page — **skeleton only**)
- `zh/updates/dayN-monthDD.md` (Chinese day page — **skeleton only**)
- Updates `SUMMARY.md` navigation
- Appends to `pipeline/run_log.json`

### Record pipeline output

Note down from the printed output:
- **λ median value** — needed for Phase 4 (LAMBDA_OFFICIAL dict)
- **P(λ>1) percentage** — needed for Phase 4 (P_LAMBDA_GT1 dict)
- **Verdict** (STABLE/METASTABLE/UNSTABLE)
- **Breach count and list**

---

## Phase 4: Tracker Charts Regeneration

**CRITICAL: The pipeline generates 2 charts. The tracker needs 5 additional charts regenerated by a separate script. The regen script also overwrites the pipeline's lambda chart with one using correct official values.**

### Step 4A: Update `regen_tracker_charts.py` with new lambda values

Before running the script, update the two dicts at the top of the file:

```python
LAMBDA_OFFICIAL = {
    1:  0.750,
    2:  0.470,
    3:  1.703,
    4:  1.677,
    5:  1.669,
    6:  1.754,
    7:  0.496,
    8:  2.589,
    9:  2.712,
    10: 2.061,
    11: 2.081,
    N:  X.XXX,   # ← ADD NEW DAY'S VALUE FROM PIPELINE OUTPUT
}

P_LAMBDA_GT1 = {
    1:  5.5,
    2:  5.4,
    3:  99.9,
    4:  99.7,
    5:  99.7,
    6:  100.0,
    7:  5.8,
    8:  100.0,
    9:  100.0,
    10: 100.0,
    11: 100.0,
    N:  XXX.X,   # ← ADD NEW DAY'S P(λ>1) FROM PIPELINE OUTPUT
}
```

**Why this matters:** The pipeline re-runs Monte Carlo each time it generates the lambda chart, producing slightly different values each run. The regen script uses the stored official values so ALL charts show consistent, matching lambda numbers.

### Step 4B: Run the regen script

```bash
cd /sessions/great-lucid-cori/mnt/flea/gitbook-evacuation-model
python /sessions/great-lucid-cori/regen_tracker_charts.py
```

This generates **5 charts**:

| # | Chart | File | Type |
|---|-------|------|------|
| 1 | Divergence Heatmap | `charts/divergence_heatmap.png` | Heatmap of % deviation across 6 metrics |
| 2 | 6-Panel Comparison | `charts/model_vs_actual_lines.png` | **Line plot** — model (blue dashed) vs actual (red solid) with shaded divergence fill |
| 3 | Divergence Scorecard | `charts/divergence_scorecard.png` | Stacked divergence + verdict timeline |
| 4 | BM Trajectory | `charts/bm_trajectory.png` | Daily + cumulative BMs vs model decay |
| 5 | Lambda Evolution | `charts/lambda_evolution_dayN.png` | **Overwrites pipeline version** with official stored values |

### Step 4C: Verify all 7 charts (2 pipeline + 5 regen)

```
charts/model_vs_actual_dayN.png    ← pipeline (6-panel day comparison)
charts/lambda_evolution_dayN.png   ← regen OVERWRITES pipeline version (official λ values)
charts/divergence_heatmap.png      ← regen
charts/model_vs_actual_lines.png    ← regen (LINE PLOT, not bars)
charts/divergence_scorecard.png    ← regen
charts/bm_trajectory.png           ← regen
```

Visually verify at least 2 charts to confirm Day N data appears.

---

## Phase 5: Manual Enrichment

The pipeline generates skeleton pages. Enrich them with analysis.

### 5A. English Day Page (`updates/dayN-monthDD.md`)

Add these sections between "Lambda Recalculation" and "Charts":

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

To get the previous day's decomposition, read the previous day's page file (`updates/dayN-1-monthDD.md`).

#### Defense Cost Update

Add after Charts section:

```markdown
## Defense Cost Update

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | X | THAAD @ $12.7M | X | X |
| BM (PAC-3, 40%) | X | PAC-3 @ $3.9M | X | X |
| Cruise Missiles | X | PAC-3 @ $3.9M | X | X |
| Drones | X | SHORAD @ $0.7M | X | X |
| **TOTAL** | **X** | | **$X** | **$X** |

### Oil Revenue Not Sold (Cumulative, X days Hormuz closure)

| Component | Volume | Revenue Loss |
|-----------|--------|-------------|
| Stranded oil (no Hormuz) | 1.7M bbl/d × X days × $WTI | **$XM** |
| Voluntary production cuts | 0.5M bbl/d × X days × $WTI | **$XM** |
| **TOTAL OIL LOSS** | | **$XM ($X.XB)** |

### Grand Total Cost to UAE (Day N)

| Scenario | Defense | Oil Loss | **Grand Total** |
|----------|---------|----------|----------------|
| 1:1 | $X.XXB | $X.XXB | **$X.XXB** |
| 1:2 | $X.XXB | $X.XXB | **$X.XXB** |
| 1:3 | $X.XXB | $X.XXB | **$X.XXB** |
```

#### Enhanced Recommendation

Replace the generic recommendation with a specific one referencing:
- Current λ value and trend direction
- Which structural destabilizers persist
- Drone stockpile days remaining (at current burn rate AND at pre-collapse rate)
- Ceasefire odds and trend
- Airport window viability and which carriers are suspended

#### Sources Table

Replace generic sources with actual URLs from web searches:

```markdown
## Sources

| Source | Type |
|--------|------|
| [@modgovae](https://x.com/modgovae) | UAE MOD daily update (Month Day) |
| [Gulf News — headline](URL) | Specific article |
| [CNBC — headline](URL) | Oil price article |
| [Polymarket](URL) | Ceasefire odds |
| [USNI Fleet Tracker](URL) | Naval disposition |
| Model pipeline | ABC + HAM (50K MC) |
| Generated | YYYY-MM-DD |
```

### 5B. Chinese Day Page (`zh/updates/dayN-monthDD.md`)

Mirror all enrichments from the English page:
- Translate key_events to Chinese
- Add 第N-1天→第N天变化分析 section (same decomposition table with Chinese labels)
- Add 防御成本更新 section (with Chinese headers)
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

**⚠️ THIS IS THE LARGEST AND MOST ERROR-PRONE STEP. Update ALL 16+ sections:**

| # | Section | What to Update |
|---|---------|---------------|
| 1 | **Header** | `Last Updated: [Date] (Day N)` |
| 2 | **Divergence Heatmap text** | Mention Day N if notable |
| 3 | **Scorecard text** | Update "all N days" count |
| 4 | **Lambda Evolution text** | Add Day N λ value and trend note |
| 5 | **BM Trajectory text** | Note if rebound continues/breaks, drone trends |
| 6 | **Attack Volume — Daily** | Add Day N row |
| 7 | **Attack Volume — Cumulative** | Add Day N row |
| 8 | **Interception Rate** | Add Day N row + notes if daily rate < 90% |
| 9 | **Drone Stockpile** | Add Day N row + update exhaustion estimates |
| 10 | **Cascade Thresholds** | Add Day N column (including daily interception row) |
| 11 | **Breaches/Verdict** | Add Day N row |
| 12 | **Lambda Evolution table** | Add Day N row |
| 13 | **Scenario Probability** | Update "Day N Assessment" column header + all 4 scenario rows |
| 14 | **Polymarket** | Add Day N row + trend note |
| 15 | **Airport & Flight** | Add Day N row + update positive divergence note |
| 16 | **Casualty Tracker** | Add Day N row + notes if notable |
| 17 | **Economic Impact** | Add Day N row |
| 18 | **Key Events Timeline** | Add Day N events (3-5 rows) |
| 19 | **Scorecard** | Update to "Day N-1 Observed" vs "Day N Observed" columns + rating |
| 20 | **Recommendation History** | Add Day N row + full analysis paragraph |

**Common mistakes to avoid:**
- Forgetting to update the **Scenario Probability Tracker** (header says "Day X Assessment" — must update to current day)
- Leaving previous day rows in **bold** — only current day should be bold
- Not updating the **lambda_evolution_dayN.png** reference in the Lambda Evolution section
- Missing the chart description text updates (items 2-5 above)

### 5D. Chinese Tracker (`zh/updates/daily-tracker.md`)

**⚠️ FULL UPDATE REQUIRED — not just header. Mirror ALL 20 sections from Phase 5C in Chinese.**

| # | Section (Chinese) | What to Update |
|---|-------------------|---------------|
| 1 | **Header** | `最后更新：2026年M月D日（第N天）` |
| 2 | **偏离热力图 text** | Mention Day N if notable |
| 3 | **6面板对比 text** | Update description, verify chart ref = `model_vs_actual_lines.png` |
| 4 | **记分卡 text** | Update "全N天" count |
| 5 | **Lambda演变 text** | Add Day N λ value + trend, update chart ref = `lambda_evolution_dayN.png` |
| 6 | **弹道导弹轨迹 text** | Note if rebound continues/breaks, drone trends |
| 7 | **每日新增攻击** | Add Day N row |
| 8 | **累计总量** | Add Day N row |
| 9 | **拦截率追踪** | Add Day N row + notes if daily rate < 90% |
| 10 | **无人机库存追踪** | Add Day N row + update exhaustion estimates |
| 11 | **级联阈值追踪** | Add Day N column (including daily interception row) |
| 12 | **突破/判定** | Add Day N row |
| 13 | **Lambda演变 table** | Add Day N row |
| 14 | **情景概率** | Update "第N天评估" column header + all 4 scenario rows |
| 15 | **Polymarket** | Add Day N row + trend note |
| 16 | **机场与航班** | Add Day N row + update divergence note |
| 17 | **伤亡追踪** | Add Day N row + notes if notable |
| 18 | **经济影响** | Add Day N row |
| 19 | **关键事件时间线** | Add Day N events (3-5 rows) |
| 20 | **模型vs现实记分卡** | Update to "第N-1天观测" vs "第N天观测" columns + rating |
| 21 | **建议历史** | Add Day N row + full analysis paragraph |

**The Chinese tracker must contain identical data to the English tracker, just translated.**

### 5E. Fix SUMMARY.md Ordering

The pipeline appends new entries at the end. Edit to ensure Day N appears **before** Day N-1 in both EN and ZH sections:

```markdown
## Daily Updates
* [📊 Day-by-Day Tracker](updates/daily-tracker.md)
* [Day N — Month DD ⚠️ UNSTABLE](updates/dayN-monthDD.md)      ← newest first
* [Day N-1 — Month DD ⚠️ UNSTABLE](updates/dayN-1-monthDD.md)
```

---

## Final Verification Checklist

Before declaring "done", verify every item:

- [ ] `pipeline/daily_data.json` has Day N entry with all fields
- [ ] `regen_tracker_charts.py` LAMBDA_OFFICIAL dict has Day N entry
- [ ] `regen_tracker_charts.py` P_LAMBDA_GT1 dict has Day N entry
- [ ] `charts/model_vs_actual_dayN.png` exists and shows Day N (pipeline)
- [ ] `charts/lambda_evolution_dayN.png` shows official λ values matching tracker table (regen)
- [ ] `charts/divergence_heatmap.png` includes Day N column (regen)
- [ ] `charts/model_vs_actual_lines.png` is a LINE PLOT with Day N (regen)
- [ ] `charts/divergence_scorecard.png` includes Day N (regen)
- [ ] `charts/bm_trajectory.png` includes Day N (regen)
- [ ] `updates/dayN-monthDD.md` has: change analysis + defense costs + oil loss + grand total + enhanced recommendation + real source URLs
- [ ] `zh/updates/dayN-monthDD.md` has: Chinese translations of ALL enrichments
- [ ] `updates/daily-tracker.md` has Day N in ALL 20 sections listed in 5C
- [ ] `updates/daily-tracker.md` Scenario Probability table says "Day N Assessment" (not older day)
- [ ] `updates/daily-tracker.md` only current day rows are **bold**
- [ ] `zh/updates/daily-tracker.md` has Day N in ALL 21 sections listed in 5D (not just header)
- [ ] `zh/updates/daily-tracker.md` chart references updated (`model_vs_actual_lines.png`, `lambda_evolution_dayN.png`)
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

# Oil revenue loss (Hormuz closed since Day 3 = March 2)
days_hormuz_closed = current_day - 2   # Day 3 onward
stranded_oil = 1.7 × days_hormuz_closed × wti_price  # $M
production_cuts = 0.5 × days_hormuz_closed × wti_price  # $M
```

### Hormuz Closure Days

```python
# Hormuz closed since Day 3 (March 2, 2026)
# Days 3,4,5,...,N = (N - 2) days of closure
days_hormuz_closed = current_day_number - 2
```

---

## Tracker Chart Script Architecture

The regen script (`/sessions/great-lucid-cori/regen_tracker_charts.py`) has this structure:

1. **Imports + config** — reads `daily_data.json`, sets chart output dir
2. **LAMBDA_OFFICIAL dict** — canonical λ values from each day's pipeline run (UPDATE DAILY)
3. **P_LAMBDA_GT1 dict** — canonical P(λ>1) values (UPDATE DAILY)
4. **Helper functions** — `cum_up_to()`, `get_lambda()`
5. **Series computation** — BM actual/model, drone actual/model, intercept, stockpile, airport, lambda
6. **Divergence computation** — % divergence for all 6 metrics
7. **Chart 1: Divergence Heatmap** — `imshow` heatmap, 6 metrics × N days
8. **Chart 2: 6-Panel Comparison** — LINE PLOT (not bars), model vs actual with shaded fill
9. **Chart 3: Divergence Scorecard** — stacked divergence + verdict timeline
10. **Chart 4: BM Trajectory** — daily BMs with model decay + cumulative with TEL lines
11. **Chart 5: Lambda Evolution** — official λ values + P(λ>1) bar chart — **overwrites pipeline version**

**Key design decisions:**
- Uses `LAMBDA_OFFICIAL` dict instead of recomputing MC → consistent values across all charts and tracker table
- Chart 2 is a LINE PLOT (changed from bars on Day 11) for better trend visibility
- Chart 5 overwrites the pipeline's `lambda_evolution_dayN.png` with official values
- All charts use matching visual style (red = actual/divergent, blue = model, green = airport positive)

---

## Timing

Typical session: ~15-20 minutes total
- Phase 1 (data collection): 3-5 min (web searches in parallel)
- Phase 2 (data entry): 1 min
- Phase 3 (pipeline): 2 min
- Phase 4 (update regen script + run): 2 min
- Phase 5 (enrichment — ALL 20 tracker sections + EN/ZH pages): 8-12 min
