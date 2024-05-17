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
D[0,0] =  1/3
D[2,2] = 1
D[3,3] = 1
D[4,4] = 1
D[5,5] = 1
D[6,6] = 1
D[7,7] = 1
D[8,8] = 1/3
D[10,10] = 1

I  =  MatrizRala(11,11) # identidad_11
I[0,0] =  1
I[1,1] = 1
I[2,2] = 1
I[3,3] = 1
I[4,4] = 1
I[5,5] = 1
I[6,6] = 1
I[7,7] = 1
I[8,8] = 1
I[9,9] = 1
I[10,10] = 1
vector_unos  =  MatrizRala(11,1) # vector de 1s
vector_unos[0,0] =  1
vector_unos[1,0] = 1
vector_unos[2,0] = 1
vector_unos[3,0] = 1
vector_unos[4,0] = 1
vector_unos[5,0] = 1
vector_unos[6,0] = 1
vector_unos[7,0] = 1
vector_unos[8,0] = 1
vector_unos[9,0] = 1
vector_unos[10,0] = 1

p_estrella_it  =  MatrizRala(11,1)
p_estrella_it[0,0] =  1/11
p_estrella_it[1,0] = 1/11
p_estrella_it[2,0] = 1/11
p_estrella_it[3,0] = 1/11
p_estrella_it[4,0] = 1/11
p_estrella_it[5,0] = 1/11
p_estrella_it[6,0] = 1/11
p_estrella_it[7,0] = 1/11
p_estrella_it[8,0] = 1/11
p_estrella_it[9,0] = 1/11
p_estrella_it[10,0] = 1/11

d  =  0.85

A  =  I - d*W@D
b  =  ((1-d)/11)*vector_unos
p_estrella  =  GaussJordan(A,b)
print('p_estrella = x / Ax=b:', p_estrella.shape)
print(p_estrella)
print('\n')

t = 3
for i in range(t):
    p_estrella_it  =  ((1-d)/11)*vector_unos + d*W@D@p_estrella_it
print('p_estrella itertativo:')
print(p_estrella_it)




'''
import matplotlib.pyplot as plt

t = 30  # Increase the number of iterations for better visualization
for i in range(t):
    p_estrella_it  =  ((1-d)/11)*vector_unos + d*W@D@p_estrella_it
print('p_estrella itertativo:', p_estrella_it.shape)
print(p_estrella_it)

# Initialize a list to store the absolute differences
abs_diffs = []
# Calculate the absolute difference and add it to the list
for j in range(p_estrella.shape[0]):
    abs_diff = p_estrella_it[j][0] - p_estrella[j][0]
    abs_diffs.append(abs(abs_diff))

# Plot the absolute differences
plt.plot(range(t), abs_diffs)
plt.xlabel('Iteration')
plt.ylabel('Absolute Difference')
plt.title('Convergence of PageRank')
plt.show()

'''