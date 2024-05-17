from matricesRalas import *
D = MatrizRala(79008,79008)
W = MatrizRala(79008,79008)
archivo_citas= open('citas.csv', encoding='utf8')
for filas in archivo_citas:
    filas = filas.split(',')
    if filas[0]!='from':
        W[int(filas[1])-1,int(filas[0])-1]=1
        if D[int(filas[0])-1,int(filas[0])-1]:
            D[int(filas[0])-1,int(filas[0])-1]+=1
        else:
            D[int(filas[0])-1,int(filas[0])-1]=1    
for i in range(D.shape[0]):
    if D[i,i]!=0:
        D[i,i]= 1/D[i,i]

i=0
vector_unos  =  MatrizRala(79008,1) # vector de 1s
while i< 79008:
    vector_unos[i,0] = 1
    i+=1

p_estrella_it = MatrizRala(79008,1)
i=0
while i< 79008:
    p_estrella_it[i,0] =  1/79008
    i+=1



d=0.85
abs_diff = 1e16
abs_diff_prev=0
epsilon = 1**(-100) 

while abs(abs_diff - abs_diff_prev)>epsilon:
    abs_diff_prev = abs_diff
    p_estrella_prev=p_estrella_it
    p_estrella_it  =  ((1-d)/79008)*vector_unos + d*W@D@p_estrella_it
    abs_diff=0
    for j in range(p_estrella.shape[0]):
        abs_diff += abs(p_estrella_it[j,0] - p_estrella_viejo[j,0])   
    
mayor=0
mayor_pos=0
ranking =[]
for i in range(10):
    for j in range(79008):
        if p_estrella_it[j,0] >  mayor and ((j+1)not in ranking):
            mayor= p_estrella_it
            mayor_pos =j+1
    ranking.append(mayor_pos)


