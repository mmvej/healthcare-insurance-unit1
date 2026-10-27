# Sites deployment

27 October 2026. The user requested deployment with Sites.

Live URL: https://healthcare-insurance-unit1-mmvej.moseth.chatgpt.site

Sites confirmed status succeeded. Access remains private to the owner by default; no sharing changes were made. This is an HTML/JavaScript web edition of the validated analysis, not a hosted Streamlit server. The Python app remains in app.py. The assignment's requirement for a deployed Streamlit app is not claimed as met by this alternative. Assessor agreement and suitable access are needed if this version is submitted instead.

Project ID: appgprj_6ae1003609c48191bab3e4a6126124d3
Saved version ID: appgprj_6ae1003609c48191bab3e4a6126124d3~appgver_b9cc557b03348191b44f0b177b87bb96
Deployment ID: appgdep_6ae100cc13048191932f98cd60276dba
Deployed Sites source commit: 0094e4cda60dab4925b1db779aed69fed4859927

The Sites source helper pushed the source and packaged the static deployment archive before native publication. A copy of the published web assets is included in web_dashboard/ in the assignment GitHub repository. No credentials are included.

Local checks: JavaScript syntax validation passed. The preview loaded all 1,338 records, showing mean 13,270.42, median 9,382.03 and smoking-group means 32,050.23 and 8,434.27, matching the executed Python notebook. Selecting southeast and smoking=yes showed 91 records, mean 34,845.00, median 37,484.45 and SD 11,324.77. Clearing every region hid results and displayed the empty-selection message. Five chart containers rendered with actual data. A browser screenshot review identified implicit SVG path fill on axes; a scoped CSS fix removed that fill, and a second visual review confirmed the histogram, box plot and regional bars displayed correctly. Source data, filter logic and chart encodings were preserved.

The notebook and its download are linked from the source-details section. Native Sites publication success confirms deployment; an unauthenticated assessor-access test is not claimed for this private site. Mobile browser QA was not performed.

## Variable definitions update

27 October 2026: added a visible 'What each variable means' section defining age, sex, BMI, covered dependants (children), smoking status, region, charges and the derived age_band. Each definition includes type/values and relevant source limitations. Added explanations of record count, mean, median, sample SD, quartiles/IQR and association. Full-file ranges are explicitly distinguished from filtered selections. All eight field names were checked against the source schema and derived field. The rendered table was checked in the browser for readable wrapping. Existing chart and filter code was unchanged.

Published successfully from Sites source commit f66154b8599e68be57c8659d22bd9fa32e988b47.
Saved version: appgprj_6ae1003609c48191bab3e4a6126124d3~appgver_35ad525098888191bfd5a9eb26a7a08e
Deployment: appgdep_6ae101ee05388191958b99746565bda3

## Display units update

27 October 2026: at the user's request, the main dashboard now uses USD for charges and kg/m² for BMI. Repeated uncertainty phrases were replaced with consistent unit labels and one visible working-assumption note. No conversion, annualisation or change to underlying values was applied. The original notebook and source record retain their acquisition-time provenance assessment. JavaScript syntax and unit-wording checks passed.

Sites source commit: 6b019687c1be278deeaf3c3882a13e2d6ddeef14
Deployment succeeded: appgdep_6ae10253c5a881918a78567f99db4078

## Relationship narrative

27 October 2026: added 'What the data tells us' above the filters, covering smoking, age, BMI, region, sex and covered dependants in relation to charges. Figures were recomputed from the cleaned CSV using pandas group summaries and Pearson correlations. The narrative reports counts, means/medians, within-smoking correlations, different regional rankings and the reversal of the sex-group mean comparison within non-smokers. Full-sample scope is stated explicitly so fixed findings are not misrepresented as filtered results. The analysis remains descriptive and does not claim causal or fully adjusted effects.

## Default dark mode

Added a keyboard-accessible Dark mode switch, defaulting to dark for new visitors. Valid light/dark preferences are remembered in localStorage; storage failure falls back safely to dark. Theme is restored before first paint. Page, controls, table text, chart axes and chart series use corresponding theme colours. Browser checks confirmed default dark, switching to light, persistence after reload and switching back. Explicit chart palette values avoid a browser colour-transformation issue seen with CSS-variable SVG fills; computed blue/orange series colours were rechecked. JavaScript syntax validation passed. Data calculations were unchanged.

## Findings placement

Moved the full-sample findings section after all five visualisations and the regional group table, before variable definitions, at the user's request. Updated the filter reference from 'below' to 'above'. Confirmed the HTML order and preserved all charts, data, calculations and theme controls.

## Visual-first revision

Replaced the extended relationship narrative with three additional filter-aware comparison charts: smoking-group mean/median, sex-group means within smoking categories, and dependant-count mean/median. All include direct numeric labels and counts. The original five charts remain, giving eight visualisations. The selected-group paragraph is reduced to a brief scope/causality note. Definitions and supporting limitations remain below the visualisations. Browser review confirmed the smoking chart's readability and checked the rendered numeric labels against the Python summaries. A smoking=yes-only selection showed 274 records and updated all eight charts. JavaScript syntax check passed.
