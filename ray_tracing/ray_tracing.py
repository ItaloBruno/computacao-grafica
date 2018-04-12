import numpy
from math import pow, sqrt
import PIL

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

# casoOrtografico(matrizImagem, numColunas, numlinhas, vetorE, vetorU, vetorV, vetorW)

casoObliquo(matrizImagem, numColunas, numlinhas, vetorE, vetorU, vetorV, vetorW, distancia)

# Caso Oblíquo e Ortogŕaficos concluídos

""" 
    Próximo passo é fazer o cálculo das funções implícitas
    Para isso, precisamos calcular a variável t na função e + td 
    onde e = origem, d = direção. 
    Nesse caso, vamos explorar a interseção entre raio X esfera
"""

# Vetor que indica a posição do centro da esfera e seu respectivo raio
centroEsfera = [0, 0, 0]
raioEsfera = 0

""" 
    Para obter o valor de t, primeiro precisamos saber se raio toca ou não a esfera.
    Primeiro calcula-se o delta, que é dado pela expressão abaixo:
    ∆ = (2d · (e − c))**2 − 4(d · d)((e − c) · (e − c) − r**2 )

    Se ∆ < 0, o raio não intercepta a esfera.
    Se ∆ = 0, o raio toca exatamente um ponto na casca da esfera
    Se ∆ > 0, existem duas soluções:
    O raio entra na esfera
    O raio sai da esfera
"""

def calculoDelta(matriz, nX, nY, centro, raio):
    matrixResultante = matriz[:]
    for i in range(nX):
        for j in range(nY):
            origem  = matrixResultante[i][j][0]
            direcao = matrixResultante[i][j][1]

            a = numpy.dot(direcao, direcao)

            b = 2 * numpy.dot(direcao,(origem - centro))

            c = numpy.dot((origem - centro), (origem - centro)) - raio**2
            
            # Cálculo Delta
            delta = b**2 - (4 * a *c)

            # Se o delta for maior que 0, o raio pode entrar ou sair da esfera
            if(delta >= 0):
                valorT1 = abs(- numpy.dot(direção, (origem - centro)) + sqrt(delta))
                valorT2 = abs(- numpy.dot(direção, (origem - centro)) - sqrt(delta))
                if (valorT1 >= valorT2)
                    matrixResultante[i][j] = valorT1
                else:
                    matrixResultante[i][j] = valorT2

    return matrixResultante

imagemEsfera = calculoDelta(matrizImagem, numColunas, numlinhas, centroEsfera, raioEsfera)

