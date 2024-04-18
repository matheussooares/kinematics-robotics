from scripts import forwardkinematics as forward
from scripts import preprocessingdatabase
from scripts import plot as plot
from scripts import createdataset as cd
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

dataset = cd.mapping(robo,joins,steps)

