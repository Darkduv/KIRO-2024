"""Default, empty solver implementation."""

from model import *
from tools import chrono, Bar


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    ## TODO TODO le default
    scheduled = []
    progress = Bar(len(instance.jobs))
    for job in instance.jobs:
        progress.advance(1)
        time_start = job.release_date
        for task_id in job.sequence:
            task: Task = Task.by_id(task_id)
            machine_task = min(task.machines_tasks,
                               key=lambda machine_task_: machine_task_.time_free)
            machine = machine_task.machine
            operator = min(machine_task.operators,
                           key=lambda op_id: Operator.by_id(op_id).time_free)
            start_time = max(machine_task.time_free, time_start)
            schedule = Schedule(task_id, start_time, machine, operator)
            scheduled.append(schedule)
            Machine.by_id(machine).time_free = start_time + task.processing_time
            Operator.by_id(operator).time_free = start_time + task.processing_time
            time_start = start_time + task.processing_time

    return Solution(schedules=scheduled)
