import numpy as np

from typing import List

random_seed = 10
assignation_probability = 0.5  # probability to assign resource r to project p


# create assignation matrix resources x projects
def generate_random_assignation_matrix(nb_resources:int, nb_projects:int) -> np.ndarray:
    np.random.seed(random_seed)  # You can choose any number as the seed
    assignation = np.random.choice([0, 1], size=(nb_resources, nb_projects),
                                   p=[1-assignation_probability, assignation_probability])

    # Ensure each project has at least one resource assignation
    for i in range(nb_projects):
        if not np.any(assignation[:, i]):  # Check if the col has no '1's
            random_row = np.random.randint(nb_resources)  # Choose a random row
            assignation[random_row, i] = 1  # Set the chosen element to '1'

    return assignation


def generate_random_requested_slots_per_project(nb_projects: int, max_total_allocation: int) -> List[int]:
    requested_slots_per_project: List[int] = []
    for i in range(nb_projects):
        requested_slots_per_project.append(
            max(0, int(np.random.normal((max_total_allocation*0.6)/nb_projects, 2)))
            )
    return requested_slots_per_project



