from PIL import Image as PilImage

class Imagem:
    def __init__(self, num_colunas, num_linhas):
        self.num_colunas = num_colunas
        self.num_linhas  = num_linhas

    def Cria_Imagem(matriz_imagem):
        imagem = PilImage.new('RGB', (self.num_colunas, self.num_lihas))
        imagem = imagem.load()
        for x in range(self.num_colunas):
            for y in range(self.num_linhas):
                imagem[x, y] = (matriz_imagem[x][y][0],
                                matriz_imagem[x][y][1], 
                                matriz_imagem[x][y][2])
        imagem.show()
        imagem.save("resultado.jpg")

