from dataclasses import dataclass

from ..utils import Position


@dataclass
class RobotState:
    robot_pos: Position
    normalized_distances: list[float]
