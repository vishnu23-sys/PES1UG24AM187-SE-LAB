# Lab 6: Code and Branch Coverage — Event Ticket Tier

Line and branch coverage analysis of `event_ticket_tier.py` (event ticket pricing by seating tier, order volume and promo codes, a fraud and audit check, plus gate turnstile monitoring) using **coverage** and **pytest**. The original module and starter test come from the assigned repo [SETAPESU26/L6_L7_06_event_ticket_tier](https://github.com/SETAPESU26/L6_L7_06_event_ticket_tier).

## Results

Coverage of `event_ticket_tier.py` (57 statements, 40 branches):

| Test file                                   | Tests | Line coverage | Branch coverage | Missing  |
| ------------------------------------------- | ----- | ------------- | --------------- | -------- |
| `test_event_ticket.py` (starter)            | 1     | 51%           | 46%             | 28 lines |
| `CodeCoverageTest_event_ticket_tier.py`     | 11    | 100%          | 99%             | `39->48` |
| `BranchCoverageTest_event_ticket_tier.py`   | 28    | 100%          | 100%            | none     |

## Line coverage vs branch coverage

`CodeCoverageTest_event_ticket_tier.py` runs every line of `event_ticket_tier.py`, so line coverage is 100%. Branch coverage is still 99%, because one decision was only ever taken one way:

- `39->48`: inside `if promo_code == "FRAUD_RISK":`, the check `if tier == "vip":` was never False. The only fraud test used a VIP manifest, which wipes the manifest and breaks out of the loop.

Taking that branch the other way showed something line coverage hid: a `FRAUD_RISK` order on a **premium or general** manifest is counted as rejected but is **still billed**, because the code falls through to `manifest_total += order_price`. Two premium seats flagged as fraud still bill 180.0 with status `COMPLETED`. The module is left unchanged as the lab requires, and the test documents the current behaviour, but this is likely a bug worth raising.

`BranchCoverageTest_event_ticket_tier.py` adds tests for the missing path and for edge cases:

- non-VIP `FRAUD_RISK` order (rejected but billed), and VIP fraud skipping later orders while the lounge fee is still added
- negative tax rate, empty manifest list, missing `tier` (defaults to general) and missing `is_confirmed` (skipped)
- a lounge-only manifest with no orders
- the bulk discount boundary (4 seats: none, 5 seats: −20) and `EARLYBIRD` replacing the bulk discount
- the audit boundary (exactly 4 rejections is fine, 5 is `AUDIT_REJECTED`) and audit taking priority over `ZERO_SALES`
- several manifests summed before tax
- gate flow: `None`, a rate of exactly 50 (not congested), overflow in a later stream, the streak resetting between streams, and an empty stream

## Running it

```bash
pip install coverage pytest

# line coverage
coverage run -m pytest CodeCoverageTest_event_ticket_tier.py
coverage report -m --include=event_ticket_tier.py

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_event_ticket_tier.py
coverage report -m --include=event_ticket_tier.py
```

## Folder structure

```
Lab-6/
├── event_ticket_tier.py                      # module under test (unchanged)
├── test_event_ticket.py                      # starter test from the assigned repo
├── CodeCoverageTest_event_ticket_tier.py     # tests for line coverage
├── BranchCoverageTest_event_ticket_tier.py   # tests for branch coverage
├── README.md
└── screenshots/
    ├── starter_coverage.png                  # starter test only (51% line, 46% branch)
    ├── code_coverage_line.png                # line coverage report (100%)
    ├── code_coverage_branch.png              # same tests with --branch (99%)
    └── branch_coverage.png                   # branch coverage report (100%)
```

## Submission checklist

- [x] Code coverage analysis with terminal screenshots
- [x] Branch coverage analysis with terminal screenshots
- [x] `CodeCoverageTest_event_ticket_tier.py` (at least 90% line coverage)
- [x] `BranchCoverageTest_event_ticket_tier.py` (at least 90% branch coverage)
- [x] Commit history: one commit for the code coverage tests, one for the branch coverage tests
