from modules.path_and_trajectory_planning.mesh_grid_graph.mesh_node import MeshNode
from ..a_star_search import Node

import numpy as np


class MeshGridGraph:

    __grid: np.ndarray
    __limit_index_x: int
    __limit_index_y: int

    def __init__(self, grid: np.ndarray) -> None:
        assert grid.shape[-1] == 2, "expected and grid with last shape is x,y pos"
        assert len(grid.shape) == 3, "expected an grid 3D shape"
        self.__grid = grid

    def get_neighbors(self, node: Node) -> list[Node]:
        mesh_node: MeshNode = node
        neighbors = list()
        for i in [-1, 1]:
            for j in [-1, 1]:
                index = (mesh_node.x_index + i, mesh_node.y_index + j)
                if not self.__out_of_bounds(index):
                    neighbors.append(MeshNode(x_index=i, y_index=j))

        return neighbors

    def get_real_cost(self, origin: Node, target: Node) -> float:
        origin_mesh_node: MeshNode = origin
        target_mesh_node: MeshNode = target
        pos_origin = self.__grid[origin_mesh_node.x_index][origin_mesh_node.y_index]
        pos_target = self.__grid[target_mesh_node.x_index][target_mesh_node.y_index]

        return np.linalg.norm(pos_origin - pos_target)

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:

        pass

    def __out_of_bounds(self, index: tuple[int, int]) -> bool:
        x_out_of_bound = index[0] < 0 or index[1] > self.__grid.shape[0]
        y_out_of_bound = index[1] < 0 or index[1] > self.__grid.shape[1]

        return x_out_of_bound or y_out_of_bound
