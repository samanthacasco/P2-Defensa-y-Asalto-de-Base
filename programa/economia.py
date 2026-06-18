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
