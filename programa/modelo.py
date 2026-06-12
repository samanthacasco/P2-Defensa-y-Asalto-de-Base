"""
Módulo del juego.
Contiene las clases relacionadas con la base, muros, torres y unidades.
"""

class Base:
    """Representa la base central que debe proteger el defensor"""

    def __init__(self):
        """Crea una base con 1000 puntos de vida"""
        self.vida = 1000

    def recibir_dano(self, dano):
        """Reduce la vida de la base según el daño recibido
        Recibe la cantidad de daño
        No devuelve nada
        """
        self.vida -= dano

    def esta_destruida(self):
        """Indica si la base ha sido destruida
        Devuelve True si la vida es menor o igual a 0
        o False en caso contrario
        """

        if self.vida <= 0:
            return True
        return False
    
class Muro:
    """Representa un muro utilizado para proteger la base"""
    def __init__(self):
        self.vida = 500
        self.costo = 150

    def recibir_dano(self, dano):
        """Reduce la vida del muro según el daño recibido
        Recibe la cantidad de daño
        No devuelve nada
        """

        self.vida -= dano

    def esta_destruido(self):
        """Indica si el muro ha sido destruido
        Devuelve True si la vida es menor o igual a 0
        """

        if self.vida <= 0:
            return True
        return False
    
class Torre:
    """Representa una torre defensiva"""

    def __init__(self, nombre, costo, vida, dano, alcance, habilidad, tiempo_activacion):
        """Crea una torre con sus características
        Recibe nombre, costo, vida, daño, alcance, habilidad especial
        y el tiempo necesario para activar la habilidad
        """
         
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.dano = dano
        self.alcance = alcance
        self.habilidad = habilidad
        self.tiempo_activacion = tiempo_activacion
        self.turnos_transcurridos = 0

    def recibir_dano(self, dano):
        self.vida -= dano

    def esta_destruida(self):
        if self.vida <= 0:
            return True
        return False
    
class TorreBasica(Torre):
    """Representa una torre básica"""

    def __init__(self):
        """Crea una torre básica con estadísticas predeterminadas"""
        super().__init__("Basica",100,150,20,2,"Disparo doble",3)

class TorrePesada(Torre):
    """Representa una torre pesada"""

    def __init__(self):
        super().__init__("Pesada",200,250,40,2,"Danio aumentado",4)

class TorreMagica(Torre):
    """Representa una torre mágica"""

    def __init__(self):
        super().__init__("Magica",150,100,15,3,"Congelar",2)


class Unidad:
    """Representa una unidad atacante"""

    def __init__(self, nombre, costo, vida, dano, velocidad, habilidad, tiempo_activacion):
        """Crea una unidad con sus características
        Recibe nombre, costo, vida, daño, velocidad,
        habilidad especial y tiempo de activación
        """
         
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.dano = dano
        self.velocidad = velocidad
        self.habilidad = habilidad
        self.tiempo_activacion = tiempo_activacion
        self.turnos_transcurridos = 0

    def recibir_dano(self, dano):
        self.vida -= dano

    def esta_destruida(self):
        if self.vida <= 0:
            return True
        return False
    

class Soldado(Unidad):
    """Representa un soldado básico"""

    def __init__(self):
        """Crea un soldado con estadísticas predeterminadas"""
        super().__init__("Soldado",50,100,20,1,"Ataque doble",3)

class Tanque(Unidad):
    """Representa una unidad tipo tanque"""

    def __init__(self):
        super().__init__("Tanque",150,300,40,1,"Escudo temporal",4)

class UnidadRapida(Unidad):
    """Representa una unidad rápida"""

    def __init__(self):
        super().__init__("Unidad rápida",75,80,15,2,"Aumento de velocidad",2)
        