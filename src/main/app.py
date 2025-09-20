from datetime import datetime, timedelta
from src.main.job_scheduler_app import JobSchedulerApp
from src.main.config.job_type import JobType

import time

if __name__ == "__main__":
    app = JobSchedulerApp()
    app.start()
    
    # Example usage
    app.add_task("Send Welcome Email", JobType.EMAIL, datetime.now() + timedelta(seconds=5))
    app.add_task("Generate Report", JobType.REPORT, datetime.now() + timedelta(seconds=10))
    app.add_task("Send Notification", JobType.NOTIFICATION, datetime.now() + timedelta(seconds=15))
    
    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        app.stop()