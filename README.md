# ghidra-sleigh

[![PyPI version](https://img.shields.io/pypi/v/ghidra-sleigh)](https://pypi.org/project/ghidra-sleigh/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Ghidra](https://img.shields.io/badge/Ghidra-12.0.3-green)](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.0.3_build)

**Pre-compiled Sleigh runtime data for the Ghidra decompiler, packaged as a Python library.**

Ghidra's Sleigh language definitions (`.sla` files) are large binary artifacts compiled from
human-readable `.slaspec` sources. This package compiles them once at build time and ships the
results as ordinary Python package data, so that downstream tools — disassemblers, decompilers,
binary analysis frameworks — can load them immediately. No Ghidra installation required, no
build step at runtime, no Java.

The package version **exactly tracks the upstream Ghidra release tag** it was compiled from:
`12.0.3` here means the files were compiled from
[`Ghidra_12.0.3_build`](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.0.3_build).

---

## Why this exists

Projects that need Sleigh data (e.g. a binary lifter or a decompiler library) typically have to
either vendor the entire Ghidra tree or ask users to install Ghidra manually. Both options are
heavy — the raw processor definitions alone are hundreds of megabytes when compiled.

`ghidra-sleigh` solves this by:

- Compiling only the **priority ISAs** (x86, AArch64, RISC-V, MIPS, plus the shared DATA
  processor) that cover the vast majority of real-world binaries.
- Exposing a **simple Python API** — one function call returns the path to the data directory.
- Matching the **directory layout** expected by `SleighArchitecture::scanForSleighDirectories()`,
  so it plugs into any Ghidra-compatible consumer without adaptation.

---

## Upstream pin

| Field | Value |
|-------|-------|
| Ghidra tag | `Ghidra_12.0.3_build` |
| Ghidra commit | `09f14c92d3da6e5d5f6b7dea115409719db3cce1` |
| Commit date | 2026-02-10 |

---

## Bundled processors

| Processor | Architectures covered |
|-----------|----------------------|
| `DATA`    | Shared cspec / pspec definitions used by all processors |
| `x86`     | x86 16-bit, 32-bit, 64-bit (IA-32, x86-64) |
| `AARCH64` | AArch64 / ARM64 (A64 instruction set) |
| `RISCV`   | RISC-V 32-bit and 64-bit |
| `MIPS`    | MIPS 32-bit and 64-bit (big- and little-endian) |

All other Ghidra processors (ARM 32-bit, PowerPC, SPARC, …) can be compiled in by setting the
`all_processors` build option — see [Building from source](#building-from-source).

---

## Installation

```bash
pip install ghidra-sleigh
```

Building from source requires a C++ compiler and zlib. If a pre-built wheel is available for
your platform it will be installed directly with no build step.

---

## Usage

```python
import ghidra_sleigh

# Absolute path to the bundled runtime data directory.
data_dir = ghidra_sleigh.get_runtime_data_dir()
# → /path/to/site-packages/ghidra_sleigh/data

# Upstream Ghidra tag this package was compiled from.
print(ghidra_sleigh.GHIDRA_TAG)     # "Ghidra_12.0.3_build"
print(ghidra_sleigh.GHIDRA_COMMIT)  # "09f14c92d3da6e5d5f6b7dea115409719db3cce1"

# Tuple of processor names whose .sla files are included.
print(ghidra_sleigh.PROCESSORS)     # ("DATA", "x86", "AARCH64", "RISCV", "MIPS")
```

The `data_dir` is structured exactly as `SleighArchitecture::scanForSleighDirectories()` expects:

```
data/
└── Ghidra/
    └── Processors/
        ├── DATA/data/languages/    ← .cspec / .pspec
        ├── x86/data/languages/     ← .sla / .ldefs / .pspec / .cspec
        ├── AARCH64/data/languages/
        ├── RISCV/data/languages/
        └── MIPS/data/languages/
```

Pass `data_dir` as the Sleigh root to any Ghidra-compatible library and it will discover all
bundled language definitions automatically.

---

## Building from source

The build requires:

- Python ≥ 3.13
- Meson ≥ 1.6
- A C++20 compiler (GCC ≥ 11, Clang ≥ 14, or MSVC 2022)
- zlib development headers

```bash
# Clone with the Ghidra submodule (required for the C++ sources)
git clone --recurse-submodules https://github.com/patacca/ghidra-sleigh
cd ghidra-sleigh

pip install --no-build-isolation -e .
```

**Build options:**

| Option | Default | Description |
|--------|---------|-------------|
| `ghidra_root` | `../third_party/ghidra` | Path to the Ghidra source tree |
| `all_processors` | `false` | Compile all 60+ Ghidra processor families instead of only the priority five |

```bash
# Point to an existing Ghidra checkout
pip install --no-build-isolation \
  --config-settings=setup-args="-Dghidra_root=/path/to/ghidra" \
  -e .

# Build with all processors
pip install --no-build-isolation \
  --config-settings=setup-args="-Dall_processors=true" \
  -e .
```

---

## Versioning

Each release of `ghidra-sleigh` is pinned to exactly one Ghidra upstream revision. The package
version mirrors the Ghidra release version directly (e.g. `12.0.3` ↔ `Ghidra_12.0.3_build`),
making the relationship immediately obvious.

---

## Relation to upstream Ghidra

The C++ `sleighc` compiler and all `.slaspec` source files are taken verbatim from the
[Ghidra repository](https://github.com/NationalSecurityAgency/ghidra) at the pinned tag. No
Ghidra code is modified; this project only automates the compilation step and wraps the outputs
in a Python package.

---

## Future plans

- **Automated release pipeline** — GitHub Actions workflow that watches for new Ghidra release
  tags and publishes a matching `ghidra-sleigh` version automatically, keeping the package in
  sync with upstream without manual intervention.

- **Pre-built wheels** — Provide binary wheels for Linux (x86-64, aarch64), macOS (x86-64,
  arm64), and Windows so that `pip install ghidra-sleigh` never needs a C++ compiler.

- **Architecture-specific sub-packages** — Optional extras or separate packages (e.g.
  `ghidra-sleigh[x86]`, `ghidra-sleigh-arm`) for consumers that need only a single ISA,
  reducing install size significantly.

- **Full-processor package** — A `ghidra-sleigh-full` variant that bundles all 60+
  Ghidra-supported processor families for tools that need broad architecture coverage.

- **Custom processor support** — API for loading user-supplied `.slaspec` definitions alongside
  the bundled ones, enabling experimental or proprietary ISA support without forking the package.

---

## License

Apache-2.0 — see [LICENSE](LICENSE).

The bundled compiled data is derived from the Ghidra project, also Apache-2.0.
