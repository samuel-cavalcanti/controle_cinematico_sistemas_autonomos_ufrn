# Sistemas Robóticos Autônomos UFRN

Repositório da disciplina Sistemas Robóticos autónomos.
Nessa disciplina foi realizado os seguintes projetos:

-  Simular um robô móvel com acionamento diferencial e desenvolver um sistema de controle cinemático que permita ao mesmo executar movimentos especificados em espaço livre de obstáculos. [Detalhes e Resultados do Primeiro Projeto](docs/Primeiro_projeto.md)

- Desenvolver Planejadores de Caminhos para Robô Móvel que
permitam ao mesmo executar movimentos especificados em espaço
povoado de obstáculos, sem colidir com os mesmos.  [Detalhes e Resultados do Segundo Projeto](docs/Segundo_projeto.md)

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