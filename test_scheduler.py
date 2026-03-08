"""
Test Report Scheduler
---------------------
Run this script to test if report generation works before scheduling.

Usage:
    python test_scheduler.py
"""

from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

from src.scheduler.tasks import test_report_generation

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTING REPORT GENERATION")
    print("="*70)
    print("This will generate test reports to verify everything works.")
    print("Check the 'reports' folder for generated HTML files.")
    print("="*70 + "\n")
    
    success = test_report_generation()
    
    if success:
        print("\n" + "="*70)
        print("✓ TEST PASSED")
        print("="*70)
        print("\nReport generation is working correctly!")
        print("\nYou can now run the scheduler:")
        print("  1. For testing (every 2 minutes):")
        print("     - Edit scheduler_weekly.py")
        print("     - Uncomment line: schedule.every(2).minutes.do(job_weekly_reports)")
        print("     - Run: python scheduler_weekly.py")
        print("\n  2. For production (weekly schedule):")
        print("     - Run: python scheduler_weekly.py")
        print("     - Default: Every Sunday at 6:00 PM")
        print("\n  3. To run in background:")
        print("     - Run: pythonw scheduler_weekly.py")
        print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("✗ TEST FAILED")
        print("="*70)
        print("\nPlease check the errors above and fix them.")
        print("\nCommon issues:")
        print("  - Missing data files in data/processed/ or data/raw/")
        print("  - Import errors (check if src.utils.report exists)")
        print("  - Missing dependencies (run: pip install -r requirements.txt)")
        print("="*70 + "\n")
