#!/usr/bin/env python3
"""Build helper: compile all .slaspec files under a Ghidra processor directory.

Usage:
    sleigh_compile.py <sleighc> <processor-dir> <stamp-file>

Invokes ``sleighc -a <processor-dir>`` which recursively finds every
``.slaspec`` file and compiles it to a ``.sla`` alongside the source.
On success a stamp file is written so Meson can track the dependency.
"""
from __future__ import annotations

import pathlib
import subprocess
import sys


def main() -> int:
    if len(sys.argv) != 4:
        print(
            "usage: sleigh_compile.py <sleighc> <processor-dir> <stamp>",
            file=sys.stderr,
        )
        return 2

    sleighc, proc_dir, stamp_path = sys.argv[1:4]

    proc_path = pathlib.Path(proc_dir)
    if not proc_path.is_dir():
        print(f"processor directory does not exist: {proc_dir}", file=sys.stderr)
        return 1

    result = subprocess.run([sleighc, "-a", proc_dir], check=False)
    if result.returncode != 0:
        return result.returncode

    pathlib.Path(stamp_path).write_text("ok\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
