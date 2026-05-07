"""
Anonymize raw data files for public release.

Reads from data/, writes to data_public/.
A school crosswalk (data/crosswalk_schools.csv) is saved locally
to preserve the mapping between anonymized codes and real names.

Run from the project root:
    python src/anonymize.py
"""

import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
PUBLIC = ROOT / "data_public"
PUBLIC.mkdir(exist_ok=True)

# ── 1. School crosswalk ───────────────────────────────────────────────────────

schools_raw = pd.read_csv(DATA / "randomizacion_escuelas.csv", encoding="utf-8-sig")

schools_sorted = schools_raw.sort_values("school_id").reset_index(drop=True)
schools_sorted["school_name_anon"] = [
    f"School_{str(i+1).zfill(2)}" for i in range(len(schools_sorted))
]

crosswalk = schools_sorted[["school_id", "cod_mod", "ie_name", "school_name_anon"]].copy()
crosswalk.columns = ["school_id", "cod_mod_original", "school_name_original", "school_name_anon"]
crosswalk.to_csv(DATA / "crosswalk_schools.csv", index=False)
print(f"Crosswalk saved to data/crosswalk_schools.csv ({len(crosswalk)} schools)")

name_map = dict(zip(crosswalk["school_name_original"], crosswalk["school_name_anon"]))

# ── 2. randomizacion_escuelas ─────────────────────────────────────────────────

schools_anon = schools_sorted.copy()
schools_anon["ie_name"] = schools_anon["ie_name"].map(name_map)
schools_anon = schools_anon.drop(columns=["cod_mod"])
schools_anon.to_csv(PUBLIC / "randomizacion_escuelas.csv", index=False)
print(f"randomizacion_escuelas: {len(schools_anon)} rows")

# ── 3. baseline_estudiantes ───────────────────────────────────────────────────

baseline_raw = pd.read_csv(DATA / "baseline_estudiantes.csv", encoding="utf-8-sig", low_memory=False)

drop_cols = [
    # Direct identifiers
    "dni", "nombre", "apellido",
    # School display name (replaced below)
    "school_name",
    # Friend names (names of other students)
    "friend1_name", "friend2_name", "friend3_name", "friend4_name", "friend5_name",
    # Free-text fields that may contain names or identifying details
    "birth_country_other", "digital_tools_other", "barrier_finish_text",
    "institution_first_text", "plan_talks_other", "factors_career_other",
    "preferred_sector_other",
]

existing_drop = [c for c in drop_cols if c in baseline_raw.columns]
baseline_anon = baseline_raw.drop(columns=existing_drop)

baseline_anon.insert(
    baseline_anon.columns.get_loc("school_code") + 1,
    "school_name_anon",
    baseline_raw["school_name"].map(name_map),
)

baseline_anon.to_csv(PUBLIC / "baseline_estudiantes.csv", index=False)
print(f"baseline_estudiantes: {len(baseline_anon)} rows, {len(baseline_anon.columns)} cols "
      f"(dropped {len(existing_drop)} PII columns)")

# ── 4. voc_steps ─────────────────────────────────────────────────────────────

voc_steps_raw = pd.read_csv(DATA / "voc_steps.csv", encoding="utf-8-sig")

drop_voc = [
    "school_user_email", "school_user_username",
    "school_user_first_name", "school_user_last_name",
    "school_user_city", "school_user_country",
]
existing_drop_voc = [c for c in drop_voc if c in voc_steps_raw.columns]
voc_steps_anon = voc_steps_raw.drop(columns=existing_drop_voc)
voc_steps_anon.to_csv(PUBLIC / "voc_steps.csv", index=False)
print(f"voc_steps: {len(voc_steps_anon)} rows (dropped {len(existing_drop_voc)} PII columns)")

# ── 5. Chat and quiz files — published as-is (no direct PII) ─────────────────

passthrough_files = [
    "math_chat_casa.csv",
    "math_chat_escuela.csv",
    "math_ponte_prueba.csv",
    "voc_chat.csv",
]

for filename in passthrough_files:
    df = pd.read_csv(DATA / filename, encoding="utf-8-sig", low_memory=False)
    df.to_csv(PUBLIC / filename, index=False)
    print(f"{filename}: {len(df)} rows (no changes)")

print("\nDone. Anonymized files written to data_public/")
