"""
Module for the synthetic Markov transition matrix risk model.
"""

import numpy as np
import pandas as pd

class CreditRiskTransitionMatrix:
    """Manages the credit risk transition matrix."""

    def __init__(self, risk_multiplier: float = 2.0, transition_matrix: np.ndarray = None):
        self.risk_multiplier = risk_multiplier
        if transition_matrix is None:
            self.matrix = self.build_transition_matrix()
        else:
            self.matrix = transition_matrix
        self.states = ['Prime', 'Near-Prime', 'Subprime', 'High-Risk', 'Default']

    def build_transition_matrix(self) -> np.ndarray:
        """Build the synthetic transition matrix based on benchmarks."""
        # Matrix values from the design doc
        return np.array([
            # To Prime, Near-Prime, Subprime, High-Risk, Default
            [0.85, 0.10, 0.01, 0.00, 0.04],  # From Prime
            [0.05, 0.80, 0.05, 0.00, 0.10],  # From Near-Prime
            [0.00, 0.05, 0.60, 0.05, 0.30],  # From Subprime
            [0.00, 0.00, 0.05, 0.45, 0.50],  # From High-Risk
            [0.00, 0.00, 0.00, 0.00, 1.00],  # From Default
        ])

    def get_default_probability(self, risk_category: str) -> float:
        """Get the default probability for a given risk category."""
        try:
            state_index = self.states.index(risk_category)
            return self.matrix[state_index, -1]
        except ValueError:
            raise ValueError(f"Unknown risk category: {risk_category}")

    def simulate_transition(self, current_state: str) -> str:
        """Simulate the next state for a customer."""
        try:
            state_index = self.states.index(current_state)
            probabilities = self.matrix[state_index]
            return np.random.choice(self.states, p=probabilities)
        except ValueError:
            raise ValueError(f"Unknown risk category: {current_state}")

    def validate_matrix(self):
        """Validate the transition matrix."""
        assert np.allclose(self.matrix.sum(axis=1), 1.0), "Matrix rows must sum to 1.0"
        assert self.matrix[4, 4] == 1.0, "Default state must be absorbing"
