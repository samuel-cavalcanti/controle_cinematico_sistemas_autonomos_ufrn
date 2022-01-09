"""
Basend in:
https://github.com/AtsushiSakai/PythonRobotics/blob/master/PathPlanning/PotentialFieldPlanning/potential_field_planning.py

Potential Field based path planner

author: Atsushi Sakai (@Atsushi_twi)

Ref:
https://www.cs.cmu.edu/~motionplanning/lecture/Chap4-Potential-Field_howie.pdf

"""

from dataclasses import dataclass
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Parameters
KP = 5.0  # attractive potential gain
ETA = 100.0  # repulsive potential gain
AREA_WIDTH = 30.0  # potential area width [m]
# the number of previous positions used to check oscillations
OSCILLATIONS_DETECTION_LENGTH = 3

show_animation = True


@dataclass
class Position:
    x: float
    y: float



def calc_potential_field(goal: Position, obstacles_position_x: list[float], obstacles_position_y: list[float], resolution_grid: float, robot_radios: float, start: Position):

    x_min = min(min(obstacles_position_x), start.x,
                goal.x) - AREA_WIDTH / 2.0
    y_min = min(min(obstacles_position_y), start.y,
                goal.y) - AREA_WIDTH / 2.0
    x_max = max(max(obstacles_position_x), start.x,
                goal.x) + AREA_WIDTH / 2.0
    y_max = max(max(obstacles_position_y), start.y,
                goal.y) + AREA_WIDTH / 2.0
    grid_width_x = int(round((x_max - x_min) / resolution_grid))
    grid_width_y = int(round((y_max - y_min) / resolution_grid))

    print(f'grid size: {grid_width_x} ,{grid_width_y}')
    # calc each potential
    pmap = np.zeros(shape=(grid_width_x, grid_width_y))

    for index_x in range(grid_width_x):
        x_in_meters = index_x * resolution_grid + x_min

        for index_y in range(grid_width_y):
            y_in_meters = index_y * resolution_grid + y_min
            grid_position = Position(x=x_in_meters, y=y_in_meters)
            ug = calc_attractive_potential(grid_position, goal)
            uo = calc_repulsive_potential(
                grid_position, obstacles_position_x, obstacles_position_y, robot_radios)
            uf = ug + uo
            pmap[index_x][index_y] = uf

    return pmap, x_min, y_min


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
    if nearest_obstacle_distance <= robot_radius:
        if nearest_obstacle_distance <= 0.1:
            nearest_obstacle_distance = 0.1

        return 0.5 * ETA * (1.0 / nearest_obstacle_distance - 1.0 / robot_radius) ** 2
    else:
        return 0.0


def oscillations_detection(previous_ids: deque[tuple[int, int]], id: tuple[int, int]):
    previous_ids.append(id)

    if (len(previous_ids) > OSCILLATIONS_DETECTION_LENGTH):
        previous_ids.popleft()

    # check if contains any duplicates by copying into a set
    previous_ids_set = set()
    for id in previous_ids:
        if id in previous_ids_set:
            return True
        else:
            previous_ids_set.add(id)
    return False


def move_in_potential_map(potential_map: np.ndarray, current_index: tuple[int, int]) -> tuple[int, int]:
    best_move = (-1, -1)
    min_potencial_field_value = float('inf')
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            move = (current_index[0] + dx, current_index[1] + dy)
            if is_valid_move(move, dx, dy, potential_map):
                if potential_map[move[0]][move[1]] < min_potencial_field_value:
                    min_potencial_field_value = potential_map[move[0]][move[1]]
                    best_move = move

    return best_move


def is_valid_move(index: tuple[int, int], dx: int, dy: int, potential_map: np.ndarray) -> bool:
    if (dx, dy) == (0, 0):
        return False
    try:
        potential_map[index[0]][index[1]]
        return True
    except IndexError:
        return False  # outside area


def index_to_real_pos(index: tuple[int, int], resolution_grid: float, min_values: tuple[float]) -> tuple[float, float]:
    position_x = index[0] * resolution_grid + min_values[0]
    position_y = index[1] * resolution_grid + min_values[1]

    return position_x, position_y


def real_pos_to_index(real_pos: Position, resolution_grid: float, min_grid_values: tuple[float]) -> tuple[int, int]:
    index_x = round((real_pos.x - min_grid_values[0]) / resolution_grid)
    index_y = round((real_pos.y - min_grid_values[1]) / resolution_grid)

    return index_x, index_y


def potential_field_planning(start: Position, goal: Position, obstacles_x: list[float], obstacles_y: list[float], resolution_grid: float, robot_radius: float):

    # calc potential field
    pmap, x_min, y_min = calc_potential_field(
        goal, obstacles_x, obstacles_y, resolution_grid, robot_radius, start)

    min_grid_values = (x_min, y_min)
    # search path
    euclidean_distance_to_goal = np.hypot(start.x - goal.x, start.y - goal.y)
    current_index = real_pos_to_index(start, resolution_grid, min_grid_values)

    goal_index = real_pos_to_index(goal, resolution_grid, min_grid_values)

    if show_animation:
        draw_heatmap(pmap)
        # for stopping simulation with the esc key.
        plt.gcf().canvas.mpl_connect('key_release_event',
                                     lambda event: [exit(0) if event.key == 'escape' else None])
        plt.plot(current_index[0], current_index[1], "*k")
        plt.plot(goal_index[0], goal_index[1], "*m")

    rx, ry = [start.x], [start.y]
    previous_ids = deque()

    while euclidean_distance_to_goal >= resolution_grid:
        current_index = move_in_potential_map(
            potential_map=pmap, current_index=current_index)

        real_pos = index_to_real_pos(
            current_index, resolution_grid, min_grid_values)

        euclidean_distance_to_goal = np.hypot(
            goal.x - real_pos[0], goal.y - real_pos[1])
        rx.append(real_pos[0])
        ry.append(real_pos[1])

        if oscillations_detection(previous_ids, current_index):
            print(
                f"Oscillation detected at ({current_index[0]},{current_index[1]})!")
            break

        if show_animation:
            plt.plot(current_index[0], current_index[1], ".r")
            plt.pause(0.01)

    print("Goal!!")

    return rx, ry


def draw_heatmap(data:np.ndarray):

    plt.imshow(data.T,vmax=100.0 )#, cmap=plt.cm.Blues


def main():
    print("potential_field_planning start")

    grid_size = 0.5  # potential grid size [m]
    robot_radius = 5.0  # robot radius [m]

    start_position = Position(x=0.0, y=10.0)
    goal_position = Position(x=30.0, y=30.0)

    # obstacle x position list [m]
    obstacles_positions_x = [15.0, 5.0, 20.0, 25.0]
    # obstacle y position list [m]
    obstacles_positions_y = [25.0, 15.0, 26.0, 25.0]

    if show_animation:
        plt.grid(True)
        plt.axis("equal")

    # path generation
    _, _ = potential_field_planning(
        start_position, goal_position, obstacles_positions_x, obstacles_positions_y, grid_size, robot_radius)
    plt.savefig(Path('output').joinpath('simple_potential_field_test.pdf'), dpi=1200)
    if show_animation:
        plt.show()
	

if __name__ == '__main__':
    print(__file__ + " start!!")
    main()
   
    print(__file__ + " Done!!")
