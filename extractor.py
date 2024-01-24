import re
from typing import List

from Project import Project
from Resource import Resource


def extract_int_from_line(file):
    content = file.readline()
    parts = content.split("=")
    return int(parts[1].strip())


def parse_resource(line) -> Resource:
    pattern = r'id=(\d+)'
    match = re.match(pattern, line)
    if match:
        id = int(match.group(1))
        return Resource(id=id)
    else:
        raise ValueError('incorrect pattern matching for project line')


def parse_project(line, resources: List[Resource]) -> Project:
    pattern = r'id=(\d+), requested_slots=(\d+), non_start_before=(\d+), non_end_after=(\d+), assigned_resources=\[([0-9, ]+)\]'
    match = re.match(pattern, line)
    if match:
        id = int(match.group(1))
        requested_slots = int(match.group(2))
        start_time = int(match.group(3))
        end_time = int(match.group(4))
        assigned_resources_id = list(map(int, match.group(5).split(', ')))
        assigned_resources: List[Resource] = []
        for _id in assigned_resources_id:
            if _id < 0 or _id >= len(resources):
                raise ValueError(f'incorrect assignation of resource {_id} to project {id}')
            assigned_resources.append(resources[_id])

        return Project(id=id, requested_slots=requested_slots, non_start_before=start_time,
                       not_end_after=end_time, assigned_resources=assigned_resources)
    else:
        raise ValueError('incorrect pattern matching for project line')


def extract_problem_data(filename: str):
    # Open the file in read mode
    with open(filename, "r") as file:
        # extract the value in the header
        days = extract_int_from_line(file)
        slots_per_day = extract_int_from_line(file)
        nb_resources = extract_int_from_line(file)
        nb_projects = extract_int_from_line(file)

        # skip 2 line
        file.readline()
        file.readline()

        resources: List[Resource] = []
        for r in range(nb_resources):
            resources.append(parse_resource(file.readline().strip()))

        # skip 2 line
        file.readline()
        file.readline()

        projects: List[Project] = []
        for p in range(nb_projects):
            projects.append(parse_project(file.readline().strip(), resources=resources))

        return days, slots_per_day, nb_resources, nb_projects, resources, projects


#days, slots_per_day, nb_resources, nb_projects, resources, projects = extract_problem_data(filename="problems/instance_1.txt")

