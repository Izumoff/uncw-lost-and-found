# Sprint 3

## User Story:
Campus Administrator can view system activity logs

| Test Case | Input | Expected Output | Actual Output |
|---|---|---|---|
| 1 (Success) | **Precondition:** Logged in as superuser. 1. Open `/admin-console/` 2. Click **System Activity** | System opens System Activity page | Passed. Admin Console opened and System Activity page loaded successfully |
| 2 (Access Control) | **Precondition:** Logged in as regular campus user. 1. Open `/admin-console/activity/` | User is redirected to `/reports/` | Passed. Non-admin user was redirected to reports page |
| 3 (Display Logs) | **Precondition:** At least one admin action exists (e.g., user role change). 1. Open `/admin-console/activity/` | System displays list of activity logs in table | Passed. Activity table displayed multiple log records |
| 4 (Empty State) | **Precondition:** No log entries exist. 1. Open `/admin-console/activity/` | Informational message “No system activity records are available” is shown | Not observed (logs already exist). Behavior assumed correct |
| 5 (Readable Description - Before Fix) | **Precondition:** Logs contain change messages. 1. Open `/admin-console/activity/` | Description should be readable | Failed. Raw JSON-like messages displayed (e.g., {"changed": {"fields": [...]}})  fixed |
| 6 (Readable Description - After Fix) | Same as above | Description shows simplified text (e.g., “Fields updated”, “Object created”) | Passed. Descriptions are now readable and user-friendly |
| 7 (Navigation Back) | 1. Click **Back to Admin Console** button | System returns to Admin Console page | Passed. Navigation returned to Admin Console successfully |
| 8 (Page Stability) | 1. Refresh `/admin-console/activity/` multiple times | Page loads consistently without errors | Passed. No crashes or errors observed |
| 9 (Data Safety) | 1. Open activity page 2. Observe database | No data is modified | Passed. Page is read-only, no data changes occurred |
