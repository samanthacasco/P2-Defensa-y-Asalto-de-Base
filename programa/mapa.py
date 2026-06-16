from modelo import Base, Muro, Torre, Unidad

class Mapa:
    """Representa el tablero del juego"""

    def __init__(self):
        """Crea un mapa de 21x21 casillas y coloca la base central"""
        self.filas = 21
        self.columnas = 21
        self.matriz = self.crear_matriz()
        self.base = Base()
        self.muros = [ ]
        self.torres = [ ]
        self.unidades = [ ]
 
        self.colocar_base()

    def crear_matriz(self):
        """Crea una matriz de 21x21 inicializada con valores None
        No recibe parámetros 
        Devuelve la matriz creada """
        
        matriz = []
        i = 0
        while i < self.filas:
            fila = []
            j = 0  # contador para columnas

            while j < self.columnas:
                fila.append(None)
                j += 1

            matriz.append(fila)
            i += 1
        return matriz
    
    def colocar_base(self):
        """Coloca la base en la posición central del mapa 
        No recibe parámetros 
        No devuelve nada """

        fila_central = self.filas // 2
        columna_central = self.columnas // 2
        self.base.posicion = (fila_central, columna_central)
        self.matriz[fila_central][columna_central] = self.base

    def colocar_objeto(self, objeto, fila, columna):
        """Coloca un objeto en una posición del mapa si la casilla está libre 
        Recibe el objeto y las coordenadas fila y columna 
        Devuelve True si el objeto fue colocado o False en caso contrario """

        if not (0 <= fila < self.filas and 0 <= columna < self.columnas):
            return False
        
        if self.matriz[fila][columna] is None:
            self.matriz[fila][columna] = objeto
            objeto.posicion = (fila, columna)

            if isinstance(objeto, Muro): 
                self.muros.append(objeto)

            elif isinstance(objeto, Torre):
                self.torres.append(objeto)

            elif isinstance(objeto, Unidad):
                self.unidades.append(objeto)

            return True
        
        return False
    
    def eliminar_objeto(self, objeto):
        """Elimina un objeto del mapa
        Recibe el objeto que se desea eliminar
        Devuelve True si el objeto fue eliminado o False en caso contrario
        """
        
        if objeto.posicion is None:
            return False

        fila, columna = objeto.posicion

        self.matriz[fila][columna] = None
        objeto.posicion = None

        if isinstance(objeto, Muro):
            self.muros.remove(objeto)

        elif isinstance(objeto, Torre):
            self.torres.remove(objeto)

        elif isinstance(objeto, Unidad):
            self.unidades.remove(objeto)

        return True






