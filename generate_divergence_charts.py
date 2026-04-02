#!/usr/bin/env python3
"""
Generate 5 divergence charts for the UAE Evacuation Decision Model GitBook.
Charts include: heatmap, bars, scorecard, lambda evolution, and BM trajectory.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Rectangle
import seaborn as sns
from pathlib import Path
from typing import Dict, List, Tuple

# Configure matplotlib for dark professional theme
plt.style.use('dark_background')
sns.set_palette("husl")

# Chart configuration
CHART_CONFIG = {
    'figsize': (12, 8),
    'dpi': 150,
    'font_size': 10,
    'title_size': 14,
    'label_size': 11
}

# Output directory
OUTPUT_DIR = Path("/sessions/busy-determined-carson/mnt/flea/gitbook-evacuation-model/charts")
OUTPUT_DIR.mkdir(exist_ok=True)

def load_data():
    """Load daily_data.json and run_log.json"""
    daily_path = Path("/sessions/busy-determined-carson/mnt/flea/gitbook-evacuation-model/pipeline/daily_data.json")
    run_log_path = Path("/sessions/busy-determined-carson/mnt/flea/gitbook-evacuation-model/pipeline/run_log.json")

    with open(daily_path, 'r') as f:
        daily_data = json.load(f)

    with open(run_log_path, 'r') as f:
        run_log = json.load(f)

    return daily_data, run_log

def get_model_predictions(num_days: int) -> Dict:
    """Generate model predictions for each metric"""
    predictions = {
        'bm': [],
        'drones': [],
        'airport_capacity': [],
        'polymarket_ceasefire': []
    }

    for day in range(1, num_days + 1):
        # BM model: starts at 137, decays with half-life pattern
        bm_pred = 137 * (0.85 ** (day - 1))
        predictions['bm'].append(bm_pred)

        # Drone model: starts at 209, similar decay
        drone_pred = 209 * (0.85 ** (day - 1))
        predictions['drones'].append(drone_pred)

        # Airport capacity: linearly recovers from 30% to 100% over 30 days
        airport_pred = 30 + (70 * min((day - 1) / 29, 1.0))
        predictions['airport_capacity'].append(airport_pred)

    return predictions

def calculate_divergence(actual: float, predicted: float) -> float:
    """
    Calculate divergence percentage.
    Positive = actual worse than model (red)
    Negative = actual better than model (blue)
    """
    if predicted == 0:
        return 0
    # Divergence = (actual - predicted) / predicted * 100
    # For BM/drones: higher is worse
    # For airport: higher is better, so we flip it
    return ((actual - predicted) / predicted) * 100 if predicted != 0 else 0

def generate_divergence_heatmap(daily_data, run_log):
    """Generate heatmap showing model vs actual divergence"""
    days_data = daily_data['days']
    num_days = len(days_data)

    # Get predictions
    predictions = get_model_predictions(num_days)

    # Create lambda dict
    lambda_dict = {}
    for entry in run_log:
        lambda_dict[entry['day']] = entry['lambda_median']

    # Build divergence matrix
    metrics = ['BM', 'Drones', 'Airport %', 'Polymarket', 'Lambda']
    divergence_matrix = np.zeros((len(metrics), num_days))

    for day_idx, day_data in enumerate(days_data):
        day_num = day_data['day']

        # BM divergence
        bm_actual = day_data['bm_detected']
        bm_pred = predictions['bm'][day_idx]
        divergence_matrix[0, day_idx] = calculate_divergence(bm_actual, bm_pred)

        # Drone divergence
        drone_actual = day_data['drones_detected']
        drone_pred = predictions['drones'][day_idx]
        divergence_matrix[1, day_idx] = calculate_divergence(drone_actual, drone_pred)

        # Airport capacity divergence (flip: higher is better)
        airport_actual = day_data['airport_capacity_pct']
        airport_pred = predictions['airport_capacity'][day_idx]
        # For airport, invert sign so higher actual = blue (good)
        divergence_matrix[2, day_idx] = -calculate_divergence(airport_actual, airport_pred)

        # Polymarket divergence (if available, use placeholder)
        if day_data.get('polymarket_ceasefire_mar31'):
            divergence_matrix[3, day_idx] = day_data['polymarket_ceasefire_mar31']
        else:
            divergence_matrix[3, day_idx] = 0

        # Lambda divergence (actual vs threshold of 1.0)
        lambda_val = lambda_dict.get(day_num, 2.0)
        lambda_divergence = ((lambda_val - 1.0) / 1.0) * 100
        divergence_matrix[4, day_idx] = lambda_divergence

    # Create figure
    fig, ax = plt.subplots(figsize=CHART_CONFIG['figsize'], dpi=CHART_CONFIG['dpi'])

    # Plot heatmap with custom colormap (red for positive divergence, blue for negative)
    im = ax.imshow(divergence_matrix, cmap='RdBu_r', aspect='auto', vmin=-100, vmax=200)

    # Set ticks and labels
    ax.set_xticks(np.arange(num_days))
    ax.set_yticks(np.arange(len(metrics)))
    ax.set_xticklabels([f"Day {i+1}" for i in range(num_days)], fontsize=8, rotation=45)
    ax.set_yticklabels(metrics, fontsize=CHART_CONFIG['label_size'])

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax, label='Divergence %')
    cbar.ax.tick_params(labelsize=9)

    ax.set_title('Model Prediction vs Actual Divergence Across Metrics',
                fontsize=CHART_CONFIG['title_size'], pad=20, fontweight='bold')
    ax.set_xlabel('Days', fontsize=CHART_CONFIG['label_size'], labelpad=10)
    ax.set_ylabel('Metrics', fontsize=CHART_CONFIG['label_size'], labelpad=10)

    # Add text annotations for key cells
    for i in range(len(metrics)):
        for j in range(0, num_days, 3):  # Annotate every 3rd day to avoid clutter
            text = ax.text(j, i, f'{divergence_matrix[i, j]:.0f}',
                          ha="center", va="center", color="white", fontsize=7)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'divergence_heatmap.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.close()
    print("Generated: divergence_heatmap.png")

def generate_model_vs_actual_bars(daily_data):
    """Generate grouped bar chart showing model vs actual for key metrics"""
    days_data = daily_data['days']
    num_days = len(days_data)

    predictions = get_model_predictions(num_days)

    # Prepare data
    days = np.arange(num_days)
    width = 0.25

    bm_actual = [d['bm_detected'] for d in days_data]
    bm_pred = predictions['bm']

    drone_actual = [d['drones_detected'] for d in days_data]
    drone_pred = predictions['drones']

    airport_actual = [d['airport_capacity_pct'] for d in days_data]
    airport_pred = predictions['airport_capacity']

    # Create figure with subplots for each metric
    fig, axes = plt.subplots(1, 3, figsize=(18, 6), dpi=CHART_CONFIG['dpi'])
    fig.suptitle('Model Predictions vs Actual Values - Key Metrics',
                fontsize=CHART_CONFIG['title_size'], fontweight='bold', y=1.00)

    # BM Chart
    ax = axes[0]
    x = np.arange(num_days)
    ax.bar(x - width/2, bm_actual, width, label='Actual', alpha=0.8, color='#FF6B6B')
    ax.plot(x, bm_pred, 'o-', label='Model Prediction', color='#4ECDC4', linewidth=2, markersize=4)
    ax.set_xlabel('Day', fontsize=CHART_CONFIG['label_size'])
    ax.set_ylabel('Count', fontsize=CHART_CONFIG['label_size'])
    ax.set_title('Ballistic Missiles', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.set_xticks(np.arange(0, num_days, 5))

    # Drone Chart
    ax = axes[1]
    ax.bar(x - width/2, drone_actual, width, label='Actual', alpha=0.8, color='#95E1D3')
    ax.plot(x, drone_pred, 'o-', label='Model Prediction', color='#F38181', linewidth=2, markersize=4)
    ax.set_xlabel('Day', fontsize=CHART_CONFIG['label_size'])
    ax.set_ylabel('Count', fontsize=CHART_CONFIG['label_size'])
    ax.set_title('Drones', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.set_xticks(np.arange(0, num_days, 5))

    # Airport Capacity Chart
    ax = axes[2]
    ax.bar(x - width/2, airport_actual, width, label='Actual', alpha=0.8, color='#AA96DA')
    ax.plot(x, airport_pred, 'o-', label='Model Prediction', color='#FCBAD3', linewidth=2, markersize=4)
    ax.set_xlabel('Day', fontsize=CHART_CONFIG['label_size'])
    ax.set_ylabel('Capacity %', fontsize=CHART_CONFIG['label_size'])
    ax.set_title('Airport Capacity', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(axis='y', alpha=0.3)
    ax.set_xticks(np.arange(0, num_days, 5))
    ax.set_ylim(0, 100)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'model_vs_actual_bars.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.close()
    print("Generated: model_vs_actual_bars.png")

def generate_divergence_scorecard(daily_data, run_log):
    """Generate visual scorecard table showing daily divergence metrics"""
    days_data = daily_data['days']
    num_days = len(days_data)

    predictions = get_model_predictions(num_days)

    # Create lambda dict
    lambda_dict = {}
    for entry in run_log:
        lambda_dict[entry['day']] = entry['lambda_median']

    # Prepare scorecard data
    scorecard_data = []
    for day_idx, day_data in enumerate(days_data):
        day_num = day_data['day']

        bm_actual = day_data['bm_detected']
        bm_pred = predictions['bm'][day_idx]
        bm_div = abs(calculate_divergence(bm_actual, bm_pred))

        drone_actual = day_data['drones_detected']
        drone_pred = predictions['drones'][day_idx]
        drone_div = abs(calculate_divergence(drone_actual, drone_pred))

        airport_actual = day_data['airport_capacity_pct']
        airport_pred = predictions['airport_capacity'][day_idx]
        airport_div = abs(calculate_divergence(airport_actual, airport_pred))

        # Overall score (average absolute divergence)
        overall_score = (bm_div + drone_div + airport_div) / 3

        # Verdict based on overall score and lambda
        lambda_val = lambda_dict.get(day_num, 2.0)
        if lambda_val > 1.5:
            verdict = "CRITICAL"
            verdict_color = '#FF4444'
        elif lambda_val > 1.0:
            verdict = "UNSTABLE"
            verdict_color = '#FFaa00'
        else:
            verdict = "STABLE"
            verdict_color = '#44FF44'

        scorecard_data.append({
            'day': day_num,
            'bm_div': bm_div,
            'drone_div': drone_div,
            'airport_div': airport_div,
            'overall': overall_score,
            'verdict': verdict,
            'color': verdict_color
        })

    # Create figure for scorecard
    fig, ax = plt.subplots(figsize=CHART_CONFIG['figsize'], dpi=CHART_CONFIG['dpi'])
    ax.axis('tight')
    ax.axis('off')

    # Prepare table data
    table_data = [['Day', 'BM Div %', 'Drone Div %', 'Airport Div %', 'Overall Score', 'Verdict']]
    colors = [['#333333'] * 6]  # Header row color

    for entry in scorecard_data:
        row = [
            f"D{entry['day']}",
            f"{entry['bm_div']:.1f}",
            f"{entry['drone_div']:.1f}",
            f"{entry['airport_div']:.1f}",
            f"{entry['overall']:.1f}",
            entry['verdict']
        ]
        table_data.append(row)

        # Color code the verdict cell
        row_color = ['#1a1a1a'] * 5 + [entry['color']]
        colors.append(row_color)

    # Create table
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    cellColours=colors, colWidths=[0.08, 0.15, 0.15, 0.18, 0.18, 0.18])

    table.auto_set_font_size(False)
    table.set_fontsize(9)
    table.scale(1, 2)

    # Style header row
    for i in range(6):
        table[(0, i)].set_text_props(weight='bold', color='white')
        table[(0, i)].set_facecolor('#444444')

    plt.title('Daily Divergence Scorecard - Model vs Actual',
             fontsize=CHART_CONFIG['title_size'], fontweight='bold', pad=20)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'divergence_scorecard.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.close()
    print("Generated: divergence_scorecard.png")

def generate_lambda_evolution(run_log):
    """Generate lambda evolution line chart"""
    # Extract lambda data from run_log
    days = []
    lambdas = []
    unstable_days = set()

    for entry in run_log:
        days.append(entry['day'])
        lambdas.append(entry['lambda_median'])
        if entry['verdict'] == 'UNSTABLE':
            unstable_days.add(entry['day'])

    # Sort by day
    sorted_data = sorted(zip(days, lambdas), key=lambda x: x[0])
    days, lambdas = zip(*sorted_data)
    days = list(days)
    lambdas = list(lambdas)

    # Create figure
    fig, ax = plt.subplots(figsize=CHART_CONFIG['figsize'], dpi=CHART_CONFIG['dpi'])

    # Plot lambda evolution
    ax.plot(days, lambdas, 'o-', color='#4ECDC4', linewidth=2.5, markersize=8, label='λ Median')

    # Add threshold line at λ=1
    ax.axhline(y=1.0, color='#44FF44', linestyle='--', linewidth=2, label='λ=1 Threshold (Stable)')

    # Highlight unstable days
    for day in days:
        if day in unstable_days:
            idx = days.index(day)
            ax.scatter(day, lambdas[idx], color='#FF4444', s=200, zorder=5,
                      marker='X', edgecolors='white', linewidths=1.5)

    # Fill regions
    ax.fill_between(days, 1, max(lambdas) + 0.2, where=(np.array(lambdas) > 1.0),
                    alpha=0.1, color='#FF4444', label='Unstable Region (λ > 1)')

    ax.set_xlabel('Day', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.set_ylabel('λ Median', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.set_title('Lambda Evolution - Queue Stability Across 34 Days',
                fontsize=CHART_CONFIG['title_size'], fontweight='bold', pad=20)

    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper right', framealpha=0.95)

    # Set x-axis to show every 2 days
    ax.set_xticks(np.arange(min(days), max(days) + 1, 2))
    ax.set_xlim(min(days) - 0.5, max(days) + 0.5)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'lambda_evolution_day34.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.close()
    print("Generated: lambda_evolution_day34.png")

def generate_bm_trajectory(daily_data):
    """Generate BM trajectory line chart with model overlay"""
    days_data = daily_data['days']
    num_days = len(days_data)

    predictions = get_model_predictions(num_days)

    # Extract BM actual values
    days = np.arange(1, num_days + 1)
    bm_actual = [d['bm_detected'] for d in days_data]
    bm_pred = predictions['bm']

    # Create figure
    fig, ax = plt.subplots(figsize=CHART_CONFIG['figsize'], dpi=CHART_CONFIG['dpi'])

    # Plot actual BM counts
    ax.plot(days, bm_actual, 'o-', color='#FF6B6B', linewidth=2.5, markersize=8,
           label='Actual BM Detected', zorder=3)
    ax.fill_between(days, 0, bm_actual, alpha=0.2, color='#FF6B6B')

    # Plot model prediction
    ax.plot(days, bm_pred, 's--', color='#4ECDC4', linewidth=2.5, markersize=6,
           label='Model Prediction (85% Decay)', zorder=2)

    # Styling
    ax.set_xlabel('Day', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.set_ylabel('Ballistic Missile Count', fontsize=CHART_CONFIG['label_size'], fontweight='bold')
    ax.set_title('Daily Ballistic Missile Detections vs Model Prediction',
                fontsize=CHART_CONFIG['title_size'], fontweight='bold', pad=20)

    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper right', framealpha=0.95)

    # Set x-axis ticks
    ax.set_xticks(np.arange(1, num_days + 1, 3))
    ax.set_xlim(0.5, num_days + 0.5)
    ax.set_ylim(0, max(bm_actual) * 1.1)

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / 'bm_trajectory.png', dpi=CHART_CONFIG['dpi'], bbox_inches='tight')
    plt.close()
    print("Generated: bm_trajectory.png")

def main():
    """Main execution function"""
    print("Loading data...")
    daily_data, run_log = load_data()

    print(f"Loaded {len(daily_data['days'])} days of data")
    print(f"Loaded {len(run_log)} lambda entries")

    print("\nGenerating charts...")

    # Generate all 5 charts
    generate_divergence_heatmap(daily_data, run_log)
    generate_model_vs_actual_bars(daily_data)
    generate_divergence_scorecard(daily_data, run_log)
    generate_lambda_evolution(run_log)
    generate_bm_trajectory(daily_data)

    print("\nAll charts generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}")

    # List generated files
    chart_files = sorted(OUTPUT_DIR.glob('divergence_*.png') |
                        OUTPUT_DIR.glob('model_vs_actual_*.png') |
                        OUTPUT_DIR.glob('lambda_evolution_*.png') |
                        OUTPUT_DIR.glob('bm_trajectory.png'))

    # Actually list them correctly
    chart_files = [
        OUTPUT_DIR / 'divergence_heatmap.png',
        OUTPUT_DIR / 'model_vs_actual_bars.png',
        OUTPUT_DIR / 'divergence_scorecard.png',
        OUTPUT_DIR / 'lambda_evolution_day34.png',
        OUTPUT_DIR / 'bm_trajectory.png'
    ]

    for chart_file in chart_files:
        if chart_file.exists():
            size_kb = chart_file.stat().st_size / 1024
            print(f"  ✓ {chart_file.name} ({size_kb:.1f} KB)")
        else:
            print(f"  ✗ {chart_file.name} (MISSING)")

if __name__ == '__main__':
    main()
