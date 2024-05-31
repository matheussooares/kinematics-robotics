from sklearn.model_selection import ShuffleSplit,RandomizedSearchCV,GridSearchCV
from itertools import product
from sklearn.metrics import mean_squared_error,r2_score
from pandas import DataFrame

# Calcula a porcentagem relativa dos dados de treino e validação
def size_split(size_train,size_val):
    size_val = (1 - size_train/(size_train+size_val))
    return size_val

# Espaço de busca dos neurônios
def space_hidden(min_neurons,max_neurons,layers,step):
    # Lista que armazena os neurônios
    neuron_space = []
    
    # Gera a lista de possíveis números de neurônios em cada camada
    possible_neurons = list(range(min_neurons, max_neurons + 1,step))
    
    # Crie todas as combinações possíveis
    for num_layers in layers:
        neuron_combinations = list(product(possible_neurons, repeat=num_layers))
        neuron_space.extend(neuron_combinations)

    return neuron_space

# Parâmetro da rede mlp
def parameter_mlp(min_neurons,max_neurons,layers,step,func_act): 
    # Dicionário que armazena os hiperparâmetros
    param_grid = {
        'hidden_layer_sizes': space_hidden(min_neurons, max_neurons,layers,step),
        'activation': func_act
    }

    return param_grid

# Random Search
def RandomizedSearch(x, y, model, param_grid, scoring,cv, n_iter):
    # Configura os parâmetros da técnica de otimização 
    random_search = RandomizedSearchCV(estimator=model, 
                                       param_distributions=param_grid, 
                                       scoring=scoring, 
                                       cv=cv, 
                                       n_iter=n_iter, 
                                       random_state=42, 
                                       return_train_score=True,
                                       verbose=0)
    
    # Treina os modelos
    random_search.fit(x, y)

    # DataFrame que armazena os resultado dos hiperparâmetros
    history = DataFrame(random_search.cv_results_)

    # Melhor hiperparâmetro
    best_estimator = random_search.best_estimator_

    return history,best_estimator

# Grid Search
def GridSearch(x, y, model, param_grid, scoring, cv):
    # Configura os parâmetros da técnica de otimização 
    gridshearch = GridSearchCV(estimator=model,
                               param_grid=param_grid,
                               cv=cv,
                               scoring=scoring,
                               verbose=0,
                               return_train_score=True)
    
    # Treina os modelos
    gridshearch.fit(x, y)
    
    # Armazena os resultado dos hiperparâmetros
    history = DataFrame(gridshearch.cv_results_)
    
    best_estimator = gridshearch.best_estimator_

    return history,best_estimator

# Validação cruzada hold out
def holdout(n_splits,test_size):
    return ShuffleSplit(n_splits=n_splits, 
                      test_size=test_size, 
                      random_state=42)
