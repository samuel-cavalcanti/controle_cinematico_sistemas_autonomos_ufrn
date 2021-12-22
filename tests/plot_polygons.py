import os
import sys
sys.path.append(os.getcwd())

"""Cuidado com o autoformat do arquivo, pode quebrar o import: from src.modules.configuration_space import configuration_space"""

from matplotlib import pyplot
from src.modules.configuration_space import configuration_space
from src.modules.utils import Polygon, Vertex
import dataclasses
import json
from pathlib import Path
import numpy as np



def map_dict_to_polygon(poly_dict: dict) -> Polygon:
    vertices = [Vertex(**v) for v in poly_dict['vertices']]

    return Polygon(name=poly_dict['name'], vertices=vertices)


def load_json(path_to_file: Path) -> list[Polygon]:
    with open(path_to_file, 'r') as json_file:
        polygons = json.loads(json_file.read())

        return list(map(map_dict_to_polygon, polygons))


def polygon_2_numpy_array(polygon: Polygon) -> np.ndarray:
    return np.array([v.position for v in polygon.vertices])


def draw_polygon(vertices_positions: np.ndarray):
    pyplot.fill(vertices_positions[:, 0], vertices_positions[:, 1])
    pyplot.scatter(vertices_positions[:, 0].mean(), vertices_positions[:, 1].mean())


def draw_vertices(vertices_positions: np.ndarray):
    pyplot.scatter(vertices_positions[:, 0], vertices_positions[:, 1])
    pyplot.draw()


def draw_polygons(polygon: list[np.ndarray]):
    [draw_polygon(sorting_vertices(p)) for p in polygon]
    pyplot.draw()


def main():
    polygons = load_json(Path('output/obstacles_vertices.json'))

    robot = polygons[-1]
    robot_vertices = polygon_2_numpy_array(robot)
    obstacles = [polygon_2_numpy_array(p) for p in polygons[:-1]]

    draw_mapping(robot_vertices, obstacles)

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

    obstacles = [rectangle]
    robot_vertices = triangle

    draw_mapping(robot_vertices, obstacles)

    pyplot.show()


def draw_mapping(robot_vertices: np.ndarray, obstacles: np.ndarray):
    obstacles_on_configuration_space = configuration_space.make_configuration_space(robot_vertices, obstacles)

    draw_work_space_and_conf_space(robot_vertices, obstacles, obstacles_on_configuration_space)

    draw_vertices(np.array([[robot_vertices[:, 0].mean(), robot_vertices[:, 1].mean()]]))

    pyplot.figure(pyplot.gcf().number + 1)


def draw_work_space_and_conf_space(robot_vertices: np.ndarray, obstacles: np.ndarray, obstacles_on_configuration_space: np.ndarray):
    draw_polygons(obstacles)
    draw_polygon(robot_vertices)
    # pyplot.savefig('output/work_space.pdf', dpi=1200)

    pyplot.figure(pyplot.gcf().number + 1)

    draw_polygons(obstacles_on_configuration_space)
    # pyplot.savefig('output/conf_space.pdf', dpi=1200)


def vertices_to_polygon(vertices: np.ndarray, polygon_name: str) -> Polygon:
    return Polygon(polygon_name, np_array_to_vertex(vertices, polygon_name))


def np_array_to_vertex(vertices: np.ndarray, polygon_name: str) -> list[Vertex]:
    list_of_vertices = list()
    for index, vertex_array in enumerate(vertices):
        list_of_vertices.append(Vertex(name=f"{polygon_name}_P{index}", position=vertex_array.tolist()))

    return list_of_vertices


def to_json(obstacles: list[Polygon], path_file: Path):
    dict_obstacles: list[dict] = [dataclasses.asdict(o) for o in obstacles]

    with open(path_file, 'w') as json_file:
        json_file.write(json.dumps(dict_obstacles))


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


if __name__ == '__main__':
    main()
