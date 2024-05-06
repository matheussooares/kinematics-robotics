import os
class save:
    def __init__(self,path_project):
        self.path_project = path_project
        
    def dataframe(self,data,path):
        path_data = os.path.join(self.path_project,path)
        data.to_csv(path_data,index=False)