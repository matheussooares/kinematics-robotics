from sklearn.neural_network import MLPRegressor

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
    def mlp_regressor(cls,*, EPOCHS = 1000, EPOCHS_NOCHANGE = 5, ERROR = 1e-4, early_stopping = True, verbose=False, random_state=42, **kw):
        model = MLPRegressor(max_iter = EPOCHS,
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
    
