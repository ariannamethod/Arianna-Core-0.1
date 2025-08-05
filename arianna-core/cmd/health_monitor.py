#!/usr/bin/env python3
"""RU: Мониторинг состояния системы и запись логов."""
import os
import time
import json

LOG_DIR = "/arianna_core/log"
os.makedirs(LOG_DIR, exist_ok=True)


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
    if total2 == total1:
        return 0.0
    return 100.0 * (1.0 - (idle2 - idle1) / (total2 - total1))


def mem_info():
    info = {}
    with open("/proc/meminfo") as f:
        for line in f:
            k, v = line.split(":")
            parts = v.strip().split()
            value = int(parts[0])
            if len(parts) > 1 and parts[1] == "kB":
                value *= 1024
            info[k] = value
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
        "timestamp": time.time(),
    }
    with open(os.path.join(LOG_DIR, "health.json"), "w") as fh:
        json.dump(data, fh)


if __name__ == "__main__":
    while True:
        snapshot()
        time.sleep(60)
