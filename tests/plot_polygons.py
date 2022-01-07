import os
import sys


try:
    from src.modules.path_and_trajectory_planning.graph_algorithms.mesh_grid_graph import MeshGridGraph, MeshNode
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from src.modules.path_and_trajectory_planning.graph_algorithms.mesh_grid_graph import MeshGridGraph, MeshNode


from src.modules.path_and_trajectory_planning.graph_algorithms.a_star_search import AStarSearch
from src.modules.polygon_collision_detection import polygon_collision_detection
from src.modules.utils.plotter_2d import Plotter2D, RGB
from src.modules.configuration_space import configuration_space
from src.modules.path_and_trajectory_planning import path_by_polynomials
from src.modules.utils.polygon import Polygon, Vertex
from src.modules.utils import Polygon, Position, sorting_vertices_of_convex_polygon
import json
from pathlib import Path
import numpy as np


def polygon_2_numpy_array(polygon: Polygon) -> np.ndarray:
    return np.array([v.position for v in polygon.vertices])


def load_json(path_to_file: Path) -> list[Polygon]:
    with open(path_to_file, 'r') as json_file:
        polygons = json.loads(json_file.read())

        return list(map(Polygon.from_dict, polygons))


def find_polynomial_path(initial_pos: np.ndarray, final_pos: np.ndarray) -> np.ndarray:
    init = Position(x=initial_pos[0], y=initial_pos[1], theta_in_rads=0)
    final = Position(x=final_pos[0], y=final_pos[1], theta_in_rads=np.pi/2)

    x_coefficients, y_coefficients = path_by_polynomials.find_coefficients(init, final)
    p_x, p_y, _ = path_by_polynomials.create_path_functions(x_coefficients=x_coefficients,
                                                            y_coefficients=y_coefficients)

    lamp = np.arange(0.0, 1.0, 0.001)

    sample_x = p_x(lamp)
    sample_y = p_y(lamp)

    return np.array([[x, y] for x, y in zip(sample_x, sample_y)])


def make_grid(limit_x: tuple[float, float], limit_y: tuple[float, float], obstacles: list[np.ndarray]) -> np.ndarray:
    x_space = np.linspace(limit_x[0], limit_x[1], 50)
    y_space = np.linspace(limit_y[0], limit_y[1], 50)

    xx, yy = np.meshgrid(x_space, y_space)

    grid_points = list()

    for x, y in zip(xx, yy):
        for x_value, y_value in zip(x, y):

            if collided_with_polygons(point=(x_value, y_value), obstacles=obstacles):
                grid_points.append([float('inf'), float('inf')])
            else:
                grid_points.append([x_value, y_value])

    grid_points = np.array(grid_points)

    print('grid_points shape: ', grid_points.shape)

    return grid_points.reshape((len(x_space), len(y_space), -1))


def collided_with_polygons(point: tuple[float, float], obstacles: list[np.ndarray]) -> bool:

    for obstacle in obstacles:
        sorted_vertices = sorting_vertices_of_convex_polygon(obstacle)
        polygon = numpy_to_polygon(sorted_vertices)
        if polygon_collision_detection.check_detection_between_polygon_and_point(point=point, poly=polygon):
            return True

    return False


def numpy_to_polygon(vertices: np.ndarray) -> Polygon:

    vertices = [Vertex('Test', position=np.round(vertex, decimals=2).tolist()) for vertex in vertices]
    return Polygon(name='Test', vertices=vertices)


def plot_test_case_data():
    """
        Robot Motion Planning -Jean Claude Latombe example

        inspirado no obstáculo exemplo na página 123
        Capítulo 3: Obstáculos no espaço de configuração
        Figura 9
    """

    b = 0.2
    h = 0.5

    triangle = np.array([
        [b / 3, -h / 3],  # a_1
        [b / 3 + 0.1, 2 * h / 3 + 0.1],  # a_2
        [-2 * b / 3, -h / 3 + 0.2],  # a_3
    ])

    rectangle = np.array([
        [1.7, 1.5],
        [1.7, 1.7],
        [1.5, 1.7],
        [1.5, 1.5],
    ])

    plotter = Plotter2D()

    plotter.view_grid(True)

    plotter.draw_polygons([triangle, rectangle])
    plotter.next_figure()

    plotter.view_grid(True)

    plotter.draw_polygons(configuration_space.make_configuration_space(robot_vertices=triangle, obstacles_vertices=[rectangle]))

    plotter.show()


def plot_simulation_data():
    """
        Após a coleta dos vertices do simulador foi gerado um gráfico
        do seu espaço de configuração e de uma tentativa de gerar um caminho
    """
    polygons = load_json(Path('output').joinpath('obstacles_vertices.json'))

    robot = polygons[-1]
    robot_vertices = polygon_2_numpy_array(robot)
    obstacles = [polygon_2_numpy_array(p) for p in polygons[:-1]]

    work_space_limits = np.array([
        [-2.1850e+00, 2.2506e+00],
        [2.1850e+00, 2.2506e+00],
        [-2.1850e+00, -2.2506e+00],
        [2.1850e+00, -2.2506e+00]
    ])

    desired_pos = np.array([-3.8350e-01, +1.3220e+00])
    initial_pos = np.array([-1.2705e+00, +4.7000e-02])

    path_points = find_polynomial_path(initial_pos, final_pos=desired_pos)

    obstacles_in_c_space = configuration_space.make_configuration_space(robot_vertices, obstacles)

    limit_x = (-2.1850e+00, 2.1850e+00)
    limit_y = (-2.2506e+00, 2.2506e+00)

    grid = make_grid(limit_x, limit_y, obstacles_in_c_space)

    graph = MeshGridGraph(grid)

    start = MeshNode(x_index=10, y_index=25)
    goal = MeshNode(x_index=20, y_index=39)

    graph.set_goal(goal)

    a_star = AStarSearch(graph)

    paths = a_star.run(initial_node=start, desired_node=goal)

    def mesh_node_to_point(node: MeshNode) -> np.ndarray:
        return grid[node.y_index, node.x_index]

    a_star_path_points = np.array([mesh_node_to_point(node) for node in paths])

    reshaped_grid = grid.reshape(-1, 2)

    plotter = Plotter2D()

    plotter.draw_points(work_space_limits)
    plotter.draw_points(reshaped_grid, color=RGB(r=184, g=184, b=184))
    plotter.draw_polygons(obstacles + [robot_vertices])
    plotter.draw_lines(path_points)

    plotter.draw_lines(a_star_path_points)

    plotter.save_figure(Path('output').joinpath('work_space_with_graph.pdf'))

    plotter.next_figure()

    plotter.draw_points(work_space_limits)
    plotter.draw_polygons(obstacles_in_c_space)
    plotter.draw_points(reshaped_grid, color=RGB(r=184, g=184, b=184))

    plotter.draw_points(np.array([[
        robot_vertices[:, 0].mean(),
        robot_vertices[:, 1].mean(),
    ]]))

    plotter.draw_lines(path_points)
    plotter.draw_lines(a_star_path_points)

    plotter.save_figure(Path('output').joinpath('conf_space_with_graph.pdf'))

    plotter.show()


if __name__ == '__main__':
    # plot_test_case_data()
    plot_simulation_data()
