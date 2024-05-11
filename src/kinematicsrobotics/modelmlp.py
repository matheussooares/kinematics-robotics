from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor

def predict_mse(model,X_test,Y_test):
    y_predic = model.predict(X_test)
    return mean_squared_error(Y_test, y_predic,multioutput='raw_values')
    
def modelo(hidden):
    func_act = 'tanh'
    model = MLPRegressor(hidden_layer_sizes=hidden,
                        activation=func_act)
