from ..utils import Position

from dataclasses import dataclass
@dataclass
class RobotState:
    robot_position: Position
    normalized_distance: float