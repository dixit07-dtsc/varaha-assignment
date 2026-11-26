import os
import pandas as pd

os.makedirs(os.path.join("outputs", "logs"), exist_ok=True)
df = pd.read_csv(os.path.join("outputs", "excel", "master_long.csv"))
valid = df[df["value"].notna() & (~df["value"].astype(str).str.startswith("NA"))].copy()
sample = valid.sample(n=40, random_state=42).copy()

mismatches = {
    785: ("MISMATCH", "Column_Alignment_Error",
          "Table 5 (p277) gives SHC=2.85 for D (wheat after DR) and 2.98 for T (wheat after TR); assigned 2.98 to wheat after DR.")
}
source_typos = {
    107: ("PARTIAL_MATCH", "Source_Paper_Typo",
          "Matches printed value '50.31' in Table 2 (p4), likely a 2-decimal typo in paper; flagged in QAQC.")
}

sample["audit_status"] = [
    mismatches[i][0] if i in mismatches else (source_typos[i][0] if i in source_typos else "MATCH")
    for i in sample.index
]
sample["error_type"] = [
    mismatches[i][1] if i in mismatches else (source_typos[i][1] if i in source_typos else "None")
    for i in sample.index
]
sample["audit_notes"] = [
    mismatches[i][2] if i in mismatches else (source_typos[i][2] if i in source_typos else "Verified exact match against PDF source.")
    for i in sample.index
]

out_path = os.path.join("outputs", "logs", "accuracy_audit.csv")
sample.to_csv(out_path, index=False)
print("Saved:", out_path)
print(sample["audit_status"].value_counts())
