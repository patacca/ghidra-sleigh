#!/usr/bin/env python3
"""Extract Ghidra version metadata from the git submodule.

Usage:
    python get_ghidra_info.py [version|tag|commit]

Output (one line, no trailing newline):
    version  - PEP 440 version string derived from the tag (e.g. "12.0.3")
    tag      - exact git tag                               (e.g. "Ghidra_12.0.3_build")
    commit   - full commit SHA-1                           (e.g. "09f14c92...")

Falls back gracefully when git is unavailable or the submodule is not
pinned to an exact tag:
    version  -> "0.0.0.dev0"
    tag      -> "unknown"
    commit   -> "unknown"
"""

from __future__ import annotations

import os
import pathlib
import re
import subprocess
import sys

_PROJECT_ROOT = pathlib.Path(__file__).parent.parent
_GHIDRA_DIR = _PROJECT_ROOT / "third_party" / "ghidra"

_FALLBACK_VERSION = "0.0.0.dev0"
_FALLBACK_TAG = "unknown"
_FALLBACK_COMMIT = "unknown"

_TAG_RE = re.compile(r"^Ghidra_(.+)_build$")


def _git(*args: str) -> str:
    try:
        r = subprocess.run(
            ["git", "-C", str(_GHIDRA_DIR), *args],
            capture_output=True,
            text=True,
        )
        return r.stdout.strip() if r.returncode == 0 else ""
    except FileNotFoundError:
        return ""


def get_tag() -> str:
    return _git("describe", "--tags", "--exact-match", "HEAD") or _FALLBACK_TAG


def get_commit() -> str:
    return _git("rev-parse", "HEAD") or _FALLBACK_COMMIT


def get_version(tag: str | None = None) -> str:
    if tag is None:
        tag = get_tag()
    m = _TAG_RE.match(tag)
    version = m.group(1) if m else _FALLBACK_VERSION
    suffix = os.environ.get("GHIDRA_SLEIGH_VERSION_SUFFIX", "")
    return version + suffix


def main() -> None:
    field = sys.argv[1] if len(sys.argv) > 1 else "version"
    if field == "version":
        print(get_version())
    elif field == "tag":
        print(get_tag())
    elif field == "commit":
        print(get_commit())
    else:
        print(f"unknown field: {field!r}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
