# IMPORTANTE: Para importar estas clases en otro archivo (que se encuentre en la misma carpeta), escribir:
# from matricesRalas import MatrizRala, GaussJordan 

class ListaEnlazada:
    def __init__( self ):
        self.raiz = None
        self.longitud = 0
        
        self.current = self.Nodo(None, self.raiz)

    def insertarFrente( self, valor ):
        # Inserta un elemento al inicio de la lista
        if len(self) == 0:
            return self.push(valor)    
    
        nuevoNodo = self.Nodo( valor, self.raiz )
        self.raiz = nuevoNodo
        self.longitud += 1

        return self

    def insertarDespuesDeNodo( self, valor, nodoAnterior ):
        # Inserta un elemento tras el nodo "nodoAnterior"
        nuevoNodo = self.Nodo( valor, nodoAnterior.siguiente)
        nodoAnterior.siguiente = nuevoNodo

        self.longitud += 1
        return self

    def push( self, valor ):
        # Inserta un elemento al final de la lista
        if self.longitud == 0:
            self.raiz = self.Nodo( valor, None )
        else:      
            nuevoNodo = self.Nodo( valor, None )
            ultimoNodo = self.nodoPorCondicion( lambda n: n.siguiente is None )
            ultimoNodo.siguiente = nuevoNodo

        self.longitud += 1
        return self
    
    def pop( self ):
        # Elimina el ultimo elemento de la lista
        if len(self) == 0:
            raise ValueError("La lista esta vacia")
        elif len(self) == 1:
            self.raiz = None
        else:
            anteUltimoNodo = self.nodoPorCondicion( lambda n: n.siguiente.siguiente is None )
            anteUltimoNodo.siguiente = None
        
        self.longitud -= 1

        return self

    def nodoPorCondicion( self, funcionCondicion ):
        # Devuelve el primer nodo que satisface la funcion "funcionCondicion"
        if self.longitud == 0:
            raise IndexError('No hay nodos en la lista')
        
        nodoActual = self.raiz
        while not funcionCondicion( nodoActual ):
            nodoActual = nodoActual.siguiente
            if nodoActual is None:
                raise ValueError('Ningun nodo en la lista satisface la condicion')
            
        return nodoActual
        
    def __len__( self ):
        return self.longitud

    def __iter__( self ):
        self.current = self.Nodo( None, self.raiz )
        return self

    def __next__( self ):
        if self.current.siguiente is None:
            raise StopIteration
        else:
            self.current = self.current.siguiente
            return self.current.valor
    
    def __repr__( self ):
        res = 'ListaEnlazada([ '

        for valor in self:
            res += str(valor) + ' '

        res += '])'

        return res

    class Nodo:
        def __init__( self, valor, siguiente ):
            self.valor = valor # valor {(columna, num)}
            self.siguiente = siguiente


class MatrizRala:
    def __init__( self, M, N ):
        self.filas = {} # Dict de key [fila] = valor {(columna, 1 o 0)}
        self.shape = (M, N)

    def __getitem__( self, Idx ):
        if Idx[0] in self.filas:
            try:
                self.filas[Idx[0]].nodoPorCondicion(lambda y: y.valor[0] == Idx[1])
                current = self.filas[Idx[0]].raiz
                while current is not None:
                    if current.valor[0] == Idx[1]:
                        return (current.valor[1])
                    current = current.siguiente
            except (ValueError, IndexError): # no existe el nodo
                return 0        
        else:
            return 0
    
    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        if Idx[0] in self.filas:
            try:
                self.filas[Idx[0]].nodoPorCondicion(lambda y: y.valor[0] == Idx[1]) # existe el nodo n en la fila m
                nodo = self.filas[Idx[0]].nodoPorCondicion( lambda y: y.valor[0] == Idx[1])
                nodo.valor=(Idx[1], v)    
            except ValueError or IndexError: # no existe el nodo
                actual = self.filas[Idx[0]].raiz
                if actual.valor[0]> Idx[1]:
                    self.filas[Idx[0]].insertarFrente((Idx[1], v)) 
               
                else:
                    while actual.siguiente is not None:
                        actual = actual.siguiente
                    if actual.valor[0] < Idx[1]:
                        self.filas[Idx[0]].insertarDespuesDeNodo((Idx[1], v), actual)

                    else:
                        prev = self.filas[Idx[0]].raiz
                        actual = self.filas[Idx[0]].raiz
                        while actual is not None:
                            if actual.valor[0] > Idx[1]:
                                self.filas[Idx[0]].insertarDespuesDeNodo((Idx[1], v), prev)
                                break
                            prev = actual
                            actual = actual.siguiente
        else: # no existe la fila m
            self.filas[Idx[0]] = ListaEnlazada()
            self.filas[Idx[0]].insertarFrente((Idx[1], v)) 
               
        
       

    def __mul__( self, k ):
        # Esta funcion implementa el producto matriz-escalar -> A * k
        matMul = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                matMul[i,j] = self[i,j]*k
        return matMul   
    
                    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape != other.shape:
            raise Exception('Las matrices deben tener las mismas dimensiones')
      
        matAdd = MatrizRala(self.shape[0], self.shape[1])
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                matAdd[i,j] = self[i,j] + other[i,j]
        return matAdd
    
    def __sub__( self, other ):
        # Esta funcion implementa la resta de matrices (pueden usar suma y producto) -> A - B
        if self.shape != other.shape:
            raise Exception('Las matrices deben tener las mismas dimensiones')
        
        matSub = MatrizRala(self.shape[0], self.shape[1])
        for i in range (self.shape[0]):
            for j in range (self.shape[1]):
                matSub[i,j] = self[i,j] - other[i,j]
        return matSub
        
    def __matmul__( self, other ):
        # Esta funcion implementa el producto matricial (notado en Python con el operador "@" ) -> A @ B
        if self.shape[1] != other.shape[0]:
            raise Exception('Las dimensiones de las matrices no son compatibles para el producto matricial')
        matMul = MatrizRala(self.shape[0], other.shape[1])
        for i in range(self.shape[0]): # filas de A
            for j in range(other.shape[1]): # columnas de B
                for k in range(self.shape[1]): # columnas de A
                    matMul[i,j] += self[i,k] * other[k,j]
        return matMul
        
    def __repr__( self ):
        res = 'MatrizRala([ \n'
        for i in range( self.shape[0] ):
            res += '    [ '
            for j in range( self.shape[1] ):
                res += str(self[i,j]) + ' '
            res += ']\n'
        res += '])'

        return res

def GaussJordan( A, b ):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado

    if A.shape[0] != b.shape[0]:
        raise Exception('A y b deben tener la misma cantidad de filas')

    C=MatrizRala(A.shape[0], A.shape[1]+1)
    
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i,j]=A[i,j]
    for i in range(A.shape[0]):
        C[i, C.shape[1]-1] = b[i,0]
      
    
    for i in range(C.shape[0]):
        
        # buscas pivote
     
        if C[i,i] !=0:
            pivote = C[i,i]
            
        else:
            # Swapear filas
            for fila in range(i+1, C.shape[0]):
                if C[fila,i]!=0:
                   lista1= C.filas[fila]
                   indice_fila=fila
                   break
            lista2= C.filas[i] 
            C.filas[i]=lista1
            C.filas[indice_fila]=lista2
            pivote = C[i,i]
        # dividis por pivote    
        
        for k in range(C.shape[1]) :
            C[i,k]= C[i,k]*(1/pivote)
        
        # ceros
        for j in range(i+1, C.shape[0]):
            escalar = C[j,i]
            for k in range(C.shape[1]):
                C[j,k]= C[j,k] - (escalar*C[i,k])      
    print(C)
    for i in range(C.shape[0],0,-1):
        pivote = C[i,i]
        print(f"pivote {pivote}")
        for j in range(C.shape[0]-i,0,-1):
            escalar = C[j,i]
            print(f"j={j}escalar {escalar}")
            for k in range(C.shape[1]):
                C[j,k]= C[j,k] - (escalar*pivote)        
    print(C)
    zeros = False
    absurd = False
    for i in range(A.shape[0]):
        current = A.filas[i].raiz
        t = 0
        while current is not None and (current.valor[1] == 0): 
            t+=1
        if t == A.shape[1]-1:
            absurd = True
        elif t == A.shape[1]:
            zeros = True

    if absurd:
        raise Exception('No tiene solucion')
    elif zeros:
        raise Exception('Infinitas soluciones')
    else:
        x = MatrizRala(A.shape[1],b.shape[0])
        for i in range(C.shape[0]):
            x[i,0]= C[i, C.shape[1]-1]
        return x

'''
def GaussJordan( A, b ):
    # Hallar solucion x para el sistema Ax = b
    # Devolver error si el sistema no tiene solucion o tiene infinitas soluciones, con el mensaje apropiado

    if A.shape[0] != b.shape[0]:
        raise Exception('A y b deben tener la misma cantidad de filas')

    C=MatrizRala(A.shape[0], A.shape[1]+1)
    for i in range(A.shape[0]):
        for j in range(A.shape[1]):
            C[i,j]=A[i,j]
    for i in range(A.shape[0]):
        C[i, C.shape[1]-1] = b[i,0]

    for i in range(C.shape[0]):
        # buscas pivote
        pivote=1
        for k in range(i, C.shape[1]-1):
            if C[i,k] !=0:
                pivote = C[i,k]
                columna_pivote=k
                break
        # dividis por pivote    
        for j in range(C.shape[1]) :
            C[i,j]= C[i,j]*(1/pivote)
        
        # ceros
        for j in range(i+1,C.shape[0]):
            escalar = C[j,columna_pivote]
            for k in range(C.shape[1]):
                C[j,k]= C[j,k] - (escalar*C[i,k])      
        print(C)
    for i in range(C.shape[0]):
        non_zero_count = sum([1 for j in range(C.shape[1]-1) if C[i,j] != 0])
        if non_zero_count == 0 and C[i, C.shape[1]-1] != 0:
            raise Exception('No tiene solucion')
        elif non_zero_count == 0 and C[i, C.shape[1]-1] == 0:
            raise Exception('Infinitas soluciones')

    x = MatrizRala(A.shape[1],b.shape[0])
    for i in range(C.shape[0]):
        x[i,0]= C[i, C.shape[1]-1]
    return x                   

'''