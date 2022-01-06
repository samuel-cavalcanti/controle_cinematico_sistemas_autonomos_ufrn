from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import numpy as np
from matplotlib import pyplot


@dataclass
class RGB:
    """Onde r,g,b varia de 0 até 255"""
    r: int
    g: int
    b: int


class Plotter2D:

    @staticmethod
    def draw_points(vertices_positions: np.ndarray, color: Optional[RGB] = None):
        """ Espera um vetor v no seguinte formato:
            v = [
                [x,y],
                [x,y],
                [x,y],
                 ...
            ]
        """
       
        if color:
            color = np.array([color.r, color.g, color.b])/255
       
        pyplot.scatter(vertices_positions[:, 0], vertices_positions[:, 1], color=color)
        pyplot.draw()

    def draw_polygons(self, polygon: list[np.ndarray]):
        """ Espera uma lista de vertices, cujo os vertices são um vetor v no seguinte formato:
            v = [
                [x,y],
                [x,y],
                [x,y],
                 ...
            ]

            Os vertices tem que estar ordenados no sentido anti-horário, ou seja da seguinte maneira:

                         .(3)
                    .(4)       .(2)

                     .(5)    .(1)

        """

        [self.__draw_polygon(p) for p in polygon]
        pyplot.draw()

    @staticmethod
    def next_figure():
        """Cria uma nova folha para exibir outro gráfico"""
        pyplot.figure(pyplot.gcf().number + 1)

    @staticmethod
    def __draw_polygon(vertices_positions: np.ndarray):
        pyplot.fill(vertices_positions[:, 0], vertices_positions[:, 1])
        pyplot.scatter(vertices_positions[:, 0].mean(), vertices_positions[:, 1].mean())

    @staticmethod
    def draw_lines(lines: np.ndarray):
        """Desenha uma linha seguida da outra
            line[0]: (x1,y1) .......................(x2,y2)
            line[1]:                                (x2,y2) ............................(x3,y3)
        """
        pyplot.plot(lines[:, 0], lines[:, 1])
        pyplot.draw()

    @staticmethod
    def __draw_polygon(vertices_positions: np.ndarray):
        pyplot.fill(vertices_positions[:, 0], vertices_positions[:, 1])
        pyplot.scatter(vertices_positions[:, 0].mean(), vertices_positions[:, 1].mean())

    @staticmethod
    def save_figure(path: Path):
        # figure = pyplot.gcf()
        # figure.set_size_inches(18, 16)
        pyplot.savefig(str(path), dpi=1200)

    @staticmethod
    def view_grid(enable: bool = True):
        """Habilita e desabilita a visualização da grade"""
        pyplot.grid(enable)

    @staticmethod
    def show():
        """cria uma janela para cada gráfico desenhado e segura o processo até fechar as janelas"""
        pyplot.show()
