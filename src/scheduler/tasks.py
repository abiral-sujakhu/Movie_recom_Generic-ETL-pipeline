"""
Scheduler Tasks Module
----------------------
Contains task functions for scheduled jobs like weekly report generation.
"""

import logging
from datetime import datetime
from pathlib import Path
import sys
import pandas as pd

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.utils.report import generate_html_report


def generate_weekly_reports():
    """
    Generate HTML reports for all available datasets.
    This task runs weekly to create updated analysis reports.
    """
    logger.info("=" * 60)
    logger.info("Starting Weekly Report Generation")
    logger.info("=" * 60)
    
    try:
        # Define paths
        data_dir = project_root / "data" / "processed"
        raw_dir = project_root / "data" / "raw"
        reports_dir = project_root / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        generated_reports = []
        
        # Priority 1: Check for movies_transformed.csv (processed data)
        transformed_file = data_dir / "movies_transformed.csv"
        if transformed_file.exists():
            try:
                logger.info("Processing: Movies Transformed Dataset")
                
                df = pd.read_csv(transformed_file)
                logger.info(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
                
                html_content = generate_html_report(df, "Movies Transformed Dataset")
                
                output_file = reports_dir / f"movies_transformed_report_{timestamp}.html"
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                file_size = output_file.stat().st_size / 1024
                logger.info(f"  ✓ Saved: {output_file.name} ({file_size:.1f} KB)")
                
                generated_reports.append({
                    "name": "Movies Transformed",
                    "file": output_file.name,
                    "size_kb": file_size,
                    "rows": len(df)
                })
            except Exception as e:
                logger.error(f"  ✗ Failed to process movies_transformed.csv: {e}")
        else:
            logger.warning("Movies transformed dataset not found at: " + str(transformed_file))
        
        # Priority 2: Check for datasets in raw folder
        if raw_dir.exists():
            for csv_file in raw_dir.glob("*.csv"):
                try:
                    logger.info(f"Processing: {csv_file.name}")
                    
                    df = pd.read_csv(csv_file)
                    dataset_name = csv_file.stem.replace('_', ' ').title()
                    
                    html_content = generate_html_report(df, dataset_name)
                    
                    output_file = reports_dir / f"{csv_file.stem}_report_{timestamp}.html"
                    with open(output_file, "w", encoding="utf-8") as f:
                        f.write(html_content)
                    
                    file_size = output_file.stat().st_size / 1024
                    logger.info(f"  ✓ Saved: {output_file.name} ({file_size:.1f} KB)")
                    
                    generated_reports.append({
                        "name": dataset_name,
                        "file": output_file.name,
                        "size_kb": file_size,
                        "rows": len(df)
                    })
                except Exception as e:
                    logger.error(f"  ✗ Failed to process {csv_file.name}: {e}")
        
        # Summary
        logger.info("=" * 60)
        logger.info(f"Weekly Report Generation Complete")
        logger.info(f"  Total Reports Generated: {len(generated_reports)}")
        for report in generated_reports:
            logger.info(f"  - {report['name']}: {report['file']} ({report['size_kb']:.1f} KB, {report['rows']} rows)")
        logger.info("=" * 60)
        
        return generated_reports
        
    except Exception as e:
        logger.error(f"Weekly report generation failed: {e}", exc_info=True)
        raise


def cleanup_old_reports(days_to_keep=30):
    """
    Remove report files older than specified days.
    Keeps your reports folder from growing too large.
    
    Args:
        days_to_keep (int): Number of days to keep reports. Default is 30.
    """
    logger.info(f"Cleaning up reports older than {days_to_keep} days...")
    
    try:
        reports_dir = project_root / "reports"
        if not reports_dir.exists():
            logger.info("  No reports directory found")
            return
        
        from datetime import timedelta
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        removed_count = 0
        total_size_kb = 0
        
        for report_file in reports_dir.glob("*.html"):
            file_time = datetime.fromtimestamp(report_file.stat().st_mtime)
            if file_time < cutoff_date:
                file_size = report_file.stat().st_size / 1024
                report_file.unlink()
                removed_count += 1
                total_size_kb += file_size
                logger.info(f"  Removed: {report_file.name} ({file_size:.1f} KB)")
        
        if removed_count > 0:
            logger.info(f"  Cleanup complete: {removed_count} old report(s) removed ({total_size_kb:.1f} KB freed)")
        else:
            logger.info("  No old reports to remove")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")


def test_report_generation():
    """
    Test function to verify report generation works.
    Run this before scheduling to ensure everything is set up correctly.
    """
    logger.info("Testing report generation...")
    try:
        reports = generate_weekly_reports()
        logger.info(f"✓ Test successful! Generated {len(reports)} report(s)")
        return True
    except Exception as e:
        logger.error(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Test the report generation when run directly
    print("\n" + "="*70)
    print("TESTING REPORT GENERATION")
    print("="*70 + "\n")
    
    success = test_report_generation()
    
    if success:
        print("\n" + "="*70)
        print("✓ TEST PASSED")
        print("Report generation is working correctly!")
        print("="*70 + "\n")
    else:
        print("\n" + "="*70)
        print("✗ TEST FAILED")
        print("Please check the errors above and fix before scheduling.")
        print("="*70 + "\n")
