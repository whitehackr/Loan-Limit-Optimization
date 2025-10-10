"""
Configuration Constants for Loan Limit Optimization

This module contains all configurable business parameters for the loan limit
optimization model. All values can be overridden for scenario analysis.
"""

# Business Parameters
PROFIT_PER_INCREASE = 40  # dollars (on-time repayment - legacy parameter)
CAC_OFFSET = 2  # First 2 increases recover costs
ANNUAL_DISCOUNT_RATE = 0.19  # 19% annual discount rate for NPV calculations

# Outcome Values (Three-outcome model)
PROFIT_ON_TIME = 40  # Profit when customer repays on time
PROFIT_EARLY = 30    # Profit when customer repays early (less interest collected)

# Early Repayment Probabilities (Conditional on not defaulting)
# Higher-rated customers more likely to repay early
EARLY_REPAY_PROBS = {
    'Prime': 0.20,
    'Near-Prime': 0.15,
    'Subprime': 0.10,
    'High-Risk': 0.05
}

# Loan Parameters
DEFAULT_INCREASE_PCT = 0.20  # 20% loan limit increase amount
DEFAULT_RECOVERY_RATE = 0.10  # 10% recovery rate on defaulted loans
LOSS_REALIZATION_PCT = 0.50  # Assumption: default occurs at 50% loan paydown

# Eligibility Rules
ELIGIBILITY_DAYS = 60  # Minimum days between loan limit increases
MIN_ONTIME_PAYMENT_PCT = 0.80  # Minimum 80% on-time payment rate for eligibility

# Risk Categories (explicit boundaries)
# Using explicit min/max for clear boundary handling
RISK_CATEGORIES = {
    'Prime': {'min': 95.0, 'max': 100.0},        # [95, 100]
    'Near-Prime': {'min': 90.0, 'max': 95.0},    # [90, 95)
    'Subprime': {'min': 85.0, 'max': 90.0},      # [85, 90)
    'High-Risk': {'min': 80.0, 'max': 85.0}      # [80, 85)
}

# MILP Constraints (daily operational limits)
DEFAULT_RISK_APPETITE = 0.15  # Max 15% weighted default rate per day
# Note: Daily capital limit is calculated dynamically from portfolio data
# Formula: (sum(Initial_Loan) / 365) * increase_pct

# Annual Regulatory Constraint (strategic limit)
ANNUAL_REGULATORY_LIMIT = 120_000_000  # $120M annual cap on total increase volume

# Economic Factors (2023 Kenya baseline)
INFLATION_RATE = 0.077  # 7.7% inflation rate
UNEMPLOYMENT_RATE = 0.0557  # 5.57% unemployment rate
INFLATION_IMPACT = -0.05  # Estimated -5% negative impact on demand
UNEMPLOYMENT_IMPACT = -0.02  # Estimated -2% negative impact on demand

# Macro Demand Factor Calculation
# Combined impact: (1 + INFLATION_IMPACT) * (1 + UNEMPLOYMENT_IMPACT)
# = (1 - 0.05) * (1 - 0.02) = 0.95 * 0.98 = 0.931
MACRO_DEMAND_FACTOR = (1 + INFLATION_IMPACT) * (1 + UNEMPLOYMENT_IMPACT)

# Risk Modeling
EMERGING_MARKET_RISK_MULTIPLIER = 2.0  # 2x multiplier on baseline default rates

# Simulation Parameters
SIMULATION_START_DATE = "2024-01-01"  # Forecast period starts Jan 1, 2024
SIMULATION_DAYS = 365  # Full year simulation
DEFAULT_N_ITERATIONS = 100  # Start with 100 for testing (scale to 10,000 for production)
RANDOM_SEED = 42  # For reproducibility

# Data Assumptions
ANALYSIS_DATE = "2023-12-31"  # End of observation period

# Display Configuration
VERBOSE = True  # Show progress bars and detailed logging
