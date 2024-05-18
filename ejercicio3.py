import matplotlib.pyplot as plt
from matricesRalas import *

W =  MatrizRala(11,11)
# W[i,j] =  1 si p_j cita a p_i
# 0 = A 1 = B 2 = C 3 = D 4 = E 5 = F 6 = G 7 = H 8 = I 9 = J 10 = K

W[1,0] = 1      # A -> B
W[5,0] = 1      # A -> F
W[6,0] = 1      # A -> G
W[0,2] =  1     # C -> A
W[0,3] = 1      # D -> A
W[0,4] = 1      # E -> A
W[8,5] = 1      # F -> I
W[5,6] = 1      # G -> F
W[6,7] = 1      # H -> G
W[6,8] = 1      # I -> G
W[7,8] = 1      # I -> H
W[9,8] = 1      # I -> J
W[4,10] = 1     # K -> E

D  =  MatrizRala(11,11)
D[0,0] = 1/3
D[2,2] = 1
D[3,3] = 1
D[4,4] = 1
D[5,5] = 1
D[6,6] = 1
D[7,7] = 1
D[8,8] = 1/3
D[10,10] = 1

I  =  MatrizRala(11,11) # identidad_11
vector_unos  =  MatrizRala(11,1) # vector de 1s
p_estrella_it  =  MatrizRala(11,1)
for i in range(11):
    I[i, i] = 1
    vector_unos[i,0] = 1
    p_estrella_it[i,0] = 1/11

d = 0.85
A = I + (-1)*(d*W@D)
b = ((1-d)/11)*vector_unos
p_estrella = GaussJordan(A,b) # p_estrella = x / Ax=b:
diferencias_abs = []
t = 100
for i in range(t):
    p_estrella_it  =  ((1-d)/11)*vector_unos + d*W@D@p_estrella_it
    delta = 0
    for j in range(p_estrella.shape[0]):
        delta += abs(p_estrella_it[j,0] - p_estrella[j,0])   
    diferencias_abs.append(delta)

plt.plot(range(t), diferencias_abs)
plt.xlabel('Iteración')
plt.ylabel('Diferencia absoluta')
plt.title('Convergencia en PageRank')
# plt.show()
filename = 'plots/PageRank_convergencia_t' + str(t) + '.png'
plt.savefig(filename)