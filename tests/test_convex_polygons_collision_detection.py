import unittest
import numpy as np

from src.modules.utils.polygon import Polygon, Vertex
from src.modules.utils.convex_polygons_collision_detection import ConvexPolygonsCollisionDetection


class ConvexPolygonsCollisionDetectionTestCase(unittest.TestCase):

    @staticmethod
    def __numpy_to_polygon(vertices: np.ndarray) -> Polygon:
        return Polygon('Test', vertices=[Vertex('Test', vertex) for vertex in vertices])

    def test_collision_detection(self):
        """test the separate axis theorem Collision detection"""


        """

                             .(2)


                .(3)    
                          .(1)
        """
        b = 0.2
        h = 0.5

        triangle_vertices = np.array([
            [b / 3, -h / 3],  # a_1
            [b / 3 + 0.1, 2 * h / 3 + 0.1],  # a_2
            [-2 * b / 3, -h / 3 + 0.2],  # a_3
        ])

        """
          .(3)              .(2)  [1.7, 1.7],



          .(4)              .(1)  [1.7, 1.5],
        """
        rectangle_vertices = np.array([
            [1.7, 1.5],
            [1.7, 1.7],
            [1.5, 1.7],
            [1.5, 1.5],
        ])

        """
          .(r_3)              .(r_2)

                    .(3)            .(2)        

          .(r_4)              .(r_1)

                    .(4)            .(1)
        """
        colision_rectangle_vertices = np.array([
            [1.8, 1.1],
            [1.8, 1.6],
            [1.6, 1.6],
            [1.6, 1.1],
        ])


        """
              .(r_3)              .(r_2)
         .(3)                                .(2)  [2.0, 1.65],

         .(4)                                .(1) [2.0, 1.6],
              .(r_4)              .(r_1)
        """

        another_colision_rectangle_vertices = np.array([
            [2.0, 1.6],
            [2.0, 1.65],
            [1.2, 1.65],
            [1.2, 1.6],
        ])

        colision_rectangle = self.__numpy_to_polygon(colision_rectangle_vertices)

        another_colision_rectangle = self.__numpy_to_polygon(another_colision_rectangle_vertices)

        rectangle = self.__numpy_to_polygon(rectangle_vertices)

        triangle = self.__numpy_to_polygon(triangle_vertices)

        collisions = [
            ConvexPolygonsCollisionDetection(triangle, rectangle).run(),
            ConvexPolygonsCollisionDetection(colision_rectangle, rectangle).run(),
            ConvexPolygonsCollisionDetection(colision_rectangle, triangle).run(),
            ConvexPolygonsCollisionDetection(another_colision_rectangle, rectangle).run(),
            ConvexPolygonsCollisionDetection(another_colision_rectangle, colision_rectangle).run()
        ]

        self.assertFalse(collisions[0], "esse Triangulo e retangulo não deveriam colidir")

        self.assertTrue(collisions[1], "esses retangulos deveriam colidir")

        self.assertFalse(collisions[2], "esse Triangulo e retangulo não deveriam colidir")

        self.assertTrue(collisions[3], "esses retangulos estão sobrepostos")

        self.assertTrue(collisions[4], "esses retangulos se tocam na face inferiror")
