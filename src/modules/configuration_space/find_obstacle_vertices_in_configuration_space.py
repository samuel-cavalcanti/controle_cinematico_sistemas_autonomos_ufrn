from functools import reduce
from typing import Optional

import numpy as np

from .normal_vector_wrapper import NormalVectorWrapper


class FindObstacleVerticesInConfigurationSpace:
    __sorted_nodes: list[NormalVectorWrapper]
    __length_sorted_list: int

    def execute(self, sorted_nodes: list[NormalVectorWrapper], obstacle_nodes: list[NormalVectorWrapper]) -> np.ndarray:

        self.__length_sorted_list = len(sorted_nodes)
        self.__sorted_nodes = sorted_nodes

        new_obstacles_vertices: list[np.ndarray] = reduce(self.__find_new_vertices, obstacle_nodes, [])

        return np.array(new_obstacles_vertices)

    def __find_new_vertices(self, vertices: list[np.ndarray], obstacle_node: NormalVectorWrapper) -> list[np.ndarray]:
        next_node_index = obstacle_node.next_node_index

        next_robot_node = self.__search_for_node(obstacle_node, next_node_index, is_robot_vector=True)
        next_obstacle_node = self.__search_for_node(obstacle_node, next_node_index, is_robot_vector=False)

        if next_robot_node is None or next_obstacle_node is None:
            return vertices

        new_vertices = [next_obstacle_node.vertex - next_robot_node.vertex,
                        obstacle_node.vertex - next_robot_node.vertex]

        return vertices + new_vertices

    def __search_for_node(self, first_node: NormalVectorWrapper, node_index: int, is_robot_vector: bool) -> Optional[NormalVectorWrapper]:
        node = self.__sorted_nodes[node_index]

        if first_node is node:
            return None

        if node.is_robot_vector == is_robot_vector:
            return node

        next_index = node_index + 1

        next_index = next_index if next_index < self.__length_sorted_list else 0

        return self.__search_for_node(first_node, next_index, is_robot_vector)
