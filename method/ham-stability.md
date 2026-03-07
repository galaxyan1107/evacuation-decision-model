# 3. HAM Stability Analysis

The Heterogeneous Agent Model stability module assesses whether the conflict system is in a **stable equilibrium**, **metastable** (resilient to small shocks), or approaching a **cascade tipping point**.

## Key Metric: Feedback Gain λ

The central diagnostic is the feedback gain λ. When λ > 1.0, positive feedback loops dominate and the system enters an escalation cascade.

```
λ > 1.0  →  CASCADE (positive feedback dominates)
λ < 1.0  →  STABLE/METASTABLE (negative feedback dominates)
```

## Cascade Threshold Metrics

Five binary threshold indicators are monitored:

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Launcher Depletion | 85.7% | > 85% | **BREACHED** |
| Drone Stockpile Remaining | 40.8% | < 30% | OK |
| Interception Rate | 92.7% | < 90% | OK |
| Daily Casualties | 16.4 | > 10 | **BREACHED** |
| New Weapon Type | No | Yes | OK |

**Verdict Rule:** ≥ 3 breaches = UNSTABLE, ≥ 1 = METASTABLE, 0 = STABLE

Current status: **METASTABLE** (2/5 breached)

## Feedback Gain λ Decomposition

The feedback gain is computed as a sum of six stochastic effects via 50K Monte Carlo simulations:

```
λ = 1.0 + λ_launcher + λ_drone + λ_intercept + λ_proxy + λ_hormuz + λ_weapon
```

### Stabilizing Effects (Negative Feedback)

**Launcher Attrition** — ~300 of 350 TELs destroyed by coalition strikes:
```
λ_launcher = -0.55 · depletion · (1 + N(0, 0.12))
```
This is the dominant stabilizing force, pulling λ significantly below 1.0.

### Destabilizing Effects (Positive Feedback)

**Drone Persistence** — Production-rate-limited at ~130/day sustains pressure:
```
λ_drone = +0.25 · (1 - stockpile_remaining) · (1 + N(0, 0.2))
```

**Interception Degradation** — Fat-tailed risk of defense system degradation:
```
λ_intercept = +0.15 · Exp(0.03) / (1 - int_rate + 0.01)
```

**Proxy Activation** — Houthi/Hezbollah joining (P=6%, high impact):
```
λ_proxy = +0.8 · Bernoulli(0.06) · U(0.5, 2.0)
```

**Hormuz Closure** — Strait closure risk (P=4%):
```
λ_hormuz = +0.6 · Bernoulli(0.04) · U(0.6, 1.5)
```

**New Weapon Introduction** — Novel capability emergence (P=3%):
```
λ_weapon = +0.4 · Bernoulli(0.03) · U(0.5, 1.5)
```

![HAM Feedback Gain λ Distribution](../assets/lambda_distribution.png)

## Results

| Metric | Value |
|--------|-------|
| λ median | 0.729 |
| λ 95th percentile | ~1.35 |
| Daily cascade probability | P(λ > 1) per sim |
| 14-day cumulative cascade probability | 1 - (1 - P_daily)^14 |

**Interpretation:** The system is metastable — launcher attrition provides strong stabilization, but fat-tailed risks from proxy activation or Hormuz closure create a non-trivial cascade probability over a 14-day horizon.
