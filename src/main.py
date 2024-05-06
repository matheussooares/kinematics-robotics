from kinematicsrobotics import kinematics
from kinematicsrobotics import dataprocessing
from kinematicsrobotics import spacemapping
from kinematicsrobotics import load
import pandas as pd

# Raiz do diretorio
path_project = r"C:\Users\mathe\OneDrive\Graduação - UFC\Engenharia da Computação\TCC\Códigos e implementações\V.2"
# Inicializando a classe save
save = load.save(path_project)

#----------------------- Mapeamento dos espaços -----------------------
# Modelagem da cinemática direta usando Denavit-hartenberg
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0],
        ['theta_4',0,0,90,90],
        ['theta_5',18,0,0,0]
]

robo = kinematics.Robo("Robo",Elos)

# Mapeamento do espaço das juntas e o espaço operacional
joins = [[0, 10],[0, 10],[0, 10],[0, 10],[0, 0]]
steps = [10, joins[1][1]//2, joins[2][1]//2, joins[3][1]//2, 1]

dataset = spacemapping.mapping(robo,joins,steps)

# Salvar dados brutos
path = r'kinematics-robotics\src\data\raw\dataset-raw.csv'
print(dataset.shape)
save.dataframe(dataset,path)

#----------------------- Pré-processamento dos dados -----------------------
# incluir as colunas pich, roll e yaw
dataset = dataprocessing.concat_data(
    dataset[['theta_1','theta_2','theta_3','theta_4','theta_5','p_x','p_y','p_z']],
    dataprocessing.rotations(dataset)
)

path = r'kinematics-robotics\src\data\raw\dataset-semi-raw.csv' # Salvar dados brutos
save.dataframe(dataset,path)
print(dataset.shape)


# Altura negativa
height = 0
dataset = dataprocessing.remove_height(dataset,height)

# Elos negativos
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0]
        ]

dataset = dataprocessing.remove_height_join(
     dataset,Elos,'bot',['theta_1','theta_2','theta_3'],height)



## Removendo redundâncias
radius = [0.5,0.7,1,1.25,1.5]
attr_neighbors = ['p_x','p_y','p_z']
attr_redundancy = ['theta_2','theta_3','theta_4','theta_5']

for radi in radius:
     df_redcy = dataprocessing.remove_redundancy(dataset,radi,attr_neighbors,attr_redundancy) 
     #print(df_redcy)   

for radi in radius:
     df_redcy = dataprocessing.remove_redundancy(dataset,radi,attr_neighbors,attr_redundancy) 
     path = f'kinematics-robotics\\src\\data\\ready\\dataset-radius-{radi}cm.csv'
     save.dataframe(df_redcy,path)   




# # path = r'C:\Users\mathe\OneDrive\Graduação - UFC\Engenharia da Computação\TCC\Códigos e implementações\V.2\kinematics-robotics\src\data\ready\datasettest_10mm.csv'
# # dataset.to_csv(path,index=False)