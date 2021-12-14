from dataclasses import dataclass
from typing import Optional

import numpy as np


@dataclass
class NormalVectorWrapper:
    is_robot_vector: bool
    normal_vec: np.ndarray
    vertex: np.ndarray
    next_node_index: Optional[int]

    def __str__(self) -> str:
        normal_angle_in_rads = np.arctan2(self.normal_vec[1], self.normal_vec[0])
        normal_angle_in_deg = np.rad2deg(normal_angle_in_rads) if normal_angle_in_rads >= 0 else 360 + np.rad2deg(
            normal_angle_in_rads)
        return f'robot: {self.is_robot_vector} normal : {self.normal_vec} ' \
               f' vertice: {self.vertex} angle: {normal_angle_in_deg}' \
               f' next node: {self.next_node_index}'
