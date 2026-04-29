

from utils import (
    now_iso, hr, logger,
    load_problems, save_problems,
    load_changes, save_changes,
)



class IncidentManager:
    """Handles outages and failures quickly."""

    def process(self, ticket):
        logger.warning(
            f"INCIDENT MANAGEMENT: {ticket.ticket_id} [{ticket.priority}] "
            f"- {ticket.issue_description[:50]}"
        )
        print(f"\n  [INCIDENT] {ticket.ticket_id} logged.")
        print(f"  Priority : {ticket.priority}")
        print(f"  Action   : Immediate response required.\n")

    @staticmethod
    def get_open_incidents(tickets):
        return [t for t in tickets
                if t.category == "Incident" and t.status != "Closed"]



class ServiceRequestManager:
    """Handles standard requests - password reset, software install."""

    def process(self, ticket):
        logger.info(
            f"SERVICE REQUEST: {ticket.ticket_id} "
            f"- {ticket.issue_description[:50]}"
        )
        print(f"\n  [SERVICE REQUEST] {ticket.ticket_id} logged.")
        print(f"  Priority : {ticket.priority}")
        print(f"  Action   : Scheduled for next available agent.\n")

    @staticmethod
    def get_open_requests(tickets):
        return [t for t in tickets
                if t.category == "Service Request" and t.status != "Closed"]



class ProblemManager:
    """Creates Problem Record when same issue occurs 5 times."""

    def check_and_create(self, issue_key, count, department):
        problems = load_problems()
        existing = next(
            (p for p in problems if p["issue_key"] == issue_key), None
        )
        if existing:
            existing["occurrence_count"] = count
            existing["last_updated"]     = now_iso()
        else:
            problem = {
                "problem_id":       f"PRB-{len(problems)+1:04d}",
                "issue_key":        issue_key,
                "occurrence_count": count,
                "department":       department,
                "status":           "Under Investigation",
                "created_at":       now_iso(),
                "last_updated":     now_iso(),
            }
            problems.append(problem)
            logger.critical(
                f"PROBLEM RECORD: '{issue_key}' occurred {count} times"
            )
            print(f"\n  [PROBLEM MANAGEMENT] Problem Record created!")
            print(f"  Issue  : {issue_key}")
            print(f"  Count  : {count} occurrences\n")

        save_problems(problems)
        return problems

    def view_all(self):
        problems = load_problems()
        if not problems:
            print("\n  No problem records found.\n")
            return
        print(hr())
        print("  PROBLEM RECORDS")
        print(hr())
        for p in problems:
            print(f"  {p['problem_id']}  |  {p['issue_key']:30}  "
                  f"|  {p['occurrence_count']}x  |  {p['status']}")
        print(hr())



class ChangeManager:
    """Tracks updates, patches, and requested changes."""

    def create_change(self, title, description, requested_by, department):
        changes = load_changes()
        change = {
            "change_id":    f"CHG-{len(changes)+1:04d}",
            "title":        title,
            "description":  description,
            "requested_by": requested_by,
            "department":   department,
            "status":       "Pending Approval",
            "created_at":   now_iso(),
        }
        changes.append(change)
        save_changes(changes)
        logger.info(f"Change request created: {change['change_id']} - {title}")
        print(f"\n  [CHANGE MANAGEMENT] {change['change_id']} created!")
        print(f"  Title  : {title}")
        print(f"  Status : Pending Approval\n")
        return change

    def view_all(self):
        changes = load_changes()
        if not changes:
            print("\n  No change requests found.\n")
            return
        print(hr())
        print("  CHANGE REQUESTS")
        print(hr())
        for c in changes:
            print(f"  {c['change_id']}  |  {c['title']:30}  "
                  f"|  {c['requested_by']:15}  |  {c['status']}")
        print(hr())

    def update_status(self, change_id, new_status):
        changes = load_changes()
        for c in changes:
            if c["change_id"] == change_id.upper():
                c["status"] = new_status
                save_changes(changes)
                logger.info(f"Change {change_id} updated to {new_status}")
                print(f"  Change {change_id} updated to: {new_status}")
                return True
        print(f"  Change {change_id} not found.")
        return False