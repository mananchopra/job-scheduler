import threading
import time
from datetime import datetime
from src.main.job.job_priority_queue import JobPriorityQueue
from src.main.worker.worker_queue import WorkerQueue
from src.main.job.job import Job
from src.main.config.job_status import JobStatus

class Scheduler(threading.Thread):
    def __init__(self, priority_queue: JobPriorityQueue, worker_queue: WorkerQueue, task_management):
        super().__init__()
        self.priority_queue = priority_queue
        self.worker_queue = worker_queue
        self.task_management = task_management
        self.daemon = True
        self.running = True
        self.check_interval = 1  # Check every second
        
    def run(self):
        """Main scheduler loop - runs in its own thread"""
        print("[Scheduler] Started")
        while self.running:
            try:
                # Check for ready tasks and create jobs
                self._create_jobs_from_ready_tasks()
                
                # Move ready jobs from priority queue to worker queue
                self._move_ready_jobs_to_worker_queue()
                
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"[Scheduler] Error: {e}")
                time.sleep(self.check_interval)
    
    def _create_jobs_from_ready_tasks(self):
        """Create jobs from tasks that are ready to run"""
        ready_tasks = self.task_management.get_ready_tasks()
        current_time = datetime.now()
        
        for task in ready_tasks:
            # Create a job for this task
            job = Job(
                task_id=task.id,
                run_time=task.schedule_time,
                priority=0,  # Default priority, can be enhanced
                status=JobStatus.IN_QUEUE
            )
            
            # Add job to priority queue
            self.priority_queue.add(job)
            print(f"[Scheduler] Created job {job.id} for task {task.name}")
            
            # Handle recurring tasks
            if task.is_recurring():
                task.mark_executed()
                # Update schedule time for next run
                task.schedule_time = task.next_run_time()
            else:
                # Remove non-recurring tasks after creating job
                self.task_management.remove_task(task.id)
    
    def _move_ready_jobs_to_worker_queue(self):
        """Move jobs that are ready to run from priority queue to worker queue"""
        current_time = datetime.now()
        
        # Check jobs in priority queue and move ready ones
        while not self.priority_queue.is_empty():
            job = self.priority_queue.peek()
            
            if job and job.run_time <= current_time:
                # Remove from priority queue and add to worker queue
                job = self.priority_queue.pop()
                self.worker_queue.push(job)
                print(f"[Scheduler] Moved job {job.id} to worker queue")
            else:
                # No more ready jobs
                break
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        print("[Scheduler] Stopping...")
