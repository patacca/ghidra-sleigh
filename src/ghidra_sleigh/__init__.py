"""Compiled Sleigh runtime data for the Ghidra decompiler.

This package bundles pre-compiled ``.sla`` files and associated language
definitions (``.ldefs``, ``.pspec``, ``.cspec``) for all 60+ ISAs
supported by the Ghidra decompiler.

Public API
----------
get_runtime_data_dir() -> pathlib.Path
    Return the absolute filesystem path to the runtime data root.

GHIDRA_TAG : str
    The Ghidra release tag these assets were compiled from.

GHIDRA_COMMIT : str
    The upstream commit hash.

PROCESSORS : tuple[str, ...]
    Processor families included in this build.
"""

from __future__ import annotations

import importlib.resources
import pathlib

try:
    from ghidra_sleigh._version import (
        GHIDRA_COMMIT,
        GHIDRA_TAG,
        PROCESSORS,
        __version__,
    )
except ModuleNotFoundError:  # pragma: no cover - build-time generated in releases.
    GHIDRA_COMMIT = "unknown"
    GHIDRA_TAG = "unknown"
    PROCESSORS: tuple[str, ...] = ()
    __version__ = "0.0.0.dev0"

__all__ = [
    "GHIDRA_COMMIT",
    "GHIDRA_TAG",
    "PROCESSORS",
    "__version__",
    "get_runtime_data_dir",
]


def get_runtime_data_dir() -> pathlib.Path:
    """Return the absolute path to the bundled runtime data root.

    The returned directory follows the Ghidra ``Processors/*/data/languages``
    layout so that ``SleighArchitecture::scanForSleighDirectories`` discovers
    all bundled ``.ldefs`` and ``.sla`` files automatically.
    """
    data_path = importlib.resources.files("ghidra_sleigh") / "data"
    # Materialise to a real filesystem path (required by the native layer).
    resolved = pathlib.Path(str(data_path)).resolve()
    if not resolved.is_dir():
        msg = f"ghidra-sleigh runtime data directory missing: {resolved}"
        raise RuntimeError(msg)
    return resolved
