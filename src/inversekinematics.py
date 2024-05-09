from kinematicsrobotics import datahandler

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt


#--------------- Extração e transformação dos dados ---------------------
path_project = r'C:\Users\je7560\Downloads\matheus\kinematics-robotics'
path_data = r'src\data\ready\dataset-radius-0.5cm.csv'

ext = datahandler.extract(path_project)

dataset = ext.dataframe(path_data)

## Dados de entrada e saída do modelo
y = dataset.iloc[:,0:4]
x = dataset.iloc[:,5:11]

## Dados de treino e teste
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

## Normalizando os dados
scaler = StandardScaler()
X = scaler.fit_transform(x_train)
Y = scaler.fit_transform(y_train)
X_test = scaler.fit_transform(x_test)
Y_test = scaler.fit_transform(y_test)


#--------------- Modelos de predição --------------------------
model = MLPRegressor(hidden_layer_sizes=(200,200,200),
                    activation='relu')


## Treinamento 
model.fit(X,Y)

print(f"Melhor erro: {model.best_loss_}\n")

plt.plot(model.loss_curve_)
plt.title('Erro Quadratico')
plt.xlabel('Épocas')
plt.ylabel('MSE')
plt.show()


## Predição
y_predic = model.predict(X_test)

## Métrica
mse = mean_squared_error(Y_test, y_predic)
print(mse)