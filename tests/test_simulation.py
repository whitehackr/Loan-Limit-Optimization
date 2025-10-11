import pandas as pd
import pytest
from src.simulation import MonteCarloSimulation
from src.demand_model import AcceptanceProbabilityModel
from src.optimization import DailyOptimizationModel
from config.scenarios import SCENARIOS

@pytest.fixture
def sample_df():
    """Creates a sample DataFrame of 10 customers."""
    data = {
        'customer_id': range(10),
        'initial_loan': [1000] * 10,
        'days_since_last_loan': range(55, 65), # Some will be eligible, some not
        'no_of_increases_in_2023': [0] * 10,
        'risk_category': ['Prime'] * 10,
        'on-time_payments': [98.0] * 10,
        'total_profit_contribution': [0] * 10,
    }
    return pd.DataFrame(data)

@pytest.fixture
def mock_demand_model(sample_df):
    """Mocks the demand model to return a fixed probability."""
    class MockDemandModel:
        def predict_proba(self, df, apply_macro_adjustment=True):
            return pd.Series([0.5] * len(df), index=df.index)
    return MockDemandModel()

def test_weekly_batch_logic(monkeypatch, sample_df, mock_demand_model):
    """
    Tests that the optimizer is called only once per week.
    """
    # Spy on the DailyOptimizationModel.solve method
    call_log = []
    original_solve = DailyOptimizationModel.solve
    def spy_solve(self, *args, **kwargs):
        call_log.append(self.cohort) # Log the call
        return original_solve(self, *args, **kwargs)
    
    monkeypatch.setattr(DailyOptimizationModel, "solve", spy_solve)

    # Run a 15-day simulation
    scenario = SCENARIOS['baseline']
    # Temporarily reduce SIMULATION_DAYS for this test
    monkeypatch.setattr('src.simulation.SIMULATION_DAYS', 15)

    mc_sim = MonteCarloSimulation(
        initial_df=sample_df,
        demand_model=mock_demand_model,
        scenario=scenario,
        n_iterations=1 # Only one iteration needed to test the mechanics
    )
    
    mc_sim.run_simulation(verbose=False)

    # The optimizer should be called on day 1 and day 8.
    assert len(call_log) == 3, "Optimizer should be called three times in a 15-day simulation"

def test_simulation_runs_to_completion(sample_df, mock_demand_model):
    """
    Tests that the simulation runs end-to-end without errors and returns
    a correctly formatted DataFrame.
    """
    scenario = SCENARIOS['baseline']
    mc_sim = MonteCarloSimulation(
        initial_df=sample_df,
        demand_model=mock_demand_model,
        scenario=scenario,
        n_iterations=2 # Run a couple of iterations
    )
    
    results_df = mc_sim.run_simulation(verbose=False)

    assert isinstance(results_df, pd.DataFrame)
    assert len(results_df) == 2
    assert 'total_npv' in results_df.columns
    assert 'total_defaults' in results_df.columns
