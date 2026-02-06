# Python Website Blocker

A simple Python script designed for Linux systems (like Kali Linux) to block a predefined list of websites by modifying the local system's `hosts` file.

## Prerequisites

- **Operating System:** Linux (Kali Linux, Ubuntu, etc.)
- **Python:** Python 3 must be installed.
- **Permissions:** Must be run with `sudo`.

## Installation

1. Clone the repository:
   ````bash
   git clone github.com
   cd porn-blocker   ```
   ````

## Usage 🔧

This repository now includes `webblocker.py`, a safe CLI utility to add and remove a marked block section in a hosts file.

- Block sites (writes markers and creates a backup):

  ```bash
  # Test mode (uses a local file so it won't touch /etc/hosts)
  python3 webblocker.py --block --hosts hosts.test

  # To apply to the real hosts file you must run with sudo
  sudo python3 webblocker.py --block
  ```

- Unblock sites (removes the block section):

  ```bash
  python3 webblocker.py --unblock --hosts hosts.test   # test
  sudo python3 webblocker.py --unblock                 # real hosts (requires sudo)
  ```

- Dry run (show what would change without modifying the file):

  ```bash
  python3 webblocker.py --block --hosts hosts.test --dry-run
  ```

- List currently blocked entries:
  ```bash
  python3 webblocker.py --list --hosts hosts.test
  ```

Notes:

- The script wraps blocked entries between markers `# WEBBLOCKER START` and `# WEBBLOCKER END` for safe removal.
- A backup file named `<hosts-file>.webblocker.bak` is created before modifications by default.
- Always use `--hosts` to test against a local file before touching `/etc/hosts`.

**Security & Safety** ⚠️

- Modifying `/etc/hosts` requires root privileges. Make a backup and verify before running.
- If you want, I can add an `--apply` confirmation prompt to the script before it changes `/etc/hosts`.
