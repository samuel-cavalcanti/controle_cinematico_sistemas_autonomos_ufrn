from .mesh_node import MeshNode
from ..a_star_search import Node
from ....grid import Grid
import numpy as np


class MeshGridGraph:
    """
        Grafo formado por uma malha 2D
    """

    __grid: Grid
    __motion = [(1, 0),
                (0, 1),
                (-1, 0),
                (0, -1),
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1)]

    def __init__(self, grid: Grid) -> None:
        self.__grid = grid

    def get_neighbors(self, node: Node) -> list[Node]:
        mesh_node: MeshNode = node
        neighbors = list()
        for i, j in self.__motion:
            index = (mesh_node.x_index + i, mesh_node.y_index + j)
            if self.__grid.is_valid_index(x=index[0], y=index[1]):
                neighbors.append(MeshNode(x_index=index[0], y_index=index[1]))

        return neighbors
