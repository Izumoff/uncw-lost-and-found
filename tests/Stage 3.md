# Sprint 3

## User Story:
Campus Community User can view published Lost and Found reports

| Test Case  | Input | Expected Output | Actual output |
|---|---|---|---|
| 1 (Success) | **Precondition:** Database contains one published report and one unpublished report. 1. Open `/reports/` 2. Observe the reports list | The system shows the published report in the list | Passed. `/reports/` opened successfully and the published report was displayed in the reports list |
| 2 (Failure) | **Precondition:** Database contains one unpublished report. 1. Open `/reports/` 2. Check whether the unpublished report appears in the list | The unpublished report is not shown in the list | Passed. The unpublished report did not appear on the reports list page |
| 3 (Success) | **Precondition:** At least one published report exists in the list. 1. Open `/reports/` 2. Click **View** for the published report | The system opens the detail page for the selected published report | Passed. The **View** link worked and opened the published report detail page |
| 4 (Success) | **Precondition:** A published report detail page is open. 1. Verify report title 2. Verify type 3. Verify location 4. Verify created date 5. Verify description | The detail page displays all main report fields in read-only mode | Passed. Title, type, location, created date, and description were shown correctly |
| 5 (Failure) | **Precondition:** One unpublished report exists in the database. 1. Manually open `/reports/<unpublished_id>/` in browser | The system blocks access to the unpublished report detail page | Passed. Direct access to the unpublished report detail page was blocked with 404 behavior |
| 6 (Success) | **Precondition:** A published report detail page is open. 1. Click **Back to Reports** | The system returns to the published reports list page | Passed. The **Back to Reports** link returned to `/reports/` successfully |
| 7 (Success) | **Precondition:** User has admin access. 1. Open Django admin 2. Open Report records 3. Confirm one report has `is_published = checked` and another has `is_published = unchecked` | The test data can be managed through admin for Stage 3 verification | Passed. Report model was available in admin and both test records were created successfully |
