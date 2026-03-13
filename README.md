# ghidra-sleigh

[![PyPI version](https://img.shields.io/pypi/v/ghidra-sleigh)](https://pypi.org/project/ghidra-sleigh/)
[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](LICENSE)
[![Ghidra](https://img.shields.io/badge/Ghidra-12.0.4-green)](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.0.4_build)

**Pre-compiled Sleigh runtime data from Ghidra, packaged as a Python library.**

Ghidra's Sleigh language definitions (`.sla` files) are large binary artifacts compiled from
human-readable `.slaspec` sources. This package compiles them once at build time and ships the
results as ordinary Python package data, so that downstream tools — disassemblers, decompilers,
binary analysis frameworks — can load them immediately. No Ghidra installation required, no
build step at runtime, no Java.

The package version **exactly tracks the upstream Ghidra release tag** it was compiled from:
for example, `12.0.3` means the files were compiled from
[`Ghidra_12.0.3_build`](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.0.3_build).

---

## Why this exists

Projects that need Sleigh data — such as [`flatline`](https://github.com/patacca/flatline), a
binary lifter and decompiler — typically have to either vendor the entire Ghidra tree or ask
users to install Ghidra manually. Both options are heavy — the raw processor definitions alone
are tens of megabytes when compiled.

`ghidra-sleigh` solves this by:

- Compiling **all 60+ Ghidra processor families** by default (~26 MB), covering every ISA
  Ghidra supports. A lighter build (~10 MB) with only the major ISAs is available via a
  build option.
- Exposing a **simple Python API** — one function call returns the path to the data directory.
- Matching the **directory layout** expected by `SleighArchitecture::scanForSleighDirectories()`,
  so it plugs into any Ghidra-compatible consumer without adaptation.

---

## Supported versions

| ghidra-sleigh | Ghidra tag | Ghidra commit | ghidra-sleigh commit |
|---------------|------------|---------------|----------------------|
| 12.0.4 | [`Ghidra_12.0.4_build`](https://github.com/NationalSecurityAgency/ghidra/releases/tag/Ghidra_12.0.4_build) | `e40ed13014025f82488b1f8f7bca566894ac376b` | `e1cd442` |

---

## Bundled processors

By default **all 60+ Ghidra processor families** are compiled and included (~26 MB installed).
The most commonly used processors are:

| Processor | Architectures covered |
|-----------|----------------------|
| `DATA`    | Shared cspec / pspec definitions used by all processors |
| `x86`     | x86 16-bit, 32-bit (IA-32), 64-bit (x86-64) |
| `AARCH64` | ARM 64-bit (AArch64 / A64 instruction set) |
| `ARM`     | ARM 32-bit (A32 / Thumb instruction sets) |
| `RISCV`   | RISC-V 32-bit (RV32) and 64-bit (RV64) |
| `MIPS`    | MIPS 32-bit and 64-bit, big- and little-endian |

A lighter build (~10 MB) containing only these major ISAs can be produced by setting
`all_processors` to `false` — see [Building from source](#building-from-source).

---

## Installation

```bash
python -m venv venv
. venv/bin/activate
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
print(ghidra_sleigh.GHIDRA_TAG)     # "Ghidra_12.0.4_build"
print(ghidra_sleigh.GHIDRA_COMMIT)  # "e40ed13014025f82488b1f8f7bca566894ac376b"

# Tuple of processor names whose .sla files are included.
print(ghidra_sleigh.PROCESSORS)     # ("DATA", "x86", "AARCH64", "ARM", "RISCV", "MIPS")
```

The `data_dir` is structured exactly as `SleighArchitecture::scanForSleighDirectories()` expects:

```
data/
└── Ghidra/
    └── Processors/
        ├── DATA/data/languages/    ← .cspec / .pspec
        ├── x86/data/languages/     ← .sla / .ldefs / .pspec / .cspec
        ├── AARCH64/data/languages/
        ├── ARM/data/languages/
        ├── RISCV/data/languages/
        └── MIPS/data/languages/
```

Pass `data_dir` as the Sleigh root to any Ghidra-compatible library and it will discover all
bundled language definitions automatically.

---

## Building from source

The build requires:

- Minimum supported Python version: 3.13+
- Meson ≥ 1.6
- A C++11 compiler.
    - **GCC ≥ 4.8**, **Clang ≥ 3.3**, or **MSVC ≥ 19.0** (Visual Studio 2015).
- zlib development headers

```bash
# Clone with the Ghidra submodule (required for the C++ sources)
git clone --recurse-submodules https://github.com/patacca/ghidra-sleigh
cd ghidra-sleigh

python -m venv venv
. venv/bin/activate
pip install .
```

**Build options:**

| Option | Default | Description |
|--------|---------|-------------|
| `ghidra_root` | `third_party/ghidra` | Path to the Ghidra source tree |
| `all_processors` | `true` | Compile all 60+ Ghidra processor families; set to `false` for a lighter build with only the major ISAs |

```bash
# Point to an existing Ghidra checkout
pip install --config-settings=setup-args="-Dghidra_root=/path/to/ghidra" .

# Build with only the major ISAs (lighter, ~10 MB)
pip install --config-settings=setup-args="-Dall_processors=false" .
```

---

## Development

Install development tooling:

```bash
python -m venv venv
. venv/bin/activate
pip install -e ".[dev]"
```

Run checks via `tox`:

```bash
# Run all environments
tox

# Run one environment
tox -e lint
tox -e format
tox -e py
```

The configured `tox` environments are:

- `lint`: lint checks
- `format`: formatting checks
- `py`: tests (active interpreter)

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

- **Custom processor support** — API for loading user-supplied `.slaspec` definitions alongside
  the bundled ones, enabling experimental or proprietary ISA support without forking the package.

---

## License

Apache-2.0 — see [LICENSE](LICENSE).

The bundled compiled data is derived from the Ghidra project, also Apache-2.0.
