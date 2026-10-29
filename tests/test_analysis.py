"""Checks for data preservation, independent calculations and dashboard behaviour."""

import csv
from statistics import mean, median

import numpy as np
import pandas as pd
import pytest
from streamlit.testing.v1 import AppTest

from src.analysis import (
    AGE_LABELS,
    CATEGORIES,
    RAW,
    ROOT,
    filter_data,
    narrative,
    prepare_data,
    save_and_check,
    summary,
    validate,
)


def test_preserve_and_reload(tmp_path):
    raw, cleaned, changes = prepare_data()
    result = save_and_check(cleaned, tmp_path / "cleaned.csv")
    assert len(raw) == len(result) == 1338
    assert raw.duplicated().sum() == 1
    assert len(raw.loc[raw.duplicated(keep=False)]) == 2
    assert changes.labels_changed.sum() == 0
    pd.testing.assert_frame_equal(raw, cleaned[raw.columns], check_dtype=False)


def test_independent_csv_calculations():
    _, cleaned, _ = prepare_data()
    with RAW.open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    values = [float(row["charges"]) for row in rows]
    assert np.isclose(mean(values), cleaned.charges.mean())
    assert np.isclose(median(values), cleaned.charges.median())
    groups = summary(cleaned, "smoker")
    for group in ["no", "yes"]:
        values = [float(row["charges"]) for row in rows if row["smoker"] == group]
        assert len(values) == groups.loc[group, "count"]
        assert np.isclose(mean(values), groups.loc[group, "mean"])
    assert np.isclose(
        np.average(groups["mean"], weights=groups["count"]), cleaned.charges.mean()
    )
    assert not np.isclose(groups["mean"].mean(), cleaned.charges.mean())


def test_band_boundaries():
    raw, _, _ = prepare_data()
    ages = pd.Series([18, 29, 30, 44, 45, 59, 60, 64])
    bands = pd.cut(ages, [18, 30, 45, 60, 65], right=False, labels=AGE_LABELS)
    assert bands.astype(str).tolist() == [band for band in AGE_LABELS for _ in range(2)]
    assert raw.age.min() == 18 and raw.age.max() == 64


@pytest.mark.parametrize(
    "column,value",
    [
        ("charges", -1),
        ("bmi", 0),
        ("age", 17),
        ("children", 1.5),
        ("smoker", "unknown"),
        ("charges", float("inf")),
        ("charges", float("nan")),
    ],
)
def test_reject_bad_source_values(column, value):
    _, cleaned, _ = prepare_data()
    cleaned[column] = cleaned[column].astype("object")
    cleaned.loc[0, column] = value
    if column in ["charges", "bmi", "age", "children"]:
        cleaned[column] = pd.to_numeric(cleaned[column])
    with pytest.raises(ValueError):
        validate(cleaned)


def test_filters_and_story():
    _, data, _ = prepare_data()
    full = filter_data(data, CATEGORIES["region"], ["no", "yes"], AGE_LABELS)
    assert len(full) == 1338
    part = filter_data(data, ["southeast"], ["yes"], ["18-29"])
    assert not part.empty
    assert part.region.eq("southeast").all() and part.smoker.eq("yes").all()
    assert f"{part.charges.mean():,.2f}" in narrative(part)
    assert "Only one smoking category" in narrative(part)
    empty = filter_data(data, [], ["no", "yes"], AGE_LABELS)
    assert empty.empty and "No records" in narrative(empty)


def test_dashboard_default_and_filtered():
    app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=60).run()
    assert not app.exception
    assert app.metric[0].value == "1,338"
    assert len(app.get("image")) == 9
    app.multiselect[0].set_value(["southeast"])
    app.multiselect[1].set_value(["yes"])
    app.run()
    assert not app.exception
    assert app.metric[0].value == "91"
    _, data, _ = prepare_data()
    expected = data.loc[data.region.eq("southeast") & data.smoker.eq("yes")]
    assert app.metric[1].value == f"{expected.charges.mean():,.2f}"
    app.multiselect[2].set_value(["60-64"]).run()
    assert not app.exception
    expected = expected.loc[expected.age_band.eq("60-64")]
    assert app.metric[0].value == str(len(expected))
    app.multiselect[0].set_value([]).run()
    assert not app.exception
    assert len(app.metric) == 0
    assert any("No records" in info.value for info in app.info)
