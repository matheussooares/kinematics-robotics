from kinematicsrobotics import plottingutils
from kinematicsrobotics import datahandler

# Extração das bases de dados
path_project = r"C:\Users\mathe\OneDrive\Graduação - UFC\Engenharia da Computação\TCC\Códigos e implementações\V.2"
path_data_raw = r'kinematics-robotics\src\data\raw\dataset-semi-raw.csv'
path_data = r'kinematics-robotics\src\data\ready\dataset-radius-1cm.csv'

ext = datahandler.extract(path_project)

dataset_raw = ext.dataframe(path_data_raw)


# Gráfico do espaço operacional bruto

# plottingutils.plot2D(dataset_raw,['p_x','p_y'])
# plottingutils.plot2D(dataset_raw,['p_x','p_z'])
# plottingutils.plot2D(dataset_raw,['p_y','p_z'])


# plottingutils.plot3D(dataset_raw,['p_x','p_y','p_z'])

# Gráfico do espaço operacional filtrados
dataset = ext.dataframe(path_data)
plottingutils.plot3D(dataset,['p_x','p_y','p_z'])






