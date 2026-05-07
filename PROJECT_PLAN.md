# Math AI RCT — Portfolio Project Plan

## Goal
End-to-end data/research project showcasing: data quality assessment, descriptive analysis, and balance tests on a real RCT dataset (AI math tutoring, Lima Peru, ~1,200 students, 30 schools).

## Tools
- **Python** — `pandas`, `scipy`, `statsmodels`, `seaborn`, `matplotlib`, `great_tables`
- **Quarto** — reproducible HTML/PDF report (narrative + code + output in one file)
- **GitHub** — version control and public portfolio artifact
- **Quarto Pub** — free one-command publishing; link on CV/LinkedIn

---

## Directory Structure

```
math-ai-rct/
├── _quarto.yml
├── README.md
├── requirements.txt
├── data/               ← raw CSVs (gitignored or included)
├── src/
│   └── utils.py        ← reusable helpers (loaders, table formatters, plot themes)
└── report/
    ├── 00_index.qmd    ← executive summary + navigation
    ├── 01_data_quality.qmd
    ├── 02_descriptives.qmd
    └── 03_balance.qmd
```

---

## Phase 0 — Project Setup ✅
- [x] Initialize GitHub repo with clean directory structure
- [x] Set up Python virtual environment + `requirements.txt`
- [x] Configure Quarto project (`_quarto.yml`) targeting HTML output
- [x] Create stub `.qmd` files and `src/utils.py`

---

## Phase 1 — Data Quality Assessment (`01_data_quality.qmd`)

### 1a. Per-file completeness
- Missing rate per variable and per row, with a heatmap
- Flag variables with >10% and >50% missing

### 1b. Value validity
- Range checks on Likert scales (1–5), binary variables (0/1), timestamps (chronological order)
- Implausible values: negative message lengths, duplicate message IDs, zero-length conversations

### 1c. Merge quality
- How many students in `baseline_estudiantes` appear in each platform file?
- Orphaned platform IDs (users with no baseline record)
- Cross-validate school IDs between `randomizacion_escuelas` and `baseline_estudiantes`
- UpSet plot or coverage table across datasets

**Deliverable:** Summary table of issues per dataset + data quality scorecard

---

## Phase 2 — Descriptive Analysis (`02_descriptives.qmd`)

### 2a. Sample characteristics table (Table 1-style)
- Demographics, prior academic performance, psychological scales — overall + by treatment arm

### 2b. Platform engagement
- Message counts, conversation length, session frequency (math and vocational modules)
- Funnel chart: completion rates across the 8 vocational journey steps
- Time-on-platform distributions, flagging outliers

### 2c. Math performance
- `is_correct` distributions by topic/subtopic (`math_chat_escuela`, `math_ponte_prueba`)
- Baseline math score distribution

**Deliverable:** ~8–10 publication-quality figures + 2–3 summary tables

---

## Phase 3 — Balance Tests (`03_balance.qmd`)

### 3a. Covariate balance table
- Mean (SD) by arm (Control / T1 / T2)
- Pairwise t-test p-values (Control vs T1, Control vs T2, T1 vs T2)
- Standardized mean differences (Cohen's d)
- Key variables: gender, baseline math score, grit, self-efficacy, growth mindset, career aspiration index, prior grades, SES proxy

### 3b. Joint F-test
- Regress treatment indicator on all baseline covariates; report F-statistic and p-value

### 3c. Love plot (dot-whisker)
- Standardized differences for all covariates — standard RCT balance diagnostic

**Deliverable:** Formatted balance table (paper-ready) + love plot

---

## Phase 4 — Synthesis & Recommendations (`00_index.qmd`)
- Executive summary of data quality issues and implications for analysis
- Recommendations: which variables to use/avoid, which subsamples are clean, how to handle attrition, whether balance concerns warrant covariate adjustment
- Limitations section

---

## Deliverables Summary

| Artifact | Purpose |
|---|---|
| GitHub repo | Reproducibility, coding skills |
| Published Quarto site (Quarto Pub) | Live link for CV/LinkedIn |
| PDF export of report | Attach to applications |
| `requirements.txt` + README | Professional habits |
| Balance table | Reusable for any paper on this data |

## What This Showcases

- **Economics/policy roles:** RCT methodology fluency, causal inference awareness, clean data documentation
- **Data science roles:** end-to-end pipeline, reproducible research, publication-quality visualization
- **Research roles:** codebook literacy, merge diagnostics, balance testing, honest limitations
