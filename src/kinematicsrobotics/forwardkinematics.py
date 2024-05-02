from numpy import array
from numpy import radians as npradians
from sympy import sin, cos, Matrix,symbols, simplify, nsimplify, eye,Symbol
from math import radians


class Elo:
  """
    Clase que define um elo físico do rôbo. Essa representação de elo é descrito 
    por meio dos parâmetros da notação de Denavit-Hartenberg (DH).
    
    Os parâmetros que compõem a classe:
      - theta: Ângulo de rotação em torno do eixo z (graus)
      - d: Distância ao longo do eixo z (cm)
      - a: Comprimento do elo (cm)
      - alpha: Ângulo de rotação em torno do eixo x comum (graus)
      - phase: Fase do ângulo de rotação em torno do eixo z (graus)

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
    
    exemplo:
      Elos = [['theta_1',d_1,a_1,alpha_1,phase_1],
            ['theta_2',d_2,a_2,alpha_2,phase_2]]
    
    Os parâmetros variáveis das juntas rotativa/torcional devem ser definidos como uma string.
    Até o momento só é possível criar robôs com juntas rotativas e torcionais. Os demais valores 
    devem seguir a definição da classe elo.
      - d: Distância ao longo do eixo z (cm)
      - a: Comprimento do elo (cm)
      - alpha: Ângulo de rotação em torno do eixo x comum (graus)
      - phase: Fase do ângulo de rotação em torno do eixo z (graus)
  """
  # Construtor da classe robo
  def __init__(self,nameBot,elos):
    self.nameBot = nameBot
    self.series = self.__series_link(elos)
    self.matrixForwardKinematics = self.__homogeneous_transformations()
    self.joinName = self.__join_names()
    self.__simplifForwardKinematics = None

  # Cria a cadeia cinemática de elos
  def __series_link(self,elos):
    series = []
    for row in elos:
      series.append(Elo(symbols(row[0], real = True),row[1],row[2],row[3],row[4]))
    return series

  # Método privado para criar uma matriz de transformação homogênea de DH genérica
  def __matrix_homogeneous_transformations(self,theta, d, a, alpha):
    alpha = radians(alpha)
    r = 5
    # Matriz TH para a notação denavit-hartenberg
    matrix = Matrix([
            [cos(theta), -sin(theta) * cos(alpha).round(r), sin(theta) * sin(alpha).round(r), a * cos(theta)],
            [sin(theta), cos(theta) * cos(alpha).round(r), -cos(theta) * sin(alpha).round(r), a * sin(theta)],
            [0, sin(alpha).round(r), cos(alpha).round(r), d],
            [0, 0, 0, 1]
        ])
    return matrix

  # Método privado que define a matriz de tranformação total do manipulador
  def __homogeneous_transformations(self):
    # Inicializa a matriz transformação homogênea
    matrix_TH = eye(4)
    # Percorre os elos
    for elo in self.series:
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

  # Método privado que coleta as variáveis das juntas
  def __join_names(self):
    # Declara a variável como um conjunto para que só exista apenas uma varivel
    joinName = []
    # Percorre a cadeia cinemática de elos
    for elo in self.series:
      # Analisa cada atributo da classe elo
      for att,val in elo.__dict__.items():
        # Amazena o nome da variavel do atributo que é uma variável simbólica
        if isinstance(val, Symbol):
          joinName.append(val)
    return joinName

  # Método que retorna a matriz de transform
  def frame_effector(self,pose):
    joinName = self.joinName
    pose = npradians(pose)
    #if len(joinName) == len(pose):
    data = dict(zip(joinName,pose))
    return self.matrixForwardKinematics.evalf(subs=data).tolist()
    #else:
      #print("Número de valores é diferente das variáveis")

