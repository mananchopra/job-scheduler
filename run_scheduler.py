#!/usr/bin/env python3
"""
Job Scheduler Runner Script
Run this from the project root directory
"""
import sys
import os
from datetime import datetime, timedelta
import time

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main.job_scheduler_app import JobSchedulerApp
from src.main.config.job_type import JobType

def main():
    print("🚀 Starting Job Scheduler System...")
    
    # Create and start the job scheduler
    app = JobSchedulerApp(num_workers=3)
    app.start()
    
    # Add some example tasks
    print("\n📋 Adding example tasks...")
    app.add_task("Send Welcome Email", JobType.EMAIL, datetime.now() + timedelta(seconds=3))
    app.add_task("Generate Monthly Report", JobType.REPORT, datetime.now() + timedelta(seconds=6))
    app.add_task("Send Push Notification", JobType.NOTIFICATION, datetime.now() + timedelta(seconds=9))
    app.add_task("Export User Data", JobType.DATA_EXPORT, datetime.now() + timedelta(seconds=12))
    
    print("\n⏳ Job Scheduler is running... (Press Ctrl+C to stop)")
    
    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping Job Scheduler...")
        app.stop()
        print("✅ Job Scheduler stopped successfully!")

if __name__ == "__main__":
    main()
