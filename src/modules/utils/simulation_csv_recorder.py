from pathlib import Path
import csv


class SimulationCSVRecorder:
    __headers: list[str]
    __samples: list[list[float]]

    def __init__(self, headers: list[str]) -> None:
        self.__headers = headers

        self.__samples = list()
        pass

    def add_sample(self, sample: list[float]):

        assert len(self.__headers) == len(sample), "O Tamanho da amostra deve ser igual ao do cabeçalho"

        self.__samples.append(sample)

    def save(self, file_path: Path):

        with open(file_path, mode='w') as file:

            writer = csv.writer(file)
            writer.writerow(self.__headers)
            writer.writerows(self.__samples)
