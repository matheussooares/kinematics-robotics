from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

def predict_mse(model,X_test,Y_test):
    y_predic = model.predict(X_test)
    return mean_squared_error(Y_test, y_predic,multioutput='raw_values')

def curve_loss(model):
    plt.plot(model.loss_curve_)
    plt.title('Erro Quadratico')
    plt.xlabel('Épocas')
    plt.ylabel('MSE')
    plt.show()