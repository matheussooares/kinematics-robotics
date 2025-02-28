from kinematicsrobotics.utils.datahandler import Save
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
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
            **kw
        )
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
        # Configura o modelo para divisões dos grupos usando o método k-means
        self.kmeans(
            n_clusters = n_clusters, 
            n_init = n_init,  
            **kw
        )
        # Treina os modelos 
        self.fit(data = data)

    def kmeans(self, *, n_clusters: int = 4, n_init = 'auto', **kw): 
        # Define um modelo K-means dado as configurações do biblioteca 
        self._model = KMeans(
            n_clusters = n_clusters, 
            random_state = 42,
            n_init = n_init,
            **kw
        )
    
    def fit(self, *, data):
        # Inicializa o método de normzalização dos dados
        scaler = StandardScaler()
        # Normaliza os dados
        data_normalizados = scaler.fit_transform(data)
        # Treina o método de agrupamento usando os dados 
        self._model.fit(data_normalizados)
        # Armazena os centroides normalizados
        self._norm_centroide = self._model.cluster_centers_
        # Armazena os centroides dos dados
        self.centroides = scaler.inverse_transform(self._model.cluster_centers_)
        # Agrupa os 
        self.cluster_indices = self.clusters(x_features=data_normalizados)

    def clusters(self, x_features):
        """Função que agrupa a base de dados fornecida. 

        Args:
            x_features (_type_): Dados que seram agrupados

        Returns:
            _type_: Retorna um dicionário contendo os indices da base de dados referente a acda agrupamento
        """
        # Capta todas as labels dos agrupamentos
        self._labels_cluster = set(self._model.labels_)
        # dicionoario que contem os de índices da base de dados dos agrupamento
        index_clusters = dict()
        # Prediz qual o cluster de cada vetor dos dados
        cluster_predict = self._model.predict(x_features)
        
        # Percorre as predições dos cluster e armazena os índices dos dados por cada grupo 
        for cluster in self._labels_cluster:
            # Armazena os índices da grupo atual
            idex_labels = []
            i = 0
            # Armazena as indices da labels 
            for labels in cluster_predict:
                # Se o label atual for igual a label do grupo selecionado
                if labels == cluster:
                    idex_labels.append(i)
                i +=1
                # Armazena todos os indices da base de dados correspondente ao label atual  
            index_clusters[cluster] = idex_labels
        
        return index_clusters
    
    def save(self, *, columns, path_data_centers, path_data_cluster):
        sv = Save()

        df_labels = DataFrame(self._centroide, columns = columns)
        sv.dataframe(data = df_labels, path_data=path_data_centers)

        df_labels = DataFrame(self._model.labels_)
        sv.dataframe(data = df_labels, path_data=path_data_cluster)

class LocalModels:
    def __init__(self, *, data, n_clusters = None, cluster = None, **kw):
        # define o modelo de agrupamento
        self.cluster(data = data, n_clusters = n_clusters, cluster = cluster)
        # Configura os modelos com os parâmetros fixos
        self.set_models(**kw)
        
    def cluster(self, data, n_clusters = None, cluster = None):
        # Gera a divisão do espaço pelo método do kmeans caso não exista
        if cluster == None and n_clusters != None:
            # Cria um modelo local
            self._cluster = Cluster(
                data = data,
                n_clusters=n_clusters
            )
        elif isinstance(cluster, Cluster):
            # se ja existe uma divisão apenas armazena o método
            self._cluster = cluster
        else:
            self._cluster = None       

    def set_models(self, **kw):
        # Cria o modelo local
        models = dict()
        # Configura cada modelo de aprendizado
        for cluster in self._cluster._labels_cluster:
            models[cluster] = Model.mlp_regressor(**kw)
        # Salva na classe
        self.models = models
    
    def fit(self, x, y):
        # Pega o número de features usadas no treinamento do agrupamento
        num_features_clusters = self._cluster._model.cluster_centers_.shape[1]
        # Prediz qual o cluster das features
        predict_cluster = self._cluster.clusters(x[:,:num_features_clusters])
        # Percorre os dados agrupados para treinar os modelos locais
        for cluster, indices_dados in predict_cluster.items():
            self.models[cluster].fit(
                x = x[indices_dados],
                y = y[indices_dados]
            )
    
    def predict(self, *, x):
        # Dicionário que armazenará as predições
        predict_model = dict()
        # Pega o número de features usadas no treinamento do agrupamento
        num_features_clusters = self._cluster._model.cluster_centers_.shape[1]
        # Prediz qual o cluster das features
        predict_cluster = self._cluster.clusters(x[:,:num_features_clusters])
        # Percorre os dados agrupados para treinar o modelo
        for cluster, indices_dados in predict_cluster.items():
            predict_model[cluster] = self.models[cluster].predict(
                x = x[indices_dados]
            )
        return predict_model