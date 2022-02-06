from pathlib import Path
from typing import Protocol


class SimulationRecorder(Protocol):
    """Interface: Gavador de amostradas da simulação
    Essa interface é importante para desacoplar e saída de dados da gravação
    é muito frequente ter que trocar a forma de gravar os dados.
    """

    def add_sample(self, sample: list[float]):
        """Adiciona uma amostra no gravador"""

    def save(self, file_path: Path):
        """Salva a gravação em um arquivo desejado"""
