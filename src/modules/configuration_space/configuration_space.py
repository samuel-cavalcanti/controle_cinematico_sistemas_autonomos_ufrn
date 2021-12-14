import numpy as np

from . import sorted_nodes_creator
from .find_obstacle_vertices_in_configuration_space import FindObstacleVerticesInConfigurationSpace
from .normal_vector_wrapper import NormalVectorWrapper


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

    normal_vectors = [normal_vector(initial_point=polygon_points[0], final_point=polygon_points[-1])]

    def get_normal_vector(index: int) -> np.ndarray:
        final_point = polygon_points[index]
        initial_point = polygon_points[index + 1]
        return normal_vector(initial_point, final_point)

    normal_vectors += [get_normal_vector(index) for index in range(length - 1)]

    return np.array(normal_vectors)


def make_configuration_space(robot_vertices: np.ndarray, obstacles_vertices: list[np.ndarray]) -> list[np.ndarray]:
    """
           Recebe os vértices do robô onde a origem do centro de coordenadas é o centro geométrico do polígonos convexo
           do robô, caso não esteja, o algoritmo não funciona. 

           Esse algoritmo parte que os pontos já estejam  ordenados da seguinte maneira circular:

            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """
    robot_normals = get_normal_vectors_from_convex_polygon(robot_vertices)

    """
            Um NormalVectorWrapper nada mais é um struct que encapsula os vetores normais com algumas informações
            adicionais que são utilizadas durante a execução do algoritmo de busca, busca essa que será a verificação
            se um vetor normal do robô está entre dois vetores normais dos obstáculos.
            Caso entre essas 3 normais, significa que deve-se ser gerado um vértice. Para gerar o vértice precisa
            dessas informações adicionais. Para dizer se o vetor normal é do robô ou do obstáculo, precisa das
            informações adicionais
            
            informações adicionais:
                o vértice que deve subtraído para obter o vértice no espaço de configuração 
                se o vetor normal é ou não do robô
                o próximo nó (essa informação só irá ser obtida ao final da criação da lista ordenada)

    """

    robot_nodes = [NormalVectorWrapper(is_robot_vector=True,
                                       next_node_index=None,
                                       normal_vec=normal,
                                       vertex=robot_vertices[index])
                   for index, normal in enumerate(-robot_normals)]

    def obstacles_vertices_to_configuration_space_vertices(obstacle_vertices: np.ndarray) -> np.ndarray:
        obstacle_normals = get_normal_vectors_from_convex_polygon(obstacle_vertices)

        obstacle_nodes = [NormalVectorWrapper(is_robot_vector=False,
                                              next_node_index=None,
                                              normal_vec=normal,
                                              vertex=obstacle_vertices[index])
                          for index, normal in enumerate(obstacle_normals)]

        sorted_nodes = sorted_nodes_creator.create_sorted_nodes(obstacle_nodes=obstacle_nodes,
                                                                robot_nodes=robot_nodes)

        return FindObstacleVerticesInConfigurationSpace().execute(sorted_nodes, obstacle_nodes)

    return [obstacles_vertices_to_configuration_space_vertices(vertices) for vertices in obstacles_vertices]

    """ ordenar por angulo, do menor angulo para o maior
         O(nlog(n))
         
         gerar indices O(n)

         busca linear em um anel, O(n)

         complexidade: O(nlog(n))         
    """
