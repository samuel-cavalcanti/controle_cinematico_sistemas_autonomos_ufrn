from ...utils.polygon import Polygon, Vertex

from .check_intersection import CheckInterSection


Point = tuple[float, float]


class PointLiesOnPolygon:

    __checker: CheckInterSection
    __point: Point

    vertices: list[Vertex]

    def __init__(self, poly: Polygon, point: Point) -> None:
        self.__point = point
        self.__checker = CheckInterSection(point)
        self.vertices = poly.vertices

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
        caso a reta horizontal esteja em "cima" de um dos lados do poligono, mas esteja fora dos limites desse lado
        então o ponto está fora.  


                                    (caso especial 1)
        caso a reta horizontal esteja em "cima" de um dos lados do poligono, mas o ponto está entre os limites desse lado
        então, o ponto está dentro do poligono.

        Perceba que:
         se a reta passar por 0 lados então, não pertence ao poligono
         se a reta passar por 1 lado  então, pertence ao poligono
         se a reta passar por 2 lados então, não pertence ao poligono

         então, dado um lado l, se l % 2 == 1, implica que o ponto pertence ao poligono.

         caso a reta passar por mais que 3 lados, então está em um dos casos especiais, ou seja,
         verifica-se quando ocorre a interceção especial e verifica os limites.


        """

        intersection_counter = 0
        number_of_vertices = len(self.vertices)

        for i in range(number_of_vertices):
            point_a = tuple(self.vertices[i].position)
            point_b = tuple(self.vertices[(i+1) % number_of_vertices].position)
            edge = (point_a, point_b)
            result = self.__checker.check(edge)
            if result.is_intersect:
                if result.is_horizontal_line:
                    return self.__on_segment(edge)

                intersection_counter += 1

        return intersection_counter % 2 == 1

    def __on_segment(self, edge: tuple[Point, Point]) -> bool:
        point_a = edge[0]
        point_b = edge[1]

        if point_a[0] > point_b[0]:
            x_max = point_a[0]
            x_min = point_b[0]
        else:
            x_max = point_b[0]
            x_min = point_a[0]

        return x_min <= self.__point[0] <= x_max
