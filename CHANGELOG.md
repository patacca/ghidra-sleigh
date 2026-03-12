# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Sleigh compiler integration that builds `.sla` files from Ghidra's `.slaspec` sources at package build time
- Bundled all Ghidra ISA processor specifications (`.sla` runtime data)
- Version and Ghidra metadata derived automatically from the git submodule
- Python package exposing pre-compiled Sleigh data (`ghidra-sleigh`)
- Test suite and linting with `ruff`, `pytest`, and `tox`
- GitHub Actions CI pipeline for lint, format, and test checks

### Fixed
- Sleigh compilation errors for certain processor specifications

[Unreleased]: https://github.com/patacca/ghidra-sleigh/commits/main
