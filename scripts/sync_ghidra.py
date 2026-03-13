#!/usr/bin/env python3
"""Check for new Ghidra releases and optionally sync the submodule.

Usage:
    python scripts/sync_ghidra.py                      # show missed releases
    python scripts/sync_ghidra.py Ghidra_12.1.0_build  # sync to specific tag
    python scripts/sync_ghidra.py latest               # sync to latest
"""

from __future__ import annotations

import pathlib
import re
import subprocess
import sys

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
_GHIDRA_DIR = _PROJECT_ROOT / "third_party" / "ghidra"

_TAG_RE = re.compile(r"^Ghidra_(.+)_build$")


def _git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-C", str(_GHIDRA_DIR), *args],
        capture_output=True,
        text=True,
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr.strip() or f"git {args[0]} failed")
    return r.stdout.strip()


def _parse_version(tag: str) -> tuple[int, ...] | None:
    m = _TAG_RE.match(tag)
    if not m:
        return None
    try:
        return tuple(int(x) for x in m.group(1).split("."))
    except ValueError:
        return None


def _format_version(v: tuple[int, ...]) -> str:
    return ".".join(str(x) for x in v)


def main() -> int:
    target_arg = sys.argv[1] if len(sys.argv) > 1 else None

    if not _GHIDRA_DIR.exists():
        print(
            "Submodule not found. Run: git submodule update --init third_party/ghidra",
            file=sys.stderr,
        )
        return 1

    # Current state
    try:
        current_tag = _git("describe", "--tags", "--exact-match", "HEAD")
    except RuntimeError:
        current_tag = None
    current_version = _parse_version(current_tag) if current_tag else None

    print(f"Current: {current_tag or 'not at a tag'}", end="")
    if current_version:
        print(f"  ({_format_version(current_version)})")
    else:
        print()

    # Fetch upstream tags
    print("Fetching upstream tags...")
    _git("fetch", "origin", "--tags")

    # Collect and sort all release tags
    all_tags: list[tuple[tuple[int, ...], str]] = []
    for tag in _git("tag", "-l", "Ghidra_*_build").splitlines():
        v = _parse_version(tag)
        if v:
            all_tags.append((v, tag))
    all_tags.sort()

    if not all_tags:
        print("No Ghidra release tags found.")
        return 1

    latest_version, latest_tag = all_tags[-1]

    # Missed releases
    if current_version:
        missed = [(v, t) for v, t in all_tags if v > current_version]
    else:
        missed = list(all_tags)

    if not missed:
        print("Already at the latest release.")
        if target_arg is None:
            return 0

    if missed:
        print(f"\nNew releases ({len(missed)}):")
        for v, tag in missed:
            marker = "  <- latest" if tag == latest_tag else ""
            print(f"  {tag}  ({_format_version(v)}){marker}")

    # If no target requested, just report
    if target_arg is None:
        return 0

    # Resolve target
    if target_arg == "latest":
        target_tag = latest_tag
    else:
        target_tag = target_arg

    target_version = _parse_version(target_tag)
    if target_version is None:
        tag_list = [t for _, t in all_tags]
        if target_tag not in tag_list:
            print(f"\nError: '{target_tag}' is not a valid Ghidra release tag.")
            return 1

    if current_tag and target_tag == current_tag:
        print(f"\nAlready at {target_tag}, nothing to do.")
        return 0

    # Fetch the target commit objects (handles shallow clones)
    print(f"\nSyncing submodule to {target_tag}...")
    _git("fetch", "origin", "tag", target_tag, "--depth", "1")
    _git("checkout", target_tag)

    tv = _format_version(target_version) if target_version else target_tag
    print(f"Submodule now at {target_tag}")
    print("\nNext steps:")
    print("  git add third_party/ghidra")
    print(f"  git commit -m 'Bump Ghidra to {tv}'")
    print("  git push origin main")
    print(f"  # Create GitHub release for version {tv}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
