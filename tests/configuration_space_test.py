import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from numpy.core.fromnumeric import shape
from numpy.lib.function_base import angle
from numpy.lib.twodim_base import tri

sys.path.append(os.getcwd())


def normal_vector(initial_point: np.ndarray, final_point: np.ndarray) -> np.ndarray:

    vector = final_point - initial_point

    """ 
        é feita uma rotação de 90 graus com o vetor, que se traduz em
        x = -y
        y = x
    """
    return np.array([-vector[1], vector[0]])


def get_normal_vectors_from_convex_polygon(polygon_points: np.ndarray) -> np.ndarray:
    """
        Esse algoritmo parte que os pontos já estejam  ordenados de maneira circular:


            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """

    length = len(polygon_points)

    normal_vectors = [normal_vector(polygon_points[0], polygon_points[-1])]

    for index in range(length - 1):

        final_point = polygon_points[index]
        initial_point = polygon_points[index+1]

        normal = normal_vector(initial_point, final_point)

        normal_vectors.append(normal)

    return np.array(normal_vectors)


def type_a_colision_check(normal_vector: np.ndarray, polygon_points: np.ndarray):

    length = len(polygon_points)

    for i, _ in enumerate(polygon_points):

        w_1 = polygon_points[i - 1] - polygon_points[i]

        w_2 = polygon_points[(i + 1) % length] - polygon_points[i]

        inner_prodoct_w_1 = np.dot(normal_vector, w_1)

        inner_prodoct_w_2 = np.dot(normal_vector, w_2)


def draw_normals(polygon_points: np.ndarray, center: np.ndarray):
    normals = get_normal_vectors_from_convex_polygon(polygon_points)
    plt.scatter(polygon_points[:, 0], polygon_points[:, 1])

    for n in normals:
        mean_x = center[0]
        mean_y = center[1]
        plt.plot([mean_x, n[0] + mean_x], [mean_y, n[1] + mean_y])

    plt.draw()


def main():
    """
        Esse algoritmo parte que os pontos já estejam  ordenados de maneira circular:


            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """

    """
    
                    .(2)

            .(3)

                    .(1)
    """
    triangle = np.array([
        [2.5, 2.0],
        [2.5, 2.5],
        [2.3, 2.25],
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
    """ nesse teste, o triangulo é o nosso robô"""
    triangle_normals = get_normal_vectors_from_convex_polygon(triangle)

    rectangle_normals = get_normal_vectors_from_convex_polygon(rectangle)

    inverted_triangle_normals = -triangle_normals
    """
        pseudo codigo não funciona
    """
    """ ordenar por angulo, do menor angulo para o maior"""
    rectangle_normals.sort()

    """ ordenar por angulo, do menor angulo para o maior"""
    inverted_triangle_normals.sort()



    draw_normals(triangle, np.array([2.3 + 2/15, 2.25]))

    draw_normals(rectangle, np.array([1.6, 1.6]))

    draw_normals(triangle, np.array([0.0, 0.0]))

    draw_normals(rectangle, np.array([0.0, 0.0]))

    """1. fixar normais"""
    # normal_set = [-v_i for v_i in triangle ] + rectangle

    


    plt.show()


if __name__ == '__main__':
    main()



def gerando_espaco_de_trabalho():

    """
            tentando implementar o algoritmo do professor passou em aula
            Vídeo Espaço de Configuração -Parte 2 tempo: 11:06 
    """

    last_index_triangle = 0

    last_index_rectangle = 0


    current_normal_triangle_vector =  inverted_triangle_normals[last_index_triangle]

    current_normal_retangle_vector = rectangle_normals[last_index_rectangle]

    if angle(current_normal_triangle_vector) < angle(current_normal_retangle_vector):
        next_normal_triangle_vector = inverted_triangle_normals[last_index_triangle +1]
        # se a < b < c
        if angle(current_normal_triangle_vector)  < angle(current_normal_retangle_vector) < angle(next_normal_triangle_vector):
            """The vertex  is then generated"""
       
    
    else:# b < a < c
        next_normal_triangle_vector = inverted_triangle_normals[last_index_triangle +1]
        if  angle(current_normal_retangle_vector) < angle(current_normal_triangle_vector) < angle(next_normal_triangle_vector):
            """The vertex  is then generated"""
       
