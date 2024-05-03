from kinematicsrobotics import forwardkinematics as forward
from kinematicsrobotics import dataprocessing as pp
from kinematicsrobotics import plot as plot
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
joins = [[0, 120],[0, 120],[0, 120],[0, 120],[0, 0]]
steps = [5, joins[1][1]//10, joins[2][1]//10, joins[3][1]//10, 1]

dataset = spacemapping.mapping(robo,joins,steps)

# Tratamento da base de dados
## Altura negativa
height = 0
dataset = pp.remove_height(dataset,height)
## Elos negativos
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0]
        ]

dataset = pp.remove_height_join(dataset,Elos,'bot',['theta_1','theta_2','theta_3'],height)

## Removendo redundância
# Usando 10 mm de raio
radius = 1
# Análise de vizinhos é no espaço operacional 
attr_neighbors = ['p_x','p_y','p_z']
# O critério de escolha é no espaço das juntas
attr_redundancy = ['theta_2','theta_3','theta_4','theta_5']
# remove as redundâncias
dataset = pp.remove_redundancy(dataset,radius,attr_neighbors, attr_redundancy)

## Redução de atributos
dataset = pd.concat([dataset[['theta_1','theta_2','theta_3','theta_4','theta_5','p_x','p_y','p_z']],pp.rotations(dataset)],axis=1)
path = r'\kinematics-robotics\src\data\ready\dataset_15mm.csv'
dataset.to_csv(path)


