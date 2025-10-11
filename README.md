# Loan Limit Optimization

**Loan Limit Optimization: Hybrid OR & ML for Credit Risk Management**

_A production-ready system combining Cox Proportional Hazards survival analysis, Markov chain risk modeling, and mixed-integer programming to optimize loan limit increase strategies under regulatory constraints._

## Business Problem

Financial institutions face a critical optimization challenge: **Which customers should receive loan limit increases, and when?** 

Offering too liberally increases default risk; being too conservative leaves profit on the table. This project develops a sophisticated decision framework that:
- Predicts customer acceptance probability
- Models dynamic credit risk transitions
- Optimizes offers under capital and regulatory constraints
- Quantifies expected profit with uncertainty bounds

The system demonstrates $28.1M annual value-add over naive "offer to all" approaches.

## Overview

This project implements a production-ready loan limit optimization system that integrates Cox Proportional Hazards demand forecasting, Markov chain risk modeling, and mixed-integer linear programming under realistic operational constraints. A Monte Carlo simulation framework evaluates strategic scenarios, revealing that a conservative policy (10% risk appetite, 10% increase size) delivers optimal risk-adjusted returns ($114.8k annual NPV) while a no-optimization baseline produces -$28.0M losses, quantifying the MILP's value-add at $28.1M annually.

## Key Features

- **Cox Proportional Hazards Model** for demand forecasting with macro economic adjustments
- **Synthetic Markov Transition Matrix** for dynamic risk state modeling (FICO-adjusted)
- **Mixed-Integer Linear Programming (MILP)** with monthly batch optimization
- **Expected Profit Pre-filtering** reducing MILP problem size by 10x
- **Monte Carlo Simulation** evaluating 4 strategic scenarios over 365-day horizon
- **Performance Optimizations** achieving 50x speedup through batching and solver tuning
- **Comprehensive Risk Analytics** (VaR, CVaR, comparative scenario analysis)

## Project Structure

```
Loan-Limit-Optimization/
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   ├── constants.py          # All business parameters
│   └── scenarios.py           # Scenario configurations
├── data/
│   ├── raw/                   # Original datasets
│   └── processed/             # Processed datasets
├── notebooks/
│   ├── 01_exploratory_data_analysis.ipynb
│   ├── 02_demand_risk_modeling.ipynb
│   └── 03_simulation_and_analysis.ipynb
├── src/
│   ├── data_processing.py    # Data loading & feature engineering
│   ├── risk_segmentation.py  # Risk categorization
│   ├── demand_model.py        # Cox PH model for P(Accept)
│   ├── risk_model.py          # Markov transition matrix
│   ├── optimization.py        # MILP solver with pre-filtering
│   └── simulation.py          # Monte Carlo simulation engine
├── tests/
│   ├── test_optimization.py
│   └── test_simulation.py
└── outputs/
    ├── figures/               # Visualizations
    ├── models/                # Saved models
    └── results/               # Simulation results
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/whitehackr/Loan-Limit-Optimization.git
cd Loan-Limit-Optimization
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Dataset

Place the `loan_limit_increases.xlsx` file in the `data/raw/` directory.

## Configuration

All business parameters are centralized in `config/constants.py`:

- **Profit Parameters**: `PROFIT_ON_TIME`, `PROFIT_EARLY`
- **Risk Parameters**: `DEFAULT_RECOVERY_RATE`, `EARLY_REPAY_PROBS`
- **Constraints**: `DEFAULT_RISK_APPETITE`, `ANNUAL_REGULATORY_LIMIT`
- **Economic Factors**: `INFLATION_RATE`, `UNEMPLOYMENT_RATE`

To modify scenarios, edit `config/scenarios.py`.

## Running the Analysis

### Step 1: Exploratory Data Analysis

```bash
jupyter notebook notebooks/01_exploratory_data_analysis.ipynb
```

Performs data quality assessment, feature engineering, and risk segmentation using centralized modules.

### Step 2: Demand & Risk Modeling

```bash
jupyter notebook notebooks/02_demand_risk_modeling.ipynb
```

Builds Cox PH demand model (C-index = 0.506) and implements synthetic Markov transition matrix with train/test evaluation.

### Step 3: Simulation & Comparative Analysis

```bash
jupyter notebook notebooks/03_simulation_and_analysis.ipynb
```

Executes Monte Carlo simulations across 4 scenarios (baseline, conservative, aggressive, no_optimization) with comprehensive technical analysis.

## Methodology

### 1. Data Foundation & Risk Segmentation
- Centralized risk categorization module (Prime ≥95%, Near-Prime ≥90%, Subprime ≥85%, High-Risk ≥80%)
- Feature engineering for eligibility rules (60-day minimum between offers)

### 2. Probabilistic Modeling
- **Demand Model**: Cox Proportional Hazards with macro adjustment factor (0.931 for inflation/unemployment)
- **Risk Model**: Synthetic Markov transition matrix (FICO-adjusted, 2.0x emerging market multiplier)
- **Expected Profit**: $E[\pi_i] = P(\text{Accept}_i) \cdot [(1 - P(\text{Default}_i)) \cdot 40 - P(\text{Default}_i) \cdot \text{LGD}_i]$

### 3. Monthly Tactical Optimization (MILP)
- Maximize expected profit subject to:
  - Monthly capital allocation constraint ($1.24M)
  - Portfolio risk constraint (weighted average default rate ≤ 15%)
- Pre-filtering eliminates negative expected profit customers before optimization
- CBC solver with 30-second timeout, presolve enabled, cuts disabled

### 4. Strategic Simulation (Monte Carlo)
- 365-day horizon with monthly batch optimization (12 solves per iteration)
- Annual regulatory limit enforcement ($120M cap)
- Stochastic acceptance, default, and risk state transitions via Markov chain
- Comparative analysis across 4 scenarios: baseline, conservative, aggressive, no_optimization

### 5. Performance Engineering
- Expected profit pre-filtering: 10x problem size reduction
- Monthly batching: 30x fewer MILP solves vs daily optimization
- Solver optimizations: 50-70% per-solve speedup
- Combined: 50x overall speedup (312 minutes → 6 minutes per simulation)

## Key Results

### Scenario Comparison (N=25 iterations)

| Scenario | Mean NPV | VaR (95%) | CVaR (95%) | Avg Defaults | Avg Volume |
|----------|----------|-----------|------------|--------------|------------|
| **Conservative** | **$114,757** | $92,472 | $91,430 | 451 | $1.05M |
| Baseline | $95,607 | $78,381 | $74,954 | 381 | $1.72M |
| Aggressive | $81,924 | $62,158 | $59,548 | 321 | $2.15M |
| No Optimization | **-$27.97M** | -$28.08M | -$28.09M | 21,754 | $48.48M |

### Strategic Findings

**1. Conservative Policy Optimal**
- 10% risk appetite + 10% increase size delivers 20% higher NPV than baseline
- Weak demand signals (C-index 0.506) make selectivity more valuable than scale
- Smaller exposures preserve capital when model cannot rank customers effectively

**2. MILP Value-Add: $28.1M**
- No-optimization scenario loses $27.97M with 21,754 defaults (72% of customer base)
- Validates constrained optimization as non-negotiable infrastructure

**3. Model Limitation Drives Strategy**
- Cox PH C-index of 0.506 (60 bps above random) limits targeting precision
- Expected profit calculation degenerates to risk-weighted filtering
- Demand model improvement is critical path to unlocking higher-volume strategies

**Production Recommendation**: Deploy conservative policy immediately while prioritizing demand model enhancement through longitudinal data collection and feature enrichment.

## Technical Approach

This implementation addresses all required components:

✅ **Dynamic credit eligibility** - Markov transition matrix updates risk categories post-acceptance
✅ **Markov chain modeling** - Synthetic 5×5 transition matrix with absorbing default state
✅ **Stochastic demand forecasting** - Cox PH with macro adjustment factor
✅ **Loan lifecycle simulation** - 365-day Monte Carlo with monthly MILP optimization
✅ **Constraint optimization** - Capital and risk appetite constraints with 30s timeout
✅ **Mathematical formulation** - Documented in notebook analysis
✅ **Python implementation** - Full modular codebase with unit tests
✅ **Simulation results** - Comparative scenario analysis with VaR/CVaR metrics
✅ **Operational recommendations** - Production deployment strategy and monitoring framework

## Testing

Run unit tests:
```bash
pytest tests/
```

## Authors

Kevin Waithaka
Data Scientist | Operations Research & Machine Learning

## License

MIT License - see LICENSE file for details

---

**Status**: ✅ Complete

**Last Updated**: October 11, 2025
