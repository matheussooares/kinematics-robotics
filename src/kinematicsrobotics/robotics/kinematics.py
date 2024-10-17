from sympy import sin, cos, Matrix, symbols, simplify, nsimplify, eye, Symbol, rad, latex
from pandas import DataFrame, concat
from itertools import product
from numpy import radians

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
        theta = Elo.theta + rad(Elo.phase)
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
    def frame(self, pose: list):
      if len(pose) == self._lenjoin:
        pose = radians(pose)
        input = dict(zip(self._JointVariable,pose))
        return self._matrixForwardKinematics.evalf(subs=input)
      else:
         print("Número de entradas inválidos")
    
    def latex(self):
       return latex(self._matrixForwardKinematics)
            
       
            
class Spacemapping:
    def __init__(self, robo: Robo) -> None:
        self._robo = robo
        self._LABELSJOINS = self._robo._JointNames
        self._LABELSOPERATIONAL =  ['R_11','R_12','R_13','p_x','R_21','R_22','R_23','p_y','R_31','R_32','R_33','p_z']

    # Mapeia o espaço da juntas
    def joint_space(self, joins: list, steps: list):
        ranges = [list(range(joins[i][0], joins[i][1] + 1, steps[i])) for i in range(len(joins))]
        
        all_combinations = list(product(*ranges))
        
        data_join = [list(comb) for comb in all_combinations]
        return data_join

    # Mapeia o espaço operacional
    def operational_space(self, data_join: list[list], n_atributos=12, output_format: str = 'list'):
        data = []
        for pose in data_join:
            matrix = self._robo.frame(pose)
            data.append(self.float(matrix[:n_atributos]))
        if output_format == 'DataFrame':
          data = DataFrame(data,columns=self._LABELSOPERATIONAL)
        return data

    # Relaciona os espaços mapeados melhorado
    def space_mapping(self, joins: list, steps: list, n_atributos=12):
        data_joint = self.joint_space(joins, steps) 
        data_operational = self.operational_space(data_joint, n_atributos)
       
        return self.dataframe(data_operational, data_joint)
    
    # Cria um dataframe
    def dataframe(self, data_operational, data_joint):
        df_operacional = DataFrame(data_operational, columns=self._LABELSOPERATIONAL)
        df_joint = DataFrame(data_joint, columns=self._LABELSJOINS)

        return concat([df_joint,df_operacional], axis=1)
    
    # Tranforma os dados em float
    def float(self, list):
        list_float = [float(val) for val in list] 
        return list_float