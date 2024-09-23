import roboticstoolbox as rtb
import matplotlib.pyplot as plt
from math import pi  # Importa o valor de pi

# ---------Parâmetros DH----------
# theta, d, a, alpha
L1 = rtb.RevoluteDH(d=0.1, a=0, alpha=pi/2, offset = 0)   # Criando elo 0
L2 = rtb.RevoluteDH(d=0, a=0.18, alpha=pi, offset = 0)     # Criando elo 1
L3 = rtb.RevoluteDH(d=0, a=0.18, alpha=-pi, offset = 0)     # Criando elo 2
L4 = rtb.RevoluteDH(d=0, a=0, alpha=pi/2, offset = pi/2)     # Criando elo 3
L5 = rtb.RevoluteDH(d=0.18, a=0, alpha=0, offset = 0)     # Criando elo 4

# ---------Criação do robô----------
robo = rtb.DHRobot([L1, L2, L3, L4, L5])

# Ângulos predefinidos
qf0 = [[0, 0, 0, 0, 0], [0, 7*pi/36, 5*pi/9, 7*pi/18, 0]]


# Interface gráfica teach do robô
robo.teach(qf0[1])  # Passa os ângulos predefinidos como argumento
