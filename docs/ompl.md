# OPEN MOTION PLANNING LIBRARY (OMPL)


##  Soluções comuns para planejamento de movimento

- Soluções baseadas em Amostragem
- Soluções baseadas em buscas com Heurística em mapas discretizados
- Soluções baseadas em Otimização
- Soluções baseadas em Teoria de Controle

## Soluções do OMPL

OMPL implementa as soluções baseadas em amostragem e 
e outras poucas soluções baseadas em Teoria de controle.
OMPL não possui algoritmos para detecção de colisão ou
cálculo de cinemática do robô.

Todos os planejadores disponíveis pelo OMPL: [OMPL Available Planners](https://ompl.kavrakilab.org/planners.html) 

## Ecossistema do OMPL

### OMPL.app
Existe um outro projeto vizinho chamado OMPL.app
que implementa alguns algoritmos de colisão e uma interface
simples feita em QT para visualização do robô, mas assumindo
que o robô é formado por triângulos.

### Planner Arena - OMPL benchmarking
Devido ao fato do OMPL ter uma quantidade significativa
de planejadores, se viu necessário criar uma aplicação
chamada **_Planner Arena_**) que 
fez um benchmarking desses algoritmos, onde foi coletado
diversas medidas de performance e armazenado essa medidas em
um banco de dados que por fim pode ser visualizado através
do site  [plannerarena.org](http://plannerarena.org/)

### Outros

Existem outros projetos que usam o OMPL como:

- CoppeliaSim
- Open Robotics Automation Virtual Environment (OpenRAVE)
- Robotics Library
- The Modular OpenRobots Simulation Engine (MORSE)
- VEROSIM SOLUTIONS, 3D Simulation for Environment topics
- Ros-MoveIt!
