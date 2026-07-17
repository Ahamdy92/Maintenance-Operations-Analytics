"""
Warehouse script: builds star schema and saves CSV tables.
"""

import pandas as pd
from pathlib import Path
from python import config, utils

def build_dim_date(df: pd.DataFrame, date_col: str) -> pd.DataFrame:
    df = pd.DataFrame({"Date": pd.to_datetime(df[date_col].dropna().unique())})
    df["Year"] = df["Date"].dt.year
    df["Month"] =
