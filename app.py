"""Streamlit dashboard based on the validated notebook analysis."""

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.analysis import (
    AGE_LABELS,
    CLEAN,
    chart,
    filter_data,
    narrative,
    summary,
    validate,
)

st.set_page_config(page_title="Healthcare insurance charges", layout="wide")
st.title("Healthcare insurance charges")
st.write("Explore recorded charges by smoking status, age, BMI and region.")
st.caption(
    "Public Kaggle teaching dataset. Currency and observation dates are not confirmed. "
    "Recorded charges are not assumed to be premiums."
)
try:
    data = pd.read_csv(CLEAN)
    validate(data)
    if "age_band" not in data or not data.age_band.isin(AGE_LABELS).all():
        raise ValueError("Invalid cleaned age bands; rerun the notebook.")
except (OSError, ValueError) as exc:
    st.error(f"The cleaned data could not be loaded: {exc}")
    st.stop()

with st.sidebar:
    st.header("Choose records")
    regions = st.multiselect(
        "Region", sorted(data.region.unique()), default=sorted(data.region.unique())
    )
    smokers = st.multiselect("Smoking status", ["no", "yes"], default=["no", "yes"])
    bands = st.multiselect("Age band", AGE_LABELS, default=AGE_LABELS)
    st.caption("Clearing any filter shows an empty selection.")
selected = filter_data(data, regions, smokers, bands)
st.write(narrative(selected))
if selected.empty:
    st.info("No records match these selections. Add options to the filters.")
    st.stop()
if len(selected) < 30:
    st.warning(
        "Fewer than 30 records are selected. Comparisons may be unstable; "
        "30 is a display warning, not a statistical guarantee."
    )
cols = st.columns(3)
for col, label, value in zip(
    cols,
    ["Records", "Mean charges", "Median charges"],
    [
        f"{len(selected):,}",
        f"{selected.charges.mean():,.2f}",
        f"{selected.charges.median():,.2f}",
    ],
):
    col.metric(label, value)
for title, kinds in [
    ("Charges and smoking", ["distribution", "smoking"]),
    ("Regional comparison", ["region"]),
    ("Age and BMI", ["age", "bmi"]),
]:
    st.subheader(title)
    for kind in kinds:
        figure = chart(selected, kind)
        st.pyplot(figure)
        plt.close(figure)
st.caption(
    "Box: middle 50%; centre line: median; whiskers: 1.5 × IQR; "
    "points beyond whiskers are retained observations."
)
st.subheader("Compare groups within regions")
st.dataframe(summary(selected, ["region", "smoker"]).round(2))
st.write(
    "Regional averages can reflect different population mixes. Comparing smoking "
    "groups separately gives more context but does not adjust for every difference."
)
with st.expander("Source and limitations"):
    st.markdown(
        "[Dataset: willian oliveira, Healthcare Insurance, version 1]"
        "(https://www.kaggle.com/datasets/willianoliveiragibin/healthcare-insurance)"
    )
    st.write(
        "Downloaded 27 October 2026; Kaggle metadata lists CC0. "
        "There are no dates, diagnoses, treatment details or person IDs. "
        "One repeated row was retained because distinct people could share its values. "
        "Do not use this exploratory sample for individual pricing or eligibility decisions."
    )
    st.write(
        "AI assistance: OpenAI Codex helped prepare the analysis, code and narrative. "
        "Calculations were checked through notebook execution and automated tests; "
        "the student must review and understand the work before submitting it."
    )
