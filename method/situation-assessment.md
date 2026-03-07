# 1. Situation Assessment

The first module ingests cumulative attack data from UAE MOD infographics posted daily on X.com via the `@modgovae` account, cross-verified against wire services (WAM, Reuters) and regional press (Gulf News, Khaleeji Times). Cumulative figures are differenced to produce daily new-attack vectors.

## Data Ingestion

Raw cumulative data is stored in a structured dictionary keyed by conflict day:

```python
UAE_MOD_CUMULATIVE = {
    1: {"date": "Feb 28", "ballistic": 137, "intercepted": 132,
        "sea": 5, "land": 0, "cruise": 0, "drones": 209, "int_rate": None},
    # ... through Day 7
    7: {"date": "Mar 6", "ballistic": 205, "intercepted": 190,
        "sea": 13, "land": 2, "cruise": 8, "drones": 1184, "int_rate": 0.927},
}
```

The `compute_daily_attacks()` function differences cumulative data to produce daily new-attack counts for each weapon type.

## Trend Metrics

| Metric | Method | Value (Day 7) |
|--------|--------|---------------|
| Ballistic Decay Rate | Log-linear regression on daily BM counts | 0.608/day (OLS) vs 0.25 (Bayesian) |
| Drone Steady-State | Mean of last 3 days' drone launches | ~124/day |
| Interception Rate | Cumulative MOD-reported figure | 92.7% |
| Drone Stockpile | 2000 estimated initial - 1184 launched | 40.8% remaining |

## Ballistic Decay Model

The ballistic missile launch rate follows an exponential decay pattern:

```
BM(t) = BM₀ · exp(-β · t) + εₜ
```

Where:
- `β` = decay rate per day
- `BM₀` = 137 (Day 1 observed opening salvo)
- `εₜ` = noise term

**Key divergence:** The report uses a Bayesian posterior estimate of β = 0.25/day, while simple OLS log-linear regression yields β = 0.608/day. The OLS is inflated by the Day 1 opening salvo (137 BMs) followed by steep drop-off. The Bayesian approach regularizes through priors informed by historical conflict decay patterns.

![Attack Forecast — 30-Day Horizon](../assets/attack_forecast.png)

## Drone Stockpile Estimation

```python
estimated_initial_stockpile = 2000  # per intelligence estimates
drone_remaining_pct = (2000 - total_drones_launched) / 2000
```

At Day 7: 1184 of ~2000 drones launched = 40.8% remaining, approximately 7-8 days of sustained operations at current 112/day rate.
