from sklearn.neural_network import MLPRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from kinematicsrobotics.utils.datahandler import Save
from pandas import DataFrame

class Model:
    def __init__(self, model = None, params = None):
        self._model = model
        self._params = params

    @property
    def params(self):
        return self._params
    
    @property
    def model(self):
        return self._model
    
    @classmethod
    def mlp_regressor(cls,*, EPOCHS = 1000, EPOCHS_NOCHANGE = 5, ERROR = 1e-4, early_stopping = True, verbose=True, random_state=42, **kw):
        model = MLPRegressor(
            max_iter = EPOCHS,
            tol = ERROR,
            n_iter_no_change = EPOCHS_NOCHANGE,
            early_stopping = early_stopping,
            verbose = verbose,
            random_state=random_state,
            **kw)
        return cls(model,model.get_params())

    
    def set_model(self,**params):
        self._model.set_params(**params)

    def fit(self,*,x,y):
        self._model =  self._model.fit(x,y)

    def predict(self,*, x):
        return self._model.predict(x)
    
    def __str__(self):
        return f"{self.__class__.__name__}: {[f'{chave}={valor}' for chave,valor in self.__dict__.items()]}"
    

class Cluster:
    def __init__(self, *, data, n_clusters: int = 4, n_init = 'auto', **kw):
        self.kmeans(n_clusters = n_clusters, 
                    n_init = n_init,  
                    **kw)
        
        self.fit(data = data)

    def kmeans(self, *, n_clusters: int = 4, n_init = 'auto', **kw):        
        self._model = KMeans(n_clusters=n_clusters, 
                        random_state=42,
                        n_init = n_init,
                        **kw)
    
    def fit(self, *, data):
        scaler = StandardScaler()
        self._model.fit(scaler.fit_transform(data))

        # Centroides
        self._norm_centroide = self._model.cluster_centers_
        self._centroide = scaler.inverse_transform(self._model.cluster_centers_)

        # Grupos (cluster)
        self.agrupamento()


    def agrupamento(self):
        self._class_cluster = set(self._model.labels_)

        index_clusters = []

        for cluster in self._class_cluster:
            idex_labels = []
            i = 0
            for labels in self._model.labels_:
                if labels == cluster:
                    idex_labels.append(i)
                i +=1
            index_clusters.append(idex_labels)
        
        self._clusters = index_clusters
    
    def save(self, *, columns, path_data_centers, path_data_cluster):
        sv = Save()

        df_labels = DataFrame(self._centroide, columns = columns)
        sv.dataframe(data = df_labels, path_data=path_data_centers)

        df_labels = DataFrame(self._model.labels_)
        sv.dataframe(data = df_labels, path_data=path_data_cluster)
