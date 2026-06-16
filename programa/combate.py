from modelo import Base 

def esta_al_alcance(atacante, objetivo):
    """Verifica si un objetivo se encuentra al alcance de ataque
    Recibe el objeto atacante y el objeto objetivo
    Devuelve True si el objetivo está al alcance o False en caso contrario
    """

    # Verifica que ambos objetos estén colocados en el mapa
    if atacante.posicion is None or objetivo.posicion is None:
        return False

    # Obtiene las posiciones del atacante y del objetivo
    fila_atacante, columna_atacante = atacante.posicion
    fila_objetivo, columna_objetivo = objetivo.posicion

    # Calcula la distancia entre ambas posiciones
    distancia = abs(fila_atacante - fila_objetivo) + \
                abs(columna_atacante - columna_objetivo)

    # Verifica si la distancia es menor o igual al alcance del atacante
    if distancia <= atacante.alcance:
        return True

    return False

def atacar(atacante, objetivo, mapa):
    """Realiza un ataque sobre un objetivo
    Recibe el objeto atacante, el objetivo y el mapa
    Devuelve True si el ataque se realizó o False en caso contrario
    """
    # Verifica que el objetivo se encuentre al alcance
    if not esta_al_alcance(atacante, objetivo):
        return False 
    
    # Reduce la vida del objetivo según el daño del atacante
    objetivo.recibir_dano(atacante.dano)

    # Verifica si el objetivo fue destruido
    if objetivo.esta_destruida():

        # Elimina el objetivo del mapa si no es la base
        if not isinstance(objetivo, Base):
            mapa.eliminar_objetivo(objetivo)

    # Indica que el ataque se realizó correctamente
    return True



