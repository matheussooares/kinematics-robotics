from pandas import DataFrame

def create_dataset(joins,steps,joinName):
    # Criando uma lista para armazenar os dados
    data_join = []
    # Criando a matriz com todas as combinações de ângulos
    for angulo_1 in range(joins[0][0], joins[0][1] + 1, steps[0]):
        for angulo_2 in range(joins[1][0], joins[1][1] + 1, steps[1]):
            for angulo_3 in range(joins[2][0], joins[2][1] + 1, steps[2]):
                for angulo_4 in range(joins[3][0], joins[3][1] + 1, steps[3]):
                    data_join.append([angulo_1, angulo_2, angulo_3, angulo_4, joins[4][0]])
    data = DataFrame(data_join, columns=joinName)
    return data