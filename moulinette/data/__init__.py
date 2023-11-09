"""Handling of input/output files through aliases.
Parsing method to read an Instance and write/retrieve a Solution.
Driver instantiated for one instance by alias.
Parser (loaded with `Driver.load`) implements 'next' iterative parsing method.
"""

from model import *

from .driver import DriverBase

# todo: download input files

# todo-dev: single output file description


class Driver(DriverBase):
    """Custom model building methods."""

    def read(self):
        """Read instance from file."""
        reader = self.load("r", "in")
        json_dict = reader.next()
        # print(json_dict)
        json_parameters = json_dict["parameters"]
        parameters_class = {"costs": Costs, "size": Size}
        parameters = Parameters(**{a: parameters_class[a](**json_parameters[a])
                                   for a in json_parameters})
        json_jobs = json_dict["jobs"]
        jobs = [Job(**a) for a in json_jobs]

        tasks = []
        for json_task in json_dict["tasks"]:
            json_machines = json_task["machines"]
            machines_tasks = [MachineTask(**machine) for machine in json_machines]
            d_task = {"task": json_task["task"],
                      "processing_time": json_task["processing_time"],
                      "machines_tasks": machines_tasks}
            tasks.append(Task(**d_task))
        for job in jobs:
            for task_id in job.sequence:
                Task.by_id(task_id).job = job.id_
                Task.time_free = job.release_date

        operators = [Operator(i+1) for i in range(parameters.size.nb_operators)]
        machines = [Machine(i+1) for i in range(parameters.size.nb_machines)]
        inst = Instance(json_dict, parameters, jobs, tasks, operators, machines)
        return inst

    def write(self, solution):
        """Write solution to file."""
        writer = self.load("w", "out")
        writer.next([schedule.__dict__ for schedule in solution.schedules])

    def retrieve(self):
        """Read solution from file."""
        reader = self.load("r", "out")
        json_sol = reader.next()
        return Solution(schedules=[Schedule(**d) for d in json_sol])


def better_gain(gain):
    """Is the gain better ?

    if the objective is a minimization, the gains are better if < 0.
    else when gain > 0 :
        correct the return below in function of that."""
    return gain < 0
