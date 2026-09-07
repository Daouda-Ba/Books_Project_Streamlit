"""Fonctions de validation des donnees."""

from typing import Optional

import pandas as pd


def validate_dataframe(df: pd.DataFrame, min_rows: int = 1) -> bool:
    """Valide qu'un DataFrame existe et contient assez de lignes."""
    return df is not None and not df.empty and len(df) >= min_rows


def safe_access_column(
    df: pd.DataFrame, column: str, default: str = "N/A"
) -> pd.Series:
    """Retourne une colonne si elle existe, sinon une serie de valeurs par defaut."""
    if column not in df.columns:
        return pd.Series([default] * len(df), index=df.index)
    return df[column].fillna(default)


def truncate_title(title: Optional[str], max_len: int = 50) -> str:
    """Tronque un titre de maniere sure."""
    if title is None or pd.isna(title):
        return "Sans titre"

    title_str = str(title)
    return f"{title_str[:max_len]}..." if len(title_str) > max_len else title_str
