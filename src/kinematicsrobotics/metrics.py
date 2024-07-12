from sklearn.metrics import mean_squared_error
from dataprocessing import DataPreprocessing
from model import Model



class Metrics:
    def __init__(self, *, model: Model, datapreprocessing: DataPreprocessing):
        self._model = model
        self._datapreprocessing = datapreprocessing
    
    def mse_joint(self):
        self._model.predict()
        pass




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