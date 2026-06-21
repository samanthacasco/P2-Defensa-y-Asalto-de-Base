from mapa import Mapa
from economia import agregar_recursos
from jugador import cargar_jugadores, guardar_jugadores

class Partida:
    def __init__(self, jugador_defensor, jugador_atacante):
        """Crea una partida nueva entre dos jugadores.
        Recibe el jugador defensor y el jugador atacante.
        El dinero inicial, el marcador de rondas y el turno arrancan en valores fijos
        (dinero inicial para ambos, rondas en cero y el primer turno para el defensor).
        """
        self.jugador_defensor = jugador_defensor
        self.jugador_atacante = jugador_atacante
        
        self.dinero_defensor = 500
        self.dinero_atacante = 500
        self.rondas_defensor = 0
        self.rondas_atacante = 0
        self.mapa = Mapa()
        self.turno = 1
        self.jugador_actual = "defensor"
        self.faccion_defensor = None
        self.faccion_atacante = None
    
    def cambiar_turno(self):
        """Avanza al siguiente turno y alterna el jugador actual.
        No recibe nada; aumenta el contador y cambia de defensor a atacante o viceversa.
        """
        self.turno += 1
        if self.jugador_actual == "defensor":
            self.jugador_actual = "atacante"
        else:
            self.jugador_actual = "defensor"
            agregar_recursos(self)
    
    def obtener_jugador_actual(self):
        """Devuelve el jugador al que le corresponde jugar"""

        if self.jugador_actual == "defensor":
            return self.jugador_defensor

        return self.jugador_atacante
    

    def gano_defensor(self):
        """Indica si el defensor ganó la ronda.
        El defensor gana si el atacante se quedó sin dinero, sin unidades en el mapa
        y la base central sigue en pie.
        Devuelve True si el defensor ganó, False en caso contrario.
        """
        if (self.dinero_atacante <= 0 and len(self.mapa.unidades) == 0 and not self.mapa.base.esta_destruida()):
            return True
        return False
    
    def gano_atacante(self):
        """Indica si el atacante ganó la ronda.
        El atacante gana cuando destruye la base central.
        Devuelve True si ganó la ronda o False en caso contrario.
        """

        if self.mapa.base.esta_destruida():
            return True

        return False
    
    def registrar_ronda(self):
        """Actualiza el marcador de rondas ganadas.
        No recibe parámetros ni devuelve nada.
        """

        if self.gano_defensor():
            self.rondas_defensor += 1

        elif self.gano_atacante():
            self.rondas_atacante += 1

    def obtener_ganador(self):
        """Devuelve el ganador de la partida.
        El primer jugador en ganar 3 rondas gana la partida.
        Devuelve 'defensor', 'atacante' o None.
        """

        if self.rondas_defensor >= 3:
            return "defensor"

        if self.rondas_atacante >= 3:
            return "atacante"
        return None
    
    def actualizar_victorias(self):
        """Suma una victoria al jugador ganador de la partida y la guarda en el archivo.
        Determina el ganador, lo busca en la lista de jugadores guardados,
        le suma la victoria según su rol y guarda la lista actualizada.
        """
        ganador = self.obtener_ganador()
        if ganador is None:
            return
         
        if ganador == "defensor":
            usuario_ganador = self.jugador_defensor.usuario
        else:
            usuario_ganador = self.jugador_atacante.usuario
        
        lista_jugadores = cargar_jugadores()
        for jugador in lista_jugadores:
            if jugador.usuario == usuario_ganador:
                jugador.agregar_victoria(ganador)
        
        guardar_jugadores(lista_jugadores)  
        
