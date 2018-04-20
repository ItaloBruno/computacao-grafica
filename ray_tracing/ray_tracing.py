import numpy
from PIL import Image as PilImage

def Norma_Vetor(vetor):
    norma = 0
    for indice in range(len(vetor)):
        norma = norma + vetor[indice] ** 2
    return norma ** (1/2)

def Calculo_Vetor_Unitario(vetor):
    vetor_unitario = vetor[:]
    norma_vetor = Norma_Vetor(vetor)
    for indice in range(len(vetor)):
        vetor_unitario[indice] = vetor[indice] / norma_vetor
    return vetor_unitario
    
def Calculo_Vetor_W(vet_a):
    vet_w = Calculo_Vetor_Unitario(vet_a)
    return vet_w

def Calculo_Vetor_T(vet_w):
    vet_t = vet_w[:]
    indice_menor_valor = 0
    for indice, valor in enumerate(vet_w):
        if(0 > abs(valor)):
            indice_menor_valor = indice
    vet_t[indice_menor_valor] = 0
    return vet_t

def Calculo_Vetor_U(vet_t, vet_w):
    vet_u = numpy.cross(vet_t, vet_w)
    # print(vet_u)
    vet_u = Calculo_Vetor_Unitario(vet_u)
    return vet_u

def Calculo_Vetor_V(vet_w, vet_u):
    vet_v = numpy.cross(vet_w, vet_u)
    return vet_v

def Criar_Matriz(colunas, linhas, valor):
    matriz = [] 
    for x in range(colunas):
        linha = []
        for y in range(linhas):
	        linha.append(valor)
        matriz.append(linha)
    return matriz

def Calculo_Valore_U_V(matriz, colunas, linhas, l, r, b, t):
    for i in range(colunas):
        for j in range(linhas):
            u = (l + (r - l) * (i + 0.5))/ linhas
            v = (b + (t - b) * (j + 0.5))/ colunas
            matriz[i][j] = (u, v)
    
def Caso_Ortografico(matriz_valores_uv, colunas, linhas, vet_a, vet_w, vet_u, vet_v):
    matriz_result = matriz_valores_uv[:]
    direcao_raio  = numpy.dot(vet_w, -1)
    for x in range(colunas):
        for y in range(linhas):
            comp_u = numpy.dot(vet_u, matriz_valores_uv[x][y][0])
            comp_v = numpy.dot(vet_v, matriz_valores_uv[x][y][1])
            origem_raio = vet_a + comp_u + comp_v
            # print(direcao_raio)
            # print(origem_raio)
            matriz_result[x][y] = (direcao_raio, origem_raio)
            print(matriz_result[x][y])
    return matriz_result

def Caso_Obliquo(matriz_valores_uv, colunas, linhas, vet_a, vet_w, vet_u, vet_v, dist):
    matriz_result = matriz_valores_uv[:]
    origem_raio   = vet_a[:]
    for x in range(colunas):
        for y in range(linhas):
            aux    = numpy.dot(vet_w, -dist)
            comp_u = numpy.dot(vet_u, matriz_valores_uv[x][y][0])
            comp_v = numpy.dot(vet_v, matriz_valores_uv[x][y][1])
            direcao_raio =  aux + comp_u + comp_v
            matriz_result[x][y] = (direcao_raio, origem_raio)
            # print(matriz_result[x][y])
    return matriz_result


def Calculo_Delta(matriz_caso, colunas, linhas, centro, raio):
    matriz_result = matriz_caso[:]
    for x in range(colunas):
        for y in range(linhas):
            direcao = matriz_caso[x][y][0]
            origem  = matriz_caso[x][y][1]
            a = numpy.dot(direcao, direcao)
            

            if(delta >= 0):
                matriz_result[x][y] = (100, 150, 100)
            else:
                matriz_result[x][y] = (0, 0, 0)
    return matriz_result


def Cria_Imagem(matriz_img, colunas, linhas):
        img = PilImage.new('RGB', (colunas, linhas))
        imagem = img.load()
        for x in range(colunas):
            for y in range(linhas):
                imagem[x, y] = (matriz_img[x][y][0], 
                matriz_img[x][y][1],
                matriz_img[x][y][2])
        img.show()
        img.save("resultado.jpg")

# Valores dos lados do plano da imagem
left      = -13
right     =  13
top       =  10
bottom    = -10
distancia =  4

# Declaração de vetores que serão usados
vetor_a = [10, 10, 10]
vetor_w = [0, 0, 0]
vetor_t = [0, 0, 0]
vetor_v = [0, 0, 0]
vetor_u = [0, 0, 0]
num_colunas = 640
num_linhas  = 480
centro_esfera = [0, 0, 0]
raio_esfera   = 1
cor_esfera    = (100, 150, 100)

vetor_w  = Calculo_Vetor_W(vetor_a)
# print(vetor_w)
# print(vetor_a)
vetor_t  = Calculo_Vetor_T(vetor_w)
# print(vetor_t) 
vetor_u  = Calculo_Vetor_U(vetor_t, vetor_w)
# print(vetor_u)
vetor_v  = Calculo_Vetor_V(vetor_w, vetor_u)
# print(vetor_v)

matriz_uv = Criar_Matriz(num_colunas, num_linhas, 0)

# print(matriz_uv)
Calculo_Valore_U_V(matriz_uv, num_colunas, num_linhas, left, right, bottom, top)
# print(matriz_uv)
# print(matriz_uv[639][477])
# print(matriz_uv[639][478])
# print(matriz_uv[639][479])

# matriz_imagem = Caso_Ortografico(matriz_uv, num_colunas, num_linhas, vetor_a, vetor_w, vetor_u, vetor_v)
# print(matriz_imagem)
matriz_caso_obliquo = Caso_Obliquo(matriz_uv, num_colunas, num_linhas, vetor_a, vetor_w, vetor_u, vetor_v, distancia)

matriz_imagem = Calculo_Delta(matriz_caso_obliquo, num_colunas, num_linhas, centro_esfera, raio_esfera)

# print(matriz_imagem)
Cria_Imagem(matriz_imagem, num_colunas, num_linhas)



