from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float
    theta_in_rads: float

"""
EM C
struct Position {
    float x;
    float y;
    float theta;
}
"""