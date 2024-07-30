from kinematicsrobotics.datahandler import Extract, Save
from pandas import DataFrame
from matplotlib.pyplot import subplots, show, title, tight_layout, figure
from mpl_toolkits.mplot3d import Axes3D
from numpy.random import rand

class Plot:
  def __init__(self,*, data: DataFrame = None, path: str = None, figsize: tuple = (10, 5)):
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
            c=rand(self._tam_data[0]), 
            alpha=alpha, 
            cmap=cmap,
            ** kw)
    show()

  def scatter3D(self,*, labels, s = 1,  cmap="inferno", alpha=1, name_labels, **kw):
    fig = figure(figsize=self._figsize)
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(self._data[labels[0]], 
              self._data[labels[1]], 
              self._data[labels[2]],
              s = s,
              c = rand(self._tam_data),
              alpha=alpha, 
              cmap=cmap,
              **kw
    )

    ax.set_xlabel(name_labels[0])
    ax.set_ylabel(name_labels[1])
    ax.set_zlabel(name_labels[2])
    show()

  def save(self, path):
    self._save.figure(path)

  def __data(self, data, path):
    if data or (isinstance(data, DataFrame) and not data.empty):
      self._data = data
    elif path:
      self._data = self._extract.dataframe(path)


