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
- [x] Connect local repo to GitHub (GitHub Desktop)
- [x] Anonymize raw data: create `src/anonymize.py` and `data_public/`
- [x] Create school crosswalk (`data/crosswalk_schools.csv`)

---

## Phase 1 — Data Quality Assessment (`01_data_quality.qmd`) 🔄

### Setup
- [x] Create `src/checks.py` with 12 reusable quality check functions
- [x] Add assessment approach section to `01_data_quality.qmd`
- [x] Create `phase-1-data-quality` branch

### Per-file assessment plans
- [x] `baseline_estudiantes` — detailed plan finalized (15 sections: A–O)
- [ ] `randomizacion_escuelas`
- [ ] `math_chat_casa` / `math_chat_escuela`
- [ ] `math_ponte_prueba`
- [ ] `voc_chat`
- [ ] `voc_steps`

### Implementation
- [ ] Write `baseline_estudiantes` checks in `01_data_quality.qmd`
- [ ] Write remaining file checks
- [ ] Data quality scorecard (summary table across all files)

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
