

import sys
from tickets import TicketManager
from monitor import Monitor
from reports import ReportGenerator
from itil    import IncidentManager, ServiceRequestManager, ProblemManager, ChangeManager
from utils   import hr, logger, is_valid_ticket_id
from logger  import log_info, log_warning, log_error


# ── Input helpers ─────────────────────────────────────────────────────────────
def input_str(prompt, allow_empty=False):
    while True:
        try:
            val = input(prompt).strip()
            if not allow_empty and not val:
                print("  Input cannot be empty. Please try again.")
                continue
            return val
        except (EOFError, KeyboardInterrupt):
            print("\n  Returning to menu...")
            return ""

def input_int(prompt, lo, hi):
    while True:
        try:
            raw = input(prompt).strip()
            if raw.lower() in ("q", "back", ""):
                return None
            val = int(raw)
            if lo <= val <= hi:
                return val
            print(f"  Enter a number between {lo} and {hi}.")
        except ValueError:
            print("  Invalid input - please enter a number.")
        except (EOFError, KeyboardInterrupt):
            return None


# ── Menu functions ────────────────────────────────────────────────────────────
def menu_create_ticket(tm):
    print(hr())
    print("  CREATE NEW TICKET")
    print(hr())
    try:
        name  = input_str("  Employee Name    : ")
        dept  = input_str("  Department       : ")
        issue = input_str("  Issue Description: ")
        if not issue:
            print("  Issue description cannot be empty.")
            return
        ticket = tm.create_ticket(name, dept, issue)
        print("\n  Ticket created successfully!")
        ticket.display()

        # Route to correct ITIL manager
        if ticket.category == "Incident":
            IncidentManager().process(ticket)
        else:
            ServiceRequestManager().process(ticket)

    except Exception as e:
        print(f"  Error: {e}")
        log_error(f"Ticket creation error: {e}")


def menu_view_all(tm):
    tickets = tm.view_all()
    if not tickets:
        print("\n  No tickets found.\n")
        return
    print(f"\n  {len(tickets)} Ticket(s):\n")
    for t in tickets:
        sla = " [SLA!]" if t.to_dict().get("sla_breached") else ""
        esc = " [ESC!]" if t.check_escalation() else ""
        print(f"  {t.ticket_id:12}  [{t.priority}]  {t.status:12}"
              f"  {t.employee_name:20}  {t.issue_description[:35]:35}"
              f"{sla}{esc}")
    print()


def menu_search_ticket(tm):
    tid = input_str("  Enter Ticket ID : ").upper()
    if not is_valid_ticket_id(tid):
        print(f"  Invalid ticket ID format. Use TKT-XXXXXX")
        return
    ticket = tm.search_by_id(tid)
    if ticket:
        ticket.display()
    else:
        print(f"  Ticket '{tid}' not found.")
        log_warning(f"Search: ticket not found - {tid}")


def menu_update_status(tm):
    tid = input_str("  Enter Ticket ID : ").upper()
    print("  1=Open  2=In Progress  3=Closed")
    choice = input_int("  Choose status   : ", 1, 3)
    if choice is None:
        return
    status_map = {1: "Open", 2: "In Progress", 3: "Closed"}
    ok = tm.update_status(tid, status_map[choice])
    print("  Updated." if ok else f"  Ticket '{tid}' not found.")


def menu_close_ticket(tm):
    tid = input_str("  Enter Ticket ID to close: ").upper()
    ok = tm.close_ticket(tid)
    print("  Ticket closed." if ok else f"  Ticket '{tid}' not found.")


def menu_delete_ticket(tm):
    tid = input_str("  Enter Ticket ID to delete: ").upper()
    confirm = input_str(f"  Delete {tid}? (yes/no): ").lower()
    if confirm == "yes":
        ok = tm.delete_ticket(tid)
        print("  Deleted." if ok else f"  Ticket '{tid}' not found.")
    else:
        print("  Cancelled.")


def menu_sla_status(tm):
    from utils import minutes_open
    breached    = tm.get_sla_breached()
    escalations = tm.get_escalations()
    print(hr())
    print(f"  SLA BREACHED ({len(breached)}):")
    for t in breached:
        print(f"    * {t.ticket_id}  [{t.priority}]  {t.issue_description[:50]}")
    if not breached:
        print("    None")
    print(f"\n  ESCALATION ALERTS ({len(escalations)}):")
    for t in escalations:
        mins = minutes_open(t.to_dict())
        print(f"    * {t.ticket_id}  [{t.priority}]  "
              f"Open {mins:.0f} min  -  {t.issue_description[:40]}")
    if not escalations:
        print("    None")
    print(hr())


def menu_system_monitor(tm):
    print("\n  Running system health check...")
    mon  = Monitor()
    snap = mon.capture()
    Monitor.display(snap)
    if snap.alerts:
        confirm = input_str("\n  Auto-create tickets for alerts? (yes/no): ").lower()
        if confirm == "yes":
            created = mon.raise_auto_tickets(snap, tm)
            for t in created:
                print(f"  Auto-ticket: {t.ticket_id}  [{t.priority}]")


def menu_reports(tm):
    rg = ReportGenerator(tm.view_all())
    print("\n  1=Daily Summary  2=Monthly Trend  3=SLA Alerts  4=Back")
    choice = input_int("  Choose: ", 1, 4)
    if choice == 1:
        print(rg.daily_summary())
    elif choice == 2:
        print(rg.monthly_trend())
    elif choice == 3:
        print(rg.sla_alert_report())


def menu_backup(tm):
    path = tm.backup_to_csv()
    print(f"  Backup saved to: {path}" if path else "  Backup failed.")


def menu_view_problems(tm):
    ProblemManager().view_all()


def menu_create_change(tm):
    print(hr())
    print("  CREATE CHANGE REQUEST")
    print(hr())
    title  = input_str("  Title       : ")
    desc   = input_str("  Description : ")
    person = input_str("  Requested By: ")
    dept   = input_str("  Department  : ")
    ChangeManager().create_change(title, desc, person, dept)


def menu_view_changes(tm):
    ChangeManager().view_all()


MAIN_MENU = """
  +==================================================+
  |   TechNova IT Service Desk - Main Menu           |
  +==================================================+
  |  1.  Create Ticket                               |
  |  2.  View All Tickets                            |
  |  3.  Search Ticket by ID                         |
  |  4.  Update Ticket Status                        |
  |  5.  Close Ticket                                |
  |  6.  Delete Ticket                               |
  |  ------------------------------------------------|
  |  7.  SLA / Escalation Status                     |
  |  8.  System Health Monitor                       |
  |  ------------------------------------------------|
  |  9.  Reports                                     |
  |  10. Backup Tickets to CSV                       |
  |  ------------------------------------------------|
  |  11. View Problem Records                        |
  |  12. Create Change Request                       |
  |  13. View Change Requests                        |
  |  ------------------------------------------------|
  |  0.  Exit                                        |
  +==================================================+
"""

MENU_ACTIONS = {
    1:  menu_create_ticket,
    2:  menu_view_all,
    3:  menu_search_ticket,
    4:  menu_update_status,
    5:  menu_close_ticket,
    6:  menu_delete_ticket,
    7:  menu_sla_status,
    8:  menu_system_monitor,
    9:  menu_reports,
    10: menu_backup,
    11: menu_view_problems,
    12: menu_create_change,
    13: menu_view_changes,
}


def main():
    print("\n  Smart IT Service Desk - Starting up...")
    log_info("Application started.")

    try:
        tm = TicketManager()
    except Exception as e:
        log_error(f"Startup error: {e}")
        print(f"  Startup error: {e}")
        sys.exit(1)

    breached = tm.get_sla_breached()
    if breached:
        print(f"\n  WARNING: {len(breached)} ticket(s) have breached SLA!\n")

    while True:
        try:
            print(MAIN_MENU)
            choice = input_int("  Enter choice: ", 0, 13)
            if choice is None:
                continue
            if choice == 0:
                tm.backup_to_csv()
                print("\n  Goodbye!\n")
                log_info("Application exited cleanly.")
                break
            action = MENU_ACTIONS.get(choice)
            if action:
                try:
                    action(tm)
                except Exception as e:
                    print(f"\n  Unexpected error: {e}")
                    log_error(f"Menu action {choice} error: {e}", )
        except (KeyboardInterrupt, EOFError):
            print("\n\n  Interrupted. Saving backup...")
            tm.backup_to_csv()
            log_info("Application interrupted.")
            sys.exit(0)


if __name__ == "__main__":
    main()