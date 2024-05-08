import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def plot2D(df_dataset,labels):
  """
    Plota um gráfico de dispersão 2D.

    Parameters:
        df_dataset (pandas.DataFrame): O conjunto de dados.
        labels (list): Uma lista contendo os rótulos dos atributos a serem plotados.
  """
  # Cria uma figura
  fig = plt.figure(figsize=(10, 10))

  # Configura o subplot para gráficos 2D
  ax = fig.add_subplot(111)

  # Plota o gráfico de dispersão
  ax.scatter(df_dataset[labels[0]], df_dataset[labels[1]], s=1, c=np.random.rand(len(df_dataset)), alpha=1, cmap="inferno")

  # Define os limites dos eixos
  min_vals = df_dataset.min()
  max_vals = df_dataset.max()
  ax.set_xlim(min_vals[labels[0]], max_vals[labels[0]])
  ax.set_ylim(min_vals[labels[1]], max_vals[labels[1]])

  # Define os rótulos dos eixos
  ax.set_xlabel(labels[0])
  ax.set_ylabel(labels[1])
  plt.show()


def plot3D(df_dataset,labels):
  """
    Plota um gráfico de dispersão 3D.

    Parameters:
        df_dataset (pandas.DataFrame): O conjunto de dados.
        labels (list): Uma lista contendo os rótulos dos atributos a serem plotados.
  """
  # Cria uma figura
  fig = plt.figure(figsize=(10, 10))
  
  # Configura o subplot para gráficos 3D
  ax = fig.add_subplot(111, projection='3d')

  # Plota o gráfico de dispersão
  ax.scatter(df_dataset[labels[0]], df_dataset[labels[1]], df_dataset[labels[2]], s=1, c=np.random.rand(len(df_dataset)), alpha=1, cmap="inferno")

  # Define os limites dos eixos
  min_vals = df_dataset.min()
  max_vals = df_dataset.max()
  ax.set_xlim(min_vals[labels[0]], max_vals[labels[0]])
  ax.set_ylim(min_vals[labels[1]], max_vals[labels[1]])
  ax.set_zlim(min_vals[labels[2]], max_vals[labels[2]])

  # Define os rótulos dos eixos
  ax.set_xlabel(labels[0])
  ax.set_ylabel(labels[1])
  ax.set_zlabel(labels[2])

  plt.show()