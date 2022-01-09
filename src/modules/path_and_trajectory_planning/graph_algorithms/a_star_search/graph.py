
from typing import Protocol
from .node import Node
from src.modules.utils import Position


class Graph(Protocol):

    def get_neighbors(self, node: Node) -> list[Node]:
        ...