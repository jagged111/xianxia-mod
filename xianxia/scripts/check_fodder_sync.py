#!/usr/bin/env python3
"""Fail if runtime files changed without updating mapped common/fodder mirrors."""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

MAP_FILE = Path("common/fodder/00_runtime_sync_map.txt")


def changed_files() -> set[str]:
    cmd = ["git", "diff", "--name-only", "--cached"]
    out = subprocess.check_output(cmd, text=True)
    files = {line.strip() for line in out.splitlines() if line.strip()}
    if files:
        return files
    out = subprocess.check_output(["git", "diff", "--name-only"], text=True)
    return {line.strip() for line in out.splitlines() if line.strip()}


def parse_sync_map(text: str) -> list[tuple[list[str], str]]:
    blocks = re.findall(r"\w+\s*=\s*\{([^}]*)\}", text, flags=re.S)
    pairs: list[tuple[list[str], str]] = []
    for block in blocks:
        runtimes = re.findall(r'runtime\s*=\s*"([^"]+)"', block)
        mirrors = re.findall(r'mirror\s*=\s*"([^"]+)"', block)
        if runtimes and mirrors:
            pairs.append((runtimes, mirrors[0]))
    return pairs


def main() -> int:
    if not MAP_FILE.exists():
        print(f"Missing sync map: {MAP_FILE}")
        return 1

    pairs = parse_sync_map(MAP_FILE.read_text())
    files = changed_files()

    violations: list[str] = []
    for runtimes, mirror in pairs:
        runtime_changed = any(path in files for path in runtimes)
        mirror_changed = mirror in files
        if runtime_changed and not mirror_changed:
            violations.append(
                f"Runtime changed without mirror update: {', '.join(runtimes)} -> {mirror}"
            )

    if violations:
        print("Fodder sync violations detected:")
        for violation in violations:
            print(f" - {violation}")
        print("\nUpdate mapped common/fodder mirror files before committing.")
        return 2

    print("Fodder sync check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
