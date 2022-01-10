import numpy as np

from ...utils.polygon import Polygon


class PotentialFieldCalculator:

    __obstacles: list[Polygon]
    __goal: np.ndarray
    __robot_radius: float
    KP = 1  # attractive potential gain
    ETA = 120.0  # repulsive potential gain

    def __init__(self, obstacles: list[Polygon],  goal: np.ndarray, robot: Polygon) -> None:
        self.__obstacles = obstacles
        self.__goal = goal
        self.__robot_radius = self.__calculate_robot_radius(robot)

    def calculate_potencial_value(self, position: np.ndarray) -> float:

        repulsive = 0
        for obstacle in self.__obstacles:
            repulsive += self.__calc_repulsive_potential_from_obstacle(position, obstacle)

        attractive = self.__calc_attractive_potential(position)
        return repulsive + attractive

    def __calc_attractive_potential(self, position: np.ndarray) -> float:
        return 0.5 * self.KP * np.linalg.norm(position - self.__goal)

    def __calc_repulsive_potential_from_obstacle(self, position: np.ndarray, obstacle: Polygon) -> float:
        # center = self.__center_of_polygon(obstacle)
        potential = 0
        for vertex in obstacle.vertices:
            potential += self.__calc_repulsive_potential(position, np.array(vertex.position))

        return potential

    def __calc_repulsive_potential(self, position: np.ndarray, vertex_position: np.ndarray) -> float:
        distance = np.linalg.norm(vertex_position - position)
        if distance <= self.__robot_radius:
            if distance <= 0.1:
                distance = 0.1

            return 0.5 * self.ETA * (1.0 / distance - 1.0 / self.__robot_radius) ** 2
        else:
            return 0.0

    def __center_of_polygon(self, polygon: Polygon) -> np.ndarray:
        mean_x = 0
        mean_y = 0

        for vertex in polygon.vertices:
            mean_x += vertex.position[0]
            mean_y += vertex.position[1]

        number_of_vertices = len(polygon.vertices)

        return np.array([mean_x/number_of_vertices, mean_y/number_of_vertices])

    def __calculate_robot_radius(self, robot: Polygon) -> float:
        robot_center = self.__center_of_polygon(robot)
        max_distance = -1
        for vertex in robot.vertices:
            distance = np.hypot(robot_center[0] - vertex.position[0], robot_center[1] - vertex.position[1])
            if distance > max_distance:
                max_distance = distance
        return max_distance
