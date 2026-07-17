"""
Configuration file for Maintenance-Operations-Analytics ETL project.
Stores paths, filenames, column names, business rules, thresholds, and report names.
No business logic here.
"""

from pathlib import Path

# Project Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_DIR = BASE_DIR / "logs"

LANDING_DIR = DATA_DIR / "01_landing"
VALIDATION_DIR = DATA_DIR / "02_validation"
CLEAN_DIR = DATA_DIR / "03_clean"
WAREHOUSE_DIR = DATA_DIR / "04_DataWarehouse"

# File Names
FILES = {
    "cases": "Cases.xlsx",
    "spareparts": "SpareParts.xlsx",
    "replacement": "Replacement.xlsx",
}

# Column Names
COLUMNS = {
    "cases": ["CaseID", "CustomerName", "DateOpened", "WarrantyStatus", "EngineerID", "DefectCode"],
    "spareparts": ["PartID", "CaseID", "PartName", "Quantity"],
    "replacement": ["ReplacementID", "CaseID", "ProductCode", "DateReplaced"],
}

# Business Rules
BUSINESS_RULES = {
    "warranty_status": ["VALID", "EXPIRED", "UNKNOWN"],
    "date_format": "%Y-%m-%d",
}

# Quality Thresholds
QUALITY_THRESHOLDS = {
    "missing_values": 0.05,  # 5% allowed
    "duplicate_records": 0.02,  # 2% allowed
}

# Report Names
REPORTS = {
    "validation": "Validation_Report.xlsx",
}
