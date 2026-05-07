"""Shared loaders, constants, and plot theme for the Math AI RCT analysis."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIGS = ROOT / "outputs" / "figures"
TABS = ROOT / "outputs" / "tables"

FIGS.mkdir(parents=True, exist_ok=True)
TABS.mkdir(parents=True, exist_ok=True)

# ── Treatment labels ──────────────────────────────────────────────────────────
TREATMENT_MAP = {0: "Control", 1: "T1 — Standard AI", 2: "T2 — Modified AI"}
TREATMENT_COLORS = {
    "Control": "#4C72B0",
    "T1 — Standard AI": "#DD8452",
    "T2 — Modified AI": "#55A868",
}

# ── Loaders ───────────────────────────────────────────────────────────────────

def load_baseline() -> pd.DataFrame:
    df = pd.read_csv(DATA / "baseline_estudiantes.csv", encoding="utf-8-sig", low_memory=False)
    return df

def load_schools() -> pd.DataFrame:
    df = pd.read_csv(DATA / "randomizacion_escuelas.csv", encoding="utf-8-sig")
    df["treatment_label"] = df["treatment"].map(TREATMENT_MAP)
    return df

def load_math_chat() -> pd.DataFrame:
    casa = pd.read_csv(DATA / "math_chat_casa.csv", encoding="utf-8-sig", parse_dates=["ts_created", "date_created"])
    casa["location"] = "home"
    escuela = pd.read_csv(DATA / "math_chat_escuela.csv", encoding="utf-8-sig", parse_dates=["ts_created", "date_created"])
    escuela["location"] = "school"
    return pd.concat([casa, escuela], ignore_index=True)

def load_math_quiz() -> pd.DataFrame:
    return pd.read_csv(DATA / "math_ponte_prueba.csv", encoding="utf-8-sig", parse_dates=["ts_created", "date_created"])

def load_voc_chat() -> pd.DataFrame:
    return pd.read_csv(DATA / "voc_chat.csv", encoding="utf-8-sig", parse_dates=["ts_created", "date_created"])

def load_voc_steps() -> pd.DataFrame:
    return pd.read_csv(DATA / "voc_steps.csv", encoding="utf-8-sig")

def load_all() -> dict[str, pd.DataFrame]:
    return {
        "baseline": load_baseline(),
        "schools": load_schools(),
        "math_chat": load_math_chat(),
        "math_quiz": load_math_quiz(),
        "voc_chat": load_voc_chat(),
        "voc_steps": load_voc_steps(),
    }

# ── Plot theme ────────────────────────────────────────────────────────────────

def set_theme():
    """Apply a clean, publication-ready matplotlib theme."""
    mpl.rcParams.update({
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": "#E5E5E5",
        "grid.linewidth": 0.8,
        "font.family": "sans-serif",
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.labelsize": 11,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.frameon": False,
    })

# ── Key variable groups (baseline) ────────────────────────────────────────────

# Variables used in the balance table and descriptives
BALANCE_VARS = {
    "Demographics": {
        "female": "Female",
        "age": "Age",
        "educ_parent_max": "Parent education (max yrs)",
        "has_computer": "Has computer at home",
        "has_internet": "Has internet at home",
    },
    "Academic": {
        "math_grade_prev": "Prior math grade",
        "score_pct_baseline": "Baseline math score (%)",
        "hours_study": "Study hours/day",
    },
    "Psychological scales (1–5)": {
        "grit_avg": "Grit",
        "mindset_avg": "Growth mindset",
        "locus_avg": "Locus of control",
        "efficacy_avg": "Self-efficacy",
        "math_enjoy_avg": "Math enjoyment",
        "math_anxiety_avg": "Math anxiety",
        "math_selfconcept_avg": "Math self-concept",
        "belonging_avg": "School belonging",
    },
    "Aspirations": {
        "plans_higher_ed": "Plans for higher education",
        "knows_career": "Has identified a career",
        "plan_feasibility": "Plan feasibility (self-assessed)",
    },
}

SCALE_VARS = [
    "grit_avg", "mindset_avg", "locus_avg", "efficacy_avg",
    "math_enjoy_avg", "math_anxiety_avg", "math_selfconcept_avg", "belonging_avg",
]
