from __future__ import annotations
import os
import sys
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
sys.path.append(os.getcwd())

from configuration_space.configuration_space import get_normal_vectors_from_convex_polygon, make_configuration_space


def type_a_colision_check(normal_vector: np.ndarray, polygon_points: np.ndarray):

    length = len(polygon_points)

    for i, _ in enumerate(polygon_points):

        w_1 = polygon_points[i - 1] - polygon_points[i]

        w_2 = polygon_points[(i + 1) % length] - polygon_points[i]

        inner_prodoct_w_1 = np.dot(normal_vector, w_1)

        inner_prodoct_w_2 = np.dot(normal_vector, w_2)


def draw_normals(polygon_points: np.ndarray, center: np.ndarray):
    normals = get_normal_vectors_from_convex_polygon(polygon_points)

    for n in normals:
        mean_x = center[0]
        mean_y = center[1]
        plt.plot([mean_x, n[0] + mean_x], [mean_y, n[1] + mean_y])

    plt.draw()


def sort_vector_by_angle(vectors: np.ndarray) -> np.ndarray:

    def vector_angle(vector: np.ndarray) -> float:
        theta = np.arctan2(vector[1], vector[0])
        if theta >= 0:
            return theta
        else:
            return 2*np.pi + theta

    angles = np.array([vector_angle(v) for v in vectors])

    arg_sort = np.argsort(angles)

    return vectors[arg_sort]  # > vector_angle(vector_b)


def test_sort_vectors(triangle: np.ndarray, rectangle: np.ndarray):
    """ nesse teste, o triangulo é o nosso robô"""
    triangle_normals = get_normal_vectors_from_convex_polygon(triangle)

    rectangle_normals = get_normal_vectors_from_convex_polygon(rectangle)

    inverted_triangle_normals = -triangle_normals

    print('inverted_triangle_normals')

    sorted_inverted_triangle_normals = sort_vector_by_angle(inverted_triangle_normals)

    sorted_rectangle_normals = sort_vector_by_angle(rectangle_normals)

    for n in sorted_inverted_triangle_normals:
        theta = np.arctan2(n[1], n[0])
        theta_in_degree = np.rad2deg(theta)
        theta_in_degree = theta_in_degree if theta_in_degree >= 0 else 360 + theta_in_degree
        print(f'theta: {theta_in_degree  }')

    print('sorted_rectangle_normals')
    for n in sorted_rectangle_normals:
        theta = np.arctan2(n[1], n[0])
        theta_in_degree = np.rad2deg(theta)
        theta_in_degree = theta_in_degree if theta_in_degree >= 0 or theta_in_degree >= -0 else 360 + theta_in_degree
        print(f'theta: {theta_in_degree  }')


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

    # [2.5, 2.0],
    #     [2.5, 2.5],
    #     [2.3, 2.25],

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

    draw_normals(rectangle, np.array([1.6, 1.6]))

    draw_normals(triangle, np.array([0, 0]))

    list_of_vertices = make_configuration_space(triangle, [rectangle])
    
   
    vertices = np.array(list_of_vertices[0])

    plt.scatter(vertices[:, 0], vertices[:, 1])
    plt.scatter(rectangle[:, 0], rectangle[:, 1])
    plt.scatter(triangle[:, 0], triangle[:, 1])

    plt.show()


if __name__ == '__main__':
    main()
