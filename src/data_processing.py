"""
Data processing module for loan limit optimization system.

Handles data loading, cleaning, feature engineering, and preprocessing.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional


def load_raw_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load raw loan data from Excel file.

    Parameters
    ----------
    file_path : str, optional
        Path to the Excel file. If None, uses default path in data/raw/

    Returns
    -------
    pd.DataFrame
        Raw loan data with all original columns

    Raises
    ------
    FileNotFoundError
        If the specified file does not exist
    ValueError
        If the file cannot be read or is in incorrect format
    """
    if file_path is None:
        # Default path relative to project root
        project_root = Path(__file__).parent.parent
        file_path = project_root / "data" / "raw" / "loan_limit_increases.xlsx"

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"Data file not found at {file_path}")

    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        raise ValueError(f"Error reading Excel file: {e}")

    # Clean column names: lowercase and replace spaces with underscores
    df.columns = df.columns.str.lower().str.replace(' ', '_')

    return df


def get_data_info(df: pd.DataFrame) -> dict:
    """
    Extract comprehensive data information for EDA.

    Parameters
    ----------
    df : pd.DataFrame
        Input dataframe

    Returns
    -------
    dict
        Dictionary containing:
        - shape: tuple of (rows, columns)
        - columns: list of column names
        - dtypes: series of data types
        - missing: series of missing value counts
        - missing_pct: series of missing value percentages
    """
    info = {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes,
        'missing': df.isnull().sum(),
        'missing_pct': (df.isnull().sum() / len(df) * 100).round(2)
    }
    return info
