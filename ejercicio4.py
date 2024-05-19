from matricesRalas import *
import numpy as np
import math

D = MatrizRala(629814,629814)
W = MatrizRala(629814,629814)

archivo_citas = open('citas.csv', encoding='utf8')
for fila in archivo_citas:
    fila = fila.split(',')
    if fila[0] != 'from':

        W[int(fila[1]),int(fila[0])] = 1

        if D[int(fila[0]),int(fila[0])]:
            D[int(fila[0]),int(fila[0])] += 1
        else:
            D[int(fila[0]),int(fila[0])] = 1

print("sali del primer ciclo")
archivo_citas.close()

for i in range(D.shape[0]):
    if D[i,i] != 0:
        D[i,i] = 1/D[i,i] 

print("sali del segundo ciclo")
vector_unos  =  MatrizRala(629814,1)
p_estrella_it = MatrizRala(629814,1)
for i in range(629814):
    vector_unos[i,0] = 1
    p_estrella_it[i,0] =  1/629814

print("sali del tercer ciclo")
d = 0.85
dif_abs = 1e16
dif_abs_prev = 0
epsilon = 1e-5

k = ((1-d)/629814)*vector_unos
print("hice k")
s= d*W@D
print("hice s")
i=0
while math.sqrt(dif_abs) > epsilon:
    p_estrella_prev = p_estrella_it
    p_estrella_it = k + s@p_estrella_it
    dif_abs=0
    for i in range(629814):
        temp = p_estrella_it[i,0] - p_estrella_prev[i,0]
        dif_abs+=temp**2
           
print(p_estrella_it[327827,0])
print(p_estrella_it[81323,0])  



    
print("sali del cuarto ciclo")
ranking_impacto = []

for i in range(10):
    mayor_imp = 0
    mayor_imp_pos = 0
   
    for j in range(629814):
        if (p_estrella_it[j,0] > mayor_imp) and (j not in ranking_impacto):
            mayor_imp = p_estrella_it[j,0]
            mayor_imp_pos = j
        
    ranking_impacto.append(mayor_imp_pos)
print("sali del quinto ciclo")
citas=W*vector_unos
ranking_citas =[]  
for i in range(10):
    mayor_cit =0
    mayor_cit_pos =0
    for j in range(629814):
        if(citas[j,0]>mayor_cit) and (j not in ranking_citas):
            mayor_cit=citas[j,0]
            mayor_cit_pos=j
    ranking_citas.append(mayor_cit_pos)

print("Top 10 papers con mayor impacto")
for i in ranking_impacto:
    print(f"ID:{ranking_impacto[i]} Impacto:{p_estrella_it[ranking_impacto[i],0]}")
print("Top 10 papers con mayor cantidad de citas")

for i in ranking_citas:
    print(f"ID:{ranking_citas[i]} Citas:{citas[ranking_citas[i],0]} Impacto{p_estrella_it[ranking_citas[i],0]}")   