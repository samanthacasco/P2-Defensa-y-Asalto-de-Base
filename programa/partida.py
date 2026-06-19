from mapa import Mapa

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
    
    def cambiar_turno(self):
        """Avanza al siguiente turno y alterna el jugador actual.
        No recibe nada; aumenta el contador y cambia de defensor a atacante o viceversa.
        """
        self.turno += 1
        if self.jugador_actual == "defensor":
            self.jugador_actual = "atacante"
        else:
            self.jugador_actual = "defensor"
    
    def gano_defensor(self):
        """Indica si el defensor ganó la ronda.
        El defensor gana si el atacante se quedó sin dinero y sin unidades en el mapa.
        Devuelve True si el defensor ganó, False en caso contrario.
        """
        if self.dinero_atacante <= 0 and len(self.mapa.unidades) == 0:
            return True
        return False
        
        

        
