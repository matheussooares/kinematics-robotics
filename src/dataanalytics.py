from kinematicsrobotics import plot
from kinematicsrobotics import datahandler
# Extração dos dados
path_project = r"C:\Users\mathe\OneDrive\Graduação - UFC\Engenharia da Computação\TCC\Códigos e implementações\V.2"
path_data = r'kinematics-robotics\src\data\raw\dataset-semi-raw.csv'

ext = datahandler.extract(path_project)

dataset_raw = ext.dataframe(path_data)







