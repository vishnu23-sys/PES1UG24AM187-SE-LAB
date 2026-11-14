"""IT helpdesk ticket allocator: raise, assign, annotate, close and save."""
import hmac
import itertools
import json
import os
import platform
import re
import shutil
import subprocess  # nosec B404 - shell-free ping with a validated host only
from datetime import datetime

# Global state
tickets = {}
TICKET_IDS = itertools.count(101)
ADMIN_PASSWORD = os.environ.get("HELPDESK_ADMIN_PASSWORD", "")
MIN_URGENCY = 1
MAX_URGENCY = 5
HIGH_PRIORITY = 4
HOSTNAME_PATTERN = re.compile(
    r"[A-Za-z0-9]([A-Za-z0-9.-]{0,251}[A-Za-z0-9])?"
)


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket for user and return its id.

    urgency must be a whole number from 1 to 5, otherwise ValueError is
    raised and no ticket is created.
    """
    try:
        priority = int(urgency)
    except (TypeError, ValueError):
        raise ValueError(
            f"Urgency must be a whole number, got {urgency!r}"
        ) from None
    if not MIN_URGENCY <= priority <= MAX_URGENCY:
        raise ValueError(
            f"Urgency must be between {MIN_URGENCY} and {MAX_URGENCY}, "
            f"got {priority}"
        )
    ticket_id = next(TICKET_IDS)
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }
    if audit_trail is not None:
        audit_trail.append(f"{user} raised #{ticket_id} at {datetime.now()}")
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign a technician to a ticket; return True if it exists."""
    if ticket_id not in tickets:
        print(f"Ticket #{ticket_id} not found, cannot assign {technician}")
        return False
    tickets[ticket_id]["tech"] = technician
    return True


def add_note(ticket_id, note):
    """Attach a note to a ticket; return True if it exists."""
    if ticket_id not in tickets:
        print(f"Ticket #{ticket_id} not found, note not added")
        return False
    tickets[ticket_id]["notes"].append(note)
    return True


def close_ticket(ticket_id, password):
    """Close (remove) a ticket if the admin password matches.

    Returns True if the ticket was closed.
    """
    if ticket_id not in tickets:
        print(f"Ticket #{ticket_id} not found, nothing to close")
        return False
    if not ADMIN_PASSWORD:
        print("Cannot close tickets: HELPDESK_ADMIN_PASSWORD is not set")
        return False
    supplied = str(password).encode()
    if not hmac.compare_digest(supplied, ADMIN_PASSWORD.encode()):
        print(f"Wrong admin password, ticket #{ticket_id} not closed")
        return False
    del tickets[ticket_id]
    return True


def unresolved_high_priority():
    """Return the ids of high-priority tickets that have no technician yet."""
    result = []
    for ticket_id, ticket in tickets.items():
        if ticket["priority"] >= HIGH_PRIORITY and ticket["tech"] is None:
            result.append(ticket_id)
    return result


def ping_user_machine(hostname):
    """Ping a user's machine once and return the exit code."""
    if not isinstance(hostname, str):
        raise ValueError(f"Invalid hostname: {hostname!r}")
    if not HOSTNAME_PATTERN.fullmatch(hostname):
        raise ValueError(f"Invalid hostname: {hostname!r}")
    ping = shutil.which("ping")
    if ping is None:
        raise FileNotFoundError("ping command not found")
    count_flag = "-n" if platform.system() == "Windows" else "-c"
    # argv list, no shell, and the hostname is validated above
    return subprocess.call([ping, count_flag, "1", hostname])  # nosec B603


def save_tickets(file="tickets.json"):
    """Write all open tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(tickets))


def main():
    """Run a short demonstration of the helpdesk workflow."""
    audit_trail = []
    t1 = raise_ticket("anil", "printer", "5", audit_trail)
    raise_ticket("meera", "wifi", "4", audit_trail)
    try:
        raise_ticket("joe", "vpn", "-7", audit_trail)
    except ValueError as error:
        print("Ticket rejected:", error)
    t3 = raise_ticket("joe", "vpn", "2", audit_trail)
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())
    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ")
    try:
        raise_ticket("sana", "laptop", level.strip() or "3", audit_trail)
    except ValueError as error:
        print("Ticket rejected:", error)
    close_ticket(t3, os.environ.get("HELPDESK_ADMIN_PASSWORD", ""))
    save_tickets()
    print("Open tickets:", list(tickets.keys()))
    print("Audit trail entries:", len(audit_trail))


if __name__ == "__main__":
    main()
