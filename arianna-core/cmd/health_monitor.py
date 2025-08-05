#!/usr/bin/env python3
"""RU: Мониторинг состояния системы и запись логов."""
import glob
import os
import time
import json
import logging
from datetime import datetime, timedelta

LOG_DIR = "/arianna_core/log"
os.makedirs(LOG_DIR, exist_ok=True)

LOGGER = logging.getLogger("health_monitor")
LOGGER.setLevel(logging.INFO)
_current_handler_date = None


def _get_log_handler():
    """Get a file handler that writes to today's log file."""
    global _current_handler_date
    date_str = datetime.now().strftime("%Y%m%d")
    if _current_handler_date != date_str:
        for h in list(LOGGER.handlers):
            LOGGER.removeHandler(h)
            h.close()
        log_path = os.path.join(LOG_DIR, f"health-{date_str}.json")
        handler = logging.FileHandler(log_path)
        handler.setFormatter(logging.Formatter("%(message)s"))
        LOGGER.addHandler(handler)
        _current_handler_date = date_str


def _cleanup_logs(retention_days: int = 30) -> None:
    """Remove log files older than retention_days."""
    cutoff = datetime.now() - timedelta(days=retention_days)
    pattern = os.path.join(LOG_DIR, "health-*.json")
    for path in glob.glob(pattern):
        try:
            datestr = os.path.basename(path)[7:-5]
            file_date = datetime.strptime(datestr, "%Y%m%d")
        except ValueError:
            continue
        if file_date < cutoff:
            try:
                os.remove(path)
            except OSError:
                pass


def read_cpu():
    with open("/proc/stat") as f:
        line = f.readline()
    parts = [float(x) for x in line.split()[1:]]
    idle = parts[3]
    total = sum(parts)
    return idle, total


def cpu_percent():
    idle1, total1 = read_cpu()
    time.sleep(0.5)
    idle2, total2 = read_cpu()
    return 100.0 * (1.0 - (idle2 - idle1) / (total2 - total1))


def mem_info():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            info[k] = v.strip()
    return info


def disk_info(path="/"):
    stat = os.statvfs(path)
    total = stat.f_frsize * stat.f_blocks
    free = stat.f_frsize * stat.f_bfree
    return {"total": total, "free": free}


def snapshot():
    """Collect system metrics and append them to today's log file."""
    data = {
        "cpu": cpu_percent(),
        "mem": mem_info(),
        "disk": disk_info(),
    }
    _get_log_handler()
    LOGGER.info(json.dumps(data))
    _cleanup_logs()


if __name__ == "__main__":
    while True:
        snapshot()
        time.sleep(60)
