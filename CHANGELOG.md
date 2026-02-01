# Changelog

All notable changes to Lazarus Downloader will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Nothing yet

## [1.0.0] - 2026-02-01

### Added
- Initial release
- GUI-based download interface using PySide6
- Nemo file manager integration via context menu
- Automatic clipboard URL detection
- Smart resume for interrupted downloads using HTTP Range Requests
- SHA256 hash verification upon completion
- "Hot-swap" URL feature to replace expired download links
- Real-time progress tracking with speed and ETA
- Detailed download logs
- Support for partial file detection and continuation
- Bilingual documentation (English and Portuguese)

### Features
- Resilient download mechanism designed for unstable connections
- Automatic detection of partial downloads on restart
- Thread-based downloading to prevent UI freezing
- Support for Anna's Archive and other slow/unstable mirrors
- Command-line interface option

### Installation
- User-local installation (no sudo required)
- Automatic dependency management via pip
- PATH configuration helper

[Unreleased]: https://github.com/dimasgomez/lazarus/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/dimasgomez/lazarus/releases/tag/v1.0.0
