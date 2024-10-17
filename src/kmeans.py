from kinematicsrobotics.utils.datahandler import Extract
from kinematicsrobotics.utils.plottingutils import Plot
from kinematicsrobotics.model import Cluster

ext = Extract()
dataset = ext.dataframe(r'src\data\ready\dataset-radius-1cm.csv')

kmeans = Cluster(data = dataset[['p_x','p_y','p_z']], 
                n_clusters = 4, 
                n_init = 'auto')
#'roll','pich','yaw'

kmeans.save(columns=['p_x','p_y','p_z'],
            path_data_centers = r'src\data\ready\data-r1cm-split-local\centers.csv',
            path_data_cluster = r'src\data\ready\data-r1cm-split-local\cluster.csv',
)

plt = Plot(data = dataset, figsize=(10,30))

plt.scatter3D(labels=['p_x','p_y','p_z'], 
              name_labels=['x','y','z'],
              s = 3,
              cmap="viridis",
              alpha=1,
              c = kmeans._model.labels_)