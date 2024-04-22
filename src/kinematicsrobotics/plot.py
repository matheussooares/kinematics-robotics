import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot2D(df_dataset,labels):
  # Cria uma figura de tamanho n por n
  figura = plt.figure(figsize=(10, 10))

  num_amostra, num_feat = df_dataset.shape

  # Configura o suubplot para gráficos 3D
  grafico = figura.add_subplot(111)

  # Adiciona ao subplot um gráfico de dispersão
  grafico.scatter(df_dataset[labels[0]],df_dataset[labels[1]], s=1, c=np.random.rand(num_amostra), alpha=1, cmap="inferno")

  minimos = df_dataset.min()
  maximos = df_dataset.max()

  grafico.set_xlim(minimos[labels[0]], maximos[labels[0]])
  grafico.set_ylim(minimos[labels[1]], maximos[labels[1]])

  grafico.set_xlabel(labels[0])
  grafico.set_ylabel(labels[1])

  plt.show()

def plot3D(df_dataset,labels):
  # Cria uma figura de tamanho n por n
  figura = plt.figure(figsize=(10, 10))

  num_amostra, num_feat = df_dataset.shape

  # Configura o suubplot para gráficos 3D
  grafico = figura.add_subplot(111, projection='3d')

  # Adiciona ao subplot um gráfico de dispersão
  grafico.scatter(df_dataset[labels[0]],df_dataset[labels[1]],df_dataset[labels[2]], s=1, c=np.random.rand(num_amostra), alpha=1, cmap="inferno")

  minimos = df_dataset.min()
  maximos = df_dataset.max()

  grafico.set_xlim(minimos[labels[0]], maximos[labels[0]])
  grafico.set_ylim(minimos[labels[1]], maximos[labels[1]])
  grafico.set_zlim(minimos[labels[2]], maximos[labels[2]])

  grafico.set_xlabel(labels[0])
  grafico.set_ylabel(labels[1])
  grafico.set_zlabel(labels[2])
  plt.show()