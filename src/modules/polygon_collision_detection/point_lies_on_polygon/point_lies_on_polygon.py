from ...utils.polygon import Polygon




Point = tuple[float, float]




class PointLiesOnPolygon:

    __point: Point

    __polygon_vertices: list[Point]

    def __init__(self, poly: Polygon, point: Point) -> None:
        self.__point = point
        self.__polygon_vertices = [(vertex.position[0], vertex.position[1]) for vertex in poly.vertices]

    

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
