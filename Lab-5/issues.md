# Lab 5 – Issue Table (helpdesk_system.py)

Before: Pylint **5.53/10**, Bandit **1 High / 3 Low**, Flake8 **15**.
After: Pylint **10.00/10**, Bandit **0**, Flake8 **0**.
Reports: [`reports/before/`](reports/before/) and [`reports/after/`](reports/after/).

Line numbers refer to the original file from SETAPESU26/L5_06_it_helpdesk. High and medium severity issues are listed first.

| Issue | Type | Line(s) | Description | Fix Approach |
| ----- | ---- | ------- | ----------- | ------------ |
| B602 subprocess with `shell=True` | Security (High) | 38 | `"ping -c 1 " + hostname` is run through a shell, so a hostname like `pc1; rm -rf ~` runs any command the caller likes (command injection, CWE-78). | Removed `shell=True`; call `[ping, "-c"/"-n", "1", hostname]` as an argv list; accept only a valid hostname (letters, digits, `.`, `-`, cannot start with `-`), else `ValueError`. |
| B105 Hardcoded password | Security (Low) | 8, 54 | `ADMIN_PASSWORD = "helpdesk@123"` is committed to source control, and `main()` repeats it. | Read from the `HELPDESK_ADMIN_PASSWORD` environment variable; closing is refused when it is not set. Compared with `hmac.compare_digest`. |
| B110 try / except / pass | Security (Low) | 21–24 | `add_note` swallows every error, so a note for a ticket that does not exist (`add_note(999, ...)`) disappears silently. | Check the ticket exists, print "not found" and return `False`; no `try/except` needed. |
| B404 subprocess import | Security (Low) | 2 | Informational flag on importing `subprocess`. | Kept (needed for ping); `# nosec B404` with a reason, since the call is shell-free and the input is validated. The B603 on the call is suppressed the same way. |
| Urgency not validated (not tool-flagged) | Bug | 13, 48, 52–53 | `int(urgency)` accepts `-7` and `9` (outside 1–5), and typing `abc` at the prompt crashes the program with a `ValueError` traceback. | Validate in `raise_ticket`: whole number 1–5, else `ValueError` with a clear message; `main()` catches it and prints "Ticket rejected". |
| Mutable default argument (W0102) | Bug | 10, 14 | `audit_trail=[]` is created once and shared by every call; the audit entries pile up in a hidden list nobody can read. | Default to `None`; only append when the caller passes a list. `main()` now keeps its own audit trail. |
| Unknown ticket crashes (not tool-flagged) | Bug | 17–18, 26–28 | `assign_ticket(555, ...)` and `close_ticket(555, ...)` raise `KeyError`. A wrong password silently does nothing. | Check `ticket_id in tickets` first, print a message and return `False`; wrong password prints a message too. |
| Global counter (W0603) | Quality | 7, 11–12 | `global ticket_counter` mutated from a function; Pylint also flags the lowercase module constant (C0103). | Replaced with `TICKET_IDS = itertools.count(101)` and `next(TICKET_IDS)`. |
| `open()` without encoding / `with` (W1514, R1732) | Quality | 41–43 | File opened without an encoding and closed by hand, so an error while writing leaks the handle. | `with open(file, "w", encoding="utf-8") as handle:`. |
| No `__main__` guard (not tool-flagged) | Quality | 58 | `main()` runs on import: importing the module asks for input and writes `tickets.json`. | `if __name__ == "__main__": main()`. |
| Singleton comparison, dict iteration (C0121, C0206) | Quality | 32–33 | `== None` and `for t in tickets: tickets[t][...]`. | `is None` and `for ticket_id, ticket in tickets.items()`; `4` became the `HIGH_PRIORITY` constant. |
| Naming (C0103) | Style | 30 | `unresolvedHighPriority` is camelCase. | Renamed to `unresolved_high_priority` and updated the call site. |
| Missing docstrings (C0114, C0116 ×8) | Style | 1, 10–45 | No module or function docstrings. | Added short docstrings. |
| `%` formatting (C0209), unused `t2` (W0612 / F841) | Style | 14, 47 | Old-style formatting; `t2` assigned but never used. | f-string; dropped the unused variable. |
| E302 / E305 blank lines ×9 | Style (Flake8) | 10–58 | One blank line between top-level functions, two required. | Two blank lines everywhere. |
| E501 line too long ×3 | Style (Flake8) | 13, 14, 52 | Lines of 118, 86 and 80 characters. | Split the ticket dict over several lines and shortened the others. |
| E722 bare except, E711 `== None` | Style (Flake8) | 23, 33 | Same findings as B110 and C0121 above. | Fixed by the changes above. |

Not changed on purpose: the demo still calls `add_note(999, ...)` and raises a ticket with urgency `-7`. Those are deliberate error-path demonstrations and now print clean messages instead of failing silently or being accepted.
