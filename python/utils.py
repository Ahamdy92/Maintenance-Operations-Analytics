"""
Utility functions for ETL pipeline.
Reusable helpers for reading/writing Excel, logging, timestamps, folders, printing headers, scoring, etc.
"""

import logging
from pathlib import Path
import pandas as pd
from datetime import datetime
from colorama import Fore, Style

# Logger setup
def get_logger(log_file: Path):
    logger = logging.getLogger(str(log_file))
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

# Read Excel
def read_excel(file_path: Path) -> pd.DataFrame:
    return pd.read_excel(file_path)

# Save Excel
def save_excel(df_dict: dict, file_path: Path):
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for sheet_name, df in df_dict.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)

# Timestamp
def get_timestamp() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Create Folder
def create_folder(path: Path):
    path.mkdir(parents=True, exist_ok=True)

# Print Header
def print_header(title: str):
    print(Fore.CYAN + "=" * 60)
    print(Fore.YELLOW + f"{title}")
    print(Fore.CYAN + "=" * 60 + Style.RESET_ALL)

# Data Quality Score
def data_quality_score(total_records: int, failed_records: int) -> float:
    if total_records == 0:
        return 0.0
    return round((1 - failed_records / total_records) * 100, 2)

# Status Function
def status_message(score: float, threshold: float) -> str:
    if score >= (100 - threshold * 100):
        return "PASS"
    elif score >= (100 - (threshold * 200)):
        return "WARNING"
    else:
        return "FAIL"
