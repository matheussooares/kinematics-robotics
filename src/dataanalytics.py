from kinematicsrobotics.plottingutils import Plot


# Extração das bases de dados
plot = Plot(path = r'src\data\raw\dataset-semi-raw.csv')

plot.scatter3D(labels=['p_x','p_y','p_z'], 
               name_labels = ['x', 'y', 'z'],
               s=2,
               c='#1a3c7d'
            #    marker = '.'
               
)






