"""Sorting a little better"""

from model import *
from tools import chrono, Bar


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    scheduled = []
    progress = Bar(len(instance.jobs))
    instance.jobs.sort(key=lambda job_: job_.due_date)
    for job in instance.jobs:
        progress.advance(1)
        cost_job, scheduled_job = test_job(instance, job, restore_time=False)
        scheduled.extend(scheduled_job)
    return Solution(schedules=scheduled)


def test_job(instance: Instance, job: Job, restore_time=True):
    dict_machine = Machine.dict_id["Machine"]
    save_time_machine = {machine_id: dict_machine[machine_id].time_free
                         for machine_id in dict_machine}
    dict_operator = Operator.dict_id["Operator"]
    save_time_operator = {operator_id: dict_operator[operator_id].time_free
                          for operator_id in dict_operator}

    time_start = job.release_date
    scheduled = []
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

    costs = instance.parameters.costs
    tardiness = max(time_start-job.due_date, 0)
    u_j = 1 if tardiness > 0 else 0
    cost_job = job.weight * (
                time_start + costs.alpha * u_j + costs.beta * tardiness)
    if restore_time:
        for machine_id in save_time_machine:
            Machine.by_id(machine_id).time_free = save_time_machine[machine_id]
        for operator_id in save_time_operator:
            Operator.by_id(operator_id).time_free = save_time_operator[operator_id]
    return cost_job, scheduled

