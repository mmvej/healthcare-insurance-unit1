# Testing and delivery record

Date: 27 October 2026. Checks performed by the assistant in this session.

## Notebook and calculations

The 29-cell notebook was executed in order in a fresh Python kernel using the project environment. It completed successfully and was saved with table and chart outputs. The execution record is notebook_execution.txt. A readable HTML export was generated from the same executed notebook. nbformat validation passed.

The workflow confirms 1,338 source and cleaned rows, seven source fields and one derived field, zero missing source cells and zero changed category labels. It retains one repeat after the first and all high charges. The original raw file hash is unchanged after transformation. The cleaned CSV reload matches the cleaned DataFrame, including restored age-band order. Overall and smoking-group calculations are checked independently from the raw CSV with csv/statistics. Group counts reconcile and the weighted group average equals the overall average.

## Automated checks

Command: python -m pytest -q. Result: 12 passed. Full output: test_results.txt.

Coverage includes raw-value preservation and reload equality; the duplicated(keep=False) correction; independent means and medians; age-band boundaries; seven invalid-input cases; all/partial/empty filters; selection-specific narrative; and the Streamlit application. The dashboard check confirms 1,338 default records and five plot images, 91 records for southeast and smoking=yes with the correct mean, the 60-64 age-band filter, and an empty-filter message without metrics or exceptions.

Initial testing used the outdated element name 'imgs'. The installed Streamlit test tree exposes 'image'. The test was revised after inspecting the actual rendered element tree, then rerun successfully. This corrected the test's interface assumption; the five charts were already present.

Command: ruff check src app.py tests scripts. Result: all checks passed. Import ordering and formatting were applied. Full result: lint_results.txt. Command: python -m pip check. Result: no broken requirements found.

The seaborn box plot emits a Matplotlib deprecation warning about an internal orientation argument. It does not affect the plotted values or current functionality. Direct package versions are pinned; review this compatibility when upgrading Matplotlib or seaborn.

## Visual review

All six notebook figures were rendered and visually inspected as a contact sheet: histogram, smoking box plot, region mean/median bars, age scatter, BMI scatter and numeric-only correlation heatmap. Labels, legends, counts and units were readable, the plots showed actual data, and regional bars started at zero. Blue circles and orange triangles distinguish smoking groups in the scatter plots.

The local Streamlit page at http://localhost:8501 was opened in a browser. Its displayed count, mean, median and narrative agreed with the notebook. The visible top section, filters and distribution chart were inspected. The other dashboard chart images are covered by the automated app test and the shared figure review; a complete manual browser traversal and mobile-layout review are not claimed.

The saved notebook HTML was opened in the browser. Its opening text layout was visually inspected; the rendered page contained the task sections, saved calculations, tables and six chart outputs. The separate chart contact-sheet review covered figure readability. A page-by-page screenshot review of the entire long notebook is not claimed.

## Version control

Separate actual commits record the source/raw snapshot, shared analysis functions, executed notebook/AI evidence, dashboard/testing and delivery documentation. See git_history.txt and the GitHub history. Commits describe the assistant-led work in this session; they do not imply independent student development.

## Delivery status

GitHub repository: https://github.com/mmvej/healthcare-insurance-unit1

Remote Streamlit deployment: pending. Streamlit Community Cloud opened at https://share.streamlit.io and showed an unauthenticated sign-in page stating that signing in agrees to its Terms of Service. The assistant did not accept terms on the user's behalf. The project can be deployed after the user signs in and accepts any required terms. No remote dashboard URL or remote assessor-access test is claimed. The README includes the remaining deployment steps.

The assignment's required remote dashboard deliverable is therefore outstanding. Local execution, source availability and automated tests do not establish that a remote assessor can access the app. Final submission through the college channel also remains the student's responsibility.

## Sites follow-up

The user subsequently requested Sites deployment. A browser-based equivalent was published successfully at https://healthcare-insurance-unit1-mmvej.moseth.chatgpt.site with default private access. See sites_deployment.md for the exact saved version, deployment ID and browser checks. This updates the availability of a hosted web edition; the Python Streamlit deployment and assessor-access requirements above remain unresolved.
