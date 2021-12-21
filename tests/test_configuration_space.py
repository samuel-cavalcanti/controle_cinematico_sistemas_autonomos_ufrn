import unittest
from functools import reduce

import numpy as np

from src.modules.configuration_space import configuration_space
from src.modules.configuration_space.convex_hull_jarvis import ConvexHULL


class ConfigurationSpaceTestCase(unittest.TestCase):

    def test_convex_hull_jarvis_algorithm(self):
        """geeksforgeeks convex hull test"""
        vertices = np.array([
            [0, 3],
            [2, 2],
            [1, 1],
            [2, 1],
            [3, 0],
            [0, 0],
            [3, 3]
        ])

        expected_vertices = np.array([
            [0, 3],
            [0, 0],
            [3, 0],
            [3, 3]
        ])

        result_vertices = ConvexHULL(vertices).run()

        self.assert_vertices(expected_vertices, result_vertices)

    def test_make_configuration_space(self):

        """

                        .(2)


                .(3)    .(1)
        """
        b = 0.2
        h = 0.5

        triangle = np.array([
            [b / 3, -h / 3],  # a_1
            [b / 3 + 0.1, 2 * h / 3 + 0.1],  # a_2
            [-2 * b / 3, -h / 3 + 0.2],  # a_3
        ])

        """
          .(3)              .(2)



          .(4)              .(1)
        """
        rectangle = np.array([
            [1.7, 1.5],
            [1.7, 1.7],
            [1.5, 1.7],
            [1.5, 1.5],
        ])

        list_of_vertices = configuration_space.make_configuration_space(triangle, [rectangle])

        vertices = list_of_vertices[0]

        expected_vertices = np.array([
            rectangle[0] - triangle[2],  # b_1 - a_3

            rectangle[1] - triangle[2],  # b_2 - a_3
            rectangle[1] - triangle[0],  # b_2 - a_1

            rectangle[2] - triangle[0],  # b_3 - a_1

            rectangle[3] - triangle[0],  # b_4 - a_1

            rectangle[0] - triangle[1],  # b_1 - a_2
        ])

        self.assertFalse(self.__is_in_array(np.array([1, 2]), vertices),
                         msg="esse vertex não deveria existir na lista")

        self.assertFalse(self.__is_in_array(np.array([1.86666667, 1.83333333]), vertices),
                         msg="esse vertex não deveria existir na lista")

        self.assert_vertices(expected_vertices, vertices)

        self.assertEqual(len(vertices), 8,
                         msg="O número total de vertices deve ser igual a 8 onde b_3 - a_1 se repete 2 vezes")

        b_3_a_1 = rectangle[2] - triangle[0]

        self.assertEqual(reduce(self.__sum_true_booleans, vertices == b_3_a_1, 0), 2,
                         msg="O vertex b_3 - a_1 deve se repetir 2 vezes")

    @staticmethod
    def __sum_true_booleans(total: int, boolean_vector: np.ndarray):
        return total + 1 if boolean_vector.all() else total

    @staticmethod
    def __is_in_array(element, array: np.ndarray) -> bool:
        for value in array:
            if (value == element).all():
                return True
        return False

    def assert_vertices(self, expected_vertices: np.ndarray, vertices: np.ndarray):
        for index, expected_vertex in enumerate(expected_vertices):
            self.assertTrue(self.__is_in_array(expected_vertex, vertices),
                            msg=f"Foi calculado na mão esse exemplo e o vertex {expected_vertex} de index {index} deveria está em {vertices}")
