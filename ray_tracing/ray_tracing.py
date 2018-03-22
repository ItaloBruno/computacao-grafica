
import numpy as np
import copy

left = -10
right = 10
top = 5
bottom = -5

e =[2,-2,3]
w=[0,0,0]
u =[]
t=[0,0,0]
Matrix = []
Matrix2 = []

norma = ((2**2) + ((-2**2)*-1) + (3**2))**(1/2)

for i in range(0,len(e)):
    w[i] = e[i]/norma

t = w[:]

t[0] = 1

u2 = np.cross(t,w)

norma2 = ((u2[0]**2) + ((u2[1]**2)) + (u2[2]**2))**(1/2)

u = np.cross(t,w) /norma2

v = np.cross(u,w)




j = 0
for j in range(0,640,1):
    for i in range(0,480,1):
        Matrix.append(0);
    Matrix2.append(Matrix)
    Matrix = []

##while(j<480):
##    i=0
##    linha = []
##    while(i<640):
##        linha[i].append(0)
##        i+=1
##    Tamx.append(linha)
##    j+=

print(w)
print(t)
print(u)
print(v)
#print(Matrix2[0])
i = 0
j = 0
print(Matrix2[0][200])
for j in range(0,640,1):
    for i in range(0,480,1):
        #print(j,i)
        U = float(left +  (right - left) * (j + 0.5))
        V = float(bottom + (top - bottom) * ( i + 0.5))
        #print(U,V)
        Matrix2[j][i]=(U,V)

print(Matrix2)