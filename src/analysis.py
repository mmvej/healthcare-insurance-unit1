"""Prepare and describe the Kaggle healthcare insurance CSV."""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/insurance.csv"
CLEAN = ROOT / "data/processed/insurance_cleaned.csv"
COLUMNS = ["age", "sex", "bmi", "children", "smoker", "region", "charges"]
NUMERIC = ["age", "bmi", "children", "charges"]
CATEGORIES = {
    "sex": ["female", "male"],
    "smoker": ["no", "yes"],
    "region": ["northeast", "northwest", "southeast", "southwest"],
}
AGE_LABELS = ["18-29", "30-44", "45-59", "60-64"]
PALETTE = {"no": "#245C88", "yes": "#A95B12"}


def validate(frame):
    """Reject unusable inputs; flag plausible extremes separately."""
    if list(frame.columns[:7]) != COLUMNS:
        raise ValueError("The seven source fields or their order have changed.")
    if frame.empty or frame[COLUMNS].isna().any().any():
        raise ValueError("Empty dataset or missing source values: review before use.")
    for column in NUMERIC:
        if not pd.api.types.is_numeric_dtype(frame[column]):
            raise ValueError(f"{column} must be numeric.")
        if not np.isfinite(frame[column].to_numpy(dtype=float)).all():
            raise ValueError(f"{column} contains a non-finite value.")
    if not frame.age.between(18, 64).all():
        raise ValueError("Age outside the documented analysis bands; review scope.")
    if not ((frame.age % 1 == 0) & (frame.children % 1 == 0)).all():
        raise ValueError("Age and covered dependants must be whole numbers.")
    if (
        (frame.children < 0).any()
        or (frame.bmi <= 0).any()
        or (frame.charges < 0).any()
    ):
        raise ValueError(
            "Negative counts/charges or non-positive BMI need investigation."
        )
    for column, allowed in CATEGORIES.items():
        if not frame[column].isin(allowed).all():
            raise ValueError(f"Unexpected category in {column}; review source mapping.")


def prepare_data(path=RAW):
    """Preserve raw rows, normalise labels and add explicit age bands."""
    raw = pd.read_csv(path)
    if list(raw.columns) != COLUMNS:
        raise ValueError("Unexpected source schema.")
    cleaned = raw.copy(deep=True)
    changes = []
    for column in CATEGORIES:
        normalised = cleaned[column].astype("string").str.strip().str.lower()
        changes.append(
            {
                "field": column,
                "labels_changed": int(
                    (normalised != cleaned[column]).fillna(False).sum()
                ),
            }
        )
        cleaned[column] = normalised
    for column in NUMERIC:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="raise")
    validate(cleaned)
    cleaned["age"] = cleaned.age.astype("int64")
    cleaned["children"] = cleaned.children.astype("int64")
    cleaned["age_band"] = pd.cut(
        cleaned.age, bins=[18, 30, 45, 60, 65], right=False, labels=AGE_LABELS
    )
    if cleaned.age_band.isna().any():
        raise ValueError("An age was not assigned a band.")
    return raw, cleaned, pd.DataFrame(changes)


def save_and_check(cleaned, path=CLEAN):
    """Save CSV and verify values and restored category types after reloading."""
    path.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(path, index=False)
    reloaded = pd.read_csv(path)
    validate(reloaded)
    reloaded["age_band"] = pd.Categorical(
        reloaded.age_band, categories=AGE_LABELS, ordered=True
    )
    for column in CATEGORIES:
        reloaded[column] = reloaded[column].astype("string")
    pd.testing.assert_frame_equal(cleaned, reloaded, check_dtype=False, rtol=1e-12)
    return reloaded


def summary(frame, groups):
    """Report denominators and spread alongside mean and median."""
    return frame.groupby(groups, observed=True).charges.agg(
        count="size",
        mean="mean",
        median="median",
        std="std",
        minimum="min",
        maximum="max",
        q1=lambda values: values.quantile(0.25),
        q3=lambda values: values.quantile(0.75),
    )


def filter_data(frame, regions, smokers, age_bands):
    """An empty control selection means no rows, not all rows."""
    return frame.loc[
        frame.region.isin(regions)
        & frame.smoker.isin(smokers)
        & frame.age_band.isin(age_bands)
    ].copy()


def narrative(frame):
    """Use the current selection for every number in the management story."""
    if frame.empty:
        return "No records match these selections. Choose at least one option in each filter."
    text = (
        f"This selection contains {len(frame):,} records. Mean recorded charges are "
        f"{frame.charges.mean():,.2f}, compared with a median of "
        f"{frame.charges.median():,.2f} (source currency unspecified). "
    )
    smoking = summary(frame, "smoker")
    if {"no", "yes"}.issubset(smoking.index):
        text += (
            f"The mean is {smoking.loc['yes', 'mean']:,.2f} for smoking=yes "
            f"(n={smoking.loc['yes', 'count']:,.0f}) and "
            f"{smoking.loc['no', 'mean']:,.2f} for smoking=no "
            f"(n={smoking.loc['no', 'count']:,.0f}). "
        )
    else:
        text += "Only one smoking category is selected, so a smoking-group comparison is unavailable. "
    return text + (
        "Use these differences to guide further investigation and scenario planning. "
        "They do not establish causes, future costs or suitable prices for individuals. "
        "The source does not confirm observation dates, currency or sampling coverage."
    )


def chart(frame, kind):
    """Return a labelled figure using readable, consistent group encodings."""
    sns.set_theme(style="whitegrid", font_scale=1.0)
    fig, ax = plt.subplots(figsize=(8.6, 4.8), layout="constrained")
    if kind == "distribution":
        ax.hist(frame.charges, bins=30, color=PALETTE["no"], edgecolor="white")
        ax.set(
            xlabel="Recorded charges (currency unspecified)",
            ylabel="Record count",
            title=f"Distribution of recorded charges (n={len(frame):,})",
        )
        ax.axvline(
            frame.charges.median(), color="#242424", linestyle="--", label="Median"
        )
        ax.legend()
    elif kind == "smoking":
        sns.boxplot(
            data=frame,
            x="smoker",
            y="charges",
            order=["no", "yes"],
            hue="smoker",
            palette=PALETTE,
            legend=False,
            ax=ax,
        )
        counts = frame.smoker.value_counts()
        ax.set_xticks(
            [0, 1], [f"{group} (n={counts.get(group, 0):,})" for group in ["no", "yes"]]
        )
        ax.set(
            xlabel="Smoking status",
            ylabel="Recorded charges (currency unspecified)",
            title="Charge distributions by smoking status",
        )
    elif kind == "region":
        groups = summary(frame, "region").sort_index()
        positions = np.arange(len(groups))
        ax.bar(
            positions - 0.18,
            groups["mean"],
            width=0.36,
            label="Mean",
            color=PALETTE["no"],
        )
        ax.bar(
            positions + 0.18,
            groups["median"],
            width=0.36,
            label="Median",
            color=PALETTE["yes"],
        )
        ax.set_xticks(
            positions,
            [f"{name}\n(n={row['count']:,.0f})" for name, row in groups.iterrows()],
        )
        ax.set(
            xlabel="Source region category",
            ylabel="Recorded charges (currency unspecified)",
            title="Mean and median recorded charges by region",
            ylim=(0, None),
        )
        ax.legend()
    elif kind in ["age", "bmi"]:
        for group, marker in [("no", "o"), ("yes", "^")]:
            selected = frame.loc[frame.smoker.eq(group)]
            if not selected.empty:
                ax.scatter(
                    selected[kind],
                    selected.charges,
                    s=23,
                    alpha=0.5,
                    marker=marker,
                    c=PALETTE[group],
                    label=f"Smoking={group} (n={len(selected):,})",
                )
        ax.set(
            xlabel="Age (years)" if kind == "age" else "BMI (kg/m²; conventional unit)",
            ylabel="Recorded charges (currency unspecified)",
            title=f"{'Age' if kind == 'age' else 'BMI'} and recorded charges",
        )
        ax.legend()
    elif kind == "correlation":
        sns.heatmap(
            frame[NUMERIC].corr(),
            annot=True,
            fmt=".2f",
            vmin=-1,
            vmax=1,
            cmap="BrBG",
            ax=ax,
            square=True,
        )
        ax.set_title("Pearson correlation: numeric measurements only")
    else:
        raise ValueError("Unknown chart type.")
    return fig
