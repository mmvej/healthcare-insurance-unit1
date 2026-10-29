# Testing and delivery record

## Current assessment revision — 29 October 2026

The current notebook contains 33 cells, including 14 code cells. A fresh kernel executed every cell in order using `scripts/execute_notebook.py`; all completed without saved error outputs. The notebook and HTML preview were regenerated together. `notebook_execution.txt` records this run. The opening cell was also checked from the notebooks directory and successfully loaded all 1,338 records; data paths now resolve from either documented launch folder.

New executed evidence reconciles sex-by-smoking and children-group counts, means and medians with the dashboard's shared summary function. Both sets of group counts sum to 1,338. Checks confirm the sex-group mean reversal across smoking groups, the non-monotonic children-group means, and the two plotted BMI lines against NumPy least-squares calculations. Current chart explanations are saved in the notebook output. The new BMI figure was visually inspected for readable labels and lines.

The existing automated suite passed: **16 passed** (`streamlit_parity_tests.txt`). Ruff passed for `src`, `app.py`, `tests` and `scripts` (`lint_results.txt`); notebook cells are not included in that lint command. The tests exercise all eight charts, filters, empty and tiny selections, themes, reset, independent CSV calculations and BMI trend handling.

### Current live deployment status — verified 29 October 2026

The owner made the GitHub repository public and authorised a dashboard restart. Streamlit then cloned the repository, installed its dependencies and started successfully. The earlier source-download failure is resolved.

A subsequent browser check confirmed all eight chart sections and the default 1,338 records, mean 13,270.42 and median 9,382.03. Selecting smokers returned 274 records, mean 32,050.23 and median 34,456.35, with updated chart explanations. Clearing the region selection displayed the no-records message without results; reset restored all 1,338 records and the original summary figures. The Sources section now uses native Streamlit link buttons for the repository and executed notebook. Their deployed destinations were inspected; opening GitHub through those buttons was not independently confirmed in the browser environment.

The latest local verification passed all 16 tests and Ruff. The local and remote revisions matched at e38ea76 during the assessment recheck. These checks establish working deployment and filter behaviour in the browser session used; a separate signed-out assessor session was not tested.

The student's personal review and college submission remain unverified.
