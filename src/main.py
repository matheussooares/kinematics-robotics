from scripts import forwardkinematics as forward
from scripts import preprocessingdatabase
from scripts import plot as plot
import pandas as pd

path = f'src/data/raw/dataset.csv'
dataset = pd.read_csv(path)


#plot.plot3D(dataset,['p_x','p_y','p_z'])


#print(robo.nameBot)