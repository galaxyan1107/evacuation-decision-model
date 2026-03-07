# Daily Update Pipeline

> 🌐 **EN** | [中文](../zh/pipeline/README.md)

Automated daily process for updating the Evacuation Decision Model with new data from UAE MOD (@modgovae) and other sources.

---

## Quick Start

```bash
# Process latest day (already in daily_data.json)
python pipeline/daily_update.py

# Add new day via CLI and process
python pipeline/daily_update.py --add \
    --day 9 --date 2026-03-08 \
    --bm 12 --bm-int 11 --bm-sea 1 \
    --drones 118 --drones-int 112 --drones-fell 6 \
    --deaths 0 --injuries 14 \
    --airport 60 --oil 99 --vlcc 430000 \
    --hormuz-status closed \
    --carriers 3 --carriers-eff 2.5 \
    --weapon-event "" \
    --events "12 BMs detected|Emirates 65% network" \
    --notes "Day 9 update"

# Add new day interactively
python pipeline/daily_update.py --add
```

---

## Pipeline Steps

The script runs 6 steps in sequence:

| Step | Action | Output |
|------|--------|--------|
| 1 | **Monte Carlo** (50K simulations) | λ median, P(λ>1), verdict, breaches |
| 2 | **Comparison Chart** (6 panels) | `charts/model_vs_actual_day{N}.png` |
| 3 | **Lambda Evolution Chart** | `charts/lambda_evolution_day{N}.png` |
| 4 | **English Update Page** | `updates/day{N}-{month}{day}.md` |
| 5 | **Chinese Update Page** | `zh/updates/day{N}-{month}{day}.md` |
| 6 | **SUMMARY.md** navigation update | Links to new pages |

---

## Data File

All historical data is stored in `pipeline/daily_data.json`.

### Adding a New Day

Each day entry requires these fields:

| Field | Type | Source | Example |
|-------|------|--------|---------|
| `bm_detected` | int | @modgovae | 16 |
| `bm_intercepted` | int | @modgovae | 15 |
| `bm_fell_sea` | int | @modgovae | 1 |
| `bm_fell_land` | int | @modgovae | 0 |
| `drones_detected` | int | @modgovae | 125 |
| `drones_intercepted` | int | @modgovae | 119 |
| `drones_fell_uae` | int | @modgovae | 6 |
| `cruise_missiles` | int | @modgovae | 0 |
| `deaths` | int | WAM/Reuters | 0 |
| `injuries` | int | WAM/Reuters | 19 |
| `airport_capacity_pct` | int | Gulf News | 55 |
| `oil_wti` | float | Bloomberg | 97.0 |
| `vlcc_rate` | int | Bloomberg | 424000 |
| `hormuz_status` | str | Maritime trackers | "closed" |
| `polymarket_ceasefire_mar31` | int | Polymarket | 61 |
| `carrier_count` | int | USNI News | 3 |
| `carrier_effective` | float | Model estimate | 2.3 |
| `new_weapon_event` | str/null | News | "Al Dhafra air base strike" |
| `realized_tail_risks` | object | Analysis | hormuz/proxy/air_base booleans |

---

## Model Parameters

### HAM Lambda Components

```
λ = 1.0 (base)
  + λ_launcher     = f(TEL depletion)        stabilizing (-)
  + λ_drone         = f(stockpile remaining)  destabilizing (+)
  + λ_intercept     = f(cumulative rate)      destabilizing (+)
  + λ_hormuz        = f(strait status)        destabilizing (+)
  + λ_proxy         = f(proxy activation)     destabilizing (+)
  + λ_weapon        = f(new escalation)       destabilizing (+)
  + λ_bm_rebound    = f(BM trajectory)        destabilizing (+)
  + λ_naval         = f(carrier count)        stabilizing (-)
```

### Cascade Thresholds

| Metric | Threshold | Breach = |
|--------|-----------|----------|
| Launcher Depletion | > 85% | BREACH |
| Drone Stockpile | < 30% remaining | BREACH |
| Interception Rate | < 90% cumulative | BREACH |
| Daily Casualties | > 10 | BREACH |
| New Weapon/Target | any | BREACH |

**Verdict Rule:** ≥3 breaches = UNSTABLE, ≥1 = METASTABLE, 0 = STABLE

---

## Run Log

Every pipeline run is logged to `pipeline/run_log.json` with timestamp, day number, λ median, verdict, and breach count. Use this to track model evolution over time.

---

## Dependencies

```
numpy
matplotlib
```

Install: `pip install numpy matplotlib`
