# Test Cases

**Sprint 3**
**Stage 16 — Admin Console: Usage Monitoring**
**User Story:** Campus Administrator can view summary statistics (reports, users, activity)

| Test Case | Input | Expected Output | Actual Output |
|---|---|---|---|
| Open Usage Monitoring from Admin Console | Log in as Django superuser  open Admin Console  click **Usage Monitoring** | Usage Monitoring page opens successfully | Passed — page opened successfully |
| Direct admin route access | Log in as Django superuser  open `/admin-console/usage/` | Usage Monitoring page opens successfully | Passed — route works |
| Non-admin access restriction | Log in as non-admin user  open `/admin-console/usage/` | User is redirected to Reports page | Passed — redirect works |
| Admin Console link visibility | Log in as Django superuser  open Admin Console | **Usage Monitoring** button is visible | Passed — button visible |
| Existing admin links still work | Open Admin Console and use **View All Reports**, **Manage Users & Roles**, **System Activity** | Existing admin pages still work | Passed — existing buttons still work |
| Reports statistics section renders | Open Usage Monitoring page | Reports panel shows count values for report totals and statuses | Passed — reports statistics displayed |
| Users statistics section renders | Open Usage Monitoring page | Users panel shows count values for users and role groups | Passed — users statistics displayed |
| Activity statistics section renders | Open Usage Monitoring page | Activity panel shows total log count and latest activity or fallback text | Passed — activity statistics displayed |
| Back button works | Open Usage Monitoring page  click **Back to Admin Console** | Returns to Admin Console page | Passed — button works |
| Page loads without template error | Open Usage Monitoring page after creating template | Page renders normally | Passed — template works |
