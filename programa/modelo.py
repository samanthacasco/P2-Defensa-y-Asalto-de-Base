"""
Módulo del juego.
Contiene las clases relacionadas con la base, muros, torres y unidades.
"""

class Base:
    """Representa la base central que debe proteger el defensor"""

    def __init__(self):
        """Crea una base con 1000 puntos de vida"""
        self.vida = 1000
        self.posicion = None
        self.imagen = "imagenes/base.png"

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
        self.posicion = None
        self.imagen = "imagenes/muro.png"

    def recibir_dano(self, dano):
        """Reduce la vida del muro según el daño recibido
        Recibe la cantidad de daño
        No devuelve nada
        """

        self.vida -= dano

    def esta_destruida(self):
        """Indica si el muro ha sido destruido
        Devuelve True si la vida es menor o igual a 0
        """

        if self.vida <= 0:
            return True
        return False
    
class Torre:
    """Representa una torre defensiva"""

    def __init__(self, nombre, costo, vida, dano, alcance, habilidad, tiempo_activacion, imagen):
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
        self.posicion = None
        self.imagen = imagen

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
        super().__init__("Basica",100,150,20,2,"Disparo doble",3,"imagenes/torre_basica.png")

class TorrePesada(Torre):
    """Representa una torre pesada"""

    def __init__(self):
        super().__init__("Pesada",200,250,40,2,"Danio aumentado",4,"imagenes/torre_pesada.png")

class TorreMagica(Torre):
    """Representa una torre mágica"""

    def __init__(self):
        super().__init__("Magica",150,100,15,3,"Congelar",2,"imagenes/torre_magica.png")


class Unidad:
    """Representa una unidad atacante"""

    def __init__(self, nombre, costo, vida, dano, velocidad, alcance, habilidad, tiempo_activacion, imagen):
        """Crea una unidad con sus características
        Recibe nombre, costo, vida, daño, velocidad,
        habilidad especial y tiempo de activación
        """
         
        self.nombre = nombre
        self.costo = costo
        self.vida = vida
        self.dano = dano
        self.velocidad = velocidad
        self.alcance = alcance 
        self.habilidad = habilidad
        self.tiempo_activacion = tiempo_activacion
        self.turnos_transcurridos = 0
        self.posicion = None
        self.imagen = imagen

        # indica si la unidad está congelada y no puede moverse
        self.congelada = False

        # Indica si la unidad tiene un escudo temporal activo
        self.escudo_activo = False

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
        super().__init__("Soldado",50,100,20,1,1,"Ataque doble",3, "imagenes/soldado.png")

class Tanque(Unidad):
    """Representa una unidad tipo tanque"""

    def __init__(self):
        super().__init__("Tanque",150,300,40,1,2,"Escudo temporal",4, "imagenes/tanque.png")

class UnidadRapida(Unidad):
    """Representa una unidad rápida"""

    def __init__(self):
        super().__init__("Unidad rapida",75,80,15,2,1,"Aumento de velocidad",2,"imagenes/unidad_rapida.png")
        

class Faccion:
    """Representa una facción del juego """

    def __init__(self, nombre,imagen_base, imagen_muro, imagen_torre_basica, imagen_torre_pesada, imagen_torre_magica, imagen_soldado, imagen_tanque, imagen_unidad_rapida):
        """Crea una facción con un nombre y las imagenes de sus estructuras y unidades
        Recibe el nombre y las imagenes correspondientes
        """
         
        self.nombre = nombre
        self.imagen_base = imagen_base
        self.imagen_muro = imagen_muro
        self.imagen_torre_basica = imagen_torre_basica
        self.imagen_torre_pesada = imagen_torre_pesada
        self.imagen_torre_magica = imagen_torre_magica
        self.imagen_soldado = imagen_soldado
        self.imagen_tanque = imagen_tanque
        self.imagen_unidad_rapida = imagen_unidad_rapida

class Medieval(Faccion):
    """Representa la faccion medieval"""

    def __init__(self):
        """Crea una facción medieval con sus imágenes correspondientes"""

        super().__init__("Medieval", "imagenes/medieval/base.png", "imagenes/medieval/muro.png", "imagenes/medieval/torre_basica.png", "imagenes/medieval/torre_pesada.png", "imagenes/medieval/torre_magica.png", "imagenes/medieval/soldado.png", "imagenes/medieval/tanque.png", "imagenes/medieval/unidad_rapida.png")

class Futurista(Faccion):
    def __init__(self):
        super().__init__("Futurista",  "imagenes/futurista/base.png", "imagenes/futurista/muro.png", "imagenes/futurista/torre_basica.png", "imagenes/futurista/torre_pesada.png", "imagenes/futurista/torre_magica.png", "imagenes/futurista/soldado.png", "imagenes/futurista/tanque.png", "imagenes/futurista/unidad_rapida.png")

class Naturaleza(Faccion):
    def __init__(self):
        super().__init__("Naturaleza",  "imagenes/naturaleza/base.png", "imagenes/naturaleza/muro.png", "imagenes/naturaleza/torre_basica.png", "imagenes/naturaleza/torre_pesada.png", "imagenes/naturaleza/torre_magica.png", "imagenes/naturaleza/soldado.png", "imagenes/naturaleza/tanque.png", "imagenes/naturaleza/unidad_rapida.png")
