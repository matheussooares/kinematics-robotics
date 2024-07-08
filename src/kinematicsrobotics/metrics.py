from sklearn.metrics import mean_squared_error
from plottingutils import Plot
from model import Model



class Metrics:
    def __init__(self, *, model: Model):
        self._model = model

    def mse(self, x, y):
       return mean_squared_error(x, y, multioutput='raw_values')
    
    # def mse_real(self):
    








    #import matplotlib.pyplot as plt
    # def curve_loss(self):

    #     plt.plot(self._model.loss_curve_)
    #     plt.title('Erro Quadratico')
    #     plt.xlabel('Épocas')
    #     plt.ylabel('MSE')
    #     plt.show()