# Testing and delivery record

## Current assessment revision — 29 October 2026

The current notebook contains 39 cells, including 16 code cells. A fresh kernel executed every cell in order using `scripts/execute_notebook.py`; all completed without saved error outputs. The notebook and HTML preview were regenerated together. `notebook_execution.txt` records this run. The opening cell was also checked from the notebooks directory and successfully loaded all 1,338 records; data paths now resolve from either documented launch folder.

New executed evidence reconciles sex-by-smoking and children-group counts, means and medians with the dashboard's shared summary function. Both sets of group counts sum to 1,338. Checks confirm the sex-group mean reversal across smoking groups, the non-monotonic children-group means, and the two plotted BMI lines against NumPy least-squares calculations. Current chart explanations are saved in the notebook output. The new BMI figure was visually inspected for readable labels and lines.

The existing automated suite passed: **21 passed** (`streamlit_parity_tests.txt`). Ruff passed for `src`, `app.py`, `tests` and `scripts` (`lint_results.txt`); notebook cells are not included in that lint command. The tests exercise all eight charts, filters, empty and tiny selections, themes, reset, independent CSV calculations and BMI trend handling.

### Current live deployment status — verified 29 October 2026

The owner made the GitHub repository public and authorised a dashboard restart. Streamlit then cloned the repository, installed its dependencies and started successfully. The earlier source-download failure is resolved.

A subsequent browser check confirmed all eight chart sections and the default 1,338 records, mean 13,270.42 and median 9,382.03. Selecting smokers returned 274 records, mean 32,050.23 and median 34,456.35, with updated chart explanations. Clearing the region selection displayed the no-records message without results; reset restored all 1,338 records and the original summary figures. The Sources section now uses native Streamlit link buttons for the repository and executed notebook. Their deployed destinations were inspected; opening GitHub through those buttons was not independently confirmed in the browser environment.

The latest local verification passed all 21 tests and Ruff. The local and remote revisions matched at e38ea76 during the assessment recheck. These checks establish working deployment and filter behaviour in the browser session used; a separate signed-out assessor session was not tested.

The student's personal review and college submission remain unverified.

## Optional regression — 29 October 2026

Fresh-kernel execution succeeded after the extension. The fixed seed-42 grouped split gives 1,070 training records and 268 test records; identical source rows cannot occur on both sides. All six source predictors are used, plus a prespecified BMI × smoking interaction. Charges and age_band are excluded from predictors. One-hot encoding and linear fitting use training data only. The test set is not used for parameter tuning. Earlier full-sample exploration informed the interaction, so evaluation is labelled exploratory.

Test MAE: training-median baseline 7,721.87; regression 2,723.40, a 64.7% reduction. Non-smokers: 223 test records, MAE 2,477.32. Smokers: 45 test records, MAE 3,942.85. No test prediction was negative; no clipping is applied. These are point estimates from one split, not prediction intervals.

Three new tests verify deterministic disjoint splitting (including duplicate groups), unchanged predictions when only test targets are altered, and independent NumPy MAE/baseline and weighted subgroup-error reconciliation. Streamlit tests now expect nine figures: eight descriptive plots and one fixed-split prediction plot. All 19 tests pass; Ruff and pip dependency checks pass. The notebook's saved prediction plot and a dark-theme rendering were visually checked for labels, readable points and a perfect-prediction reference line.

Live deployment check: the “Optional predictive regression” expander opened successfully on the public Streamlit URL after commit c7ac431. It displayed 1,070 training / 268 test records, both MAEs matching the notebook, the prediction chart, smoking-group errors and limitations. The rendered dark-theme section was visually inspected; evidence is saved in `regression_live.png`.

## Distribution explanations — 29 October 2026

Replaced the generic histogram and smoking box-plot narratives with selected-data explanations. Histogram captions summarise skewness and Fisher excess kurtosis in two sentences. Box-plot captions compare group medians, middle-50% spread and upper outliers in two sentences. Detailed statistical definitions remain in the expander and notebook. Overall adjusted skewness is 1.52 and excess kurtosis 1.61; non-smokers 1.54 / 3.15; smokers 0.13 / −1.04. Near-zero skew is not described as proof of normality or a single peak. Kurtosis is interpreted as extreme-deviation weight relative to the normal reference, not peak height. Small/constant selections have specific fallbacks.

Two additional tests check the reported sample moments against independent SciPy calculations and cover tiny and constant groups. Fresh notebook execution saved the new group shape table and current explanations.

Caption refinement: removed the lengthy chart-reading tutorial, repeated ranges/quartiles and repeated caveats from the two captions at the user’s request. Avoided dollar signs in the new captions to prevent Markdown interpreting pairs as equations. Fresh notebook execution, 21 tests and Ruff passed.
