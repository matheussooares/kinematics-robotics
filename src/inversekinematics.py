from kinematicsrobotics.datahandler import Extract
from kinematicsrobotics.dataprocessing import Preprocessing
from kinematicsrobotics.model import Model


# Extração das bases de dados
extrator = Extract()

dataset = extrator.dataframe(path_data = r'src\data\ready\dataset-radius-0.5cm.csv')

# Pré-processamento da base de dados
processed_data = Preprocessing(dataset = dataset, 
                               x_labels=['p_x', 'p_y','p_z', 'roll', 'pich', 'yaw'],
                               y_labels=['theta_1', 'theta_2', 'theta_3', 'theta_4']
                               )

x_train, x_test, y_train, y_test = processed_data.data_train_test

# Estimação de hiperparâmetros
history = extrator.dataframe(r'src\data\ready\history.csv')

history_best = history[history['rank_test_score'] == 1]

params = eval(history_best.iloc[0]['params'])

#  Modelos de predição
mlp = Model.mlp_regressor(**params)

# Treinamento
mlp.fit(x = x_train, y = y_train)

y_est = mlp.predict(x = x_train)

print(y_est)

# print(f"Melhor erro: {model.best_loss_}\n")

# # plt.plot(model.loss_curve_)
# # plt.title('Erro Quadratico')
# # plt.xlabel('Épocas')
# # plt.ylabel('MSE')
# # plt.show()

# ## Métrica
# mse = modelmlp.predict_mse(model,X_test,Y_test)
# print(mse)