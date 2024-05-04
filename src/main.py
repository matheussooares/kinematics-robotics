from kinematicsrobotics import kinematics
from kinematicsrobotics import dataprocessing
from kinematicsrobotics import spacemapping
import pandas as pd
import numpy as np

# Modelagem da cinemática direta usando Denavit-hartenberg
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0],
        ['theta_4',0,0,90,90],
        ['theta_5',18,0,0,0]
]

robo = kinematics.Robo("Robo",Elos)

# Mapeamento do espaço das juntas e o espaço operacional
joins = [[0, 10],[0, 10],[0, 10],[0, 10],[0, 0]]
steps = [10, joins[1][1]//2, joins[2][1]//2, joins[3][1]//2, 1]

dataset = spacemapping.mapping(robo,joins,steps)
print(dataset.shape)



## Altura negativa
height = 0
dataset = dataprocessing.remove_height(dataset,height)

## Elos negativos
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0]
        ]

dataset = dataprocessing.remove_height_join(dataset,Elos,'bot',['theta_1','theta_2','theta_3'],height)
# Usando 10 mm de raio
radius = 1
# Análise de vizinhos é no espaço operacional 
attr_neighbors = ['p_x','p_y','p_z']
# O critério de escolha é no espaço das juntas
attr_redundancy = ['theta_2','theta_3','theta_4','theta_5']

dataset_1mm = dataprocessing.remove_redundancy(dataset,radius,attr_neighbors, attr_redundancy)

print(dataset_1mm.head(3))
print(dataset_1mm.shape)