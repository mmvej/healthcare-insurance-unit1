"""Native Python charts and selection-aware explanations matching the Sites report."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import StrMethodFormatter

from src.analysis import summary

SMOKING = {"no": "Non-smokers", "yes": "Smokers"}


def correlation(frame, field):
    if len(frame) < 3 or frame[field].nunique() < 2 or frame.charges.nunique() < 2:
        return None
    return frame[field].corr(frame.charges)


def chart_style(dark=True):
    """Keep theme colours active during both construction and image export."""
    background, text, grid = (
        ("#18232f", "#e8eef3", "#354657") if dark else ("#ffffff", "#20313e", "#dfe5e8")
    )
    return {
        "figure.facecolor": background,
        "axes.facecolor": background,
        "text.color": text,
        "axes.labelcolor": text,
        "xtick.color": text,
        "ytick.color": text,
        "axes.edgecolor": grid,
        "grid.color": grid,
        "font.size": 11,
        "legend.facecolor": background,
        "legend.edgecolor": grid,
        "savefig.facecolor": background,
    }


def report_chart(frame, kind, dark=True):
    """Render eight complementary comparisons, with each useful count shown once."""
    background = "#18232f" if dark else "#ffffff"
    text = "#e8eef3" if dark else "#20313e"
    blue, orange = ("#8bbfe8", "#efb86f") if dark else ("#245c88", "#a95b12")
    with plt.rc_context(chart_style(dark)):
        fig, ax = plt.subplots(figsize=(10, 4.8), layout="constrained")
        ax.grid(axis="y", alpha=0.6)
        ax.set_axisbelow(True)
        ax.spines[["top", "right"]].set_visible(False)
        ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
        ax.set_ylabel("Charges ($)")
        if kind in ["smokingcomparison", "childrencomparison", "regionchart"]:
            key = {
                "smokingcomparison": "smoker",
                "childrencomparison": "children",
                "regionchart": "region",
            }[kind]
            groups = summary(frame, key).sort_index()
            x = np.arange(len(groups))
            for offset, metric, colour in [
                (-0.19, "mean", blue),
                (0.19, "median", orange),
            ]:
                bars = ax.bar(
                    x + offset,
                    groups[metric],
                    width=0.36,
                    label=metric.title(),
                    color=colour,
                )
                if kind != "regionchart":
                    ax.bar_label(
                        bars,
                        labels=[f"{v:,.2f}" for v in groups[metric]],
                        padding=5,
                        fontsize=9,
                        color=text,
                    )
            names = [SMOKING[v] if key == "smoker" else str(v) for v in groups.index]
            ax.set_xticks(
                x,
                [
                    f"{name}\n{int(n):,} records"
                    for name, n in zip(names, groups["count"])
                ],
            )
            ax.set_ylim(0, groups[["mean", "median"]].max().max() * 1.23)
            ax.legend()
        elif kind == "sexcomparison":
            sexes = [s for s in ["female", "male"] if frame.sex.eq(s).any()]
            x = np.arange(len(sexes))
            largest = 0
            for offset, group, colour in [(-0.19, "no", blue), (0.19, "yes", orange)]:
                part = frame.loc[frame.smoker.eq(group)]
                table = summary(part, "sex")
                values = [
                    table.loc[s, "mean"] if s in table.index else np.nan for s in sexes
                ]
                bars = ax.bar(
                    x + offset, values, width=0.36, label=SMOKING[group], color=colour
                )
                for sex, bar, value in zip(sexes, bars, values):
                    if np.isfinite(value):
                        largest = max(largest, value)
                        ax.annotate(
                            f"n={int(table.loc[sex, 'count'])}\n{value:,.2f}",
                            (bar.get_x() + bar.get_width() / 2, value),
                            xytext=(0, 5),
                            textcoords="offset points",
                            ha="center",
                            va="bottom",
                            fontsize=10,
                            color=text,
                        )
            ax.set_xticks(x, [s.title() for s in sexes])
            ax.set_ylim(0, largest * 1.28)
            ax.legend()
        elif kind == "hist":
            ax.hist(frame.charges, bins=30, color=blue, edgecolor=background)
            ax.axvline(
                frame.charges.median(), color=text, linestyle="--", label="Median"
            )
            ax.set(xlabel="Charges ($)", ylabel="Records")
            ax.legend()
        elif kind == "box":
            for i, (group, colour) in enumerate([("no", blue), ("yes", orange)]):
                values = frame.loc[frame.smoker.eq(group), "charges"]
                if not values.empty:
                    ax.boxplot(
                        values,
                        positions=[i],
                        widths=0.5,
                        patch_artist=True,
                        boxprops={
                            "facecolor": colour,
                            "alpha": 0.3,
                            "edgecolor": colour,
                        },
                        medianprops={"color": colour, "linewidth": 2},
                        whiskerprops={"color": colour},
                        capprops={"color": colour},
                        flierprops={"markeredgecolor": colour, "markersize": 3},
                    )
            ax.set_xticks([0, 1], ["Non-smokers", "Smokers"])
            ax.set_xlim(-0.7, 1.7)
        elif kind in ["agechart", "bmichart"]:
            key = "age" if kind == "agechart" else "bmi"
            for group, colour, marker in [("no", blue, "o"), ("yes", orange, "^")]:
                part = frame.loc[frame.smoker.eq(group)]
                if not part.empty:
                    r = correlation(part, key) if kind == "bmichart" else None
                    label = SMOKING[group]
                    if kind == "bmichart":
                        label += f" (r = {r:.2f})" if r is not None else " (r unavailable)"
                    ax.scatter(
                        part[key],
                        part.charges,
                        color=colour,
                        marker=marker,
                        alpha=0.55,
                        s=23,
                        label=label,
                    )
                    if kind == "bmichart" and r is not None:
                        slope, intercept = np.polyfit(part.bmi, part.charges, 1)
                        x = np.array([part.bmi.min(), part.bmi.max()])
                        ax.plot(x, slope * x + intercept, color=colour,
                                linewidth=2.2, linestyle="--")
            ax.set_xlabel("Age (years)" if key == "age" else "BMI (kg/m²)")
            ax.legend()
        else:
            raise ValueError(f"Unknown report chart: {kind}")
        return fig


def explanations(frame):
    """Interpret the selected data without duplicating chart labels and counts."""
    out = {}
    no, yes = (frame.loc[frame.smoker.eq(g)] for g in ["no", "yes"])
    if len(no) and len(yes):
        a, b = no.charges.mean(), yes.charges.mean()
        group = "smoking" if b >= a else "non-smoking"
        ratio = (
            f"Smokers’ mean costs are {b / a:.2f} times those of non-smokers. "
            if a
            else ""
        )
        out["smokingcomparison"] = (
            f"The {group} group has higher average costs, with a gap of ${abs(b - a):,.2f}. "
            + ratio
        )
        if yes.charges.median() > no.charges.median():
            pattern = (
                "The higher median for smokers shows that the difference extends to "
                "typical records, rather than only a few unusually large amounts."
            )
        elif yes.charges.median() < no.charges.median():
            pattern = (
                "The median is higher among non-smokers in this selection, so the "
                "middle of each distribution adds context beyond the averages."
            )
        else:
            pattern = "The medians coincide; the boxes still show variation within each group."
        out["box"] = (
            "The boxes show the middle half of each group’s recorded costs. " + pattern
        )
    else:
        group = "smokers" if len(yes) else "non-smokers"
        out["smokingcomparison"] = (
            f"Only {group} are selected. Select both smoking groups "
            "to compare their costs."
        )
        out["box"] = (
            "The box shows how much costs vary within the selected group; "
            "the centre line marks the median."
        )
    difference = frame.charges.mean() - frame.charges.median()
    out["hist"] = (
        "Larger amounts pull the mean above the median. The average therefore exceeds the "
        "cost of the middle record, making the median useful for describing a typical case."
        if difference > 0
        else "The mean falls below the median. The distribution adds context that a single average would miss."
        if difference < 0
        else "The mean and median coincide here; the distribution shows the variation around them."
    )
    regions = summary(frame, "region")
    mean_region, median_region = regions["mean"].idxmax(), regions["median"].idxmax()
    if len(regions) > 1:
        pattern = (
            "Both measures rank the same region first."
            if mean_region == median_region
            else "Different rankings show that the region with the largest average "
            "is not necessarily the one with the largest typical cost."
        )
        out["regionchart"] = (
            f"{mean_region.title()} has the highest mean; {median_region} "
            f"has the highest median. {pattern}"
        )
    else:
        out["regionchart"] = (
            f"Only {mean_region} is selected. Add other regions to make "
            "a geographic comparison."
        )
    for key, chart_id in [("age", "agechart"), ("bmi", "bmichart")]:
        r = correlation(frame, key)
        label = "age" if key == "age" else "BMI"
        if r is None:
            text = f"There is not enough variation or enough records to summarise the {label}–charge relationship."
        elif abs(r) < 0.15:
            text = f"{label.capitalize() if key == 'age' else label} shows little overall linear relationship with medical costs (correlation {r:.2f})."
        else:
            text = f"{'Higher' if r > 0 else 'Lower'} {label} tends to accompany higher costs (correlation {r:.2f})."
        rn, ry = correlation(no, key), correlation(yes, key)
        if rn is not None and ry is not None:
            text += f" The correlation is {rn:.2f} among non-smokers and {ry:.2f} among smokers. "
            text += (
                "Separating the groups reveals a pattern that the overall result can hide."
                if abs(rn - ry) > 0.25
                else "The markers show the pattern within each smoking group."
            )
        else:
            text += " The spread shows that this variable alone does not explain individual costs."
        out[chart_id] = text
    comparisons = []
    for group in ["no", "yes"]:
        part = frame.loc[frame.smoker.eq(group)]
        if {"female", "male"}.issubset(set(part.sex)):
            means = part.groupby("sex").charges.mean()
            comparisons.append((group, means["female"] - means["male"]))
    sex_text = []
    for group, delta in comparisons:
        category = "smokers" if group == "yes" else "non-smokers"
        higher, lower = ("female", "male") if delta > 0 else ("male", "female")
        sex_text.append(
            f"Among {category}, the {higher} group has higher average costs "
            f"than the {lower} group."
            if delta
            else f"Among {category}, both sex groups have the same average costs."
        )
    if len(comparisons) == 2 and comparisons[0][1] * comparisons[1][1] < 0:
        sex_text.append(
            "The direction reverses between smoking groups, so one overall sex "
            "comparison would hide an important difference."
        )
    elif comparisons:
        sex_text.append(
            "Comparing within smoking groups helps separate these patterns from "
            "differences in smoking-group mix."
        )
    out["sexcomparison"] = (
        " ".join(sex_text)
        if sex_text
        else (
            "The selection does not contain both sex groups within a smoking group. Widen the filters to compare them."
        )
    )
    children = summary(frame, "children").sort_index()
    if len(children) > 1:
        rising = children["mean"].is_monotonic_increasing
        text = (
            "Means increase across the selected categories, but this does not establish "
            "that each extra dependant raises charges."
            if rising
            else "Average costs do not rise consistently with dependant count, so there "
            "is no simple “more dependants, higher costs” pattern."
        )
        if (children["count"] < 30).any():
            text += " The smaller groups shown in the chart should be interpreted cautiously."
        out["childrencomparison"] = text
    else:
        out["childrencomparison"] = (
            f"Only the {children.index[0]}-dependant category appears. "
            "Widen the filters to compare dependant counts."
        )
    out["groups"] = (
        "Compare regions within each smoking group to see whether the overall "
        "regional pattern remains."
    )
    return out
