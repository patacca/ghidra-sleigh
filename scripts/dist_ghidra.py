#!/usr/bin/env python3
"""Meson dist script: populate the sdist with only the needed Ghidra files.

This script is invoked by meson.add_dist_script() after ``meson dist``
populates the tarball directory.  It replaces the full Ghidra submodule
content with the minimal subset required for the build:

  - Ghidra/Features/Decompiler/src/decompile/cpp/  (sleighc C++ sources)
  - Ghidra/Processors/*/data/languages/            (processor spec files)

It also writes a GHIDRA_INFO file so that version detection works when
building from the extracted sdist (where there is no git repo).

Environment variables (set by Meson):
    MESON_DIST_ROOT   - root of the distribution directory
    MESON_SOURCE_ROOT - root of the source tree
"""

from __future__ import annotations

import os
import pathlib
import shutil
import subprocess
import sys


def main() -> int:
    dist_root = pathlib.Path(os.environ["MESON_DIST_ROOT"])
    source_root = pathlib.Path(os.environ["MESON_SOURCE_ROOT"])

    ghidra_src = source_root / "third_party" / "ghidra"
    ghidra_dst = dist_root / "third_party" / "ghidra"

    if not ghidra_src.is_dir():
        print("error: Ghidra submodule not found at", ghidra_src, file=sys.stderr)
        return 1

    # Remove whatever meson dist included for the submodule
    if ghidra_dst.exists():
        shutil.rmtree(ghidra_dst)
    ghidra_dst.mkdir(parents=True)

    # Copy sleighc C++ sources
    cpp_rel = pathlib.PurePosixPath("Ghidra/Features/Decompiler/src/decompile/cpp")
    shutil.copytree(ghidra_src / cpp_rel, ghidra_dst / cpp_rel)

    # Copy processor language data
    processors_src = ghidra_src / "Ghidra" / "Processors"
    processors_dst = ghidra_dst / "Ghidra" / "Processors"
    for proc_dir in sorted(processors_src.iterdir()):
        if not proc_dir.is_dir():
            continue
        lang_src = proc_dir / "data" / "languages"
        if not lang_src.is_dir():
            continue
        lang_dst = processors_dst / proc_dir.name / "data" / "languages"
        shutil.copytree(lang_src, lang_dst)

    # Write GHIDRA_INFO for version detection when building from sdist
    info_script = source_root / "scripts" / "get_ghidra_info.py"
    tag = subprocess.run(
        [sys.executable, str(info_script), "tag"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    commit = subprocess.run(
        [sys.executable, str(info_script), "commit"],
        capture_output=True,
        text=True,
    ).stdout.strip()

    info_file = ghidra_dst / "GHIDRA_INFO"
    info_file.write_text(f"tag={tag}\ncommit={commit}\n")

    file_count = sum(1 for f in ghidra_dst.rglob("*") if f.is_file())
    print(f"dist_ghidra: included {file_count} files in sdist")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
