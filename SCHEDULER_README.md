# Weekly Report Scheduler - Setup Guide

## Overview
Automatically generates movie analysis reports on a weekly schedule. Reports are saved as HTML files in the `reports` folder.

---

## Quick Start

### Step 1: Install Dependencies
```bash
pip install schedule
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Test Report Generation
Before scheduling, verify everything works:
```bash
python test_scheduler.py
```

This will generate test reports in the `reports` folder.

### Step 3: Run the Scheduler

#### Option A: Run in Console (Visible)
```bash
python scheduler_weekly.py
```

#### Option B: Run in Background (Hidden)
```bash
pythonw scheduler_weekly.py
```

#### Option C: Use Batch File
Double-click `run_scheduler.bat` or run:
```bash
run_scheduler.bat
```

---

## Default Schedule

**Every Sunday at 6:00 PM**

The scheduler will:
1. Generate reports for all datasets in `data/processed/` and `data/raw/`
2. Save reports with timestamps to `reports/` folder
3. Clean up reports older than 30 days

---

## Customizing the Schedule

Edit `scheduler_weekly.py` around line 50:

### Examples:

**Every Monday at 9:00 AM:**
```python
schedule.every().monday.at("09:00").do(job_weekly_reports)
```

**Every Friday at 5:00 PM:**
```python
schedule.every().friday.at("17:00").do(job_weekly_reports)
```

**Every 7 days at 6:00 PM:**
```python
schedule.every(7).days.at("18:00").do(job_weekly_reports)
```

**For Testing - Every 2 minutes:**
```python
schedule.every(2).minutes.do(job_weekly_reports)
```

---

## Running as Windows Service

### Method 1: Windows Task Scheduler

1. **Open Task Scheduler** (search in Start menu)
2. **Create Basic Task**
   - Name: "Weekly Movie Reports"
   - Description: "Auto-generate movie analysis reports"
3. **Trigger:** "When I log on"
4. **Action:** "Start a program"
   - Program: Browse to `run_scheduler.bat`
5. **Finish**

### Method 2: Startup Folder

1. Press `Win + R`
2. Type: `shell:startup`
3. Create shortcut to `run_scheduler.bat` in the opened folder

---

## Monitoring

### Check if Scheduler is Running

**PowerShell:**
```powershell
Get-Process python* | Where-Object {$_.CommandLine -like "*scheduler*"}
```

**Command Prompt:**
```cmd
tasklist /fi "imagename eq python.exe" /v
```

### View Generated Reports

Reports are saved in the `reports` folder with timestamps:
```
reports/
├── movies_transformed_report_20260308_180000.html
├── movies_clean_report_20260308_180000.html
└── imdb_top_1000_report_20260308_180000.html
```

---

## Stopping the Scheduler

### If Running in Console:
Press `Ctrl + C`

### If Running in Background:
**PowerShell:**
```powershell
Get-Process pythonw | Stop-Process
```

**Command Prompt:**
```cmd
taskkill /f /im pythonw.exe
```

---

## Troubleshooting

### Problem: "No module named 'schedule'"
**Solution:**
```bash
pip install schedule
```

### Problem: No reports generated
**Solution:**
1. Run test: `python test_scheduler.py`
2. Check data files exist in `data/processed/` or `data/raw/`
3. Check console output for errors

### Problem: Scheduler not running at scheduled time
**Solution:**
1. Verify computer time is correct
2. Don't close the terminal/console window
3. For background operation, use `pythonw scheduler_weekly.py`

### Problem: Import errors
**Solution:**
```bash
pip install -r requirements.txt
```

---

## File Structure

```
project/
├── scheduler_weekly.py          # Main scheduler script
├── test_scheduler.py            # Test script
├── run_scheduler.bat            # Windows batch file
├── src/
│   └── scheduler/
│       ├── __init__.py
│       └── tasks.py             # Report generation tasks
└── reports/                     # Generated reports saved here
```

---

## Advanced Configuration

### Change Report Cleanup Period

Edit `scheduler_weekly.py`, around line 42:
```python
cleanup_old_reports(days_to_keep=30)  # Change 30 to desired days
```

### Add Custom Tasks

Edit `src/scheduler/tasks.py` to add your own scheduled tasks:
```python
def my_custom_task():
    logger.info("Running custom task...")
    # Your code here
```

Then in `scheduler_weekly.py`:
```python
schedule.every().day.at("10:00").do(my_custom_task)
```

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the console output for error messages
3. Test with `python test_scheduler.py` first

---

## Notes

- The scheduler must remain running for scheduled tasks to execute
- Use `pythonw` instead of `python` to run without a console window
- Reports are timestamped to avoid overwriting
- Old reports are automatically cleaned up (30 days by default)
