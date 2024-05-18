from matricesRalas import *
import numpy as np

D = MatrizRala(50,50)
W = MatrizRala(50,50)

archivo_citas = open('citas.csv', encoding='utf8')
for fila in archivo_citas:
    fila = fila.split(',')
    i = 0
    while i<50:
        if fila[0] != 'from':

            W[int(fila[1])-1,int(fila[0])-1] = 1

            if D[int(fila[0])-1,int(fila[0])-1]:
                D[int(fila[0])-1,int(fila[0])-1] += 1
            else:
                D[int(fila[0])-1,int(fila[0])-1] = 1
        i+=1
    break

for i in range(D.shape[0]):
    if D[i,i] != 0:
        D[i,i] = 1/D[i,i]

vector_unos  =  MatrizRala(50,1)
p_estrella_it = MatrizRala(50,1)
for i in range(50):
    vector_unos[i,0] = 1
    p_estrella_it[i,0] =  1/50

d = 0.85
dif_abs = 1e16
dif_abs_prev = 0
epsilon = 0.00001
k = ((1-d)/50)*vector_unos
M = d*W@D

while abs(dif_abs - dif_abs_prev) > epsilon:
    dif_abs_prev = dif_abs
    p_estrella_prev = p_estrella_it
    p_estrella_it = k + M @ p_estrella_it
    dif_abs = 0
    for j in range(p_estrella_it.shape[0]):
        dif_abs += abs(p_estrella_it[j,0] - p_estrella_prev[j,0])   
    
ranking = []
for i in range(10):
    mayor = 0
    mayor_pos = 0
    for j in range(10):
        if (p_estrella_it[j,0] > mayor) and ((j+1) not in ranking):
            mayor = p_estrella_it[j,0]
            mayor_pos = j+1
    ranking.append(mayor_pos)

print(ranking)