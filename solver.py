import gurobipy as gb
import pandas as pd
import numpy as np

from extractor import extract_problem_data

"""
This file is used to solve a single problem

@filename: is the path to the problem file to be solved

"""
def solve_problem(filename):

    days, slots_per_day, nb_resources, nb_projects, resources, projects = extract_problem_data(filename=f"problems/{filename}")


    squash_factor= 1 # value that indicate how much to squash the planning of the project. It need to be >= 1

    # calculated data
    total_time_slots = days * slots_per_day
    BIG_M = max(2*total_time_slots, 99)
    max_total_allocation = total_time_slots * nb_resources  # calculate max allocation


    env = gb.Env(empty=True)
    env.setParam("OutputFlag", 0)
    env.start()

    model = gb.Model()

    model.modelSense = gb.GRB.MINIMIZE  #declare minimization

    # variables definition

    X = {}
    for p in range(nb_projects):
        for r in range(nb_resources):
            for t in range(total_time_slots):
                X[(p, r, t)] = model.addVar(vtype=gb.GRB.BINARY, name=f"X_p{p}_r{r}_t{t}")
    S = {}
    F = {}
    for p in range(nb_projects):
        S[(p)] = model.addVar(vtype=gb.GRB.INTEGER, lb=0, ub=total_time_slots, name=f"S_p{p}")
        F[(p)] = model.addVar(vtype=gb.GRB.INTEGER, lb=0, ub=total_time_slots, name=f"F_p{p}")


    Y = model.addVar(vtype=gb.GRB.INTEGER, lb=0, ub=total_time_slots, name=f"Y")

    for v in model.getVars():
        print(v.varName)

    # constraint 1
    # Define constraint: Total working time for each project respect the request
    for p in range(nb_projects):
        model.addConstr(
            sum(X[(p, r, t)] for r in range(nb_resources) for t in range(total_time_slots)) == projects[p].requested_slots)

    # constraint 2
    # constraints no double booking
    for r in range(nb_resources):
        for t in range(total_time_slots):
            model.addConstr(sum(X[(p, r, t)] for p in range(nb_projects)) <= 1)

    # constraint 3
    # on each project only some resources can work on it (the one that are assigned to the project)
    for project in projects:
        for resource in resources:
            if (not project.is_resource_assigned(resource)):
                for t in range(total_time_slots):
                    model.addConstr(X[project.id, resource.id, t] == 0)

    # constraint 2
    for p in range(nb_projects):
        for r in range(nb_resources):
            for t in range(total_time_slots):
                model.addConstr(t * X[(p, r, t)] <= F[p])

    # constraint 3
    for p in range(nb_projects):
        for r in range(nb_resources):
            for t in range(total_time_slots):
                model.addConstr(S[p] <= t * X[(p, r, t)] + (1 - X[(p, r, t)]) * BIG_M)

    # constraint 4
    # constraint assign lower bound of y
    for p in range(nb_projects):
        model.addConstr(F[p] <= Y)

    # constraint 5
    for p in range(nb_projects):
        model.addConstr(F[p] - S[p] + 1 <= projects[p].requested_slots * squash_factor)

    # constraint 8
    # each task are planned to do not start before some specific time
    for p in range(nb_projects):
        model.addConstr(S[p] >= projects[p].non_start_before)

    # constraint 9
    # each task are planned to do not finish after some specific time
    for p in range(nb_projects):
        model.addConstr(F[p] <= projects[p].non_end_after)



    model.setObjective(Y, gb.GRB.MINIMIZE)

    # Set the OutputFlag parameter to 0 to suppress the log
    model.setParam('OutputFlag', 0)

    model.optimize()

    # Write the result on the solution file


    from Allocation import Allocation
    from typing import List

    # write the solution in the file
    output_file = f"solutions/{filename}"

    # Check the status of the model
    status = model.Status
    if status == gb.GRB.INFEASIBLE:
        output_file = f"solutions/infeasible/{filename}"

    # Open the file in write mode
    with open(output_file, "w") as file:
        if status == gb.GRB.INFEASIBLE:
            file.write("Model is infeasible\n")
        elif status == gb.GRB.UNBOUNDED:
            file.write("Model is unbounded\n")
        elif status == gb.GRB.INF_OR_UNBD:
            file.write("Model is infeasible or unbounded\n")
        elif status == gb.GRB.OPTIMAL:
            # Solution found and is optimal
            file.write("Optimal solution found\n")

            # Check the number of solutions
            sol_count = model.SolCount
            file.write(f"Number of solutions found: {sol_count}\n")
            file.write(f"Objective value: {model.ObjVal}\n")
            file.write(f"Solver runtime: {model.Runtime:f} seconds\n\n")

            allocations: List[Allocation] = []
            for project in projects:
                for resource in project.assigned_resources:
                    for t in range(int(Y.x)):
                        if (X[(project.id, resource.id, t)].x == 1.0):
                            allocations.append(Allocation(project, resource,
                                                          t))  # this update the two collections in project and resource to plan the schedule

            for project in projects:
                project.calculate_real_schedule()  # calculate real_start and real_end

            file.write(f"PROJECT SCHEDULE, nb_projects: {len(projects)}\n")
            for project in projects:
                file.write(
                    f"Project_ID: {project.id}, resources_used: {len(project.allocations)}, requested_slots: {project.requested_slots}\n")
                for resource, value in project.allocations.items():
                    file.write(f"Resource: {resource.id}, working: {value}\n")
                file.write("\n")

            # Resource POV allocation
            file.write(f"RESOURCE ALLOCATION, nb_resources: {len(resources)}\n")
            for resource in resources:
                file.write(f"Resource_ID: {resource.id}, allocations: {len(resource.allocations)}\n")
                for t in resource.allocations:
                    file.write(f"t: {t}, project: {resource.allocations[t].id}\n")
                file.write("\n")

        else:
            file.write(f"Optimization was stopped with status ={status}\n", )