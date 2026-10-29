# Unit 1 assignment requirements and evidence audit

> Historical audit: this describes 28 October before subsequent dashboard and assessment revisions. For the current local revision and test results, see `testing.md` (29 October 2026). Do not treat the gaps below as a current checklist.

Audit date: 28 October 2026 (Europe/London).

Controlling source: Unit_1_Healthcare_Insurance_Assignment_Brief_v5.pdf, issued 26 October 2026, deadline 10 November 2026. The separate Code Institute handbook mentioned by the brief was not supplied or independently reviewed. This is an evidence audit, not an assessor's grade or a declaration that the student has achieved every criterion.

## Overall finding

The core analytical work is substantially evidenced. The notebook, data pipeline, sources, charts, written discussion and AI record exist. A real Python Streamlit dashboard is deployed, not merely a Sites substitute. However, the project is not ready to call a fully reconciled final submission: mandatory delivery documentation is stale, the latest requested Streamlit revision is unpublished, its latest test run is not completely passing, and the student's understanding and final college submission are not evidenced by the files.

A request to audit does not itself authorise claiming unfinished work as complete. This audit leaves the implementation and existing test results unchanged.

## Evidence inspected

- Assignment brief, printed pages 1-14, including Tasks 1-4 and delivery checklist.
- notebooks/healthcare_insurance_analysis.ipynb: 29 cells; all 12 code cells have execution counts; six embedded figures; no saved error outputs; nbformat validation passed during this audit.
- GitHub notebook matches the local notebook's Git blob hash: 6c2324e6c7649f079fd9b72e551fc2d9bdb01e33.
- src/analysis.py; the committed original Streamlit app fetched from GitHub; the local revised app.py; src/report.py; tests; requirements.txt; README.md and evidence records.
- data/raw/insurance.csv and data/processed/insurance_cleaned.csv. Existing cleaned output matches the preparation function without overwriting it. Both contain 1,338 rows; raw data has seven fields, cleaned data eight; zero missing source cells; one repeat after the first retained. Mean 13,270.422265 and median 9,382.033 reconcile. Raw SHA-256: 388eff679557d08ac19f463d025de5e0b4adc482537c8456d19934d78621fd47.
- Public GitHub repository: https://github.com/mmvej/healthcare-insurance-unit1 . Remote main at inspection: f45f9366ee62e8ae94ca1aa824fe5513bff2ac2a, adding .devcontainer/devcontainer.json. Its app.py is still the original five-chart implementation. No remote changes were overwritten or merged for the audit.
- Live Streamlit: https://mnus7hgvzqu2kdugdnuhvu.streamlit.app/ . Opened during the audit. Share dialog showed 'Make this app public' checked; no sharing changes were made. The page displays the original title and five charts.
- Remote filter checks during the audit: all records show 1,338, mean 13,270.42 and median 9,382.03. Selecting smokers only shows 274, mean 32,050.23 and median 34,456.35. Clearing the region selection shows an empty-selection message rather than an exception. The original app repeats this empty message twice, a presentation issue rather than a failure to handle the case.
- Sites: https://healthcare-insurance-unit1-mmvej.moseth.chatgpt.site/ . Source and deployment records document the refined eight-chart web edition. Sites is supplementary; it does not replace the specified Python/Streamlit delivery.

## 1. Isolated assignment tasks

### Task 1 — Analyse applications and define the business problem (brief pp. 4-5)

1.1 Analyse at least three healthcare-insurance analytics applications. For each explain use, required data, supported decisions, benefits, limitations and a realistic example. Research the discussion and separate general domain possibilities from findings obtainable from this CSV.

1.2 Define a specific challenge/opportunity, audience and two or three answerable questions. Explain analytics and a realistic AI contribution; include a relevant data challenge and planning opportunity, stakeholder needs and checks on AI outputs.

Deliverable: a researched business case.

### Task 2 — Prepare and analyse data with Python (brief pp. 5-7)

2.1 Load and profile the real CSV; use pandas selection/filtering/grouping/aggregation, relevant NumPy statistics and suitable Python plots. Handle types and justified derived features; save and validate cleaned data. Explain why unnecessary imputation or encoding is omitted. Show correct outputs, denominators and interpretations.

2.2 Review selections, calculations, transformations and plotting. Show at least two meaningful corrections/improvements with the original issue, revision and validation. Review readability, names, PEP8, comments/docstrings, reuse, error handling, testing and meaningful Git commits. Do not claim unmeasured speed improvements.

2.3 Use a structured ETL/exploratory workflow developed in Jupyter; record Python/pip setup and requirements.txt. Use suitable functions and plots and explain choices. Build the interactive Python Streamlit application from validated cleaned data.

Additional mandatory dashboard deliverable supporting 2.1/2.3: deploy the Streamlit app, test filters/charts/empty selections, reconcile it with the notebook and record a working assessor-accessible URL. Include code/supporting files in GitHub and both delivery links plus setup in README.md.

### Task 3 — Use AI and communicate/evaluate findings (brief pp. 8-9)

3.1 Use AI for a genuine workflow task. Name the tool, justify use, retain selected prompts/responses and acceptance/modification/rejection decisions. Validate code/claims, acknowledge assistance and demonstrate the student's judgement and understanding. Do not upload confidential identifiable health data.

3.2 Use AI to help draft/revise a management narrative from actual analysis. Preserve the prompt, draft, checks and revisions. Include the verified final narrative with the relevant charts in Streamlit; distinguish association from causation. A live AI API is not required.

3.3 Evaluate which questions were answered, partly answered or unresolved; explain stages and choices, data/AI limitations, imbalance/confounding, an alternative approach and its trade-off, lessons and a justified next improvement.

### Task 4 — Apply and justify data management (brief pp. 10-11)

4.1 Record source, acquisition, secondary/primary status, format and permissions. Profile quality and duplicates; document cleaning, before/after counts, exclusions/change record and reload checks. Supply a dictionary with types/meaning/confirmed units, lineage, storage rationale, CSV/database comparison and repeatable error checks.

4.2 Justify handling/processing against alternatives. Assess completeness, consistency, accuracy, timeliness, uniqueness and validity, including what cannot be verified. Explain validation rules and failure actions; privacy, minimisation, access, secure sharing, retention, permission, bias and limits on individual decisions. Consider healthcare standards only where applicable.

## 2. Comparison with our work

'Evidence present' means inspectable material addresses the requirement, not an awarded pass. 'Partial' identifies a concrete outstanding part. 'Unverified' identifies something the available files cannot establish.

| Criterion | Evidence of completion | Gaps / current status |
| --- | --- | --- |
| 1.1 | Notebook cell 2 discusses four applications: resource/cost planning, population grouping, expense estimation and treatment/service evaluation. Each links data needs, management decisions and limitations; references 2-5 support the discussion. | Evidence present. Clinical forecasting and treatment effectiveness are explicitly possibilities needing other data, not claimed results. |
| 1.2 | Cell 3 names finance/operations managers, the planning challenge, three questions, interpretability/source-quality challenges and proposed AI checks. | Evidence present. |
| 2.1 | Cells 5-22 show real raw-file inspection, .loc/Boolean selection, groupby, aggregation, NumPy mean/median/SD, age bands, save/reload validation, six figures and independent csv/statistics checks. | Evidence present for the original analysis. The new sex/dependant dashboard comparisons are not yet added as executed notebook outputs, so final notebook/dashboard scope should be reconciled. |
| 2.2 | Cell 23 records the actual duplicated(False) error/correction, repeat-row policy, mean/median/weighted-group improvements and filter handling. src/analysis.py supplies reusable functions and explicit validation; test_results.txt records 12 passing original tests; real Git commits exist. | Substantial evidence present. The latest revised dashboard's test record has 14 passes and one failure. Current src/report.py/app.py lint check passed. The old four-commit git_history.txt is a historical snapshot, not current history. Clear old/new code snippets for another improvement would strengthen the before/after presentation. |
| 2.3 | Executed Jupyter notebook, separate raw/clean data, requirements.txt, reusable Python ETL and a working deployed Streamlit app. | Core requirement evidenced by original version. The requested eight-chart parity work is local/uncommitted and has not been deployed. Do not confuse this enhancement gap with absence of a Streamlit app. |
| 3.1 | Notebook cell 24 and evidence/ai_use.md name Codex, retain the actual broad task prompt, workflow response, correction, decisions and validation, and acknowledge that the project was assistant-led. | Technical AI-workflow evidence present. Student domain judgement, personal review and ability to explain the code are unverified. The assistant's decisions cannot be presented as proof of the student's independent judgement. |
| 3.2 | Cells 25-26, management_narrative.txt and ai_use.md preserve a draft/revision/check record; the deployed original app shows a filter-aware AI-assisted management narrative. Sites has chart-linked explanations; local src/report.py ports that approach. | Original storytelling requirement has evidence. The final intended wording/figures should be traced to the notebook and AI record after migration; the eight-chart narrative version is not yet deployed to Streamlit. |
| 3.3 | Cell 27 evaluates the three questions, mean/median and alternative chart/statistical choices, absent dates/diagnoses, coverage, imbalance/confounding and AI limitations; it proposes dated claims/enrolment/clinical data. | Evidence present. No causal or live-budget success claim is made. Personal lessons/understanding still require the student's review. |
| 4.1 | Cell 28, evidence/source.md and kaggle_metadata.json, raw/clean files, cleaning_changes.csv and reload checks show source/CC0/acquisition, dictionary, lineage and CSV/PostgreSQL comparison. | Evidence present. Source currency is not confirmed; Sites uses USD as an explicit display assumption in expandable notes. Retain that distinction in the final app and notebook. |
| 4.2 | Cell 28 addresses all six quality dimensions, explicit checks, failure actions, valid outliers, duplicate uncertainty, minimisation, restricted operational access, sharing/retention, licence limits, bias and conditional ICO/FHIR relevance. | Evidence present as practical public-data handling plus a reasoned operational policy discussion. Real insurer access controls or FHIR integration were not implemented and are not needed for this public CSV project. |

## 3. Mandatory delivery checklist

| Required deliverable | Current evidence | Status |
| --- | --- | --- |
| Executed .ipynb with outputs and criterion labels | Notebook validated; 12 executed code cells, six images, no saved error outputs; GitHub copy matches. Prior fresh-kernel success log exists. | Present. This audit inspected saved outputs and prior execution evidence; it did not rerun the full notebook. |
| Reproducible environment and package list | requirements.txt pins packages; notebook/README record setup. The original app successfully installed and ran in Streamlit Cloud on Python 3.14. | Present for original version; repeat final checks after revision. |
| Raw/processed separation and permissions | raw insurance.csv preserved, cleaned CSV included under separate folder, source licence metadata and change record retained. | Present. |
| GitHub with meaningful history and assessor access | Public repository confirmed; notebook, original app, data and documents are available, with separate commits. | Present for committed version. src/report.py, revised app.py, theme configuration and new tests are not yet committed. |
| Working deployed Python Streamlit URL | Live URL verified and public setting checked; smoking and empty-selection tests passed in browser during this audit. | Present. Sites is an additional web edition, not a substitute. |
| Final dashboard version matches intended report | Live Streamlit still has five charts and original wording. Eight-chart/native revision exists locally. | Partial: migration requested by the user remains unfinished. Eight charts themselves are not a minimum imposed by the brief. |
| Final tests documented and errors resolved | Historical original suite: 12 passed. Latest local suite: 14 passed, 1 failed, in streamlit_parity_tests.txt. Failure is tests/test_report.py:47 expecting ['light'] while AppTest returns 'light'. | Partial. This failure is a test-interface expectation mismatch, not evidence that theme switching itself crashed. Correct/validate the expectation and rerun before claiming a clean final run. |
| README with both submission URLs and setup | GitHub URL and setup are present. README line 11 still says Streamlit deployment is pending and omits the actual deployed URL. | Not complete. Explicit brief requirement unmet in the document. |
| Current testing/delivery documentation | evidence/testing.md still says no remote Streamlit URL/test is claimed and describes five charts; the actual deployment and newer work are not reconciled there. | Partial: update to accurate current status and distinguish historical checks from final checks. |
| Final narrative/check record and consistent units | Original narrative record matches original notebook/live app; newer chart explanations and USD display assumption are documented elsewhere. | Partial final reconciliation, not absence of narrative. |
| Student attribution, review and ability to explain | AI assistance and sources acknowledged; no independent authorship claim invented. | Attribution present; student's understanding/review unverified. |
| Submit both links through college channel | No submission receipt or confirmation supplied. | No evidence of completion. Do not submit or claim submission on the student's behalf. |

## 4. What is optional or not required

- Predictive regression is explicitly optional. Its absence is not a missing pass requirement. If added, a split, baseline, error measure, leakage controls and uncertainty would become necessary for that extension.
- A live AI API is not required; verified AI-assisted drafting with a record is sufficient in principle.
- Joins, extra formats, APIs and image analysis are only required when relevant to the chosen questions. They are unnecessary for this one-file analysis.
- Encoding, imputation and hypothesis testing are not compulsory techniques. Explaining why they are unnecessary is part of the expected performance.
- A precise map is not required and should not be fabricated without geographic information.
- The brief asks for suitable controls; it gives age/smoking/region filters as examples. It does not prescribe a particular colour theme, eight charts, a custom toggle, or the Sites layout. Those are user-requested presentation choices.
- Unknown clinical accuracy, dates, coverage or currency cannot be repaired by guessing; explaining limits is required, not inventing provenance.

## 5. Prioritised completion actions

1. Finish the already-requested native Streamlit migration. Preserve the remote .devcontainer addition when synchronising; do not overwrite other remote work.
2. Correct the theme query-parameter test expectation based on the installed AppTest interface, rerun the final suite and inspect the revised app in both themes and with partial/empty selections. Publish only the validated revision, then check the live deployment.
3. Add the real Streamlit URL to README.md. Refresh the testing record and make clear which version each result covers. Both submission links should be unambiguous.
4. Add executed notebook evidence for the new sex/dependant analyses or otherwise clearly align the final dashboard scope and its numerical checks with the submitted notebook. Update the AI-use/narrative record to trace the final explanations and display assumptions.
5. Review the work personally, record genuine judgement/changes where appropriate, and be ready to explain the code and conclusions. The assistant cannot supply evidence of the student's understanding.
6. Confirm the assessor can open the final public links and submit through the college's designated channel. Retain submission evidence.

The audit does not label the whole assignment complete merely because the visible dashboard looks finished. Conversely, it does not mark the original analysis absent merely because the newer presentation work is unfinished.
