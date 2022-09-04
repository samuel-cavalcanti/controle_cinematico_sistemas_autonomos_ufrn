from pathlib import Path
import csv


class SimulationCSVRecorder:
    """Gavador de amostradas da simulação, ele salva as amostradas no formado csv com um header
    csv === comma separated value
    geralmente busca-se salvar esses arquivos também com o nome .csv, mas não é obrigatório.

    Um header ou cabeçalho do arquivo é a primeira linha do arquivo, que contem os nomes da coluna. Um exemplo de arquivo csv:

    posição x do robô, posição y do robô, orientação do robô, sensor 1, sensor 2
    10,20,0,1,1
    12,20,0,1,1
    14,20,0,0.5,1
    """
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

        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, mode='w') as file:

            writer = csv.writer(file)
            writer.writerow(self.__headers)
            writer.writerows(self.__samples)
