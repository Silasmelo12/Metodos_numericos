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

y = np.arange(0, l_y + delta_y, delta_y)
x = np.arange(0, l_x + delta_x, delta_x)

quantidade_de_iteracao = 1000
quantidade_de_pontos_y = len(y)
quantidade_de_pontos_x = len(x)

u_old = np.zeros((quantidade_de_pontos_y, quantidade_de_pontos_x))
u_new = np.zeros((quantidade_de_pontos_y, quantidade_de_pontos_x))
u_new_corrigido = np.zeros((quantidade_de_pontos_y, quantidade_de_pontos_x))

# chute inicial que é a média
u_old[:, :] = np.mean(np.sin(x * np.pi))

# condições de contorno
constante = 0
u_old[0, :] = constante
u_old[:, 0] = 0
u_old[:, -1] = 0
u_old[-1, :] = np.sin(x * np.pi)

# Recebe iteração dos valores k+1. é -2 porque os contornos se repetem.
u_new[:, :] = u_old[:, :]
u_new_corrigido[:, :] = u_old[:, :]

beta = delta_x / delta_y

# sigma
omega = 1

# PLACA.round(2)
fig = plt.figure(figsize=(11, 7), dpi=100)
for n in range(0, quantidade_de_iteracao):
    for i in range(1, quantidade_de_pontos_y - 1):
        for j in range(1, quantidade_de_pontos_x - 1):
            u_new[i, j] = (u_old[i + 1, j] + u_new[i - 1, j] + beta ** 2 * (u_old[i, j + 1] + u_new[i, j - 1])) / (
                        2 * (1 + beta ** 2))
            u_new_corrigido = u_new_corrigido + 1.99 * (u_new - u_new_corrigido)
            u_old = u_new_corrigido

    cs = plt.contourf(x,y,u_new_corrigido)
    cs.cmap.set_over('red')
    cs.cmap.set_under('blue')
    plt.pause(0.1)
plt.colorbar()

plt.show()
