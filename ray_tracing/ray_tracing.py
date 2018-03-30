import numpy
from math import pow, sqrt
#import copy

# Parâmetros disponibilizados
left   = -10
right  =  10
top    =  5
bottom = -5

# Declaração de vetores que serão usados
vetorE = [2, -2, 3]

vetorW = [0, 0, 0]
vetorT = [0, 0, 0]
vetorV = [0, 0, 0]
vetorU = [0, 0, 0]

# Dimensões da imagem
numColunas = 640
numlinhas  = 480

# ================================ Funções ================================
def criaMatriz(numlinhas, numColunas, valor):
    matriz = [] 
    for x in range(numColunas):
        linha = []
        for y in range(numlinhas):
	        linha += [valor]
        matriz += [linha]
    return matriz

def normaVetor(vetor):
    norma = pow(vetor[0], 2) + pow(vetor[1], 2) + pow(vetor[2], 2)
    norma = sqrt(norma)
    return norma

def vetorUnitario(vetor, norma):
    vetorAux = vetor[:]
    for i in range (len(vetorAux)):
        vetorAux[i] = vetorAux[i]/norma
    return vetorAux

def calculoVetorT(vetor):
    vetorAux  = vetor[:]
    indiceMin = 0
    for indice, valor in enumerate(vetor):
        if(0 > abs(valor)):
            indiceMin = indice
    vetorAux[indiceMin] = 1
    return vetorAux

def produtoEscalar(vetor, escalar):
    vetorAux = vetor[:]
    for i in range(len(vetorAux)):
        vetorAux[i] = vetorAux[i] * escalar
    return vetorAux

def calculaValoresUV(matrizImagem, numColunas, numlinhas, left, right, top, bottom):
    for i in range(numColunas):
        for j in range(numlinhas):
            u = float((left + (right -left) * (i + 0.5))) / numColunas
            v = float((bottom + (top - bottom) * (j + 0.5))) / numlinhas
            matrizImagem[i, j] = (u, v)

def casoOrtografico(vetorE, vetorU, vetorV, vetorW):
    u = -1
    v = -1
    direcao  = produtoEscalar(vetorW, -1)
    escalar1 = produtoEscalar(vetorU, u)
    escalar2 = produtoEscalar(vetorV, v)
    origem   = vetorE + escalar1 + escalar2

#===========================================================================

# # Inicia todos os elementos da matriz imagem com valor 0
# matrizImagem = criaMatriz(numlinhas, numColunas, 0)

# Calculo do vetor W, que será o vetor unitário do vetor E
normaVetorE = normaVetor(vetorE)
vetorW = vetorUnitario(vetorE, normaVetorE)

# O vetor T terá os mesmos valores do vetor W, 
# com a diferença que o menor elemento (valor absoluto) de T será setado para 1
vetorT = calculoVetorT(vetorW)

# Vetor U será o vetor unitário do produto vetorial entre os vetores T e W
vetorialTxW = numpy.cross(vetorT, vetorW)
normaTxW    = normaVetor(vetorialTxW)
vetorU      = vetorUnitario(vetorialTxW, normaTxW)

# Vetor V será o resultado do produto vetorial entre os vetores W e U
vetorV = numpy.cross(vetorW, vetorU)

print(vetorU)
print(vetorV)
print(vetorW)

