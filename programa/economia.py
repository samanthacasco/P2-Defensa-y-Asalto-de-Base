"""
Módulo de economía.
Contiene las funciones para comprar torres, muros y unidades,
verificando el dinero del jugador y colocando el objeto en el mapa.
"""

def comprar_torre(partida, torre, fila, columna, rol):
    """Compra y coloca una torre si el jugador tiene dinero suficiente.
    Recibe la partida, la torre, la posición (fila, columna) y el rol del jugador.
    Devuelve True si la compra y colocación tuvieron éxito, False si no.
    """
    if rol == "defensor":
        dinero = partida.dinero_defensor 
    else:
        dinero = partida.dinero_atacante
    
    if dinero < torre.costo:
        return False
    
    if not partida.mapa.colocar_objeto(torre, fila, columna):
        return False
    
    if rol == "defensor":
        partida.dinero_defensor -= torre.costo
    else:
        partida.dinero_atacante -= torre.costo
    return True

def comprar_muro(partida, muro, fila, columna, rol):
    """Compra y coloca un muro si el jugador tiene dinero suficiente.
    Recibe la partida, el muro, la posición (fila, columna) y el rol del jugador.
    Devuelve True si la compra y colocación tuvieron éxito, False si no.
    """
    if rol == "defensor":
        dinero = partida.dinero_defensor 
    else:
        dinero = partida.dinero_atacante
    
    if dinero < muro.costo:
        return False
    
    if not partida.mapa.colocar_objeto(muro, fila, columna):
        return False
    
    if rol == "defensor":
        partida.dinero_defensor -= muro.costo
    else:
        partida.dinero_atacante -= muro.costo
    return True

def comprar_unidad(partida, unidad, fila, columna, rol):
    """Compra y coloca una unidad si el jugador tiene dinero suficiente.
    Recibe la partida, la unidad, la posición (fila, columna) y el rol del jugador.
    Devuelve True si la compra y colocación tuvieron éxito, False si no.
    """
    if rol == "defensor":
        dinero = partida.dinero_defensor 
    else:
        dinero = partida.dinero_atacante
    
    if dinero < unidad.costo:
        return False
    
    if not partida.mapa.colocar_objeto(unidad, fila, columna):
        return False
    
    if rol == "defensor":
        partida.dinero_defensor -= unidad.costo
    else:
        partida.dinero_atacante -= unidad.costo
    return True

def agregar_recursos(partida):
    """Agrega recursos al inicio de una ronda.
    Recibe la partida.
    No devuelve nada.
    """

    recursos_por_ronda = 50

    # aumenta el dinero del defensor
    partida.dinero_defensor += recursos_por_ronda

    # aumenta el dinero del atacante
    partida.dinero_atacante += recursos_por_ronda

def recompensa_atacante(partida, dano_realizado):
    """Otorga dinero al atacante según el daño realizado.
    Recibe la partida y el daño realizado.
    No devuelve nada.
    """

    partida.dinero_atacante += dano_realizado // 10

def recompensa_defensor(partida, unidades_eliminadas):
    """Otorga dinero al defensor por cada unidad eliminada.
    Recibe la partida y la cantidad de unidades eliminadas.
    No devuelve nada.
    """

    recompensa_por_unidad = 20

    partida.dinero_defensor += unidades_eliminadas * recompensa_por_unidad