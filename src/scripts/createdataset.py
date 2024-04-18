from pandas import DataFrame, concat
from numpy import array 

def joint_space(robo,joins,steps):
    # Criando uma lista para armazenar os dados
    data_join = []
    # Criando a matriz com todas as combinações de ângulos
    for angulo_1 in range(joins[0][0], joins[0][1] + 1, steps[0]):
        for angulo_2 in range(joins[1][0], joins[1][1] + 1, steps[1]):
            for angulo_3 in range(joins[2][0], joins[2][1] + 1, steps[2]):
                for angulo_4 in range(joins[3][0], joins[3][1] + 1, steps[3]):
                    data_join.append([angulo_1, angulo_2, angulo_3, angulo_4, joins[4][0]]) 
    return DataFrame(data_join, columns=robo.joinName)

def mapping(robo,joins,steps):
    labels = ['R_11','R_12','R_13','p_x','R_21','R_22','R_23','p_y','R_31','R_32','R_33','p_z']
    data = []
    data_join = joint_space(robo,joins,steps)

    for _,pose in data_join.iterrows():
        data.append(array(robo.frame_effector(pose.values)[:3]).reshape(-1))
        
    return concat([data_join, DataFrame(data,columns=labels)], axis=1)
