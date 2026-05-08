"""Shared loaders, constants, and plot theme for the Math AI RCT analysis."""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path
from great_tables import GT, style, loc

# ── Paths ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data_public"
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

# ── Baseline variable groups ──────────────────────────────────────────────────
# Comprehensive grouping of all analytical variables in baseline_estudiantes.
# Used for missing value checks, range validity, and descriptive analysis.
# Excludes identifiers (qualtrics_id, school_code, school_name_anon, classroom_section)
# and structurally empty columns.

BASELINE_VARS = {
    "Survey metadata": [
        "progress", "duration_min",
    ],
    "Demographics": [
        "birth_country", "age_cat", "age", "female", "male",
        "educ_mother", "educ_father", "educ_parent_max",
        "has_computer", "has_internet", "digital_comfort", "platform_use",
    ],
    "Academic background": [
        "math_grade_prev", "like_math", "like_communication",
        "rank_math", "rank_communication",
        "mathconf_learn", "mathconf_exam", "mathconf_help_peers", "mathconf_growth",
    ],
    "Computer lab": [
        "lab_productive", "lab_preferred_hours",
    ],
    "Hours & study habits": [
        "hours_school", "hours_study", "hours_friends", "hours_entertainment",
        "hours_housework", "hours_unpaid_work", "hours_paid_work",
        "hours_sleep", "hours_sport",
        "math_study_weekly", "study_context", "digital_tools_used",
    ],
    "Grit": [
        "grit_challenge", "grit_quit_game", "grit_lose_interest", "grit_hardwork",
        "grit_avg",
    ],
    "Growth mindset": [
        "mindset_fixed1", "mindset_fixed2", "mindset_avg",
    ],
    "Locus of control": [
        "locus_luck", "locus_fate", "locus_prepared", "locus_plans", "locus_avg",
    ],
    "Self-efficacy": [
        "efficacy_hard_problems", "efficacy_effort", "efficacy_calm",
        "efficacy_solutions", "efficacy_trouble", "efficacy_avg",
    ],
    "Math enjoyment": [
        "math_enjoy", "math_wish_no", "math_like_problems", "math_enjoy_avg",
    ],
    "Math anxiety": [
        "math_worry_grades", "math_nervous_exams", "math_anxiety_avg",
    ],
    "Math self-concept": [
        "math_does_well", "math_harder_than_peers", "math_selfconcept_avg",
    ],
    "Math attitudes": [
        "math_useful",
    ],
    "Belonging": [
        "belong_outsider", "belong_fits_in", "belonging_avg",
    ],
    "Metacognition": [
        "meta_study_allocation", "meta_when_stuck", "meta_hint_use",
        "meta_review_errors", "meta_self_awareness", "meta_after_mistake",
        "meta_ai_use", "meta_expected_exam", "meta_actual_exam",
    ],
    "Barriers": [
        "barrier_finish_school",
        "barrier_money", "barrier_work_family", "barrier_parent_ideas",
        "barrier_grades", "barrier_info_careers", "barrier_info_institution",
        "barrier_family_resp",
    ],
    "Aspirations": [
        "info_postsecondary", "plan_after_school", "knows_career",
        "institution_first_choice", "plan_feasibility", "plan_talks_with",
        "parent_educ_expectation", "enrolled_academy", "belief_univ_transition",
        "factors_career_choice", "plans_higher_ed", "preferred_sector",
        "knows_jobs_sector",
    ],
    "Knowledge of opportunities": [
        "knows_scholarship", "knows_beca18", "knows_alt_training",
        "est_years_technical", "est_years_university",
    ],
    "Labor market beliefs": [
        "salary_secondary", "salary_technical", "salary_university",
        "informal_secondary", "informal_technical", "informal_university",
    ],
    "Time & risk preferences": [
        "time_pref_100v150", "time_pref_100v300",
        "risk_pref_100v250", "risk_pref_100v500",
        "patient_low", "patient_high", "risk_seeking_low", "risk_seeking_high",
    ],
    "Social network": [
        "num_close_friends",
        "friend1_recess", "friend1_homework", "friend1_future_talk", "friend1_whatsapp",
        "friend2_recess", "friend2_homework", "friend2_future_talk", "friend2_whatsapp",
        "friend3_recess", "friend3_homework", "friend3_future_talk", "friend3_whatsapp",
        "friend4_recess", "friend4_homework", "friend4_future_talk", "friend4_whatsapp",
        "friend5_recess", "friend5_homework", "friend5_future_talk", "friend5_whatsapp",
    ],
    "Math assessment": [
        "correct_a1", "correct_a2", "correct_a3", "correct_a4", "correct_a5",
        "correct_a6", "correct_a7", "correct_a8", "correct_a8m", "correct_a9s",
        "qbl_v5_a1", "qbl_v5_a2", "qbl_v5_a3", "qbl_v5_a4", "qbl_v5_a5",
        "qbl_v5_a6", "qbl_v5_a7", "qbl_v5_a8", "qbl_v5_a8m", "qbl_v5_a9s",
        "score_total_baseline", "score_pct_baseline",
    ],
}

# ── Balance table variables (Phase 3) ────────────────────────────────────────
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
    "Psychological scales": {
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

# ── Table rendering ───────────────────────────────────────────────────────────

def gt_check_results(df: pd.DataFrame, title: str = "", subtitle: str = "") -> GT:
    """Render a checks.py results DataFrame as a formatted great_tables table.
    Rows where pass == False (or n_flagged > 0) are highlighted in red.
    """
    gt = (
        GT(df)
        .tab_header(title=title, subtitle=subtitle) if title else GT(df)
    )
    gt = GT(df)
    if title:
        gt = gt.tab_header(title=title, subtitle=subtitle)

    # Highlight flagged rows
    if "n_flagged" in df.columns:
        gt = gt.tab_style(
            style=style.fill(color="#FDECEA"),
            locations=loc.body(rows=lambda x: x["n_flagged"] > 0),
        )
    if "pass" in df.columns:
        gt = gt.tab_style(
            style=style.fill(color="#FDECEA"),
            locations=loc.body(rows=lambda x: x["pass"] == False),
        )

    return gt


def gt_missing(df: pd.DataFrame, title: str = "Missing values") -> GT:
    """Render a check_missing() result as a formatted great_tables table."""
    return (
        GT(df)
        .tab_header(title=title)
        .cols_label(
            group="Dimension",
            variable="Variable",
            n_missing="N Missing",
            pct_missing="% Missing",
        )
        .tab_style(
            style=style.borders(sides="top", weight="2px", color="#333333"),
            locations=loc.body(rows=[0]),
        )
        .tab_style(
            style=style.text(weight="bold"),
            locations=loc.title(),
        )
    )
