"""Version and upstream pin constants for ghidra-sleigh."""
from __future__ import annotations

__version__ = "12.0.3"

# Must match the pinned upstream baseline in flatline's docs/specs.md S0.
GHIDRA_TAG: str = "Ghidra_12.0.3_build"
GHIDRA_COMMIT: str = "09f14c92d3da6e5d5f6b7dea115409719db3cce1"

# Processor families compiled and shipped in this package.
# Matches ADR-009 priority ISAs plus the shared DATA processor.
PROCESSORS: tuple[str, ...] = ("DATA", "x86", "AARCH64", "RISCV", "MIPS")
