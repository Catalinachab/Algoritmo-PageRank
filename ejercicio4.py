from matricesRalas import *

D = MatrizRala(79008,79008)
W = MatrizRala(79008,79008)

archivo_citas = open('citas.csv', encoding='utf8')
for fila in archivo_citas:
    fila = fila.split(',')
    if fila[0] != 'from':

        W[int(fila[1])-1,int(fila[0])-1] = 1

        if D[int(fila[0])-1,int(fila[0])-1]:
            D[int(fila[0])-1,int(fila[0])-1] += 1
        else:
            D[int(fila[0])-1,int(fila[0])-1] = 1

for i in range(D.shape[0]):
    if D[i,i] != 0:
        D[i,i] = 1/D[i,i]

vector_unos  =  MatrizRala(79008,1)
p_estrella_it = MatrizRala(79008,1)
for i in range(79008):
    vector_unos[i,0] = 1
    p_estrella_it[i,0] =  1/79008

d = 0.85
dif_abs = 1e16
dif_abs_prev = 0
epsilon = -1e-16

while abs(dif_abs - dif_abs_prev) > epsilon:
    dif_abs_prev = dif_abs
    p_estrella_prev = p_estrella_it
    p_estrella_it = ((1-d)/79008)*vector_unos + d*W@D@p_estrella_it
    dif_abs = 0
    for j in range(p_estrella.shape[0]):
        dif_abs += abs(p_estrella_it[j,0] - p_estrella_viejo[j,0])   
    
mayor = 0
mayor_pos = 0
ranking = []
for i in range(10):
    for j in range(79008):
        if (p_estrella_it[j,0] > mayor) and ((j+1)not in ranking):
            mayor = p_estrella_it
            mayor_pos = j+1
    ranking.append(mayor_pos)

print(ranking)