from kinematicsrobotics.plottingutils import Plot
from kinematicsrobotics.datahandler import Extract
# Extração das bases de dados
path_raw = r'src\data\raw\dataset-semi-raw.csv'
path_1cm = r'src\data\ready\dataset-radius-1cm.csv'

ext = Extract()
data_raw = ext.dataframe(path_raw)
data_1cm = ext.dataframe(path_1cm)

# plot = Plot(data = data_raw)

# plot.scatter3D(labels=['p_x','p_y','p_z'], 
#                name_labels = ['x', 'y', 'z'],
#                s=2,
#                c='#1a3c7d'
# )



plot = Plot(data = data_1cm)

plot.scatter3D(labels=['p_x','p_y','p_z'], 
               name_labels = ['x', 'y', 'z'],
               dataset_ext= data_raw,
               s=4,
               c='#1a3c7d'
)






