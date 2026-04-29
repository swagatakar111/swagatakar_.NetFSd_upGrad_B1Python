
import csv
import uuid
from datetime import datetime

from utils import (
    detect_priority, detect_category, is_sla_breached,
    minutes_open, needs_escalation, now_iso,
    load_tickets, save_tickets,
    BACKUP_FILE, SLA_HOURS,
    logger, hr,
    InvalidTicketError, EmptyDescriptionError,
    is_valid_ticket_id,
)


class Ticket:
    """
    Base class for all tickets.
    Encapsulation: data stored in private _data dict, exposed via @property.
    Special methods: __repr__, __str__
    """

    def __init__(self, employee_name, department, issue_description,
                 category=None, priority=None, ticket_id=None,
                 status="Open", created_at=None, resolved_at=None):

        if not issue_description.strip():
            raise EmptyDescriptionError("Issue description cannot be empty.")

        self._data = {
            "ticket_id":         ticket_id or f"TKT-{uuid.uuid4().hex[:6].upper()}",
            "employee_name":     employee_name.strip(),
            "department":        department.strip(),
            "issue_description": issue_description.strip(),
            "priority":          priority or detect_priority(issue_description),
            "category":          category or detect_category(
                                     priority or detect_priority(issue_description)),
            "status":            status,
            "created_at":        created_at or now_iso(),
            "resolved_at":       resolved_at,
            "sla_breached":      False,
        }


    @property
    def ticket_id(self):         return self._data["ticket_id"]
    @property
    def employee_name(self):     return self._data["employee_name"]
    @property
    def department(self):        return self._data["department"]
    @property
    def issue_description(self): return self._data["issue_description"]
    @property
    def priority(self):          return self._data["priority"]
    @property
    def category(self):          return self._data["category"]
    @property
    def status(self):            return self._data["status"]
    @property
    def created_at(self):        return self._data["created_at"]


    def update_status(self, new_status):
        valid = {"Open", "In Progress", "Closed"}
        if new_status not in valid:
            raise ValueError(f"Status must be one of {valid}")
        self._data["status"] = new_status
        if new_status == "Closed":
            self._data["resolved_at"] = now_iso()

    def check_sla(self):
        breached = is_sla_breached(self._data)
        self._data["sla_breached"] = breached
        return breached

    def check_escalation(self):
        return needs_escalation(self._data)

    def to_dict(self):
        return dict(self._data)

    def display(self):
        sla_info = "BREACHED" if self._data["sla_breached"] else "OK"
        print(hr())
        print(f"  Ticket ID  : {self.ticket_id}")
        print(f"  Employee   : {self.employee_name}  |  Dept: {self.department}")
        print(f"  Issue      : {self.issue_description}")
        print(f"  Category   : {self.category}  |  Priority: {self.priority}")
        print(f"  Status     : {self.status}")
        print(f"  Created    : {self.created_at}")
        print(f"  SLA        : {SLA_HOURS[self.priority]}h  [{sla_info}]")
        if self._data.get("resolved_at"):
            print(f"  Resolved   : {self._data['resolved_at']}")
        print(hr())

    
    @classmethod
    def from_dict(cls, d):
        return cls(
            employee_name     = d["employee_name"],
            department        = d["department"],
            issue_description = d["issue_description"],
            category          = d.get("category"),
            priority          = d.get("priority"),
            ticket_id         = d.get("ticket_id"),
            status            = d.get("status", "Open"),
            created_at        = d.get("created_at"),
            resolved_at       = d.get("resolved_at"),
        )

    @staticmethod
    def priority_label(p):
        return {"P1": "CRITICAL", "P2": "HIGH",
                "P3": "MEDIUM",   "P4": "LOW"}.get(p, "UNKNOWN")

    
    def __repr__(self):
        return f"<{self.__class__.__name__} {self.ticket_id} [{self.priority}] {self.status}>"

    def __str__(self):
        return f"{self.ticket_id} | {self.priority} | {self.status} | {self.issue_description[:40]}"



class IncidentTicket(Ticket):
    """P1/P2 issues - outages, failures. Overrides display()."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data["category"] = "Incident"
        if self._data["priority"] not in ("P1", "P2"):
            self._data["priority"] = "P2"

    def display(self):
        print("  [INCIDENT TICKET]")
        super().display()


class ServiceRequest(Ticket):
    """P3/P4 issues - password reset, laptop slow. Overrides display()."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data["category"] = "Service Request"
        if self._data["priority"] in ("P1", "P2"):
            self._data["priority"] = "P3"

    def display(self):
        print("  [SERVICE REQUEST]")
        super().display()


class ProblemRecord(Ticket):
    """Auto-created when same issue repeats 5 times. Overrides display()."""

    def __init__(self, recurring_issue, occurrence_count, **kwargs):
        description = (
            f"[PROBLEM RECORD] Recurring: '{recurring_issue}' "
            f"({occurrence_count} times). Root cause analysis required."
        )
        super().__init__(
            issue_description = description,
            category          = "Problem Management",
            priority          = "P2",
            **kwargs,
        )
        self._data["recurring_issue"]  = recurring_issue
        self._data["occurrence_count"] = occurrence_count
        self._data["category"]         = "Problem Management"

    def display(self):
        print("  [PROBLEM RECORD]")
        super().display()
        print(f"  Recurring  : {self._data['recurring_issue']} "
              f"({self._data['occurrence_count']} times)")
        print(hr())



class TicketManager:
    """Manages full ticket lifecycle - CRUD, SLA, escalation, backup."""

    RECURRENCE_THRESHOLD = 5

    def __init__(self):
        raw = load_tickets()
        self._tickets = [Ticket.from_dict(d) for d in raw]
        logger.info(f"Loaded {len(self._tickets)} ticket(s) from storage.")

    def _persist(self):
        save_tickets([t.to_dict() for t in self._tickets])

    def _find(self, ticket_id):
        tid = ticket_id.upper()
        if not is_valid_ticket_id(tid):
            raise InvalidTicketError(f"Invalid ticket ID format: {tid}")
        return next((t for t in self._tickets if t.ticket_id == tid), None)

    def _refresh_sla(self):
        for t in self._tickets:
            if t.status != "Closed":
                t.check_sla()

    def _normalise_issue(self, description):
        desc = description.lower()
        for keyword in ("printer not working", "laptop slow", "internet down",
                        "outlook not opening", "password reset", "server down",
                        "disk space full", "high cpu", "application crash"):
            if keyword in desc:
                return keyword
        return desc[:40]

    def _check_recurrence(self, description, department):
        issue_key = self._normalise_issue(description)
        count = sum(
            1 for t in self._tickets
            if self._normalise_issue(t.issue_description) == issue_key
            and not isinstance(t, ProblemRecord)
        )
        if count == self.RECURRENCE_THRESHOLD:
            pr = ProblemRecord(
                recurring_issue  = issue_key,
                occurrence_count = count,
                employee_name    = "System",
                department       = department,
            )
            self._tickets.append(pr)
            self._persist()
            logger.critical(
                f"Problem Record auto-created: '{issue_key}' "
                f"occurred {count} times"
            )
            print(f"\n  !! PROBLEM RECORD auto-created: '{issue_key}' "
                  f"(ticket {pr.ticket_id})\n")


    def create_ticket(self, employee_name, department,
                      issue_description, force_category=None):
        if not issue_description.strip():
            raise EmptyDescriptionError("Issue description cannot be empty.")

        priority = detect_priority(issue_description)
        category = force_category or detect_category(priority)

        if category == "Incident" or priority in ("P1", "P2"):
            ticket = IncidentTicket(employee_name, department, issue_description)
        else:
            ticket = ServiceRequest(employee_name, department, issue_description)

        self._tickets.append(ticket)
        self._persist()
        logger.info(f"Ticket created: {ticket.ticket_id} | {ticket.priority} | "
                    f"{ticket.issue_description[:50]}")
        self._check_recurrence(issue_description, department)
        return ticket

    def view_all(self):
        self._refresh_sla()
        return list(self._tickets)

    def search_by_id(self, ticket_id):
        try:
            ticket = self._find(ticket_id)
            if ticket:
                ticket.check_sla()
            return ticket
        except InvalidTicketError as e:
            logger.error(str(e))
            return None

    def update_status(self, ticket_id, new_status):
        try:
            ticket = self._find(ticket_id)
            if not ticket:
                logger.warning(f"Update failed - ticket not found: {ticket_id}")
                return False
            ticket.update_status(new_status)
            self._persist()
            logger.info(f"Ticket {ticket_id} status changed to {new_status}")
            return True
        except InvalidTicketError as e:
            logger.error(str(e))
            return False

    def close_ticket(self, ticket_id):
        return self.update_status(ticket_id, "Closed")

    def delete_ticket(self, ticket_id):
        try:
            ticket = self._find(ticket_id)
            if not ticket:
                logger.warning(f"Delete failed - ticket not found: {ticket_id}")
                return False
            self._tickets.remove(ticket)
            self._persist()
            logger.info(f"Ticket {ticket_id} deleted.")
            return True
        except InvalidTicketError as e:
            logger.error(str(e))
            return False


    def get_sla_breached(self):
        self._refresh_sla()
        breached = [t for t in self._tickets
                    if t.to_dict().get("sla_breached") and t.status != "Closed"]
        for t in breached:
            logger.warning(f"SLA BREACHED: {t.ticket_id} [{t.priority}]")
        return breached

    def get_escalations(self):
        return [t for t in self._tickets
                if t.check_escalation() and t.status != "Closed"]


    def backup_to_csv(self):
        fieldnames = ["ticket_id", "employee_name", "department",
                      "issue_description", "category", "priority",
                      "status", "created_at", "resolved_at", "sla_breached"]
        try:
            with open(BACKUP_FILE, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames,
                                        extrasaction="ignore")
                writer.writeheader()
                for t in self._tickets:
                    writer.writerow(t.to_dict())
            logger.info(f"Backup saved to {BACKUP_FILE}")
            return BACKUP_FILE
        except OSError as e:
            logger.error(f"Backup failed: {e}")
            return ""


    def open_tickets(self):
        return [t for t in self._tickets if t.status != "Closed"]

    def closed_tickets(self):
        return [t for t in self._tickets if t.status == "Closed"]

    def tickets_by_priority(self, p):
        return [t for t in self._tickets if t.priority == p]
    
    def sort_tickets(self, by="priority"):
        order = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}
        if by == "priority":
            self._tickets.sort(key=lambda t: order.get(t.priority, 9))
        elif by == "date":
            self._tickets.sort(key=lambda t: t.created_at)
        return self._tickets