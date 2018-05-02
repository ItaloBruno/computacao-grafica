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

def Calculo_Valore_U_V(matriz, colunas, linhas, l, r, b, t):
    matrizValores = matriz[:]
    for i in range(colunas):
        for j in range(linhas):
            u = (l + (r - l) * (i + 0.5))/colunas
            v = (b + (t - b) * (j + 0.5))/linhas
            matrizValores[i][j] = [u, v]
    return matrizValores

def Caso_Ortografico(matriz_valores_uv, colunas, linhas, vet_a, vet_w, vet_u, vet_v):
    matriz_result = matriz_valores_uv[:]
    direcao_raio = numpy.dot(vet_w, -1)
    for x in range(colunas):
        for y in range(linhas):
            comp_u = numpy.dot(vet_u, matriz_valores_uv[x][y][0])
            comp_v = numpy.dot(vet_v, matriz_valores_uv[x][y][1])
            # print(comp_u)
            # print(comp_v)
            origem_raio = vet_a + comp_u + comp_v
            # print(direcao_raio)
            # print(origem_raio,"\n")
            matriz_result[x][y] = [direcao_raio, origem_raio]
            # print(matriz_result[x][y]+"\n")
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
            # print(matriz_result[x][y])
    return matriz_result

def Calculo_Delta(matriz_caso, matriz_img, colunas, linhas, esferas, luz, intensidade):
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

                    ponto   = origem + (direcao * t)
                    vetor_l = (luz - ponto)
                    vetor_l = Calculo_Vetor_Unitario(vetor_l)
                    vetor_n = (ponto - centro)
                    vetor_n = Calculo_Vetor_Unitario(vetor_n)
                    aux     = numpy.dot(vetor_n, vetor_l)
                    
                    lambert  = [0, 0, 0]
                    lambert[0] = int(cor[0] * intensidade * max(0, aux))
                    lambert[1] = int(cor[1] * intensidade * max(0, aux))
                    lambert[2] = int(cor[2] * intensidade * max(0, aux))
                    # print("""Valores l, n, aux, max
                    # l = {}
                    # n = {}
                    # aux = {}
                    # max(0, aux) = {}
                    # lambert = {}

                    # """.format(vetor_l, vetor_n, aux, max(0,aux), lambert))
                    if t < matriz_t[x][y]:
                        matriz_t[x][y]   = t
                        matriz_cor[x][y] = lambert
    return matriz_cor

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
direcao_luz     = [-10, 20, 30]
intensidade_luz = 1

cor_ambiente = [255, 0, 255]
intensidade_ambiente = []
# Declaração de vetores que serão usados
vetor_a = [10, 10, 10]
vetor_w = [0, 0, 0]
vetor_t = [0, 0, 0]
vetor_v = [0, 0, 0]
vetor_u = [0, 0, 0]
num_colunas = 640
num_linhas  = 480
lista_esferas = [[[2, -15, 0], 2, [250, 250, 250]],
                 [[10, -15, 0], 2, [50, 250, 150]]]

# [4, -5, 0] [2, -5, 0] [2, -15, 0]

print("Calculando Vetores W, T, U e V...\n")
vetor_w = Calculo_Vetor_W(vetor_a)
vetor_t = Calculo_Vetor_T(vetor_w)
vetor_u = Calculo_Vetor_U(vetor_t, vetor_w)
vetor_v = Calculo_Vetor_V(vetor_w, vetor_u)
print("""Vetores A, W, T, U e V
A = {}
W = {}
T = {}
U = {} 
V = {}
""".format(vetor_a, vetor_w, vetor_t, vetor_u, vetor_v))

print("Calculando Valores u e v...")
matriz_uv = Criar_Matriz(num_colunas, num_linhas, 0)
matriz_uv = Calculo_Valore_U_V(matriz_uv, num_colunas, num_linhas, left, right, bottom, top)

print("Calculando origem e direção do caso ortográfico...")
matriz_caso_orto = Caso_Ortografico(matriz_uv, num_colunas, num_linhas, vetor_a, vetor_w, vetor_u, vetor_v)

print("Calculando o delta...")
matriz_imagem = Criar_Matriz(num_colunas, num_linhas, [0, 0, 0])
matriz_imagem = Calculo_Delta(matriz_caso_orto, matriz_imagem, num_colunas, num_linhas, lista_esferas, direcao_luz, intensidade_luz)

# print("Calculando origem e direção do caso oblíquo...")
# matriz_caso_obliquo = Caso_Obliquo(matriz_uv, num_colunas, num_linhas, vetor_a, vetor_w, vetor_u, vetor_v, distancia)

# print("Calculando o delta...")
# matriz_imagem = Criar_Matriz(num_colunas, num_linhas, [0, 0, 0])
# matriz_imagem = Calculo_Delta(matriz_caso_obliquo, num_colunas, num_linhas, centro_esfera, raio_esfera)

print("Criando a imagem...")
Cria_Imagem(matriz_imagem, num_colunas, num_linhas)
