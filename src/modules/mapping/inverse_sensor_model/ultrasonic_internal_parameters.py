
from dataclasses import dataclass


@dataclass
class UltrasonicInternalParameters:
    alpha_in_rads: float
    e_in_meters: float
    max_distance_in_meters: float
    min_distance_in_meters: float
