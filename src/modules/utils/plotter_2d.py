from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from matplotlib.colors import Colormap
import numpy as np
from matplotlib import pyplot
from matplotlib import transforms

@dataclass
class RGB:
    """Onde r,g,b varia de 0 até 255"""
    r: int
    g: int
    b: int


class Plotter2D:

    def __rgb_to_normalized_array(self,color: RGB) -> np.ndarray:
        return np.array([color.r, color.g, color.b])/255

    def draw_points(self, vertices_positions: np.ndarray, color: Optional[RGB] = None):
        """ Espera um vetor v no seguinte formato:
            v = [
                [x,y],
                [x,y],
                [x,y],
                 ...
            ]
        """

        if color:
            color = self.__rgb_to_normalized_array(color)

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

    
    def __draw_polygon(self,vertices_positions: np.ndarray):
        pyplot.fill(vertices_positions[:, 0], vertices_positions[:, 1])
        pyplot.scatter(vertices_positions[:, 0].mean(), vertices_positions[:, 1].mean())

    def draw_lines(self,lines: np.ndarray, color: Optional[RGB] = None):
        """Desenha uma linha seguida da outra
            line[0]: (x1,y1) .......................(x2,y2)
            line[1]:                                (x2,y2) ............................(x3,y3)
        """
        if color:
            color = self.__rgb_to_normalized_array(color)
        pyplot.plot(lines[:, 0], lines[:, 1],color=color)
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

    def draw_potential_field(self,field:np.ndarray):
        """Espera-se uma imagem em r,g,b ou em tom de cinza,
        """
        pyplot.pcolor(field,vmax=5,vmin=0)
    
    def draw_image(self,image:np.ndarray):
        pyplot.imshow(image)