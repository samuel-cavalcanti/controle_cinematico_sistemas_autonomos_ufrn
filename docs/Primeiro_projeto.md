# PRIMEIRO PROJETO DE SISTEMAS ROBÓTICOS AUTÔNOMOS

Simular um robô móvel com acionamento diferencial e desenvolver
um sistema de controle cinemático que permita ao mesmo executar
movimentos especificados em espaço livre de obstáculos.


## Metas

1. Simular no software V-Rep um robô móvel com acionamento
diferencial, de maneira a que o mesmo receba os comandos das
velocidades de referências para as rodas e retorne a posição e
orientação do robô (x,y,&theta;) em um referencial global. Além do
movimento do robô no espaço de trabalho, mostrar os
seguintes gráficos: velocidades das rodas (entradas) em função
do tempo; configuração do robô (x,y,&theta;), (saídas), em função do
tempo; gráfico das posições (x(t),y(t)) seguidas pelo robô no
plano xy. Entregar relatório e vídeo mostrando o a simulação e
os gráficos solicitados

2. Implementar gerador de caminho baseado em polinômios
interpoladores de 3º grau para robô móvel. Incluir gerador de
caminho na simulação. O simulador deve permitir mostrar o
caminho gerado sobre a tela do espaço de trabalho do V-Rep.
Entregar relatório e vídeo mostrando os resultados obtidos.

3. Implementar controladores cinemáticos do robô móvel no
simulador: controlador seguidor de trajetória, controlador de
posição. Testar o controlador no simulador e obter resultados
de simulação (trajetória gerada, trajetória seguida, gráficos das
variáveis de entrada e saída em função do tempo, etc.).


[__Relatório__](Relatorio_Seminario_Sistemas_Roboticos_primeiro_projeto.pdf)

### Testes

[Gráficos do gerador de caminhos](gerador_de_caminhos_plot.md)




## Demonstração do gerador de caminhos no CoppeliaSim

https://user-images.githubusercontent.com/24573157/215786342-17f21b71-4963-459c-9ca3-1bc2c2f729c4.mp4


## Demonstração do Controlador de Posição Frederico

https://user-images.githubusercontent.com/24573157/215786734-f65424ca-ff4e-499a-bf9e-f69b5b9790e9.mp4




## Demonstração do Controlador Frederico com gerador de trajetórias

https://user-images.githubusercontent.com/24573157/215786910-4351b198-f914-4ce7-a821-04ab5f5a66ff.mp4

