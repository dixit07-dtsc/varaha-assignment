r"""Step 1: merge per-paper extracted CSVs -> harmonised long table -> Excel.
Usage (PowerShell): python src\build_dataset.py [csv_dir]
Default csv_dir = outputs\csv  (put extracted_*.csv there)
"""
import sys, glob, os
import pandas as pd

csv_dir = sys.argv[1] if len(sys.argv) > 1 else os.path.join("outputs", "csv")
out_dir = os.path.join("outputs", "excel")
os.makedirs(out_dir, exist_ok=True)

files = sorted(glob.glob(os.path.join(csv_dir, "extracted_*.csv")))
df = pd.concat([pd.read_csv(f, encoding="utf-8-sig") for f in files], ignore_index=True)

# --- harmonise synonyms (same quantity, different name across papers) ---
VAR_MAP = {
    "bulk_density_end": "bulk_density", "end_bulk_density": "bulk_density",
    "SOC_end": "SOC",
    "sat_hydraulic_conductivity_end": "sat_hydraulic_conductivity",
    "grain_yield_rice": "grain_yield", "rice_grain_yield": "grain_yield",
    "grain_yield_wheat": "grain_yield",
}
# keep the original name + crop so nothing is lost
df["variable_original"] = df["variable"]
df["crop"] = ""
df.loc[df.variable_original.isin(["grain_yield_rice", "rice_grain_yield"]), "crop"] = "rice"
df.loc[df.variable_original == "grain_yield_wheat", "crop"] = "wheat"
df["variable"] = df["variable"].replace(VAR_MAP)

# profile stage: initial vs end-of-experiment
df["soil_stage"] = ""
df.loc[df.category == "b_initial_soil", "soil_stage"] = "initial"
df.loc[df.category.str.startswith("g_end"), "soil_stage"] = "end"

CAT_SHEET = {
    "a_site": "A_site", "b_initial_soil": "B_initial_soil",
    "c_crop": "C_crops", "c_crops": "C_crops", "d_tillage": "D_tillage",
    "e_fertiliser": "E_fertiliser_organic", "e_fertiliser_organic": "E_fertiliser_organic",
    "f_irrigation": "F_irrigation", "g_end_soil": "G_end_soil",
    "g_end_soil_derived": "G_end_soil_derived",
}
df["sheet"] = df.category.map(CAT_SHEET)
df = df.sort_values(["paper_name", "sheet", "treatment", "variable", "depth_cm"], na_position="first")

cols = ["paper_name","site","treatment","depth_cm","variable","value","unit","source",
        "confidence","category","soil_stage","crop","variable_original","note"]
df[cols].to_csv(os.path.join(out_dir, "master_long.csv"), index=False, encoding="utf-8-sig")

# --- summary / completeness ---
summ = (df.assign(has_value=df.confidence.ne("missing"))
          .groupby(["paper_name","sheet"]).agg(rows=("variable","size"),
              filled=("has_value","sum"),
              n_text=("confidence", lambda s:(s=="text").sum()),
              n_table=("confidence", lambda s:(s=="table").sum()),
              n_figure=("confidence", lambda s:(s=="figure").sum()),
              n_missing=("confidence", lambda s:(s=="missing").sum())).reset_index())
summ["completeness_%"] = (100*summ.filled/summ.rows).round(1)

treat = df[["paper_name","treatment"]].drop_duplicates()
miss = df[df.confidence=="missing"][["paper_name","sheet","treatment","variable","note"]]

with pd.ExcelWriter(os.path.join(out_dir, "daycent_extracted.xlsx"), engine="openpyxl") as xw:
    df[cols].to_excel(xw, sheet_name="ALL_long", index=False)
    for sh, g in df.groupby("sheet"):
        g[cols].to_excel(xw, sheet_name=sh[:31], index=False)
    treat.to_excel(xw, sheet_name="Treatments", index=False)
    summ.to_excel(xw, sheet_name="Completeness", index=False)
    miss.to_excel(xw, sheet_name="Missing_inputs", index=False)
    # formatting
    for ws in xw.book.worksheets:
        ws.freeze_panes = "A2"
        for c in ws[1]:
            c.font = c.font.copy(bold=True, name="Arial")
        for col in ws.columns:
            w = max(len(str(c.value)) if c.value is not None else 0 for c in col[:200])
            ws.column_dimensions[col[0].column_letter].width = min(max(10, w + 2), 50)
print("rows:", len(df)); print(summ.to_string(index=False))
