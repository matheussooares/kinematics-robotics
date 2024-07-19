from numpy import append
from sklearn.metrics import mean_squared_error
from kinematicsrobotics.dataprocessing import Preprocessing
from kinematicsrobotics.kinematics import Robo,Spacemapping
from kinematicsrobotics.model import Model



class Metrics:
    def __init__(self, *, model: Model, preprocessing: Preprocessing, robo: Robo = None):
        self._model = model
        self._datapreprocessing = preprocessing
        self.robotic(robo = robo)
    
    def robotic(self, *, robo: Robo):
        self._robo = robo
        if robo:
            self._mapping = Spacemapping(robo)

    def mse_joint(self, *, x, y):
        y_predict = self.predict_joint(x = x)
        y_real = self._datapreprocessing._scaler_y.inverse_transform(y)
        
        return self.mse(y_real, y_predict)
    
    def mse_operacional(self, *, x):
        x_real = self._datapreprocessing._scaler_x.inverse_transform(x)[:,:3]
        x_estimado = self.predict_operacional(x = x)
        return self.mse(x_real,x_estimado)

    def predict_joint(self, *, x):
        y_predict = self._model.predict(x = x)
        y_predict = self._datapreprocessing._scaler_y.inverse_transform(y_predict)
        return y_predict
    
    def predict_operacional(self, *, x, x_labels = ['p_x','p_y','p_z'], output_format = 'DataFrame'):
        def transfor(array):
            novo_array = []
            for sub_array in array:
                    novo_sub_array = append(sub_array, 0)
                    novo_array.append(novo_sub_array)
            return novo_array
         
        y_predict_join =  self.predict_joint(x = x)
        y_predict_join = transfor(y_predict_join)

        data_operacional = self._mapping.operational_space(y_predict_join, output_format=output_format)

        if output_format=='DataFrame' and x_labels:
            data_operacional = data_operacional[x_labels]
        
        return data_operacional

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