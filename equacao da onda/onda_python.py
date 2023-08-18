import numpy as np
import matplotlib.pyplot as plt

L    = 1.0    # tamanho do intervalo
C    = 0.75   # constante da equacao da onda
TFIM = 0.2    # tempo de simulacao
NX   = 51     # Número de pontos em X
NT   = 50    # 

DX = L/(NX-1) # tamanho do passo no espaço
DT = TFIM/NT  # tamanho do passo no tempo

NI = C*DT/DX  # numero de Courant

U_NUM = np.zeros((NT,NX))

# Condicoes Iniciais.
X = np.linspace(0,L,NX)
U_NUM[0,]  = np.sin(6*np.pi*X)
U_NUM[0,0] = U_NUM[0,NX-1]

# Solucao numerica
for i in range(NT-1):
    U_NUM[i+1,1:] = (1-NI)*U_NUM[i,1:]+NI*U_NUM[i,0:len(U_NUM)]
    U_NUM[i+1,0] = U_NUM[i+1,NX-1]

#plotar o grafico
plt.plot(X,U_NUM[0,])
