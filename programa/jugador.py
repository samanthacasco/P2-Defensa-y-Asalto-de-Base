"""
Módulo de gestión de jugadores.
Contiene la clase Jugador y las funciones para registrar, iniciar sesión
y guardar/cargar jugadores en un archivo JSON.
"""
import json

class Jugador:
    """Representa a un jugador con sus credenciales y su historial de victorias."""
    def __init__(self, usuario, clave):
        """Crea un jugador nuevo con las victorias en cero.
        Recibe el usuario y la clave; las victorias siempre arrancan en 0.
        """
        
        self.usuario = usuario
        self.clave = clave
        self.victorias_defensor = 0
        self.victorias_atacante = 0
    
    def agregar_victoria(self, rol):
        """Suma una victoria al jugador según el rol recibido ('defensor' o 'atacante').
        No devuelve nada; modifica el contador correspondiente.
        """
        
        if rol == "defensor":
            self.victorias_defensor += 1
        else:
            self.victorias_atacante += 1
    
    def diccionario(self):
        """Convierte los datos del jugador en un diccionario para guardarlo en JSON.
        Devuelve un diccionario con el usuario, la clave y las victorias.
        """
        
        return {"usuario": self.usuario, "clave": self.clave, "victorias_defensor": self.victorias_defensor, "victorias_atacante": self.victorias_atacante}

def guardar_jugadores(lista_jugadores):
    """Guarda la lista de jugadores en el archivo jugadores.json en formato JSON.
    Recibe la lista de objetos Jugador.
    No devuelve nada; escribe los datos en el archivo.
    """
    
    lista_diccionario = []
    for jugador in lista_jugadores:
        lista_diccionario.append(jugador.diccionario())    
    with open("jugadores.json", "w", encoding="utf-8") as archivo:
        json.dump(lista_diccionario, archivo, indent=4)

def cargar_jugadores():
    """Lee los jugadores del archivo jugadores.json y los reconstruye como objetos Jugador.
    Devuelve la lista de jugadores.
    Si el archivo no existe todavía, devuelve una lista vacía.
    """
    
    try:
        with open("jugadores.json", "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        return []
    
    lista_jugadores = []
    for d in datos:
        jugador = Jugador(d["usuario"], d["clave"])
        jugador.victorias_defensor = d["victorias_defensor"]
        jugador.victorias_atacante = d["victorias_atacante"] 
        lista_jugadores.append(jugador)   
    return lista_jugadores        

def registrar(usuario, clave):
    """Registra un jugador nuevo si el usuario no está repetido.
    El usuario se guarda en mayúsculas, de modo que "Samy" y "samy" se
    consideran el mismo usuario y siempre se muestra en mayúsculas.
    Recibe el usuario y la clave del nuevo jugador.
    Devuelve False si ya existe un jugador con ese usuario,
    o True si el registro se realizó con éxito.
    """
    
    lista_jugadores = cargar_jugadores()
    for jugador in lista_jugadores:
        if jugador.usuario == usuario.upper():
            return False
    jugador = Jugador(usuario.upper(), clave)
    lista_jugadores.append(jugador)
    guardar_jugadores(lista_jugadores)
    return True

def login(usuario, clave):
    """Busca un jugador cuyo usuario y clave coincidan.
    El usuario se compara en mayúsculas (como se guarda), pero la clave
    se compara de forma exacta (distingue mayúsculas, por seguridad).
    Devuelve el objeto Jugador si la combinación es correcta,
    o None si el usuario no existe o la clave es incorrecta.
    """
    
    lista_jugadores = cargar_jugadores()
    for jugador in lista_jugadores:
        if jugador.usuario == usuario.upper() and jugador.clave == clave:
            return jugador
    return None

def ranking_defensores():
    """Ordena los jugadores de mayor a menor según sus victorias como defensor.
    Devuelve una lista con los 5 jugadores con más victorias de defensor
    (o menos, si hay menos de 5 jugadores registrados).
    """
    lista_jugadores = cargar_jugadores()
    lista_ordenada = sorted(lista_jugadores, key=lambda jugador: jugador.victorias_defensor, reverse=True)
    top5 = lista_ordenada[:5]
    return top5

def ranking_atacantes():
    """Ordena los jugadores de mayor a menor según sus victorias como atacante.
    Devuelve una lista con los 5 jugadores con más victorias de atacante
    (o menos, si hay menos de 5 jugadores registrados).
    """
    lista_jugadores = cargar_jugadores()
    lista_ordenada = sorted(lista_jugadores, key=lambda jugador: jugador.victorias_atacante, reverse=True)
    top5 = lista_ordenada[:5]
    return top5
