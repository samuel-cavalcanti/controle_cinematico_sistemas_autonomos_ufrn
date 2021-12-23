from matplotlib import pyplot

import os
import sys
sys.path.append(os.getcwd())

from src.modules.path_and_trajectory_planning import path_by_polynomials
from src.modules.configuration_space import configuration_space
from src.modules.utils import Polygon, Vertex, Position
import json
from pathlib import Path
import numpy as np




"""Cuidado com o autoformat do arquivo, pode quebrar o import: from src.modules.configuration_space import configuration_space"""


def map_dict_to_polygon(poly_dict: dict) -> Polygon:
    vertices = [Vertex(**v) for v in poly_dict['vertices']]

    return Polygon(name=poly_dict['name'], vertices=vertices)


def polygon_2_numpy_array(polygon: Polygon) -> np.ndarray:
    return np.array([v.position for v in polygon.vertices])


def draw_polygon(vertices_positions: np.ndarray):
    pyplot.fill(vertices_positions[:, 0], vertices_positions[:, 1])
    pyplot.scatter(vertices_positions[:, 0].mean(), vertices_positions[:, 1].mean())


def draw_points(vertices_positions: np.ndarray):
    pyplot.scatter(vertices_positions[:, 0], vertices_positions[:, 1])
    pyplot.draw()


def draw_lines(lines: np.ndarray):
    pyplot.plot(lines[:, 0], lines[:, 1])
    pyplot.draw()


def draw_polygons(polygon: list[np.ndarray]):
    [draw_polygon(sorting_vertices(p)) for p in polygon]
    pyplot.draw()


def sorting_vertices(vertices: np.ndarray):
    """
    Dado um polígono convexo você pode organizar os vertices
    pela fase entre o ponto médio do polígono com seus vértices
    """
    mean_x = np.mean(vertices[:, 0])
    mean_y = np.mean(vertices[:, 1])
    mean_point = np.array([mean_x, mean_y])

    def sort_by_angle(vertex: np.ndarray) -> float:
        vector = vertex - mean_point
        theta = np.arctan2(vector[1], vector[0])
        return theta if theta >= 0 else 2 * np.pi + theta

    return np.array(sorted(vertices, key=sort_by_angle))


def load_json(path_to_file: Path) -> list[Polygon]:
    with open(path_to_file, 'r') as json_file:
        polygons = json.loads(json_file.read())

        return list(map(map_dict_to_polygon, polygons))


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
   
    pyplot.grid()

    draw_polygons([triangle, rectangle])

    next_figure()

    pyplot.grid()
    draw_polygons(configuration_space.make_configuration_space(robot_vertices=triangle, obstacles_vertices=[rectangle]))

    pyplot.show()

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
        [-2.1824e+00, 2.1908e+00],
        [2.1472e+00, 2.1908e+00],
        [-2.1472e+00, -2.1908e+00],
        [2.1472e+00, -2.1908e+00]
    ])

    desired_pos = np.array([-3.8350e-01, +1.3220e+00])
    initial_pos = np.array([-1.2705e+00, +4.7000e-02])

    path_points = find_polynomial_path(initial_pos, final_pos=desired_pos)

    pyplot.grid()

    draw_points(work_space_limits)
    draw_polygons(obstacles + [robot_vertices])
    draw_lines(path_points)

    save_figure(Path('output').joinpath('work_space.pdf'))

    next_figure()

    pyplot.grid()
    draw_points(work_space_limits)
    draw_polygons(configuration_space.make_configuration_space(robot_vertices, obstacles))

    draw_points(np.array([[
        robot_vertices[:, 0].mean(),
        robot_vertices[:, 1].mean(),
    ]]))

    draw_lines(path_points)

    save_figure(Path('output').joinpath('conf_space.pdf'))

    pyplot.show()



def next_figure():
    pyplot.figure(pyplot.gcf().number + 1)

def save_figure(path:Path):
    pyplot.savefig(str(path), dpi=1200)

if __name__ == '__main__':
    # plot_test_case_data()
    plot_simulation_data()
