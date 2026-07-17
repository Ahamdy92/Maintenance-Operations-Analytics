"""
Cleaning script for CRM data.
Reads from validation or landing, cleans, and exports to 03_clean.
"""

import pandas as pd
from pathlib import Path
from python import config, utils

def clean_cases(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # Trim Spaces
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    # Normalize Text
    df["CustomerName"] = df["CustomerName"].str.title()
    # Uppercase Codes
    df["DefectCode"] = df["DefectCode"].str.upper()
    # Standardize Warranty Status
    df["WarrantyStatus"] = df["WarrantyStatus"].str.upper()
    # Fix Dates
    df["DateOpened"] = pd.to_datetime(df["DateOpened"], errors="coerce")
    # Remove Duplicates
    df = df.drop_duplicates(subset=["CaseID"])
    return df

def main():
    utils.print_header("CLEANING PROCESS STARTED")
    utils.create_folder(config.CLEAN_DIR)

    cases = utils.read_excel(config.LANDING_DIR / config.FILES["cases"])
    clean_cases_df = clean_cases(cases)

    clean_cases_df.to_excel(config.CLEAN_DIR / config.FILES["cases"], index=False)

    print("Cleaning completed. Files saved in 03_clean.")

if __name__ == "__main__":
    main()
