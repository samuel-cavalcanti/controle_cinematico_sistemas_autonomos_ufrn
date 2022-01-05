from ...utils.polygon import Polygon

from dataclasses import dataclass


Point = tuple[float, float]


@dataclass
class IntersectionResult:
    is_intersect: bool
    is_horizontal_line: bool


class PointLiesOnPolygon:

    __point: Point

    __polygon_vertices: list[Point]

    def __init__(self, poly: Polygon, point: Point) -> None:
        self.__point = point
        self.__polygon_vertices = [(vertex.position[0], vertex.position[1]) for vertex in poly.vertices]

    def __check_intersection(self, point_a: Point, point_b: Point) -> IntersectionResult:
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

    def run(self) -> bool:
        """
        Esse algoritmo foi aprendido no geeksforgeeks
        https://www.geeksforgeeks.org/how-to-check-if-a-given-point-lies-inside-a-polygon/

        onde:
            1. desenha uma linha horizontal partindo do ponto  até infinito
            2. conta o número de interseções entre essa linha horizontal e os lados do poligono
            3. a partir das interseções é tomado a decisão se o ponto pertence ou não ao poligono
            tendo em vista os seguintes casos:


                -------------------
          o-----|-----------------|-------------->
                |                 |  o----------->
                |        o--------|-------------->
                -------------------

        Perceba que em um polígono convexo, se trassarmos uma reta horizontal a partir de um ponto

        caso a reta se intersecte com apenas 1 lado do polígono então ele está dentro.

        caso a reta não intersecte com nenhum lado, então ele está fora do polígono

                --------o------------------------> (caso especial 1)
                |                 |
                |                 |
                |                 |
            o-------------------------------------> (caso especial 2)


                                    (caso especial 2)
        caso a reta intersecte com mais de 2 lados do polígono então ele está fora do poligono


                                    (caso especial 1)
        caso a reta intersecte 2 lados, então, pode ser o caso que o ponto está fora do poligono
        ou pode ser o caso especial 1, então se o ponto for tiver colidido com uma reta horizontal logo,
        estamos falando do caso especial 1, portanto o ponto está dentro do poligono caso contrario está fora.
        """

        pass
