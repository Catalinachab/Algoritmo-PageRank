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
            current = self.filas[Idx[0]].raiz
            while current is not None:
                if current.valor[0] == Idx[1]:
                    return (current.valor[1])
                current = current.siguiente
        else:
            return 0
    
    def __setitem__( self, Idx, v ):
        # Esta funcion implementa la asignacion durante indexacion ( Idx es una tupla (m,n) ) -> A[m,n] = v
        if Idx[0] in self.filas: # existe la fila m (el paper m fue referenciado por algun otro)
            if self.filas[Idx[0]].nodoPorCondicion(lambda y: y.valor[0] == Idx[1]) is not ValueError or IndexError:
                print('hola entre al if')
                self.filas[Idx[0]].nodoPorCondicion( lambda y: y.valor[0] == Idx[1] ).valor[1] = v
            else:
                prev = self.filas[Idx[0]].raiz
                actual = self.filas[Idx[0]].raiz
                while actual.siguiente is not None:
                    if actual.valor[0] > Idx[1]:
                        self.filas[Idx[0]].insertarDespuesDeNodo(v, prev)
                        break
                    prev = actual
                    actual = actual.siguiente
            '''
            try:
                self.filas[Idx[0]].nodoPorCondicion(lambda y: y.valor[0] == Idx[1]) # existe el nodo n en la fila m
                self.filas[Idx[0]].nodoPorCondicion( lambda y: y.valor[0] == Idx[1] ).valor[1] = v
                
            except ValueError or IndexError: # no existe el nodo

                prev = self.filas[Idx[0]].raiz
                actual = self.filas[Idx[0]].raiz
                while actual.siguiente is not None:
                    if actual.valor[0] > Idx[1]:
                        self.filas[Idx[0]].insertarDespuesDeNodo(v, prev)
                        break
                    prev = actual
                    actual = actual.siguiente
                    
            '''
        else: # no existe la fila m
            self.filas[Idx[0]] = ListaEnlazada()
            self.filas[Idx[0]].insertarFrente((Idx[1], v)) 


    def __mul__( self, k ):
        # Esta funcion implementa el producto matriz-escalar -> A * k
        for key in self.filas.keys():
            current = self.filas[key].raiz
            while current.siguiente is not None:
                current.valor[1] = current.valor[1] * k
                current = current.siguiente
    
    def __rmul__( self, k ):
        # Esta funcion implementa el producto escalar-matriz -> k * A
        return self * k

    def __add__( self, other ):
        # Esta funcion implementa la suma de matrices -> A + B
        if self.shape != other.shape:
            raise Exception('Las matrices deben tener las mismas dimensiones')
        
        matAdd = MatrizRala(self.shape[0], self.shape[1])
        for i in range (self.shape[0]):
            for j in range (self.shape[1]):
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
    
    # poner pivotes (dividir la fila por el valor de la pos que quiero q sea el pivote)
    # hacer 0s arriba y abajo (restar/sumar a la fila la fila que tiene el pivote * el valor de la pos que quiero q sea 0)

    pass