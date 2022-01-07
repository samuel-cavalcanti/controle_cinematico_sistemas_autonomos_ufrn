import unittest
from pathlib import Path
from .json_graph_wrapper import JsonGraphWrapper
from src.modules.path_and_trajectory_planning.graph_algorithms.a_star_search import Graph, AStarSearch
from .dict_graph import DictNode


class AStarSearchTestCase(unittest.TestCase):

    def test_a_star(self):
        """Testando A* com a atividade da 1 unidade de IA"""
        wrapper = JsonGraphWrapper(Path('tests').joinpath('a_star_search').joinpath('assets').joinpath('test_graph.json'))

        graph: Graph = wrapper.make_graph()

        arad = DictNode(name='Arad')

        bucharest = DictNode(name='Bucharest')

        a_star = AStarSearch(graph)

        path: list[DictNode] = a_star.run(initial_node=arad, desired_node=bucharest)

        cities = [node.name for node in path]

        cost = sum(map(lambda i: graph.get_real_cost(path[i], path[i+1]), range(len(path)-1)))

        expected_cities = ['Arad', 'Sibiu', 'Rimnicu Vilcea', 'Pitesti', 'Bucharest']

        self.assertEqual(expected_cities, cities)
        self.assertEqual(418, cost)
