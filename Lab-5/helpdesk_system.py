"""IT helpdesk ticket allocator: raise, assign, annotate, close and save tickets."""
import itertools
import json
import subprocess
from datetime import datetime

# Global state
tickets = {}
TICKET_IDS = itertools.count(101)
ADMIN_PASSWORD = "helpdesk@123"
HIGH_PRIORITY = 4

def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket for user and return its id."""
    ticket_id = next(TICKET_IDS)
    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": int(urgency),
        "tech": None,
        "notes": [],
    }
    if audit_trail is not None:
        audit_trail.append(f"{user} raised #{ticket_id} at {datetime.now()}")
    return ticket_id

def assign_ticket(ticket_id, technician):
    """Assign a technician to a ticket."""
    tickets[ticket_id]["tech"] = technician

def add_note(ticket_id, note):
    """Attach a note to a ticket."""
    try:
        tickets[ticket_id]["notes"].append(note)
    except KeyError:
        pass

def close_ticket(ticket_id, password):
    """Close (remove) a ticket if the admin password matches."""
    if password == ADMIN_PASSWORD:
        del tickets[ticket_id]

def unresolved_high_priority():
    """Return the ids of high-priority tickets that have no technician yet."""
    result = []
    for ticket_id, ticket in tickets.items():
        if ticket["priority"] >= HIGH_PRIORITY and ticket["tech"] is None:
            result.append(ticket_id)
    return result

def ping_user_machine(hostname):
    """Ping a user's machine once and return the exit code."""
    return subprocess.call("ping -c 1 " + hostname, shell=True)

def save_tickets(file="tickets.json"):
    """Write all open tickets to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(tickets))

def main():
    """Run a short demonstration of the helpdesk workflow."""
    audit_trail = []
    t1 = raise_ticket("anil", "printer", "5", audit_trail)
    raise_ticket("meera", "wifi", "4", audit_trail)
    t3 = raise_ticket("joe", "vpn", "-7", audit_trail)
    assign_ticket(t1, "Tech-Kiran")
    add_note(999, "Called user")
    print("Unassigned high priority:", unresolved_high_priority())
    level = input("Urgency for a new laptop ticket (1-5, Enter for 3): ") or "3"
    raise_ticket("sana", "laptop", level, audit_trail)
    close_ticket(t3, "helpdesk@123")
    save_tickets()
    print("Open tickets:", list(tickets.keys()))

main()
