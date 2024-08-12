from kinematicsrobotics.datahandler import Save
from kinematicsrobotics.model import Model
from pandas import DataFrame
from itertools import product
from sklearn.model_selection import ShuffleSplit, RandomizedSearchCV, GridSearchCV

class ParameterOptimizer:
    
    def __init__(self, *, model: Model, x_train, y_train, size_train = 0.7, size_val =  0.1, size_test = 0.2, n_splits: int = 4) -> None:
        self._save = Save()
        self._model = model
        self._x = x_train
        self._y = y_train
        self.size_validation(size_train = size_train, 
                             size_val = size_val,
                             size_test = size_test
        )
        self.holdout(n_splits = n_splits)
    
    # Método público que define a divisão dos dados de treino e validação
    def size_validation(self, *, size_train, size_val, size_test):
        self._size_val = (1 - size_train/(size_train+size_val))
        self._size_train = 1 - self._size_val
        self._size_test = size_test

    # Validação cruzada hold out
    def holdout(self, *, n_splits = 4):
        self._n_splits = n_splits
        
        self._cv = ShuffleSplit(n_splits=n_splits, 
                                test_size = self._size_val, 
                                random_state=42
        )
    
       
class ParameterSearchMLP(ParameterOptimizer):
    def __init__(self, *, min_neurons: int, max_neurons: int, num_layers: int, step: int, activation, **kw) -> None:
        self._min_neurons = min_neurons
        self._max_neurons = max_neurons
        self._num_layers = num_layers
        self._step = step
        self._activation = activation
        self.parameter()
        super().__init__(**kw)


    def RandomizedSearch(self,*, scoring = 'neg_mean_squared_error', n_iter, path_cv_results = None, path_best_params = None, **kw):
        # Configura os parâmetros da técnica de otimização 
        random_search = RandomizedSearchCV(estimator = self._model.model, 
                                           param_distributions = self.param_grid, 
                                           scoring = scoring, 
                                           cv = self._cv, 
                                           n_iter = n_iter, 
                                           random_state = 42, 
                                           return_train_score = True,
                                           verbose = True,
                                           **kw
        )
        
        # Treina os modelos
        random_search.fit(self._x, self._y)

        # DataFrame que armazena os resultado dos hiperparâmetros
        history = DataFrame(random_search.cv_results_)

        best_params = DataFrame(random_search.best_params_)

        if path_cv_results:
            self._save.dataframe(data = history, path_data = path_cv_results)
        
        if path_best_params:
            self._save.dataframe(data = best_params, path_data = path_best_params)

        # Melhor hiperparâmetro       

        return random_search.best_estimator_
    
    def parameter(self):
        param_grid = []
        
        for i, layers in enumerate(self._num_layers):
            hidden_layer = self.space_hidden(layers = layers, 
                                             min_neurons = self._min_neurons[i], 
                                             max_neurons = self._max_neurons[i], 
                                             step = self._step[i]
            )

            param = { 
                'hidden_layer_sizes': hidden_layer,
                'activation': self._activation
            }

            param_grid.append(param)
 
        self.param_grid = param_grid
            

    def space_hidden(self,*, layers, min_neurons, max_neurons, step):    
        # Gera a lista de possíveis números de neurônios em cada camada
        possible_neurons = list(range(min_neurons, max_neurons + 1, step))

        return list(product(possible_neurons, repeat=layers))

    