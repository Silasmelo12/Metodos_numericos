from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

l_y = 1
l_x = 1
delta_x = 0.1
delta_y = 0.1
quantidade_de_iteracao = 100

y = np.arange(0, l_y + delta_y, delta_y)
x = np.arange(0, l_x + delta_x, delta_x)

quantidade_de_pontos_y = len(y)
quantidade_de_pontos_x = len(x)

# Definindo a dimensão da matriz, -2 dois, porque leva em consideracação os pontos de contorno
# eles não são contados na matriz A, pois sao conhecidos.
quantidade_linhas_matriz_A = quantidade_de_pontos_x - 2
quantidade_colunas_matriz_A = quantidade_de_pontos_x - 2

# definindo os elementos do sistema Ax=C
beta  = delta_x / delta_y
#a     = 1 / (2 * (1 + beta ** 2))
#b     = (beta ** 2) / (2 * (1 + beta ** 2))
p = quantidade_de_pontos_x - 1
q = quantidade_de_pontos_y - 1

sigma_otimo = (1/(1+beta**2))*(np.cos(np.pi/p)+beta**2*np.cos(np.pi/q))
omega_otimo = 2/((1+(1-sigma_otimo**2))**(1/2))

omega = 1

d = omega/(2*(1+beta**2))
e = (omega*beta**2)/(2*(1+beta**2))

# Criação da matriz A
A = np.zeros((quantidade_linhas_matriz_A + 1, quantidade_colunas_matriz_A + 1))
C = np.zeros(quantidade_linhas_matriz_A)

# Construção da matriz A
for i in range(0, quantidade_linhas_matriz_A):
    A[i, i - 1] = -d
    A[i, i] = 1
    A[i, i + 1] = -d
A = np.delete(A, (-1), axis=0)
A = np.delete(A, (-1), axis=1)

u = np.zeros((quantidade_de_iteracao, quantidade_de_pontos_y, quantidade_de_pontos_y, quantidade_de_pontos_x))
u_old = np.zeros((quantidade_de_pontos_y, quantidade_de_pontos_x))
u_new = np.zeros((quantidade_de_pontos_y, quantidade_de_pontos_x))

# chute inicial que é a média
u_old[:, :] = np.mean(np.sin(x * np.pi))
u_new = u_old
u[0] = u_old

# Condições de contorno
u_old[0, :] = 0
u_old[:, 0] = 0
u_old[:, -1] = 0
u_old[-1, :] = np.sin(x * np.pi)

# Solução numérica
for n in range(0, quantidade_de_iteracao):
    for j in range(1, quantidade_de_pontos_y - 1):
        C[:]  = (1-omega) * u_old[j,1:-1] + e * (u_old[j+1,1:-1] + u_old[j-1,1:-1])
        C[0]  = C[0]  + d * (u_old[j, 0])
        C[-1] = C[-1] + d * (u_old[j,-1])

        u_new[j, 1:-1] = np.linalg.solve(A, C)
        u[n, j][:, :] = u_new
        u_old = u_new


for n in range(0, quantidade_de_iteracao):
    for j in range(1, quantidade_de_pontos_y - 1):
        cs = plt.contourf(x, y, u[n, j][:, :])

        cs.cmap.set_over('red')
        cs.cmap.set_under('blue')
        plt.pause(0.0000005)
        #plt.show()

plt.colorbar()
