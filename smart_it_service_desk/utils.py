

import json
import os
import re
from datetime import datetime, timedelta
from functools import reduce

from logger import logger

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
DATA_DIR      = os.path.join(BASE_DIR, "data")
TICKET_FILE   = os.path.join(DATA_DIR, "tickets.json")
PROBLEMS_FILE = os.path.join(DATA_DIR, "problems.json")
CHANGES_FILE  = os.path.join(DATA_DIR, "changes.json")
BACKUP_FILE   = os.path.join(DATA_DIR, "backup.csv")
LOG_FILE      = os.path.join(DATA_DIR, "logs.txt")

os.makedirs(DATA_DIR, exist_ok=True)


PRIORITY_MAP = {
    "server down":           "P1",
    "high cpu usage":        "P1",
    "disk space full":       "P1",
    "internet down":         "P2",
    "internet disconnected": "P2",
    "application crash":     "P2",
    "outlook not opening":   "P3",
    "laptop slow":           "P3",
    "laptop running slow":   "P3",
    "printer not working":   "P3",
    "password reset":        "P4",
}

SLA_HOURS          = {"P1": 1,  "P2": 4,   "P3": 8,  "P4": 24}
ESCALATION_MINUTES = {"P1": 30, "P2": 120}
CATEGORY_MAP       = {"P1": "Incident", "P2": "Incident",
                      "P3": "Service Request", "P4": "Service Request"}

# ── File I/O ──────────────────────────────────────────────────────────────────
def load_json(filepath):
    f = None
    try:
        f = open(filepath, "r", encoding="utf-8")
        return json.load(f)
    except FileNotFoundError:
        logger.warning(f"{filepath} not found - starting fresh.")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse {filepath}: {e}")
        return []
    finally:
        if f:
            f.close()
            logger.info(f"File closed: {filepath}")

def save_json(filepath, data):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, default=str)
    except OSError as e:
        logger.error(f"Could not save {filepath}: {e}")

def load_tickets():   return load_json(TICKET_FILE)
def save_tickets(t):  save_json(TICKET_FILE, t)
def load_problems():  return load_json(PROBLEMS_FILE)
def save_problems(p): save_json(PROBLEMS_FILE, p)
def load_changes():   return load_json(CHANGES_FILE)
def save_changes(c):  save_json(CHANGES_FILE, c)

# ── Priority helpers ──────────────────────────────────────────────────────────
def detect_priority(description):
    desc = description.lower()
    for keyword, priority in PRIORITY_MAP.items():
        if keyword in desc:
            return priority
    return "P3"

def detect_category(priority):
    return CATEGORY_MAP.get(priority, "Service Request")

# ── SLA helpers ───────────────────────────────────────────────────────────────
def now_iso():
    return datetime.now().isoformat()

def sla_deadline(created_at, priority):
    return datetime.fromisoformat(created_at) + timedelta(hours=SLA_HOURS.get(priority, 8))

def is_sla_breached(ticket):
    if ticket["status"] == "Closed":
        return False
    return datetime.now() > sla_deadline(ticket["created_at"], ticket["priority"])

def minutes_open(ticket):
    return (datetime.now() - datetime.fromisoformat(ticket["created_at"])).total_seconds() / 60

def needs_escalation(ticket):
    if ticket["status"] == "Closed":
        return False
    limit = ESCALATION_MINUTES.get(ticket["priority"])
    if limit is None:
        return False
    return minutes_open(ticket) >= limit

# ── Display helper ────────────────────────────────────────────────────────────
def hr(char="─", width=60):
    return char * width

# ── Advanced Python ───────────────────────────────────────────────────────────

# Decorator - logs any function call
def log_action(func):
    def wrapper(*args, **kwargs):
        logger.info(f"Started: {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"Finished: {func.__name__}")
        return result
    return wrapper

# Generator - yields tickets one by one
def ticket_generator(tickets):
    for ticket in tickets:
        yield ticket

# Iterator - custom iterator over ticket list
class TicketIterator:
    def __init__(self, tickets):
        self._tickets = tickets
        self._index   = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._tickets):
            raise StopIteration
        ticket = self._tickets[self._index]
        self._index += 1
        return ticket

# map / filter / reduce
def get_high_priority_ids(tickets):
    filtered = filter(lambda t: t["priority"] in ("P1", "P2"), tickets)
    return list(map(lambda t: t["ticket_id"], filtered))

def count_total_tickets(tickets):
    return reduce(lambda acc, _: acc + 1, tickets, 0)

# Regex - validate ticket ID format
def is_valid_ticket_id(ticket_id):
    return bool(re.match(r"^TKT-[A-Z0-9]{6}$", ticket_id.upper()))

# Custom Exception
class InvalidTicketError(Exception):
    pass

class EmptyDescriptionError(Exception):
    pass

# Tuple - fixed priority levels (immutable)
PRIORITY_LEVELS = ("P1", "P2", "P3", "P4")

# Set - unique departments tracker
def get_unique_departments(tickets):
    return {t["department"] for t in tickets}

# ── Append to log (explicit file append example) ──────────────────────────────
def append_to_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} | {message}\n")