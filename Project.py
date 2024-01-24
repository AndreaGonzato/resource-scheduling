from typing import Dict, List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Resource import Resource


class Project:
    def __init__(self, id: int, requested_slots: int, non_start_before: int = 0,
                 not_end_after: int = float('inf'), assigned_resources: List['Resource'] = []) -> None:
        self.real_end = None
        self.real_start = None
        self.id = id
        self.requested_slots: int = requested_slots
        self.assigned_resources: List[Resource] = assigned_resources
        self.allocations: Dict[Resource, List[int]] = {}
        if non_start_before <= not_end_after:
            self.non_start_before: int = non_start_before
            self.non_end_after: int = not_end_after
        else:
            raise ValueError(f"non_start_before {non_start_before} can not be smaller than not_end_after {not_end_after}")

    def add_schedule_work(self, resource: 'Resource', time: int) -> None:
        if resource not in self.allocations:
            self.allocations[resource] = []
        if time in self.allocations[resource]:
            return
        self.allocations[resource].append(time)

    def calculate_real_schedule(self):
        # calculate real_start and real_end
        min_time_slot = float('inf')
        max_time_slot = 0
        for resource, working_slots in self.allocations.items():
            for working_slot in working_slots:
                if working_slot < min_time_slot:
                    min_time_slot = working_slot
                if working_slot > max_time_slot:
                    max_time_slot = working_slot

        self.real_start = min_time_slot
        self.real_end = max_time_slot

    def is_resource_assigned(self, resource: 'Resource') -> bool:
        if resource in self.assigned_resources:
            return True
        else:
            return False


    def __repr__(self) -> str:
        return (f"Project{{id : {self.id}, requested_slot : {self.requested_slots}, "
                f"non_start_before: {self.non_start_before}, non_end_after: {self.non_end_after}, "
                f"assigned_resources: {self.assigned_resources}  }}")
