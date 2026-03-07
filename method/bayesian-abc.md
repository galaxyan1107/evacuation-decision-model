# 2. Bayesian Conflict Forecast (ABC)

> 🌐 **EN** | [中文](../zh/method/bayesian-abc.md)


The core forecasting engine uses **Approximate Bayesian Computation** with 50,000 Monte Carlo simulations to estimate posterior probabilities over four conflict scenarios.

## Why ABC?

Traditional Bayesian inference requires a likelihood function, which is intractable for complex conflict dynamics. ABC sidesteps this by:
1. Simulating attack trajectories from each scenario's generative model
2. Comparing simulated trajectories against observed data using a distance metric
3. Weighting scenarios by how well their simulations match reality

## Scenario Definitions

| Scenario | β Decay | Drone Rate | Cruise Rate | Duration | Escalation P |
|----------|---------|------------|-------------|----------|-------------|
| **Ceasefire** | 0.50 | 60/day | 0.3/day | 7 ± 3d | 0% |
| **Baseline** | 0.35 | 130/day | 1.0/day | 20 ± 6d | 3% |
| **Escalation** | 0.18 | 180/day | 2.5/day | 35 ± 10d | 10% |
| **Regime War** | 0.08 | 300/day | 6.0/day | 60 ± 15d | 25% |

Each scenario is defined by a `ScenarioParams` dataclass with parameters governing ballistic decay, drone production rate, cruise missile frequency, expected conflict duration, and escalation probability.

## Soft ABC Algorithm

Unlike standard ABC which uses hard rejection thresholds, this implementation uses **soft ABC with Gaussian kernel weighting**. All simulations are retained but weighted by fit quality:

```
NRMSE_i = RMSE(sim_i[0:T_obs], observed) / mean(observed)

w_i = exp(-0.5 · (NRMSE_i / h)²) · π_s
```

Where:
- `h = 0.35` is the kernel bandwidth
- `π_s` is the informative prior for scenario s

### Informative Priors

```python
prior_weights = {
    "ceasefire": 0.05,     # Low prior — no ceasefire signals yet
    "baseline": 0.45,      # Highest prior — most consistent with data
    "escalation": 0.35,    # Substantial prior — tail risk
    "regime_war": 0.15     # Small but non-zero — extreme scenario
}
```

## Time-Dependent Posterior Evolution

A key innovation: posteriors **evolve over time** beyond the observation window. This reflects the physical reality that destroyed TELs cannot be replaced, making sustained ballistic campaigns progressively less viable.

### Boost Functions

```
boost_ceasefire(d)   = 1 + 3.0 · (1 - exp(-0.15 · (d - T_obs)))
boost_baseline(d)    = 1 + 0.5 · exp(-0.05 · (d - T_obs))
boost_escalation(d)  = max(0.1, 1 - 0.7 · (1 - exp(-0.10 · (d - T_obs))))
boost_regime_war(d)  = max(0.05, 1 - 0.85 · (1 - exp(-0.08 · (d - T_obs))))
```

**Interpretation:**
- Ceasefire probability **grows** over time as launcher attrition accumulates
- Baseline remains relatively stable with slight initial boost
- Escalation and Regime War probabilities **decay** as the physical capacity for escalation diminishes

## Output

The ABC module produces:
- **Posterior probabilities** for each scenario at each day (30-day horizon)
- **Attack forecasts** with median and 50%/90% confidence intervals per scenario
- **Effective Sample Size (ESS)** for assessing posterior quality
- **Probability summary** at Day 6, 14, and 30 milestones

![Posterior Scenario Probabilities Over Time](../assets/bayesian_posteriors.png)

### Example Output (Day 7 Data)

| Scenario | Day 6 | Day 14 | Day 30 |
|----------|-------|--------|--------|
| Ceasefire | 3.3% | 7.8% | 12.8% |
| Baseline | 64.9% | 71.2% | 75.4% |
| Escalation | 31.4% | 20.1% | 11.7% |
| Regime War | 0.4% | 0.9% | 0.1% |
