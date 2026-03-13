# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [12.0.4] - 2025-06-09

### Changed
- Bump Ghidra submodule to 12.0.4

### Added
- Sdist support via meson dist script
- Script to check and sync Ghidra submodule releases

## [12.0.3] - 2025-05-15

### Added
- Sleigh compiler integration that builds `.sla` files from Ghidra's `.slaspec` sources at package build time
- Bundled all Ghidra ISA processor specifications (`.sla` runtime data)
- Version and Ghidra metadata derived automatically from the git submodule
- Python package exposing pre-compiled Sleigh data (`ghidra-sleigh`)
- Test suite and linting with `ruff`, `pytest`, and `tox`
- GitHub Actions CI pipeline for lint, format, and test checks
- Platform-independent wheel builds and TestPyPI release support

### Fixed
- Sleigh compilation errors for certain processor specifications

[Unreleased]: https://github.com/patacca/ghidra-sleigh/compare/v12.0.4...HEAD
[12.0.4]: https://github.com/patacca/ghidra-sleigh/compare/v12.0.3...v12.0.4
[12.0.3]: https://github.com/patacca/ghidra-sleigh/commits/v12.0.3
