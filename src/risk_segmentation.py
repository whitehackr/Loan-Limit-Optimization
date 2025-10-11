"""
Risk segmentation module for loan limit optimization.

Implements risk categorization based on on-time payment percentages
using configurable boundaries from constants.py.
"""

from typing import Union
import pandas as pd
from config.constants import RISK_CATEGORIES


def assign_risk_category(ontime_pct: float) -> str:
    """
    Assign risk category based on on-time payment percentage.

    Uses explicit boundary handling with categories from constants.py:
    - Prime: [95, 100]
    - Near-Prime: [90, 95)
    - Subprime: [85, 90)
    - High-Risk: [80, 85)

    Parameters
    ----------
    ontime_pct : float
        On-time payment percentage (0-100)

    Returns
    -------
    str
        Risk category name

    Raises
    ------
    ValueError
        If on-time payment percentage is outside expected range [80, 100]

    Examples
    --------
    >>> assign_risk_category(97.5)
    'Prime'
    >>> assign_risk_category(92.3)
    'Near-Prime'
    >>> assign_risk_category(87.1)
    'Subprime'
    >>> assign_risk_category(82.5)
    'High-Risk'
    """
    if ontime_pct >= 95.0:
        return 'Prime'
    elif ontime_pct >= 90.0:
        return 'Near-Prime'
    elif ontime_pct >= 85.0:
        return 'Subprime'
    elif ontime_pct >= 80.0:
        return 'High-Risk'
    else:
        raise ValueError(
            f"On-time payment {ontime_pct}% outside expected range [80, 100]. "
            "All customers should have ≥80% on-time payments to be eligible."
        )


def assign_risk_categories_bulk(df: pd.DataFrame,
                                ontime_col: str = 'on-time_payments') -> pd.Series:
    """
    Assign risk categories to multiple customers at once.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing on-time payment data
    ontime_col : str, default='on-time_payments'
        Name of column containing on-time payment percentages

    Returns
    -------
    pd.Series
        Risk categories for each customer

    Raises
    ------
    KeyError
        If ontime_col not found in DataFrame
    ValueError
        If any on-time payment percentage is outside expected range

    Examples
    --------
    >>> df['risk_category'] = assign_risk_categories_bulk(df)
    """
    if ontime_col not in df.columns:
        raise KeyError(f"Column '{ontime_col}' not found in DataFrame")

    return df[ontime_col].apply(assign_risk_category)


def validate_risk_distribution(df: pd.DataFrame,
                               risk_col: str = 'risk_category') -> pd.DataFrame:
    """
    Validate and summarize risk category distribution.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame with risk categories assigned
    risk_col : str, default='risk_category'
        Name of risk category column

    Returns
    -------
    pd.DataFrame
        Summary statistics by risk category
    """
    summary = df.groupby(risk_col).size().reset_index(name='count')
    summary['percentage'] = (summary['count'] / len(df) * 100).round(2)

    # Ensure all categories are present (even if count is 0)
    expected_categories = ['Prime', 'Near-Prime', 'Subprime', 'High-Risk']
    for cat in expected_categories:
        if cat not in summary[risk_col].values:
            summary = pd.concat([
                summary,
                pd.DataFrame({risk_col: [cat], 'count': [0], 'percentage': [0.0]})
            ], ignore_index=True)

    # Sort by risk level (Prime first)
    category_order = {'Prime': 0, 'Near-Prime': 1, 'Subprime': 2, 'High-Risk': 3}
    summary['_sort_order'] = summary[risk_col].map(category_order)
    summary = summary.sort_values('_sort_order').drop('_sort_order', axis=1)

    return summary.reset_index(drop=True)
