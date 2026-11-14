from hypothesis import given, settings, strategies as st
from processor import decode_promo_voucher, calculate_seat_tier_price, parse_attendee_badge

TIER_RATES = {"VIP": 150.0, "PREMIUM": 90.0, "GENERAL": 45.0}

# Strategies that build almost-valid input, so the fuzzer also reaches the
# logic after the parsing step (negative numbers, huge values, blank fields).
prefixes = st.text(min_size=0, max_size=8)
numbers = st.integers(min_value=-1000, max_value=1000)
tiers = st.sampled_from(["vip", "VIP", " premium ", "General", "balcony", ""])


# ---- 1. Fuzz with any text (or None): the functions must never crash ----

@given(st.text() | st.none())
def test_decode_promo_voucher_no_crash(s):
    try:
        result = decode_promo_voucher(s)
    except Exception as e:
        assert False, f"decode_promo_voucher crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, str)


@given(st.text() | st.none())
def test_calculate_seat_tier_price_safe(s):
    try:
        result = calculate_seat_tier_price(s)
    except Exception as e:
        assert False, f"calculate_seat_tier_price crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, float)


@given(st.text() | st.none())
def test_parse_attendee_badge_safe(s):
    try:
        result = parse_attendee_badge(s)
    except Exception as e:
        assert False, f"parse_attendee_badge crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, str)


# ---- 2. Fuzz with structured input: the results must make sense ----

@given(prefixes, numbers)
def test_voucher_discount_is_a_real_percentage(prefix, pct):
    try:
        result = decode_promo_voucher(f"{prefix}-{pct}")
    except Exception as e:
        assert False, f"decode_promo_voucher crashed on {prefix}-{pct} with: {type(e).__name__}: {e}"
    if result is not None:
        assert 0 <= pct <= 100, f"accepted a {pct}% discount: {result!r}"
        assert prefix.strip(), f"accepted a voucher with no prefix: {result!r}"


@given(tiers, numbers)
def test_seat_price_is_never_below_tier_base(tier, row):
    spec = f"{tier}@{row}"
    try:
        result = calculate_seat_tier_price(spec)
    except Exception as e:
        assert False, f"calculate_seat_tier_price crashed on {spec!r} with: {type(e).__name__}: {e}"
    if result is not None:
        base = TIER_RATES[tier.strip().upper()]
        assert row >= 1, f"accepted row {row} in {spec!r} (price {result})"
        assert result >= base, f"{spec!r} priced at {result}, below the {base} base rate"


@settings(max_examples=200)
@given(st.text(max_size=10), numbers, st.text(max_size=5))
def test_badge_age_and_fields_are_sensible(name, age, seat):
    badge = f"{name},{age},{seat}"
    try:
        result = parse_attendee_badge(badge)
    except Exception as e:
        assert False, f"parse_attendee_badge crashed on {badge!r} with: {type(e).__name__}: {e}"
    if result is not None:
        assert 0 <= age <= 120, f"accepted age {age}: {result!r}"
        assert name.strip() and seat.strip(), f"accepted a blank field: {result!r}"
        assert ("[Child]" in result) == (age < 18)
