from numpy import array
from numpy import radians as npradians
from sympy import sin, cos, Matrix,symbols, simplify, nsimplify, eye,Symbol
from math import radians


class Elo:
  """
    Classe que define um elo físico do rôbo. Essa representação de elo é descrito 
    por meio dos parâmetros da notação de Denavit-Hartenberg (DH).
    
    Os parâmetros que compõem a classe:
      - theta: ângulo de rotação em torno do eixo z (graus)
      - d: distância ao longo do eixo z (cm)
      - a: comprimento do elo (cm)
      - alpha: ângulo de rotação em torno do eixo x comum (graus)
      - phase: fase do ângulo de rotação em torno do eixo z (graus)

    Exemplo:
      import sympy

      theta = sympy.symbols('theta')

      elo = Elo(theta,10,0,90,0)    
  """
  # Construtor da classe Elo
  def __init__(self,theta,d,a,alpha,phase):
    self.theta = theta
    self.d = d
    self.a = a
    self.alpha = alpha
    self.phase = phase

class Robo:
  """
    Classe que define um robô seguindo a notação de Denavit-Hartenberg (DH). 

    Os parâmetros para a construção da classe:
      - nameBot: nome do robô
      - elos: lista com os parâmetros DH de cada elo seguindo a ordem do exemplo abaixo.
              Elos = [['theta_1',d,a,alpha,phase]]
    
    Os parâmetros variáveis das juntas rotativa/torcional devem ser definidos como uma string.
    Até o momento só é possível criar robôs com juntas rotativas e torcionais. Os demais valores 
    devem seguir a definição da classe elo.
      - d: distância ao longo do eixo z (cm)
      - a: comprimento do elo (cm)
      - alpha: ângulo de rotação em torno do eixo x comum (graus)
      - phase: fase do ângulo de rotação em torno do eixo z (graus)

    Exemplo:
      Elos = [['theta_1',10,0,90,0],
              ['theta_2',0,18,180,0]]

      robo = Robo('NomeRobo',Elos)
  """
  # Construtor da classe robo
  def __init__(self,nameBot,parameters):
    self.nameBot = nameBot
    self.parameters = parameters
    self.serieslink = self.__series_link(parameters)
    self.matrixForwardKinematics = self.__homogeneous_transformations()
    self.__joinVar = self.__join_var()
    self.joinName = self.__join_name()
    self.__simplifForwardKinematics = None

  # Cria a cadeia cinemática de elos
  def __series_link(self,parameters):
    # Lista de classe Elos
    series = []
    # Armazena na lista as classes elos
    for row in parameters:
      series.append(Elo(symbols(row[0], real = True),row[1],row[2],row[3],row[4]))
    return series

  # Cria uma matriz de transformação homogênea de DH genérica
  def __matrix_homogeneous_transformations(self,theta, d, a, alpha):
    # Converte o dado em radianos
    alpha = radians(alpha)
    # Matriz TH para a notação denavit-hartenberg
    matrix = Matrix([
            [cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), a * cos(theta)],
            [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), a * sin(theta)],
            [0, sin(alpha), cos(alpha), d],
            [0, 0, 0, 1]
    ])
    return matrix

  # Método privado que define a matriz de tranformação total do manipulador
  def __homogeneous_transformations(self):
    # Inicializa a matriz transformação homogênea
    matrix_TH = eye(4)
    # Muiltiplica cada matriz DH simbolica
    for elo in self.serieslink:
      matrix = self.__matrix_homogeneous_transformations(elo.theta+radians(elo.phase),elo.d,elo.a,elo.alpha)
      matrix_TH = matrix_TH @ matrix
    return matrix_TH

  # Método público que exibe e seta a matriz de transformação no formato reduzida
  def show_matrix_ForwardKinematics(self):
    # Simplifica uma unica vez e exibe nas proximas vezes a matriz homogenia
    if self.__simplifForwardKinematics is None:
      self.__simplifForwardKinematics = simplify(nsimplify(self.matrixForwardKinematics))
      self.matrixForwardKinematics = self.__simplifForwardKinematics
      return self.__simplifForwardKinematics
    else:
      return self.__simplifForwardKinematics

  # Método privado que coleta as variáveis simbólicas das juntas
  def __join_var(self):
    # Declara a variável como um conjunto para que só exista apenas uma varivel
    joinName = []
    # Percorre a cadeia cinemática de elos
    for elo in self.serieslink:
      # Analisa cada atributo da classe elo
      for att,val in elo.__dict__.items():
        # Amazena o nome da variavel do atributo que é uma variável simbólica
        if isinstance(val, Symbol):
          joinName.append(val)
    return joinName
  
  # Método que retorna o nome da variável
  def __join_name(self):
    joinVar = self.__joinVar
    joinName = []
    for var in joinVar:
      joinName.append(var.name)
    return joinName

  # Método que retorna a matriz de transform
  def frame_effector(self,pose):
    joinName = self.__joinVar
    pose = npradians(pose)
    if len(joinName) == len(pose):
      data = dict(zip(joinName,pose))
      return self.matrixForwardKinematics.evalf(subs=data).tolist()
    else:
      print("Número de valores é diferente das variáveis")

