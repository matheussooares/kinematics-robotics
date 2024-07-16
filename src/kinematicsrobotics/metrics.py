from numpy import append
from sklearn.metrics import mean_squared_error
from dataprocessing import DataPreprocessing
from model import Model



class Metrics:
    def __init__(self, *, model: Model, datapreprocessing: DataPreprocessing):
        self._model = model
        self._datapreprocessing = datapreprocessing
    
    def predict_joint(self, x):
        y_predict = self._model.predict(x)
        y_predict = self._datapreprocessing._scaler_y.inverse_transform(y_predict)
        return y_predict
    
    def predict_operacional(self):
        
        def transfor(array):
            novo_array = []
            for sub_array in array:
                    novo_sub_array = append(sub_array, 0)
                    novo_array.append(novo_sub_array)
            return novo_array




    @staticmethod
    def mse(real, predict):
       return mean_squared_error(real, predict, multioutput='raw_values')
    
    








    #import matplotlib.pyplot as plt
    #from plottingutils import Plot
    # def curve_loss(self):

    #     plt.plot(self._model.loss_curve_)
    #     plt.title('Erro Quadratico')
    #     plt.xlabel('Épocas')
    #     plt.ylabel('MSE')
    #     plt.show()