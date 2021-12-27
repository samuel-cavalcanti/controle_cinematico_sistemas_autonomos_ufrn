import os
import sys
sys.path.append(os.getcwd())

from src.modules.path_and_trajectory_planning import path_by_polynomials
from src.modules.configuration_space import configuration_space
from src.modules.utils.plotter_2d import Plotter2D
from src.modules.utils.convex_polygons_collision_detection import ConvexPolygonsCollisionDetection
import json
from pathlib import Path
import numpy as np
from src.modules.utils import Polygon, Position



"""Cuidado com o autoformat do arquivo, pode quebrar o import: from src.modules.configuration_space import configuration_space"""


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


    x_space = np.linspace(-2.1850e+00, 2.1850e+00, 50)
    y_space = np.linspace(-2.1850e+00, 2.1850e+00, 50)

    xx, yy = np.meshgrid(x_space, y_space)
    grid_points = list()
    
    # collision_detection = ConvexPolygonsCollisionDetection.from_numpy()

    for x, y in zip(xx, yy):
        for x_value, y_value in zip(x, y):

            grid_points.append([x_value, y_value])

    grid_points = np.array(grid_points)

    plotter = Plotter2D()


    plotter.draw_points(work_space_limits)
    plotter.draw_polygons(obstacles + [robot_vertices])
    plotter.draw_lines(path_points)

    plotter.save_figure(Path('output').joinpath('work_space.pdf'))

    plotter.next_figure()

    # plotter.view_grid(True)
    plotter.draw_points(grid_points)

    plotter.draw_points(work_space_limits)
    plotter.draw_polygons(obstacles_in_c_space)

    plotter.draw_points(np.array([[
        robot_vertices[:, 0].mean(),
        robot_vertices[:, 1].mean(),
    ]]))

    plotter.draw_lines(path_points)

    plotter.save_figure(Path('output').joinpath('conf_space.pdf'))

    plotter.show()


if __name__ == '__main__':
    # plot_test_case_data()
    plot_simulation_data()
