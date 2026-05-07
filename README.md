# Math AI RCT — Data Analysis

Reproducible data quality assessment, descriptive analysis, and balance tests for a randomized controlled trial evaluating an AI-based math tutor in 30 secondary schools in Lima, Peru (~1,200 fifth-year students).

## Study Design

Three treatment arms assigned at the school level:
- **Control** — no intervention
- **T1** — Standard AI Tutor
- **T2** — Modified AI Tutor

Data sources: Qualtrics baseline survey + uDocz platform interaction logs.

## Report Sections

| Section | Description |
|---|---|
| [Overview](report/00_index.qmd) | Executive summary and recommendations |
| [Data Quality](report/01_data_quality.qmd) | Missing values, validity checks, merge coverage |
| [Descriptives](report/02_descriptives.qmd) | Sample characteristics and platform engagement |
| [Balance Tests](report/03_balance.qmd) | Covariate balance across treatment arms |

## Reproducing the Analysis

**1. Install dependencies**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

**2. Install Quarto**
Download from [quarto.org](https://quarto.org/docs/get-started/) and follow the installer.

**3. Render the report**
```bash
quarto render
```
Output goes to `_site/`. Open `_site/index.html` to view locally.

**4. Publish to Quarto Pub**
```bash
quarto publish quarto-pub
```

## Data

Raw CSVs are in `data/`. See `codebook.pdf` for variable definitions (Spanish).

| File | Rows | Grain |
|---|---|---|
| `baseline_estudiantes.csv` | 1,204 | Student |
| `randomizacion_escuelas.csv` | 32 | School |
| `math_chat_casa.csv` | 8,061 | Message |
| `math_chat_escuela.csv` | 6,366 | Message |
| `math_ponte_prueba.csv` | 5,224 | Quiz attempt |
| `voc_chat.csv` | 5,122 | Message |
| `voc_steps.csv` | 1,178 | Student × step |

## Project Structure

```
├── _quarto.yml           # Quarto project config
├── requirements.txt
├── data/                 # Raw CSVs (not tracked by git)
├── src/
│   └── utils.py          # Shared loaders, helpers, plot theme
├── report/
│   ├── 00_index.qmd      # Executive summary
│   ├── 01_data_quality.qmd
│   ├── 02_descriptives.qmd
│   └── 03_balance.qmd
└── outputs/
    ├── figures/
    └── tables/
```
