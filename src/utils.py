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

# ── Variable labels ───────────────────────────────────────────────────────────
VARIABLE_LABELS: dict[str, str] = {
    # Survey metadata
    "progress":                    "Survey completion (%)",
    "duration_min":                "Duration (minutes)",
    # Demographics
    "birth_country":               "Birth country",
    "age":                         "Age",
    "age_cat":                     "Age category",
    "female":                      "Female",
    "male":                        "Male",
    "female / male":               "Female / Male",
    "educ_mother":                 "Mother's education",
    "educ_father":                 "Father's education",
    "educ_parent_max":             "Parent education (max)",
    "has_computer":                "Has computer at home",
    "has_internet":                "Has internet at home",
    "digital_comfort":             "Digital comfort",
    "platform_use":                "Platform use",
    # Academic background
    "math_grade_prev":             "Prior math grade",
    "like_math":                   "Likes math",
    "like_communication":          "Likes communication",
    "rank_math":                   "Self-rank in math",
    "rank_communication":          "Self-rank in communication",
    "mathconf_learn":              "Math confidence: learning",
    "mathconf_exam":               "Math confidence: exams",
    "mathconf_help_peers":         "Math confidence: helping peers",
    "mathconf_growth":             "Math confidence: growth",
    # Computer lab
    "lab_productive":              "Lab productivity",
    "lab_preferred_hours":         "Preferred lab hours",
    # Hours & study habits
    "hours_school":                "Hours at school",
    "hours_study":                 "Hours studying",
    "hours_friends":               "Hours with friends",
    "hours_entertainment":         "Hours on entertainment",
    "hours_housework":             "Hours on housework",
    "hours_unpaid_work":           "Hours on unpaid work",
    "hours_paid_work":             "Hours on paid work",
    "hours_sleep":                 "Hours sleeping",
    "hours_sport":                 "Hours on sport",
    "math_study_weekly":           "Math study frequency (weekly)",
    "study_context":               "Study context",
    "digital_tools_used":          "Digital tools used",
    # Grit
    "grit_challenge":              "Grit: overcomes challenges",
    "grit_quit_game":              "Grit: quits games (R)",
    "grit_lose_interest":          "Grit: loses interest (R)",
    "grit_hardwork":               "Grit: works hard",
    "grit_avg":                    "Grit (average)",
    # Growth mindset
    "mindset_fixed1":              "Fixed mindset item 1",
    "mindset_fixed2":              "Fixed mindset item 2",
    "mindset_avg":                 "Growth mindset (average)",
    # Locus of control
    "locus_luck":                  "Locus: luck determines outcomes",
    "locus_fate":                  "Locus: fate determines outcomes",
    "locus_prepared":              "Locus: being prepared matters",
    "locus_plans":                 "Locus: plans help succeed",
    "locus_avg":                   "Locus of control (average)",
    # Self-efficacy
    "efficacy_hard_problems":      "Efficacy: solves hard problems",
    "efficacy_effort":             "Efficacy: persists with effort",
    "efficacy_calm":               "Efficacy: stays calm",
    "efficacy_solutions":          "Efficacy: finds solutions",
    "efficacy_trouble":            "Efficacy: handles trouble",
    "efficacy_avg":                "Self-efficacy (average)",
    # Math enjoyment
    "math_enjoy":                  "Enjoys math",
    "math_wish_no":                "Wishes not to study math (R)",
    "math_like_problems":          "Likes math problems",
    "math_enjoy_avg":              "Math enjoyment (average)",
    # Math anxiety
    "math_worry_grades":           "Worried about math grades",
    "math_nervous_exams":          "Nervous about math exams",
    "math_anxiety_avg":            "Math anxiety (average)",
    # Math self-concept
    "math_does_well":              "Does well in math",
    "math_harder_than_peers":      "Math harder than peers (R)",
    "math_selfconcept_avg":        "Math self-concept (average)",
    # Math attitudes
    "math_useful":                 "Math is useful",
    # Belonging
    "belong_outsider":             "Feels like an outsider",
    "belong_fits_in":              "Fits in at school",
    "belonging_avg":               "School belonging (average)",
    # Metacognition
    "meta_study_allocation":       "Study time allocation",
    "meta_when_stuck":             "Strategy when stuck",
    "meta_hint_use":               "Hint use",
    "meta_review_errors":          "Reviews errors",
    "meta_after_mistake":          "Adjusts after mistake",
    "meta_ai_use":                 "AI use strategy",
    "meta_expected_exam":          "Expected exam score",
    "meta_actual_exam":            "Actual exam score",
    "meta_self_awareness":         "Self-awareness",
    # Barriers
    "barrier_finish_school":       "Barrier: finishing school",
    "barrier_money":               "Barrier: money",
    "barrier_work_family":         "Barrier: work/family obligations",
    "barrier_parent_ideas":        "Barrier: parent opinions",
    "barrier_grades":              "Barrier: grades",
    "barrier_info_careers":        "Barrier: career information",
    "barrier_info_institution":    "Barrier: institution information",
    "barrier_family_resp":         "Barrier: family responsibilities",
    # Aspirations
    "info_postsecondary":          "Post-secondary information",
    "plan_after_school":           "Plan after school",
    "plan_feasibility":            "Plan feasibility",
    "knows_career":                "Has identified a career",
    "institution_first_choice":    "First institution choice",
    "plan_talks_with":             "Discusses plans with",
    "parent_educ_expectation":     "Parent's education expectation",
    "enrolled_academy":            "Enrolled in academy",
    "belief_univ_transition":      "Belief in university transition",
    "factors_career_choice":       "Career choice factors",
    "plans_higher_ed":             "Plans for higher education",
    "preferred_sector":            "Preferred work sector",
    "knows_jobs_sector":           "Knows jobs in sector",
    # Knowledge of opportunities
    "knows_scholarship":           "Knows about scholarships",
    "knows_beca18":                "Knows about Beca 18",
    "knows_alt_training":          "Knows about alternative training",
    "est_years_technical":         "Estimated years (technical)",
    "est_years_university":        "Estimated years (university)",
    # Labor market beliefs
    "salary_secondary":            "Salary: secondary education",
    "salary_technical":            "Salary: technical education",
    "salary_university":           "Salary: university education",
    "salary_secondary / salary_technical / salary_university":
                                   "Salary ordering (secondary / technical / university)",
    "informal_secondary":          "Informality: secondary education",
    "informal_technical":          "Informality: technical education",
    "informal_university":         "Informality: university education",
    # Time & risk preferences
    "time_pref_100v150":           "Time preference: 100 vs 150",
    "time_pref_100v300":           "Time preference: 100 vs 300",
    "risk_pref_100v250":           "Risk preference: 100 vs 250",
    "risk_pref_100v500":           "Risk preference: 100 vs 500",
    "patient_low":                 "Patient (low stakes)",
    "patient_high":                "Patient (high stakes)",
    "risk_seeking_low":            "Risk-seeking (low stakes)",
    "risk_seeking_high":           "Risk-seeking (high stakes)",
    # Social network
    "num_close_friends":           "Number of close friends",
    **{f"friend{i}_{rel}": f"Friend {i}: {rel.replace('_', ' ')}"
       for i in range(1, 6)
       for rel in ["recess", "homework", "future_talk", "whatsapp"]},
    # Math assessment items
    "correct_a1":                  "Math item 1",
    "correct_a2":                  "Math item 2",
    "correct_a3":                  "Math item 3",
    "correct_a4":                  "Math item 4",
    "correct_a5":                  "Math item 5",
    "correct_a6":                  "Math item 6",
    "correct_a7":                  "Math item 7",
    "correct_a8":                  "Math item 8",
    "correct_a8m":                 "Math item 8M",
    "correct_a9s":                 "Math item 9S",
    # Derived / composite
    "score_total_baseline":        "Baseline math score (total items)",
    "score_pct_baseline":          "Baseline math score (%)",
    # Identifiers
    "qualtrics_id":                "Student ID (Qualtrics)",
}

# ── Table rendering ───────────────────────────────────────────────────────────

def gt_check_results(
    df: pd.DataFrame,
    title: str = "",
    subtitle: str = "",
    show_pass: bool = False,
) -> GT:
    """Render a checks.py results DataFrame as a formatted great_tables table.
    Rows where pass == False (or n_flagged > 0) are highlighted in red.
    Set show_pass=True to include the Pass column.
    """
    display_df = df.drop(columns=["pass"]) if "pass" in df.columns and not show_pass else df.copy()
    if "variable" in display_df.columns:
        display_df["variable"] = display_df["variable"].map(
            lambda v: VARIABLE_LABELS.get(v, v)
        )

    col_labels = {}
    if "variable" in display_df.columns:    col_labels["variable"]    = "Variable"
    if "check" in display_df.columns:       col_labels["check"]       = "Check"
    if "n_flagged" in display_df.columns:   col_labels["n_flagged"]   = "N Flagged"
    if "pct_flagged" in display_df.columns: col_labels["pct_flagged"] = "% Flagged"
    if "pass" in display_df.columns:        col_labels["pass"]        = "Pass"

    gt = GT(display_df)
    if title:
        gt = (
            gt.tab_header(title=title, subtitle=subtitle)
            .tab_style(style=style.text(weight="bold"), locations=loc.title())
        )
    gt = gt.cols_label(**col_labels)
    gt = gt.tab_style(
        style=style.borders(sides="top", weight="2px", color="#333333"),
        locations=loc.body(rows=[0]),
    )

    if "n_flagged" in df.columns:
        gt = gt.tab_style(
            style=style.fill(color="#FDECEA"),
            locations=loc.body(rows=lambda x: x["n_flagged"] > 0),
        )
    if show_pass and "pass" in df.columns:
        gt = gt.tab_style(
            style=style.fill(color="#FDECEA"),
            locations=loc.body(rows=lambda x: x["pass"] == False),
        )

    return gt


def gt_missing(df: pd.DataFrame, title: str = "Missing values") -> GT:
    """Render a check_missing() result as a formatted great_tables table."""
    display_df = df.copy()
    if "variable" in display_df.columns:
        display_df["variable"] = display_df["variable"].map(
            lambda v: VARIABLE_LABELS.get(v, v)
        )
    return (
        GT(display_df)
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
