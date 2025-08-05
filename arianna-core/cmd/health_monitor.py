#!/usr/bin/env python3
"""RU: Мониторинг состояния системы и запись логов."""
import os
import time
import json
import logging

LOG_DIR = "/arianna_core/log"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)


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
    data = {
        "cpu": cpu_percent(),
        "mem": mem_info(),
        "disk": disk_info(),
    }
    with open(os.path.join(LOG_DIR, "health.json"), "w") as fh:
        json.dump(data, fh)
        fh.flush()
        os.fsync(fh.fileno())
    logger.debug("Health snapshot written: %s", data)


if __name__ == "__main__":
    while True:
        try:
            snapshot()
        except Exception:  # noqa: BLE001
            logger.exception("Failed to capture health snapshot")
        time.sleep(60)
