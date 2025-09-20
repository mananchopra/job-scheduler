import heapq
from src.main.config.singleton import singleton
from src.main.job.job import Job

@singleton
class JobPriorityQueue:

    def __init__(self):
        self.heap = []

    def add (self, job: Job):
        heapq.heappush(self.heap, job)
    
    def pop(self):
        return heapq.heappop(self.heap) if self.heap else None
    
    def peek(self):
        return self.heap[0] if self.heap else None
    
    def is_empty(self):
        return len(self.heap) == 0