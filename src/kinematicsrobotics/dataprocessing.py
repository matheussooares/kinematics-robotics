from kinematics import Robo
from numpy import array,arctan2,cos,sin,sqrt
from pandas import concat, DataFrame



class DataTransformation:
   pass

def remove_height(df_dataset,height):
    # pega os indices que se deseja remover
    idx_remove = df_dataset[df_dataset['p_z']<height].index
    # Remove da base de dados
    df_dataset = df_dataset.drop(idx_remove)
    return df_dataset

def remove_height_join(df_dataset,elos,namebot,namejoins,height):
    # Cria um robô intermediario 
    robo = Robo(namebot,elos)
    # Pega apenas as juntas referentes ao robô intermediário
    df_join3 = df_dataset[namejoins]
    
    # Percorre a base de dados 
    for indx,angle in df_join3.iterrows():
        # Se altura alcançada em Z for menor que a desejada
        if (robo.frame(angle)[11]) < height:
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
  """
    Remove amostras redundantes de um conjunto de dados.

    Parameters:
        dataset (pandas.DataFrame): O conjunto de dados a ser analisado.
        raio (float): O raio para considerar vizinhança.
        attr_vizinhos (list): Lista de atributos a serem considerados para determinar vizinhança.
        attr_redundancia (list): Lista de atributos a serem considerados para determinar redundância.

    Returns:
        pandas.DataFrame: O conjunto de dados resultante após remover amostras redundantes.
  """
  # Conjunto que armazena os índices das amostras redundantes
  redund_ind = set()
  
  # Percorre todas as linhas do conjunto de dados
  for indice in dataset.index:
    # Analisa amostra em seguente a amostra atual
    df = dataset.loc[indice:]
    amostra = dataset.loc[indice]
    # Pega os vizinhos da amostra atual sobre um raio
    vizinhos = neighbors(amostra[attr_neighbors],df[attr_neighbors],radius)
    # Armazena no conjunto os indices das amostras redundântes
    redund_ind.update(redundancy(vizinhos,df[attr_redundancy]))
  return  dataset.drop(redund_ind)

def concat_data(df_1,df_2):
  """
    Concatena dois DataFrames horizontalmente.

    Parameters:
        df_1 (pandas.DataFrame): O primeiro DataFrame.
        df_2 (pandas.DataFrame): O segundo DataFrame.

    Returns:
        pandas.DataFrame: O DataFrame resultante da concatenação de df_1 e df_2.
  """
  # Redefine os índices dos DataFrames para evitar índices duplicados
  df_1 = df_1.reset_index(drop=True)
  df_2 = df_2.reset_index(drop=True)
    
  # Concatena os DataFrames horizontalmente
  df_concatenado = concat([df_1, df_2], axis=1)
    
  return df_concatenado

# Cria o pich, roll e yaw a partir da matriz de transformação
def rotations(dataset):
    """
    Converte uma matriz de rotação em ângulos de Euler (pith, roll, yaw).
    
    Args:
    dataframe contendo 
    
    Retorna:
    Dataframe contendo os ângulos de Euler (pith, roll, yaw) em radianos
    """
    colunas=['roll','pich','yaw']
    df = []
    for ind,amostra in dataset.iterrows():
        roll = arctan2(amostra['R_32'],amostra['R_33'])
        yaw = arctan2(amostra['R_21'],amostra['R_11'])
        if cos(yaw) < 1e-6:
            pich = arctan2(-amostra['R_31'],amostra['R_21']/sin(yaw))
        else:
            pich = arctan2(-amostra['R_31'],float(amostra['R_11'])/cos(yaw))
        df.append([roll,pich,yaw])
    df = DataFrame(df,columns = colunas)
    return df

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class DataPreprocessing:
    def __init__(self, *, dataset: DataFrame, x_labels: list = None, y_labels: list = None, size_train = 0.7, size_val = 0.2, size_test = 0.1, normalize = True) -> None:
      self._dataset = dataset
      self.partition(x_labels = x_labels, 
                     y_labels = y_labels)
      self.split(size_train = size_train, 
                 size_val = size_val, 
                 size_test = size_test,
                 normalize = normalize)
      
    @property
    def data_train_test(self):
      return self._x_train, self._x_test, self._y_train, self._y_test

    @property
    def scale(self):
      return self._scaler_x, self._scaler_y
    
    def partition(self , *, x_labels, y_labels):
      self._x_labels = x_labels
      self._y_labels = y_labels

      if self._x_labels and self._y_labels:
        data_partition = []
        axis = [self._x_labels,self._y_labels]
        for axi in axis:
          data_partition.append(array(self._dataset[axi]))
        self._x, self._y = data_partition[0], data_partition[1]
      else:
        self._y, self._x = None, None
      
      return self._y, self._x

    def split(self, *,size_test, size_train = None, size_val = None, normalize = True):
      self._size_train = size_train
      self._size_val = size_val
      self._size_test = size_test

      if self._x and self._y:
        x_train, x_test, y_train, y_test = train_test_split(self._x, self._y, test_size=self._size_test)
        if normalize:
          x_train, x_test, y_train, y_test, scaler_x, scaler_y  = self.zscore(x_train, x_test, y_train, y_test)

      else: 
        x_train, x_test, y_train, y_test, scaler_x, scaler_y = None, None, None, None , None, None
      
      self._x_train, self._x_test, self._y_train, self._y_test, self._scaler_x, self._scaler_y = x_train, x_test, y_train, y_test, scaler_x, scaler_y
    
    @staticmethod
    def zscore(x_train, x_test, y_train, y_test):
      scaler_x = StandardScaler()
      scaler_y = StandardScaler()

      x_train = scaler_x.fit_transform(x_train)
      x_test = scaler_x.transform(x_test)

      y_train = scaler_y.fit_transform(y_train)
      y_test = scaler_y.transform(y_test)

      return x_train, x_test, y_train, y_test, scaler_x, scaler_y
      



from datahandler import Extract

extract = Extract()
path_data = r'src\data\ready\dataset-radius-1.5cm.csv'

dataset  = extract.dataframe(path_data)

data  = DataPreprocessing(dataset = dataset, 
                          x_labels=['p_x', 'p_y','p_z', 'roll', 'pich', 'yaw'],
                          y_labels=['theta_1', 'theta_2', 'theta_3', 'theta_4']
                        )
print(data.data_train_test)

