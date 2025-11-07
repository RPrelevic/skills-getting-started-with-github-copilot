# Scripts Directory

This directory contains automation scripts for the project.

## Files

### `update_coverage_badge.py`
Python script that automatically:
- Runs the test suite with coverage
- Extracts coverage percentage
- Updates the coverage badge in `src/README.md`
- Applies appropriate color coding (green/orange/red)

### `update_badge.bat` (Windows)
Batch script wrapper for Windows systems to run the badge update.
Usage: `scripts\update_badge.bat`

### `update_badge.sh` (Linux/Mac)
Shell script wrapper for Unix-like systems to run the badge update.
Usage: `./scripts/update_badge.sh`

## Usage

From the project root directory:

```bash
# Direct Python execution (recommended)
py scripts/update_coverage_badge.py

# Windows batch script
scripts\update_badge.bat

# Linux/Mac shell script
./scripts/update_badge.sh
```

## Automation

The badge is automatically updated via GitHub Actions on every push/PR. See `.github/workflows/coverage-badge.yml` for the automation configuration.