# This script write and generate an instance of the optimization problem
import math
import random
import numpy as np
from typing import List


filename = "problems/instance_1.txt"  # Define the filename

# DATA
days = 5
slots_per_day = 6
nb_resources = 5
nb_projects = 8

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
        requested_slots = min(total_time_slots//2, max(0, int(np.random.normal((max_total_allocation*0.6)/nb_projects, 2))))
        total_requested_slots += requested_slots

        start_time = random.randint(0, total_time_slots//2)
        end_time = min(total_time_slots, math.ceil(start_time+random.uniform(1, 2)*requested_slots))

        assigned_resources: List[int] = []
        for i in range(nb_resources):
            if random.random() <= assignation_probability:
                assigned_resources.append(i)

        if len(assigned_resources) == 0:
            # ensure that each project has at least one resource assigned
            assigned_resources.append(random.randint(0, len(assigned_resources)-1))

        file.write(f"id={p}, requested_slots={requested_slots}, start_time={start_time}, end_time={end_time}, "
                   f"assigned_resources={assigned_resources}\n")

    print("max_total_allocation:", max_total_allocation)
    print("total_requested_slots:", total_requested_slots)

