# Smart IT Service Desk & System Monitoring Automation

A Python-based IT helpdesk automation system built for TechNova Solutions.
Replaces manual support processes with automated ticket management,
SLA tracking, system monitoring, and ITIL workflows.

---

## Project Structure

smart_it_service_desk/
├── main.py          # Entry point - main menu
├── tickets.py       # Ticket classes + TicketManager
├── monitor.py       # System health monitoring
├── reports.py       # Daily and monthly reports
├── itil.py          # ITIL workflows
├── utils.py         # Shared helpers and constants
├── logger.py        # Centralised logging
├── requirements.txt # Dependencies
├── data/
│   ├── tickets.json
│   ├── problems.json
│   ├── changes.json
│   ├── logs.txt
│   └── backup.csv
├── screenshots/     # App screenshots
└── README.md

---

## Features

- Ticket Management: Create, View, Search, Update, Close, Delete
- Auto Priority Detection: P1 to P4 based on issue type
- SLA Tracking: Breach detection and escalation alerts
- System Monitoring: CPU, RAM, Disk, Network (via psutil)
- Auto Ticket Creation: When system thresholds exceeded
- ITIL Workflows: Incident, Service Request, Problem, Change Management
- Problem Records: Auto-created when same issue repeats 5 times
- Reports: Daily summary and monthly trend
- Logging: INFO, WARNING, ERROR, CRITICAL levels
- Backup: CSV export of all tickets

---

## Priority Rules

| Issue Type      | Priority |
|----------------|----------|
| Server Down     | P1       |
| Internet Down   | P2       |
| Laptop Slow     | P3       |
| Password Reset  | P4       |

---

## SLA Rules

| Priority | SLA Time |
|----------|----------|
| P1       | 1 Hour   |
| P2       | 4 Hours  |
| P3       | 8 Hours  |
| P4       | 24 Hours |

---

## Setup & Installation

### 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/smart-it-service-desk.git
cd smart-it-service-desk

### 2. Install dependencies
pip install -r requirements.txt

### 3. Run the application
python main.py

---

## Python Concepts Used

- OOP: Classes, Inheritance, Polymorphism, Encapsulation
- File Handling: JSON, CSV, Context Managers
- Exception Handling: try/except/finally, Custom Exceptions
- Advanced Python: Decorators, Generators, Iterators, map/filter/reduce
- Logging: INFO, WARNING, ERROR, CRITICAL
- Regex: Ticket ID validation
- Data Structures: Lists, Tuples, Sets, Dictionaries

---

## ITIL Concepts Implemented

- Incident Management: P1/P2 outages handled immediately
- Service Request Management: P3/P4 requests scheduled
- Problem Management: Auto Problem Record after 5 repeats
- Change Management: Track updates and patches
- SLA Monitoring: Breach detection and escalation

---

## Screenshots

See the screenshots/ folder for full walkthrough.

---

## Author

Swagata Das
Electronics & Communication Engineering Graduate 2025