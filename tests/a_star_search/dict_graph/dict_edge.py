from dataclasses import dataclass


@dataclass
class DictEdge:
    origin: str
    target: str
    weight: int
