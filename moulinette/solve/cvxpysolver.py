import cvxpy
import numpy as np

from model import *
from tools import chrono


@chrono
def solve(instance: Instance):
    """Compute nothing."""
    sizes = instance.parameters.size
    costs = instance.parameters.costs
    B_i = cvxpy.Variable(sizes.nb_tasks, integer=True)
    B_j = cvxpy.Variable(sizes.nb_jobs, integer=True)
    C_i = cvxpy.Variable(sizes.nb_tasks, integer=True)
    C_j = cvxpy.Variable(sizes.nb_jobs, integer=True)
    T_j = cvxpy.Variable(sizes.nb_jobs, integer=True)
    p_i = np.array([Task.by_id(task_id+1).processing_time
                    for task_id in range(sizes.nb_tasks)])
    w_j = np.array([Job.by_id(job_id+1).weight
                    for job_id in range(sizes.nb_jobs)])
    r_j = np.array([Job.by_id(job_id+1).release_date
                    for job_id in range(sizes.nb_jobs)])
    d_j = np.array([Job.by_id(job_id+1).due_date
                    for job_id in range(sizes.nb_jobs)])
    mat_M = cvxpy.Variable((sizes.nb_tasks, sizes.nb_machines), boolean=True)
    mat_O = cvxpy.Variable((sizes.nb_tasks, sizes.nb_operators), boolean=True)
    first_task_j = []
    last_task_j = []
    first_task = []
    second_task = []
    for job in instance.jobs:
        val = np.array([0]*sizes.nb_tasks)
        val1 = val[:]
        val1[job.sequence[0]-1] = 1
        val2 = val[:]
        val2[job.sequence[-1]-1] = 1
        first_task_j.append(val1)
        last_task_j.append(val2)
        for k in range(len(job.sequence)-1):
            val3 = val[:]
            val3[job.sequence[k]-1] = 1
            val4 = val[:]
            val4[job.sequence[k+1]-1] = 1
            first_task.append(val3)
            second_task.append(val4)

    first_task_j = np.array(first_task_j)
    last_task_j = np.array(last_task_j)
    first_task = np.array(first_task)
    second_task = np.array(second_task)


    cons = [
        C_i == B_i + p_i,
        B_j >= r_j,
        T_j >= 0,
        T_j >= C_j - d_j,
        first_task_j @ B_i == B_j,
        last_task_j @ C_i == C_j,
        first_task @ C_i <= second_task @ B_i,
        cvxpy.sum(mat_M, axis=1) == 1,
        cvxpy.sum(mat_O, axis=1) == 1,
    ]
    cost = w_j @ (C_j + costs.alpha * 1 + costs.beta * T_j)

    prob = cvxpy.Problem(cvxpy.Minimize(cost), cons)
    prob.solve(solver=cvxpy.GLPK_MI)

    return Solution(prods, distribs, commands)
