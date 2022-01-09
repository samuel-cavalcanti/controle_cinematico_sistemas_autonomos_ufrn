from typing import Protocol
from .node import Node

class AStarParameters(Protocol):

    def get_real_cost(self, origin: Node, target: Node) -> float:
        ...

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:
        ...