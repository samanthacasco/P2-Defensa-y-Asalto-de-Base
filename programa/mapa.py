from modelo import Base, Muro, Torre, Unidad

class Mapa:
    """Representa el tablero del juego"""

    def __init__(self):
        """Crea un mapa de 13x13 casillas y coloca la base central"""
        self.filas = 13
        self.columnas = 13
        self.matriz = self.crear_matriz()
        self.base = Base()
        self.muros = [ ]
        self.torres = [ ]
        self.unidades = [ ]
 
        self.colocar_base()

    def crear_matriz(self):
        """Crea una matriz de 13x13 inicializada con valores None
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

# -------------------------------------

    def mover_objeto(self, objeto, nueva_fila, nueva_columna):
        """Mueve un objeto a una nueva posición del mapa
        Recibe el objeto y las coordenadas de destino
        Devuelve True si el movimiento se realizó o False en caso contrario 
        """

        # Solo las unidades pueden moverse
        if not isinstance(objeto, Unidad):
            return False
        
        # Verifica que la unidad se encuentre colocada en el mapa
        if objeto.posicion is None:
            return False
        
         # Si la unidad está congelada, pierde el turno y se descongela
        if objeto.congelada:
            objeto.congelada = False
            return False
        
        # Verifica que la nueva posición esté dentro del mapa
        if not (0 <= nueva_fila < self.filas and 0 <= nueva_columna < self.columnas):
            return False

        # verifica que la casilla de destino esté vacía
        if self.matriz[nueva_fila][nueva_columna] is not None:
            return False

        # obtiene la posición actual de la unidad
        fila_actual, columna_actual = objeto.posicion

        # libera la casilla donde se encontraba la unidad
        self.matriz[fila_actual][columna_actual] = None

        # coloca la unidad en la nueva posición
        self.matriz[nueva_fila][nueva_columna] = objeto
        
        # actualiza la posición almacenada en la unidad
        objeto.posicion = (nueva_fila, nueva_columna)

        return True # el movimiento se realizó correctamente
    
    def obtener_velocidad_movimiento(self, unidad):
        # Usa la velocidad normal de la unidad
        velocidad = unidad.velocidad

        # Si la unidad tiene aumento de velocidad activo,
        # se suma una casilla extra y luego se desactiva la habilidad
        if unidad.velocidad_aumentada:
            velocidad += 1
            unidad.velocidad_aumentada = False

        return velocidad

    def mover_arriba(self, objeto):
        """Mueve una unidad hacia arriba según su velocidad.
        Recibe la unidad a mover.
        Devuelve True si el movimiento se realizó o False en caso contrario.
        """

        if objeto.posicion is None:
            return False

        fila, columna = objeto.posicion

        velocidad = self.obtener_velocidad_movimiento(objeto)

        return self.mover_objeto(objeto, fila - velocidad, columna)


    def mover_abajo(self, objeto):
        """Mueve una unidad hacia abajo según su velocidad."""

        if objeto.posicion is None:
            return False

        fila, columna = objeto.posicion

        velocidad = self.obtener_velocidad_movimiento(objeto)

        return self.mover_objeto(objeto, fila + velocidad, columna)


    def mover_izquierda(self, objeto):
        """Mueve una unidad hacia la izquierda según su velocidad."""

        if objeto.posicion is None:
            return False

        fila, columna = objeto.posicion

        velocidad = self.obtener_velocidad_movimiento(objeto)

        return self.mover_objeto(objeto, fila, columna - velocidad)


    def mover_derecha(self, objeto):
        """Mueve una unidad hacia la derecha según su velocidad."""

        if objeto.posicion is None:
            return False

        fila, columna = objeto.posicion

        velocidad = self.obtener_velocidad_movimiento(objeto)

        return self.mover_objeto(objeto, fila, columna + velocidad)
    