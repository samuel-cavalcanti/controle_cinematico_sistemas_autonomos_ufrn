# Sistemas Robóticos Autônomos UFRN

Repositório da disciplina Sistemas Robóticos autónomos.
Nessa disciplina foi realizado os seguintes projetos:

- [x]  Simular um robô móvel com acionamento diferencial e desenvolver um sistema de controle cinemático que permita ao mesmo executar movimentos especificados em espaço livre de obstáculos. [Detalhes e Resultados do Primeiro Projeto](docs/Primeiro_projeto.md)

- [x] Desenvolver Planejadores de Caminhos para Robô Móvel que
permitam ao mesmo executar movimentos especificados em espaço
povoado de obstáculos, sem colidir com os mesmos.  [Detalhes e Resultados do Segundo Projeto](docs/Segundo_projeto.md)

- [ ] Desenvolver sistema de mapeamento para robô móvel que permita ao mesmo construir um mapa a partir de sensor de alcance, de maneira a possibilitar posteriormente a execução de movimentos especificados em um espaço de trabalho povoado de obstáculos poligonais, sem colidir com os mesmos e sem dispor de um mapa previamente fornecido pelo operador [Detalhes e Resultados do Terceiro Projeto](docs/Terceiro_projeto.md)

Anotações sobre [Open Motion Planning Library (OMPL)](docs/ompl.md)

### Observações
Para a execução desse projeto, foi utilizado:
- _python_ na sua versão __3.10__
- _Coppeliasim_ na sua versão __V4.2.0 rev5__
- instale as dependências do projeto:

```shell
pip install -r requirements.txt
```

### Executar Testes automatizados
```shell
python -m unittest discover  -v
```


## Passos para executar a aplicação

0. instale as dependências

1. abra o coppeliasim, e abra a simulação que deseja, seja [simple_scene.ttt](scenes/simple_scene.ttt) ou [simple_scene_with_obstacles](scenes/simple_scene_with_obstacles.ttt)
   File -> open scene... >

2. inicialize a simulação, clicando no ícone do PLAY

3. execute a aplicação em python:

### testar o controlador braitenberg
```shell
python src/main_braitenberg.py 
```

###  para testar o controlador de Posição Frederico
```shell
python src/main_frederico.py
```

### para testar o controlador Frederico com gerador de trajetórias
```shell
python src/main_trajectory_follow.py 
```

### para testar o controlador Frederico com o planejador de caminho a-star + espaço de configuração
```shell
python src/main_path_follow.py c_space
```

### para testar o controlador Frederico com o planejador de caminho a-star + campo de potencial
```shell
python src/main_path_follow.py p_space
```