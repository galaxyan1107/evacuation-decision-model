# Data Sources & Verification

## Primary Sources

### UAE Ministry of Defence (`@modgovae`)
- **Platform:** X.com (formerly Twitter)
- **Frequency:** Daily infographics
- **Content:** Cumulative intercept counts by weapon type, interception rates, drone counts
- **Verification:** Cross-checked against WAM wire service and Gulf News reporting
- **Reliability:** High — official government source with consistent reporting format

### WAM (Emirates News Agency)
- **Type:** State wire service
- **Role:** Official confirmation of MOD figures, additional operational context
- **Used for:** Casualty figures, airspace status updates, coalition statements

### GCAA (General Civil Aviation Authority)
- **Content:** Airport operational status, capacity recovery data, airspace NOTAM updates
- **Used for:** Airport capacity constraint curve in population flight model

## Secondary Sources

### Gulf News / Khaleeji Times
- **Role:** Regional press reporting for context and cross-verification
- **Used for:** Qualitative assessment, evacuation logistics, ground-truth anecdotes

### Polymarket
- **Type:** Prediction market
- **Used for:** Real-time ceasefire probability odds as external validation
- **Day 7 data:** ~63% ceasefire by end of March (vs model's 84% by Day 31)
- **Caveat:** Market efficiency varies; thin liquidity during early conflict

### FlightRadar24
- **Type:** Aviation tracking
- **Used for:** Inferring actual flight volumes for airport capacity validation
- **Resolution:** Aggregated daily movements, not individual flights

## Verification Protocol

Each data point undergoes a three-source check where possible:

1. **Primary source** (MOD/GCAA): Official figures
2. **Wire service** (WAM/Reuters): Independent confirmation
3. **Regional press**: Qualitative cross-check

Discrepancies are flagged in the `check_data_consistency()` function, which compares model inputs against v2/v3 code implementations and report tables.
