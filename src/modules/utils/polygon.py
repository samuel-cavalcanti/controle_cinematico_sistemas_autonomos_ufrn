from __future__ import annotations

from dataclasses import dataclass


@dataclass()
class Vertex:
    name: str
    position: list[float]


@dataclass()
class Polygon:
    name: str
    vertices: list[Vertex]

    @staticmethod
    def from_dict(poly_dict: dict)->Polygon:
        vertices = [Vertex(**v) for v in poly_dict['vertices']]

        return Polygon(name=poly_dict['name'], vertices=vertices)
