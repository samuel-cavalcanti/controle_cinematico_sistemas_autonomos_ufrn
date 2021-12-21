import numpy as np

""" https://www.geeksforgeeks.org/convex-hull-set-1-jarviss-algorithm-or-wrapping/
        https://en.wikipedia.org/wiki/Gift_wrapping_algorithm
"""


class ConvexHULL:
    __vertices: np.ndarray

    def __init__(self, vertices: np.ndarray):
        """Onde vertices é um vetor de vértices:
         vertices[0] = [x,y]

         vertices = [
             [x1,y1],
             [x2,y2].
             [x3,y3]
             ....
            ]
         """
        self.__vertices = vertices

    def run(self) -> np.ndarray:

        point_on_hull = self.__find_left_most_point()
        hull = list()
        while True:
            hull.append(point_on_hull)

            next_hull_point = self.__find_nex_hull_point(point_on_hull)

            if (next_hull_point == hull[0]).all():
                break

            point_on_hull = next_hull_point

        return np.array(hull)

    def __find_left_most_point(self) -> np.ndarray:
        """Encontrando o vértice mais a a esquerda do conjunto de vertices"""
        left_vertex = self.__vertices[0]

        for vertex in self.__vertices:
            if vertex[0] < left_vertex[0]:
                left_vertex = vertex
            elif vertex[0] == left_vertex[0]:
                if vertex[1] > left_vertex[1]:
                    left_vertex = vertex

        return left_vertex

    def __find_nex_hull_point(self, current_hull_point: np.ndarray) -> np.ndarray:

        current_next_point = self.__vertices[0]
        for vertex in self.__vertices:
            if (current_next_point == current_hull_point).all() or self.__is_counterclockwise(current_hull_point,
                                                                                              vertex,
                                                                                              current_next_point):
                current_next_point = vertex

        return current_next_point

    @staticmethod
    def __is_counterclockwise(current_hull_point: np.ndarray, vertex: np.ndarray,
                              current_next_point: np.ndarray) -> bool:
        '''
           To find orientation of ordered triplet (current_hull_point, vertex, current_next_point).
           The function returns following values
           value == 0 --> current_hull_point, vertex and current_next_point are collinear
           value > 0 --> Clockwise
           value < 0 --> Counterclockwise
        '''

        value = (vertex[1] - current_hull_point[1]) * (current_next_point[0] - vertex[0]) - \
                (vertex[0] - current_hull_point[0]) * (current_next_point[1] - vertex[1])

        if value == 0:
            return False
        elif value > 0:
            return False
        return True
