"""Native Streamlit edition of the refined Sites healthcare report."""

import re

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.analysis import AGE_LABELS, CLEAN, ROOT, filter_data, summary, validate
from src.regression import interpretation, prediction_chart, regression_results
from src.report import SMOKING, chart_style, explanations, report_chart

TITLE = "Medical insurance charges (USD) by age, BMI, smoking status and region"
st.set_page_config(page_title=TITLE, layout="wide")


def remember_theme():
    st.query_params["theme"] = "dark" if st.session_state.dark_mode else "light"


# Each new visit starts dark, including links carrying an older light preference.
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
    st.query_params["theme"] = "dark"

heading, theme_control = st.columns([5, 1])
with theme_control:
    dark = st.toggle(
        "Dark mode",
        key="dark_mode",
        on_change=remember_theme,
    )
background, surface, text, border = (
    ("#101821", "#18232f", "#e8eef3", "#354657")
    if dark
    else ("#f6f7f8", "#ffffff", "#20313e", "#cbd5df")
)
st.markdown(
    f"""<style>
.stApp,[data-testid="stAppViewContainer"],[data-testid="stHeader"] {{
 background-color:{background};color:{text};color-scheme:{"dark" if dark else "light"};
}}
[data-testid="stMain"] h1,[data-testid="stMain"] h2,[data-testid="stMain"] h3,
[data-testid="stMain"] p,[data-testid="stMain"] label,
[data-testid="stMetricValue"],[data-testid="stMetricLabel"] {{color:{text}}}
[data-baseweb="select"],[data-baseweb="select"]>div,[data-testid="stExpander"],[data-baseweb="popover"]>div,[role="listbox"],[role="option"],[data-testid="stBaseButton-secondary"] {{background:{surface};color:{text};border-color:{border}}}
[data-baseweb="select"] *,[data-baseweb="popover"] *,[data-testid="stBaseButton-secondary"] * {{color:{text}}}
[data-baseweb="tag"] {{background:{border}}}
[data-testid="stMultiSelect"] div {{background-color:{surface}!important;color:{text}!important}}
[data-testid="stMultiSelect"] span,[data-testid="stMultiSelect"] input {{color:{text}!important}}
[data-testid="stMultiSelect"] svg {{fill:{text}!important}}

[data-baseweb="switch"]>div:first-child {{background:{border}}}
[data-testid="stMainBlockContainer"] {{max-width:1240px;padding-top:3rem}}
h1 {{font-size:2rem!important}}
.regional-table {{overflow-x:auto;border:1px solid {border};border-radius:8px;background:{surface};color:{text}}}
.regional-table table {{width:100%;border-collapse:collapse;font-size:15px;font-variant-numeric:tabular-nums}}
.regional-table th,.regional-table td {{padding:12px;border-bottom:1px solid {border};text-align:right;white-space:nowrap;background:{surface};color:{text}}}
.regional-table th:first-child,.regional-table td:first-child,.regional-table th:nth-child(2),.regional-table td:nth-child(2) {{text-align:left}}
[data-testid="stExpander"] details,[data-testid="stExpander"] summary {{background-color:{surface}!important;color:{text}!important}}
[data-testid="stExpander"] summary *,[data-testid="stExpander"] details[open] summary * {{color:{text}!important}}
[data-testid="stExpander"] summary svg {{fill:currentColor}}
.report-definitions table {{width:100%;border-collapse:collapse;font-size:15px}}
.report-definitions th,.report-definitions td {{padding:12px;text-align:left;vertical-align:top;border-bottom:1px solid {border};color:{text}}}
.report-definitions .terms {{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px;margin-top:24px}}
.report-definitions .terms p {{min-width:0}}
[data-testid="stLatex"] {{overflow-x:auto;padding:8px 0}}
.report-definitions p {{font-size:15px;line-height:1.7;color:{text}}}
@media(max-width:760px){{.report-definitions .terms{{grid-template-columns:1fr}}.report-definitions .tablewrap{{overflow:auto}}}}
</style>""",
    unsafe_allow_html=True,
)
with heading:
    st.title(TITLE)

try:
    data = pd.read_csv(CLEAN)
    validate(data)
    if "age_band" not in data or not data.age_band.isin(AGE_LABELS).all():
        raise ValueError("Invalid cleaned age bands; rerun the notebook.")
except (OSError, ValueError) as exc:
    st.error(f"The cleaned data could not be loaded: {exc}")
    st.stop()

def reset_filters():
    st.session_state.regions = sorted(data.region.unique())
    st.session_state.smokers = ["no", "yes"]
    st.session_state.bands = AGE_LABELS


filters = st.columns(3)
with filters[0]:
    regions = st.multiselect(
        "Region", sorted(data.region.unique()), default=sorted(data.region.unique()), key="regions"
    )
with filters[1]:
    smokers = st.multiselect(
        "Smoking status", ["no", "yes"], default=["no", "yes"], format_func=SMOKING.get, key="smokers"
    )
with filters[2]:
    bands = st.multiselect("Age band", AGE_LABELS, default=AGE_LABELS, key="bands")
st.button("Reset filters", on_click=reset_filters)
selected = filter_data(data, regions, smokers, bands)


def visual(kind, title, explanation):
    st.subheader(title)
    figure = report_chart(selected, kind, dark=dark)
    with plt.rc_context(chart_style(dark)):
        st.pyplot(figure, alt=title)
    plt.close(figure)
    st.write(explanation)


if selected.empty:
    st.info(
        "No records match these selections. Choose at least one option in each filter."
    )
else:
    cols = st.columns(3)
    for col, label, value in zip(
        cols,
        ["Selected records", "Mean recorded charges (USD)", "Median recorded charges (USD)"],
        [
            f"{len(selected):,}",
            f"{selected.charges.mean():,.2f}",
            f"{selected.charges.median():,.2f}",
        ],
    ):
        col.metric(label, value)
    if len(selected) < 30:
        st.warning("Fewer than 30 records are selected. Comparisons may be unstable; 30 is a display warning, not a statistical guarantee.")
    notes = explanations(selected)
    st.header("Explore the relationships")
    visual(
        "smokingcomparison",
        "Smoking groups: mean and median charges (USD)",
        notes["smokingcomparison"],
    )
    left, right = st.columns(2)
    with left:
        visual("hist", "Distribution of charges", notes["hist"])
    with right:
        visual("box", "Charges by smoking status (USD)", notes["box"])
    visual("regionchart", "Regional comparison (USD)", notes["regionchart"])
    left, right = st.columns(2)
    with left:
        visual("agechart", "Age and charges (USD)", notes["agechart"])
    with right:
        visual("bmichart", "BMI and charges (USD)", notes["bmichart"])
    visual(
        "sexcomparison",
        "Sex and charges within smoking groups (USD)",
        notes["sexcomparison"],
    )
    visual(
        "childrencomparison",
        "Children and charges (USD)",
        notes["childrencomparison"],
    )
    st.subheader("Within-region smoking groups")
    table = summary(selected, ["region", "smoker"]).reset_index()
    table["smoker"] = table.smoker.map(SMOKING)
    table = table[["region", "smoker", "count", "mean", "median", "std"]].rename(
        columns={
            "region": "Region",
            "smoker": "Smoking group",
            "count": "Records",
            "mean": "Mean ($)",
            "median": "Median ($)",
            "std": "SD ($)",
        }
    )
    st.html(
        '<div class="regional-table">'
        + table.to_html(
            index=False, border=0, na_rep="—",
            formatters={column: lambda value: f"{value:,.2f}"
                        for column in ["Mean ($)", "Median ($)", "SD ($)"]},
        )
        + "</div>"
    )
    st.write(notes["groups"])

with st.expander("Optional predictive regression"):
    st.write("Full-dataset prediction of recorded charges from six source fields and a BMI–smoking interaction. Descriptive filters do not change this fixed evaluation.")
    train, test, scores, predictions, group_errors = regression_results(data)
    st.write(f"Training: {len(train):,} records. Test: {len(test):,} records.")
    st.dataframe(scores.round(2), hide_index=True)
    figure = prediction_chart(predictions, dark=dark)
    st.pyplot(figure, alt="Held-out predicted versus actual recorded charges")
    plt.close(figure)
    st.write(interpretation(scores, predictions))
    st.dataframe(group_errors.rename(index={"no": "Non-smokers", "yes": "Smokers"}).round(2))



# Reuse the authored definitions and conclusion so their wording stays aligned.
source = (ROOT / "web_dashboard/index.html").read_text()
definitions = re.search(
    r'<section(?=[^>]*aria-labelledby="variables-title")[^>]*>.*?</section>',
    source,
    re.DOTALL,
).group()
with st.expander("Variable and statistical definitions"):
    terms_pattern = r'<div aria-label="Summary measure definitions".*?</div>'
    terms = re.search(terms_pattern, definitions, re.DOTALL).group()
    dictionary = re.sub(terms_pattern, '', definitions, flags=re.DOTALL)
    st.html('<div class="report-definitions">' + dictionary + '</div>')
    equations = [
        r"n = \sum_{i=1}^{n} 1",
        r"\bar{x} = \frac{1}{n}\sum_{i=1}^{n}x_i",
        r"\operatorname{Median} = \begin{cases}x_{\left(\frac{n+1}{2}\right)}, & n\text{ odd} \\ \dfrac{x_{(n/2)} + x_{(n/2+1)}}{2}, & n\text{ even}\end{cases}",
        r"s = \sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}",
        r"\begin{aligned} Q_1 &= Q(0.25),\quad Q_3 = Q(0.75) \\ \mathrm{IQR} &= Q_3-Q_1\end{aligned}",
        r"r = \frac{\sum_{i=1}^{n}(x_i-\bar{x})(y_i-\bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i-\bar{x})^2\,\sum_{i=1}^{n}(y_i-\bar{y})^2}}",
    ]
    paragraphs = re.findall(r'<p>.*?</p>', terms, re.DOTALL)
    for start in range(0, len(paragraphs), 2):
        for index, column in zip(range(start, min(start + 2, len(paragraphs))), st.columns(2)):
            paragraph = paragraphs[index]
            with column:
                parts = re.split(r'<span class="equation">.*?</span>', paragraph, flags=re.DOTALL)
                if len(parts) == 2:
                    st.html('<div class="report-definitions">' + parts[0] + '</p></div>')
                    st.latex(equations[index])
                else:
                    st.html('<div class="report-definitions">' + paragraph + '</div>')
    st.markdown("### How to read the charts")
    st.markdown("""
- **Comparison bars:** heights show group means and medians. Counts give the size of each group; differences are descriptive associations.
- **Histogram:** the 30 equal-width intervals show record counts, not spending totals. The dashed line marks the median.
- **Box plots:** boxes contain the middle 50%, with a median line. Whiskers reach observed values within 1.5 × IQR of each box edge; points beyond them are retained extremes.
- **Age/BMI scatter plots:** each point is a record. Colour and shape identify smoking groups; BMI dashed lines are separate least-squares fits. Correlation measures linear association, not causation.
- **Prediction scatter:** the dashed diagonal marks perfect prediction. Above it means overprediction; below it means underprediction. MAE is the average absolute error in original charge units, not percentage accuracy.
""")
    st.markdown("### Regression method and limits")
    st.write("The fixed seed-42 split keeps identical records together. Encoding, model fitting and the baseline median use training data only; no test-set tuning is used. The BMI–smoking interaction was motivated by prior full-sample exploration, so evaluation is exploratory. Linear regression is unconstrained and can produce negative estimates. A single split gives uncertain performance estimates; cross-validation and external data would strengthen validation. Missing dates, diagnoses and sampling details prevent current-cost forecasts or individual pricing decisions. Charge units remain unconfirmed.")
with st.expander("Source, limitations and project files"):
    details = re.search(r"<details>.*?</details>", source, re.DOTALL).group()
    details = re.sub(
        r"</?details>|<summary>.*?</summary>", "", details, flags=re.DOTALL
    )
    details = re.sub(r"<p>This Sites edition.*?</p>|<p>Chart guide:.*?</p>", "", details, flags=re.DOTALL)
    details = details.replace(
        'href="notebook.html"',
        'href="https://github.com/mmvej/healthcare-insurance-unit1/blob/main/notebooks/healthcare_insurance_analysis.ipynb"',
    )
    details = re.sub(
        r'<a[^>]*href="healthcare_insurance_analysis.ipynb"[^>]*>.*?</a>\s*·?',
        "",
        details,
    )
    details = re.sub(r'<p><a href="https://github.com/.*?</p>', "", details, flags=re.DOTALL)
    st.html('<div class="report-definitions">' + details + "</div>")
    st.link_button("Read the executed assignment notebook", "https://github.com/mmvej/healthcare-insurance-unit1/blob/main/notebooks/healthcare_insurance_analysis.ipynb")
    st.link_button("GitHub repository and Python Streamlit source", "https://github.com/mmvej/healthcare-insurance-unit1")
    st.download_button(
        "Download the executed notebook",
        (ROOT / "notebooks/healthcare_insurance_analysis.ipynb").read_bytes(),
        file_name="healthcare_insurance_analysis.ipynb",
        mime="application/x-ipynb+json",
    )
conclusion = re.search(
    r'<section(?=[^>]*aria-labelledby="conclusion-title")[^>]*>.*?</section>',
    source,
    re.DOTALL,
).group()
with st.expander("Conclusion"):
    st.html('<div class="report-definitions">' + conclusion + "</div>")
