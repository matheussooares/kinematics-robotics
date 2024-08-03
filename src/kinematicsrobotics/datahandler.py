from os import path
import pandas as pd
from matplotlib.pyplot import savefig

class Data:
    def __init__(self):
        self._path_project = path.abspath('')


class Save(Data):
    def __init__(self):
        super().__init__()
        
        
    def dataframe(self, *, data, path_data):
        path_data = path.join(self._path_project, path_data)
        data.to_csv(path_data,index=False)
    
    def figure(self, path_fig):
        savefig(path.join(self._path_project,path_fig))



class Extract(Data):
    def __init__(self):
        super().__init__()

    def dataframe(self, path_data):
        path_data = path.join(self._path_project, path_data)
        return pd.read_csv(path_data)

