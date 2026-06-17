from combate import atacar 

def habilidad_lista(objeto):
    """Verifica si la habilidad especial del objeto está lista para activarse
    Recibe una unidad o torre
    Devuelve True si la habilidad puede activarse o False en caso contrario
    """

    # aumenta la cantidad de turnos transcurridos
    objeto.turnos_transcurridos += 1

    # verifica si ya se alcanzó el tiempo de activación
    if objeto.turnos_transcurridos >= objeto.tiempo_activacion:

        # reinicia el contador de turnos
        objeto.turnos_transcurridos = 0

        # indica que la habilidad está lista
        return True

    # indica que la habilidad todavía no está disponible
    return False

def ataque_doble(soldado, objetivo, mapa):
    """Permite al soldado realizar dos ataques cuando su habilidad está lista
    Recibe el soldado, el objetivo y el mapa
    Devuelve True si se realizó al menos un ataque o False en caso contrario
    """

    # Verifica si la habilidad especial está lista
    if habilidad_lista(soldado):

        # Realiza el primer ataque
        resultado = atacar(soldado, objetivo, mapa)

        # Si el objetivo sobrevivió, realiza el segundo ataque
        # si el primer ataque destruye a la unidad enemiga, el segundo ataque se pierde
        if not objetivo.esta_destruida():
            atacar(soldado, objetivo, mapa)

        return resultado

    # Si la habilidad no está lista, realiza un ataque normal (o sea, si no han pasado 3 turnos)
    return atacar(soldado, objetivo, mapa)

def disparo_doble(torre, objetivo, mapa):
    """Permite a la torre realizar dos ataques cuando su habilidad está lista
    Recibe la torre, el objetivo y el mapa
    Devuelve True si se realizó al menos un ataque o False en caso contrario
    """

    # verifica si la habilidad especial está lista
    if habilidad_lista(torre):

        # realiza el primer ataque
        resultado = atacar(torre, objetivo, mapa)

        # si el objetivo sobrevivió, realiza el segundo ataque
        # si el primer ataque destruye a la unidad enemiga, el segundo ataque se pierde
        if not objetivo.esta_destruida():
            atacar(torre, objetivo, mapa)

        return resultado

    # si la habilidad no está lista, realiza un ataque normal (o sea, si no han pasado 3 turnos)
    return atacar(torre, objetivo, mapa)

def danio_aumentado(torre, objetivo, mapa):
    """Permite a la torre pesada aumentar temporalmente su daño
    Recibe la torre, el objetivo y el mapa
    Devuelve True si se realizó el ataque o False en caso contrario
    """

    # verifica si la habilidad especial está lista
    if habilidad_lista(torre):

        # guarda el daño original de la torre
        dano_original = torre.dano

        # aumenta temporalmente el daño
        torre.dano += 20

        # realiza el ataque
        resultado = atacar(torre, objetivo, mapa)

        # restaura el daño original
        torre.dano = dano_original

        return resultado

    # si la habilidad no está lista, realiza un ataque normal
    return atacar(torre, objetivo, mapa)

