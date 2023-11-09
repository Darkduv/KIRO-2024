"""Solution scoring and verification."""

# import numpy as np
from .definitions import *


def score(instance: Instance, solution: Solution):
    """Compute solution score for given instance and check its validity."""
    # TODO TODO le judge est ici
    machine_tasks = {}
    operator_tasks = {}
    costs = instance.parameters.costs

    for schedule in solution.schedules:
        machine_id = schedule.machine
        operator_id = schedule.operator
        if machine_id not in machine_tasks:
            machine_tasks[machine_id] = []
        if operator_id not in operator_tasks:
            operator_tasks[operator_id] = []
        task_id = schedule.task
        start = schedule.start
        task: Task = Task.by_id(task_id)
        end = start + task.processing_time
        if start < Job.by_id(task.job).release_date:
            raise ValueError(f"Task id:{task_id} must start"
                             f" after job {task.job} release date")
        machine_tasks[machine_id].append((start, end, task_id))
        operator_tasks[operator_id].append((start, end, task_id))

    for operator_id in operator_tasks:
        operator_tasks[operator_id].sort()
        start0, end0, task_id0 = operator_tasks[operator_id][0]
        for start, end, task_id in operator_tasks[operator_id][1:]:
            if start < end0:
                print(f"{start = } and {end0 = }")
                print(f"{start0 = } and {end0 = }")
                print(f"{start = } and {end = }")
                raise ValueError(f"Task {task_id0} and {task_id} overlap"
                                 f" for operator {operator_id}")
            start0, end0 = start, end

    for machine_id in machine_tasks:
        machine_tasks[machine_id].sort()
        start0, end0, task_id0 = machine_tasks[machine_id][0]
        for start, end, task_id in machine_tasks[machine_id][1:]:
            if start < end0:
                print(f"{start = } and {end0 = }")
                print(f"{start0 = } and {end0 = }")
                print(f"{start = } and {end = }")
                raise ValueError(f"Task {task_id0} and {task_id} overlap for"
                                 f" machine {machine_id}")
            start0, end0 = start, end
    schedules_task_id = {schedule.task: schedule for schedule in solution.schedules}
    cost_all = 0
    for job in instance.jobs:
        start0, end0 = job.release_date, job.release_date
        for task_id in job.sequence:
            task: Task = Task.by_id(task_id)
            schedule = schedules_task_id[task_id]
            if task_id in [3, 4]:
                print(f"task: {task} \n   and {schedule =}")
            start = schedule.start
            end = start + task.processing_time
            if start < end0:
                print(f"{job.sequence = }")
                print(f"{job.release_date = }")
                raise ValueError(f"Job {job.id_} in wrong order/overlap of "
                                 f"task_id: {task_id}")
            start0, end0 = start, end
        end_job = end0
        tardiness = max(end_job-job.due_date, 0)
        u_j = 1 if tardiness > 0 else 0
        cost_all += job.weight * (end_job + costs.alpha * u_j + costs.beta * tardiness)
    return cost_all
