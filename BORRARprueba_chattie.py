import numpy as np
from scipy.sparse import lil_matrix

max_indice_nodo = 0

with open('citas.csv', encoding='utf8') as archivo_citas:
    for fila in archivo_citas:
        if not fila.startswith('from'):
            origen, destino = map(int, fila.strip().split(','))
            max_indice_nodo = max(max_indice_nodo, origen, destino)

num_nodos = max_indice_nodo
D = lil_matrix((num_nodos, num_nodos))
W = lil_matrix((num_nodos, num_nodos))

with open('citas.csv', encoding='utf8') as archivo_citas:
    for fila in archivo_citas:
        if not fila.startswith('from'):
            origen, destino = map(int, fila.strip().split(','))
            W[destino - 1, origen - 1] = 1
            D[origen - 1, origen - 1] += 1

D.setdiag(1 / D.diagonal())

vector_unos = np.ones((num_nodos, 1))
p_estrella_it = np.ones((num_nodos, 1)) / num_nodos

d = 0.85
epsilon = 1e-16
max_iteraciones = 100
iteracion = 0

while True:
    p_estrella_prev = p_estrella_it.copy()
    p_estrella_it = ((1 - d) / num_nodos) * vector_unos + d * W.dot(D.dot(p_estrella_it))
    dif_abs = np.sum(np.abs(p_estrella_it - p_estrella_prev))
    if dif_abs < epsilon or iteracion >= max_iteraciones:
        break
    iteracion += 1

ranking = np.argsort(p_estrella_it.flatten())[::-1][:10] + 1
print(ranking)