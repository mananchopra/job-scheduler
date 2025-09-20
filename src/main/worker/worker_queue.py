import queue

class WorkerQueue:
    def __init__(self):
        self.q = queue.Queue()

    def push(self, job):
        self.q.put(job)
    
    def pop(self):
        return self.q.get()
    
    def is_empty(self):
        return self.q.empty()
    