"""
Scenario Configurations for Loan Limit Optimization

This module defines various strategic scenarios for comparative analysis.
Each scenario specifies key parameters that differ from the baseline.
"""

SCENARIOS = {
    # Baseline Strategy: Balanced risk/return approach
    'baseline': {
        'increase_pct': 0.20,           # 20% increase amount
        'risk_appetite': 0.15,          # 15% max daily default rate
        'recovery_rate': 0.10,          # 10% recovery on defaults
        'risk_multiplier': 2.0,         # 2x emerging market risk
        'demand_factor': 0.931,         # 2023 Kenya economic conditions
        'description': 'Baseline policy with balanced risk-return profile'
    },

    # Conservative Strategy: Lower risk, lower returns
    'conservative': {
        'increase_pct': 0.10,           # 10% increase (smaller offers)
        'risk_appetite': 0.10,          # 10% max daily default rate (stricter)
        'recovery_rate': 0.10,
        'risk_multiplier': 2.0,
        'demand_factor': 0.931,
        'description': 'Conservative approach with lower risk exposure'
    },

    # Aggressive Growth Strategy: Higher risk, higher potential returns
    'aggressive': {
        'increase_pct': 0.30,           # 30% increase (larger offers)
        'risk_appetite': 0.20,          # 20% max daily default rate (looser)
        'recovery_rate': 0.10,
        'risk_multiplier': 2.0,
        'demand_factor': 0.931,
        'description': 'Aggressive growth strategy with higher risk tolerance'
    },

    # Low Recovery Scenario: Poor collections effectiveness
    'low_recovery': {
        'increase_pct': 0.20,
        'risk_appetite': 0.15,
        'recovery_rate': 0.05,          # 5% recovery (weak collections)
        'risk_multiplier': 2.0,
        'demand_factor': 0.931,
        'description': 'Scenario with low recovery rate (poor collections)'
    },

    # High Recovery Scenario: Strong collections effectiveness
    'high_recovery': {
        'increase_pct': 0.20,
        'risk_appetite': 0.15,
        'recovery_rate': 0.20,          # 20% recovery (strong collections)
        'risk_multiplier': 2.0,
        'demand_factor': 0.931,
        'description': 'Scenario with high recovery rate (effective collections)'
    },

    # Pessimistic Economic Scenario: Recession conditions
    'pessimistic': {
        'increase_pct': 0.20,
        'risk_appetite': 0.15,
        'recovery_rate': 0.10,
        'risk_multiplier': 2.5,         # 2.5x risk (worsening conditions)
        'demand_factor': 0.85,          # Lower demand (15% reduction)
        'description': 'Pessimistic economic scenario (recession)'
    },

    # Optimistic Economic Scenario: Economic expansion
    'optimistic': {
        'increase_pct': 0.20,
        'risk_appetite': 0.15,
        'recovery_rate': 0.10,
        'risk_multiplier': 1.5,         # 1.5x risk (improving conditions)
        'demand_factor': 1.0,           # No macro dampening effect
        'description': 'Optimistic economic scenario (expansion)'
    },

    # No Optimization Baseline: Accept all eligible customers
    'no_optimization': {
        'increase_pct': 0.20,
        'risk_appetite': None,          # No risk constraint (accept all)
        'recovery_rate': 0.10,
        'risk_multiplier': 2.0,
        'demand_factor': 0.931,
        'description': 'No optimization - offer to all eligible customers'
    }
}

# Sensitivity Analysis Parameters
# Define ranges for key parameters to test sensitivity

SENSITIVITY_PARAMS = {
    'recovery_rate': [0.05, 0.10, 0.15, 0.20],
    'risk_multiplier': [1.5, 2.0, 2.5, 3.0],
    'increase_pct': [0.10, 0.15, 0.20, 0.25, 0.30],
    'risk_appetite': [0.10, 0.12, 0.15, 0.18, 0.20],
    'demand_factor': [0.85, 0.90, 0.931, 0.95, 1.0]
}
