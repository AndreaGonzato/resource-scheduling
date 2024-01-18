from typing import List

from Resource import Resource


class Project:
    def __init__(self, id: int, requested_slots: int, assigned_resources: List[Resource] = []) -> None:
        self.id = id
        self.requested_slots: int = requested_slots
        self.assigned_resources = assigned_resources

    def is_resource_assigned(self, resource: Resource) -> bool:
        if resource in self.assigned_resources:
            return True
        else:
            return False

    def __repr__(self) -> str:
        return f"Project{{id : {self.id}, requested_slot : {self.requested_slots}, assigned_resources: {self.assigned_resources} }}"
