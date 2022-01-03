from src.modules.path_and_trajectory_planning.a_star_search import Node
from .dict_edge import DictEdge
from .dict_node import DictNode


class DictGraph:
    __straight_line_distance: dict[str, int]
    __table: dict[str, dict[str, DictEdge]]

    def __init__(self, straight_line_distance: dict[str, int], table: dict[str, dict[str, DictEdge]]) -> None:
        self.__straight_line_distance = straight_line_distance
        self.__table = table

    def get_neighbors(self, node: Node) -> list[Node]:
        dict_node: DictNode = node
        """Essa abstração/ generalização custa O(m) onde m é  número de vizinhos :("""
        return list(map(self.__map_dictedge_to_node, self.__table[dict_node.name].values()))

    @staticmethod
    def __map_dictedge_to_node(edge: DictEdge) -> DictNode:
        return DictNode(name=edge.target)

    def get_real_cost(self, origin: Node, target: Node) -> float:
        dict_origin: DictNode = origin
        dict_target: DictNode = target

        edge = self.__table[dict_origin.name][dict_target.name]

        real_cost = edge.weight 

        return real_cost 

    def get_heuristic_cost(self, origin: Node, target: Node) -> float:
        
        return 0