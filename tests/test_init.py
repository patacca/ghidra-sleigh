"""Smoke tests for the ghidra_sleigh public API surface."""

from __future__ import annotations

from pathlib import Path

import ghidra_sleigh


def test_all_exports_exist() -> None:
    for name in ghidra_sleigh.__all__:
        assert hasattr(ghidra_sleigh, name), f"missing export: {name}"


def test_get_runtime_data_dir_is_callable() -> None:
    assert callable(ghidra_sleigh.get_runtime_data_dir)


def test_get_runtime_data_dir_exists_and_contains_ghidra_tree() -> None:
    try:
        data_dir = Path(ghidra_sleigh.get_runtime_data_dir())
    except RuntimeError as exc:
        assert "runtime data directory missing" in str(exc)
        return
    assert data_dir.is_dir()
    assert (data_dir / "Ghidra" / "Processors").is_dir()
