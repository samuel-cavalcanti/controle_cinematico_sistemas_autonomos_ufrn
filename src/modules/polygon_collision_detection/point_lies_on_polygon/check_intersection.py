
from .intersection_result import IntersectionResult


Point = tuple[float, float]
Line = tuple[Point, Point]


class CheckInterSection:
    """
        Dado um ponto, cria-se uma reta horizontal a partir desse ponto. Na função check, verifica-se
        se essa reta cruza ou não uma outra reta dada
    """

    __point: Point

    def __init__(self, point: Point) -> None:
        self.__point = point

    def check(self, line: Line):

        point_a = line[0]
        point_b = line[1]

        """
            equação geral da reta ax + dy +c = 0,
            onde a = (y_a - y_b)
                 d = (x_b - x_a)
                 c = x_a*y_b - x_b*y_a

        """
        a = point_a[1] - point_b[1]
        d = point_b[0] - point_a[0]
        c = point_a[0]*point_b[1] - point_b[0]*point_a[1]

        if d == 0:
            return IntersectionResult(is_intersect=self.__check_intersection_case_2(x_1=point_a[0]), is_horizontal_line=False)

        if a == 0:
            return IntersectionResult(is_intersect=self.__check_intersection_case_3(x_1=point_a[0], x_2=point_b[0], y_1=point_a[1]), is_horizontal_line=True)

        return IntersectionResult(is_intersect=self.__check_intersection_case_1(m=-a/d, b=-c/d), is_horizontal_line=False)

        pass

    def __check_intersection_case_1(self, m: float, b: float) -> bool:
        """
                        y
                         |   (ax+b)
                         |         /
                         |        /
                     y_0 |       /|   o-------------------(essa reta parde de (x_0,y_0),vai até infinito em x, ou seja, (inf,y_0))
                         |      / |   |
                          ----------------------------->
                                 x_1   x_0             x

                                se x_0 > x_1  então uma reta a partir do x_o não intersecta
                                se x_0 == x_1 então ele intersecta em  x_0, ou x_1
                                se x_0 < x_1 então ele interceta em algum ponto após x_0
        """

        x_1 = (self.__point[1] - b)/m

        return self.__point[0] <= x_1

    def __check_intersection_case_2(self, x_1: float) -> bool:
        """
            nesse caso a reta, é uma reta vertical ou seja:

           y
            |         |
            |         |
            |         |     o--------->
            |         |     |
            --------------------------->
                      x_1  x_0         x

                    se  x_0 >  x_1,  então uma reta a partir do x_o não intersecta
                    se  x_0 <= x_1,  então ele intersecta
        """

        return self.__point[0] <= x_1

    def __check_intersection_case_3(self, x_1: float, x_2: float, y_1: float) -> bool:
        """
            Nesse caso a reta é uma reta horizontal ou seja:

           y
            |
       y_1  |   -----------o----------
            |                    
            |                    
            |                       
            --------------------------------------->
               x_1         x_0       x_2             x

            se  o ponto "o", estiver o y = y_1 e se tiver o x, tal que, x_1 <= x <= x_2
            então, o ponto intersecta
        """

        return self.__point[1] == y_1 and x_1 <= self.__point[0] <= x_2
