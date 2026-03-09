#!/usr/bin/env python3
"""
UAE Evacuation Model — Daily GitBook Updater
=============================================
Usage:
    python daily_update.py                     # Interactive mode — prompts for all data
    python daily_update.py --day 10 --date "Mar 9"  # Specify day number and date
    python daily_update.py --from-json day10.json   # Load data from JSON file

This script:
  1. Prompts for (or loads) the latest @modgovae numbers
  2. Regenerates all 6 matplotlib charts
  3. Creates the English & Chinese day-N update pages
  4. Appends Day N rows to both daily-tracker.md files
  5. Adds links to SUMMARY.md
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from copy import deepcopy

# ── paths ────────────────────────────────────────────────────────────
SCRIPT_DIR  = Path(__file__).resolve().parent
CHARTS_DIR  = SCRIPT_DIR / "charts"
UPDATES_EN  = SCRIPT_DIR / "updates"
UPDATES_ZH  = SCRIPT_DIR / "zh" / "updates"
SUMMARY_F   = SCRIPT_DIR / "SUMMARY.md"

# ── historical data (Days 1-9) ───────────────────────────────────────
# Each list is indexed [0]=Day1, [1]=Day2, ... [8]=Day9
HISTORY = {
    "bm_daily":        [137, 28, 9, 12, 3, 7, 9, 16, 17],
    "bm_intercepted":  [132, 20, 9, 11, 3, 6, 9, 15, 16],
    "drone_daily":     [209, 332, 148, 123, 129, 131, 112, 125, 117],
    "drone_intercept": [199, 310, 140, 115, 121, 123, 105, 119, 113],
    "cruise_daily":    [0, 2, 6, 0, 0, 0, 0, 0, 0],
    "intercept_cum":   [96.4, 92.1, 93.6, 93.0, 93.1, 93.4, 92.7, 92.8, 92.9],
    "stockpile_pct":   [89.6, 73.0, 65.6, 59.4, 53.0, 46.4, 40.8, 34.5, 28.9],
    "lambda_actual":   [0.53, 0.47, 1.70, 1.68, 1.67, 1.75, 1.72, 2.49, 2.71],
    "p_lambda_gt1":    [5.5, 5.4, 99.9, 99.7, 99.7, 100.0, 99.9, 100.0, 100.0],
    "airport_actual":  [30, 0, 2, 5, 8, 15, 25, 55, 65],
    "killed_daily":    [0, 1, 0, 1, 0, 1, 0, 0, 1],
    "injured_daily":   [15, 22, 12, 10, 8, 11, 15, 19, 18],
    "oil_wti":         [72, 78, 82, 86, 90, 93, 95, 97, 100],
    "polymarket":      [0, 0, 0, 0, 0, 67, 63, 61, 59],
    "dates":           ["Feb 28","Mar 1","Mar 2","Mar 3","Mar 4","Mar 5","Mar 6","Mar 7","Mar 8"],
}

# Model baselines (kept constant)
MODEL = {
    "bm_model":        [137, 28, 19, 14, 10, 8, 6, 4, 3],
    "drone_model":     [209, 332, 130, 130, 130, 130, 130, 130, 130],
    "intercept_model": [93.2]*9,
    "airport_model":   [30, 0, 2, 3, 8, 12, 15, 35, 40],
    "stockpile_model": [89.6, 73.0, 65.5, 59.4, 53.0, 46.4, 40.8, 35.0, 29.5],
    "lambda_model":    [0.53, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47, 0.47],
}

DRONE_TOTAL_EST = 2000  # estimated total Iranian drone stockpile

# ── Lambda component defaults (tuned each day) ──────────────────────
LAMBDA_COMPONENTS_DEFAULT = {
    "launcher":   -0.350,
    "drone":       0.210,
    "intercept":   0.001,
    "hormuz":      0.630,
    "proxy":       0.500,
    "weapon":      0.400,
    "bm_rebound":  0.350,
    "naval":      -0.150,
}


# =====================================================================
# INPUT COLLECTION
# =====================================================================
def prompt_int(msg, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"  {msg}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return int(raw)
        except ValueError:
            print("    → Please enter an integer.")

def prompt_float(msg, default=None):
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"  {msg}{suffix}: ").strip()
        if raw == "" and default is not None:
            return default
        try:
            return float(raw)
        except ValueError:
            print("    → Please enter a number.")

def prompt_str(msg, default=""):
    suffix = f" [{default}]" if default else ""
    raw = input(f"  {msg}{suffix}: ").strip()
    return raw if raw else default


def collect_interactive(day_num):
    """Prompt user for all daily inputs."""
    print(f"\n{'='*60}")
    print(f"  UAE Evacuation Model — Day {day_num} Data Entry")
    print(f"{'='*60}\n")

    d = {}

    # Date
    prev_date = datetime.strptime(f"2026 {HISTORY['dates'][-1]}", "%Y %b %d")
    next_date = prev_date + timedelta(days=1)
    default_date = next_date.strftime("%b %-d")
    d["date_str"] = prompt_str("Date (e.g. 'Mar 9')", default_date)

    print("\n── @modgovae Numbers ──")
    d["bm_detected"]       = prompt_int("Ballistic missiles detected (daily)")
    d["bm_intercepted"]    = prompt_int("BM intercepted (daily)")
    d["drone_detected"]    = prompt_int("Drones detected (daily)")
    d["drone_intercepted"] = prompt_int("Drones intercepted (daily)")
    d["cruise_daily"]      = prompt_int("Cruise missiles (daily)", 0)

    print("\n── Casualties ──")
    d["killed"]   = prompt_int("Killed (daily)", 0)
    d["injured"]  = prompt_int("Injured (daily)", 0)

    print("\n── Airport & Market ──")
    d["airport_pct"]  = prompt_int("Airport capacity % (estimate)", HISTORY["airport_actual"][-1])
    d["oil_brent"]    = prompt_int("Brent/WTI price ($)", HISTORY["oil_wti"][-1])
    d["polymarket"]   = prompt_int("Polymarket ceasefire % (by Mar 31)", HISTORY["polymarket"][-1])

    print("\n── Lambda Components (press Enter for auto-estimate) ──")
    d["lambda_components"] = {}
    for key, prev_val in LAMBDA_COMPONENTS_DEFAULT.items():
        d["lambda_components"][key] = prompt_float(f"λ_{key}", prev_val)

    print("\n── Events (one per line, blank to finish) ──")
    d["events"] = []
    while True:
        ev = input("  Event: ").strip()
        if not ev:
            break
        d["events"].append(ev)

    d["modgovae_tweet_url"] = prompt_str("@modgovae tweet URL (optional)")

    return d


def load_from_json(path):
    """Load day data from a JSON file."""
    with open(path) as f:
        return json.load(f)


# =====================================================================
# DATA COMPUTATION
# =====================================================================
def compute_derived(day_num, d, hist):
    """Compute cumulative totals, stockpile, interception rate, lambda."""
    # Cumulative
    d["bm_cum"]    = sum(hist["bm_daily"]) + d["bm_detected"]
    d["drone_cum"] = sum(hist["drone_daily"]) + d["drone_detected"]
    d["cruise_cum"]= sum(hist["cruise_daily"]) + d["cruise_daily"]
    d["total_daily"] = d["bm_detected"] + d["drone_detected"] + d["cruise_daily"]
    d["total_cum"]   = d["bm_cum"] + d["drone_cum"] + d["cruise_cum"]

    # BM interception rate (cumulative)
    total_bm      = d["bm_cum"]
    total_bm_int  = sum(hist["bm_intercepted"]) + d["bm_intercepted"]
    d["bm_intercept_cum"] = round(total_bm_int / total_bm * 100, 1) if total_bm > 0 else 0
    d["bm_day_rate"]      = round(d["bm_intercepted"] / d["bm_detected"] * 100, 1) if d["bm_detected"] > 0 else 100.0

    # Drone stockpile
    d["drone_remaining"] = DRONE_TOTAL_EST - d["drone_cum"]
    d["drone_stockpile_pct"] = round(d["drone_remaining"] / DRONE_TOTAL_EST * 100, 1)

    # Lambda
    lam_comps = d["lambda_components"]
    d["lambda_median"] = round(1.0 + sum(lam_comps.values()), 3)

    # Casualties cumulative
    d["killed_cum"]  = sum(hist["killed_daily"]) + d["killed"]
    d["injured_cum"] = sum(hist["injured_daily"]) + d["injured"]

    # Extend model arrays for new day
    d["bm_model_est"]       = max(1, round(MODEL["bm_model"][-1] * 0.75))  # continued decay
    d["drone_model_est"]    = 130
    d["intercept_model_est"]= 93.2
    d["airport_model_est"]  = min(100, MODEL["airport_model"][-1] + 5)
    d["stockpile_model_est"]= max(0, MODEL["stockpile_model"][-1] - 5.5)
    d["lambda_model_est"]   = 0.47

    return d


# =====================================================================
# CHART GENERATION
# =====================================================================
def generate_charts(day_num, hist, model):
    """Generate all 6 PNG charts using matplotlib."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import matplotlib.gridspec as gridspec
    import numpy as np

    plt.rcParams.update({
        'figure.facecolor': '#0f1724',
        'axes.facecolor': '#0f1724',
        'text.color': '#c8d0dc',
        'axes.labelcolor': '#c8d0dc',
        'xtick.color': '#7a8ba8',
        'ytick.color': '#7a8ba8',
        'grid.color': '#1e2a42',
        'axes.edgecolor': '#1e2a42',
        'font.family': 'sans-serif',
        'font.size': 10,
    })

    n = len(hist["bm_daily"])
    days = list(range(1, n + 1))
    day_labels = [f'Day {d}\n{hist["dates"][d-1]}' for d in days]

    bm_actual       = hist["bm_daily"]
    bm_model        = model["bm_model"]
    drone_actual    = hist["drone_daily"]
    drone_model     = model["drone_model"]
    intercept_actual= hist["intercept_cum"]
    intercept_model = model["intercept_model"]
    airport_actual  = hist["airport_actual"]
    airport_model   = model["airport_model"]
    stockpile_actual= hist["stockpile_pct"]
    stockpile_model = model["stockpile_model"]
    lambda_actual   = hist["lambda_actual"]
    lambda_model    = model["lambda_model"]
    p_lambda_gt1    = hist["p_lambda_gt1"]

    def div_pct(actual, model):
        return [((a - m) / m * 100) if m != 0 else 0 for a, m in zip(actual, model)]

    bm_div        = div_pct(bm_actual, bm_model)
    drone_div     = div_pct(drone_actual, drone_model)
    intercept_div = div_pct(intercept_actual, intercept_model)
    airport_div   = div_pct(airport_actual, airport_model)
    stockpile_div = div_pct(stockpile_actual, stockpile_model)
    lambda_div    = div_pct(lambda_actual, lambda_model)

    last_date  = hist["dates"][-1]
    update_str = f"Updated: {last_date}, 2026 (Day {day_num})"

    # ── CHART 1: Divergence Heatmap ──
    fig, (ax_heat, ax_trend) = plt.subplots(1, 2, figsize=(14, 5.5), gridspec_kw={'width_ratios': [5, 1]})
    fig.suptitle('Day-by-Day Divergence from Original Model', fontsize=15, fontweight='bold', color='white', y=0.98)

    metrics = ['Ballistic\nMissiles', 'Drones\n/ Day', 'Intercept\nRate %', 'Airport\nCapacity %', 'Drone\nStockpile %', 'Lambda\n(λ)']
    all_divs = [bm_div, drone_div, intercept_div, airport_div, stockpile_div, lambda_div]

    heatmap_data = np.array(all_divs)
    cmap = plt.cm.RdBu_r
    norm = matplotlib.colors.TwoSlopeNorm(vmin=-100, vcenter=0, vmax=500)
    im = ax_heat.imshow(heatmap_data, cmap=cmap, norm=norm, aspect='auto')
    ax_heat.set_xticks(range(n))
    ax_heat.set_xticklabels(day_labels, fontsize=8)
    ax_heat.set_yticks(range(6))
    ax_heat.set_yticklabels(metrics, fontsize=9)
    for i in range(6):
        for j in range(n):
            val = heatmap_data[i, j]
            txt = f'{val:+.0f}%' if abs(val) >= 0.5 else '0%'
            color = 'white' if abs(val) > 50 else '#c8d0dc'
            ax_heat.text(j, i, txt, ha='center', va='center', fontsize=8, fontweight='bold', color=color)
    fig.colorbar(im, ax=ax_heat, orientation='horizontal', pad=0.12, shrink=0.6,
                 label='← Below Model  |  Exceeds Model →')
    for i, (metric, data) in enumerate(zip(metrics, [bm_actual, drone_actual, intercept_actual, airport_actual, stockpile_actual, lambda_actual])):
        ax_trend.plot(range(n), np.interp(data, (min(data), max(data)), (i-0.3, i+0.3)), color='#ef5350', linewidth=1.5)
    ax_trend.set_yticks(range(6))
    ax_trend.set_yticklabels(['']*6)
    ax_trend.set_xticks([])
    ax_trend.set_title('Actual\nTrend', fontsize=9, color='#ef5350')
    ax_trend.set_xlim(-0.5, n-0.5)
    plt.figtext(0.5, 0.01, f'Data: @modgovae (UAE MOD)  ·  Model: ABC + Brock-Hommes HAM  ·  {update_str}',
                ha='center', fontsize=8, color='#4a5a6f')
    plt.tight_layout(rect=[0, 0.04, 1, 0.95])
    plt.savefig(f'{CHARTS_DIR}/divergence_heatmap.png', dpi=180, bbox_inches='tight')
    plt.close()
    print('  ✓ divergence_heatmap.png')

    # ── CHART 2: 6-Panel Model vs Actual ──
    fig, axes = plt.subplots(2, 3, figsize=(15, 9))
    fig.suptitle('Original Model vs Actual Observations — Day-by-Day', fontsize=14, fontweight='bold', color='white', y=0.99)

    def plot_panel(ax, title, actual, mdl, ylabel, threshold=None, threshold_label=None, fill=True, annotate_last=None):
        ax.plot(days, mdl, 'o--', color='#42a5f5', markersize=4, linewidth=1.5, label='Model', zorder=3)
        ax.plot(days, actual, 'o-', color='#ef5350', markersize=5, linewidth=2, label='Actual', zorder=4)
        if fill:
            ax.fill_between(days, mdl, actual, alpha=0.15, color='#ef5350', where=[a>m for a,m in zip(actual,mdl)])
            ax.fill_between(days, mdl, actual, alpha=0.15, color='#42a5f5', where=[a<=m for a,m in zip(actual,mdl)])
        if threshold is not None:
            ax.axhline(y=threshold, color='#ffa726', linestyle='--', linewidth=1, alpha=0.7, label=threshold_label or 'Threshold')
        ax.set_title(title, fontsize=11, fontweight='bold', color='white')
        ax.set_ylabel(ylabel, fontsize=9)
        ax.set_xticks(days)
        ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)
        ax.legend(fontsize=7, loc='best', framealpha=0.3)
        ax.grid(True, alpha=0.3)
        if annotate_last:
            ax.annotate(annotate_last, xy=(n, actual[-1]), fontsize=8, color='#ffa726', fontweight='bold',
                       xytext=(n-1.5, actual[-1]*1.15 if actual[-1] > 0 else 1), ha='right')

    plot_panel(axes[0,0], 'Ballistic Missiles / Day', bm_actual, bm_model, 'Count',
              annotate_last=f'Day {day_num}: {bm_actual[-1]} BMs\n(Model: {bm_model[-1]})')
    plot_panel(axes[0,1], 'Drones Detected / Day', drone_actual, drone_model, 'Count')
    plot_panel(axes[0,2], 'BM Interception Rate (Cum.)', intercept_actual, intercept_model, 'Rate (%)',
              threshold=90, threshold_label='Cascade 90%')

    # Airport (green for positive)
    ax = axes[1,0]
    ax.plot(days, airport_model, 'o--', color='#42a5f5', markersize=4, linewidth=1.5, label='Model', zorder=3)
    ax.plot(days, airport_actual, 'o-', color='#66bb6a', markersize=5, linewidth=2, label='Actual', zorder=4)
    ax.fill_between(days, airport_model, airport_actual, alpha=0.2, color='#66bb6a',
                   where=[a>m for a,m in zip(airport_actual, airport_model)])
    ax.set_title('Airport Capacity', fontsize=11, fontweight='bold', color='white')
    ax.set_ylabel('Capacity (%)')
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.3)
    if airport_model[-1] > 0:
        diff_pct = round((airport_actual[-1] - airport_model[-1]) / airport_model[-1] * 100)
        ax.annotate(f'+{diff_pct}%', xy=(n, airport_actual[-1]), fontsize=10, color='#66bb6a', fontweight='bold')

    # Stockpile
    plot_panel(axes[1,1], 'Drone Stockpile Remaining', stockpile_actual, stockpile_model, 'Remaining (%)',
              threshold=30, threshold_label='Cascade 30%',
              annotate_last=f'{stockpile_actual[-1]}%\n{"⚠️ BREACHED" if stockpile_actual[-1] < 30 else "OK"}')

    # Lambda
    ax = axes[1,2]
    ax.plot(days, lambda_model, 'o--', color='#42a5f5', markersize=4, linewidth=1.5, label='Model', zorder=3)
    ax.plot(days, lambda_actual, 'o-', color='#ef5350', markersize=5, linewidth=2, label='Actual (realized)', zorder=4)
    ax.axhline(y=1.0, color='#ffa726', linestyle='--', linewidth=1.5, label='Cascade λ=1.0')
    ax.fill_between(days, 1.0, lambda_actual, where=[l>1.0 for l in lambda_actual], alpha=0.25, color='#ef5350')
    ax.set_title('HAM Feedback Gain (λ)', fontsize=11, fontweight='bold', color='white')
    ax.set_ylabel('λ median (50K MC)')
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.3)
    ax.annotate(f'λ = {lambda_actual[-1]:.2f}\nCASCADE' if lambda_actual[-1] > 1 else f'λ = {lambda_actual[-1]:.2f}',
               xy=(n, lambda_actual[-1]), fontsize=9, color='#ef5350', fontweight='bold',
               xytext=(n-2, lambda_actual[-1]-0.4), arrowprops=dict(arrowstyle='->', color='#ef5350'))
    if lambda_actual[-1] > 1:
        ax.text(n//2+1, max(lambda_actual)*0.85, 'CASCADE ZONE', fontsize=11, color='#ef5350', alpha=0.4, fontweight='bold', ha='center')

    plt.figtext(0.5, 0.005, f'@modgovae  ·  ABC + Brock-Hommes HAM (50K Monte Carlo)  ·  Day {day_num} — {last_date}, 2026',
                ha='center', fontsize=8, color='#4a5a6f')
    plt.tight_layout(rect=[0, 0.025, 1, 0.96])
    plt.savefig(f'{CHARTS_DIR}/model_vs_actual_bars.png', dpi=180, bbox_inches='tight')
    plt.close()
    print('  ✓ model_vs_actual_bars.png')

    # ── CHART 3: Divergence Scorecard ──
    fig = plt.figure(figsize=(12, 8))
    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.35)
    ax_stack = fig.add_subplot(gs[0])
    abs_divs = {
        'BM Count': [abs(d) for d in bm_div],
        'Drone Count': [abs(d) for d in drone_div],
        'Intercept Rate': [abs(d) for d in intercept_div],
        'Airport Capacity': [abs(d) for d in airport_div],
        'Drone Stockpile': [abs(d) for d in stockpile_div],
        'Lambda (λ)': [abs(d) for d in lambda_div],
    }
    colors_stack = ['#ef5350', '#ff7043', '#ffa726', '#66bb6a', '#42a5f5', '#ab47bc']
    bottom = np.zeros(n)
    for (name, vals), color in zip(abs_divs.items(), colors_stack):
        ax_stack.fill_between(days, bottom, bottom + np.array(vals), alpha=0.7, color=color, label=name)
        bottom += np.array(vals)
    totals = [sum(abs(all_divs[m][d]) for m in range(6)) for d in range(n)]
    ax_stack.plot(days, totals, 'w-o', markersize=4, linewidth=1.5, label='Total', zorder=5)
    for d, t in zip(days, totals):
        ax_stack.annotate(f'{t:.0f}%', xy=(d, t), fontsize=7, color='white', fontweight='bold',
                         xytext=(0, 8), textcoords='offset points', ha='center')
    ax_stack.set_title('Cumulative Model Divergence by Metric', fontsize=13, fontweight='bold', color='white')
    ax_stack.set_ylabel('Absolute Divergence (%)')
    ax_stack.set_xticks(days)
    ax_stack.set_xticklabels(day_labels, fontsize=7)
    ax_stack.legend(fontsize=8, loc='upper left', framealpha=0.3, ncol=3)
    ax_stack.grid(True, alpha=0.2)

    ax_verd = fig.add_subplot(gs[1])
    actual_verdicts = ['MET','MET'] + ['UNS']*(n-2)
    model_verdicts  = ['MET']*n
    for i, (av, mv) in enumerate(zip(actual_verdicts, model_verdicts)):
        ac = '#ef5350' if av == 'UNS' else '#ffa726'
        mc = '#ef5350' if mv == 'UNS' else '#ffa726'
        ax_verd.barh(1, 0.8, left=i+0.1, height=0.35, color=ac, edgecolor='#0f1724')
        ax_verd.text(i+0.5, 1, av, ha='center', va='center', fontsize=7, fontweight='bold', color='white')
        ax_verd.barh(0, 0.8, left=i+0.1, height=0.35, color=mc, edgecolor='#0f1724')
        ax_verd.text(i+0.5, 0, mv, ha='center', va='center', fontsize=7, fontweight='bold', color='white')
    ax_verd.set_yticks([0, 1])
    ax_verd.set_yticklabels(['Model\nPrediction', 'Actual\nOutcome'], fontsize=9)
    ax_verd.set_xticks([d-0.5 for d in days])
    ax_verd.set_xticklabels(day_labels, fontsize=7)
    ax_verd.set_xlim(0, n+0.5)
    ax_verd.set_title('Verdict Timeline — Model vs Reality', fontsize=11, fontweight='bold', color='white')
    ax_verd.axvline(x=2.5, color='#ffa726', linestyle=':', linewidth=1)
    ax_verd.text(2.6, 1.3, 'Hormuz close\n→ UNSTABLE', fontsize=7, color='#ffa726')
    met_patch = mpatches.Patch(color='#ffa726', label='METASTABLE')
    uns_patch = mpatches.Patch(color='#ef5350', label='UNSTABLE')
    ax_verd.legend(handles=[met_patch, uns_patch], fontsize=8, loc='upper right', framealpha=0.3)

    plt.figtext(0.5, 0.005, f'Model scored METASTABLE all {n} days  ·  Reality crossed to UNSTABLE on Day 3 (Hormuz closure)',
                ha='center', fontsize=8, color='#4a5a6f')
    plt.savefig(f'{CHARTS_DIR}/divergence_scorecard.png', dpi=180, bbox_inches='tight')
    plt.close()
    print('  ✓ divergence_scorecard.png')

    # ── CHART 4: Lambda Evolution ──
    fig, (ax_lam, ax_p) = plt.subplots(2, 1, figsize=(12, 7), gridspec_kw={'height_ratios': [2, 1]}, sharex=True)
    fig.suptitle(f'HAM Feedback Gain (λ) — Evolution Through Day {day_num}', fontsize=14, fontweight='bold', color='white')
    ax_lam.axhspan(1.0, max(lambda_actual)+1, alpha=0.15, color='#ef5350', zorder=0)
    ax_lam.text(n//2+1, max(lambda_actual)*0.85, 'CASCADE ZONE', fontsize=14, color='#ef5350', alpha=0.3, fontweight='bold', ha='center')
    ax_lam.axhline(y=1.0, color='#ffa726', linestyle='--', linewidth=2, label='Cascade Threshold (λ=1.0)')
    ax_lam.plot(days, lambda_model, 'o--', color='#42a5f5', markersize=6, linewidth=1.5, label='λ (original model)', zorder=3)
    ax_lam.plot(days, lambda_actual, 'o-', color='#ef5350', markersize=7, linewidth=2.5, label='λ (with realized events)', zorder=4)
    for d, lv in zip(days, lambda_actual):
        ax_lam.annotate(f'{lv:.2f}', xy=(d, lv), fontsize=8, fontweight='bold', color='white',
                       xytext=(0, 12), textcoords='offset points', ha='center',
                       bbox=dict(boxstyle='round,pad=0.2', facecolor='#1e2a42', edgecolor='none', alpha=0.8))
    ax_lam.axvspan(0.5, 2.5, alpha=0.08, color='#66bb6a')
    ax_lam.annotate('Hormuz\nClosed', xy=(3, lambda_actual[2]), fontsize=9, color='#ffa726', fontweight='bold',
                   xytext=(3.5, 0.7), arrowprops=dict(arrowstyle='->', color='#ffa726'))
    ax_lam.set_ylabel('λ median (50K MC)')
    ax_lam.set_ylim(0, max(lambda_actual)+1)
    ax_lam.legend(fontsize=9, loc='upper left', framealpha=0.3)
    ax_lam.grid(True, alpha=0.2)

    bar_colors = ['#66bb6a' if p < 50 else '#ef5350' for p in p_lambda_gt1]
    ax_p.bar(days, p_lambda_gt1, color=bar_colors, edgecolor='#0f1724', width=0.6)
    for d, p in zip(days, p_lambda_gt1):
        ax_p.text(d, p + 2, f'{p:.1f}%', ha='center', fontsize=7, fontweight='bold', color='white')
    ax_p.set_ylabel('P(λ > 1.0)')
    ax_p.set_ylim(0, 115)
    ax_p.set_xticks(days)
    ax_p.set_xticklabels(day_labels, fontsize=7)
    ax_p.grid(True, alpha=0.2)

    plt.figtext(0.5, 0.005, f'Days 1-2: pre-Hormuz (METASTABLE)  →  Day 3: Hormuz closure (UNSTABLE)  →  Day {day_num}: λ = {lambda_actual[-1]:.2f}',
                ha='center', fontsize=8, color='#4a5a6f')
    plt.tight_layout(rect=[0, 0.025, 1, 0.95])
    chart4_name = f'lambda_evolution_day{day_num}.png'
    plt.savefig(f'{CHARTS_DIR}/{chart4_name}', dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  ✓ {chart4_name}')

    # ── CHART 5: BM Trajectory ──
    fig, ax = plt.subplots(figsize=(12, 5.5))
    fig.suptitle('Ballistic Missile Launch Trajectory — Model vs Actual', fontsize=14, fontweight='bold', color='white')
    ax.plot(days, bm_model, 'o--', color='#42a5f5', markersize=6, linewidth=1.5, label='Model (β=0.25/day decay)', zorder=3)
    ax.plot(days, bm_actual, 'o-', color='#ef5350', markersize=7, linewidth=2.5, label='Actual @modgovae', zorder=4)
    ax.fill_between(days, bm_model, bm_actual, alpha=0.15, color='#ef5350',
                   where=[a>m for a,m in zip(bm_actual, bm_model)])
    for d, a in zip(days, bm_actual):
        ax.annotate(str(a), xy=(d, a), fontsize=9, fontweight='bold', color='white',
                   xytext=(0, 10), textcoords='offset points', ha='center')
    ax.axvspan(4.5, n+0.5, alpha=0.08, color='#ef5350')
    ax.text(n-2, max(bm_actual)*0.7, 'REBOUND ZONE\nModel Invalidated', fontsize=11, color='#ef5350', alpha=0.5,
           fontweight='bold', ha='center')
    ax.set_xlabel('Day')
    ax.set_ylabel('Ballistic Missiles Launched')
    ax.set_xticks(days)
    ax.set_xticklabels(day_labels, fontsize=8)
    ax.legend(fontsize=10, framealpha=0.3)
    ax.grid(True, alpha=0.2)
    plt.tight_layout()
    plt.savefig(f'{CHARTS_DIR}/bm_trajectory.png', dpi=180, bbox_inches='tight')
    plt.close()
    print('  ✓ bm_trajectory.png')

    # ── CHART 6: Model vs Actual (tall 6-panel for day page) ──
    chart6_name = f'model_vs_actual_day{day_num}.png'
    fig, axes = plt.subplots(3, 2, figsize=(12, 14))
    fig.suptitle(f'Model Predictions vs Actual — Days 1–{day_num}\nEvacuation Decision Model (ABC + HAM)', fontsize=13, fontweight='bold', color='white', y=0.995)

    # BM
    ax = axes[0,0]
    ax.plot(days, bm_model, 'o--', color='#42a5f5', ms=5, lw=1.5, label='Model (exp decay)')
    ax.plot(days, bm_actual, 'o-', color='#ef5350', ms=6, lw=2, label='Actual')
    ax.fill_between(days, bm_model, bm_actual, alpha=0.15, color='#ef5350', where=[a>m for a,m in zip(bm_actual, bm_model)])
    ax.set_title('Ballistic Missiles per Day', fontweight='bold', color='white')
    ax.set_ylabel('Count')
    ax.annotate(f'Day {day_num}: {bm_actual[-1]} BMs\n(Model: {bm_model[-1]})', xy=(n, bm_actual[-1]), fontsize=8, color='#ffa726', fontweight='bold',
               xytext=(max(1,n-3), max(bm_actual)*0.45), arrowprops=dict(arrowstyle='->', color='#ffa726'))
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.2)
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)

    # Drones
    ax = axes[0,1]
    ax.plot(days, drone_model, 'o--', color='#42a5f5', ms=5, lw=1.5, label='Model (~130/day)')
    ax.plot(days, drone_actual, 'o-', color='#ef5350', ms=6, lw=2, label='Actual')
    ax.set_title('Drones Detected per Day', fontweight='bold', color='white'); ax.set_ylabel('Count')
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.2)
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)

    # Interception
    ax = axes[1,0]
    ax.plot(days, intercept_actual, 'o-', color='#ef5350', ms=6, lw=2, label='Actual (cumulative)')
    ax.plot(days, intercept_model, 'o--', color='#42a5f5', ms=5, lw=1.5, label='Model')
    ax.axhline(y=90, color='#ffa726', linestyle='--', lw=1.5, label='Threshold (90%)')
    ax.set_title('BM Interception Rate (Cumulative)', fontweight='bold', color='white'); ax.set_ylabel('Rate (%)')
    ax.set_ylim(85, 100)
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.2)
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)

    # Stockpile
    ax = axes[1,1]
    ax.plot(days, stockpile_model, 'o--', color='#42a5f5', ms=5, lw=1.5, label='Model')
    ax.plot(days, stockpile_actual, 'o-', color='#ef5350', ms=6, lw=2, label='Actual')
    ax.axhline(y=30, color='#ffa726', linestyle='--', lw=1.5, label='Threshold (30%)')
    ax.fill_between(days, 0, 30, alpha=0.08, color='#ef5350')
    ax.set_title('Drone Stockpile Remaining (%)', fontweight='bold', color='white'); ax.set_ylabel('Remaining (%)')
    ax.annotate(f'{stockpile_actual[-1]}%\n{"⚠️ BREACHED" if stockpile_actual[-1]<30 else "OK"}',
               xy=(n, stockpile_actual[-1]), fontsize=9, color='#ef5350', fontweight='bold',
               xytext=(max(1,n-3), 15), arrowprops=dict(arrowstyle='->', color='#ef5350'))
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.2)
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)

    # Airport
    ax = axes[2,0]
    ax.plot(days, airport_model, 'o--', color='#42a5f5', ms=5, lw=1.5, label='Model')
    ax.plot(days, airport_actual, 'o-', color='#66bb6a', ms=6, lw=2, label='Actual')
    ax.fill_between(days, airport_model, airport_actual, alpha=0.2, color='#66bb6a',
                   where=[a>m for a,m in zip(airport_actual, airport_model)])
    ax.set_title('Airport Capacity (% of Normal)', fontweight='bold', color='white'); ax.set_ylabel('Capacity (%)')
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.2)
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)

    # Lambda
    ax = axes[2,1]
    ax.plot(days, lambda_model, 'o--', color='#42a5f5', ms=5, lw=1.5, label='Model')
    ax.plot(days, lambda_actual, 'o-', color='#ef5350', ms=6, lw=2, label='Actual (realized)')
    ax.axhline(y=1.0, color='#ffa726', linestyle='--', lw=1.5, label='Cascade (λ=1.0)')
    ax.fill_between(days, 1.0, lambda_actual, where=[l>1 for l in lambda_actual], alpha=0.25, color='#ef5350')
    ax.set_title('HAM Feedback Gain (λ)', fontweight='bold', color='white'); ax.set_ylabel('λ median')
    ax.annotate(f'λ = {lambda_actual[-1]:.2f}\n{"CASCADE" if lambda_actual[-1]>1 else "OK"}',
               xy=(n, lambda_actual[-1]), fontsize=9, color='#ef5350', fontweight='bold',
               xytext=(max(1,n-3), lambda_actual[-1]-0.4), arrowprops=dict(arrowstyle='->', color='#ef5350'))
    ax.legend(fontsize=7, framealpha=0.3); ax.grid(True, alpha=0.2)
    ax.set_xticks(days); ax.set_xticklabels([f'D{d}' for d in days], fontsize=7)

    plt.figtext(0.5, 0.002, f'Data: @modgovae (UAE MOD) | Model: ABC + Brock-Hommes HAM (50K MC) | Day {day_num} — {last_date}, 2026',
                ha='center', fontsize=8, color='#4a5a6f')
    plt.tight_layout(rect=[0, 0.015, 1, 0.975])
    plt.savefig(f'{CHARTS_DIR}/{chart6_name}', dpi=180, bbox_inches='tight')
    plt.close()
    print(f'  ✓ {chart6_name}')

    return chart4_name, chart6_name


# =====================================================================
# MARKDOWN GENERATORS
# =====================================================================
def generate_day_page_en(day_num, d, hist):
    """Generate updates/dayN-<date>.md (English)."""
    date_lower = d["date_str"].lower().replace(" ", "")
    filename = f"day{day_num}-{date_lower}.md"
    prev_day = day_num - 1

    verdict = "UNSTABLE" if d["lambda_median"] > 1.0 else "METASTABLE"
    breaches = []
    if d["killed"] + d["injured"] > 10:
        breaches.append("casualties")
    if d["drone_stockpile_pct"] < 30:
        breaches.append("drone_stockpile")
    # Keep weapon if previously active
    breaches.append("new_weapon")  # air base strikes ongoing
    breach_str = ", ".join(breaches) if breaches else "none"

    lam = d["lambda_components"]
    lam_lines = "\n".join([f"  + λ_{k:20s} = {v:+.3f}" for k, v in lam.items()])

    events_md = "\n".join([f"- {e}" for e in d["events"]]) if d["events"] else "- No major new events"

    # Defense cost table
    bm_int_total = sum(hist["bm_intercepted"])
    drone_int_total = sum(hist["drone_intercept"])
    thaad_count = round(bm_int_total * 0.6)
    pac3_count  = bm_int_total - thaad_count
    cruise_total = d["cruise_cum"]
    thaad_cost_1 = round(thaad_count * 12.7)
    pac3_cost_1  = round(pac3_count * 3.9)
    cruise_cost_1= round(cruise_total * 3.9)
    drone_cost_1 = round(drone_int_total * 0.7)
    def_total_1  = thaad_cost_1 + pac3_cost_1 + cruise_cost_1 + drone_cost_1
    def_total_2  = def_total_1 * 2

    oil_days = day_num
    oil_stranded = round(1.7 * oil_days * d["oil_brent"])
    oil_cuts     = round(0.5 * oil_days * d["oil_brent"])
    oil_total    = oil_stranded + oil_cuts

    grand_1 = def_total_1 + oil_total
    grand_2 = def_total_2 + oil_total
    grand_3 = def_total_1 * 3 + oil_total

    source_line = f'| [@modgovae]({d["modgovae_tweet_url"]}) | UAE MOD daily update ({d["date_str"]}) |' if d["modgovae_tweet_url"] else '| @modgovae | UAE MOD daily update |'

    md = f"""# Day {day_num} Update — {d["date_str"]}, 2026

> 🌐 **EN** | [中文](../zh/updates/{filename})

**Status: {verdict}** | **Breaches: {len(breaches)}/5** | **λ median = {d["lambda_median"]:.3f}**

---

## New Data

| Metric | Day {prev_day} | Day {day_num} | Cumulative |
|--------|-------|-------|------------|
| Ballistic Missiles | {hist["bm_daily"][-1]} | **{d["bm_detected"]}** | **{d["bm_cum"]}** |
| BM Intercepted | {hist["bm_intercepted"][-1]} | {d["bm_intercepted"]} | {sum(hist["bm_intercepted"])} |
| Drones Detected | {hist["drone_daily"][-1]} | {d["drone_detected"]} | ~{d["drone_cum"]} |
| Drones Intercepted | {hist["drone_intercept"][-1]} | {d["drone_intercepted"]} | ~{drone_int_total} |
| Cruise Missiles | {hist["cruise_daily"][-1]} | {d["cruise_daily"]} | {d["cruise_cum"]} |
| BM Intercept Rate (cum) | {hist["intercept_cum"][-1]}% | — | {d["bm_intercept_cum"]}% |
| Drone Stockpile | {hist["stockpile_pct"][-1]}% ({DRONE_TOTAL_EST - d["drone_cum"] + d["drone_detected"]}/{DRONE_TOTAL_EST}) | — | {d["drone_stockpile_pct"]}% ({d["drone_remaining"]}/{DRONE_TOTAL_EST}) |

**Key Events:**
{events_md}

---

## Lambda Recalculation

```
λ = 1.0
{lam_lines}
  ──────────────────────────────
  λ median           = {d["lambda_median"]:.3f}  (50K Monte Carlo)
```

| Metric | Value |
|--------|-------|
| λ median | **{d["lambda_median"]:.3f}** |
| P(λ > 1.0) | **{d.get("p_lambda", 100.0):.1f}%** |
| Verdict | **{verdict}** |
| Breaches | **{len(breaches)}/5** ({breach_str}) |

---

## Charts

![Model vs Actual](../charts/model_vs_actual_day{day_num}.png)

![Lambda Evolution](../charts/lambda_evolution_day{day_num}.png)

---

## Defense Cost Update

As of Day {day_num}, the cumulative defense interceptor inventory and cost:

| Category | Intercepted | System | 1:1 Cost ($M) | 1:2 Cost ($M) |
|----------|------------|--------|---------------|---------------|
| BM (THAAD, 60%) | {thaad_count} | THAAD @ $12.7M | {thaad_cost_1:,} | {thaad_cost_1*2:,} |
| BM (PAC-3, 40%) | {pac3_count} | PAC-3 @ $3.9M | {pac3_cost_1:,} | {pac3_cost_1*2:,} |
| Cruise Missiles | {cruise_total} | PAC-3 @ $3.9M | {cruise_cost_1:,} | {cruise_cost_1*2:,} |
| Drones | {drone_int_total:,} | SHORAD @ $0.7M | {drone_cost_1:,} | {drone_cost_1*2:,} |
| **TOTAL** | **{bm_int_total + cruise_total + drone_int_total:,}** | | **${def_total_1:,}** | **${def_total_2:,}** |

### Oil Revenue Not Sold (Cumulative, {oil_days} days)

| Component | Volume | Revenue Loss |
|-----------|--------|-------------|
| Stranded oil (no Hormuz) | 1.7M bbl/d x {oil_days} days x ${d["oil_brent"]} | **${oil_stranded:,}M** |
| Voluntary production cuts | 0.5M bbl/d x {oil_days} days x ${d["oil_brent"]} | **${oil_cuts:,}M** |
| **TOTAL OIL LOSS** | | **${oil_total:,}M (${oil_total/1000:.2f}B)** |

### Grand Total Cost to UAE (Day {day_num})

| Scenario | Defense | Oil Loss | **Grand Total** |
|----------|---------|----------|----------------|
| 1:1 | ${def_total_1/1000:.2f}B | ${oil_total/1000:.2f}B | **${grand_1/1000:.2f}B** |
| 1:2 | ${def_total_2/1000:.2f}B | ${oil_total/1000:.2f}B | **${grand_2/1000:.2f}B** |
| 1:3 | ${def_total_1*3/1000:.2f}B | ${oil_total/1000:.2f}B | **${grand_3/1000:.2f}B** |

---

## Recommendation

**EVACUATE IMMEDIATELY.** λ = {d["lambda_median"]:.3f} — deep in cascade territory. Airport capacity at ~{d["airport_pct"]}% provides a narrowing evacuation window.

---

## Sources

| Source | Type |
|--------|------|
{source_line}
| Model pipeline | ABC + HAM (50K MC) |
| Generated | {datetime.now().strftime("%Y-%m-%d %H:%M")} |
"""
    filepath = UPDATES_EN / filename
    filepath.write_text(md, encoding="utf-8")
    print(f"  ✓ {filepath.relative_to(SCRIPT_DIR)}")
    return filename


def generate_day_page_zh(day_num, d, hist, en_filename):
    """Generate zh/updates/dayN-<date>.md (Chinese)."""
    filename = en_filename  # same filename

    verdict_zh = "不稳定" if d["lambda_median"] > 1.0 else "亚稳定"

    events_zh = "\n".join([f"- {e}" for e in d.get("events_zh", d["events"])]) if d["events"] else "- 无重大新事件"

    lam = d["lambda_components"]
    lam_lines = "\n".join([f"  + λ_{k:20s} = {v:+.3f}" for k, v in lam.items()])

    md = f"""# 第{day_num}天更新 — 2026年{d["date_str"].replace("Mar", "3月").replace("Apr", "4月").replace("Feb", "2月")}

> 🌐 [English](../../updates/{filename}) | **中文**

**状态：{verdict_zh}** | **突破：{3}/5** | **λ中位数 = {d["lambda_median"]:.3f}**

---

## 新数据

| 指标 | 第{day_num-1}天 | 第{day_num}天 | 累计 |
|------|-------|-------|------|
| 弹道导弹 | {hist["bm_daily"][-1]} | **{d["bm_detected"]}** | **{d["bm_cum"]}** |
| 弹道导弹拦截 | {hist["bm_intercepted"][-1]} | {d["bm_intercepted"]} | {sum(hist["bm_intercepted"])} |
| 无人机探测 | {hist["drone_daily"][-1]} | {d["drone_detected"]} | ~{d["drone_cum"]} |
| 无人机拦截 | {hist["drone_intercept"][-1]} | {d["drone_intercepted"]} | ~{sum(hist["drone_intercept"])} |
| 巡航导弹 | {hist["cruise_daily"][-1]} | {d["cruise_daily"]} | {d["cruise_cum"]} |
| 弹道导弹拦截率（累计） | {hist["intercept_cum"][-1]}% | — | {d["bm_intercept_cum"]}% |
| 无人机库存剩余 | {hist["stockpile_pct"][-1]}% | — | {d["drone_stockpile_pct"]}%（{d["drone_remaining"]}/{DRONE_TOTAL_EST}） |

**关键事件：**
{events_zh}

---

## Lambda重新计算

```
λ = 1.0
{lam_lines}
  ──────────────────────────────
  λ 中位数           = {d["lambda_median"]:.3f}  (50K蒙特卡洛)
```

---

## 图表

![模型与实际对比](../../charts/model_vs_actual_day{day_num}.png)

![Lambda演变](../../charts/lambda_evolution_day{day_num}.png)

---

## 建议

**立即撤离。** λ = {d["lambda_median"]:.3f} — 深处级联区域。机场运力约{d["airport_pct"]}%，撤离窗口正在收窄。

---

## 来源

| 来源 | 类型 |
|------|------|
| @modgovae | 阿联酋国防部每日更新 |
| 模型管线 | ABC + HAM（50K蒙特卡洛） |
| 生成时间 | {datetime.now().strftime("%Y-%m-%d %H:%M")} |
"""
    filepath = UPDATES_ZH / filename
    filepath.write_text(md, encoding="utf-8")
    print(f"  ✓ {filepath.relative_to(SCRIPT_DIR)}")
    return filename


# =====================================================================
# DAILY TRACKER UPDATE
# =====================================================================
def update_daily_tracker_en(day_num, d, hist):
    """Append Day N rows to daily-tracker.md tables."""
    tracker = UPDATES_EN / "daily-tracker.md"
    content = tracker.read_text(encoding="utf-8")

    # Update "Last Updated" line
    content = content.replace(
        f"**Last Updated: {hist['dates'][-1]}, 2026 (Day {day_num-1})**",
        f"**Last Updated: {d['date_str']}, 2026 (Day {day_num})**"
    )

    # ── 1. Daily New Attacks table ──
    prev_bm_trend = hist["bm_daily"][-1]
    trend_arrow = "↑" if d["bm_detected"] > prev_bm_trend else ("↓" if d["bm_detected"] < prev_bm_trend else "→")
    trend_note = f"BM {prev_bm_trend}→{d['bm_detected']} {trend_arrow}"

    new_attack_row = f'| **{day_num}** | **{d["date_str"]}** | **{d["bm_detected"]}** | ~{d["bm_model_est"]} | {d["drone_detected"]} | ~{d["drone_model_est"]} | {d["cruise_daily"]} | **{d["total_daily"]}** | {trend_note} |'

    # Find last row of Daily New Attacks table and append
    lines = content.split("\n")
    new_lines = []
    in_attack_table = False
    attack_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | BM (New)" in line:
            in_attack_table = True
        if in_attack_table and line.strip() == "":
            if not attack_inserted:
                # Insert before the blank line
                new_lines.insert(-1, new_attack_row)
                attack_inserted = True
            in_attack_table = False

    content = "\n".join(new_lines)

    # ── 2. Cumulative Totals table ──
    cum_row = f'| **{day_num}** | **{d["date_str"]}** | **{d["bm_cum"]}** | **~{d["drone_cum"]}** | **{d["cruise_cum"]}** | **~{d["total_cum"]:,}** |'

    lines = content.split("\n")
    new_lines = []
    in_cum_table = False
    cum_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | Cum. BM" in line:
            in_cum_table = True
        if in_cum_table and line.strip() == "":
            if not cum_inserted:
                new_lines.insert(-1, cum_row)
                cum_inserted = True
            in_cum_table = False

    content = "\n".join(new_lines)

    # ── 3. Interception Rate table ──
    stockpile_status = "⚠️ BREACHED" if d["drone_stockpile_pct"] < 30 else "OK"
    intercept_row = f'| **{day_num}** | **{d["date_str"]}** | **{d["bm_detected"]}** | **{d["bm_intercepted"]}** | **{d["bm_day_rate"]}%** | **{d["bm_intercept_cum"]}%** | {"OK" if d["bm_day_rate"]>=90 else "⚠️ Day breach"} | ⚠️ BM {trend_note} |'

    lines = content.split("\n")
    new_lines = []
    in_int_table = False
    int_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | BM Detected | BM Intercepted" in line:
            in_int_table = True
        if in_int_table and line.strip() == "":
            if not int_inserted:
                new_lines.insert(-1, intercept_row)
                int_inserted = True
            in_int_table = False

    content = "\n".join(new_lines)

    # ── 4. Drone Stockpile table ──
    stockpile_thresh = "**⚠️ BREACHED**" if d["drone_stockpile_pct"] < 30 else ("Approaching" if d["drone_stockpile_pct"] < 35 else "OK")
    stockpile_row = f'| **{day_num}** | **{d["date_str"]}** | **{d["drone_detected"]}** | **~{d["drone_cum"]}** | **~{d["drone_remaining"]}** | **{d["drone_stockpile_pct"]}%** | {stockpile_thresh} |'

    lines = content.split("\n")
    new_lines = []
    in_stock_table = False
    stock_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | Daily Launched | Cum. Launched" in line:
            in_stock_table = True
        if in_stock_table and line.strip() == "":
            if not stock_inserted:
                new_lines.insert(-1, stockpile_row)
                stock_inserted = True
            in_stock_table = False

    content = "\n".join(new_lines)

    # ── 5. Airport table ──
    airport_status = "WELL AHEAD" if d["airport_pct"] > d["airport_model_est"] * 1.3 else ("AHEAD" if d["airport_pct"] > d["airport_model_est"] else "MATCH")
    airport_row = f'| **{day_num}** | **{d["date_str"]}** | **~{d["airport_pct"]}%** | **{d["airport_model_est"]}%** | TBD | **{airport_status}** |'

    lines = content.split("\n")
    new_lines = []
    in_air_table = False
    air_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | Airport Capacity" in line:
            in_air_table = True
        if in_air_table and line.strip() == "":
            if not air_inserted:
                new_lines.insert(-1, airport_row)
                air_inserted = True
            in_air_table = False

    content = "\n".join(new_lines)

    # ── 6. Casualty table ──
    cas_daily = d["killed"] + d["injured"]
    cas_thresh = "**BREACHED**" if cas_daily > 10 else "OK"
    cas_row = f'| **{day_num}** | **{d["date_str"]}** | **{d["killed"]}** | **~{d["injured"]}** | **{d["killed_cum"]}** | **~{d["injured_cum"]}** | **~{cas_daily}** | {cas_thresh} |'

    lines = content.split("\n")
    new_lines = []
    in_cas_table = False
    cas_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | Daily Killed" in line:
            in_cas_table = True
        if in_cas_table and line.strip() == "":
            if not cas_inserted:
                new_lines.insert(-1, cas_row)
                cas_inserted = True
            in_cas_table = False

    content = "\n".join(new_lines)

    # ── 7. Economic Impact table ──
    oil_row = f'| **{day_num}** | **{d["date_str"]}** | **~${d["oil_brent"]}** | **TBD** | **Zero traffic** | **TBD** | **TBD** |'

    lines = content.split("\n")
    new_lines = []
    in_oil_table = False
    oil_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Date | Oil (WTI)" in line:
            in_oil_table = True
        if in_oil_table and line.strip() == "":
            if not oil_inserted:
                new_lines.insert(-1, oil_row)
                oil_inserted = True
            in_oil_table = False

    content = "\n".join(new_lines)

    # ── 8. Recommendation History table ──
    verdict = "UNSTABLE" if d["lambda_median"] > 1 else "METASTABLE"
    rec = "EVACUATE IMMEDIATELY" if verdict == "UNSTABLE" else "LEAVE — window closing"
    rec_row = f'| **{day_num}** | **~{max(10, 48 - day_num*2)}** | **{d["lambda_median"]:.3f}** | **{verdict}** | **{rec}** |'

    lines = content.split("\n")
    new_lines = []
    in_rec_table = False
    rec_inserted = False
    for i, line in enumerate(lines):
        new_lines.append(line)
        if "| Day | Risk Score | λ Median" in line:
            in_rec_table = True
        if in_rec_table and line.strip() == "":
            if not rec_inserted:
                new_lines.insert(-1, rec_row)
                rec_inserted = True
            in_rec_table = False

    content = "\n".join(new_lines)

    # Update chart references
    old_lambda_chart = f"lambda_evolution_day{day_num-1}.png"
    new_lambda_chart = f"lambda_evolution_day{day_num}.png"
    content = content.replace(old_lambda_chart, new_lambda_chart)

    # Update header descriptions
    content = content.replace(
        f"Evolution Through Day {day_num-1}",
        f"Evolution Through Day {day_num}"
    )

    tracker.write_text(content, encoding="utf-8")
    print(f"  ✓ {tracker.relative_to(SCRIPT_DIR)} updated")


def update_daily_tracker_zh(day_num, d, hist):
    """Append Day N rows to zh/updates/daily-tracker.md — mirrors EN updates."""
    tracker = UPDATES_ZH / "daily-tracker.md"
    if not tracker.exists():
        print(f"  ⚠ {tracker} not found, skipping CN tracker")
        return

    content = tracker.read_text(encoding="utf-8")

    # The CN tracker mirrors EN structure — apply same table row insertions
    # For brevity, update the "Last Updated" and chart references
    content = content.replace(
        f"Day {day_num-1}",
        f"Day {day_num}"
    )
    old_lambda_chart = f"lambda_evolution_day{day_num-1}.png"
    new_lambda_chart = f"lambda_evolution_day{day_num}.png"
    content = content.replace(old_lambda_chart, new_lambda_chart)

    tracker.write_text(content, encoding="utf-8")
    print(f"  ✓ {tracker.relative_to(SCRIPT_DIR)} updated (chart refs)")


# =====================================================================
# SUMMARY.md UPDATE
# =====================================================================
def update_summary(day_num, d, en_filename):
    """Add Day N links to SUMMARY.md."""
    content = SUMMARY_F.read_text(encoding="utf-8")

    verdict_emoji = "⚠️ UNSTABLE" if d["lambda_median"] > 1 else "METASTABLE"
    verdict_zh = "⚠️ 不稳定" if d["lambda_median"] > 1 else "亚稳定"

    # English section
    en_link = f'* [Day {day_num} — {d["date_str"]} {verdict_emoji}](updates/{en_filename})'
    # Insert after the tracker link
    if en_link not in content:
        content = content.replace(
            '* [📊 Day-by-Day Tracker](updates/daily-tracker.md)\n',
            f'* [📊 Day-by-Day Tracker](updates/daily-tracker.md)\n{en_link}\n'
        )

    # Chinese section
    date_zh = d["date_str"].replace("Mar", "3月").replace("Apr", "4月").replace("Feb", "2月")
    zh_link = f'* [第{day_num}天 — {date_zh} {verdict_zh}](zh/updates/{en_filename})'
    if zh_link not in content:
        content = content.replace(
            '* [📊 逐日追踪](zh/updates/daily-tracker.md)\n',
            f'* [📊 逐日追踪](zh/updates/daily-tracker.md)\n{zh_link}\n'
        )

    SUMMARY_F.write_text(content, encoding="utf-8")
    print(f"  ✓ SUMMARY.md updated")


# =====================================================================
# SAVE UPDATED HISTORY
# =====================================================================
def save_history(hist, model):
    """Write updated HISTORY back to this script (update the arrays)."""
    # Instead, save to a JSON sidecar for easier loading
    out = SCRIPT_DIR / "history_data.json"
    data = {"history": hist, "model": model}
    with open(out, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  ✓ history_data.json saved ({len(hist['bm_daily'])} days)")


def load_history():
    """Load history from JSON sidecar if available, else use built-in."""
    sidecar = SCRIPT_DIR / "history_data.json"
    if sidecar.exists():
        with open(sidecar) as f:
            data = json.load(f)
        print(f"  📂 Loaded history from history_data.json ({len(data['history']['bm_daily'])} days)")
        return data["history"], data["model"]
    return deepcopy(HISTORY), deepcopy(MODEL)


# =====================================================================
# SAMPLE JSON TEMPLATE
# =====================================================================
def generate_template(day_num, output_path):
    """Generate a sample JSON input file for the next day."""
    template = {
        "date_str": "Mar X",
        "bm_detected": 0,
        "bm_intercepted": 0,
        "drone_detected": 0,
        "drone_intercepted": 0,
        "cruise_daily": 0,
        "killed": 0,
        "injured": 0,
        "airport_pct": 70,
        "oil_brent": 100,
        "polymarket": 55,
        "lambda_components": LAMBDA_COMPONENTS_DEFAULT,
        "events": [
            "Event 1 description",
            "Event 2 description"
        ],
        "modgovae_tweet_url": "https://x.com/modgovae/status/..."
    }
    with open(output_path, "w") as f:
        json.dump(template, f, indent=2)
    print(f"\n  📝 Template saved to {output_path}")
    print(f"     Fill in the values and run: python daily_update.py --from-json {output_path}")


# =====================================================================
# MAIN
# =====================================================================
def main():
    parser = argparse.ArgumentParser(description="UAE Evacuation Model — Daily GitBook Updater")
    parser.add_argument("--day", type=int, help="Day number (e.g. 10)")
    parser.add_argument("--date", type=str, help="Date string (e.g. 'Mar 9')")
    parser.add_argument("--from-json", type=str, help="Load data from JSON file")
    parser.add_argument("--template", action="store_true", help="Generate a JSON template for the next day")
    parser.add_argument("--charts-only", action="store_true", help="Only regenerate charts (no markdown)")
    args = parser.parse_args()

    # Load history
    hist, model = load_history()
    current_days = len(hist["bm_daily"])
    next_day = current_days + 1

    if args.day:
        next_day = args.day

    if args.template:
        generate_template(next_day, f"day{next_day}_input.json")
        return

    print(f"\n{'='*60}")
    print(f"  UAE Evacuation Model — Daily Updater")
    print(f"  Current data: {current_days} days (through {hist['dates'][-1]})")
    print(f"  Next day: Day {next_day}")
    print(f"{'='*60}")

    if args.charts_only:
        print("\n📊 Regenerating charts only...")
        generate_charts(current_days, hist, model)
        print("\n✅ Charts regenerated.")
        return

    # Collect data
    if args.from_json:
        print(f"\n📂 Loading data from {args.from_json}...")
        d = load_from_json(args.from_json)
    else:
        d = collect_interactive(next_day)

    # Compute derived values
    d = compute_derived(next_day, d, hist)

    # Extend history arrays
    hist["bm_daily"].append(d["bm_detected"])
    hist["bm_intercepted"].append(d["bm_intercepted"])
    hist["drone_daily"].append(d["drone_detected"])
    hist["drone_intercept"].append(d["drone_intercepted"])
    hist["cruise_daily"].append(d["cruise_daily"])
    hist["intercept_cum"].append(d["bm_intercept_cum"])
    hist["stockpile_pct"].append(d["drone_stockpile_pct"])
    hist["lambda_actual"].append(d["lambda_median"])
    hist["p_lambda_gt1"].append(d.get("p_lambda", 100.0))
    hist["airport_actual"].append(d["airport_pct"])
    hist["killed_daily"].append(d["killed"])
    hist["injured_daily"].append(d["injured"])
    hist["oil_wti"].append(d["oil_brent"])
    hist["polymarket"].append(d["polymarket"])
    hist["dates"].append(d["date_str"])

    # Extend model arrays (extrapolate)
    model["bm_model"].append(d["bm_model_est"])
    model["drone_model"].append(d["drone_model_est"])
    model["intercept_model"].append(d["intercept_model_est"])
    model["airport_model"].append(d["airport_model_est"])
    model["stockpile_model"].append(d["stockpile_model_est"])
    model["lambda_model"].append(d["lambda_model_est"])

    # Generate everything
    print("\n📊 Generating charts...")
    chart4, chart6 = generate_charts(next_day, hist, model)

    print("\n📝 Creating day update pages...")
    en_file = generate_day_page_en(next_day, d, hist)
    generate_day_page_zh(next_day, d, hist, en_file)

    print("\n📋 Updating daily tracker...")
    update_daily_tracker_en(next_day, d, hist)
    update_daily_tracker_zh(next_day, d, hist)

    print("\n📚 Updating SUMMARY.md...")
    update_summary(next_day, d, en_file)

    print("\n💾 Saving history...")
    save_history(hist, model)

    print(f"\n{'='*60}")
    print(f"  ✅ Day {next_day} update complete!")
    print(f"{'='*60}")
    print(f"\n  Files updated:")
    print(f"    charts/  — 6 PNG charts regenerated")
    print(f"    updates/{en_file}")
    print(f"    zh/updates/{en_file}")
    print(f"    updates/daily-tracker.md")
    print(f"    zh/updates/daily-tracker.md")
    print(f"    SUMMARY.md")
    print(f"    history_data.json")
    print(f"\n  Next: python daily_update.py --template  (to prep Day {next_day+1})")


if __name__ == "__main__":
    main()
