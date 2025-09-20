from datetime import datetime
from src.main.task.task import Task

class TaskManagement:
    """Centralized task management"""
    def __init__(self):
        self.tasks = {}
    
    def add_task(self, task: Task):
        self.tasks[task.id] = task
    
    def get_task(self, task_id: str):
        return self.tasks.get(task_id)
    
    def get_ready_tasks(self):
        """Get tasks that are ready to be executed"""
        current_time = datetime.now()
        ready_tasks = []
        
        for task in self.tasks.values():
            if task.schedule_time <= current_time:
                ready_tasks.append(task)
        
        return ready_tasks
    
    def remove_task(self, task_id: str):
        if task_id in self.tasks:
            del self.tasks[task_id]
