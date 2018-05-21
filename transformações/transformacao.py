import numpy
from PIL import Image as PilImage

def Norma_Vetor(vetor):
    norma = 0
    for indice in range(len(vetor)):
        norma = norma + vetor[indice] ** 2
    return norma ** (1 / 2)

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
        if (0 > abs(valor)):
            indice_menor_valor = indice
    vet_t[indice_menor_valor]  = 1
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
    coluna = []
    linha  = []
    for x in range(colunas):
        for y in range(linhas):
            linha.append(valor)
        coluna.append(linha)
        linha = []
    return coluna

def Calculo_Valore_U_V(matriz, colunas, linhas, l, r, b, t, val_u, val_v):
    matrizValores = matriz[:]
    for i in range(colunas):
        for j in range(linhas):
            u = ((l + (r - l) * (i + 0.5))/colunas) + val_u
            v = ((b + (t - b) * (j + 0.5))/linhas)  + val_v
            matrizValores[i][j] = [u, v]
    return matrizValores

def Caso_Ortografico(matriz_valores_uv, colunas, linhas, vet_a, vet_w, vet_u, vet_v):
    matriz_result = matriz_valores_uv[:]
    direcao_raio = numpy.dot(vet_w, -1)
    for x in range(colunas):
        for y in range(linhas):
            comp_u = numpy.dot(vet_u, matriz_valores_uv[x][y][0])
            comp_v = numpy.dot(vet_v, matriz_valores_uv[x][y][1])

            origem_raio = vet_a + comp_u + comp_v

            matriz_result[x][y] = [direcao_raio, origem_raio]

    return matriz_result

def Caso_Obliquo(matriz_valores_uv, colunas, linhas, vet_a, vet_w, vet_u, vet_v, dist):
    matriz_result = matriz_valores_uv[:]
    origem_raio = vet_a[:]
    for x in range(colunas):
        for y in range(linhas):
            aux = numpy.dot(vet_w, -dist)
            comp_u = numpy.dot(vet_u, matriz_valores_uv[x][y][0])
            comp_v = numpy.dot(vet_v, matriz_valores_uv[x][y][1])
            direcao_raio = aux + comp_u + comp_v
            matriz_result[x][y] = [origem_raio, direcao_raio]
    return matriz_result

def Calculo_Delta(matriz_caso, matriz_img, colunas, linhas, esferas):
    matriz_t    = Criar_Matriz(colunas, linhas, 999999999999999999)
    matriz_cor  = matriz_img[:]
    for x in range(colunas):
        for y in range(linhas):
            for esfera in esferas:
                direcao = matriz_caso[x][y][0]
                origem  = matriz_caso[x][y][1]
                centro  = esfera[0]
                raio    = esfera[1]
                cor     = esfera[2]

                a = numpy.dot(direcao, direcao)
                b = 2 * (numpy.dot(direcao, (origem - centro)))
                c = numpy.dot((origem - centro), (origem - centro)) - raio ** 2

                delta = (b ** 2) - 4 * a * c

                if delta >= 0:
                    t1 = ((-b) + (delta ** 1/2)) / (2 * a)
                    t2 = ((-b) - (delta ** 1/2)) / (2 * a)
                    t1 = abs(t1)
                    t2 = abs(t2)
                    t  = min(t1, t2)

                    if t < matriz_t[x][y]:
                        matriz_t[x][y] = t
                        matriz_cor[x][y] = esfera[2]
    return matriz_cor

def Transformacao_Matriz(matriz_u_v, matriz_transformacao, colunas, linhas, val_u, val_v):
    matriz_resultante = matriz_u_v[:]
    for x in range(colunas):
        for y in range(linhas):
            transfor = numpy.matmul(matriz_u_v[x][y], matriz_transformacao)
            matriz_resultante[x][y] = [transfor[0] - val_u, transfor[1] - val_v]
    return matriz_resultante

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
lista_esferas = [[[2, -15, 0], 2, [250, 50, 100]],
                 [[10, -15, 0], 2, [50, 250, 150]]]

# [4, -5, 0] [2, -5, 0] [2, -15, 0]

#Matrizes de transformação
valor_u = 0
valor_v = 0
transfor_escala = [[1.5, 0],[0, 1.5]]
transfor_cisa   = [[1, 0], [1, 1]]

print("Calculando vetores W, T, U e V...\n")
vetor_w = Calculo_Vetor_W(vetor_a)
vetor_t = Calculo_Vetor_T(vetor_w)
vetor_u = Calculo_Vetor_U(vetor_t, vetor_w)
vetor_v = Calculo_Vetor_V(vetor_w, vetor_u)
# print("""Vetores A, W, T, U e V
# A = {}
# W = {}
# T = {}
# U = {}
# V = {}
# """.format(vetor_a, vetor_w, vetor_t, vetor_u, vetor_v))

print("Calculando valores u e v...")
matriz_uv = Criar_Matriz(num_colunas, num_linhas, 0)
matriz_uv = Calculo_Valore_U_V(matriz_uv, num_colunas, num_linhas, left, right, bottom, top, valor_u, valor_v)

print("Calculando a transformação de escala...")
matriz_transformada = matriz_uv[:]
matriz_transformada = Transformacao_Matriz(matriz_uv, transfor_cisa, num_colunas, num_linhas, valor_u, valor_v)

print("Calculando origem e direção do caso ortográfico...")
matriz_caso_orto = Caso_Ortografico(matriz_transformada, num_colunas, num_linhas, vetor_a, vetor_w, vetor_u, vetor_v)

print("Calculando o delta...")
matriz_imagem = Criar_Matriz(num_colunas, num_linhas, [0, 0, 0])
matriz_imagem = Calculo_Delta(matriz_caso_orto, matriz_imagem, num_colunas, num_linhas, lista_esferas)

print("Criando a imagem...")
Cria_Imagem(matriz_imagem, num_colunas, num_linhas)
