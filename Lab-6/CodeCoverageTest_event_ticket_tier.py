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


# Code coverage test cases: each one runs lines not executed yet.
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
