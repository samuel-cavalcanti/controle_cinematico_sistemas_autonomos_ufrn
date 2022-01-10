from pathlib import Path
import json
from src.modules.path_and_trajectory_planning.graph_algorithms.a_star_search.graph import Graph

from .dict_graph import DictGraph, DictEdge


class JsonGraphWrapper:
    __json_file_path: Path

    __ORIGIN = "origin"
    __NAME = "name"
    __TARGET = "target"
    __WEIGHT = "weight"
    __EDGES = "edges"
    __STRAIGHT_LINE_DISTANCE = "straight_line_distance"

    def __init__(self, json_file_path: Path) -> None:
        self.__json_file_path = json_file_path

    @staticmethod
    def __load_json_object(json_file_path: Path) -> dict:
        with open(json_file_path) as json_file:
            return json.load(json_file)

    def make_graph(self) -> Graph:
        json_object = self.__load_json_object(self.__json_file_path)
        distance = json_object[self.__STRAIGHT_LINE_DISTANCE]
        edges_table = self.__make_edges_table(json_object[self.__EDGES])

        return DictGraph(straight_line_distance=distance, table=edges_table)

    def __make_edges_table(self, json_edges: dict) -> dict[str, dict[str, DictEdge]]:
        edges_table: dict[str, dict[str, DictEdge]] = dict()

        for json_edge in json_edges:
            origin_node_name = json_edge[self.__ORIGIN][self.__NAME]
            target_node_name = json_edge[self.__TARGET][self.__NAME]
            edge = edges_table.get(origin_node_name, {})
            edge[target_node_name] = DictEdge(origin=origin_node_name, target=target_node_name, weight=json_edge[self.__WEIGHT])

            edges_table[origin_node_name] = edge

        return edges_table
