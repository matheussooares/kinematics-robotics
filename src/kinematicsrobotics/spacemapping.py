from pandas import DataFrame, concat
from numpy import array 

def joint_space(robo,joins,steps):
    """
        Mapeia o espaço das juntas por meio das permutações possíveis
        dos ângulos das juntas.

        Args:
        - robo (class Robo): instância de um robô fixo com base na notação DH
        - joins (list): limites minimos e máximos de atuação de cada junta
        - steps (list): passo de amostragem dos ângulos de cada junta
        Returns:
        - dataframe: dataframe contendo o espaço das juntas
    """
    # Criando uma lista para armazenar os dados
    data_join = []
    # Criando a matriz com todas as combinações de ângulos
    for angulo_1 in range(joins[0][0], joins[0][1] + 1, steps[0]):
        for angulo_2 in range(joins[1][0], joins[1][1] + 1, steps[1]):
            for angulo_3 in range(joins[2][0], joins[2][1] + 1, steps[2]):
                for angulo_4 in range(joins[3][0], joins[3][1] + 1, steps[3]):
                    data_join.append([angulo_1, angulo_2, angulo_3, angulo_4, joins[4][0]]) 
    return DataFrame(data_join, columns=robo.joinName)

# Mapeia o espaço operacional
def operational_space(robo,data_join):
    labels = ['R_11','R_12','R_13','p_x','R_21','R_22','R_23','p_y','R_31','R_32','R_33','p_z']
    data_operational = []
    for _,pose in data_join.iterrows():
        data_operational.append(array(robo.frame_effector(pose.values)[:3]).reshape(-1))
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