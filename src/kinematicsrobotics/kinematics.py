from numpy import radians
from sympy import sin, cos, Matrix, symbols, simplify, nsimplify, eye, Symbol, rad

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
  def __init__(self,theta,d,a,alpha,phase):
    self.theta = theta
    self.d = d
    self.a = a
    self.alpha = alpha
    self.phase = phase


class Robo:
    def __init__(self, name: str ,parameters: list) -> None:
      self._name = name
      self._parameters = parameters
      self.__series_link()
      self.__homogeneous_transformations()
      self.__joints()

    @property
    def matrixForwardKinematics(self):
      return self._matrixForwardKinematics
    
    @property
    def parameters(self):
      return self._parameters
    
    @property
    def name(self):
       return self._name
    
    @property
    def Joints(self):
      return self._JointVariable


    # Cria a cadeia cinemática de elos
    def __series_link(self):
      """
      Cria uma cadeia cinemática de elos a partir dos parâmetros fornecidos.

      Args:
      None

      Returns:
      None

      Raises:
      None
      """ 
      serieslink = []
      parameter_list = []
      for parameter in self._parameters:
          for value in parameter:
              if isinstance(value, str):
                  parameter_list.append(symbols(value))
              else:
                  parameter_list.append(value)
          
          serieslink.append(Elo(*parameter_list))
          parameter_list.clear()
      
      self._serieslink = serieslink

    # Método privado que define a matriz de tranformação total do manipulador
    def __homogeneous_transformations(self):
      matrix_TH = eye(4)
      for Elo in self._serieslink:
        matrix = self.__matrix_homogeneous(Elo)
        matrix_TH = matrix_TH @ matrix
    
      self._matrixForwardKinematics = matrix_TH

      self.simplify_ForwardKinematics()
    
    # Método que aplica uma simplificação na matriz de transformação 
    def simplify_ForwardKinematics(self):
      self._matrixForwardKinematics = simplify(nsimplify(self._matrixForwardKinematics))
    
    # Método privado que cria uma matriz de transformação homogênea de DH genérica
    def __matrix_homogeneous(self,Elo):
        theta = Elo.theta + rad(Elo.alpha)
        alpha = rad(Elo.alpha)
        matrix = Matrix([
            [cos(theta), -sin(theta) * cos(alpha), sin(theta) * sin(alpha), Elo.a * cos(theta)],
            [sin(theta), cos(theta) * cos(alpha), -cos(theta) * sin(alpha), Elo.a * sin(theta)],
            [0, sin(alpha), cos(alpha), Elo.d],
            [0, 0, 0, 1]
        ])
        return matrix
    
    # Método privado que coleta informações das variáveis de junta
    def __joints(self):
      joins = []
      names = []
      for elo in self._serieslink:
         for _,val in elo.__dict__.items():
            if isinstance(val, Symbol):
              joins.append(val)
              names.append(val.name)
      
      self._JointVariable = joins
      self._JointNames = names
      self._lenjoin = len(joins)
      
    # Método público que retorna a matriz de transformação de um frame
    def frame(self,pose):
      if len(pose) == self._lenjoin:
        pose = radians(pose)
        input = dict(zip(self._JointVariable,pose))
        return self._matrixForwardKinematics.evalf(subs=input)
      else:
         print("Número de entradas inválidos")
       
            
