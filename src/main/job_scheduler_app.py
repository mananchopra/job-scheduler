from datetime import datetime, timedelta
from src.main.task.task import Task
from src.main.task.task_management import TaskManagement
from src.main.job.job import Job
from src.main.job.job_priority_queue import JobPriorityQueue
from src.main.worker.worker_queue import WorkerQueue
from src.main.worker.scheduler import Scheduler
from src.main.worker.worker import Worker
from src.main.config.job_type import JobType
from src.main.config.job_status import JobStatus
import threading
import time

class JobSchedulerApp:
    def __init__(self, num_workers=3):
        self.task_management = TaskManagement()
        self.job_priority_queue = JobPriorityQueue()
        self.worker_queue = WorkerQueue()
        self.scheduler = Scheduler(self.job_priority_queue, self.worker_queue, self.task_management)
        self.workers = []
        self.num_workers = num_workers
        
    def start(self):
        """Start the job scheduler system"""
        # Start scheduler thread
        self.scheduler.start()
        
        # Start worker threads
        for i in range(self.num_workers):
            worker = Worker(f"worker-{i}", self.worker_queue)
            worker.start()
            self.workers.append(worker)
        
        print(f"Job Scheduler started with {self.num_workers} workers")
    
    def add_task(self, name: str, job_type: str, schedule_time: datetime, **kwargs):
        """Add a new task to the system"""
        task = Task(name, job_type, schedule_time, **kwargs)
        self.task_management.add_task(task)
        print(f"Task '{name}' added with ID: {task.id}")
        return task.id
    
    def stop(self):
        """Stop the job scheduler system"""
        self.scheduler.stop()
        print("Job Scheduler stopped")
