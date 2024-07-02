from kinematicsrobotics.kinematics import Robo, Spacemapping
from kinematicsrobotics import dataprocessing
from kinematicsrobotics.datahandler import Save


# Inicializando a classe save
save = Save()

#----------------------- Mapeamento dos espaços -----------------------

# Modelagem da cinemática direta usando Denavit-hartenberg
Elos = [['theta_1',10,0,90,0],
        ['theta_2',0,18,180,0],
        ['theta_3',0,18,-180,0],
        ['theta_4',0,0,90,90],
        ['theta_5',18,0,0,0]
]

robo = Robo("Robo",Elos)

# Mapeamento do espaço das juntas e o espaço operacional
joins = [[0, 120],[0, 120],[0, 120],[0, 120],[0, 0]]
steps = [5, joins[1][1]//10, joins[2][1]//10, joins[3][1]//10, 1]

mapping = Spacemapping(robo=robo)

dataset = mapping.space_mapping(joins,steps)

# Salvar dados brutos
save.dataframe(dataset, r'src\data\raw\dataset-raw.csv')

#----------------------- Pré-processamento dos dados -----------------------
# incluir as colunas pich, roll e yaw
dataset = dataprocessing.concat_data(
                dataset[['theta_1','theta_2','theta_3','theta_4','theta_5','p_x','p_y','p_z']],
                dataprocessing.rotations(dataset)
)

# Salvar dados brutos
save.dataframe(dataset, r'src\data\raw\dataset-semi-raw.csv')

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

# Removendo redundâncias
radius = [0.5,0.7,1,1.25,1.5]
attr_neighbors = ['p_x','p_y','p_z']
attr_redundancy = ['theta_2','theta_3','theta_4','theta_5']

for radi in radius:
     df_redcy = dataprocessing.remove_redundancy(dataset,radi,attr_neighbors,attr_redundancy) 
     path = f'src\\data\\ready\\dataset-radius-{radi}cm.csv'
     save.dataframe(df_redcy,path)   


