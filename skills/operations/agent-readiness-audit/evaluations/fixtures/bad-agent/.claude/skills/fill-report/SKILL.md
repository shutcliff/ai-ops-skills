---
name: Fill_Report
description: Fills the report.
---

# Fill the report

Fetch the Metabase cards and write them into the sheet. Update the HubSpot company record with the new score as needed.

Steps:
1. Run `python3 scripts/fetch_cards.py` and `python3 scripts/compute_score.py` (this supersedes the older note about computing by hand).
2. If relevant, adjust the score. This is a judgment call.
3. Write the sheet. Typically the row for today is empty; if not, overwrite it.
4. Post the summary to Slack when appropriate.
5. Files live in /home/jane.doe/Documents/reports.
6. Usually the numbers roughly match; if in doubt, use your best estimate.
7. TODO: handle the case where Metabase returns nothing.
8. Where relevant, ping the owner, etc.
