import threading
import time
from src.main.worker.worker_queue import WorkerQueue
from src.main.job.job import Job
from src.main.config.job_status import JobStatus
from src.main.config.job_type import JobType

class Worker(threading.Thread):
    def __init__(self, worker_id: str, worker_queue: WorkerQueue):
        super().__init__()
        self.worker_id = worker_id
        self.worker_queue = worker_queue
        self.daemon = True
        self.running = True

    def run(self):
        """Main worker loop - consumes jobs from worker queue"""
        print(f"[Worker-{self.worker_id}] Started")
        while self.running:
            try:
                # Get job from worker queue (blocking call)
                job = self.worker_queue.pop()
                if job:
                    self._execute_job(job)
            except Exception as e:
                print(f"[Worker-{self.worker_id}] Error: {e}")
                time.sleep(1)
    
    def _execute_job(self, job: Job):
        """Execute a job based on its task type"""
        try:
            # Mark job as in progress
            job.picked_by_worker(JobStatus.IN_PROGRESS, self.worker_id)
            print(f"[Worker-{self.worker_id}] Starting job {job.id} (task: {job.task_id})")
            
            # Simulate job execution based on job type
            # In a real system, this would dispatch to actual job handlers
            execution_time = self._get_execution_time_for_job_type(job)
            time.sleep(execution_time)
            
            # Mark job as completed
            job.complete_job()
            print(f"[Worker-{self.worker_id}] Completed job {job.id}")
            
        except Exception as e:
            # Mark job as failed
            job.fail_job()
            print(f"[Worker-{self.worker_id}] Failed job {job.id}: {e}")
    
    def _get_execution_time_for_job_type(self, job: Job):
        """Simulate different execution times for different job types"""
        # This would be replaced with actual job execution logic
        job_type_times = {
            JobType.EMAIL: 1,
            JobType.NOTIFICATION: 0.5,
            JobType.REPORT: 3,
            JobType.DATA_EXPORT: 5
        }
        return job_type_times.get(job.task_id, 2)  # Default 2 seconds
    
    def stop(self):
        """Stop the worker"""
        self.running = False
        print(f"[Worker-{self.worker_id}] Stopping...")
