import numpy as np

from .normal_vector_wrapper import NormalVectorWrapper


def sort_nodes_by_normal_angle(node: NormalVectorWrapper) -> float:
    theta = np.arctan2(node.normal_vec[1], node.normal_vec[0])
    if theta >= 0:
        return theta
    else:
        return 2 * np.pi + theta


def create_sorted_nodes(obstacle_nodes: list[NormalVectorWrapper], robot_nodes: list[NormalVectorWrapper]):
    nodes = obstacle_nodes + robot_nodes
    sorted_nodes: list[NormalVectorWrapper] = sorted(nodes, key=sort_nodes_by_normal_angle)
    length_sorted_node = len(sorted_nodes)

    for index, node in enumerate(sorted_nodes):
        next_index = index + 1
        node.next_node_index = next_index if next_index < length_sorted_node else 0

    return sorted_nodes

