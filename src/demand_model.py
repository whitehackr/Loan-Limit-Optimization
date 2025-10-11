"""
Module for the Cox Proportional Hazards demand model.
"""

import pandas as pd
from lifelines import CoxPHFitter
import joblib

import numpy as np

class AcceptanceProbabilityModel:
    """Cox Proportional Hazards model for P(Accept)."""

    def __init__(self, macro_demand_factor: float = 1.0):
        self.macro_demand_factor = macro_demand_factor
        self.model = CoxPHFitter()

    def fit(self, df: pd.DataFrame):
        """Fit the Cox PH model."""
        df_survival = df.copy()

        # One-hot encode risk category (using lowercase convention)
        df_survival = pd.get_dummies(df_survival, columns=['risk_category'], drop_first=True)

        # Prepare data for lifelines
        df_lifelines = df_survival[[
            'no_of_increases_in_2023',
            'initial_loan',
            'days_since_last_loan',
            'risk_category_Near-Prime',
            'risk_category_Prime',
            'risk_category_Subprime'
        ]].copy()

        df_lifelines.rename(columns={'no_of_increases_in_2023': 'duration'}, inplace=True)
        df_lifelines['event'] = 1  # All are right-censored

        self.model.fit(df_lifelines, duration_col='duration', event_col='event')
        self.fitted_columns = df_lifelines.columns
        return self

    def predict_proba(self, df: pd.DataFrame, apply_macro_adjustment: bool = True) -> pd.Series:
        """Predict acceptance probability."""
        df_pred = df.copy()
        df_pred = pd.get_dummies(df_pred, columns=['risk_category'], drop_first=True)

        # Ensure columns match training columns
        for col in self.fitted_columns:
            if col not in df_pred.columns and col not in ['duration', 'event']:
                df_pred[col] = 0
        df_pred = df_pred[self.fitted_columns.drop(['duration', 'event'])]

        # Predict partial hazard
        hazard = self.model.predict_partial_hazard(df_pred)

        # Convert hazard to probability
        p_accept = 1 - np.exp(-hazard)

        if apply_macro_adjustment:
            p_accept *= self.macro_demand_factor

        # Clip probabilities to [0, 1]
        return p_accept.clip(0, 1)

    def save_model(self, filepath: str):
        """Save the trained model."""
        joblib.dump(self, filepath)

    @classmethod
    def load_model(cls, filepath: str):
        """Load a trained model."""
        return joblib.load(filepath)
