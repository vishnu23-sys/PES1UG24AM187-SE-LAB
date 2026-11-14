# Lab 7: Fuzz Testing with Hypothesis — Event Ticket Tier

Property-based fuzz testing of `processor.py` (promo voucher codes, tiered seat prices and attendee badge CSV strings) using **Hypothesis** and **pytest**, then hardening the code against every input the fuzzer found. The original script and test stub come from the Lab 7 folder of the assigned repo [SETAPESU26/L6_L7_06_event_ticket_tier](https://github.com/SETAPESU26/L6_L7_06_event_ticket_tier).

## Results

| Run                                 | Tests passing | What happened |
| ----------------------------------- | ------------- | ------------- |
| Buggy `processor.py`                | 0 / 6         | 9 crashing inputs and 6 wrong results found |
| Fixed `processor.py`                | 6 / 6         | no crashes, every result in range |

## What the fuzzer found

The three starter tests feed each function any text or `None` and fail if it raises. Three more property tests build almost-valid input (`PREFIX-n`, `tier@row`, `name,age,seat` with random integers and text) to check that the results make sense, not just that nothing crashes.

| Function | Crashes (minimal input) | Wrong results |
| -------- | ----------------------- | ------------- |
| `decode_promo_voucher` | `None`, `''`, `'-'`, `'--1'` | 101% discount accepted; empty prefix accepted |
| `calculate_seat_tier_price` | `None`, `''`, `'@'`, `'balcony@0'` (KeyError) | row 0 and negative rows accepted, giving a price below the tier's base rate |
| `parse_attendee_badge` | `None`, `''`, `','` | age -1 accepted as a Child; blank name and seat accepted |

## How it was fixed

Each function now returns `None` for input it cannot use instead of raising, and `main()` prints the expected format:

- anything that is not a string returns `None`
- `split` must give exactly 2 parts (voucher, tier spec) or 3 (badge) before any index is used
- numbers must be plain ASCII digits (at most 3); `int()` alone would also accept `+5`, `1_0` and non-Latin digits
- ranges are checked: discount 0–100, row 1–100, age 0–120
- the tier is looked up in the rate table before use
- the voucher prefix must be letters/digits, and the badge name and seat must be non-blank

Valid input gives exactly the same output as before (`EARLY-20` → `Valid EARLY: 20% OFF`, `VIP@4` → `158.0`).

## Running it

```bash
pip install hypothesis pytest

python processor.py
python -m pytest test_processor.py
```

## Folder structure

```
Lab-7/
├── processor.py                           # fixed application script
├── test_processor.py                      # completed Hypothesis tests
├── PES1UG24AM187_Lab7_Fuzz_Testing.pdf    # report with all screenshots
├── README.md
└── screenshots/
    ├── 1_buggy_run.png                    # step 2: original program crashing
    ├── 2_tests_failing_summary.png        # step 4: all 6 tests failing
    ├── 3a_failing_voucher_crashes.png     # step 4: falsifying examples (voucher)
    ├── 3b_failing_seat_price.png          # step 4: falsifying examples (seat price)
    ├── 4_fixed_run.png                    # step 5: fixed program
    └── 5_tests_passing.png                # step 6: all 6 tests passing
```

## Submission checklist

- [x] PDF document with the screenshots (`PES1UG24AM187_Lab7_Fuzz_Testing.pdf`)
- [x] Fixed application script (`processor.py`)
- [x] Updated `test_processor.py`
