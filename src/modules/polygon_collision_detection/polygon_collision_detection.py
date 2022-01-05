from ..utils.polygon import Polygon

from .convex_polygons_collision_detection import ConvexPolygonsCollisionDetection
from .point_lies_on_polygon.point_lies_on_polygon import PointLiesOnPolygon

def check_detection_between_polygons(poly_a: Polygon, poly_b: Polygon) -> bool:
    """
        Verifica se um polígono 2D está dentro do outro ou se eles se tocam
        Retorna True caso se toquem ou está dentro do outro e False caso contrário
    """
    return ConvexPolygonsCollisionDetection(poly_a, poly_b).run()


def check_detection_between_polygon_and_point(poly: Polygon, point: tuple[float, float]) -> bool:
    """
        Verifica se um ponto (x,y) está de dentro de polígono
        Retorna True se o ponto pertence ao polígono e False caso contrário
     """

    PointLiesOnPolygon(poly,point).run()