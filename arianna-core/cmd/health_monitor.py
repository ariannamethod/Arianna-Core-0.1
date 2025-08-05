#!/usr/bin/env python3
"""RU: Мониторинг состояния системы и запись логов."""
import json
import os
import sys
import time

LOG_DIR = "/arianna_core/log"
os.makedirs(LOG_DIR, exist_ok=True)


def read_cpu():
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        parts = [float(x) for x in line.split()[1:]]
        idle = parts[3]
        total = sum(parts)
        return idle, total
    except Exception as exc:  # pragma: no cover - logging
        print(f"Failed to read CPU stats: {exc}", file=sys.stderr)
        return 0.0, 0.0


def cpu_percent():
    idle1, total1 = read_cpu()
    time.sleep(0.5)
    idle2, total2 = read_cpu()
    if total2 - total1 == 0:
        return None
    return 100.0 * (1.0 - (idle2 - idle1) / (total2 - total1))


def mem_info():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            info[k] = int(v.strip().split()[0])
    return info


def disk_info(path="/"):
    try:
        stat = os.statvfs(path)
        total = stat.f_frsize * stat.f_blocks
        free = stat.f_frsize * stat.f_bfree
        return {"total": total, "free": free}
    except Exception as exc:  # pragma: no cover - logging
        print(f"Failed to read disk stats: {exc}", file=sys.stderr)
        return {"total": None, "free": None}


def snapshot():
    data = {
        "timestamp": int(time.time()),
        "cpu": cpu_percent(),
        "mem": mem_info(),
        "disk": disk_info(),
    }
    with open(os.path.join(LOG_DIR, "health.json"), "w") as fh:
        json.dump(data, fh, indent=2)


if __name__ == "__main__":
    while True:
        snapshot()
        time.sleep(60)
