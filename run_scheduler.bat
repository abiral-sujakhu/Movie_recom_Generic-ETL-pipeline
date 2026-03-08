@echo off
REM Weekly Report Scheduler - Windows Batch File
REM This file can be added to Windows Task Scheduler for auto-start

cd /d "%~dp0"
echo Starting Weekly Report Scheduler...
echo Press Ctrl+C to stop
echo.

REM Run with console window visible
python scheduler_weekly.py

REM Or run in background without console (uncomment below, comment above)
REM pythonw scheduler_weekly.py

pause
