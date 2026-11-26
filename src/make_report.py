import os
import pandas as pd
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

os.makedirs("docs", exist_ok=True)
doc = Document()

# Page margins for tight, clean 3-page layout
for sec in doc.sections:
    sec.top_margin = Inches(0.6)
    sec.bottom_margin = Inches(0.6)
    sec.left_margin = Inches(0.65)
    sec.right_margin = Inches(0.65)

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(9.5)
style.paragraph_format.space_after = Pt(3)
style.paragraph_format.line_spacing = 1.08

def add_h1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(11.5)
    r.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)
    return p

def add_table(headers, rows):
    tbl = doc.add_table(rows=1 + len(rows), cols=len(headers))
    tbl.style = "Table Grid"
    for j, h in enumerate(headers):
        cell = tbl.rows[0].cells[j]
        cell.text = str(h)
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(1)
            for r in p.runs:
                r.bold = True
                r.font.size = Pt(8.5)
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = tbl.rows[i + 1].cells[j]
            cell.text = str(val)
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(1)
                for r in p.runs:
                    r.font.size = Pt(8.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(1)

title = doc.add_paragraph()
title.paragraph_format.space_after = Pt(2)
rt = title.add_run("Draft AI-Assisted Extraction & QAQC Pipeline for DayCent Model Inputs")
rt.bold = True
rt.font.size = Pt(14)
rt.font.color.rgb = RGBColor(0x1B, 0x43, 0x32)

sub = doc.add_paragraph()
sub.paragraph_format.space_after = Pt(4)
rs = sub.add_run("MRV & Methodology Report | Varaha Agri-Carbon Assignment | Indo-Gangetic Plain Field Trials")
rs.italic = True
rs.font.size = Pt(9)

# 1. PURPOSE AND SCOPE
add_h1("1. Purpose and Scope")
doc.add_paragraph(
    "This report documents a semi-automated extraction and quality assurance/quality control (QAQC) pipeline "
    "designed to convert agronomy and soil carbon research papers into structured, traceable inputs for the DayCent "
    "biogeochemical model in support of Monitoring, Reporting, and Verification (MRV) workflows. Three Indo-Gangetic "
    "Plain (IGP) rice-wheat and diversified cereal-legume studies were processed: Pandey et al. (2012) (BHU Varanasi, "
    "rice-wheat tillage permutations & GHGs, 2003-2010), Ghosh et al. (2017) (ICAR-IIPR Kanpur, lowland RW/RWRC and "
    "upland MW/MWMC with chickpea & nutrient/residue treatments, 2003-2011), and Sarkar & Kar (2011) (IIT Kharagpur, "
    "transplanted/direct-seeded rice-wheat tillage, residue & N rates, 2001-2003). Data were mapped into a long-format "
    "schema (paper_name, site, treatment, depth_cm, variable, value, unit, source, confidence) and organized into "
    "DayCent-aligned workbook sheets (A_site through G_end_soil, plus treatments, sources, and QAQC)."
)

# 2. METHOD
add_h1("2. Method, Architecture, and Tool Justification")
doc.add_paragraph(
    "Pipeline Flow: PDF Papers -> Text/Table Inspection & Structured Extraction (long CSV per paper) -> "
    "Dataset Builder (src/build_dataset.py -> master_long.csv & daycent_extracted.xlsx) -> Automated QAQC "
    "(src/qaqc.py -> outputs/logs/qaqc_log.csv) -> Stratified Accuracy Audit (src/accuracy_audit.py -> "
    "outputs/logs/accuracy_audit.csv). "
    "Tools & Model Choice: Python with pandas and openpyxl provides deterministic schema normalization, auditability, "
    "and direct Excel generation; Google Gemini models via google-genai were selected for zero-cost prototyping "
    "under free-tier constraints, while structuring prompts and schemas to remain model-agnostic. "
    "Alternatives Rejected: Pure regex/rule-based PDF parsers fail on multi-column academic layouts, split tables, "
    "and narrative agronomic schedules; paid commercial LLM APIs were avoided due to budget constraints; fully "
    "automated chart digitizers were omitted for figure-only series to prevent unverified reading of dense axes."
)

# 3. DATA
add_h1("3. Extracted Dataset Summary, Completeness, and Missing DayCent Inputs")
df = pd.read_csv(os.path.join("outputs", "excel", "master_long.csv"))
non_na = df[df["value"].notna() & (~df["value"].astype(str).str.startswith("NA"))]

summary_rows = []
for p, g in df.groupby("paper_name"):
    n_tot = len(g)
    n_val = len(g[g["value"].notna() & (~g["value"].astype(str).str.startswith("NA"))])
    pct = (n_val / n_tot * 100) if n_tot else 0
    summary_rows.append([p, n_tot, n_val, n_tot - n_val, f"{pct:.1f}%"])
summary_rows.append(["TOTAL", len(df), len(non_na), len(df) - len(non_na), f"{len(non_na)/len(df)*100:.1f}%"])
add_table(["Paper", "Total Rows", "Populated", "NA / Missing", "Populated %"], summary_rows)

doc.add_paragraph(
    "Missing DayCent Inputs Across Papers: None of the three PDFs provide daily weather series (Tmax, Tmin, "
    "precipitation required by DayCent weather files), volumetric soil field capacity (DUL) or wilting point (LL15), "
    "or numeric straw/stover biomass yields. Ghosh_2017 lacks soil bulk density, sand/silt/clay percentages, and "
    "exact irrigation dates/depths; Pandey_2012 lacks exact wheat sowing/harvest dates and irrigation volumes; "
    "Sarkar_2011 reports SOC end-values as marginal means without depth in Table 2 and lacks exact irrigation dates."
)

# 4. QAQC
add_h1("4. QAQC Checks and Errors Caught")
doc.add_paragraph(
    "Automated QAQC checks (src/qaqc.py) protect DayCent parameterization against physically impossible soil "
    "hydraulics, wrong mass balances, and misread table values. Texture closure (sand + silt + clay = 100%) and "
    "Ghosh C-fraction mass balance (Cfrac1..4 sum = TOC across 30 rows) passed. Key failures/warnings caught: "
    "(1) Pandey Table 1 reports bulk density = 2.53 g/cm3 for RNT-WNT (implausible for sandy loam) and inconsistent "
    "SE/units; (2) Sarkar Table 1 0-15 cm OC (0.36% = 3.6 g/kg) with total N (0.04 g/kg) implies C:N = 90 (likely "
    "0.04% = 0.40 g/kg N, C:N = 9); (3) Sarkar Table 3 text vs. table mismatches on T1 BD/SHC and Table 4 "
    "identical BD rows for T3 and T4; (4) Ghosh initial SOC (2.8 g/kg) vs. control TOC (13.32-16.08 g/kg), FYM C "
    "cumulative mismatch (448 kg/ha/yr * 8 yr = 3.58 Mg C vs. 6.5 Mg C in Table 2), 50.31 typo, and April-June "
    "chickpea window."
)

# 5. ASSUMPTIONS, UNCERTAINTY, AND LIMITATIONS
add_h1("5. Assumptions, Uncertainty, and Limitations")
doc.add_paragraph(
    "Assumptions & Sources: Missing soil hydraulic properties (field capacity, wilting point) should be estimated via "
    "Saxton & Rawls (2006) pedotransfer functions using texture and organic matter; daily weather should be sourced "
    "from gridded/station reanalysis (e.g., NASA POWER or IMD) with annual rainfall cross-checked against paper "
    "totals; Walkley-Black OC in Sarkar/Pandey requires standard correction/conversion awareness for DayCent SOM pools. "
    "AI Reliability & Human Review: In a 40-row audit against PDFs, 38/40 (95.0%) were exact matches, 1/40 (2.5%) "
    "matched a source paper typo (50.31), and 1/40 (2.5%) had a column-alignment error (Sarkar Table 5 SHC). "
    "Mandatory human review is required before running DayCent for: all QAQC FAIL/WARN items, marginal vs. "
    "interaction treatment mappings, figure-only values, and any pedotransfer/weather gap-filling."
)

# 6. CONCLUSION AND NEXT STEPS
add_h1("6. Conclusion and Next Steps for Scaling")
doc.add_paragraph(
    "An LLM-assisted extraction pipeline paired with deterministic code-based QAQC and page-level citations "
    "accelerates literature-to-DayCent ingestion while surfacing scientific ambiguities that blind automation would "
    "miss. To scale from 3 papers to hundreds in an MRV pipeline: (1) add deterministic table/layout pre-parsers "
    "(e.g., pdfplumber/Camelot) with bounding-box citations; (2) enforce strict Pydantic schemas and multi-model "
    "or self-consistency checks on numeric tables; (3) automate unit normalization (kg/ha, Mg/ha, %, g/kg) and "
    "external weather/SoilsGrids enrichment; and (4) route only low-confidence or QAQC-flagged rows to a human "
    "agronomist review queue."
)

out_docx = os.path.join("docs", "Varaha_DayCent_Extraction_Report.docx")
doc.save(out_docx)
print("Saved report to:", out_docx)
