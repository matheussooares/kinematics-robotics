from scripts import forwardkinematics as forward
from scripts import preprocessingdatabase
from scripts import plot as plot
import pandas as pd

# Define os parâmetros DH para cada elo
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0]
        ]

# Cria o robo por meio dos parâmetros
path = f'C:/Users/je7560/Downloads/dataset.csv'
dataset = pd.read_csv(path)


plot.plot3D(dataset,['p_x','p_y','p_z'])


#print(robo.nameBot)