from dataclasses import dataclass
from typing import Any, Callable, Optional, Tuple
from functools import reduce
import numpy as np


def normal_vector(initial_point: np.ndarray, final_point: np.ndarray) -> np.ndarray:
    vector = final_point - initial_point
    """ 
        é feita uma rotação de 90 graus com o vetor, que se traduz em
        x = -y
        y = x
    """
    return np.array([-vector[1], vector[0]])


def get_normal_vectors_from_convex_polygon(polygon_points: np.ndarray) -> np.ndarray:
    """
        Esse algoritmo parte que os pontos já estejam  ordenados de maneira circular:

            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """

    length = len(polygon_points)

    normal_vectors = [normal_vector(initial_point=polygon_points[0], final_point=polygon_points[-1])]

    def get_normal_vector(index: int) -> np.ndarray:
        final_point = polygon_points[index]
        initial_point = polygon_points[index+1]
        return normal_vector(initial_point, final_point)

    normal_vectors += [get_normal_vector(index) for index in range(length-1)]

    return np.array(normal_vectors)


@dataclass
class Node:
    is_robot_vector: bool
    normal_vec: np.ndarray
    vertice: np.ndarray
    next_node_index: Optional[int]

    def __str__(self) -> str:
        normal_angle_in_rads = np.arctan2(self.normal_vec[1], self.normal_vec[0])
        normal_angle_in_deg = np.rad2deg(normal_angle_in_rads) if normal_angle_in_rads >= 0 else 360 + np.rad2deg(normal_angle_in_rads)
        return f'robot: {self.is_robot_vector} normal : {self.normal_vec}  vertice: {self.vertice} angle: {normal_angle_in_deg} next node: {self.next_node_index}'


def normals_to_node(is_robot: bool, vetices: np.ndarray) -> Callable[[Tuple[int,  np.ndarray]], Node]:

    def to_node(t: Tuple[int,  np.ndarray]):
        index, normal = t
        return Node(is_robot_vector=is_robot,
                    next_node_index=None,
                    normal_vec=normal,
                    vertice=vetices[index])

    return to_node


def sort_nodes_by_normal_angle(node: Node) -> float:
    theta = np.arctan2(node.normal_vec[1], node.normal_vec[0])
    if theta >= 0:
        return theta
    else:
        return 2*np.pi + theta


def find_obstacle_vertices_in_configuration_space(sorted_nodes: list[Node], obstacle_nodes: list[Node]) -> np.ndarray:

    length_sorted_node = len(sorted_nodes)

    def search_for_node(first_node: Node, node_index: int, is_robot_vector: bool) -> Optional[Node]:

        node = sorted_nodes[node_index]

        if first_node is node:
            return None

        if node.is_robot_vector == is_robot_vector:
            return node

        next_index = node_index + 1

        next_index = next_index if next_index < length_sorted_node else 0

        return search_for_node(first_node, next_index, is_robot_vector)

    def find_new_vertices(verices: list[np.ndarray], obstacle_node: Node) -> list[np.ndarray]:
        next_node_index = obstacle_node.next_node_index

        next_robot_node = search_for_node(obstacle_node, next_node_index, is_robot_vector=True)
        next_obstacle_node = search_for_node(obstacle_node, next_node_index, is_robot_vector=False)

        if next_robot_node is None or next_obstacle_node is None:
            return verices

        new_vertices = [next_obstacle_node.vertice - next_robot_node.vertice,
                        obstacle_node.vertice - next_robot_node.vertice]

        return verices + new_vertices

    new_obstacles_vertices: list[np.ndarray] = reduce(find_new_vertices, obstacle_nodes, [])

    return new_obstacles_vertices


def make_configuration_space(robot_vetices: np.ndarray, obstacles_vertices: list[np.ndarray]) -> list[np.ndarray]:
    """
           Recebe os vetices do robô onde a origem do centro de coordenadas é o centro geométrico do poligono convexo
           do robô, caso não esteja, o algoritmo não funciona. 

           Esse algoritmo parte que os pontos já estejam  ordenados da seguinte maneira circular:

            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """

    obstacles_normals = [get_normal_vectors_from_convex_polygon(vertices) for vertices in obstacles_vertices]

    robot_normals = get_normal_vectors_from_convex_polygon(robot_vetices)

    robot_nodes_map = map(normals_to_node(is_robot=True, vetices=robot_vetices), enumerate(-robot_normals))

    robot_nodes: list[Node] = list(robot_nodes_map)

    def obstacles_to_vertices(t: tuple[np.ndarray, np.ndarray]) -> np.ndarray:
        obstacle_normals, obstacle_vertices = t
        obstacle_nodes_map = map(normals_to_node(is_robot=False, vetices=obstacle_vertices), enumerate(obstacle_normals))
        obstacle_nodes: list[Node] = list(obstacle_nodes_map)
        nodes = obstacle_nodes + robot_nodes
        sorted_nodes: list[Node] = sorted(nodes, key=sort_nodes_by_normal_angle)
        length_sorted_node = len(sorted_nodes)

        for index, node in enumerate(sorted_nodes):
            next_index = index + 1
            node.next_node_index = next_index if next_index < length_sorted_node else 0

        return find_obstacle_vertices_in_configuration_space(sorted_nodes, obstacle_nodes)

    vertices_map = map(obstacles_to_vertices, zip(obstacles_normals, obstacles_vertices))

    return list(vertices_map)

    """ ordenar por angulo, do menor angulo para o maior
         O(nlog(n))
         
         gerar indices O(n)

         busca linear em um anel, O(n)

         complexidade: O(nlog(n))         
    """