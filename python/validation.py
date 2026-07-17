"""
Validation script for CRM landing data.
Generates Validation_Report.xlsx and logs/validation.log
"""

import pandas as pd
from pathlib import Path
from colorama import Fore, Style
from python import config, utils

def validate_cases(df: pd.DataFrame, logger):
    issues = []
    # Duplicate Records
    dup = df[df.duplicated(subset=["CaseID"], keep=False)]
    if not dup.empty:
        issues.append(("Duplicate Records", dup))

    # Blank Primary Keys
    blank = df[df["CaseID"].isna()]
    if not blank.empty:
        issues.append(("Blank Primary Keys", blank))

    # Missing Values
    missing = df[df.isna().any(axis=1)]
    if not missing.empty:
        issues.append(("Missing Values", missing))

    # Invalid Dates
    invalid_dates = df[pd.to_datetime(df["DateOpened"], errors="coerce").isna()]
    if not invalid_dates.empty:
        issues.append(("Invalid Dates", invalid_dates))

    # Invalid Warranty Status
    invalid_warranty = df[~df["WarrantyStatus"].isin(config.BUSINESS_RULES["warranty_status"])]
    if not invalid_warranty.empty:
        issues.append(("Invalid Warranty Status", invalid_warranty))

    return issues

def main():
    utils.print_header("VALIDATION PROCESS STARTED")
    utils.create_folder(config.VALIDATION_DIR)
    utils.create_folder(config.LOG_DIR)

    log_file = config.LOG_DIR / "validation.log"
    logger = utils.get_logger(log_file)

    # Read files
    cases = utils.read_excel(config.LANDING_DIR / config.FILES["cases"])
    spareparts = utils.read_excel(config.LANDING_DIR / config.FILES["spareparts"])
    replacement = utils.read_excel(config.LANDING_DIR / config.FILES["replacement"])

    # Validate Cases
    issues = validate_cases(cases, logger)

    # Build report
    summary = []
    failed_records = pd.DataFrame()
    for issue_name, df in issues:
        summary.append({"Issue": issue_name, "Count": len(df)})
        failed_records = pd.concat([failed_records, df])

    score = utils.data_quality_score(len(cases), len(failed_records))
    status = utils.status_message(score, config.QUALITY_THRESHOLDS["missing_values"])

    summary_df = pd.DataFrame(summary)
    score_df = pd.DataFrame([{"Data Quality Score": score, "Status": status}])

    report_path = config.VALIDATION_DIR / config.REPORTS["validation"]
    utils.save_excel(
        {
            "Validation Summary": summary_df,
            "Failed Records": failed_records,
            "Data Quality Score": score_df,
        },
        report_path,
    )

    # Logging
    logger.info("Validation completed")
    logger.info(f"Data Quality Score: {score}% - Status: {status}")

    # Terminal output
    print(Fore.GREEN + f"Validation completed. Score: {score}% - Status: {status}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
