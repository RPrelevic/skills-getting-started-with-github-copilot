@echo off
echo 🧪 Running tests and updating coverage badge...
py scripts\update_coverage_badge.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Badge update completed successfully!
) else (
    echo.
    echo ❌ Badge update failed!
    exit /b 1
)
pause