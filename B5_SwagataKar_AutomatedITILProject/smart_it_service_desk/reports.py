

from collections import Counter
from datetime import datetime
from utils import logger, hr


class ReportGenerator:
    """Generates daily and monthly reports from ticket data."""

    def __init__(self, tickets):
        self._tickets = tickets

    def daily_summary(self, target_date=None):
        target = (target_date or datetime.now()).date()
        day_tickets = [
            t for t in self._tickets
            if datetime.fromisoformat(t.created_at).date() == target
        ]

        total        = len(day_tickets)
        open_t       = sum(1 for t in day_tickets if t.status == "Open")
        in_prog      = sum(1 for t in day_tickets if t.status == "In Progress")
        closed_t     = sum(1 for t in day_tickets if t.status == "Closed")
        high_prio    = sum(1 for t in day_tickets if t.priority in ("P1", "P2"))
        sla_breached = sum(1 for t in day_tickets
                           if t.to_dict().get("sla_breached"))

        lines = [
            hr("="),
            f"  DAILY SUMMARY REPORT  -  {target.strftime('%d %B %Y')}",
            hr("="),
            f"  Total Tickets Raised  : {total}",
            f"  Open                  : {open_t}",
            f"  In Progress           : {in_prog}",
            f"  Closed                : {closed_t}",
            f"  High Priority (P1/P2) : {high_prio}",
            f"  SLA Breached          : {sla_breached}",
            hr("="),
        ]
        if not day_tickets:
            lines.insert(3, "  No tickets raised today.")

        logger.info(f"Daily summary generated for {target}")
        return "\n".join(lines)

    def monthly_trend(self, year=None, month=None):
        now   = datetime.now()
        year  = year  or now.year
        month = month or now.month

        month_tickets = [
            t for t in self._tickets
            if (d := datetime.fromisoformat(t.created_at)).year == year
            and d.month == month
        ]

        if not month_tickets:
            return f"\n  No tickets for {datetime(year, month, 1).strftime('%B %Y')}.\n"

        issue_counts = Counter(
            self._normalise(t.issue_description) for t in month_tickets
        )
        most_common, most_count = issue_counts.most_common(1)[0]

        resolved = [
            t for t in month_tickets
            if t.status == "Closed" and t.to_dict().get("resolved_at")
        ]
        if resolved:
            durations = [
                (datetime.fromisoformat(t.to_dict()["resolved_at"])
                 - datetime.fromisoformat(t.created_at)).total_seconds() / 3600
                for t in resolved
            ]
            avg_str = f"{sum(durations)/len(durations):.1f} hours"
        else:
            avg_str = "N/A"

        dept_counts      = Counter(t.department for t in month_tickets)
        top_dept, top_count = dept_counts.most_common(1)[0]
        p_counts         = Counter(t.priority for t in month_tickets)

        repeated = [
            issue for issue, cnt in issue_counts.items() if cnt >= 3
        ]

        top_issues = "\n".join(
            f"    {i+1}. {issue[:45]:<45} ({cnt}x)"
            for i, (issue, cnt) in enumerate(issue_counts.most_common(5))
        )

        lines = [
            hr("="),
            f"  MONTHLY TREND REPORT  -  {datetime(year, month, 1).strftime('%B %Y')}",
            hr("="),
            f"  Total Tickets         : {len(month_tickets)}",
            f"  Resolved              : {len(resolved)}",
            f"  Avg Resolution Time   : {avg_str}",
            "",
            f"  Most Common Issue     : {most_common} ({most_count}x)",
            f"  Top Department        : {top_dept} ({top_count} tickets)",
            f"  Repeated Problems     : {', '.join(repeated) if repeated else 'None'}",
            "",
            "  Priority Breakdown:",
            f"    P1-Critical : {p_counts.get('P1', 0)}",
            f"    P2-High     : {p_counts.get('P2', 0)}",
            f"    P3-Medium   : {p_counts.get('P3', 0)}",
            f"    P4-Low      : {p_counts.get('P4', 0)}",
            "",
            "  Top 5 Issues:",
            top_issues,
            hr("="),
        ]

        logger.info(f"Monthly trend generated for {year}-{month:02d}")
        return "\n".join(lines)

    def sla_alert_report(self):
        from utils import is_sla_breached, needs_escalation, minutes_open
        breached   = [t for t in self._tickets
                      if is_sla_breached(t.to_dict()) and t.status != "Closed"]
        escalation = [t for t in self._tickets
                      if needs_escalation(t.to_dict()) and t.status != "Closed"]

        lines = [hr(), "  SLA & ESCALATION ALERT REPORT", hr(),
                 f"  SLA Breached ({len(breached)}):"]
        for t in breached:
            lines.append(f"    * {t.ticket_id}  [{t.priority}]  "
                         f"{t.issue_description[:45]}")
        if not breached:
            lines.append("    None")

        lines += ["", f"  Escalation Needed ({len(escalation)}):"]
        for t in escalation:
            mins = minutes_open(t.to_dict())
            lines.append(f"    * {t.ticket_id}  [{t.priority}]  "
                         f"Open {mins:.0f} min")
        if not escalation:
            lines.append("    None")

        lines.append(hr())
        return "\n".join(lines)

    @staticmethod
    def _normalise(description):
        desc = description.lower()
        for kw in ("printer not working", "laptop slow", "internet down",
                   "outlook not opening", "password reset", "server down",
                   "disk space", "high cpu", "application crash",
                   "problem record"):
            if kw in desc:
                return kw
        return desc[:40]

    @classmethod
    def quick_stats(cls, tickets):
        return {
            "total":       len(tickets),
            "open":        sum(1 for t in tickets if t.status == "Open"),
            "in_progress": sum(1 for t in tickets if t.status == "In Progress"),
            "closed":      sum(1 for t in tickets if t.status == "Closed"),
            "p1":          sum(1 for t in tickets if t.priority == "P1"),
            "p2":          sum(1 for t in tickets if t.priority == "P2"),
        }