from datahandler import Extract, Save
from pandas import DataFrame
from matplotlib.pyplot import figure, scatter, show, plot, title, savefig
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import rand

class Plot:
  def __init__(self,*, data: DataFrame = None, path: str = None, figsize: tuple =(20, 20)):
    self._save = Save()
    self._extract = Extract()
    self.__data(data, path)
    self._c = rand(len(self._data))
    self._figsize = figsize

  def plot2D(self,*, labels: list, titulo: str = None, linestyle: str = None, color: str = None, lw: str = None):
    plot(self._data[labels[0]],
         self._data[labels[1]],
         linestyle=linestyle,
         color = color,
         lw = lw)
    title(titulo)
    show()
  
  def scatter2D(self,*, labels,  cmap="inferno", s=1, alpha=1):
    scatter(self._data[labels[0]], 
            self._data[labels[1]], 
            s=s, 
            c=self._c, 
            alpha=alpha, 
            cmap=cmap)
    show()

  def scatter3D(self,*, labels,  cmap="inferno", s=1, alpha=1):
    scatter(self._data[labels[0]], 
            self._data[labels[1]],
            self._data[labels[2]],
            s=s, 
            c=self._c, 
            alpha=alpha, 
            cmap=cmap)
    show()

  def save(self, path):
    self._save.figure(path)
   

  def __data(self, data, path):
    if data or (isinstance(data, DataFrame) and not data.empty):
      self._data = data
    elif path:
      self._data = self._extract.dataframe(path)

# data = {
#     'x': [1, 2, 3, 4],
#     'y': [2, 3, 4, 3]
# }

# plote = Plot(data=DataFrame(data))

# plote.plot2D(labels=['x','y'])
plote = Plot(path=r"src\data\raw\dataset-semi-raw.csv")
plote.scatter3D(labels=['p_x','p_y','p_z'])


  # def scatter2D(self, labels):    
  #   # Cria uma figura
  #   fig = figure(figsize=self._figsize)

  #   scatter(self._data[labels[0]], 
  #               self._data[labels[1]], 
  #               s=self._s, 
  #               c=self._c, 
  #               alpha=self._alpha, 
  #               cmap=self._cmap)

  #   # Define os limites dos eixos
  #   min_vals = df_dataset.min()
  #   max_vals = df_dataset.max()
  #   plt.xlim(min_vals[labels[0]], max_vals[labels[0]])
  #   plt.ylim(min_vals[labels[1]], max_vals[labels[1]])

  #   # Define os rótulos dos eixos
  #   plt.xlabel(labels[0])
  #   plt.ylabel(labels[1])
  #   show()
# self._c = rand(len(self._data))
#fig = figure(figsize=(20,20))
# def plot3D(df_dataset,labels):
#   """
#     Plota um gráfico de dispersão 3D.

#     Parameters:
#         df_dataset (pandas.DataFrame): O conjunto de dados.
#         labels (list): Uma lista contendo os rótulos dos atributos a serem plotados.
#   """
#   # Cria uma figura
#   fig = plt.figure(figsize=(10, 10))
  
#   # Configura o subplot para gráficos 3D
#   ax = fig.add_subplot(111, projection='3d')

#   # Plota o gráfico de dispersão
#   ax.scatter(df_dataset[labels[0]], df_dataset[labels[1]], df_dataset[labels[2]], s=1, c=np.random.rand(len(df_dataset)), alpha=1, cmap="inferno")

#   # Define os limites dos eixos
#   min_vals = df_dataset.min()
#   max_vals = df_dataset.max()
#   ax.set_xlim(min_vals[labels[0]], max_vals[labels[0]])
#   ax.set_ylim(min_vals[labels[1]], max_vals[labels[1]])
#   ax.set_zlim(min_vals[labels[2]], max_vals[labels[2]])

#   # Define os rótulos dos eixos
#   ax.set_xlabel(labels[0])
#   ax.set_ylabel(labels[1])
#   ax.set_zlabel(labels[2])

#   plt.show()