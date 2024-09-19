from kinematicsrobotics.datahandler import Extract, Save
from pandas import DataFrame
from matplotlib.pyplot import subplots, show, title, axes, figure
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import rand
import seaborn as sns

class Plot:
  def __init__(self,*, data: DataFrame = None, path: str = None, figsize: tuple = (8, 8)):
    self._save = Save()
    self._extract = Extract()
    self.__data(data, path)
    self._tam_data = len(self._data)
    self._figsize = figsize

  def plot2D(self,*, labels: list, path: str = None,titulo: str = None, ** kw):
    fig, grafico = subplots(nrows=1, ncols=1, figsize = self._figsize)
    grafico.plot(self._data[labels[0]],
                self._data[labels[1]],
                **kw)
    title(titulo)
    if path:
      self.save(path)

    show()
    
  
  def scatter2D(self,*, labels,  cmap="inferno", s=1, alpha=1 ,** kw):
    fig, grafico = subplots(nrows=1, ncols=1, figsize = self._figsize)
    grafico.scatter(self._data[labels[0]], 
            self._data[labels[1]], 
            s=s,
            alpha=alpha, 
            cmap=cmap,
            ** kw)
    show()

  def scatter3D(self,*, labels: list, s = 1, alpha=1, name_labels: list = None, **kw):
    # sns.set_theme(style = "whitegrid")
    fig = figure(figsize=self._figsize)
    ax = axes(projection='3d')

    if not name_labels:
      name_labels = labels

    scatter = ax.scatter(self._data[labels[0]], 
                         self._data[labels[1]], 
                         self._data[labels[2]],
                         s = s,
                         alpha=alpha,
                         **kw
    )
    color = '#D3D3D3'
    # Melhorando a grade
    ax.grid(True)  # Ativando a grade
    ax.xaxis._axinfo["grid"].update(color = color, linestyle = '-', linewidth = 0.7, alpha = 0.1)  # Grid no eixo X
    ax.yaxis._axinfo["grid"].update(color = color, linestyle = '-', linewidth = 0.7, alpha = 0.1)  # Grid no eixo Y
    ax.zaxis._axinfo["grid"].update(color = color, linestyle = '-', linewidth = 0.7, alpha = 0.1)  # Grid no eixo Z


    ax.set_xlabel(name_labels[0])
    ax.set_ylabel(name_labels[1])
    ax.set_zlabel(name_labels[2])

    
    show()

  def save(self, path):
    self._save.figure(path)

  def __data(self, data, path):
    if (isinstance(data, DataFrame) and not data.empty):
      self._data = data
    elif path:
      self._data = self._extract.dataframe(path)


