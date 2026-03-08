"""
Weekly Report Scheduler
-----------------------
Automatically generates movie analysis reports on a weekly schedule.

Usage:
    python scheduler_weekly.py

To run in background (no console window):
    pythonw scheduler_weekly.py

To stop:
    Press Ctrl+C in the console window or close the terminal

Schedule:
    Default: Every Sunday at 18:00 (6:00 PM)
    Customize the schedule by modifying the schedule.every() line below
"""

import schedule
import time
from datetime import datetime
from pathlib import Path
import sys

# Add project root to path
project_root = Path(__file__).resolve().parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.scheduler.tasks import generate_weekly_reports, cleanup_old_reports


def job_weekly_reports():
    """Job wrapper for weekly report generation"""
    print(f"\n{'='*70}")
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]")
    print(f"Executing Scheduled Weekly Report Generation")
    print(f"{'='*70}\n")
    
    try:
        # Generate reports
        reports = generate_weekly_reports()
        print(f"\n✓ Successfully generated {len(reports)} report(s)")
        
        # Also cleanup old reports (keeps last 30 days)
        cleanup_old_reports(days_to_keep=30)
        
    except Exception as e:
        print(f"\n✗ Report generation failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    """Main scheduler loop"""
    print("\n" + "="*70)
    print("WEEKLY REPORT SCHEDULER - Movie Analysis Project")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-"*70)
    
    # ========================================================================
    # CONFIGURE YOUR SCHEDULE HERE
    # ========================================================================
    
    # DEFAULT: Every Sunday at 6:00 PM
    # schedule.every().sunday.at("18:00").do(job_weekly_reports)
    
    # ALTERNATIVE SCHEDULES (uncomment to use):
    # -----------------------------------------------------------------------
    # Every Monday at 9:00 AM
    # schedule.every().monday.at("09:00").do(job_weekly_reports)
    
    # Every Friday at 5:00 PM
    # schedule.every().friday.at("17:00").do(job_weekly_reports)
    
    # Every 7 days at 6:00 PM (regardless of day)
    # schedule.every(7).days.at("18:00").do(job_weekly_reports)
    
    # FOR TESTING: Run every 2 minutes (comment this out for production!)
    schedule.every(2).minutes.do(job_weekly_reports)
    
    # FOR TESTING: Run immediately once, then weekly
    # job_weekly_reports()
    # ========================================================================
    
    # Display schedule info
    jobs = schedule.get_jobs()
    print(f"Active Schedule: {len(jobs)} job(s)")
    for job in jobs:
        print(f"  - {job}")
    
    next_run = schedule.next_run()
    if next_run:
        print(f"\nNext scheduled run: {next_run.strftime('%Y-%m-%d %H:%M:%S')}")
    
    print("-"*70)
    print("Scheduler is running. Press Ctrl+C to stop.")
    print("="*70 + "\n")
    
    # Main loop - check every minute for scheduled tasks
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every 60 seconds
    except KeyboardInterrupt:
        print("\n\n" + "="*70)
        print("Scheduler stopped by user")
        print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*70 + "\n")


if __name__ == "__main__":
    main()
