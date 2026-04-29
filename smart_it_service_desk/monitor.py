

import psutil
from dataclasses import dataclass, field
from logger import logger
from utils import hr

CPU_THRESHOLD_PCT = 90.0
RAM_THRESHOLD_PCT = 95.0
DISK_FREE_MIN_PCT = 10.0


@dataclass
class SystemSnapshot:
    cpu_pct:       float
    ram_pct:       float
    ram_used_gb:   float
    ram_total_gb:  float
    disk_pct:      float
    disk_free_pct: float
    disk_free_gb:  float
    disk_total_gb: float
    net_sent_mb:   float
    net_recv_mb:   float
    alerts:        list = field(default_factory=list)


class Monitor:
    """Monitors system health and raises auto tickets if thresholds exceeded."""

    def __init__(self, disk_path="/"):
        self._disk_path = disk_path

    def capture(self):
        try:
            cpu = psutil.cpu_percent(interval=1)
        except Exception as e:
            logger.error(f"CPU read error: {e}")
            cpu = 0.0

        try:
            vm           = psutil.virtual_memory()
            ram_pct      = vm.percent
            ram_used_gb  = vm.used  / (1024 ** 3)
            ram_total_gb = vm.total / (1024 ** 3)
        except Exception as e:
            logger.error(f"RAM read error: {e}")
            ram_pct = ram_used_gb = ram_total_gb = 0.0

        try:
            disk          = psutil.disk_usage(self._disk_path)
            disk_pct      = disk.percent
            disk_free_pct = 100.0 - disk.percent
            disk_free_gb  = disk.free  / (1024 ** 3)
            disk_total_gb = disk.total / (1024 ** 3)
        except Exception as e:
            logger.error(f"Disk read error: {e}")
            disk_pct = disk_free_pct = disk_free_gb = disk_total_gb = 0.0

        try:
            net          = psutil.net_io_counters()
            net_sent_mb  = net.bytes_sent / (1024 ** 2)
            net_recv_mb  = net.bytes_recv / (1024 ** 2)
        except Exception as e:
            logger.error(f"Network read error: {e}")
            net_sent_mb = net_recv_mb = 0.0

        alerts = []
        if cpu > CPU_THRESHOLD_PCT:
            alerts.append(f"HIGH CPU: {cpu:.1f}% > {CPU_THRESHOLD_PCT}%")
        if ram_pct > RAM_THRESHOLD_PCT:
            alerts.append(f"HIGH RAM: {ram_pct:.1f}% > {RAM_THRESHOLD_PCT}%")
        if disk_free_pct < DISK_FREE_MIN_PCT:
            alerts.append(f"LOW DISK: {disk_free_pct:.1f}% free")

        snap = SystemSnapshot(
            cpu_pct       = cpu,
            ram_pct       = ram_pct,
            ram_used_gb   = ram_used_gb,
            ram_total_gb  = ram_total_gb,
            disk_pct      = disk_pct,
            disk_free_pct = disk_free_pct,
            disk_free_gb  = disk_free_gb,
            disk_total_gb = disk_total_gb,
            net_sent_mb   = net_sent_mb,
            net_recv_mb   = net_recv_mb,
            alerts        = alerts,
        )

        if alerts:
            for a in alerts:
                logger.warning(f"SYSTEM ALERT: {a}")
        else:
            logger.info("System health OK - all metrics within limits.")

        return snap

    def raise_auto_tickets(self, snapshot, ticket_manager):
        created = []
        descriptions = []

        if snapshot.cpu_pct > CPU_THRESHOLD_PCT:
            descriptions.append(
                f"High CPU usage on server: {snapshot.cpu_pct:.1f}%"
            )
        if snapshot.ram_pct > RAM_THRESHOLD_PCT:
            descriptions.append(
                f"High RAM usage: {snapshot.ram_pct:.1f}% "
                f"({snapshot.ram_used_gb:.1f}/{snapshot.ram_total_gb:.1f} GB)"
            )
        if snapshot.disk_free_pct < DISK_FREE_MIN_PCT:
            descriptions.append(
                f"Disk space full: {snapshot.disk_free_pct:.1f}% free only"
            )

        for desc in descriptions:
            t = ticket_manager.create_ticket(
                employee_name     = "System Monitor",
                department        = "IT Operations",
                issue_description = desc,
                force_category    = "Incident",
            )
            created.append(t)
            logger.critical(f"Auto-ticket raised: {t.ticket_id} - {desc}")

        return created

    @staticmethod
    def display(snapshot):
        print(hr())
        print("  SYSTEM HEALTH MONITOR")
        print(hr())
        print(f"  CPU Usage   : {Monitor._bar(snapshot.cpu_pct)}  {snapshot.cpu_pct:.1f}%")
        print(f"  RAM Usage   : {Monitor._bar(snapshot.ram_pct)}  {snapshot.ram_pct:.1f}%  "
              f"({snapshot.ram_used_gb:.1f}/{snapshot.ram_total_gb:.1f} GB)")
        print(f"  Disk Used   : {Monitor._bar(snapshot.disk_pct)}  {snapshot.disk_pct:.1f}%  "
              f"(Free: {snapshot.disk_free_gb:.1f} GB)")
        print(f"  Network     : Sent {snapshot.net_sent_mb:.1f} MB  |  "
              f"Recv {snapshot.net_recv_mb:.1f} MB")
        if snapshot.alerts:
            print()
            for alert in snapshot.alerts:
                print(f"  !! {alert}")
        else:
            print("\n  All systems within normal thresholds.")
        print(hr())

    @staticmethod
    def _bar(pct, width=20):
        filled = int(pct / 100 * width)
        return "[" + "#" * filled + "." * (width - filled) + "]"