import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow


def manifest(tier="general", orders=None, confirmed=True, lounge=False):
    return {
        "is_confirmed": confirmed,
        "tier": tier,
        "exclusive_lounge": lounge,
        "orders": orders if orders is not None else [],
    }


# Example test case:
def test_single_general_order():
    manifests = [
        {
            "is_confirmed": True,
            "tier": "general",
            "exclusive_lounge": False,
            "orders": [{"qty": 2, "promo": ""}]
        }
    ]
    result = process_ticket_manifest(manifests, 0.1)
    assert result["total_revenue"] == 99.0
    assert result["status"] == "COMPLETED"


# Code coverage test cases:
def test_manifests_not_a_list_raises():
    with pytest.raises(ValueError):
        process_ticket_manifest("not a list", 0.1)


def test_unconfirmed_manifest_gives_zero_sales():
    result = process_ticket_manifest(
        [manifest(orders=[{"qty": 2}], confirmed=False)], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_vip_with_exclusive_lounge():
    result = process_ticket_manifest(
        [manifest("vip", [{"qty": 1, "promo": ""}], lounge=True)], 0.0)
    assert result == {"total_revenue": 225.0, "status": "COMPLETED"}


def test_premium_earlybird_discount():
    result = process_ticket_manifest(
        [manifest("premium", [{"qty": 2, "promo": "EARLYBIRD"}])], 0.0)
    assert result["total_revenue"] == pytest.approx(144.0)


def test_bulk_discount_for_five_or_more_seats():
    result = process_ticket_manifest(
        [manifest("general", [{"qty": 5, "promo": ""}])], 0.0)
    assert result["total_revenue"] == pytest.approx(205.0)


def test_vip_fraud_risk_wipes_manifest():
    orders = [{"qty": 2, "promo": ""}, {"qty": 1, "promo": "FRAUD_RISK"}]
    result = process_ticket_manifest([manifest("vip", orders)], 0.1)
    assert result == {"total_revenue": 0.0, "status": "ZERO_SALES"}


def test_too_many_rejections_is_audit_rejected():
    orders = [{"qty": 0}, {"qty": -1}, {"qty": 0}, {"qty": 0},
              {"qty": 2, "promo": ""}]
    result = process_ticket_manifest(
        [manifest("balcony", [{"qty": 1}]), manifest("general", orders)],
        0.1)
    assert result["status"] == "AUDIT_REJECTED"
    assert result["total_revenue"] == pytest.approx(99.0)


def test_gate_flow_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"


def test_gate_flow_overflow():
    assert monitor_gate_flow([[60, 70]]) == "OVERFLOW"


def test_gate_flow_normal_after_streak_reset():
    assert monitor_gate_flow([[60, 10, 70]]) == "FLOW_NORMAL"


# Branch coverage test cases: take each decision the other way too.
def test_non_vip_fraud_risk_is_rejected_but_still_billed():
    # Branch 39->48: FRAUD_RISK on a non-VIP tier counts as a rejection
    # but does not skip the order, so it is still added to the total.
    result = process_ticket_manifest(
        [manifest("premium", [{"qty": 2, "promo": "FRAUD_RISK"}])], 0.0)
    assert result == {"total_revenue": 180.0, "status": "COMPLETED"}


def test_vip_fraud_risk_skips_later_orders_but_keeps_lounge():
    orders = [{"qty": 1, "promo": "FRAUD_RISK"}, {"qty": 2, "promo": ""}]
    result = process_ticket_manifest(
        [manifest("vip", orders, lounge=True)], 0.0)
    assert result == {"total_revenue": 75.0, "status": "COMPLETED"}


# Edge cases:
def test_negative_tax_rate_raises():
    with pytest.raises(ValueError):
        process_ticket_manifest([manifest(orders=[{"qty": 1}])], -0.01)


def test_empty_manifest_list_gives_zero_sales():
    assert process_ticket_manifest([], 0.1) == {
        "total_revenue": 0.0, "status": "ZERO_SALES"}


def test_missing_tier_defaults_to_general():
    result = process_ticket_manifest(
        [{"is_confirmed": True, "orders": [{"qty": 1}]}], 0.0)
    assert result["total_revenue"] == pytest.approx(45.0)


def test_missing_confirmation_is_skipped():
    result = process_ticket_manifest(
        [{"tier": "vip", "orders": [{"qty": 1}]}], 0.0)
    assert result["status"] == "ZERO_SALES"


def test_lounge_only_manifest_without_orders():
    result = process_ticket_manifest([manifest("vip", lounge=True)], 0.0)
    assert result == {"total_revenue": 75.0, "status": "COMPLETED"}


def test_four_seats_get_no_bulk_discount():
    result = process_ticket_manifest(
        [manifest("general", [{"qty": 4, "promo": ""}])], 0.0)
    assert result["total_revenue"] == pytest.approx(180.0)


def test_earlybird_replaces_bulk_discount():
    result = process_ticket_manifest(
        [manifest("general", [{"qty": 5, "promo": "EARLYBIRD"}])], 0.0)
    assert result["total_revenue"] == pytest.approx(180.0)


def test_exactly_four_rejections_is_not_audited():
    orders = [{"qty": 0}] * 4 + [{"qty": 1, "promo": ""}]
    result = process_ticket_manifest([manifest("general", orders)], 0.0)
    assert result == {"total_revenue": 45.0, "status": "COMPLETED"}


def test_audit_checked_before_zero_sales():
    orders = [{"qty": 0}] * 5
    result = process_ticket_manifest([manifest("general", orders)], 0.0)
    assert result == {"total_revenue": 0.0, "status": "AUDIT_REJECTED"}


def test_several_manifests_are_summed_then_taxed():
    manifests = [manifest("general", [{"qty": 2, "promo": ""}]),
                 manifest("premium", [{"qty": 1, "promo": ""}])]
    result = process_ticket_manifest(manifests, 0.18)
    assert result == {"total_revenue": 212.4, "status": "COMPLETED"}


def test_gate_flow_none_is_no_data():
    assert monitor_gate_flow(None) == "NO_DATA"


def test_gate_flow_rate_of_exactly_50_is_not_congested():
    assert monitor_gate_flow([[50, 50, 50]]) == "FLOW_NORMAL"


def test_gate_flow_overflow_in_a_later_stream():
    assert monitor_gate_flow([[10, 20], [55, 60]]) == "OVERFLOW"


def test_gate_flow_streak_does_not_carry_across_streams():
    assert monitor_gate_flow([[10, 60], [60, 10]]) == "FLOW_NORMAL"


def test_gate_flow_empty_stream():
    assert monitor_gate_flow([[]]) == "FLOW_NORMAL"
