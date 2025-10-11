"""
Module for the Monte Carlo simulation engine.
"""

import pandas as pd
import numpy as np
from tqdm import tqdm
from config.constants import (
    SIMULATION_DAYS,
    ANNUAL_REGULATORY_LIMIT,
    PROFIT_ON_TIME,
    ANNUAL_DISCOUNT_RATE,
    ELIGIBILITY_DAYS
)
from src.optimization import DailyOptimizationModel
from src.risk_model import CreditRiskTransitionMatrix

class MonteCarloSimulation:
    """
    Monte Carlo simulation for strategic forecasting.
    """

    def __init__(self, initial_df: pd.DataFrame, demand_model, scenario: dict, n_iterations: int = 100):
        self.initial_df = initial_df.copy()
        self.demand_model = demand_model
        self.scenario = scenario
        self.n_iterations = n_iterations
        self.risk_model = CreditRiskTransitionMatrix(risk_multiplier=scenario.get('risk_multiplier', 2.0))
        self.results = []

    def _initialize_run_df(self):
        """Initialize the state DataFrame for a single simulation run."""
        run_df = self.initial_df.copy()
        run_df['days_since_increase'] = run_df['days_since_last_loan']
        run_df['cumulative_increases'] = run_df['no_of_increases_in_2023']
        run_df['is_active'] = True
        run_df['p_default'] = run_df['risk_category'].apply(self.risk_model.get_default_probability)
        run_df['p_accept'] = self.demand_model.predict_proba(run_df, apply_macro_adjustment=True)
        return run_df

    def run_simulation(self, verbose=True):
        """Run the full Monte Carlo simulation using vectorized operations."""
        
        iterator = range(self.n_iterations)
        if verbose:
            iterator = tqdm(iterator, desc="Running Monte Carlo Simulation")

        for i in iterator:
            run_df = self._initialize_run_df()
            daily_outcomes = []
            total_increase_volume = 0

            for day in range(1, SIMULATION_DAYS + 1):
                active_mask = run_df['is_active']
                run_df.loc[active_mask, 'days_since_increase'] += 1

                eligible_mask = active_mask & (run_df['days_since_increase'] >= ELIGIBILITY_DAYS)
                if not eligible_mask.any():
                    continue

                eligible_cohort_df = run_df[eligible_mask].copy()

                if self.scenario.get('risk_appetite') is None:
                    offers_to_make_ids = eligible_cohort_df['customer_id']
                else:
                    optimizer = DailyOptimizationModel(eligible_cohort_df, self.scenario)
                    optimal_decisions = optimizer.solve()
                    offers_to_make_ids = [cid for cid, decision in optimal_decisions.items() if decision == 1]

                if not offers_to_make_ids:
                    continue
                
                offers_mask = run_df['customer_id'].isin(offers_to_make_ids)
                n_offers = offers_mask.sum()

                # Vectorized Stochastic Events
                # Acceptance
                accepted_rand = np.random.rand(n_offers)
                accepted_sub_mask = accepted_rand < run_df.loc[offers_mask, 'p_accept']
                accepted_ids = run_df.loc[offers_mask][accepted_sub_mask].index
                accepted_mask = run_df.index.isin(accepted_ids)

                if not accepted_mask.any():
                    continue

                # Regulatory limit check (vectorized)
                increase_amounts = run_df.loc[accepted_mask, 'initial_loan'] * self.scenario['increase_pct']
                cumulative_increase_amounts = increase_amounts.cumsum() + total_increase_volume
                
                allowed_increases_mask = cumulative_increase_amounts <= ANNUAL_REGULATORY_LIMIT
                allowed_ids = increase_amounts[allowed_increases_mask].index
                allowed_mask = run_df.index.isin(allowed_ids)
                
                total_increase_volume += increase_amounts[allowed_increases_mask].sum()

                if not allowed_mask.any():
                    continue

                # Default
                n_allowed = allowed_mask.sum()
                default_rand = np.random.rand(n_allowed)
                default_sub_mask = default_rand < run_df.loc[allowed_mask, 'p_default']
                default_ids = run_df.loc[allowed_mask][default_sub_mask].index
                default_mask = run_df.index.isin(default_ids)

                success_mask = allowed_mask & ~default_mask

                # Calculate outcomes
                discount_factor = (1 + ANNUAL_DISCOUNT_RATE) ** (day / 365)
                
                # Default outcomes
                if default_mask.any():
                    lgd = 0.5 * (1 + self.scenario['increase_pct']) * run_df.loc[default_mask, 'initial_loan'] * (1 - self.scenario['recovery_rate'])
                    npv = -lgd / discount_factor
                    run_df.loc[default_mask, 'is_active'] = False
                    for cid, val, outcome in zip(run_df.loc[default_mask, 'customer_id'], npv, -lgd):
                        daily_outcomes.append({'day': day, 'cid': cid, 'npv': val, 'outcome': outcome})

                # Success outcomes
                if success_mask.any():
                    single_npv = PROFIT_ON_TIME / discount_factor
                    run_df.loc[success_mask, 'cumulative_increases'] += 1
                    run_df.loc[success_mask, 'days_since_increase'] = 0
                    for cid in run_df.loc[success_mask, 'customer_id']:
                        daily_outcomes.append({'day': day, 'cid': cid, 'npv': single_npv, 'outcome': PROFIT_ON_TIME})
                    
                    # State Transition for successful customers
                    old_cats = run_df.loc[success_mask, 'risk_category'].copy()
                    new_cats = old_cats.apply(self.risk_model.simulate_transition)
                    run_df.loc[success_mask, 'risk_category'] = new_cats
                    
                    # Compare the two series which have the same index
                    changed_within_success = (old_cats != new_cats)
                    
                    # Get the original DataFrame indices for the changed customers
                    changed_indices = old_cats[changed_within_success].index

                    # Update p_default for those who changed
                    if not changed_indices.empty:
                         run_df.loc[changed_indices, 'p_default'] = run_df.loc[changed_indices, 'risk_category'].apply(self.risk_model.get_default_probability)


            # End of year: summarize run
            total_npv = sum(o['npv'] for o in daily_outcomes)
            total_defaults = sum(1 for o in daily_outcomes if o['outcome'] < 0)
            self.results.append({
                'iteration': i,
                'total_npv': total_npv,
                'total_defaults': total_defaults,
                'total_increase_volume': total_increase_volume
            })
            
        return pd.DataFrame(self.results)