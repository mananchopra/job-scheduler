import uuid
from datetime import datetime, timedelta
from src.main.config.job_type import JobType


class Task:
    def __init__(self, 
                 name: str, 
                 job_type: JobType, 
                 schedule_time: datetime, 
                 retry_policy: str = "FIXED_DELAY", 
                 max_retries: int = 3, 
                 repeat_interval: timedelta = None, 
                 timeout: int = 60):
        self.id = str(uuid.uuid4())
        self.name = name
        self.job_type = job_type
        self.schedule_time = schedule_time
        self.retry_policy = retry_policy
        self.max_retries = max_retries
        self.repeat_interval = repeat_interval
        self.timeout = timeout
        self.run_count = 0
        self.last_run_time = None
        self.created_at = datetime.now()
        self.last_updated_at = datetime.now()

    def is_recurring(self) -> bool: 
        return self.repeat_interval is not None
    
    def next_run_time(self) -> datetime:
        if not self.is_recurring():
            return None
        if self.last_run_time:
            return self.last_run_time + self.repeat_interval
        else:
            return self.schedule_time
        
    def mark_executed(self):
        self.run_count+=1
        self.last_run_time = datetime.now()


