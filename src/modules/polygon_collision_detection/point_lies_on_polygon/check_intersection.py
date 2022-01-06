
from .intersection_result import IntersectionResult


# Point = tuple[float, float]
# Line = tuple[Point, Point]


# class CheckInterSection:
#     """
#         Dado um ponto, cria-se uma reta horizontal a partir desse ponto. Na função check, verifica-se
#         se essa reta cruza ou não uma outra reta dada
#     """

#     __point: Point

#     def __init__(self, point: Point) -> None:
#         self.__point = point

#     def check(self, line: Line):

#         point_a = line[0]
#         point_b = line[1]

#         """
#             equação geral da reta ax + dy +c = 0,
#             onde a = (y_a - y_b)
#                  d = (x_b - x_a)
#                  c = x_a*y_b - x_b*y_a

#         """
#         a = point_a[1] - point_b[1]
#         d = point_b[0] - point_a[0]
#         c = point_a[0]*point_b[1] - point_b[0]*point_a[1]

#         if d == 0:
#             if point_a[1] > point_b[1]:
#                 y_max = point_a[1]
#                 y_min = point_b[1]
#             else:
#                 y_max = point_b[1]
#                 y_min = point_a[1]

#             return IntersectionResult(is_intersect=self.__check_intersection_case_2(x_1=point_a[0], y_min=y_min, y_max=y_max), is_horizontal_line=False)

#         if a == 0:
#             x_max = point_a[0] if point_a[0] > point_b[0] else point_b[0]
#             return IntersectionResult(is_intersect=self.__check_intersection_case_3(x_max=x_max, y_1=point_a[1]), is_horizontal_line=True)

#         return IntersectionResult(is_intersect=self.__check_intersection_case_1(m=-a/d, b=-c/d), is_horizontal_line=False)

#         pass

#     def __check_intersection_case_1(self, m: float, b: float) -> bool:
#         """
#                         y
#                          |   (ax+b)
#                          |         /
#                          |        /
#                      y_0 |       /|   o-------------------(essa reta parde de (x_0,y_0),vai até infinito em x, ou seja, (inf,y_0))
#                          |      / |   |
#                           ----------------------------->
#                                  x_1   x_0             x

#                                 se x_0 > x_1  então uma reta a partir do x_o não intersecta
#                                 se x_0 == x_1 então ele intersecta em  x_0, ou x_1
#                                 se x_0 < x_1 então ele interceta em algum ponto após x_0
#         """

#         x_1 = (self.__point[1] - b)/m

#         return self.__point[0] <= x_1

#     def __check_intersection_case_2(self, x_1: float, y_min: float, y_max: float) -> bool:
#         """
#             nesse caso a reta, é uma reta vertical ou seja:
#            y
#             |
#       y_max |
#             |         |
#             |         |
#         y_0 |         |     o--------->
#       y_min |         |     |
#             |               |
#             --------------------------->
#                       x_1  x_0         x

#                     se y_min <= y_0 <= y_max então:
#                         se  x_0 >  x_1,  então uma reta a partir do x_o não intersecta
#                         se  x_0 <= x_1,  então ele intersecta
#         """

#         return y_min <= self.__point[1] <= y_max and self.__point[0] <= x_1

#     def __check_intersection_case_3(self,  x_max: float, y_1: float) -> bool:
#         """
#             Nesse caso a reta é uma reta horizontal ou seja:

#            y
#             |
#        y_1  |   -----------o---------------->
#             |
#             |
#             |
#             --------------------------------------->
#                x_1         x_0       x_2             x

#             se  o ponto "o", estiver o y = y_1 e se tiver o x, tal que, x <= x_2
#             então, o ponto intersecta
#         """

#         return self.__point[1] == y_1 and self.__point[0] <= x_max


# To find orientation of ordered triplet (p, q, r).
# The function returns following values
# 0 --> p, q and r are collinear
# 1 --> Clockwise
# 2 --> Counterclockwise
def orientation(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> int:

    val = (((q[1] - p[1]) *
            (r[0] - q[0])) -
           ((q[0] - p[0]) *
            (r[1] - q[1])))

    if val == 0:
        return 0
    if val > 0:
        return 1  # Collinear
    else:
        return 2  # Clock or counterclock


def do_intersect(current_vertice: tuple[float, float], next_vertice: tuple[float, float], point: tuple[float, float], extreme: tuple[float, float]):

    # Find the four orientations needed for
    # general and special cases
    o1 = orientation(current_vertice, next_vertice, point)
    o2 = orientation(current_vertice, next_vertice, extreme)
    o3 = orientation(point, extreme, current_vertice)
    o4 = orientation(point, extreme, next_vertice)

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases
    # p1, q1 and p2 are collinear and
    # p2 lies on segment p1q1
    if (o1 == 0) and (on_segment(current_vertice, point, next_vertice)):
        return True

    # p1, q1 and p2 are collinear and
    # q2 lies on segment p1q1
    if (o2 == 0) and (on_segment(current_vertice, extreme, next_vertice)):
        return True

    # p2, q2 and p1 are collinear and
    # p1 lies on segment p2q2
    if (o3 == 0) and (on_segment(point, current_vertice, extreme)):
        return True

    # p2, q2 and q1 are collinear and
    # q1 lies on segment p2q2
    if (o4 == 0) and (on_segment(point, next_vertice, extreme)):
        return True

    return False


def on_segment(p: tuple[float, float], q: tuple[float, float], r: tuple[float, float]) -> bool:

    if ((q[0] <= max(p[0], r[0])) &
        (q[0] >= min(p[0], r[0])) &
        (q[1] <= max(p[1], r[1])) &
            (q[1] >= min(p[1], r[1]))):
        return True

    return False
