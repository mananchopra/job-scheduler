from enum import Enum

class JobStatus(Enum): 
    IN_QUEUE = 'IN_QUEUE'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
