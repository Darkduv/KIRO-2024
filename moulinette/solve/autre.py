"""Sorting a little better"""
import random

from model import *
from tools import chrono, Bar


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    scheduled = []
    progress = Bar(len(instance.tasks))
    can_start_task = [Task.by_id(job.sequence[0]) for job in instance.jobs]
    for job in instance.jobs:
        Task.by_id(job.sequence[0]).time_free = job.release_date
    while can_start_task:
        random.shuffle(can_start_task)
        progress.advance(1)
        ll = [(task.min_time_free()+task.processing_time, task) for task in can_start_task]
        maxi = max(ll, key=lambda dt_task: dt_task[0])[0]
        if random.random() <= 0.2:
            task: Task = min(ll, key=lambda dt_task: dt_task[0])[1]
        else:
            task: Task = random.choices(can_start_task, weights=[maxi + 1 - a[0] for a in ll], k=1)[0]
        can_start_task.remove(task)

        job_id = task.job
        job = Job.by_id(job_id)
        start_time = task.min_time_free()
        m_tasks = [max(mt.time_free, task.time_free) for mt in task.machines_tasks]
        m_task: MachineTask = task.machines_tasks[m_tasks.index(start_time)]
        machine = m_task.machine
        operator = min(m_task.operators, key=lambda op_id:Operator.by_id(op_id).time_free)
        schedule = Schedule(task.id_, start_time, machine, operator)
        scheduled.append(schedule)
        end = start_time + task.processing_time
        # print(f"{schedule = } and {task.processing_time=} and {task.job = }")
        Machine.by_id(machine).time_free = end
        Operator.by_id(operator).time_free = end
        i_task = job.sequence.index(task.id_)
        if i_task+1 < len(job.sequence):
            Task.by_id(job.sequence[i_task + 1]).time_free = end
            can_start_task.append(Task.by_id(job.sequence[i_task+1]))

    return Solution(schedules=scheduled)



