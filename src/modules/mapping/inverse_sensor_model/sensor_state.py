from ...utils import Position

from dataclasses import dataclass
@dataclass
class SensorState:
    robot_position: Position
    normalized_distance: float