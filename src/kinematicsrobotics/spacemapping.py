from pandas import DataFrame, concat
from itertools import product
from numpy import array 

def joint_space(joins, steps):
    # Gerar listas de ângulos para cada junta
    ranges = [list(range(joins[i][0], joins[i][1] + 1, steps[i])) for i in range(len(joins))]
    
    # Criar todas as combinações possíveis
    all_combinations = list(product(*ranges))
    
    # Adicionar as combinações à lista de dados
    data_join = [list(comb) for comb in all_combinations]
    return data_join

# Mapeia o espaço operacional
def operational_space(robo,data_join):
    labels = ['R_11','R_12','R_13','p_x','R_21','R_22','R_23','p_y','R_31','R_32','R_33','p_z']
    data_operational = []
    for _,pose in data_join.iterrows():
        matrix = floats_convert(robo.frame_effector(pose.values)[:3])
        data_operational.append(array(matrix).reshape(-1))

    
    return DataFrame(data_operational,columns=labels)

# Relaciona os espaços mapeados melhorado
def mapping(robo,joins,steps):
    data_join = joint_space(robo,joins,steps) 
    data_operational = operational_space(robo,data_join)
    return concat([data_join,data_operational], axis=1)

def floats_convert(matrix):
    """
    Converte uma lista de valores simbólicos para floats.

    Args:
    - frame (list): A lista contendo os valores simbólicos.

    Returns:
    - list: Uma nova lista com os valores convertidos para floats.
    """
    list_float = [[float(val) for val in row] for row in matrix]
    return list_float