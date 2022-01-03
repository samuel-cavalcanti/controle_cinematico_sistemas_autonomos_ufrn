
from typing import Protocol
from .node import Node
from src.modules.utils import Position


class Graph(Protocol):

    def get_neighbors(self, node: Node) -> list[Node]:
        ...

    def get_real_cost(self, origin: Node, target: Node) -> float:
        ...

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:
        ...
