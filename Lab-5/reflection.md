# Lab 5 – Reflection

## 1. Which issues were easiest and which were hardest to fix, and why?

Easiest were the Flake8 findings and the Pylint naming and docstring messages: each one names the line and the fix is mechanical (two blank lines, `is None`, snake_case, a one-line docstring). The hardest was B602 (`shell=True` in `ping_user_machine`). Removing the flag is not enough, because the function still has to run `ping`: I had to decide what a legal hostname looks like, reject anything else (including a value starting with `-`, which `ping` would read as an option), find `ping` with `shutil.which`, and pass an argv list. The urgency bug was also harder than it looked, because the fix had to change behaviour (reject bad input) without breaking the demo, so `main()` now catches the error and keeps going.

## 2. Did the tools report anything that was a false positive or not worth fixing?

B404 (importing `subprocess`) is informational: the import itself is not the problem, how it is used is. I kept the import and added a `# nosec` with a reason, and did the same for B603 on the call once it was shell-free and validated. B105 was a fair hit even though it is a demo value: the password was in source control and repeated in `main()`. B110 (try/except/pass) looked like a style complaint but pointed to a real bug: notes for missing tickets vanished without any message.

## 3. What did static analysis miss that you found another way?

Running the program found the bugs no tool named. An urgency of `-7` or `9` was stored without complaint, and typing `abc` at the prompt crashed with a traceback. `assign_ticket` and `close_ticket` raised `KeyError` for an unknown ticket, and a wrong admin password silently did nothing. `main()` also ran on import, asking for input and writing `tickets.json`. Pylint did flag `audit_trail=[]` (W0102), but only as a generic "dangerous default value"; I only saw what it meant (every audit entry piling up in one hidden list) by printing the function's defaults after a run. The tools find patterns, not intent, so running and reading the code is still needed.

## 4. How would you use these tools in a real workflow?

Run Flake8 and Pylint as pre-commit hooks and in CI so style and quality regressions fail the build, and run Bandit in CI with a rule that Medium and High findings block the merge. Every suppression (`# nosec`, `# pylint: disable`) should carry a reason and be looked at in review. Fix by severity: security first, then bugs, then style. Pin the tool versions so a new release does not suddenly fail every build. The tools catch the cheap problems early, which leaves code review free to focus on design and logic.
