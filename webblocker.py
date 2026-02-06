#!/usr/bin/env python3
"""Simple, safe web blocker CLI for hosts file (block/unblock/test).

Usage examples:
  python3 webblocker.py --block --hosts hosts.test    # write markers & blocked sites to hosts.test
  python3 webblocker.py --unblock --hosts hosts.test  # remove the block section
  python3 webblocker.py --block --dry-run             # show actions without modifying

This script reuses `sites_to_block` and `redirect` if present in `permanent_blocker.py`.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

# Try to import the sites list from existing file to avoid duplication.
try:
    from permanent_blocker import sites_to_block, redirect
except Exception:
    # Fallback short list if import fails
    sites_to_block = ["www.example.com"]
    redirect = "127.0.0.1"

START_MARKER = "# WEBBLOCKER START\n"
END_MARKER = "# WEBBLOCKER END\n"


def backup_hosts(hosts_path: str) -> str:
    bak = hosts_path + ".webblocker.bak"
    shutil.copy(hosts_path, bak)
    print(f"Backup created: {bak}")
    return bak


def add_sites_to_hosts(hosts_path: str, dry_run: bool = False, make_backup: bool = True) -> None:
    print(f"Adding block section to {hosts_path}")
    with open(hosts_path, "r+") as f:
        content = f.read()
        if START_MARKER.strip() in content:
            print("Block section already present; skipping add.")
            return
        if dry_run:
            print("DRY-RUN: Would create backup (if exists) and append block section with the following lines:")
            for s in sites_to_block:
                print(f"{redirect} {s}")
            return
        if make_backup and os.path.exists(hosts_path):
            backup_hosts(hosts_path)
        f.write("\n" + START_MARKER)
        for s in sites_to_block:
            f.write(f"{redirect} {s}\n")
        f.write(END_MARKER)
    print("Block section added.")


def remove_sites_from_hosts(hosts_path: str, dry_run: bool = False, make_backup: bool = True) -> None:
    print(f"Removing block section from {hosts_path}")
    with open(hosts_path, "r") as f:
        lines = f.readlines()
    # Try to remove marked block first
    try:
        start_idx = next(i for i, l in enumerate(lines) if l == START_MARKER)
        end_idx = next(i for i, l in enumerate(lines[start_idx + 1:], start_idx + 1) if l == END_MARKER)
        new_lines = lines[:start_idx] + lines[end_idx + 1:]
        if dry_run:
            print("DRY-RUN: Would remove lines from markers:")
            for l in lines[start_idx:end_idx+1]:
                print(l.rstrip())
            return
        if make_backup and os.path.exists(hosts_path):
            backup_hosts(hosts_path)
        with open(hosts_path, "w") as f:
            f.writelines(new_lines)
        print("Marked block removed.")
        return
    except StopIteration:
        # No marker found: fallback to removing any lines that contain blocked hostnames
        filtered = [l for l in lines if not any(site in l for site in sites_to_block)]
        if dry_run:
            print("DRY-RUN: Would remove lines matching blocked hostnames (fallback):")
            for l in lines:
                if any(site in l for site in sites_to_block):
                    print(l.rstrip())
            return
        if make_backup and os.path.exists(hosts_path):
            backup_hosts(hosts_path)
        with open(hosts_path, "w") as f:
            f.writelines(filtered)
        print("Removed matching host lines (fallback).")


def list_blocked(hosts_path: str) -> None:
    with open(hosts_path, "r") as f:
        content = f.read()
    if START_MARKER.strip() in content:
        start = content.index(START_MARKER)
        end = content.index(END_MARKER, start)
        block = content[start + len(START_MARKER):end].strip()
        print("Currently blocked entries:")
        print(block)
    else:
        print("No block section found in hosts file.")


def main(argv=None):
    p = argparse.ArgumentParser(description="Block/unblock sites in a hosts file safely.")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--block", action="store_true", help="Add block section to hosts file")
    g.add_argument("--unblock", action="store_true", help="Remove block section from hosts file")
    g.add_argument("--list", action="store_true", help="List blocked entries")
    p.add_argument("--hosts", default="/etc/hosts", help="Path to hosts file to edit (default: /etc/hosts)")
    p.add_argument("--dry-run", action="store_true", help="Show changes without modifying files")
    p.add_argument("--no-backup", action="store_true", help="Do not create a backup file before modifying hosts")

    args = p.parse_args(argv)
    hosts_path = args.hosts
    if not os.path.exists(hosts_path):
        print(f"Hosts path does not exist: {hosts_path}")
        sys.exit(2)

    if args.block:
        add_sites_to_hosts(hosts_path, dry_run=args.dry_run, make_backup=(not args.no_backup))
    elif args.unblock:
        remove_sites_from_hosts(hosts_path, dry_run=args.dry_run, make_backup=(not args.no_backup))
    elif args.list:
        list_blocked(hosts_path)
    else:
        p.print_help()


if __name__ == "__main__":
    main()
