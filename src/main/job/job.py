import uuid
from datetime import datetime

from src.main.config.job_status import JobStatus

class Job:

    def __init__(self, 
                 task_id: str,
                 run_time: datetime,
                 priority: int = 0,
                 status: JobStatus = JobStatus.IN_QUEUE
                 ):
        self.id = str(uuid.uuid4())
        self.task_id = task_id
        self.run_time = run_time
        self.priority = priority
        self.status = status
        self.attempt_count = 1
        self.started_at = None
        self.finished_at = None
        self.worker_id = None
        self.created_at = datetime.now()
        self.last_updated_at = datetime.now()

    def job_update(self, status: JobStatus, increaseAttemptCount: bool):
        self.status = status
        self.last_updated_at = datetime.now()
        if increaseAttemptCount:
            self.attempt_count += 1

    def picked_by_worker(self, status: JobStatus, worker_id: str):
        self.status = status
        self.worker_id = worker_id
        self.started_at = datetime.now()
        self.last_updated_at = datetime.now()
    
    def complete_job(self):
        self.status = JobStatus.COMPLETED
        self.finished_at = datetime.now()
        self.last_updated_at = datetime.now()
    
    def fail_job(self):
        self.status = JobStatus.FAILED
        self.finished_at = datetime.now()
        self.last_updated_at = datetime.now()
    
    # Priority queue comparison methods (lower priority number = higher priority)
    def __lt__(self, other):
        if self.priority != other.priority:
            return self.priority < other.priority
        return self.run_time < other.run_time
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other
    
    def __eq__(self, other):
        return (self.priority == other.priority and 
                self.run_time == other.run_time and 
                self.id == other.id)
    
    def __ne__(self, other):
        return not self == other
    
    def __repr__(self):
        return f"Job(id={self.id}, task_id={self.task_id}, priority={self.priority}, run_time={self.run_time}, status={self.status})"