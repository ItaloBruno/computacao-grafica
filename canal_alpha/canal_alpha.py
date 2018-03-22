from PIL import Image

# Abre as imagens de brackground, alpha_channel e foreground
imagem1 = Image.open("background.jpg")
imagem2 = Image.open("alpha_channel.png")
iamgem3 = Image.open("foreground.png")

# Carrega as imagens nas variáveis para fazer as manipulação necessárias
background = imagem1.load()
alpha_channel = imagem2.load()
foreground = iamgem3.load()

# Tamanho X e Y das imagens, para percorrer cada pixel
tamX = imagem1.size[0]
tamY = imagem1.size[1]

for i in range(0,tamX,1):
    for j in range(0,tamY,1):

        red = int(alpha_channel[i,j][0]/255) * foreground[i,j][0]
        green = int(alpha_channel[i,j][1]/255) * foreground[i,j][1]
        blue = int(alpha_channel[i,j][2]/255) * foreground[i,j][2]

        foreground[i,j] = (red,green,blue)

        alpha = 0.8

        red2 = int((alpha * foreground[i,j][0]) + ((1-alpha) * background[i,j][0]))
        green2 = int((alpha * foreground[i,j][1]) + ((1-alpha) * background[i,j][1]))
        blue2 = int((alpha * foreground[i,j][2]) + ((1-alpha) * background[i,j][2]))

        background[i,j] = (red2,green2,blue2)

#dart.show()
imagem1.show()
#imagem2.show()
#imagem1.show()