# Evacuation Decision Model

## ABC + Brock-Hommes HAM Framework

**Prepared: March 7, 2026**

This documentation provides a complete technical reference for the Evacuation Decision Model used to assess civilian departure dynamics during the February–March 2026 Gulf conflict.

The model combines **Approximate Bayesian Computation (ABC)** for conflict scenario forecasting with a **Heterogeneous Agent Model (HAM)** adapted from Brock & Hommes (1998) for population flight prediction.

### Key Metrics

| Metric | Value |
|--------|-------|
| Days of Conflict Data | 7 |
| Monte Carlo Simulations | 50,000 |
| Agent Types Modeled | 6 |
| Interception Rate | 92.7% |
| Model Reliability | MODERATE |

### Framework Overview

The pipeline flows through five interconnected modules:

```
MOD Data → Situation Assessment → Bayesian ABC (50K MC) → HAM Stability (λ) → Population Flight (6 agents) → Evacuation Risk Score
```

The framework ingests verified UAE Ministry of Defence data published via `@modgovae` on X.com, cross-referenced with Gulf News, WAM, and Khaleeji Times reporting. It produces scenario-weighted evacuation risk scores and optimal departure window recommendations for six distinct civilian population segments.

### Data Sources

| Source | Type | Frequency |
|--------|------|-----------|
| `@modgovae` (X.com) | Official UAE MOD infographics | Daily |
| WAM (Emirates News Agency) | Wire service reports | Multiple daily |
| Gulf News / Khaleeji Times | Regional press | Daily |
| GCAA (Aviation Authority) | Airport capacity / airspace status | As-announced |
| Polymarket | Ceasefire prediction market odds | Real-time |
| FlightRadar24 | Aviation movement data | Real-time |
