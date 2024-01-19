from typing import Dict, List

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Resource import Resource


class Project:
    def __init__(self, id: int, requested_slots: int, start_time: int = 0,
                 end_time: int = float('inf'), assigned_resources: List['Resource'] = []) -> None:
        self.id = id
        self.requested_slots: int = requested_slots
        self.assigned_resources: List[Resource] = assigned_resources
        self.allocations: Dict[Resource, List[int]] = {}
        if start_time < end_time:
            self.start_time: int = start_time
            self.end_time: int = end_time
        else:
            raise ValueError('start_time can not be smaller than end_time')

    def schedule_work(self, resource: 'Resource', time: int) -> None:
        if resource not in self.allocations:
            self.allocations[resource] = []
        if time in self.allocations[resource]:
            return
        self.allocations[resource].append(time)

    def is_resource_assigned(self, resource: 'Resource') -> bool:
        if resource in self.assigned_resources:
            return True
        else:
            return False

    def get_allocations(self) -> List['Resource']:
        for el in self.allocations:
            print(el)

    def __repr__(self) -> str:
        return (f"Project{{id : {self.id}, requested_slot : {self.requested_slots}, "
                f"start_time: {self.start_time}, end_time: {self.end_time}, assigned_resources: {self.assigned_resources}  }}")
