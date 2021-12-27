

from ..utils.polygon import Polygon
import math

"""
    algoritmo retirado do geeksforgeeks
    https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/

"""


class PointLiesOnPolygon:

    __point: tuple[float, float]

    __polygon_vertices: list[tuple[float, float]]

    def __init__(self, poly: Polygon, point: tuple[float, float]) -> None:
        self.__point = point
        self.__polygon_vertices = [(vertex.position[0], vertex.position[1]) for vertex in poly.vertices]

    def run(self) -> bool:

        """"""
