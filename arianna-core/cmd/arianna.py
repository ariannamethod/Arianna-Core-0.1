#!/usr/bin/env python3
"""Unified CLI and system monitor for Arianna Core."""
import argparse
import json
import os
import re
import subprocess
import sys
import time

LOG_DIR = "/arianna_core/log"


def ensure_logdir():
    os.makedirs(LOG_DIR, exist_ok=True)


def mount_device(dev: str, directory: str) -> None:
    dev_pattern = re.compile(r"^/dev/[\w/-]+$")
    dir_pattern = re.compile(r"^/[\w/.-]+$")
    if not dev_pattern.match(dev) or not dir_pattern.match(directory):
        raise ValueError("invalid device or directory format")
    subprocess.run(["mount", dev, directory], check=True)


def start_service(service: str) -> None:
    svc_pattern = re.compile(r"^[\w-]+$")
    if not svc_pattern.match(service):
        raise ValueError("invalid service name")
    subprocess.run(["rc-service", service, "start"], check=True)


def read_cpu() -> tuple[float, float]:
    with open("/proc/stat") as fh:
        parts = [float(x) for x in fh.readline().split()[1:]]
    idle = parts[3]
    total = sum(parts)
    return idle, total


def cpu_percent() -> float | None:
    idle1, total1 = read_cpu()
    time.sleep(0.5)
    idle2, total2 = read_cpu()
    if total2 - total1 == 0:
        return None
    return 100.0 * (1.0 - (idle2 - idle1) / (total2 - total1))


def mem_info() -> dict:
    info: dict[str, int] = {}
    with open("/proc/meminfo") as fh:
        for line in fh:
            key, value = line.split(":")
            info[key] = int(value.strip().split()[0])
    return info


def disk_info(path: str = "/") -> dict:
    stat = os.statvfs(path)
    total = stat.f_frsize * stat.f_blocks
    free = stat.f_frsize * stat.f_bfree
    return {"total": total, "free": free}


def snapshot() -> None:
    ensure_logdir()
    data = {
        "timestamp": int(time.time()),
        "cpu": cpu_percent(),
        "mem": mem_info(),
        "disk": disk_info(),
    }
    with open(os.path.join(LOG_DIR, "health.json"), "w") as fh:
        json.dump(data, fh, indent=2)


def health_loop(interval: int) -> None:
    while True:
        snapshot()
        time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser(description="Arianna Core utility")
    sub = parser.add_subparsers(dest="cmd", required=True)

    mnt = sub.add_parser("mount", help="mount a device")
    mnt.add_argument("device")
    mnt.add_argument("directory")

    svc = sub.add_parser("service", help="start a service")
    svc.add_argument("name")

    health = sub.add_parser("health", help="log health stats")
    health.add_argument("--interval", type=int, default=60)

    args = parser.parse_args()

    try:
        if args.cmd == "mount":
            mount_device(args.device, args.directory)
        elif args.cmd == "service":
            start_service(args.name)
        elif args.cmd == "health":
            health_loop(args.interval)
    except Exception as exc:  # pragma: no cover - logging
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
