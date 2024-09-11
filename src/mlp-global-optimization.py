from kinematicsrobotics.datahandler import Extract
from kinematicsrobotics.dataprocessing import Preprocessing
from kinematicsrobotics.model import Model
from kinematicsrobotics.crossvalidation import ParameterSearchMLP

# Base de dados
ext = Extract()

dataset = ext.dataframe(r'src\data\ready\dataset-radius-1cm.csv')

# Divisão dos dados
size_train, size_val, size_test = 0.7, 0.2, 0.1

data  = Preprocessing(dataset = dataset, 
                      x_labels=['p_x', 'p_y','p_z', 'roll', 'pich', 'yaw'],
                      y_labels=['theta_1', 'theta_2', 'theta_3', 'theta_4'],
                      path_data_split = r'src\data\ready\data-r1cm-split'
)


x_train, x_test, y_train, y_test = data.data_train_test


# Modelo
mlp = Model.mlp_regressor()

# Espaço de busca do grid search
min_neurons= [20, 100, 100, 100]
max_neurons = [6000, 500, 500, 400]
step = [5, 10, 35, 55]
layers = [1, 2, 3, 4]
activation =  ['relu', 'tanh']


cv = ParameterSearchMLP(min_neurons = min_neurons, 
                        max_neurons = max_neurons, 
                        num_layers = layers, 
                        step = step,
                        model = mlp,
                        activation = activation,
                        x_train = x_train,
                        y_train = y_train,
                        n_splits = 2
)

# Métricas de avaliação
scoring = {
    'r2': 'r2',  # Coeficiente de Determinação
    'neg_mse': 'neg_mean_squared_error',  # Erro Quadrático Médio Negativo
}

best_estimator = cv.RandomizedSearch(scoring = scoring,
                                     refit='neg_mse', 
                                     n_iter = 2000, 
                                     path_cv_results = r'src\data\history\parametersearch-mlp-global\cv_results.csv', 
                                     path_best_params = r'src\data\history\parametersearch-mlp-global\best_params.csv',
                                     
)