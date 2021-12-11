from functools import reduce
import numpy as np
import os
import sys
sys.path.append(os.getcwd())

from configuration_space.configuration_space import make_configuration_space


def main():
    """
        Esse algoritmo parte que os pontos já estejam  ordenados de maneira circular:


            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """

    """
    
                    .(2)


            .(3)    .(1)
    """
    b = 0.2
    h = 0.5

    triangle = np.array([
        [b/3, -h/3],
        [b/3, 2*h/3],
        [-2*b/3, -h/3],
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

    list_of_vertices = make_configuration_space(triangle, [rectangle])
    vertices = list_of_vertices[0]

    expected_vertices = [
        rectangle[0] - triangle[2],  # b_1 - a_3

        rectangle[1] - triangle[2],  # b_2 - a_3
        rectangle[1] - triangle[0],  # b_2 - a_1

        rectangle[2] - triangle[0],  # b_3 - a_1

        rectangle[3] - triangle[0],  # b_4 - a_1

        rectangle[0] - triangle[1],  # b_1 - a_2
    ]

    def is_in_array(element, array: np.ndarray) -> bool:
        for value in array:
            if (value == element).all():
                return True
        return False

    assert is_in_array(np.array([1, 2]), vertices) == False, "esse vertice não deveria existir na lista"
    assert is_in_array(np.array([1.86666667, 1.83333333]), vertices) == False, "esse vertice não deveria existir na lista"

    for expected_vertice in expected_vertices:
        assert is_in_array(
            expected_vertice, vertices), f"Foi calculado na mão esse exemplo e o vertice {expected_vertice} deveria está em {vertices}"

    assert len(vertices) == 8, "O número total de vertices deve ser igual a 8 onde b_3 - a_1 se repete 2 vezes"

    b_3_a_1 = rectangle[2] - triangle[0]
    

    def sum_true_booleans(total: int, boolean_vector: np.ndarray):
        return total + 1 if boolean_vector.all() else total


    assert reduce(sum_true_booleans, vertices == b_3_a_1, 0) == 2, "O vertice b_3 - a_1 deve se repetir 2 vezes"


if __name__ == '__main__':
    main()
