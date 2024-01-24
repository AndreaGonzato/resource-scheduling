# This script write and generate an instance of the optimization problem
import math
import random
import numpy as np
from typing import List


def generate_problem(nb_projects=30, nb_resources=15, days=5, slots_per_day=4, start_time_assignation=False):

    filename = (f"problems/complexity{nb_projects*nb_resources*days*slots_per_day}_nb_projects{nb_projects}_nb_resources{nb_resources}_slots{slots_per_day*days}"
                f"_start_time_assignation{start_time_assignation}.txt")


    # PARAMETERS
    assignation_probability = 0.5
    random.seed(10)
    np.random.seed(11)

    # CALCULATED DATA
    total_time_slots = days * slots_per_day
    max_total_allocation = total_time_slots * nb_resources

    # Open the file in write mode
    with open(filename, "w") as file:
        # Write the text to the file
        file.write(f"days={days}\n")
        file.write(f"slots_per_day={slots_per_day}\n")
        file.write(f"nb_resources={nb_resources}\n")
        file.write(f"nb_projects={nb_projects}\n")
        file.write(f"\n")

        file.write(f"RESOURCES\n")
        for i in range(nb_resources):
            file.write(f"id={i}\n")
        file.write(f"\n")

        total_requested_slots = 0
        file.write(f"PROJECTS\n")
        for p in range(nb_projects):
            requested_slots = min(total_time_slots//2, max(1, int(np.random.normal((max_total_allocation*0.6)/nb_projects, 2))))
            total_requested_slots += requested_slots

            if start_time_assignation:
                non_start_before = random.randint(0, total_time_slots // 2)
                non_end_after = min(total_time_slots, math.ceil(non_start_before + random.uniform(1, 2) * requested_slots))
            else:
                non_start_before = 0
                non_end_after = total_time_slots

            assigned_resources: List[int] = []
            for i in range(nb_resources):
                if random.random() <= assignation_probability:
                    assigned_resources.append(i)

            if len(assigned_resources) == 0:
                # ensure that each project has at least one resource assigned
                assigned_resources.append(random.randint(0, nb_resources-1))

            file.write(f"id={p}, requested_slots={requested_slots}, non_start_before={non_start_before}, non_end_after={non_end_after}, "
                       f"assigned_resources={assigned_resources}\n")

        print("max_total_allocation:", max_total_allocation)
        print("total_requested_slots:", total_requested_slots)




for p in [5, 10]:
    for r in [2, 10]:
        for d in [1, 5]:
            for s in [2, 8, 16]:
                generate_problem(nb_projects=p, nb_resources=r, days=d, slots_per_day=s, start_time_assignation=False)
# DATA
'''
nb_projects = 30
nb_resources = 2
days = 2
slots_per_day = 1
start_time_assignation = False
'''