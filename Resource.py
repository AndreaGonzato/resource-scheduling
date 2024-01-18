from typing import List


class Resource:
    def __init__(self, id: int) -> None:
        self.id = id

    def __repr__(self) -> str:
        return f"Resource{{id : {self.id}}}"

    def __eq__(self, other):
        if not isinstance(other, Resource):
            return NotImplemented
        return self.id == other.id

