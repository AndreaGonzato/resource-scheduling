from Project import Project
from Resource import Resource


class Allocation:
    def __init__(self, project: Project, resource: Resource, time: int) -> None:
        self.project = project
        self.resource = resource
        self.time = time

        self.resource.assign_to_work(time, project)
        self.project.add_schedule_work(resource, time)


