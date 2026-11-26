# Varaha DayCent Extraction & QAQC Pipeline

Semi-automated pipeline to extract DayCent model input data from agronomy research PDFs (`Pandey_2012.pdf`, `Ghosh_2017.pdf`, `Sarkar_2011.pdf`) into structured long-format CSV and Excel workbooks, run automated QAQC checks, audit extraction accuracy, and generate a technical MRV report.

## Repository Structure

- `papers/` — Source research PDFs
- `src/build_dataset.py` — Builds `outputs/excel/master_long.csv` and `outputs/excel/daycent_extracted.xlsx`
- `src/qaqc.py` — Runs automated QAQC checks and generates `outputs/logs/qaqc_log.csv`
- `src/accuracy_audit.py` — Audits 40 sampled values against source PDFs and generates `outputs/logs/accuracy_audit.csv`
- `src/make_report.py` — Generates the MRV methodology report at `docs/Varaha_DayCent_Extraction_Report.docx`
- `outputs/csv/` — Raw per-paper long-format extraction CSVs

## Installation

Install dependencies:

    pip install -r requirements.txt

## Run Commands

    python src\build_dataset.py
    python src\qaqc.py
    python src\accuracy_audit.py
    python src\make_report.py
