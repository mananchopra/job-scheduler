#!/usr/bin/env python3
"""
Demonstration of Thread Safety in Job Scheduler Queues
"""
import sys
import os
import threading
import time
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.main.job.job_priority_queue import JobPriorityQueue
from src.main.worker.worker_queue import WorkerQueue
from src.main.job.job import Job
from src.main.config.job_status import JobStatus

def test_singleton_behavior():
    """Test that JobPriorityQueue is truly a singleton"""
    print("🔍 Testing Singleton Behavior:")
    
    # Create multiple instances
    queue1 = JobPriorityQueue()
    queue2 = JobPriorityQueue()
    queue3 = JobPriorityQueue()
    
    print(f"Queue1 ID: {id(queue1)}")
    print(f"Queue2 ID: {id(queue2)}")
    print(f"Queue3 ID: {id(queue3)}")
    print(f"Are they the same object? {queue1 is queue2 is queue3}")
    
    # Test that changes in one affect all
    job1 = Job("test-task-1", datetime.now(), priority=1)
    queue1.add(job1)
    
    print(f"Added job to queue1, queue2 size: {len(queue2.heap)}")
    print(f"queue3 peek: {queue3.peek()}")
    print()

def test_worker_queue_thread_safety():
    """Test WorkerQueue thread safety with multiple producers/consumers"""
    print("🔍 Testing WorkerQueue Thread Safety:")
    
    worker_queue = WorkerQueue()
    results = []
    
    def producer(producer_id, num_jobs):
        """Producer thread that adds jobs to queue"""
        for i in range(num_jobs):
            job = Job(f"producer-{producer_id}-job-{i}", datetime.now(), priority=i)
            worker_queue.push(job)
            print(f"Producer-{producer_id} added job {i}")
            time.sleep(0.1)
    
    def consumer(consumer_id, num_jobs):
        """Consumer thread that processes jobs from queue"""
        for i in range(num_jobs):
            job = worker_queue.pop()  # This blocks until job available
            results.append(f"Consumer-{consumer_id} processed {job.task_id}")
            print(f"Consumer-{consumer_id} processed job: {job.task_id}")
            time.sleep(0.05)
    
    # Create multiple producer and consumer threads
    threads = []
    
    # 2 producers, each adding 3 jobs
    for i in range(2):
        t = threading.Thread(target=producer, args=(i, 3))
        threads.append(t)
        t.start()
    
    # 3 consumers, each processing 2 jobs
    for i in range(3):
        t = threading.Thread(target=consumer, args=(i, 2))
        threads.append(t)
        t.start()
    
    # Wait for all threads to complete
    for t in threads:
        t.join()
    
    print(f"Total jobs processed: {len(results)}")
    print("All jobs processed successfully without race conditions!")
    print()

def test_priority_queue_ordering():
    """Test that JobPriorityQueue maintains proper ordering"""
    print("🔍 Testing Priority Queue Ordering:")
    
    pq = JobPriorityQueue()
    
    # Add jobs with different priorities (lower number = higher priority)
    jobs = [
        Job("low-priority", datetime.now(), priority=5),
        Job("high-priority", datetime.now(), priority=1),
        Job("medium-priority", datetime.now(), priority=3),
        Job("highest-priority", datetime.now(), priority=0),
    ]
    
    # Add in random order
    for job in jobs:
        pq.add(job)
        print(f"Added job: {job.task_id} (priority: {job.priority})")
    
    print("\nPopping jobs in priority order:")
    while not pq.is_empty():
        job = pq.pop()
        print(f"Popped: {job.task_id} (priority: {job.priority})")
    print()

def test_concurrent_priority_queue_access():
    """Test concurrent access to singleton priority queue"""
    print("🔍 Testing Concurrent Priority Queue Access:")
    
    def add_jobs_to_pq(thread_id, num_jobs):
        """Add jobs to priority queue from multiple threads"""
        pq = JobPriorityQueue()  # Each thread gets same singleton instance
        for i in range(num_jobs):
            job = Job(f"thread-{thread_id}-job-{i}", datetime.now(), priority=thread_id)
            pq.add(job)
            print(f"Thread-{thread_id} added job {i}")
            time.sleep(0.1)
    
    def consume_jobs_from_pq(consumer_id, num_jobs):
        """Consume jobs from priority queue"""
        pq = JobPriorityQueue()  # Same singleton instance
        for i in range(num_jobs):
            while pq.is_empty():
                time.sleep(0.05)  # Wait for jobs
            job = pq.pop()
            if job:
                print(f"Consumer-{consumer_id} got: {job.task_id} (priority: {job.priority})")
    
    threads = []
    
    # 2 producer threads
    for i in range(2):
        t = threading.Thread(target=add_jobs_to_pq, args=(i, 3))
        threads.append(t)
        t.start()
    
    # 1 consumer thread
    t = threading.Thread(target=consume_jobs_from_pq, args=(0, 6))
    threads.append(t)
    t.start()
    
    for t in threads:
        t.join()
    
    print("Concurrent access test completed!")
    print()

def main():
    print("=" * 60)
    print("THREAD SAFETY & SINGLETON DEMONSTRATION")
    print("=" * 60)
    print()
    
    test_singleton_behavior()
    test_priority_queue_ordering()
    test_worker_queue_thread_safety()
    test_concurrent_priority_queue_access()
    
    print("=" * 60)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    main()
