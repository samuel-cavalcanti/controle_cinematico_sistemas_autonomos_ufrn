import json
import os
import sys
from pathlib import Path

import numpy as np

sys.path.append(os.getcwd())
from src.modules.utils import Polygon, Vertex
from src.modules.configuration_space import configuration_space
from matplotlib import pyplot


# from matplotlib.patches import Polygon as matplotPoly

def map_dict_to_polygon(poly_dict: dict) -> Polygon:
    vertices = [Vertex(**v) for v in poly_dict['vertices']]

    return Polygon(name=poly_dict['name'], vertices=vertices)


def load_json(path_to_file: Path) -> list[Polygon]:
    with open(path_to_file, 'r') as json_file:
        polygons = json.loads(json_file.read())

        return list(map(map_dict_to_polygon, polygons))


def polygon_2_numpy_array(polygon: Polygon) -> np.ndarray:
    return np.array([v.position for v in polygon.vertices])


def draw_vertices(vertices_positions: np.ndarray):
    pyplot.scatter(vertices_positions[:, 0], vertices_positions[:, 1])

    pyplot.scatter(vertices_positions[:, 0].mean(), vertices_positions[:, 1].mean())
    pyplot.fill(vertices_positions[:, 0], vertices_positions[:, 1])


def main():
    polygons = load_json(Path('output/obstacles_vertices.json'))
    robot = polygons[-1]
    robot_vertices_positions = polygon_2_numpy_array(robot)
    obstacles = [polygon_2_numpy_array(p) for p in polygons[:-1]]

    [draw_vertices(o) for o in obstacles]

    draw_vertices(robot_vertices_positions)

    width = np.max(robot_vertices_positions[:, 0]) - np.min(robot_vertices_positions[:, 0])
    height = np.max(robot_vertices_positions[:, 1]) - np.min(robot_vertices_positions[:, 1])
    """
            (p2) =(-width/2,height/2) .       .(p2) =(width/2,height/2)
            (p3) =(-width/2,-height/2).       .(p1) =(width/2,-height/2)
    """
    robot_vertices_positions = np.array(
        [
            [width / 2, -height / 2],
            [width / 2, height / 2],
            [-width / 2, height / 2],
            [-width / 2, -height / 2],
        ]
    )

    pyplot.draw()
    pyplot.savefig('output/work_space.pdf', dpi=1200)

    confi_obstacles_vetices = configuration_space.make_configuration_space(robot_vertices_positions, obstacles)

    pyplot.figure(2)

    [draw_vertices(sorting_vertices(np.array(o))) for o in confi_obstacles_vetices]

    pyplot.draw()
    pyplot.savefig('output/confi_space.pdf', dpi=1200)


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
