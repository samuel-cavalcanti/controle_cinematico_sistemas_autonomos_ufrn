from dataclasses import dataclass


@dataclass()
class Vertex:
    name: str
    position: list[float]


@dataclass()
class Polygon:
    name: str
    vertices: list[Vertex]
