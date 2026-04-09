# Sprint 3

## User Story:
Campus User can close own Lost Item report

| Test Case | Input | Expected Output | Actual output |
|---|---|---|---|
| 1 (Success) | **Precondition:** Logged in as Campus User who owns an open Lost Item report. 1. Open `/reports/<id>/` for that report 2. Observe available actions | **Close My Report** button is visible | Passed. The owner of the open Lost Item report could open the detail page and the **Close My Report** button was visible |
| 2 (Success) | **Precondition:** Logged in as Campus User who owns an open Lost Item report. 1. Open `/reports/<id>/` 2. Click **Close My Report** | The system closes the report, redirects back to the detail page, and shows a success message | Passed. After clicking **Close My Report**, the page reloaded successfully and displayed **Report was closed successfully** |
| 3 (Success) | **Precondition:** Same report was closed in previous step. 1. Refresh `/reports/<id>/` 2. Check report details and available actions | Outcome is shown as **Closed** and **Close My Report** button is no longer visible | Passed. The report detail page showed the report as closed, and the **Close My Report** button disappeared |
| 4 (Failure) | **Precondition:** Logged in as Campus User who owns a Found Item report. 1. Open `/reports/<id>/` for the found report 2. Check available actions | **Close My Report** button is not shown for Found reports | Passed. The **Close My Report** button did not appear on the Found Item report detail page |
| 5 (Failure) | **Precondition:** Logged in as Campus User, open a report owned by another user. 1. Open `/reports/<id>/` for another user's report 2. Check available actions | **Close My Report** button is not shown for non-owner | Passed. The button was not visible for a report owned by another user |
| 6 (Failure) | **Precondition:** Logged in as Campus User who owns a Lost Item report that is already closed. 1. Open `/reports/<id>/` 2. Check available actions | **Close My Report** button is not shown for already closed report | Passed. The already closed report detail page did not show the **Close My Report** button |
| 7 (Regression / Fixed) | **Precondition:** Staff close logic exists in project. 1. Review staff close flow after implementation 2. Open and use staff report actions | Staff close/report management still works correctly and no duplicate close logic breaks behavior | Failed initially: duplicate `close_report()` logic in `app/views.py` conflicted with the model and overrode the correct implementation. **Fixed.** After Hotfix, only one correct `close_report()` remained and staff close flow stayed consistent |
