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
            if kind == "childrencomparison":
                ax.set_xlabel("Number of children")
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
            ax.axvline(frame.charges.median(), color=text, linestyle="--", label="Median")
            ax.set(xlabel="Charges ($)", ylabel="Records")
            ax.legend()
        elif kind == "box":
            plotted = []
            for i, (group, colour) in enumerate([("no", blue), ("yes", orange)]):
                values = frame.loc[frame.smoker.eq(group), "charges"]
                if not values.empty:
                    artists = ax.boxplot(
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
                    q1, median, q3 = values.quantile([0.25, 0.5, 0.75])
                    plotted.append((q3 - q1, i, q1, median, q3, artists))
            span = max(float(frame.charges.max() - frame.charges.min()), 1)
            arrow = {'arrowstyle': '->', 'color': text, 'linewidth': 1}
            label_box = {'facecolor': background, 'edgecolor': 'none', 'alpha': 0.9}
            top_label = float(frame.charges.max())
            for iqr, position, q1, median, q3, artists in plotted:
                low = artists['whiskers'][0].get_ydata()[-1]
                high = artists['whiskers'][1].get_ydata()[-1]
                side = -1 if position == 0 else 1
                alignment = 'right' if side < 0 else 'left'
                if q1 == q3:
                    y = median + span * 0.12
                    ax.annotate(f"Q1 = median = Q3: {median:,.0f}", xy=(position, median),
                                xytext=(position + side * 0.36, y), ha=alignment,
                                color=text, fontsize=9, bbox=label_box, arrowprops=arrow)
                    top_label = max(top_label, y)
                else:
                    previous = -float('inf')
                    for title, value in [('Lower whisker', low), ('Q1', q1),
                                         ('Median', median), ('Q3', q3), ('Upper whisker', high)]:
                        label_y = max(value, previous + span * 0.06)
                        edge = 0.125 if 'whisker' in title else 0.25
                        ax.annotate(f"{title}: {value:,.0f}", xy=(position + side * edge, value),
                                    xytext=(position + side * 0.36, label_y), va='center', ha=alignment,
                                    color=text, fontsize=9, bbox=label_box, arrowprops=arrow)
                        previous = label_y
                        top_label = max(top_label, label_y)
                    inner = -side
                    ax.annotate('', xy=(position + inner * 0.33, q1),
                                xytext=(position + inner * 0.33, q3),
                                arrowprops={'arrowstyle': '|-|', 'color': text})
                    ax.text(position + inner * 0.37, (q1 + q3) / 2, f'IQR: {iqr:,.0f}',
                            ha='left' if inner > 0 else 'right', va='center',
                            color=text, fontsize=9, bbox=label_box)
                outliers = artists['fliers'][0].get_ydata()
                if len(outliers):
                    y = float(max(outliers))
                    label_y = max(y + span * 0.1, top_label if position == 1 else y + span * 0.1)
                    label = (f"Outliers: {len(outliers)}\n"
                             f"{min(outliers):,.0f}–{max(outliers):,.0f}")
                    ax.annotate(label, xy=(position, y), xytext=(position + side * 0.38, label_y),
                                ha=alignment, color=text, fontsize=9, bbox=label_box, arrowprops=arrow)
                    top_label = max(top_label, label_y)
            ax.set_ylim(min(0, frame.charges.min() - span * 0.07), top_label + span * 0.12)
            ax.set_xticks([0, 1], ["Non-smokers", "Smokers"])
            ax.set_xlim(-1.05, 2.05)
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


def distribution_shape(values):
    """Summarise selected asymmetry and tail weight in two short sentences."""
    if len(values) < 3 or values.nunique() < 2:
        return "Too few records or no variation to assess distribution shape."
    skew = values.skew()
    sign = 'Positive' if skew > 0 else 'Negative' if skew < 0 else 'Zero'
    shape = (
        'a tail towards higher charges' if skew > 0.5 else
        'a tail towards lower charges' if skew < -0.5 else
        'little overall asymmetry'
    )
    text = f"{sign} skew ({skew:.2f}): {shape}. "
    if len(values) < 4:
        return text + "At least four records are needed for kurtosis."
    kurtosis = values.kurt()
    sign = 'Positive' if kurtosis > 0 else 'Negative' if kurtosis < 0 else 'Zero'
    tails = 'greater' if kurtosis > 0 else 'less' if kurtosis < 0 else 'similar'
    return text + (
        f"{sign} kurtosis ({kurtosis:.2f}): {tails} weight in extreme deviations "
        "relative to the normal reference."
    )


def histogram_description(values):
    """Keep the chart caption focused on observed shape."""
    return distribution_shape(values)


def box_description(frame):
    """Quantify median separation, relative IQR and selected-group outliers."""
    groups = {}
    for group, label in [('no', 'Non-smokers'), ('yes', 'Smokers')]:
        values = frame.loc[frame.smoker.eq(group), 'charges']
        if values.empty:
            continue
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        above = int((values > q3 + 1.5 * iqr).sum())
        below = int((values < q1 - 1.5 * iqr).sum())
        groups[group] = (label, values.median(), iqr, above, below, q1, q3)
    if len(groups) == 2:
        no, yes = groups['no'], groups['yes']
        higher, lower = (yes, no) if yes[1] >= no[1] else (no, yes)
        centre = (
            f"{higher[0]}’ median charges are {higher[1]:,.0f} USD versus "
            f"{lower[1]:,.0f} USD for {lower[0].lower()}. "
            if higher[1] != lower[1] else
            f"Both groups have median charges of {higher[1]:,.0f} USD. "
        )
        wider, narrower = (yes, no) if yes[2] >= no[2] else (no, yes)
        if wider[2] == narrower[2]:
            spread = 'Both groups have the same IQR'
        elif narrower[2] > 0:
            spread = f"{wider[0]}’ IQR is {wider[2] / narrower[2]:.2f} times as large"
        else:
            spread = f"{wider[0]} have an IQR of {wider[2]:,.0f} USD while the other group’s IQR is zero"
        overlap = 'do not overlap' if max(no[5], yes[5]) > min(no[6], yes[6]) else 'overlap'
        return (
            centre + f"{spread}; the middle-50% ranges {overlap}. "
            f"Upper outliers: {no[3]} among non-smokers and {yes[3]} among smokers, "
            'using each group’s own cutoff.'
        )
    label, median, iqr, above, below, _q1, _q3 = next(iter(groups.values()))
    return (
        f"{label}: median charges are {median:,.0f} USD, with an IQR of {iqr:,.0f} USD. "
        f"There are {above} upper and {below} lower outliers beyond the whiskers."
    )


def explanations(frame):
    """Brief analytical findings calculated from the plotted selection."""
    out = {'box': box_description(frame), 'hist': histogram_description(frame.charges)}
    no, yes = (frame.loc[frame.smoker.eq(g)] for g in ['no', 'yes'])
    if len(no) and len(yes):
        gap = yes.charges.mean() - no.charges.mean()
        ratio = yes.charges.mean() / no.charges.mean() if no.charges.mean() else None
        median_gap = yes.charges.median() - no.charges.median()
        higher = 'Smokers' if gap > 0 else 'Non-smokers'
        mean_text = (
            f"{higher} have higher mean charges by {abs(gap):,.0f} USD"
            if gap else 'Both smoking groups have the same mean charges'
        )
        if ratio is not None:
            mean_text += f" (smokers/non-smokers: {ratio:.2f} times)"
        median_higher = 'smokers' if median_gap > 0 else 'non-smokers'
        out['smokingcomparison'] = mean_text + '. ' + (
            f"The median is also higher among {median_higher} by {abs(median_gap):,.0f} USD."
            if median_gap and gap * median_gap >= 0 else
            f"The median comparison reverses: {median_higher} are higher by {abs(median_gap):,.0f} USD."
            if median_gap else 'Both groups have the same median.'
        )
    else:
        label = 'smokers' if len(yes) else 'non-smokers'
        difference = frame.charges.mean() - frame.charges.median()
        out['smokingcomparison'] = (
            f"Only {label} are selected; their mean is {abs(difference):,.0f} USD "
            f"{'above' if difference >= 0 else 'below'} their median. "
            'A between-group comparison is unavailable.'
        )

    regions = summary(frame, 'region')
    mean_region, median_region = regions['mean'].idxmax(), regions['median'].idxmax()
    mean_gap = regions['mean'].max() - regions['mean'].min()
    if len(regions) > 1:
        out['regionchart'] = (
            f"Mean charges span {mean_gap:,.0f} USD across regions; {mean_region.title()} "
            f"has the highest mean and {regions['mean'].idxmin().title()} the lowest. "
            f"{median_region.title()} has the highest median."
            if mean_gap else 'All selected regions have equal mean charges. '
            f"{median_region.title()} has the highest median."
        )
    else:
        out['regionchart'] = (
            f"Only {mean_region} is selected: its mean is "
            f"{abs(frame.charges.mean() - frame.charges.median()):,.0f} USD "
            f"{'above' if frame.charges.mean() >= frame.charges.median() else 'below'} its median."
        )

    for key, chart_id in [('age', 'agechart'), ('bmi', 'bmichart')]:
        r = correlation(frame, key)
        label = 'Age' if key == 'age' else 'BMI'
        if r is None:
            out[chart_id] = f"There is not enough variation or enough records to assess the {label}–charge association."
            continue
        direction = 'positive' if r > 0 else 'negative' if r < 0 else 'zero'
        text = f"{label} has a {direction} overall linear association with charges (r = {r:.2f})."
        rn, ry = correlation(no, key), correlation(yes, key)
        if rn is not None and ry is not None:
            text += f" Within-group correlations are {rn:.2f} among non-smokers and {ry:.2f} among smokers."
        elif frame.smoker.nunique() == 2:
            available = [('non-smokers', rn), ('smokers', ry)]
            for group, value in available:
                if value is not None:
                    text += f" Among {group}, r = {value:.2f}; the other group has insufficient variation or records."
        out[chart_id] = text

    comparisons, clauses = [], []
    for group in ['no', 'yes']:
        part = frame.loc[frame.smoker.eq(group)]
        if {'female', 'male'}.issubset(set(part.sex)):
            means = part.groupby('sex').charges.mean()
            delta = means['female'] - means['male']
            comparisons.append(delta)
            label = 'non-smokers' if group == 'no' else 'smokers'
            higher = 'female' if delta > 0 else 'male'
            clauses.append(
                f"among {label}, the {higher} mean is {abs(delta):,.0f} USD higher"
                if delta else f"among {label}, both sex groups have equal means"
            )
    if clauses:
        text = '; '.join(clauses) + '.'
        text = text[0].upper() + text[1:]
        if len(comparisons) == 2 and comparisons[0] * comparisons[1] < 0:
            text += ' The direction reverses between smoking groups.'
        out['sexcomparison'] = text
    else:
        out['sexcomparison'] = 'No selected smoking subgroup contains both sex categories, so a within-group sex comparison is unavailable.'

    children = summary(frame, 'children').sort_index()
    if len(children) > 1:
        peak = children['mean'].idxmax()
        if children['mean'].nunique() == 1:
            pattern = 'Mean charges are equal across the selected child-count categories'
        elif children['mean'].is_monotonic_increasing:
            pattern = 'Mean charges rise across the selected child-count categories'
        elif children['mean'].is_monotonic_decreasing:
            pattern = 'Mean charges fall across the selected child-count categories'
        else:
            pattern = 'Mean charges do not change monotonically with child count'
        text = f"{pattern}; the highest mean is in the {peak}-child group ({children.loc[peak, 'mean']:,.0f} USD)."
        smallest = children['count'].idxmin()
        if children.loc[smallest, 'count'] < 30:
            count = int(children.loc[smallest, 'count'])
            text += f" The {smallest}-child estimate is based on just {count} {'record' if count == 1 else 'records'}."
        out['childrencomparison'] = text
    else:
        out['childrencomparison'] = f"Only the {children.index[0]}-child category is selected; its mean is {children['mean'].iloc[0]:,.0f} USD and median {children['median'].iloc[0]:,.0f} USD."

    if len(no) and len(yes):
        table = frame.groupby(['region', 'smoker']).charges.mean().unstack('smoker')
        gaps = (table['yes'] - table['no']).dropna()
        if len(gaps) > 1:
            region = gaps.abs().idxmax()
            higher = 'smokers' if gaps.loc[region] > 0 else 'non-smokers'
            out['groups'] = f"The largest within-region mean gap is in {region}: {higher} are higher by {abs(gaps.loc[region]):,.0f} USD."
        elif len(gaps) == 1:
            region = gaps.index[0]
            higher = 'Smokers' if gaps.iloc[0] >= 0 else 'Non-smokers'
            out['groups'] = f"{higher} have higher mean charges by {abs(gaps.iloc[0]):,.0f} USD in {region}."
        else:
            out['groups'] = 'No selected region contains both smoking groups; within-region smoking differences cannot be compared.'
    else:
        label = 'smokers' if len(yes) else 'non-smokers'
        out['groups'] = f"Among {label}, regional means span {mean_gap:,.0f} USD; {mean_region} has the highest mean."
    return out
