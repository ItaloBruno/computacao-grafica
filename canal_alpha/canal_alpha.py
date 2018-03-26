from PIL import Image

# Abre as imagens de brackground, alpha_channel e foreground
imagem_de_fundo = Image.open("background.jpg")
imagem_canal_alfa = Image.open("alpha_channel.png")
imagem_primeiro_plano = Image.open("foreground.png")

# Carrega as imagens nas variáveis para fazer as manipulação necessárias
fundo = imagem_de_fundo.load()
canal_alfa = imagem_canal_alfa.load()
primeiro_plano = imagem_primeiro_plano.load()

# Tamanho X e Y das imagens, para percorrer cada pixel
tam_eixo_x = imagem_de_fundo.size[0]
tam_eixo_y = imagem_de_fundo.size[1]

# Definindo o alfa que iremos usar
alfa = 0.5

# Percorrendo cada pixel e aplicando a fórmula
for x in range(tam_eixo_x):
    for y in range(tam_eixo_y):
        if(canal_alfa[x, y][0] == 255):
            vermelho = int(canal_alfa[x,y][0]/255) * primeiro_plano[x,y][0]
            verde = int(canal_alfa[x,y][1]/255) * primeiro_plano[x,y][1]
            azul = int(canal_alfa[x,y][2]/255) * primeiro_plano[x,y][2]

            primeiro_plano[x,y] = (vermelho,verde,azul)

            vermelho_2 = int((alfa * primeiro_plano[x,y][0]) + ((1-alfa) * fundo[x,y][0]))
            verde_2 = int((alfa * primeiro_plano[x,y][1]) + ((1-alfa) * fundo[x,y][1]))
            azul_2 = int((alfa * primeiro_plano[x,y][2]) + ((1-alfa) * fundo[x,y][2]))

            fundo[x,y] = (vermelho_2,verde_2,azul_2)

# Mostra a imagem resultante do algoritmo de aplicação do canal alfa
imagem_de_fundo.show()
