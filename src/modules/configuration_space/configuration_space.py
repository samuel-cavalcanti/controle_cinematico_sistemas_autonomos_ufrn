import numpy as np

from .convex_hull_jarvis import ConvexHULL


def make_configuration_space(robot_vertices: np.ndarray, obstacles_vertices: list[np.ndarray]) -> list[np.ndarray]:
    """
           Recebe os vértices do robô onde a origem do centro de coordenadas é o centro geométrico do polígonos convexo
           do robô, caso não esteja, o algoritmo não funciona. 

           Esse algoritmo parte que os pontos já estejam  ordenados da seguinte maneira circular:

            .(4)b-1   .(3)

        .(5)b           .(2)

            .(6)b+1    .(1)

    """

    """
        1. Pick a local coordinate system on A including an origin point. This will be the reference point on the robot.
        mudar o referencial dos vertices para o referencial do robô.
        No caso o referencial do robô é o centroide do seu poligono convexo que pode ser encontrado com a média dos pontos 
        no caso, o referencial do robô tem a mesma orientação a matrix homogenia ficaria assim:

        | 1 0 0 mean(x) |
        | 0 1 0 mean(y) |
        | 0 0 1  1      |
        ou seja é uma simples translação.
    """

    new_origin = np.array([
        robot_vertices[:, 0].mean(),
        robot_vertices[:, 1].mean(),
    ])

    """ 2. Reflect (flip) A about the origin of its local coordinate system (to get -A).

        para mudar o referencial do robô temos que translada-ló para sua origem
        e também temos que  refleti-lo, ou seja
        
        robot = , faz com que os vertices do robô fiquem na nova origem
        robot = -robot, reflete os vertices robô
        então robot = -(robot_vertices - new_origin)
        robot = -robot_vertices  + new_origin
    """

    robot = new_origin - robot_vertices

    """3. Attach -A at every obstacle_vertex of B to compute the vertices of the resulting shape B ⊕ -A.
        A ⊕ B = {a + b | a ∈; A, b ∈; B}
    """
    configuration_space_obstacles = [minkowski_sum(robot, obstacle_vertices) for obstacle_vertices in obstacles_vertices]

    """  4. Compute the convex hull of the set of the resulting vertices 
        Não precisamos de todos os vertices dos obstáculos para criar o seu
        polígono, na verdade precisamos os mais externos. Para obter os
        vertices mais externos, então usamos o algoritmo convex hull 
        https://www.geeksforgeeks.org/convex-hull-using-divide-and-conquer-algorithm/
    """

    return [convex_hull(obstacle) for obstacle in configuration_space_obstacles]


def convex_hull(vertices: np.ndarray) -> np.ndarray:
    return ConvexHULL(vertices).run()


def minkowski_sum(robot: np.ndarray, obstacle_vertices: np.ndarray) -> np.ndarray:
    """
    minkowski sum, é o conjunto resultante da seguite operação: 
    A ⊕ B = {a + b | a ∈; A, b ∈; B}
    onde no nosso caso A é o robô e B é obstáculo
    """
    configuration_space_vertices = list()

    for obstacle_vertex in obstacle_vertices:
        for robot_vertex in robot:
            configuration_space_vertices.append(robot_vertex + obstacle_vertex)


    return np.array(configuration_space_vertices)
