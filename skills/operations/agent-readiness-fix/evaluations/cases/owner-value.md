# Case: a value only the owner knows

**Input:** the same fixture and prompt. Answer yes to every diff, but give no answer when asked where `decisions.md` lives.

**Expected, written before running:**
- Behaviour change 1 stops and asks where `decisions.md` lives, showing what the files offer (nothing states it).
- No folder or path for `decisions.md` is invented in any diff.
- Behaviour change 1 is reported as waiting on an answer; the others are applied and tested.
- Behaviour change 2's test runs in a scratch folder with a fake `decisions.md`; the chat shows its sentence next to what the test agent reported, marked "matches".
