# 3. HAM Stability Analysis

> 🌐 **EN** | [中文](../zh/method/ham-stability.md)


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

The feedback gain is computed as a sum of seven stochastic effects via 50K Monte Carlo simulations:

```
λ = 1.0 + λ_launcher + λ_drone + λ_intercept + λ_proxy + λ_hormuz + λ_weapon + λ_naval
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

**Proxy Activation** — Houthi/Hezbollah joining (P=4% with 3 CSGs, high impact):
```
λ_proxy = +0.8 · Bernoulli(0.04) · U(0.5, 2.0)
```

**Hormuz Closure** — Strait closure risk (P=2% with 3 CSGs):
```
λ_hormuz = +0.6 · Bernoulli(0.02) · U(0.6, 1.5)
```

**New Weapon Introduction** — Novel capability emergence (P=3%):
```
λ_weapon = +0.4 · Bernoulli(0.03) · U(0.5, 1.5)
```

### Naval Deterrence (Stabilizing)

**Three-Carrier Deterrence** — CVN-72, CVN-78, CVN-77 with 13+ Aegis ships:
```
λ_naval = -0.08 · carrier_count · (1 + N(0, 0.10))
```
With 3 carriers: approximately **–0.24** additional stabilizing effect, the second strongest stabilizing force after launcher attrition.

![HAM Feedback Gain λ Distribution](../assets/lambda_distribution.png)

## Results

| Metric | Value |
|--------|-------|
| λ median | 0.496 |
| λ 95th percentile | 1.063 |
| P(λ > 1) | 5.8% |
| 14-day cumulative cascade probability | 1 - (1 - 0.058)^14 ≈ 57% |

**Interpretation:** The system is metastable — launcher attrition and three-carrier naval deterrence (–0.24) provide strong stabilization, pulling the median λ well below 1.0. However, fat-tailed risks from proxy activation or Hormuz closure still create a non-trivial cumulative cascade probability over a 14-day horizon.

> **UPDATE (March 7):** With the 3rd carrier strike group (CVN-77 George H.W. Bush) deploying, the naval deterrence effect increases from –0.16 to –0.24 on λ. Proxy activation probability drops from 6% to 4% and Hormuz closure risk from 4% to 2%. The λ median shifts from 0.739 to 0.496, and P(λ > 1) drops from 12.2% to 5.8%.
