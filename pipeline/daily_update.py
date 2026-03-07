#!/usr/bin/env python3
"""
Evacuation Decision Model — Daily Update Pipeline
===================================================
Usage:
  python daily_update.py                        # Process latest day in daily_data.json
  python daily_update.py --day 9                # Process specific day
  python daily_update.py --add                  # Interactive: add new day entry then process
  python daily_update.py --add --day 9 \
      --date 2026-03-08 --bm 12 --bm-int 11 \
      --drones 130 --drones-int 122 ...         # CLI add + process

Outputs:
  1. charts/model_vs_actual_day{N}.png          — 6-panel comparison chart
  2. charts/lambda_evolution_day{N}.png         — Lambda time series
  3. updates/day{N}-{month}{day}.md             — English daily update page
  4. zh/updates/day{N}-{month}{day}.md          — Chinese daily update page
  5. updates/daily-tracker.md                   — Updated tracker (EN)
  6. zh/updates/daily-tracker.md                — Updated tracker (ZH)
  7. SUMMARY.md                                 — Updated navigation
  8. pipeline/daily_data.json                   — Appended (if --add)
  9. pipeline/run_log.json                      — Append run metadata
"""

import json, os, sys, argparse, datetime
from pathlib import Path
import numpy as np

# ── Paths ─────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent
GITBOOK_DIR = SCRIPT_DIR.parent
DATA_FILE   = SCRIPT_DIR / "daily_data.json"
RUN_LOG     = SCRIPT_DIR / "run_log.json"
CHARTS_DIR  = GITBOOK_DIR / "charts"
UPDATES_DIR = GITBOOK_DIR / "updates"
ZH_UPDATES  = GITBOOK_DIR / "zh" / "updates"
SUMMARY_F   = GITBOOK_DIR / "SUMMARY.md"

CHARTS_DIR.mkdir(exist_ok=True)
UPDATES_DIR.mkdir(exist_ok=True)
ZH_UPDATES.mkdir(parents=True, exist_ok=True)

# ── Load Data ─────────────────────────────────────────────────────
def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Cumulative calculations ───────────────────────────────────────
def compute_cumulative(days_list, up_to_day):
    """Compute cumulative stats up to and including given day number."""
    subset = [d for d in days_list if d["day"] <= up_to_day]
    cum = {
        "bm_detected":      sum(d["bm_detected"] for d in subset),
        "bm_intercepted":   sum(d["bm_intercepted"] for d in subset),
        "bm_fell_sea":      sum(d.get("bm_fell_sea", 0) for d in subset),
        "bm_fell_land":     sum(d.get("bm_fell_land", 0) for d in subset),
        "drones_detected":  sum(d["drones_detected"] for d in subset),
        "drones_intercepted": sum(d["drones_intercepted"] for d in subset),
        "drones_fell_uae":  sum(d.get("drones_fell_uae", 0) for d in subset),
        "cruise_missiles":  sum(d.get("cruise_missiles", 0) for d in subset),
        "deaths":           sum(d.get("deaths", 0) for d in subset),
        "injuries":         sum(d.get("injuries", 0) for d in subset),
    }
    cum["bm_intercept_rate"] = (cum["bm_intercepted"] / cum["bm_detected"] * 100) if cum["bm_detected"] > 0 else 0
    cum["drone_intercept_rate"] = (cum["drones_intercepted"] / cum["drones_detected"] * 100) if cum["drones_detected"] > 0 else 0
    return cum

def compute_drone_stockpile(data, up_to_day):
    total_est = data["metadata"]["drone_stockpile_estimate"]
    cum = compute_cumulative(data["days"], up_to_day)
    remaining = total_est - cum["drones_detected"]
    return remaining, remaining / total_est * 100

def compute_launcher_depletion(data, up_to_day):
    """Estimate TEL depletion based on BM trajectory."""
    tel_est = data["metadata"]["tel_stockpile_estimate"]
    days_data = [d for d in data["days"] if d["day"] <= up_to_day]
    cum_bm = sum(d["bm_detected"] for d in days_data)
    # Each TEL can fire ~6 missiles on average
    tels_used = cum_bm / 6.0
    depletion = min(tels_used / tel_est, 0.99)

    # Check for BM rebound (last 4 days) — if increasing, reduce depletion estimate
    if len(days_data) >= 4:
        last4 = [d["bm_detected"] for d in days_data[-4:]]
        if all(last4[i] <= last4[i+1] for i in range(len(last4)-1)) and last4[-1] > 10:
            # Accelerating BMs suggest reserves — cap depletion lower
            depletion = min(depletion, 0.75)

    return depletion

# ── HAM Lambda Monte Carlo ────────────────────────────────────────
def compute_lambda_mc(data, day_num, n_sim=50000):
    """Run 50K Monte Carlo for HAM feedback gain lambda."""
    days_list = data["days"]
    day_data  = next(d for d in days_list if d["day"] == day_num)
    prev_days = [d for d in days_list if d["day"] < day_num]

    rng = np.random.default_rng(42)

    # Parameters from data
    launcher_dep    = compute_launcher_depletion(data, day_num)
    drone_rem, drone_pct = compute_drone_stockpile(data, day_num)
    cum = compute_cumulative(days_list, day_num)

    carrier_eff = day_data.get("carrier_effective", 2.0)
    tail = day_data.get("realized_tail_risks", {})
    hormuz_closed   = tail.get("hormuz_closed", False)
    proxy_activated  = tail.get("proxy_activated", False)
    air_base_strike  = tail.get("air_base_strike", False)

    # Check BM rebound signal
    if day_num >= 5:
        recent_bm = [d["bm_detected"] for d in days_list if day_num - 4 < d["day"] <= day_num]
        bm_rebound = len(recent_bm) >= 3 and all(recent_bm[i] <= recent_bm[i+1] for i in range(len(recent_bm)-1)) and recent_bm[-1] >= 10
    else:
        bm_rebound = False

    lambdas = np.zeros(n_sim)

    for i in range(n_sim):
        lam = 1.0

        # λ_launcher (stabilizing)
        lam += -0.55 * launcher_dep * (1 + rng.normal(0, 0.10))

        # λ_drone
        drone_frac = drone_pct / 100.0
        lam += 0.50 * (1 - drone_frac) * rng.uniform(0.2, 0.6) if drone_frac < 0.50 else 0

        # λ_intercept
        cum_rate = cum["bm_intercept_rate"] / 100.0
        if cum_rate < 0.93:
            lam += 0.3 * (0.93 - cum_rate) * rng.uniform(0.5, 1.5)

        # λ_hormuz
        if hormuz_closed:
            lam += 0.6 * 1.0 * rng.uniform(0.6, 1.5)
        else:
            lam += 0.6 * (rng.random() < 0.02) * rng.uniform(0.6, 1.5)

        # λ_proxy
        if proxy_activated:
            # Hezbollah partial
            lam += 0.8 * 0.5 * rng.uniform(0.5, 2.0)
            # Houthi stochastic (30% chance)
            lam += 0.8 * (rng.random() < 0.30) * rng.uniform(0.3, 1.0)
        else:
            lam += 0.8 * (rng.random() < 0.04) * rng.uniform(0.5, 2.0)

        # λ_weapon (new escalation)
        if air_base_strike:
            lam += 0.4 * 1.0 * rng.uniform(0.5, 1.5)
        else:
            lam += 0.4 * (rng.random() < 0.03) * rng.uniform(0.5, 1.5)

        # λ_bm_rebound (new signal)
        if bm_rebound:
            lam += 0.3 * rng.uniform(0.5, 1.5)

        # λ_naval (stabilizing)
        lam += -0.08 * carrier_eff * (1 + rng.normal(0, 0.10))

        lambdas[i] = lam

    results = {
        "median":    float(np.median(lambdas)),
        "mean":      float(np.mean(lambdas)),
        "p5":        float(np.percentile(lambdas, 5)),
        "p95":       float(np.percentile(lambdas, 95)),
        "p_gt_1":    float(np.mean(lambdas > 1.0) * 100),
        "p_gt_1_5":  float(np.mean(lambdas > 1.5) * 100),
        "p_gt_2":    float(np.mean(lambdas > 2.0) * 100),
        "n_sim":     n_sim,
    }

    # Verdict
    if results["median"] >= 1.0:
        results["verdict"] = "UNSTABLE"
    elif results["p_gt_1"] > 5.0:
        results["verdict"] = "METASTABLE"
    else:
        results["verdict"] = "STABLE"

    # Cascade threshold count
    thresholds = data["metadata"]["cascade_thresholds"]
    breaches = 0
    breach_list = []

    if launcher_dep > thresholds["launcher_depletion"]:
        breaches += 1; breach_list.append("launcher")
    if (drone_pct / 100.0) < thresholds["drone_stockpile_remaining"]:
        breaches += 1; breach_list.append("drone_stockpile")
    if (cum["bm_intercept_rate"] / 100.0) < thresholds["interception_rate_cumulative"]:
        breaches += 1; breach_list.append("interception")
    daily_cas = day_data.get("deaths", 0) + day_data.get("injuries", 0)
    if daily_cas > thresholds["daily_casualties"]:
        breaches += 1; breach_list.append("casualties")
    if day_data.get("new_weapon_event"):
        breaches += 1; breach_list.append("new_weapon")

    # Also check day-level interception rate breach
    if day_data["bm_detected"] > 0:
        day_rate = day_data["bm_intercepted"] / day_data["bm_detected"]
        if day_rate < 0.90:
            if "interception" not in breach_list:
                breaches += 1; breach_list.append("interception_day")

    results["breaches"] = breaches
    results["breach_list"] = breach_list
    results["launcher_depletion"] = launcher_dep
    results["drone_stockpile_pct"] = drone_pct
    results["bm_rebound"] = bm_rebound

    # Component decomposition (median estimates)
    results["decomposition"] = {
        "lambda_launcher": -0.55 * launcher_dep,
        "lambda_drone": 0.50 * (1 - drone_pct/100) * 0.4 if drone_pct/100 < 0.50 else 0,
        "lambda_intercept": 0.3 * max(0, 0.93 - cum["bm_intercept_rate"]/100) * 1.0,
        "lambda_hormuz": 0.63 if hormuz_closed else 0.0,
        "lambda_proxy": 0.50 if proxy_activated else 0.0,
        "lambda_weapon": 0.40 if air_base_strike else 0.0,
        "lambda_bm_rebound": 0.30 if bm_rebound else 0.0,
        "lambda_naval": -0.08 * carrier_eff,
    }

    return results

# ── Chart Generation ──────────────────────────────────────────────
def generate_charts(data, day_num, results):
    """Generate model vs actual comparison charts."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    days_list = sorted([d for d in data["days"] if d["day"] <= day_num], key=lambda x: x["day"])
    day_nums = [d["day"] for d in days_list]
    dates = [datetime.datetime.strptime(d["date"], "%Y-%m-%d").strftime("%b %d") for d in days_list]

    # Model predictions (exponential decay for BMs, ~130/day for drones)
    bm_actual = [d["bm_detected"] for d in days_list]
    bm_model  = [days_list[0]["bm_detected"] * np.exp(-0.25 * (d["day"] - 1)) for d in days_list]

    drone_actual = [d["drones_detected"] for d in days_list]
    drone_model  = [days_list[0]["drones_detected"] if d["day"] <= 2 else 130 for d in days_list]
    if len(days_list) >= 2:
        drone_model[1] = days_list[1]["drones_detected"]  # Day 2 was actual peak

    # Cumulative intercept rate
    intercept_actual = []
    for d in days_list:
        c = compute_cumulative(data["days"], d["day"])
        intercept_actual.append(c["bm_intercept_rate"])
    intercept_model = [intercept_actual[0]] + [93.2] * (len(days_list) - 1)

    # Drone stockpile
    stock_actual = []
    for d in days_list:
        _, pct = compute_drone_stockpile(data, d["day"])
        stock_actual.append(pct)
    stock_model = []
    cum_est = 0
    for d in days_list:
        if d["day"] <= 2:
            cum_est += d["drones_detected"]
        else:
            cum_est += 130
        stock_model.append((data["metadata"]["drone_stockpile_estimate"] - cum_est) / data["metadata"]["drone_stockpile_estimate"] * 100)

    # Airport capacity
    airport_actual = [d["airport_capacity_pct"] for d in days_list]
    # Model: slow recovery curve
    airport_model = []
    for d in days_list:
        if d["day"] == 1: airport_model.append(30)
        elif d["day"] == 2: airport_model.append(0)
        else: airport_model.append(min(2 + (d["day"] - 3) * 5.5, 60))

    # Lambda evolution — compute for each day
    lambda_actual = []
    for d in days_list:
        r = compute_lambda_mc(data, d["day"], n_sim=10000)
        lambda_actual.append(r["median"])

    lambda_model = [lambda_actual[0]] * len(days_list)  # Model baseline stays flat

    # ── Plot ──
    colors = {'actual': '#d32f2f', 'model': '#1976d2', 'threshold': '#ff9800'}
    fig, axes = plt.subplots(3, 2, figsize=(16, 18))
    fig.suptitle(f'Model Predictions vs Actual — Days 1–{day_num}\nEvacuation Decision Model (ABC + HAM)',
                 fontsize=16, fontweight='bold', y=0.98)

    def setup_ax(ax, title, ylabel):
        ax.set_title(title, fontsize=13, fontweight='bold')
        ax.set_ylabel(ylabel)
        ax.set_xticks(day_nums)
        ax.set_xticklabels(dates, rotation=45, fontsize=9)
        ax.grid(True, alpha=0.3)

    # Panel 1: BMs
    ax = axes[0, 0]
    ax.plot(day_nums, bm_actual, 'o-', color=colors['actual'], lw=2.5, ms=8, label='Actual', zorder=5)
    ax.plot(day_nums, bm_model, 's--', color=colors['model'], lw=2, ms=6, label='Model (exp decay)', alpha=0.8)
    ax.fill_between(day_nums, bm_actual, bm_model, alpha=0.15, color=colors['actual'])
    setup_ax(ax, 'Ballistic Missiles per Day', 'Count')
    ax.legend(loc='upper right', fontsize=9)
    # Annotate latest
    ax.annotate(f'Day {day_num}: {bm_actual[-1]} BMs\n(model: {bm_model[-1]:.0f})',
                xy=(day_num, bm_actual[-1]), xytext=(max(1, day_num-3), max(bm_actual)*0.7),
                fontsize=9, arrowprops=dict(arrowstyle='->', color='red'), color='red', fontweight='bold')

    # Panel 2: Drones
    ax = axes[0, 1]
    ax.plot(day_nums, drone_actual, 'o-', color=colors['actual'], lw=2.5, ms=8, label='Actual')
    ax.plot(day_nums, drone_model, 's--', color=colors['model'], lw=2, ms=6, label='Model (~130/day)', alpha=0.8)
    setup_ax(ax, 'Drones Detected per Day', 'Count')
    ax.legend(loc='upper right', fontsize=9)

    # Panel 3: Interception rate
    ax = axes[1, 0]
    ax.plot(day_nums, intercept_actual, 'o-', color=colors['actual'], lw=2.5, ms=8, label='Actual (cumulative)')
    ax.plot(day_nums, intercept_model, 's--', color=colors['model'], lw=2, ms=6, label='Model', alpha=0.8)
    ax.axhline(y=90, color=colors['threshold'], lw=2, ls=':', label='Threshold (90%)')
    setup_ax(ax, 'BM Interception Rate (Cumulative)', 'Rate (%)')
    ax.legend(loc='lower left', fontsize=9)
    ax.set_ylim(85, 100)

    # Panel 4: Drone stockpile
    ax = axes[1, 1]
    ax.plot(day_nums, stock_actual, 'o-', color=colors['actual'], lw=2.5, ms=8, label='Actual')
    ax.plot(day_nums, stock_model, 's--', color=colors['model'], lw=2, ms=6, label='Model', alpha=0.8)
    ax.axhline(y=30, color=colors['threshold'], lw=2, ls=':', label='Threshold (30%)')
    setup_ax(ax, 'Drone Stockpile Remaining (%)', 'Remaining (%)')
    ax.legend(loc='upper right', fontsize=9)
    ax.set_ylim(20, 95)

    # Panel 5: Airport capacity
    ax = axes[2, 0]
    ax.plot(day_nums, airport_actual, 'o-', color='#2e7d32', lw=2.5, ms=8, label='Actual')
    ax.plot(day_nums, airport_model, 's--', color=colors['model'], lw=2, ms=6, label='Model', alpha=0.8)
    ax.fill_between(day_nums, airport_actual, airport_model, alpha=0.15, color='#2e7d32')
    setup_ax(ax, 'Airport Capacity (% of Normal)', 'Capacity (%)')
    ax.legend(loc='upper left', fontsize=9)

    # Panel 6: Lambda
    ax = axes[2, 1]
    ax.plot(day_nums, lambda_actual, 'o-', color=colors['actual'], lw=2.5, ms=8, label='Actual (with realized events)')
    ax.axhline(y=1.0, color=colors['threshold'], lw=2.5, ls=':', label='Cascade Threshold (λ=1.0)')
    ax.fill_between(day_nums, lambda_actual, 1.0, where=[v > 1.0 for v in lambda_actual],
                    alpha=0.3, color='red', label='CASCADE ZONE')
    setup_ax(ax, 'HAM Feedback Gain (λ)', 'λ')
    ax.legend(loc='upper left', fontsize=9)
    if max(lambda_actual) > 1.5:
        ax.annotate(f'λ = {lambda_actual[-1]:.3f}\nCASCADE',
                    xy=(day_num, lambda_actual[-1]),
                    xytext=(max(1, day_num-3), max(lambda_actual)*0.9),
                    fontsize=11, arrowprops=dict(arrowstyle='->', color='red', lw=2),
                    color='red', fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffcdd2', edgecolor='red'))

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    fig.text(0.5, 0.005,
             f'Data: @modgovae (UAE MOD) | Model: ABC + Brock-Hommes HAM (50K MC) | Day {day_num}',
             ha='center', fontsize=10, color='gray', style='italic')

    out_path = CHARTS_DIR / f"model_vs_actual_day{day_num}.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Chart saved: {out_path}")
    return str(out_path)

# ── Generate Lambda Evolution Chart ───────────────────────────────
def generate_lambda_chart(data, day_num):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    days_list = sorted([d for d in data["days"] if d["day"] <= day_num], key=lambda x: x["day"])

    lambdas = []
    p_gt1_list = []
    verdicts = []
    for d in days_list:
        r = compute_lambda_mc(data, d["day"], n_sim=10000)
        lambdas.append(r["median"])
        p_gt1_list.append(r["p_gt_1"])
        verdicts.append(r["verdict"])

    day_nums = [d["day"] for d in days_list]
    dates = [datetime.datetime.strptime(d["date"], "%Y-%m-%d").strftime("%b %d") for d in days_list]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    fig.suptitle(f'Lambda (λ) Evolution — Days 1–{day_num}', fontsize=15, fontweight='bold')

    # Top: Lambda
    ax1.plot(day_nums, lambdas, 'o-', color='#d32f2f', lw=3, ms=10, zorder=5)
    ax1.axhline(y=1.0, color='#ff9800', lw=2.5, ls='--', label='Cascade Threshold')
    ax1.fill_between(day_nums, lambdas, 1.0, where=[v > 1 for v in lambdas], alpha=0.3, color='red')
    for i, (dn, lv, v) in enumerate(zip(day_nums, lambdas, verdicts)):
        ax1.annotate(f'{lv:.3f}', (dn, lv), textcoords="offset points", xytext=(0, 12),
                     ha='center', fontsize=9, fontweight='bold',
                     color='red' if v == 'UNSTABLE' else '#1976d2')
    ax1.set_ylabel('λ median (50K MC)', fontsize=12)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, max(lambdas) * 1.3)

    # Bottom: P(λ>1)
    bars = ax2.bar(day_nums, p_gt1_list, color=['#d32f2f' if p > 50 else '#ff9800' if p > 10 else '#4caf50' for p in p_gt1_list], alpha=0.8)
    ax2.axhline(y=50, color='gray', lw=1, ls='--', alpha=0.5)
    for dn, p in zip(day_nums, p_gt1_list):
        ax2.annotate(f'{p:.1f}%', (dn, p), textcoords="offset points", xytext=(0, 5),
                     ha='center', fontsize=9, fontweight='bold')
    ax2.set_ylabel('P(λ > 1.0) %', fontsize=12)
    ax2.set_xlabel('Day')
    ax2.set_xticks(day_nums)
    ax2.set_xticklabels([f'Day {dn}\n{dt}' for dn, dt in zip(day_nums, dates)], fontsize=9)
    ax2.grid(True, alpha=0.3, axis='y')
    ax2.set_ylim(0, 110)

    plt.tight_layout()
    out_path = CHARTS_DIR / f"lambda_evolution_day{day_num}.png"
    plt.savefig(out_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Chart saved: {out_path}")
    return str(out_path)

# ── Markdown Generators ───────────────────────────────────────────
MONTH_MAP = {1:'january',2:'february',3:'march',4:'april',5:'may',6:'june',
             7:'july',8:'august',9:'september',10:'october',11:'november',12:'december'}
MONTH_MAP_ZH = {1:'1月',2:'2月',3:'3月',4:'4月',5:'5月',6:'6月',
                7:'7月',8:'8月',9:'9月',10:'10月',11:'11月',12:'12月'}

def generate_day_page_en(data, day_num, results):
    """Generate English daily update markdown page."""
    day_data = next(d for d in data["days"] if d["day"] == day_num)
    prev_data = next((d for d in data["days"] if d["day"] == day_num - 1), None)
    dt = datetime.datetime.strptime(day_data["date"], "%Y-%m-%d")
    cum = compute_cumulative(data["days"], day_num)

    verdict_str = results["verdict"]
    breaches = results["breaches"]
    verdict_emoji = "⚠️" if verdict_str == "UNSTABLE" else "🟡" if verdict_str == "METASTABLE" else "🟢"

    # Build page
    lines = []
    lines.append(f"# Day {day_num} Update — {dt.strftime('%B %d, %Y')}")
    lines.append("")
    lines.append(f"> 🌐 **EN** | [中文](../zh/updates/day{day_num}-{MONTH_MAP[dt.month]}{dt.day}.md)")
    lines.append("")
    lines.append(f"**Status: {verdict_str}** | **Breaches: {breaches}/5** | **λ median = {results['median']:.3f}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Data table
    lines.append("## New Data")
    lines.append("")
    lines.append("| Metric | Day {} | Day {} | Cumulative |".format(day_num-1, day_num))
    lines.append("|--------|-------|-------|------------|")

    prev_bm = prev_data["bm_detected"] if prev_data else "—"
    lines.append(f"| Ballistic Missiles | {prev_bm} | **{day_data['bm_detected']}** | **{cum['bm_detected']}** |")
    lines.append(f"| BM Intercepted | {prev_data['bm_intercepted'] if prev_data else '—'} | {day_data['bm_intercepted']} | {cum['bm_intercepted']} |")
    lines.append(f"| Drones Detected | {prev_data['drones_detected'] if prev_data else '—'} | ~{day_data['drones_detected']} | ~{cum['drones_detected']} |")
    lines.append(f"| Drones Intercepted | {prev_data['drones_intercepted'] if prev_data else '—'} | {day_data['drones_intercepted']} | ~{cum['drones_intercepted']} |")
    lines.append(f"| Cruise Missiles | {prev_data['cruise_missiles'] if prev_data else '—'} | {day_data['cruise_missiles']} | {cum['cruise_missiles']} |")
    lines.append(f"| BM Intercept Rate (cum) | — | — | {cum['bm_intercept_rate']:.1f}% |")
    drone_stock_rem, drone_stock_pct = compute_drone_stockpile(data, day_num)
    lines.append(f"| Drone Stockpile | — | — | {drone_stock_pct:.1f}% ({drone_stock_rem:.0f}/{data['metadata']['drone_stockpile_estimate']}) |")
    lines.append("")

    # Key events
    if day_data.get("key_events"):
        lines.append("**Key Events:**")
        for evt in day_data["key_events"]:
            lines.append(f"- {evt}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Lambda section
    lines.append("## Lambda Recalculation")
    lines.append("")
    lines.append("```")
    decomp = results["decomposition"]
    lines.append("λ = 1.0")
    for key, val in decomp.items():
        label = key.replace("lambda_", "λ_")
        lines.append(f"  + {label:20s} = {val:+.3f}")
    lines.append("  " + "─" * 30)
    lines.append(f"  λ median           = {results['median']:.3f}  ({results['n_sim']//1000}K Monte Carlo)")
    lines.append("```")
    lines.append("")

    lines.append("| Metric | Value |")
    lines.append("|--------|-------|")
    lines.append(f"| λ median | **{results['median']:.3f}** |")
    lines.append(f"| λ 95th percentile | **{results['p95']:.3f}** |")
    lines.append(f"| P(λ > 1.0) | **{results['p_gt_1']:.1f}%** |")
    lines.append(f"| P(λ > 1.5) | **{results['p_gt_1_5']:.1f}%** |")
    lines.append(f"| P(λ > 2.0) | **{results['p_gt_2']:.1f}%** |")
    lines.append(f"| Verdict | **{verdict_str}** |")
    lines.append(f"| Breaches | **{breaches}/5** ({', '.join(results['breach_list'])}) |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Charts
    lines.append("## Charts")
    lines.append("")
    lines.append(f"![Model vs Actual](../charts/model_vs_actual_day{day_num}.png)")
    lines.append("")
    lines.append(f"![Lambda Evolution](../charts/lambda_evolution_day{day_num}.png)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Recommendation
    if results["median"] >= 1.5:
        rec = "**EVACUATE IMMEDIATELY.** System is in CASCADE territory."
    elif results["median"] >= 1.0:
        rec = "**EVACUATE.** System has crossed cascade threshold."
    elif results["p_gt_1"] > 20:
        rec = "**PREPARE TO EVACUATE.** Elevated cascade risk."
    else:
        rec = "**MONITOR.** System within normal parameters."
    lines.append("## Recommendation")
    lines.append("")
    lines.append(rec)
    lines.append("")

    # Sources
    lines.append("---")
    lines.append("")
    lines.append("## Sources")
    lines.append("")
    lines.append("| Source | Type |")
    lines.append("|--------|------|")
    lines.append("| @modgovae (X.com) | UAE MOD daily update |")
    lines.append("| Model pipeline | ABC + HAM (50K MC) |")
    lines.append(f"| Generated | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} |")
    lines.append("")

    content = "\n".join(lines)
    slug = f"day{day_num}-{MONTH_MAP[dt.month]}{dt.day}"
    out_path = UPDATES_DIR / f"{slug}.md"
    with open(out_path, "w") as f:
        f.write(content)
    print(f"  EN page saved: {out_path}")
    return slug

def generate_day_page_zh(data, day_num, results):
    """Generate Chinese daily update markdown page."""
    day_data = next(d for d in data["days"] if d["day"] == day_num)
    prev_data = next((d for d in data["days"] if d["day"] == day_num - 1), None)
    dt = datetime.datetime.strptime(day_data["date"], "%Y-%m-%d")
    cum = compute_cumulative(data["days"], day_num)

    verdict_map = {"UNSTABLE": "不稳定", "METASTABLE": "亚稳态", "STABLE": "稳定"}
    verdict_zh = verdict_map.get(results["verdict"], results["verdict"])
    verdict_emoji = "⚠️" if results["verdict"] == "UNSTABLE" else "🟡" if results["verdict"] == "METASTABLE" else "🟢"

    lines = []
    lines.append(f"# 第{day_num}天更新 — {dt.year}年{dt.month}月{dt.day}日")
    lines.append("")
    slug_en = f"day{day_num}-{MONTH_MAP[dt.month]}{dt.day}"
    lines.append(f"> 🌐 [English](../../updates/{slug_en}.md) | **中文**")
    lines.append("")
    lines.append(f"**状态：{verdict_zh}** | **突破：{results['breaches']}/5** | **λ中位数 = {results['median']:.3f}**")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Data table
    lines.append("## 新数据")
    lines.append("")
    lines.append(f"| 指标 | 第{day_num-1}天 | 第{day_num}天 | 累计 |")
    lines.append("|------|-------|-------|------|")

    prev_bm = prev_data["bm_detected"] if prev_data else "—"
    lines.append(f"| 弹道导弹 | {prev_bm} | **{day_data['bm_detected']}** | **{cum['bm_detected']}** |")
    lines.append(f"| 弹道导弹拦截 | {prev_data['bm_intercepted'] if prev_data else '—'} | {day_data['bm_intercepted']} | {cum['bm_intercepted']} |")
    lines.append(f"| 无人机探测 | {prev_data['drones_detected'] if prev_data else '—'} | ~{day_data['drones_detected']} | ~{cum['drones_detected']} |")
    lines.append(f"| 无人机拦截 | {prev_data['drones_intercepted'] if prev_data else '—'} | {day_data['drones_intercepted']} | ~{cum['drones_intercepted']} |")
    lines.append(f"| 巡航导弹 | {prev_data['cruise_missiles'] if prev_data else '—'} | {day_data['cruise_missiles']} | {cum['cruise_missiles']} |")
    lines.append(f"| 弹道导弹拦截率（累计） | — | — | {cum['bm_intercept_rate']:.1f}% |")
    drone_stock_rem, drone_stock_pct = compute_drone_stockpile(data, day_num)
    lines.append(f"| 无人机库存剩余 | — | — | {drone_stock_pct:.1f}%（{drone_stock_rem:.0f}/{data['metadata']['drone_stockpile_estimate']}） |")
    lines.append("")

    # Key events
    if day_data.get("key_events"):
        lines.append("**关键事件：**")
        for evt in day_data["key_events"]:
            lines.append(f"- {evt}")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Lambda section
    lines.append("## Lambda重新计算")
    lines.append("")
    lines.append("```")
    decomp = results["decomposition"]
    label_map = {
        "lambda_launcher": "λ_发射装置",
        "lambda_drone": "λ_无人机",
        "lambda_intercept": "λ_拦截",
        "lambda_hormuz": "λ_霍尔木兹",
        "lambda_proxy": "λ_代理人",
        "lambda_weapon": "λ_武器",
        "lambda_bm_rebound": "λ_弹道反弹",
        "lambda_naval": "λ_海军威慑",
    }
    lines.append("λ = 1.0")
    for key, val in decomp.items():
        label = label_map.get(key, key)
        lines.append(f"  + {label:14s} = {val:+.3f}")
    lines.append("  " + "─" * 28)
    lines.append(f"  λ 中位数       = {results['median']:.3f}（{results['n_sim']//1000}K蒙特卡罗）")
    lines.append("```")
    lines.append("")

    lines.append("| 指标 | 数值 |")
    lines.append("|------|------|")
    lines.append(f"| λ 中位数 | **{results['median']:.3f}** |")
    lines.append(f"| λ 第95百分位 | **{results['p95']:.3f}** |")
    lines.append(f"| P(λ > 1.0) | **{results['p_gt_1']:.1f}%** |")
    lines.append(f"| P(λ > 1.5) | **{results['p_gt_1_5']:.1f}%** |")
    lines.append(f"| P(λ > 2.0) | **{results['p_gt_2']:.1f}%** |")
    lines.append(f"| 判定 | **{verdict_zh}** |")
    lines.append(f"| 突破数 | **{results['breaches']}/5** |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Charts
    lines.append("## 图表")
    lines.append("")
    lines.append(f"![模型vs实际](../../charts/model_vs_actual_day{day_num}.png)")
    lines.append("")
    lines.append(f"![Lambda演变](../../charts/lambda_evolution_day{day_num}.png)")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Recommendation
    if results["median"] >= 1.5:
        rec = "**立即撤离。** 系统处于级联区域。"
    elif results["median"] >= 1.0:
        rec = "**撤离。** 系统已跨越级联阈值。"
    elif results["p_gt_1"] > 20:
        rec = "**准备撤离。** 级联风险升高。"
    else:
        rec = "**监测。** 系统在正常参数范围内。"
    lines.append("## 建议")
    lines.append("")
    lines.append(rec)
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## 数据来源")
    lines.append("")
    lines.append("| 来源 | 类型 |")
    lines.append("|------|------|")
    lines.append("| @modgovae (X.com) | 阿联酋国防部每日更新 |")
    lines.append("| 模型管线 | ABC + HAM (50K MC) |")
    lines.append(f"| 生成时间 | {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')} |")
    lines.append("")

    content = "\n".join(lines)
    slug = f"day{day_num}-{MONTH_MAP[dt.month]}{dt.day}"
    out_path = ZH_UPDATES / f"{slug}.md"
    with open(out_path, "w") as f:
        f.write(content)
    print(f"  ZH page saved: {out_path}")
    return slug

# ── Update SUMMARY.md ─────────────────────────────────────────────
def update_summary(data, day_num, slug, results):
    """Add new day entry to SUMMARY.md navigation."""
    verdict_emoji = "⚠️" if results["verdict"] == "UNSTABLE" else "🟡" if results["verdict"] == "METASTABLE" else "🟢"
    dt_obj = datetime.datetime.strptime(next(d for d in data["days"] if d["day"] == day_num)["date"], "%Y-%m-%d")
    month_day = f"{MONTH_MAP[dt_obj.month].capitalize()} {dt_obj.day}"

    en_entry = f"* [Day {day_num} — {month_day} {verdict_emoji} {results['verdict']}](updates/{slug}.md)"
    zh_entry = f"* [第{day_num}天 — {dt_obj.month}月{dt_obj.day}日 {verdict_emoji} {'不稳定' if results['verdict']=='UNSTABLE' else '亚稳态' if results['verdict']=='METASTABLE' else '稳定'}](zh/updates/{slug}.md)"

    summary_path = SUMMARY_F
    if not summary_path.exists():
        print(f"  WARNING: {summary_path} not found, skipping SUMMARY update")
        return

    content = summary_path.read_text()

    # Check if entry already exists
    if f"updates/{slug}.md" not in content:
        # Find insertion point for EN
        if "## Daily Updates" in content:
            # Add after the tracker line
            idx = content.find("## Daily Updates")
            # Find the end of the daily updates section
            next_section = content.find("\n## ", idx + 1)
            if next_section == -1:
                next_section = content.find("\n### ", idx + 1)
            if next_section == -1:
                next_section = len(content)
            insert_pos = next_section
            content = content[:insert_pos] + en_entry + "\n" + content[insert_pos:]
        else:
            content += f"\n## Daily Updates\n* [📊 Day-by-Day Tracker](updates/daily-tracker.md)\n{en_entry}\n"

    if f"zh/updates/{slug}.md" not in content:
        if "### 每日更新" in content:
            idx = content.find("### 每日更新")
            next_section = content.find("\n## ", idx + 1)
            if next_section == -1:
                next_section = content.find("\n### ", idx + 1)
            if next_section == -1:
                next_section = len(content)
            insert_pos = next_section
            content = content[:insert_pos] + zh_entry + "\n" + content[insert_pos:]
        else:
            content += f"\n### 每日更新\n* [📊 逐日追踪](zh/updates/daily-tracker.md)\n{zh_entry}\n"

    summary_path.write_text(content)
    print(f"  SUMMARY.md updated")

# ── Run Log ───────────────────────────────────────────────────────
def append_run_log(day_num, results, slug):
    log = []
    if RUN_LOG.exists():
        with open(RUN_LOG) as f:
            log = json.load(f)
    log.append({
        "timestamp": datetime.datetime.now().isoformat(),
        "day": day_num,
        "slug": slug,
        "lambda_median": results["median"],
        "lambda_p95": results["p95"],
        "p_gt_1": results["p_gt_1"],
        "verdict": results["verdict"],
        "breaches": results["breaches"],
    })
    with open(RUN_LOG, "w") as f:
        json.dump(log, f, indent=2)
    print(f"  Run log updated ({len(log)} entries)")

# ── CLI: Add New Day ──────────────────────────────────────────────
def add_new_day_interactive(data):
    """Interactively add a new day entry to the data file."""
    last_day = max(d["day"] for d in data["days"])
    new_day = last_day + 1
    last_date = datetime.datetime.strptime(data["days"][-1]["date"], "%Y-%m-%d")
    new_date = (last_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    print(f"\n--- Adding Day {new_day} ({new_date}) ---")

    def ask_int(prompt, default=0):
        val = input(f"  {prompt} [{default}]: ").strip()
        return int(val) if val else default

    def ask_float(prompt, default=0.0):
        val = input(f"  {prompt} [{default}]: ").strip()
        return float(val) if val else default

    def ask_bool(prompt, default=False):
        val = input(f"  {prompt} [{'Y' if default else 'N'}]: ").strip().lower()
        if val in ('y', 'yes', 'true', '1'): return True
        if val in ('n', 'no', 'false', '0'): return False
        return default

    def ask_str(prompt, default=""):
        val = input(f"  {prompt} [{default}]: ").strip()
        return val if val else default

    entry = {
        "day": new_day,
        "date": ask_str("Date (YYYY-MM-DD)", new_date),
        "bm_detected": ask_int("Ballistic missiles detected"),
        "bm_intercepted": ask_int("BM intercepted"),
        "bm_fell_sea": ask_int("BM fell in sea"),
        "bm_fell_land": ask_int("BM fell on land"),
        "drones_detected": ask_int("Drones detected"),
        "drones_intercepted": ask_int("Drones intercepted"),
        "drones_fell_uae": ask_int("Drones fell in UAE"),
        "cruise_missiles": ask_int("Cruise missiles"),
        "deaths": ask_int("Deaths"),
        "injuries": ask_int("Injuries"),
        "airport_capacity_pct": ask_int("Airport capacity %"),
        "oil_wti": ask_float("Oil WTI price"),
        "vlcc_rate": ask_int("VLCC day rate"),
        "hormuz_status": ask_str("Hormuz status (open/closed)", "closed"),
        "hormuz_crossings": ask_int("Hormuz crossings", 0),
        "proxy_active": ask_bool("Proxy forces active?", True),
        "new_weapon_event": ask_str("New weapon event (or empty)", "") or None,
        "polymarket_ceasefire_mar31": ask_int("Polymarket ceasefire Mar 31 %", 0) or None,
        "carrier_count": ask_int("Carrier count", 3),
        "carrier_effective": ask_float("Effective carriers", 2.3),
        "key_events": [],
        "realized_tail_risks": {
            "hormuz_closed": ask_bool("Hormuz closed?", True),
            "proxy_activated": ask_bool("Proxy activated?", True),
            "air_base_strike": ask_bool("Air base strike?", True),
        },
        "notes": ask_str("Notes", ""),
    }

    # Add key events
    print("  Key events (enter empty to stop):")
    while True:
        evt = input("    Event: ").strip()
        if not evt:
            break
        entry["key_events"].append(evt)

    data["days"].append(entry)
    save_data(data)
    print(f"\n  Day {new_day} added to daily_data.json")
    return new_day

# ── CLI: Add from args ────────────────────────────────────────────
def add_from_args(data, args):
    """Add new day from command-line arguments."""
    last_day = max(d["day"] for d in data["days"])
    new_day = args.day if args.day else last_day + 1
    last_date = datetime.datetime.strptime(data["days"][-1]["date"], "%Y-%m-%d")
    new_date = args.date if args.date else (last_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    entry = {
        "day": new_day,
        "date": new_date,
        "bm_detected": args.bm or 0,
        "bm_intercepted": args.bm_int or 0,
        "bm_fell_sea": args.bm_sea or 0,
        "bm_fell_land": args.bm_land or 0,
        "drones_detected": args.drones or 0,
        "drones_intercepted": args.drones_int or 0,
        "drones_fell_uae": args.drones_fell or 0,
        "cruise_missiles": args.cm or 0,
        "deaths": args.deaths or 0,
        "injuries": args.injuries or 0,
        "airport_capacity_pct": args.airport or 0,
        "oil_wti": args.oil or 0,
        "vlcc_rate": args.vlcc or 0,
        "hormuz_status": args.hormuz_status or "closed",
        "hormuz_crossings": args.hormuz_crossings or 0,
        "proxy_active": args.proxy_active if args.proxy_active is not None else True,
        "new_weapon_event": args.weapon_event or None,
        "polymarket_ceasefire_mar31": args.polymarket or None,
        "carrier_count": args.carriers or 3,
        "carrier_effective": args.carriers_eff or 2.3,
        "key_events": args.events.split("|") if args.events else [],
        "realized_tail_risks": {
            "hormuz_closed": args.hormuz_closed if args.hormuz_closed is not None else True,
            "proxy_activated": args.proxy_activated if args.proxy_activated is not None else True,
            "air_base_strike": args.air_base if args.air_base is not None else False,
        },
        "notes": args.notes or "",
    }

    data["days"].append(entry)
    save_data(data)
    print(f"  Day {new_day} added from CLI args")
    return new_day

# ── Main Pipeline ─────────────────────────────────────────────────
def run_pipeline(day_num=None):
    data = load_data()

    if day_num is None:
        day_num = max(d["day"] for d in data["days"])

    day_data = next((d for d in data["days"] if d["day"] == day_num), None)
    if day_data is None:
        print(f"ERROR: Day {day_num} not found in daily_data.json")
        sys.exit(1)

    dt = datetime.datetime.strptime(day_data["date"], "%Y-%m-%d")
    print(f"\n{'='*60}")
    print(f"  DAILY UPDATE PIPELINE — Day {day_num} ({day_data['date']})")
    print(f"{'='*60}\n")

    # Step 1: Compute lambda
    print("[1/6] Running Monte Carlo (50K simulations)...")
    results = compute_lambda_mc(data, day_num)
    print(f"  λ median = {results['median']:.3f}")
    print(f"  P(λ>1)  = {results['p_gt_1']:.1f}%")
    print(f"  Verdict  = {results['verdict']}")
    print(f"  Breaches = {results['breaches']}/5 ({', '.join(results['breach_list'])})")

    # Step 2: Generate charts
    print("\n[2/6] Generating comparison chart...")
    generate_charts(data, day_num, results)

    print("\n[3/6] Generating lambda evolution chart...")
    generate_lambda_chart(data, day_num)

    # Step 3: Generate EN page
    print("\n[4/6] Generating English update page...")
    slug = generate_day_page_en(data, day_num, results)

    # Step 4: Generate ZH page
    print("\n[5/6] Generating Chinese update page...")
    generate_day_page_zh(data, day_num, results)

    # Step 5: Update SUMMARY.md
    print("\n[6/6] Updating SUMMARY.md...")
    update_summary(data, day_num, slug, results)

    # Append run log
    append_run_log(day_num, results, slug)

    print(f"\n{'='*60}")
    print(f"  PIPELINE COMPLETE")
    print(f"  Day {day_num} | λ = {results['median']:.3f} | {results['verdict']}")
    print(f"  Outputs:")
    print(f"    charts/model_vs_actual_day{day_num}.png")
    print(f"    charts/lambda_evolution_day{day_num}.png")
    print(f"    updates/{slug}.md")
    print(f"    zh/updates/{slug}.md")
    print(f"{'='*60}\n")

    return results

# ── Argument Parser ───────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Evacuation Model Daily Update Pipeline")
    parser.add_argument("--day", type=int, help="Process specific day number")
    parser.add_argument("--add", action="store_true", help="Add new day entry (interactive)")

    # CLI add parameters
    parser.add_argument("--date", type=str)
    parser.add_argument("--bm", type=int)
    parser.add_argument("--bm-int", type=int)
    parser.add_argument("--bm-sea", type=int)
    parser.add_argument("--bm-land", type=int)
    parser.add_argument("--drones", type=int)
    parser.add_argument("--drones-int", type=int)
    parser.add_argument("--drones-fell", type=int)
    parser.add_argument("--cm", type=int)
    parser.add_argument("--deaths", type=int)
    parser.add_argument("--injuries", type=int)
    parser.add_argument("--airport", type=int)
    parser.add_argument("--oil", type=float)
    parser.add_argument("--vlcc", type=int)
    parser.add_argument("--hormuz-status", type=str)
    parser.add_argument("--hormuz-crossings", type=int)
    parser.add_argument("--proxy-active", type=bool)
    parser.add_argument("--weapon-event", type=str)
    parser.add_argument("--polymarket", type=int)
    parser.add_argument("--carriers", type=int)
    parser.add_argument("--carriers-eff", type=float)
    parser.add_argument("--hormuz-closed", type=bool)
    parser.add_argument("--proxy-activated", type=bool)
    parser.add_argument("--air-base", type=bool)
    parser.add_argument("--events", type=str, help="Pipe-separated key events")
    parser.add_argument("--notes", type=str)

    args = parser.parse_args()

    data = load_data()

    if args.add:
        if args.bm is not None:
            # CLI add mode
            day_num = add_from_args(data, args)
        else:
            # Interactive add mode
            day_num = add_new_day_interactive(data)
        data = load_data()  # Reload after add
        run_pipeline(day_num)
    else:
        run_pipeline(args.day)

if __name__ == "__main__":
    main()
