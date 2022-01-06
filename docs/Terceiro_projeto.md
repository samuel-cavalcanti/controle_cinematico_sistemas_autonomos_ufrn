# TERCEIRO PROJETO DE SISTEMAS ROBÓTICOS AUTÔNOMOS

Desenvolver sistema de mapeamento para robô móvel que permita
ao mesmo construir um mapa a partir de sensor de alcance, de
maneira a possibilitar posteriormente a execução de movimentos
especificados em um espaço de trabalho povoado de obstáculos
poligonais, sem colidir com os mesmos e sem dispor de um mapa
previamente fornecido pelo operador.

## Metas

1. Incluir modelo de sensor de alcance (sonar) no robô simulado.
Telecomandar o robô através do teclado ou um controlador
simples que faça o robô se locomover com velocidade
constante e girar aleatoriamente de modo a evitar obstáculos a
partir de um limiar especificado de distância do obstáculo
detetada. O simulador deve apresentar nova tela com as
medições obtidas pelo sensor de alcance a partir dos obstáculos
detectados pelo mesmo. Entregar relatório e vídeo mostrando o
sistema operando com as novas funcionalidades.

2. A partir dos dados do sensor de alcance, construir grade de
ocupação. Entregar relatório e vídeo apresentando as novas
funcionalidades implementadas, particularmente, mostrar a
construção progressiva da grade de ocupação.

3. Implementar a navegação do robô no ambiente simulado,
utilizando controlador implementado na primeira unidade e
planejador de caminhos implementado na segunda unidade, e
usando como mapa do ambiente a grade de ocupação obtida na
meta 2. Executar testes para diferentes configurações de
obstáculos. Entregar relatório e vídeo apresentando o
funcionamento do sistema.

