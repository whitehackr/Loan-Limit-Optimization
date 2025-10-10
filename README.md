# Loan Limit Optimization

**Advanced Operations Research & Machine Learning for Credit Risk Management**

## Overview

This project implements a sophisticated loan limit optimization system for CredAble, balancing profitability maximization with risk management. The system uses a combination of survival analysis, Markov chain modeling, mixed-integer linear programming, and Monte Carlo simulation to determine optimal loan limit increase strategies.

## Key Features

- **Cox Proportional Hazards Model** for demand forecasting (P(Accept))
- **Synthetic Markov Transition Matrix** for risk state modeling (P(Default))
- **Three-Outcome Profit Model** (Early Repayment, On-Time, Default)
- **Mixed-Integer Linear Programming (MILP)** for daily tactical optimization
- **Monte Carlo Simulation** with annual regulatory constraint ($120M cap)
- **Comprehensive Risk Analytics** (VaR, CVaR, sensitivity analysis)

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
│   ├── 02_modeling_optimization_simulation.ipynb
│   └── 03_risk_analytics_final_report.ipynb
├── src/
│   ├── data_processing.py    # Data loading & feature engineering
│   ├── risk_segmentation.py  # Risk categorization
│   ├── demand_model.py        # Cox PH model for P(Accept)
│   ├── risk_model.py          # Transition matrix & LGD
│   ├── optimization.py        # MILP engine
│   ├── simulation.py          # Monte Carlo simulator
│   ├── risk_analytics.py      # VaR, CVaR calculations
│   └── visualization.py       # Plotting functions
├── tests/                     # Unit tests
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

### Step 2: Modeling, Optimization & Simulation

```bash
jupyter notebook notebooks/02_modeling_optimization_simulation.ipynb
```

### Step 3: Risk Analytics & Final Report

```bash
jupyter notebook notebooks/03_risk_analytics_final_report.ipynb
```

## Methodology

### Block 1: Data Foundation & Feature Engineering
- Risk categorization (Prime, Near-Prime, Subprime, High-Risk)
- Feature engineering (Opportunity Number, etc.)

### Block 2: Probabilistic Modeling
- **Demand Model**: Cox Proportional Hazards for P(Accept)
- **Risk Model**: Markov transition matrix for P(Default)
- **Three-Outcome Model**: Early/OnTime/Default with risk-adjusted probabilities

### Block 3: Daily Tactical Optimization (MILP)
- Maximize expected profit subject to:
  - Daily capital allocation constraint
  - Daily portfolio risk constraint

### Block 4: Strategic Forecast (Monte Carlo Simulation)
- 10,000 iterations of 365-day forecasts
- Annual regulatory limit enforcement ($120M cap)
- Stochastic acceptance, default, and state transitions

### Block 5: Risk Analytics
- Value at Risk (VaR) and Conditional VaR (CVaR)
- Strategy comparison across scenarios
- Sensitivity analysis on key parameters

## Key Results

*(To be populated after analysis)*

- **Expected Annual NPV**: $X.XM
- **VaR @ 95%**: $Z.ZM
- **Optimal Strategy**: TBD

## Productionization Roadmap

See `docs/PRODUCTIONIZATION.md` for:
- API design for daily decision serving
- Database schema
- Model retraining strategy
- Monitoring & alerting framework

## Testing

```bash
pytest tests/
```

## Contributing

See `CONTRIBUTING.md` for guidelines.

## License

*(To be added)*

## Authors

- **Project Lead**: Kevin Waithaka

---

**Status**: 🚧 In Development

**Last Updated**: October 10, 2025