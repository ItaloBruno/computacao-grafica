from math import pow, sqrt

class Vetor:
    def __init__(self, vetor):
        self.vetor = vetor
    
    def normaVetor(self):
        self.norma = pow(self.vetor[0], 2) + 
                     pow(self.vetor[1], 2) + 
                     pow(self.vetor[2], 2)
        self.norma = sqrt(self.norma)


    
    def vetorUnitário(self):
        self.unitario = []
        for i in range(len(self.vetor)):
            self.unitario = self.vetor[i]/self.norma
        self.unitario



    