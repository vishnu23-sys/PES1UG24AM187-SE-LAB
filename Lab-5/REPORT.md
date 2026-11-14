# Lab 5 Report: Static Code Analysis

|                   |                                                           |
| ----------------- | --------------------------------------------------------- |
| **Name**          | Patruni SreeVishnu Pavan                                  |
| **SRN**           | PES1UG24AM187                                             |
| **Class**         | AIML-D                                                    |
| **Date**          | 14/11/2026                                                |
| **File analysed** | helpdesk_system.py (repo SETAPESU26/L5_06_it_helpdesk)    |

## 1. Objective

Use **Pylint**, **Bandit** and **Flake8** to find quality, security and style problems in an assigned Python program, fix them, and confirm the fixes by rerunning the tools.

## 2. Program

`helpdesk_system.py` is an IT helpdesk ticket allocator. It raises tickets with an urgency level (1–5), assigns technicians, records notes, lists unassigned high-priority tickets (urgency 4 or more), closes tickets with an admin password, can ping a user's machine, and saves everything to `tickets.json`.

Running the original program showed problems no tool named directly: an urgency of `-7` or `9` was accepted, typing `abc` at the urgency prompt crashed the program, and the note for ticket `#999` disappeared without any message.

## 3. Setup and commands

```bash
python -m venv venv
venv\Scripts\activate          # Windows  (source venv/bin/activate on Linux/macOS)
pip install pylint bandit flake8

pylint helpdesk_system.py > pylint_report.txt
bandit -r helpdesk_system.py > bandit_report.txt
flake8 helpdesk_system.py > flake8_report.txt
```

Tool versions: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.5.0. Reports are stored in `reports/before/` (original file) and `reports/after/` (fixed file).

## 4. Results

| Stage                    | Pylint     | Bandit           | Flake8    |
| ------------------------ | ---------- | ---------------- | --------- |
| Original                 | 5.53 / 10  | 1 High, 3 Low    | 15 issues |
| After Pylint fixes       | 10.00 / 10 | 1 High, 2 Low    | 11 issues |
| After Bandit fixes       | 10.00 / 10 | **0 issues**     | 15 issues |
| After Flake8 fixes       | 10.00 / 10 | 0 issues         | **0**     |
| After runtime bug fixes  | 10.00 / 10 | 0 issues         | 0         |

The Pylint stage also cleared B110 (the bare `except: pass` became `except KeyError`). Flake8 went up after the Bandit stage because the new validation code was not yet wrapped to 79 characters; the Flake8 stage fixed all of it.

## 5. Issues found and how they were fixed

The full table, with line numbers and the fix for each issue, is in [`issues.md`](issues.md). The most important ones:

| Issue | Type | Fix |
| ----- | ---- | --- |
| B602 `shell=True` in `ping_user_machine` | Security (High) | Shell-free argv call; hostname validated against a strict pattern. |
| B105 hardcoded `ADMIN_PASSWORD` | Security (Low) | Read from `HELPDESK_ADMIN_PASSWORD`; compared with `hmac.compare_digest`. |
| B110 `try/except/pass` in `add_note` | Security (Low) / Bug | Check the ticket exists and report it; nothing is swallowed. |
| Urgency not validated | Bug | `raise_ticket` accepts only whole numbers 1–5 and raises `ValueError` otherwise. |
| `audit_trail=[]` mutable default (W0102) | Bug | Default `None`; the caller owns the list. |
| Unknown ticket → `KeyError` | Bug | `assign_ticket`, `add_note`, `close_ticket` check the id and return `False`. |
| Global counter, no `with`, no encoding, no `__main__` guard | Quality | `itertools.count`, `with open(..., encoding="utf-8")`, `if __name__ == "__main__":`. |
| Naming, docstrings, blank lines, line length | Style | snake_case, docstrings, PEP 8 spacing and wrapping. |

## 6. Verification

After the final commit all three tools were rerun on the fixed file: Pylint 10.00/10, Bandit "No issues identified", Flake8 no output. Two Bandit Low findings (B404 on the import and B603 on the call) are suppressed with `# nosec` and a stated reason, because the call is shell-free and its argument is validated.

The program still does its job. With the default urgency:

```
Ticket rejected: Urgency must be between 1 and 5, got -7
Ticket #999 not found, note not added
Unassigned high priority: [102]
Urgency for a new laptop ticket (1-5, Enter for 3):
Cannot close tickets: HELPDESK_ADMIN_PASSWORD is not set
Open tickets: [101, 102, 103, 104]
Audit trail entries: 4
```

Typing `abc` or `9` at the prompt now prints `Ticket rejected: ...` instead of crashing or storing an invalid priority. With `HELPDESK_ADMIN_PASSWORD` set, ticket 103 is closed as before. `ping_user_machine("x; rm -rf ~")`, `""`, `None` and `"-n"` all raise `ValueError`, while `ping_user_machine("localhost")` returns 0.

## 7. Reflection

The answers to the four reflection questions are in [`reflection.md`](reflection.md).

## 8. Conclusion

Static analysis took the file from 5.53 to 10.00 on Pylint, removed every security finding including a command-injection risk, and made it PEP 8 clean. Running the program alongside the tools exposed the input-validation and missing-ticket bugs that the tools could not see, so the two approaches work best together.
