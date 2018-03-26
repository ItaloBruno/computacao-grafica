import numpy
import copy
from math import pow, sqrt

# Parâmetros disponibilizados
left   = -10
right  = 10
top    = 5
bottom = -5

# Declaração de vetores que serão usados
vetor_e = [2, -2, 3]
vetor_w = [0, 0, 0]
vetor_t = [0, 0, 0]

vetor_v = [0, 0, 0]
vetor_u = [0, 0, 0]

matrix_1 = []
matrix_2 = []

# Calculo da norma/módulo do vetor_e
norma = (pow(vetor_e[0], 2) + pow(vetor_e[1], 2) + pow(vetor_e[2], 2))
norma = sqrt(norma)

# Calculando o vetor unitário do vetor_e e atribuindo o valor para cada elemento do vetor_w
for i in range(len(vetor_e)):
    vetor_w[i] = vetor_e[i]/norma

# O vetor_t terá os mesmos valores do vetor_w, com a diferença que o menor elemento (valor absoluto) de t será setado para 1
vetor_t = vetor_w[:]
indice_t = 0
t_minimo = 0

for indice, valor in enumerate(vetor_t):
    if (t_minimo > abs(valor)): 
        indice_t = indice
        
vetor_t[indice_t] = 1

#====================================================================================================================
# u2 = numpy.cross(vetor_t, vetor_w)

# norma2 = ((u2[0]**2) + ((u2[1]**2)) + (u2[2]**2))**(1/2)

# vetor_u = numpy.cross(vetor_t,vetor_w) /norma2

# v = numpy.cross(vetor_u,vetor_w)


# j = 0
# for j in range(0,640,1):
#     for i in range(0,480,1):
#         matrix_1.append(0)
#     matrix_2.append(matrix_1)
#     matrix_1 = []

# ##while(j<480):
# ##    i=0
# ##    linha = []
# ##    while(i<640):
# ##        linha[i].append(0)
# ##        i+=1
# ##    Tamx.append(linha)
# ##    j+=

# print(vetor_w)
# print(vetor_t)
# print(vetor_u)
# print(v)
# #print(Matrix2[0])
# i = 0
# j = 0
# print(matrix_2[0][200])
# for j in range(0,640,1):
#     for i in range(0,480,1):
#         #print(j,i)
#         U = float(left +  (right - left) * (j + 0.5))
#         V = float(bottom + (top - bottom) * ( i + 0.5))
#         #print(U,V)
#         matrix_2[j][i]=(U,V)

