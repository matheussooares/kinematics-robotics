
import pandas as pd



#----------------------- Mapeamento dos espaços -----------------------
# Modelagem da cinemática direta usando Denavit-hartenberg
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0],
        ['theta_4',0,0,90,90],
        ['theta_5',18,0,0,0]
]



# Mapeamento do espaço das juntas e o espaço operacional
joins = [[0, 10],[0, 10],[0, 10],[0, 10],[0, 0]]
steps = [10, joins[1][1]//2, joins[2][1]//2, joins[3][1]//2, 1]

dataset = spacemapping.mapping(robo,joins,steps)



#----------------------- Pré-processamento dos dados -----------------------





# Altura negativa
height = 0
dataset = dataprocessing.remove_height(dataset,height)

# Elos negativos
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0]
        ]









