import numpy
from math import pow, sqrt

# Valores dos lados do plano da imagem
left      = -10
right     =  10
top       =  5
bottom    = -5
distancia =  4

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
	        linha.append(valor)
        matriz.append(linha)
    return matriz

def calculaNormaVetor(vetor):
    norma = pow(vetor[0], 2) + pow(vetor[1], 2) + pow(vetor[2], 2)
    norma = sqrt(norma)
    return norma

def calculaVetorUnitario(vetor, norma):
    vetorAux = vetor[:]
    for i in range (len(vetorAux)):
        vetorAux[i] = vetorAux[i]/norma
    return vetorAux

# def produtoEscalar(vetor, escalar):
#     vetorAux = vetor[:]
#     for i in range(len(vetorAux)):
#         vetorAux[i] = vetorAux[i] * escalar
#     return vetorAux

def calculaVetorW(vetorE):
    normaVetorE = calculaNormaVetor(vetorE)
    vetor = calculaVetorUnitario(vetorE, normaVetorE)
    return vetor

def calculaVetorT(vetor):
    vetorAux  = vetor[:]
    indiceMin = 0
    for indice, valor in enumerate(vetor):
        if(0 > abs(valor)):
            indiceMin = indice
    vetorAux[indiceMin] = 1
    return vetorAux

def calculaVetorU(vetorT, vetorW):
    prodVetorial = numpy.cross(vetorT, vetorW)
    norma        = calculaNormaVetor(prodVetorial)
    vetorU       = prodVetorial / norma
    return vetorU

def calculaVetorV(vetorW, vetorU):
    vetorV = numpy.cross(vetorW, vetorU)
    return vetorV

def calculaValoresUV(matrizImagem, nX, nY, l, r, t, b):
    matrizAux = matrizImagem[:]
    for i in range(numColunas):
        for j in range(numlinhas):
            u = float(l + (r - l) * (i + 0.5)) / nX
            v = float(b + (t - b) * (j + 0.5)) / nY
            matrizAux[i][j] = (u, v)
    return matrizAux

def casoOrtografico(matrizImagem, nX, nY, vetE, vetU, vetV, vetW):
    direcaoRaio = numpy.dot(vetW, -1)
    origemRaio  = 0
    for i in range(nX):
        for j in range(nY):
            for k in range(0, 1):
                if(k%2 == 0):
                    escalar1    = vetU * matrizImagem[i][j][k]
                    escalar2    = vetV * matrizImagem[i][j][k+1]
                    origemRaio  = vetE + escalar1 + escalar2
                    matrizImagem[i][j] = (direcaoRaio, origemRaio)


def casoObliquo(matrizImagem, nX, nY, vetE, vetU, vetV, vetW, distancia):
    # origem do raio = vetor E
    origemRaio  = vetorE[:]
    direcaoRaio = 0
    for i in range(nX):
        for j in range(nY):
           for k in range(0,1):
                if(k%2 ==0):
                    # direção do raio = (-d * vetorW) + (coordenada U * vetor U) + (coordenada V * vetor V)
                    escalar1    = numpy.dot(vetW, -distancia)
                    escalar2    = vetU * matrizImagem[i][j][k]
                    escalar3    = vetV * matrizImagem[i][j][k+1]
                    direcaoRaio = escalar1 + escalar2 + escalar3
                    matrizImagem[i][j] = (direcaoRaio, origemRaio)

#===========================================================================
# Inicia todos os elementos da matriz imagem com valor 0
matrizImagem = criaMatriz(numlinhas, numColunas, 0)

# Calculo do vetor W, que será o vetor unitário do vetor E
vetorW = calculaVetorW(vetorE)

# O vetor T terá os mesmos valores do vetor W, 
# com a diferença que o menor elemento (valor absoluto) de T será setado para 1
vetorT = calculaVetorT(vetorW)

# Vetor U será o vetor unitário do produto vetorial entre os vetores T e W
vetorU = calculaVetorU(vetorT, vetorW)

# Vetor V será o resultado do produto vetorial entre os vetores W e U
vetorV = calculaVetorV(vetorW, vetorU)

# print(vetorU)
# print(vetorV)
# print(vetorW)

matrizImagem = calculaValoresUV(matrizImagem, numColunas, numlinhas, left, right, top, bottom)

casoOrtografico(matrizImagem, numColunas, numlinhas, vetorE, vetorU, vetorV, vetorW)

# casoObliquo(matrizImagem, numColunas, numlinhas, vetorE, vetorU, vetorV, vetorW, 4)
print(matrizImagem)