"""
Reusable data quality check functions for the Math AI RCT analysis.
Each function returns a tidy DataFrame summarizing the check result.
"""

import numpy as np
import pandas as pd


def check_column_empty(df: pd.DataFrame) -> pd.DataFrame:
    """Identify columns where all values are missing."""
    empty = [col for col in df.columns if df[col].isnull().all()]
    return pd.DataFrame({
        "variable": empty,
        "issue": "all values missing (structurally empty)",
        "n_flagged": len(df),
        "pct_flagged": 100.0,
    })


def check_missing(
    df: pd.DataFrame,
    cols: list[str] | None = None,
    group_label: str | None = None,
) -> pd.DataFrame:
    """Missing rate per variable, optionally filtered to a subset of columns."""
    subset = df[cols] if cols else df
    n = len(subset)
    missing = subset.isnull().sum()
    pct = missing / n * 100
    result = pd.DataFrame({
        "variable": missing.index,
        "n_missing": missing.values,
        "pct_missing": pct.round(1).values,
    })
    if group_label:
        result.insert(0, "group", group_label)
    return result[result["n_missing"] > 0].sort_values("pct_missing", ascending=False).reset_index(drop=True)


def check_duplicates(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Count duplicate values in a column."""
    n_dupes = df[col].duplicated().sum()
    return pd.DataFrame([{
        "variable": col,
        "check": "duplicate values",
        "n_flagged": int(n_dupes),
        "pct_flagged": round(n_dupes / len(df) * 100, 1),
        "pass": n_dupes == 0,
    }])


def check_range(
    df: pd.DataFrame,
    col: str,
    min_val: float,
    max_val: float,
) -> pd.DataFrame:
    """Flag values outside [min_val, max_val]."""
    series = df[col].dropna()
    flagged = ((series < min_val) | (series > max_val)).sum()
    return pd.DataFrame([{
        "variable": col,
        "check": f"outside [{min_val}, {max_val}]",
        "n_flagged": int(flagged),
        "pct_flagged": round(flagged / len(df) * 100, 1),
        "pass": flagged == 0,
    }])


def check_allowed_values(
    df: pd.DataFrame,
    col: str,
    allowed: list,
) -> pd.DataFrame:
    """Flag values not in an explicit allowed set."""
    series = df[col].dropna()
    flagged = (~series.isin(allowed)).sum()
    return pd.DataFrame([{
        "variable": col,
        "check": f"not in allowed set {sorted(allowed)}",
        "n_flagged": int(flagged),
        "pct_flagged": round(flagged / len(df) * 100, 1),
        "pass": flagged == 0,
    }])


def check_binary(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Flag values not in {0, 1}."""
    return check_allowed_values(df, col, allowed=[0, 1])


def check_consistency(
    df: pd.DataFrame,
    col_a: str,
    col_b: str,
    label: str | None = None,
) -> pd.DataFrame:
    """Flag rows where col_a + col_b != 1 (i.e., not complements)."""
    flagged = (df[col_a] + df[col_b] != 1).sum()
    check_label = label or f"{col_a} + {col_b} != 1"
    return pd.DataFrame([{
        "variable": f"{col_a} / {col_b}",
        "check": check_label,
        "n_flagged": int(flagged),
        "pct_flagged": round(flagged / len(df) * 100, 1),
        "pass": flagged == 0,
    }])


def check_avg_replication(
    df: pd.DataFrame,
    items: list[str],
    avg_col: str,
    tolerance: float = 0.01,
    label: str | None = None,
) -> pd.DataFrame:
    """Check that avg_col matches the row-wise mean of items (within tolerance)."""
    computed = df[items].mean(axis=1)
    mismatch = (computed - df[avg_col]).abs() > tolerance
    n_flagged = mismatch.sum()
    check_label = label or f"stored average matches simple item mean (tol={tolerance})"
    return pd.DataFrame([{
        "variable": avg_col,
        "check": check_label,
        "n_flagged": int(n_flagged),
        "pct_flagged": round(n_flagged / len(df) * 100, 1),
        "pass": n_flagged == 0,
    }])


def check_reversal(
    df: pd.DataFrame,
    direct_items: list[str],
    reversed_items: list[str],
    avg_col: str,
    scale_max: int,
    tolerance: float = 0.01,
) -> pd.DataFrame:
    """
    Test whether avg_col was computed with or without reversing reversed_items.
    Reversal formula: scale_max + 1 - x.
    Returns which version (naive / reversed) matches avg_col.
    """
    all_items = direct_items + reversed_items

    naive = df[all_items].mean(axis=1)
    reversed_vals = df[reversed_items].apply(lambda x: scale_max + 1 - x)
    corrected = pd.concat([df[direct_items], reversed_vals], axis=1).mean(axis=1)

    naive_match = ((naive - df[avg_col]).abs() <= tolerance).sum()
    corrected_match = ((corrected - df[avg_col]).abs() <= tolerance).sum()
    n = len(df)

    return pd.DataFrame([{
        "variable": avg_col,
        "check": "reversal applied?",
        "naive_match_pct": round(naive_match / n * 100, 1),
        "reversed_match_pct": round(corrected_match / n * 100, 1),
        "conclusion": (
            "reversal applied" if corrected_match > naive_match
            else "reversal NOT applied" if naive_match > corrected_match
            else "inconclusive"
        ),
    }])


def check_hours_budget(
    df: pd.DataFrame,
    hours_cols: list[str],
    min_total: float = 10.0,
    max_total: float = 30.0,
    zero_exempt: list[str] | None = None,
    high_threshold: float | None = None,
) -> dict[str, pd.DataFrame]:
    """
    Three checks on hours_* variables:
    - Budget: per-student total outside [min_total, max_total]
    - Zeroes: unexpected zero values (excluding zero_exempt columns)
    - High values: individual variable values above high_threshold (defaults to max_total)

    Returns a dict with keys 'budget', 'zeroes', 'high_values'.
    """
    zero_exempt = zero_exempt or []
    high_threshold = high_threshold or max_total

    totals = df[hours_cols].sum(axis=1)
    budget_flagged = ((totals < min_total) | (totals > max_total)).sum()
    budget = pd.DataFrame([{
        "check": f"daily hours total outside [{min_total}, {max_total}]",
        "n_flagged": int(budget_flagged),
        "pct_flagged": round(budget_flagged / len(df) * 100, 1),
        "pass": budget_flagged == 0,
    }])

    zero_rows = []
    for col in hours_cols:
        if col in zero_exempt:
            continue
        n_zero = (df[col] == 0).sum()
        zero_rows.append({
            "variable": col,
            "n_zero": int(n_zero),
            "pct_zero": round(n_zero / len(df) * 100, 1),
        })
    zeroes = pd.DataFrame(zero_rows).sort_values("n_zero", ascending=False).reset_index(drop=True)

    high_rows = []
    for col in hours_cols:
        n_high = (df[col] > high_threshold).sum()
        high_rows.append({
            "variable": col,
            "threshold": high_threshold,
            "n_flagged": int(n_high),
            "pct_flagged": round(n_high / len(df) * 100, 1),
        })
    high_values = pd.DataFrame(high_rows).sort_values("n_flagged", ascending=False).reset_index(drop=True)

    return {"budget": budget, "zeroes": zeroes, "high_values": high_values}


def check_derived(
    df: pd.DataFrame,
    result_col: str,
    formula_fn,
    tolerance: float = 0.01,
    label: str | None = None,
) -> pd.DataFrame:
    """
    Apply formula_fn(row) to each row and compare to result_col.
    formula_fn receives the full DataFrame and returns a Series.
    """
    computed = formula_fn(df)
    mismatch = (computed - df[result_col]).abs() > tolerance
    n_flagged = mismatch.sum()
    check_label = label or f"derived {result_col} mismatch"
    return pd.DataFrame([{
        "variable": result_col,
        "check": check_label,
        "n_flagged": int(n_flagged),
        "pct_flagged": round(n_flagged / len(df) * 100, 1),
        "pass": n_flagged == 0,
    }])


def check_ordering(
    df: pd.DataFrame,
    cols: list[str],
    label: str | None = None,
) -> pd.DataFrame:
    """
    Flag rows where values do not increase (weakly) across cols left to right.
    Rows with any missing value in cols are excluded from the check.
    E.g., salary_secondary <= salary_technical <= salary_university.
    """
    complete = df[cols].dropna()
    flagged = pd.Series([False] * len(complete))
    for i in range(len(cols) - 1):
        flagged |= complete[cols[i]].values > complete[cols[i + 1]].values
    n_flagged = int(flagged.sum())
    n_complete = len(complete)
    check_label = label or f"ordering violated: {' <= '.join(cols)}"
    return pd.DataFrame([{
        "variable": " / ".join(cols),
        "check": f"{check_label} (complete cases: {n_complete:,})",
        "n_flagged": n_flagged,
        "pct_flagged": round(n_flagged / n_complete * 100, 1) if n_complete > 0 else 0.0,
        "pass": n_flagged == 0,
    }])
