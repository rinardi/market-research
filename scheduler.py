"""
Scheduler - Run analysis and update dashboard automatically
"""

import schedule
import time
import subprocess
import sys
from datetime import datetime
import os

def run_analysis():
    """Run main analysis"""
    print("\n" + "="*60)
    print(f"SCHEDULED ANALYSIS - {datetime.now()}")
    print("="*60)

    try:
        result = subprocess.run(
            [sys.executable, 'main_analysis.py'],
            capture_output=True,
            text=True,
            timeout=600
        )

        if result.returncode == 0:
            print("[OK] Analysis completed successfully")
            return True
        else:
            print(f"[ERROR] Analysis failed:\n{result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("[ERROR] Analysis timeout (10 minutes)")
        return False
    except Exception as e:
        print(f"[ERROR] Analysis error: {e}")
        return False

def update_dashboard():
    """Update HTML dashboard and send notifications"""
    print("\n" + "="*60)
    print(f"UPDATING DASHBOARD - {datetime.now()}")
    print("="*60)

    try:
        result = subprocess.run(
            [sys.executable, 'update_dashboard.py'],
            capture_output=True,
            text=True,
            timeout=120
        )

        if result.returncode == 0:
            print("[OK] Dashboard updated successfully")
            return True
        else:
            print(f"[ERROR] Dashboard update failed:\n{result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("[ERROR] Dashboard update timeout (2 minutes)")
        return False
    except Exception as e:
        print(f"[ERROR] Dashboard update error: {e}")
        return False

def daily_job():
    """Daily job: run analysis and update dashboard"""
    print(f"\n>>> Daily job started at {datetime.now()}")

    # Run analysis
    if run_analysis():
        # Update dashboard after successful analysis
        time.sleep(5)  # Wait for files to be written
        update_dashboard()
    else:
        print("[WARNING] Skipping dashboard update due to analysis failure")

    print(f">>> Daily job completed at {datetime.now()}\n")

def start_scheduler():
    """Start the scheduler"""
    print("\n" + "="*60)
    print("SWING TRADING SCHEDULER STARTED")
    print("="*60)

    # Run immediately on startup (optional)
    run_immediately = input("Run analysis now? (y/n): ").lower() == 'y'
    if run_immediately:
        daily_job()

    # Schedule daily at 09:00 AM
    schedule.every().day.at("09:00").do(daily_job)

    # Backup schedule at 17:00 (5 PM)
    schedule.every().day.at("17:00").do(daily_job)

    print("\nScheduled times:")
    print("  09:00 - Primary analysis run")
    print("  17:00 - Secondary analysis run")
    print("\nPress Ctrl+C to stop scheduler\n")

    # Keep scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n[OK] Scheduler stopped")
        sys.exit(0)

if __name__ == "__main__":
    try:
        start_scheduler()
    except Exception as e:
        print(f"\n[ERROR] Scheduler error: {e}")
        sys.exit(1)
