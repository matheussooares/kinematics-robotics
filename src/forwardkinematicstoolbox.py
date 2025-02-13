import roboticstoolbox as rtb
import matplotlib.pyplot as plt
import numpy as np
from math import pi 

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

N = 100
T = 0.008

# ---------Pontos de juntas----------
angs = [[0, 0, 0, 0, 0],
        [pi/6, pi/2, pi/2, 0, pi/6],
        [0, 0, 0, 0, 0],
        [-pi/2, pi/6, 0, -pi/4, pi/6],
        [0, 0, 0, 0, 0],
        [pi/4, pi/6, -pi/4, pi/8, pi/6],
        [0, 0, 0, 0, 0],
        [pi/2, pi/6, -pi/3, pi/4, pi/6],
        [0, 0, 0, 0, 0]
]

trajetoria = []
for i in range(0,len(angs)-1):
    trajetoria.append(rtb.jtraj(angs[i], angs[i+1], N).q)

# # ---------Trajetórias----------
trajetoria_completa = np.vstack(trajetoria)


# ---------Visualização do robô----------
robo.plot(
    trajetoria_completa,
    backend='pyplot',
    dt=T, 
    limits=[-0.4, 0.6, -0.4, 0.6, 0, 0.6],
    shadow=True,     
    loop=True
)


