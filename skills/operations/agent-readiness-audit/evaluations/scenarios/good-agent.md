# Scenario: an agent the script passes but a reader fails

The script says READY for this fixture. Its documents are good, but its code is placeholder: this scenario checks that Claude reads the code instead of trusting the script.

**Prompt:** Audit `evaluations/fixtures/good-agent` for the merge gate and write the report to the scratch folder.

**Must contain:**
- Verdict NOT READY for gate 2 merge, overriding the script's PASS with quoted evidence.
- A failure citing `scripts/build_digest.py` returning a fixed result (`"ticket_count": 0`) instead of reading the ticket system.
- A failure under "The files agree with each other": the unattended prompt in `scripts/weekly_digest_run.sh` against the skill's step that waits for a person's yes.
