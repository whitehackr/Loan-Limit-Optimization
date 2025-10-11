import pandas as pd
import pytest
from src.optimization import DailyOptimizationModel

@pytest.fixture
def sample_cohort():
    """Creates a sample DataFrame of eligible customers for testing."""
    data = {
        'customer_id': [1, 2, 3, 4],
        'initial_loan': [1000, 2000, 500, 8000],
        'p_accept': [0.6, 0.7, 0.8, 0.5],
        'p_default': [0.1, 0.2, 0.05, 0.3],
    }
    df = pd.DataFrame(data)
    return df

def test_optimizer_selects_most_profitable(sample_cohort):
    """
    Tests that the optimizer selects the single most profitable customer
    when the capital constraint is very tight.
    """
    # Customer 3 is the only one with positive expected profit.
    # Increase amount for cust 3 is 500 * 0.20 = 100.
    scenario = {
        'increase_pct': 0.20,
        'risk_appetite': 0.50, # Loose risk appetite
        'recovery_rate': 0.10,
        # Tight capital limit that only allows customer 3 (increase_amt = 100)
        'daily_capital_limit': 150 
    }

    optimizer = DailyOptimizationModel(sample_cohort, scenario)
    decisions = optimizer.solve()

    # Expected: Only customer 3 should be selected because they are the only one
    # with positive expected profit, and their increase amount fits the budget.
    assert decisions[1] == 0
    assert decisions[2] == 0
    assert decisions[3] == 1
    assert decisions[4] == 0

def test_risk_constraint(sample_cohort):
    """
    Tests that the risk appetite constraint works correctly.
    """
    # Customer 3 has p_default = 0.05 and is profitable.
    # We set a tight risk appetite that only customer 3 can satisfy on their own.
    scenario = {
        'increase_pct': 0.20,
        'risk_appetite': 0.08, # Avg risk must be <= 8%
        'recovery_rate': 0.10,
        'daily_capital_limit': 10000 # Loose capital limit
    }

    optimizer = DailyOptimizationModel(sample_cohort, scenario)
    decisions = optimizer.solve()

    # Expected: Only customer 3 is selected. If any other customer with
    # p_default > 0.08 were also selected, the average risk constraint would fail.
    assert decisions[1] == 0
    assert decisions[2] == 0
    assert decisions[3] == 1
    assert decisions[4] == 0