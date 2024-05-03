from kinematicsrobotics import forwardkinematics as forward
from kinematicsrobotics import dataprocessing
from kinematicsrobotics import plot
from kinematicsrobotics import spacemapping
import pandas as pd

# Modelagem da cinemática direta usando Denavit-hartenberg
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0],
        ['theta_4',0,0,90,90],
        ['theta_5',18,0,0,0]
]

robo = forward.Robo("Robo",Elos)

# Mapeamento do espaço das juntas e o espaço operacional
joins = [[0, 10],[0, 10],[0, 10],[0, 10],[0, 0]]
steps = [10, joins[1][1]//2, joins[2][1]//2, joins[3][1]//2, 1]

dataset = spacemapping.mapping(robo,joins,steps)

print(dataset.shape)


# Tratamento da base de dados
## Altura negativa
height = 0
dataset = dataprocessing.remove_height(dataset,height)

print(dataset[''])


