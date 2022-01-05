from dataclasses import dataclass


@dataclass
class IntersectionResult:
    is_intersect: bool
    is_horizontal_line: bool