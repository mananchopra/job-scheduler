# 🚀 Multi-Threaded Job Scheduler System

A robust, scalable job scheduling system implemented in Python that demonstrates advanced system design patterns including multi-threading, priority queues, and producer-consumer architecture.

## 📋 Table of Contents

- [Architecture Overview](#-architecture-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [System Components](#-system-components)
- [Threading Model](#-threading-model)
- [Usage Examples](#-usage-examples)
- [Configuration](#-configuration)
- [Thread Safety](#-thread-safety)
- [File Structure](#-file-structure)
- [Development](#-development)
- [Testing](#-testing)

## 🏗️ Architecture Overview

The system follows a clean, multi-layered architecture:

```
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ Task Management │───▶│ Job (w/time) │───▶│ Priority Queue  │
│   (Storage)     │    │  (Execution) │    │   (Ordering)    │
└─────────────────┘    └──────────────┘    └─────────────────┘
                                                     │
                                                     ▼
┌─────────────────┐    ┌──────────────┐    ┌─────────────────┐
│ Worker Thread(s)│◀───│ Worker Queue │◀───│ Scheduler Thread│
│   (Execute)     │    │ (Distribution)│    │  (Orchestrate)  │
└─────────────────┘    └──────────────┘    └─────────────────┘
```

### Core Flow
1. **Tasks** are stored in `TaskManagement` with scheduled execution times
2. **Scheduler Thread** monitors tasks and creates **Jobs** when ready
3. **Jobs** are queued in a **Priority Queue** based on priority and timing
4. **Scheduler** moves ready jobs to the **Worker Queue**
5. **Worker Threads** consume jobs from the queue and execute them concurrently

## ✨ Features

- 🧵 **Multi-threaded Architecture** - Separate scheduler and worker threads
- 🎯 **Priority-based Scheduling** - Jobs executed based on priority and timing
- 🔄 **Recurring Tasks** - Support for repeating jobs with intervals
- 🛡️ **Thread Safety** - Built-in synchronization and singleton patterns
- 📊 **Job Status Tracking** - Complete lifecycle monitoring (IN_QUEUE → IN_PROGRESS → COMPLETED/FAILED)
- ⚙️ **Configurable Workers** - Adjustable number of worker threads
- 🎨 **Multiple Job Types** - EMAIL, NOTIFICATION, REPORT, DATA_EXPORT
- 🔒 **Graceful Shutdown** - Clean termination of all threads
- 📈 **Scalable Design** - Easy to extend and modify

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- No external dependencies required (uses only standard library)

### Installation
```bash
git clone <repository-url>
cd job-scheduler
```

### Running the System

#### Method 1: Using the Runner Script (Recommended)
```bash
python3 run_scheduler.py
```

#### Method 2: Using Python Module Syntax
```bash
python3 -m src.main.app
```

#### Method 3: Using PYTHONPATH
```bash
PYTHONPATH=. python3 src/main/app.py
```

### Expected Output
```
🚀 Starting Job Scheduler System...
[Scheduler] Started
[Worker-worker-0] Started
[Worker-worker-1] Started
[Worker-worker-2] Started
Job Scheduler started with 3 workers

📋 Adding example tasks...
Task 'Send Welcome Email' added with ID: a588b8aa-92d4...
[Scheduler] Created job b49201cb... for task Send Welcome Email
[Worker-worker-0] Starting job b49201cb...
[Worker-worker-0] Completed job b49201cb...
```

## 🔧 System Components

### 1. TaskManagement (`src/main/task/task_management.py`)
- **Purpose**: Centralized task storage and lifecycle management
- **Key Methods**:
  - `add_task(task)` - Store new tasks
  - `get_ready_tasks()` - Retrieve tasks ready for execution
  - `remove_task(task_id)` - Clean up completed tasks

### 2. Job (`src/main/job/job.py`)
- **Purpose**: Individual execution units with priority and timing
- **Key Features**:
  - Priority-based comparison operators
  - Status tracking throughout lifecycle
  - Execution timing and worker assignment

### 3. JobPriorityQueue (`src/main/job/job_priority_queue.py`)
- **Purpose**: Priority-ordered job storage using heapq
- **Key Features**:
  - Singleton pattern ensures single instance
  - Thread-safe operations
  - Automatic priority ordering (lower number = higher priority)

### 4. Scheduler (`src/main/worker/scheduler.py`)
- **Purpose**: Background thread that orchestrates job creation and distribution
- **Key Responsibilities**:
  - Monitor TaskManagement for ready tasks
  - Create Job instances from ready tasks
  - Move ready jobs to WorkerQueue
  - Handle recurring task scheduling

### 5. WorkerQueue (`src/main/worker/worker_queue.py`)
- **Purpose**: Thread-safe job distribution to workers
- **Key Features**:
  - Built on Python's `queue.Queue` for thread safety
  - Blocking operations for efficient worker coordination
  - FIFO job processing

### 6. Worker (`src/main/worker/worker.py`)
- **Purpose**: Background threads that execute jobs
- **Key Features**:
  - Concurrent job execution
  - Job status updates
  - Error handling and reporting
  - Configurable execution logic per job type

## 🧵 Threading Model

### Thread Architecture
```
Main Thread
├── JobSchedulerApp (orchestrator)
│   ├── TaskManagement (shared state)
│   ├── JobPriorityQueue (singleton, thread-safe)
│   ├── WorkerQueue (thread-safe)
│   │
│   ├── Scheduler Thread (daemon) ──┐
│   ├── Worker Thread 0 (daemon) ───┤── All run concurrently
│   ├── Worker Thread 1 (daemon) ───┤
│   └── Worker Thread N (daemon) ───┘
│
└── Main execution loop
```

### Thread Communication
- **Scheduler → Workers**: Via thread-safe WorkerQueue
- **Shared State**: TaskManagement accessed by Scheduler
- **Synchronization**: Built-in Python queue.Queue and singleton pattern
- **Safety**: GIL protection for atomic operations

## 💡 Usage Examples

### Basic Usage
```python
from src.main.job_scheduler_app import JobSchedulerApp
from src.main.config.job_type import JobType
from datetime import datetime, timedelta

# Create and start scheduler
app = JobSchedulerApp(num_workers=5)
app.start()

# Add tasks
app.add_task("Send Email", JobType.EMAIL, datetime.now() + timedelta(seconds=10))
app.add_task("Generate Report", JobType.REPORT, datetime.now() + timedelta(minutes=5))

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    app.stop()
```

### Advanced Task Configuration
```python
from src.main.task.task import Task
from datetime import timedelta

# Recurring task
task = Task(
    name="Daily Backup",
    job_type=JobType.DATA_EXPORT,
    schedule_time=datetime.now(),
    repeat_interval=timedelta(hours=24),
    max_retries=3,
    timeout=300
)
```

## ⚙️ Configuration

### Worker Configuration
```python
# Adjust number of worker threads
app = JobSchedulerApp(num_workers=10)  # Default: 3
```

### Scheduler Configuration
```python
# In scheduler.py, modify check interval
self.check_interval = 0.5  # Check every 500ms (default: 1 second)
```

### Job Types
Available job types in `src/main/config/job_type.py`:
- `JobType.EMAIL` - Email sending tasks
- `JobType.NOTIFICATION` - Push notifications
- `JobType.REPORT` - Report generation
- `JobType.DATA_EXPORT` - Data export operations

## 🔒 Thread Safety

### Mechanisms Used
1. **Singleton Pattern** - Ensures single JobPriorityQueue instance
2. **queue.Queue** - Built-in thread-safe operations for WorkerQueue
3. **Atomic Operations** - heapq operations protected by GIL
4. **Shared Instance Pattern** - All threads access same queue objects

### Verification
Run the thread safety demonstration:
```bash
python3 thread_safety_demo.py
```

This will test:
- Singleton behavior verification
- Concurrent queue access
- Priority ordering under load
- Race condition prevention

## 📁 File Structure

```
job-scheduler/
├── src/
│   └── main/
│       ├── app.py                    # Main entry point
│       ├── job_scheduler_app.py      # Application orchestrator
│       ├── config/
│       │   ├── job_status.py         # Job status enumeration
│       │   ├── job_type.py           # Job type constants
│       │   └── singleton.py          # Singleton decorator
│       ├── job/
│       │   ├── job.py                # Job class with priority support
│       │   └── job_priority_queue.py # Priority queue implementation
│       ├── task/
│       │   ├── task.py               # Task class definition
│       │   └── task_management.py    # Task storage and management
│       └── worker/
│           ├── scheduler.py          # Scheduler thread implementation
│           ├── worker.py             # Worker thread implementation
│           └── worker_queue.py       # Thread-safe worker queue
├── run_scheduler.py                  # Convenient runner script
├── thread_safety_demo.py            # Thread safety demonstration
└── README.md                         # This file
```

## 🛠️ Development

### Adding New Job Types
1. Add new type to `src/main/config/job_type.py`:
```python
class JobType:
    NEW_TYPE = 'NEW_TYPE'
```

2. Update worker execution logic in `src/main/worker/worker.py`:
```python
def _get_execution_time_for_job_type(self, job: Job):
    job_type_times = {
        JobType.NEW_TYPE: 2.5,  # Add execution time
        # ... existing types
    }
```

### Extending Task Properties
Modify `src/main/task/task.py` to add new task attributes:
```python
def __init__(self, name, job_type, schedule_time, custom_property=None, **kwargs):
    self.custom_property = custom_property
    # ... existing initialization
```

### Custom Job Execution Logic
Override the `_execute_job` method in `Worker` class for custom execution:
```python
def _execute_job(self, job: Job):
    # Custom execution logic here
    pass
```

## 🧪 Testing

### Run Thread Safety Tests
```bash
python3 thread_safety_demo.py
```

### Manual Testing
```bash
# Test with different configurations
python3 run_scheduler.py

# Test module import
python3 -m src.main.app

# Test with PYTHONPATH
PYTHONPATH=. python3 src/main/app.py
```

### Test Scenarios Covered
- ✅ Singleton pattern verification
- ✅ Thread-safe queue operations
- ✅ Priority ordering under concurrent access
- ✅ Producer-consumer pattern validation
- ✅ Graceful shutdown handling
- ✅ Job lifecycle management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built using Python's standard library threading and queue modules
- Inspired by enterprise job scheduling systems
- Demonstrates advanced system design patterns and multi-threading concepts

---

**Happy Scheduling! 🎯**

For questions or issues, please open a GitHub issue or contact the maintainers.