# Lab 5: Static Code Analysis — IT Helpdesk Ticket Allocator

Static analysis of `helpdesk_system.py` (an IT helpdesk ticketing script) using **Pylint**, **Bandit** and **Flake8**, followed by fixing every reported issue and the bugs found by running the program. The original script comes from the assigned repo [SETAPESU26/L5_06_it_helpdesk](https://github.com/SETAPESU26/L5_06_it_helpdesk).

## Results

| Tool   | Checks                                  | Before        | After      |
| ------ | --------------------------------------- | ------------- | ---------- |
| Pylint | Code quality, naming, docstrings, logic | 5.53 / 10     | 10.00 / 10 |
| Bandit | Security                                | 1 High, 3 Low | 0 issues   |
| Flake8 | PEP 8 style                             | 15 issues     | 0 issues   |

## What I changed

- **Security (Bandit):** removed `shell=True` from `ping_user_machine` (command injection) and validate the hostname; the admin password is read from the `HELPDESK_ADMIN_PASSWORD` environment variable instead of being hardcoded; `add_note` no longer swallows errors with `try/except/pass`.
- **Bugs found by running the program:** urgency `-7` and `9` were accepted and `abc` crashed the program, so `raise_ticket` now only accepts 1–5. `assign_ticket` and `close_ticket` crashed with `KeyError` on an unknown ticket. The `audit_trail=[]` default was shared by every call. `main()` ran on import.
- **Quality (Pylint):** snake_case names, docstrings, `itertools.count` instead of a `global` counter, `with open(..., encoding="utf-8")`, `is None`, `.items()`.
- **Style (Flake8):** blank lines, line length, bare `except`, `== None`, unused variable.

The full write-up is in [`REPORT.md`](REPORT.md); the issue table is in [`issues.md`](issues.md) and the reflection answers are in [`reflection.md`](reflection.md).

## Running it

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (source venv/bin/activate on Linux/macOS)
pip install pylint bandit flake8

python helpdesk_system.py

pylint helpdesk_system.py > pylint_report.txt
bandit -r helpdesk_system.py > bandit_report.txt
flake8 helpdesk_system.py > flake8_report.txt
```

Optional environment variable: `HELPDESK_ADMIN_PASSWORD` (closing tickets is refused when it is not set).

## Folder structure

```
Lab-5/
├── helpdesk_system.py   # fixed source
├── REPORT.md            # lab report
├── issues.md            # issue table (what, where, how it was fixed)
├── reflection.md        # reflection answers
├── README.md
└── reports/
    ├── before/          # pylint / bandit / flake8 reports on the original file
    └── after/           # the same reports on the fixed file
```

## Submission checklist

- [x] Cleaned `helpdesk_system.py` with all reported issues fixed (at least 4 required)
- [x] Issue table (`issues.md`)
- [x] Reflection answers (`reflection.md`)
- [x] Pylint score above 9.5 (10.00 / 10)
- [x] Before and after `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt`
- [x] Commit history: original with errors, then one fix commit each for Pylint, Bandit, Flake8 and the runtime bugs
