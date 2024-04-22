from kinematicsrobotics import forwardkinematics as forward
from pandas import DataFrame
from numpy import arctan2,sqrt,cos,sin, array


def remove_height(df_dataset,height):
    # pega os indices que se deseja remover
    idx_remove = df_dataset[df_dataset['p_z']<height].index
    # Remove da base de dados
    df_dataset = df_dataset.drop(idx_remove)
    return df_dataset

def remove_height_join(df_dataset,elos,namebot,namejoins,height):
    # Cria um robô intermediario
    robo = forward.Robo(namebot,elos)
    # Pega apenas as juntas referentes ao robô intermediário
    df_join3 = df_dataset[namejoins]
    
    # Percorre a base de dados 
    for indx,angle in df_join3.iterrows():
        # Se altura alcançada em Z for menor que a desejada
        if (robo.frame_effector(angle)[2][3]) < height:
            # Apaga a linha do dataset
            df_dataset = df_dataset.drop(indx)
    return df_dataset

# Função que retorna os vizinhos próximos em torno de uma raio
def neighbors(amostra, posicoes, raio):
    ## Colocar restrinção se tam(amostra) = tam(posições)
    if len(amostra) == posicoes.shape[1]:
      # Converte a amostra em numpy
      amostra = array(amostra)

      # Calcula a diferença entre a amostra e a base de dados
      diferenca = (posicoes - amostra) ** 2

      # Calcula a distância euclidiana e armazena em um dataframe
      df_distancia = DataFrame(diferenca.sum(axis=1),columns=['Distâncias']).map(sqrt)

      # Retornar é menor ou igual ao raio definido
      return df_distancia[(df_distancia<=raio).all(axis=1)]
    else:
        print("Dimensão errada dos atributos")
        return None

def redundancy(vizinhos,df_dataset):
  # Retorna do dataset os vizinhos próximos
  dataset_join = df_dataset.loc[vizinhos.index]

  if not dataset_join.empty and not vizinhos.empty :
    # Percorre as colunas das juntas dos vizinhos (redundâncias) próximos excluindo (filtrados) os dados
    for col_join in dataset_join.columns:
      # theta_3 pega os indices com os menores angulos
      if col_join == 'theta_3':
        indices = dataset_join.index[dataset_join[col_join] == dataset_join[col_join].min()]
      # C.C pega os indices com os maiores angulos
      else:
        indices = dataset_join.index[dataset_join[col_join] == dataset_join[col_join].max()]
      # caso existir apenas uma amostra
      cond1 = indices.shape[0] == 1
      if cond1:
        # Retorna os indices a serem excluidos
        return  vizinhos.index.difference(indices)
        break
      elif not cond1 and col_join == 'theta_5': # caso persistir a redundância
        # Pega o indice da maior distância dos últimos vizinhos
        indices = vizinhos.loc[indices].idxmax()
        return  vizinhos.index.difference(indices)
        break
      else: # Caso ainda exista muita redundância
        # Remove da analise as amostras não pertinentes
        dataset_join.drop(dataset_join.index.difference(indices),inplace=True)

    else:
      return list([])
    
def remove_redundancy(dataset,radius,attr_neighbors, attr_redundancy):
  # Conjunto que armazena os indices das amostras redundantes
  redund_ind = set()
  # Percorre todos as linhas do dataframe
  for indice in dataset.index:
    # Analisa amostra em seguente a amostra atual
    df = dataset.loc[indice:]
    amostra = dataset.loc[indice]
    # Pega os vizinhos da amostra atual sobre um raio
    vizinhos = neighbors(amostra[attr_neighbors],df[attr_neighbors],radius)
    # Armazena no conjunto os indices das amostras redundântes
    redund_ind.update(redundancy(vizinhos,df[attr_redundancy]))
  return  dataset.drop(redund_ind)


# Cria o pich, roll e yaw a partir da matriz de transformação
def rotations(dataset):
    """
    Converte uma matriz de rotação em ângulos de Euler (pith, roll, yaw).
    
    Args:
    dataframe contendo 
    
    Retorna:
    Dataframe contendo os ângulos de Euler (pith, roll, yaw) em radianos
    """
    colunas=['Roll','Pich','Yaw']
    df = []
    for ind,amostra in dataset.iterrows():
        roll = arctan2(amostra['R_32'],amostra['R_33'])
        yaw = arctan2(amostra['R_21'],amostra['R_11'])
        if cos(yaw) < 1e-16:
            pich = arctan2(-amostra['R_31'],amostra['R_21']/sin(yaw))
        else:
            pich = arctan2(-amostra['R_31'],amostra['R_11']/cos(yaw))
        df.append([roll,pich,yaw])
    df = DataFrame(df,columns = colunas)
    return df