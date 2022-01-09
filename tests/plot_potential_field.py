import os
import json
import sys

import numpy as np
from pathlib import Path


try:
    from src.modules.utils.grid.grid_limits import GridLimits
except ModuleNotFoundError:
    sys.path.append(os.getcwd())
    from src.modules.utils.grid.grid_limits import GridLimits

from dataclasses import dataclass
from src.modules.utils.plotter_2d import RGB, Plotter2D
from src.modules.path_and_trajectory_planning.potential_field.potential_field_planning import PotentialFieldPlanning
from src.modules.path_and_trajectory_planning.potential_field.potential_field_calculator import PotentialFieldCalculator
from src.modules.path_and_trajectory_planning.graph_algorithms.potential_field_a_star_parameter import PotencialFieldAStarParameter
from src.modules.path_and_trajectory_planning.graph_algorithms.mesh_grid_graph import MeshGridGraph, MeshNode
from src.modules.path_and_trajectory_planning.graph_algorithms.a_star_search import AStarSearch
from src.modules.configuration_space import configuration_space
from src.modules.utils.grid import PotentialFielGrid
from src.modules.utils.polygon import Polygon, Vertex


@dataclass
class Position:
    x: float
    y: float


# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
AREA_WIDTH = 30.0  # potential area width [m]
# the number of previous positions used to check oscillations
OSCILLATIONS_DETECTION_LENGTH = 3


def calc_potential_field(goal: Position, obstacles_positions_x: list[float], obstacles_positions_y: list[float], resolution_grid: float, robot_radius: float, start: Position) -> tuple[np.ndarray, GridLimits]:

    x_min = min(min(obstacles_positions_x), start.x,
                goal.x) - AREA_WIDTH / 2.0
    y_min = min(min(obstacles_positions_y), start.y,
                goal.y) - AREA_WIDTH / 2.0
    x_max = max(max(obstacles_positions_x), start.x,
                goal.x) + AREA_WIDTH / 2.0
    y_max = max(max(obstacles_positions_y), start.y,
                goal.y) + AREA_WIDTH / 2.0
    grid_width_x = int(round((x_max - x_min) / resolution_grid))
    grid_width_y = int(round((y_max - y_min) / resolution_grid))

    print(f'grid size: {grid_width_x} ,{grid_width_y}')
    # calc each potential
    potential_field = np.zeros(shape=(grid_width_x, grid_width_y))

    for index_x in range(grid_width_x):
        x_in_meters = index_x * resolution_grid + x_min

        for index_y in range(grid_width_y):
            y_in_meters = index_y * resolution_grid + y_min
            grid_position = Position(x=x_in_meters, y=y_in_meters)
            ug = calc_attractive_potential(grid_position, goal)
            uo = calc_repulsive_potential(
                grid_position, obstacles_positions_x, obstacles_positions_y, robot_radius)
            uf = ug + uo
            potential_field[index_x][index_y] = uf

    return potential_field, GridLimits(x_min=x_min, x_max=x_max, y_min=y_min, y_max=y_max, resolution=resolution_grid)


def calc_attractive_potential(grid_position: Position,  goal: Position) -> float:
    return 0.5 * KP * np.hypot(grid_position.x - goal.x, grid_position.y - goal.y)


def calc_repulsive_potential(position: Position, obstacles_position_x: list[float], obstacles_position_y: list[float], robot_radius: float) -> float:
    # search nearest obstacle
    nearest_obstacle_distance = search_nearest_obstacle(position, obstacles_position_x, obstacles_position_y)
    # calc repulsive potential
    return calc_repulsive_potencial(nearest_obstacle_distance, robot_radius)


def search_nearest_obstacle(position: Position, obstacles_position_x: list[float], obstacles_position_y: list[float]) -> float:

    min_distance = float("inf")
    number_of_obstacles = len(obstacles_position_x)

    for i in range(number_of_obstacles):
        distance = np.hypot(
            position.x - obstacles_position_x[i], position.y - obstacles_position_y[i])
        if distance < min_distance:
            min_distance = distance

    return min_distance


def calc_repulsive_potencial(nearest_obstacle_distance: float, robot_radius: float) -> float:
    if 0.5*nearest_obstacle_distance <= robot_radius:
        if nearest_obstacle_distance <= 0.1:
            nearest_obstacle_distance = 0.1

        return 0.5 * ETA * (1.0 / nearest_obstacle_distance - 1.0 / robot_radius) ** 2
    else:
        return 0.0


def make_potencial_field_grid(limits: GridLimits, calculator: PotentialFieldCalculator) -> np.ndarray:

    grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
    grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

    grid = np.zeros(shape=(grid_width_x, grid_width_y))

    for x in range(grid_width_x):
        for y in range(grid_width_y):
            real_pos = index_to_real_pos((x, y), grid_limits=limits)
            grid[x, y] = calculator.calculate_potencial_value(real_pos)

    return grid


def index_to_real_pos(index: tuple[int, int], grid_limits: GridLimits) -> tuple[float, float]:
    position_x = index[0] * grid_limits.resolution + grid_limits.x_min
    position_y = index[1] * grid_limits.resolution + grid_limits.y_min

    return position_x, position_y


def load_json(path_to_file: Path) -> list[Polygon]:
    with open(path_to_file, 'r') as json_file:
        polygons = json.loads(json_file.read())

        return list(map(Polygon.from_dict, polygons))


def polygon_2_numpy_array(polygon: Polygon) -> np.ndarray:
    return np.array([v.position for v in polygon.vertices])


def plot_exemple():
    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m]

    start_position = Position(x=0.0, y=10.0)
    goal_position = Position(x=30.0, y=30.0)

    # obstacle x position list [m]
    obstacles_positions_x = [15.0, 5.0, 20.0, 25.0]
    # obstacle y position list [m]
    obstacles_positions_y = [25.0, 15.0, 26.0, 25.0]

    potential_field, field_limits = calc_potential_field(
        goal_position, obstacles_positions_x, obstacles_positions_y, grid_size, robot_radius, start_position)

    planning = PotentialFieldPlanning(potential_field, field_limits)

    start = real_pos_to_index(real_pos=start_position, field_limits=field_limits)
    goal = real_pos_to_index(real_pos=goal_position, field_limits=field_limits)

    path = planning.run(min_distance=grid_size, start_index=start, goal_index=goal)
    plotter = Plotter2D()

    plotter.draw_potential_field(potential_field.T)
    plotter.draw_points(np.array(path), RGB(255, 0, 0))
    plotter.draw_points(np.array([start, goal]), color=RGB(155, 155, 155))

    plotter.show()


def real_pos_to_index(real_pos: Position, field_limits: GridLimits) -> tuple[int, int]:
    index_x = round((real_pos.x - field_limits.x_min) / field_limits.resolution)
    index_y = round((real_pos.y - field_limits.y_min) / field_limits.resolution)

    return index_x, index_y


def calculate_robot_radius(robot_vertices: np.ndarray) -> float:
    robot_center = (robot_vertices[:, 0].mean(), robot_vertices[:, 1].mean())
    max_distance = -1
    for vertex in robot_vertices:
        distance = np.hypot(robot_center[0] - vertex[0], robot_center[1] - vertex[1])
        if distance > max_distance:
            max_distance = distance
    return max_distance


def make_points_grid(limits: GridLimits) -> np.ndarray:

    grid_width_x = int(round((limits.x_max - limits.x_min) / limits.resolution))
    grid_width_y = int(round((limits.y_max - limits.y_min) / limits.resolution))

    x_space = np.linspace(limits.x_min, limits.x_max, grid_width_x)
    y_space = np.linspace(limits.y_min, limits.y_max, grid_width_y)

    # xx, yy = np.meshgrid(x_space, y_space)
    grid_points = list()

    for x_value in x_space:
        for y_value in y_space:
            grid_points.append([x_value, y_value])

    grid_points = np.array(grid_points)

    print('grid_points shape: ', grid_points.shape)

    return grid_points.reshape((len(x_space), len(y_space), -1))


def main():
    polygons = load_json(Path('output').joinpath('obstacles_vertices.json'))

    robot = polygons[-1]
    robot_vertices = polygon_2_numpy_array(robot)
    obstacles = [polygon_2_numpy_array(p) for p in polygons[:-1]]

    obstacles_in_c_space = configuration_space.make_configuration_space(robot_vertices, obstacles)

    goal_real_position = np.array([-0.40132653, 1.19149412])
    start_real_position = np.array([-1.29316327,  0.04412941])

    grid_limits = GridLimits(x_min=-2.1850e+00, x_max=2.1850e+00, y_min=-2.2506e+00, y_max=2.2506e+00, resolution=0.087)

    calculator = PotentialFieldCalculator(polygons[:-1], goal_real_position, robot_radius=calculate_robot_radius(robot_vertices))
    potencial_field_grid = make_potencial_field_grid(limits=grid_limits, calculator=calculator)

    points_grid = make_points_grid(grid_limits)

    potential_grid = PotentialFielGrid(grid_limits=grid_limits, calculator=calculator)

    graph = MeshGridGraph(potential_grid)

    a_star_params = PotencialFieldAStarParameter(calculator, grid_limits)

    a_star_search = AStarSearch(graph, a_star_params)
    start_node = MeshNode(x_index=10, y_index=26)
    goal_node = MeshNode(x_index=20, y_index=42)

    planning = PotentialFieldPlanning(potencial_field_grid, grid_limits)

    start = (start_node.x_index, start_node.y_index)
    goal = (goal_node.x_index, goal_node.y_index)

    path = planning.run(min_distance=grid_limits.resolution, start_index=start, goal_index=goal)
    a_star_path = a_star_search.run(initial_node=start_node, desired_node=goal_node)

    a_star_path_index = [(n.x_index, n.y_index) for n in a_star_path]

    potential_planning_points = np.array(list(map(lambda index: index_to_real_pos(index, grid_limits=grid_limits), path)))

    def mesh_node_to_point(node: MeshNode) -> np.ndarray:
        return potential_grid.get(x=node.x_index, y=node.y_index)

    a_star_path_points = np.array([mesh_node_to_point(node) for node in a_star_path])

    np.savetxt(Path('output').joinpath('a_star_potential_field_path.csv'), a_star_path_points, delimiter=',')

    plotter = Plotter2D()

    plotter.draw_potential_field(potencial_field_grid.T)
    plotter.draw_points(np.array(path), RGB(255, 0, 0))
    plotter.draw_points(np.array(a_star_path_index), RGB(0, 255, 255))
    plotter.draw_points(np.array([start, goal]), color=RGB(155, 155, 155))

    plotter.save_figure(Path('output').joinpath('heatmap.pdf'))

    plotter.next_figure()
    plotter.draw_points(points_grid.reshape(-1, 2), color=RGB(r=184, g=184, b=184))
    plotter.draw_polygons(obstacles_in_c_space)
    plotter.draw_points(potential_planning_points, RGB(0, 255, 255))
    plotter.draw_points(a_star_path_points, RGB(255, 255, 0))

    plotter.save_figure(Path('output').joinpath('c_space_potential_field.pdf'))

    plotter.next_figure()
    plotter.draw_points(points_grid.reshape(-1, 2), color=RGB(r=184, g=184, b=184))
    plotter.draw_polygons(obstacles + [robot_vertices])
    plotter.draw_points(potential_planning_points, RGB(0, 255, 255))
    plotter.draw_points(a_star_path_points, RGB(255, 255, 0))
    plotter.save_figure(Path('output').joinpath('work_space_potential_field.pdf'))

    plotter.show()


if __name__ == '__main__':
    print(f'{__file__ } start!!')
    main()
    print(f'{__file__} Done!!')
