
from __future__ import annotations
from typing import Optional
import numpy as np

from ..utils.polygon import Polygon


"""
    https://hackmd.io/@US4ofdv7Sq2GRdxti381_A/ryFmIZrsl?type=view
    algoritmo retirado do hackmd.oi
"""


class ConvexPolygonsCollisionDetection:
    """Algoritmo que detecta colisão entre 2 poligonos 2D"""

    __vertices_poly_a: np.ndarray
    __vertices_poly_b: np.ndarray

    def __init__(self, poly_a: Polygon, poly_b: Polygon) -> None:
        self.__vertices_poly_a = self.__polygon_to_np_array(poly_a)
        self.__vertices_poly_b = self.__polygon_to_np_array(poly_b)

    @staticmethod
    def __polygon_to_np_array(polygon: Polygon) -> np.ndarray:

        vertices = [vertex.position for vertex in polygon.vertices]

        return np.array(vertices)

    def run(self) -> bool:
        """Return true if collision is detected, or false is not detected"""

        edges = self.__orthogonal_edges_of(self.__vertices_poly_a)
        edges += self.__orthogonal_edges_of(self.__vertices_poly_b)

        push_vectors = self.__push_vectors_of(edges)

        return len(push_vectors) >= 1

    def __orthogonal_edges_of(self, vertices: np.ndarray) -> list[np.ndarray]:

        number_of_vertices = len(vertices)
        edges = list()

        for i in range(number_of_vertices):
            edge = vertices[(i + 1) % number_of_vertices] - vertices[i]
            edges.append(self.__orthogonal(edge))

        return edges

    @staticmethod
    def __orthogonal(edge: np.ndarray) -> np.ndarray:
        return np.array([-edge[1], edge[0]])

    def __push_vectors_of(self, edges: list[np.ndarray]) -> list[np.ndarray]:
        push_vectors = list()
        for e in edges:
            push_vector = self.__is_separating_axis(e)
            if push_vector is not None:
                push_vectors.append(push_vector)

        return push_vectors

    def __is_separating_axis(self, edge: np.ndarray) -> Optional[np.ndarray]:

        min_poly_a, max_poly_a = self.__find_min_and_max_of_projection(edge, self.__vertices_poly_a)

        min_poly_b, max_poly_b = self.__find_min_and_max_of_projection(edge, self.__vertices_poly_b)

        if max_poly_a >= min_poly_b and max_poly_b >= min_poly_a:
            d = min(max_poly_b - min_poly_a, max_poly_a - min_poly_b)/np.dot(edge, edge)

            return d*edge

        return None

    @staticmethod
    def __find_min_and_max_of_projection(edge: np.ndarray, vertices: np.ndarray) -> tuple[float, float]:
        min_projection, max_projection = float('+inf'), float('-inf')

        for vertex in vertices:
            projection = np.dot(vertex, edge)
            min_projection = min(min_projection, projection)
            max_projection = max(max_projection, projection)

        return min_projection, max_projection
