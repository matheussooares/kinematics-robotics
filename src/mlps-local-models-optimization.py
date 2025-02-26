from kinematicsrobotics.utils.datahandler import Save, Extract
from kinematicsrobotics.machinelearning.model import Model, Cluster, LocalModels
from kinematicsrobotics.processing.dataprocessing import Preprocessing
from kinematicsrobotics.machinelearning.crossvalidation import ParameterSearchMLP
    
# Extrai os dados     
extrator = Extract()
dataset = extrator.dataframe(r'src\data\ready\dataset-radius-1cm.csv')
# Particiona os dados em regiões para os modelos locais
kmeans = Cluster(
    data = dataset[['p_x','p_y','p_z']], 
    n_clusters = 4, 
    n_init = 'auto'
)
# Gera os dados divididos entre treino e teste
data  = Preprocessing(
    dataset = dataset, 
    x_labels=['p_x', 'p_y','p_z', 'roll', 'pich', 'yaw'],
    y_labels=['theta_1', 'theta_2', 'theta_3', 'theta_4'],
    size_train = 0.7, 
    size_val = 0.2, 
    size_test = 0.1,
    path_data_split = r'src\data\splits\data-r1cm-split-local'
)
# Pega os dados de treinamento e teste
x_train, x_test, y_train, y_test = data.data_train_test

# Cria os modelos locais
modelos = LocalModels(
    cluster = kmeans,
    data = dataset,
    early_stopping = True, 
    EPOCHS = 1000, 
    EPOCHS_NOCHANGE = 10,
    random_state = 42, 
    verbose = True
)
# Define o Espaço de busca do grid search
min_neurons= [20, 100, 100]
max_neurons = [6000, 500, 500]
step = [5, 10, 35, 5]
layers = [1, 2, 3]
activation =  ['relu', 'tanh']

# Métricas de avaliação
scoring = {
    'r2': 'r2',  # Coeficiente de Determinação
    'neg_mse': 'neg_mean_squared_error',  # Erro Quadrático Médio Negativo
}
i = 0
# Percorre os modelos
for label, modelo in modelos.models.items():
    # Armazena os hiperrâmetros
    cv_models = dict()
    # Semente aleatoria
    random_state = 42 + i
    i = i + 1
    # Aplicando a seleção de hiperparâmetros
    cv_models[label] = ParameterSearchMLP(
        min_neurons = min_neurons, 
        max_neurons = max_neurons, 
        num_layers = layers, 
        step = step,
        model = modelo,
        activation = activation,
        x_train = x_train,
        y_train = y_train,
        n_splits = 2, 
        random_state=random_state
    )

    best_estimator = cv_models[label].RandomizedSearch(
        scoring = scoring,
        refit='neg_mse', 
        n_iter = 1000, 
        path_cv_results = f'src\data\history\parametersearch-mlp-local\cv results model {label}.csv', 
        path_best_params = f'src\data\history\parametersearch-mlp-local\\best params  model {label}.csv',
        random_state = random_state                           
    )
    
    
    

# modelos.fit(x = x_train, y = y_train)

# print(modelos.predict(x = x_train))