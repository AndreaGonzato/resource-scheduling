
from collections import OrderedDict


from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Project import Project

class Resource:
    def __init__(self, id: int) -> None:
        self.id = id
        self.allocations = OrderedDict()

    def assign_to_work(self, time: int, project: 'Project'):
        self.allocations[time] = project
        self.allocations = dict(sorted(self.allocations.items()))  # keep it ordered by key(time)

    def get_allocations(self) -> str:
        output = f"Resource {self.id}\n"
        for t in self.allocations:
            output += f"t: {t}, project: {self.allocations[t].id}\n"
        return output

    def __repr__(self) -> str:
        return f"Resource{{id : {self.id}}}"

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
