from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from kinematicsrobotics.datahandler import Save, Extract
from kinematicsrobotics.plottingutils import Plot


ext = Extract()
dataset = ext.dataframe(r'src\data\ready\dataset-radius-1cm.csv')

scaler = StandardScaler()
kmeans = KMeans(n_clusters=8, 
                random_state=42,
                n_init = 'auto')

#,'roll','pich','yaw'
kmeans.fit(scaler.fit_transform(dataset[['p_x','p_y','p_z']]))

plt = Plot(data = dataset, figsize=(10,30))

plt.scatter3D(labels=['p_x','p_y','p_z'], 
              name_labels=['x','y','z'],
              s = 3,
              cmap="viridis",
              alpha=1,
              c = kmeans.labels_)