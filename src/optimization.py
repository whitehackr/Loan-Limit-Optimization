"""
Module for the daily MILP optimization model.
"""

import pandas as pd
import pulp
from config.constants import (
    PROFIT_ON_TIME,
    DEFAULT_INCREASE_PCT,
    DEFAULT_RECOVERY_RATE,
    LOSS_REALIZATION_PCT,
    DEFAULT_RISK_APPETITE
)

class DailyOptimizationModel:
    """
    MILP model for daily loan limit increase decisions.
    """

    def __init__(self, daily_eligible_cohort: pd.DataFrame, scenario_params: dict):
        self.cohort = daily_eligible_cohort.copy()
        self.scenario = scenario_params
        self.problem = pulp.LpProblem("Daily_Loan_Limit_Optimization", pulp.LpMaximize)
        self.decision_vars = None

    def _prepare_data(self):
        """Calculate LGD and Expected Profit for each customer."""
        # LGD = Loss Realization * EAD * (1 - Recovery Rate)
        # EAD = Initial Loan * (1 + Increase Pct)
        # For this model, we only consider the increase amount as the exposure for LGD
        increase_amount = self.cohort['initial_loan'] * self.scenario['increase_pct']
        ead = self.cohort['initial_loan'] + increase_amount
        
        # Per docs: LGD_i = 0.5 * (1.2 * Initial_Loan_i) * 0.9
        self.cohort['lgd'] = 0.5 * (1 + self.scenario['increase_pct']) * self.cohort['initial_loan'] * (1 - self.scenario['recovery_rate'])

        # Expected Profit = P(Accept) * [ (1 - P(Default)) * Profit - P(Default) * LGD ]
        profit_if_good = (1 - self.cohort['p_default']) * PROFIT_ON_TIME
        loss_if_bad = self.cohort['p_default'] * self.cohort['lgd']
        self.cohort['expected_profit'] = self.cohort['p_accept'] * (profit_if_good - loss_if_bad)

    def _build_model(self):
        """Build the MILP model with objective and constraints."""
        customers = self.cohort['customer_id'].tolist()
        
        # Decision variables
        self.decision_vars = pulp.LpVariable.dicts("Offer", customers, 0, 1, pulp.LpBinary)

        # Objective function
        expected_profits = dict(zip(self.cohort['customer_id'], self.cohort['expected_profit']))
        self.problem += pulp.lpSum([self.decision_vars[i] * expected_profits[i] for i in customers]), "Total_Expected_Profit"

        # Constraints
        # 1. Daily Capital Allocation
        increase_amounts = dict(zip(self.cohort['customer_id'], self.cohort['initial_loan'] * self.scenario['increase_pct']))
        # Use the capital limit from the scenario dictionary
        self.problem += pulp.lpSum([self.decision_vars[i] * increase_amounts[i] for i in customers]) <= self.scenario['daily_capital_limit'], "Daily_Capital_Allocation"

        # 2. Daily Portfolio Risk
        if self.scenario.get('risk_appetite') is not None:
            default_probs = dict(zip(self.cohort['customer_id'], self.cohort['p_default']))
            self.problem += pulp.lpSum([self.decision_vars[i] * default_probs[i] for i in customers]) <= self.scenario['risk_appetite'] * pulp.lpSum([self.decision_vars[i] for i in customers]), "Daily_Portfolio_Risk"

    def solve(self, verbose=False, time_limit=30):
        """Solve the optimization problem.

        Args:
            verbose: Whether to print solver output
            time_limit: Maximum solver time in seconds (default: 30)
        """
        self._prepare_data()
        self._build_model()

        # Use CBC with aggressive options for speed
        solver = pulp.PULP_CBC_CMD(
            msg=verbose,
            timeLimit=time_limit,
            options=[
                'presolve on',
                'cuts off',  # Disable cut generation for speed
                'heuristics on',  # Enable heuristics for faster feasible solutions
            ]
        )
        self.problem.solve(solver)

        decisions = {}
        for v in self.problem.variables():
            cust_id = int(v.name.split('_')[1])
            decisions[cust_id] = v.varValue

        return decisions

    def get_optimal_cohort(self):
        """Return the cohort of customers who should receive an offer."""
        decisions = self.solve()
        optimal_ids = [cust_id for cust_id, decision in decisions.items() if decision == 1]
        return self.cohort[self.cohort['customer_id'].isin(optimal_ids)]
