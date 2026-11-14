"""Event ticket helpers: promo vouchers, seat tier prices and attendee badges.

Every function validates its input and returns None for anything it cannot
parse, instead of raising, so bad user input never crashes the program.
"""

TIER_RATES = {
    "VIP": 150.0,
    "PREMIUM": 90.0,
    "GENERAL": 45.0,
}
ROW_PRICE = 2.0
MAX_ROW = 100
MAX_DISCOUNT = 100
MAX_AGE = 120
ADULT_AGE = 18


def _whole_number(text, max_digits):
    """Return text as a non-negative int, or None if it is not plain digits.

    Only ASCII digits are accepted: int() would also accept "+5", "1_0",
    " 7 " and non-Latin digits such as "٣", which are not valid here.
    """
    text = text.strip()
    if not text or len(text) > max_digits:
        return None
    if not (text.isascii() and text.isdigit()):
        return None
    return int(text)


def decode_promo_voucher(voucher_code):
    """Decode a voucher like "EARLY-20" into "Valid EARLY: 20% OFF".

    Returns None if the code is not PREFIX-PERCENT with a letters/digits
    prefix and a whole-number percentage from 0 to 100.
    """
    if not isinstance(voucher_code, str):
        return None
    parts = voucher_code.strip().split("-")
    if len(parts) != 2:
        return None
    prefix = parts[0].strip()
    if not (prefix.isascii() and prefix.isalnum()):
        return None
    percentage = _whole_number(parts[1], max_digits=3)
    if percentage is None or percentage > MAX_DISCOUNT:
        return None
    return f"Valid {prefix.upper()}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    """Price a seat spec like "VIP@4": tier base rate + 2.0 per row.

    Returns None if the tier is unknown or the row is not 1 to 100.
    """
    if not isinstance(tier_spec, str):
        return None
    parts = tier_spec.split("@")
    if len(parts) != 2:
        return None
    tier = parts[0].strip().upper()
    if tier not in TIER_RATES:
        return None
    row = _whole_number(parts[1], max_digits=3)
    if row is None or not 1 <= row <= MAX_ROW:
        return None
    return TIER_RATES[tier] + (row * ROW_PRICE)


def parse_attendee_badge(badge_csv):
    """Format a badge from "Name,Age,Seat" as "Name [Adult] - Seat A12".

    Returns None unless there are exactly three fields, the name and seat
    are non-blank printable text, and the age is a whole number 0 to 120.
    """
    if not isinstance(badge_csv, str):
        return None
    tokens = badge_csv.split(",")
    if len(tokens) != 3:
        return None
    name = tokens[0].strip()
    seat = tokens[2].strip()
    if not (name and seat and name.isprintable() and seat.isprintable()):
        return None
    age = _whole_number(tokens[1], max_digits=3)
    if age is None or age > MAX_AGE:
        return None
    category = "Child" if age < ADULT_AGE else "Adult"
    return f"{name} [{category}] - Seat {seat}"


def main():
    """Ask for one input per function and print the result."""
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    voucher = decode_promo_voucher(v_input)
    if voucher is None:
        print("Invalid voucher: use PREFIX-PERCENT, e.g. EARLY-20 (0-100%)")
    else:
        print("Voucher:", voucher)

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    price = calculate_seat_tier_price(t_input)
    if price is None:
        print("Invalid tier spec: use VIP, PREMIUM or GENERAL @ row 1-100")
    else:
        print("Seat Price: $", price)

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    badge = parse_attendee_badge(b_input)
    if badge is None:
        print("Invalid badge: use Name,Age,Seat with age 0-120")
    else:
        print("Badge:", badge)


if __name__ == "__main__":
    main()
