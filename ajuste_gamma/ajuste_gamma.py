from PIL import Image

# Abre a imagem escolhida para ter o seu gamma alterado
imagem_original = Image.open("camel.jpg")
imagem_modificada = Image.open("camel.jpg")
imagem = imagem_modificada.load()

# Mostra a imagem original, sem o gamma alterado
imagem_modificada.show()

# Recolhendo as dimensões da imagem
tam_eixo_x = imagem_original.size[0]
tam_eixo_y = imagem_original.size[1]

# Gamma usado para aplicar na imagem original
gamma = 2

# Aplicação da fórmula de ajuste de gamma
for x in range (tam_eixo_x):
    for y in range (tam_eixo_y):
        novo_vermelho = (imagem[x, y][0]/255) ** (1/gamma)
        novo_vermelho = int(novo_vermelho * 255)

        novo_verde = (imagem[x, y][1]/255) ** (1/gamma)
        novo_verde = int(novo_verde * 255)

        novo_azul = (imagem[x, y][2]/255) ** (1/gamma)
        novo_azul = int(novo_azul * 255)

        imagem[x, y] = (novo_vermelho, novo_verde, novo_azul)

# Mostra a imagem com o seu gamma alterado
imagem_modificada.show()