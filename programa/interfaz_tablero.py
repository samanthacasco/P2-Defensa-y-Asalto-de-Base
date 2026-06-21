import tkinter as tk
from tkinter import messagebox
from utilidades import centrar_ventana, limpiar_ventana, cargar_imagen, crear_imagen_vacia
from modelo import (Base, Muro, Torre, Unidad, TorreBasica, TorrePesada, TorreMagica,
                    Soldado, Tanque, UnidadRapida)
from economia import comprar_unidad, comprar_torre, comprar_muro
from combate import atacar, esta_al_alcance
from habilidades import (ataque_doble, disparo_doble, danio_aumentado, congelar, escudo_temporal, aumento_velocidad)


tablero_iniciado = False

def obtener_imagen(contenido, partida):
    """Devuelve la ruta de imagen correcta para un objeto según su tipo y la facción de su dueño.
    Recibe el objeto del mapa y la partida.
    Devuelve la ruta (texto) de la imagen de la facción correspondiente.
    """
    # La base, los muros y las torres son del defensor
    if isinstance(contenido, Base):
        return partida.faccion_defensor.imagen_base
    elif isinstance(contenido, Muro):
        return partida.faccion_defensor.imagen_muro
    elif isinstance(contenido, TorreBasica):
        return partida.faccion_defensor.imagen_torre_basica
    elif isinstance(contenido, TorrePesada):
        return partida.faccion_defensor.imagen_torre_pesada
    elif isinstance(contenido, TorreMagica):
        return partida.faccion_defensor.imagen_torre_magica
    # Las unidades son del atacante
    elif isinstance(contenido, Soldado):
        return partida.faccion_atacante.imagen_soldado
    elif isinstance(contenido, Tanque):
        return partida.faccion_atacante.imagen_tanque
    elif isinstance(contenido, UnidadRapida):
        return partida.faccion_atacante.imagen_unidad_rapida


def seleccionar_objeto(ventana, objeto):
    """Guarda el objeto seleccionado del tablero
    Recibe la ventana y el objeto seleccionado
    No devuelve nada
    """
    ventana.objeto_seleccionado = objeto


def mover_arriba_interfaz(ventana, partida):
    """Mueve hacia arriba la unidad seleccionada
    Recibe la ventana y la partida
    No devuelve nada
    """
    # solo las unidades pueden moverse (las torres y muros no tienen velocidad)
    if ventana.objeto_seleccionado is not None and isinstance(ventana.objeto_seleccionado, Unidad):
        partida.mapa.mover_arriba(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


def mover_abajo_interfaz(ventana, partida):
    """Mueve hacia abajo la unidad seleccionada"""
    # solo las unidades pueden moverse
    if ventana.objeto_seleccionado is not None and isinstance(ventana.objeto_seleccionado, Unidad):
        partida.mapa.mover_abajo(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


def mover_izquierda_interfaz(ventana, partida):
    """Mueve hacia la izquierda la unidad seleccionada"""
    # solo las unidades pueden moverse
    if ventana.objeto_seleccionado is not None and isinstance(ventana.objeto_seleccionado, Unidad):
        partida.mapa.mover_izquierda(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


def mover_derecha_interfaz(ventana, partida):
    """Mueve hacia la derecha la unidad seleccionada"""
    # solo las unidades pueden moverse
    if ventana.objeto_seleccionado is not None and isinstance(ventana.objeto_seleccionado, Unidad):
        partida.mapa.mover_derecha(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


# ---- compras del atacante ----
def comprar_soldado_interfaz(ventana, partida):
    """Compra un soldado y lo coloca en la casilla seleccionada"""

    if partida.jugador_actual != "atacante":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar unidades en el turno del atacante.")
        return

    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return

    soldado = Soldado()
    compra_exitosa = comprar_unidad(partida, soldado, ventana.fila_seleccionada, ventana.columna_seleccionada, "atacante")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


def comprar_tanque_interfaz(ventana, partida):
    """Compra un tanque y lo coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual != "atacante":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar unidades en el turno del atacante.")
        return
    
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return

    tanque = Tanque()
    compra_exitosa = comprar_unidad(partida, tanque, ventana.fila_seleccionada, ventana.columna_seleccionada, "atacante")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


def comprar_unidad_rapida_interfaz(ventana, partida):
    """Compra una unidad rápida y la coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual != "atacante":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar unidades en el turno del atacante.")
        return
    
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return

    unidad_rapida = UnidadRapida()
    compra_exitosa = comprar_unidad(partida, unidad_rapida, ventana.fila_seleccionada, ventana.columna_seleccionada, "atacante")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


# ---- compras del defensor ----
def comprar_muro_interfaz(ventana, partida):
    """Compra un muro y lo coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual != "defensor":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar torres y muros en el turno del defensor.")
        return
    
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return

    muro = Muro()
    compra_exitosa = comprar_muro(partida, muro, ventana.fila_seleccionada, ventana.columna_seleccionada, "defensor")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


def comprar_torre_basica_interfaz(ventana, partida):
    """Compra una torre básica..."""

    if partida.jugador_actual != "defensor":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar torres y muros en el turno del defensor.")
        return
    
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return
    
    torre = TorreBasica()
    compra_exitosa = comprar_torre(partida, torre, ventana.fila_seleccionada, ventana.columna_seleccionada, "defensor")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


def comprar_torre_pesada_interfaz(ventana, partida):
    """Compra una torre pesada y la coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual != "defensor":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar torres y muros en el turno del defensor.")
        return
    
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return

    torre = TorrePesada()
    compra_exitosa = comprar_torre(partida, torre, ventana.fila_seleccionada, ventana.columna_seleccionada, "defensor")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


def comprar_torre_magica_interfaz(ventana, partida):
    """Compra una torre mágica y la coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual != "defensor":
        messagebox.showwarning("No es tu turno", "Solo puedes comprar torres y muros en el turno del defensor.")
        return

    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        messagebox.showwarning("Casilla no seleccionada", "Primero selecciona una casilla del tablero.")
        return

    torre = TorreMagica()
    compra_exitosa = comprar_torre(partida, torre, ventana.fila_seleccionada, ventana.columna_seleccionada, "defensor")

    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        messagebox.showerror("Compra fallida", "No hay dinero suficiente o la casilla está ocupada.")


# ---- selección de casillas ----
def seleccionar_casilla(ventana, fila, columna):
    """Guarda la posición de una casilla seleccionada.
    Recibe la ventana y las coordenadas de la casilla.
    No devuelve nada.
    """
    ventana.fila_seleccionada = fila
    ventana.columna_seleccionada = columna


def seleccionar_casilla_y_objeto(ventana, fila, columna, objeto):
    """Guarda la casilla seleccionada y el objeto que está en esa casilla.
    Recibe la ventana, la fila, la columna y el objeto de la casilla.
    No devuelve nada.
    """

    # Guarda la fila seleccionada
    ventana.fila_seleccionada = fila

    # Guarda la columna seleccionada
    ventana.columna_seleccionada = columna

    # Guarda el objeto seleccionado
    # Si la casilla está vacía, objeto será None
    ventana.objeto_seleccionado = objeto

    # Actualiza la información de la casilla seleccionada
    ventana.label_casilla.config(text=f"Casilla seleccionada: ({fila}, {columna})")

    # Actualiza la información del objeto seleccionado
    if objeto is None:
        ventana.label_objeto.config(text="Objeto seleccionado: Ninguno")

    elif isinstance(objeto, Base):
        ventana.label_objeto.config(text="Objeto seleccionado: Base")

    elif isinstance(objeto, Muro):
        ventana.label_objeto.config(text="Objeto seleccionado: Muro")

    else:
        ventana.label_objeto.config(text=f"Objeto seleccionado: {objeto.nombre}")

    if objeto is None:
        ventana.label_vida.config(text="Vida: -")
        
    else:
        ventana.label_vida.config(text=f"Vida: {objeto.vida}")

def terminar_turno_interfaz(ventana, partida):
    """Termina el turno actual y pasa al siguiente jugador.
    El combate de las torres ya no ocurre aquí: el atacante lo inicia con el botón
    'Iniciar combate'. Esta función solo cambia el turno y revisa el fin de ronda.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    partida.cambiar_turno()
    revisar_fin_de_ronda(ventana, partida)

def seleccionar_atacante(ventana):
    """Guarda el objeto seleccionado como atacante"""

    if ventana.objeto_seleccionado is None:
        messagebox.showwarning("Sin objeto", "Primero selecciona un objeto del tablero.")
        return

    if isinstance(ventana.objeto_seleccionado, (Base, Muro)):
        messagebox.showwarning("No puede atacar", "La base y los muros no pueden atacar. Selecciona una torre o una unidad.")
        return

    ventana.atacante_seleccionado = ventana.objeto_seleccionado
    messagebox.showinfo("Atacante seleccionado", "El atacante fue seleccionado correctamente.")
    

def seleccionar_objetivo(ventana):
    """Guarda el objeto seleccionado como objetivo"""

    if ventana.objeto_seleccionado is None:
        messagebox.showwarning("Sin objeto","Primero selecciona un objeto del tablero.")
        return

    ventana.objetivo_seleccionado = ventana.objeto_seleccionado
    messagebox.showinfo("Objetivo seleccionado","El objetivo fue seleccionado correctamente.")
#____________________

def ejecutar_ataque_con_habilidad(atacante, objetivo, mapa):
    """Ejecuta el ataque correspondiente según el tipo de atacante.
    Recibe el atacante, el objetivo y el mapa.
    Devuelve el resultado del ataque y el nombre de la habilidad usada.
    """

    # Guarda cuántos turnos llevaba antes del ataque
    turnos_antes = atacante.turnos_transcurridos

    # Soldado: ataque doble
    if isinstance(atacante, Soldado):
        resultado = ataque_doble(atacante, objetivo, mapa)

        if turnos_antes + 1 >= atacante.tiempo_activacion:
            return resultado, "Ataque doble"

        return resultado, None

    # Torre básica: disparo doble
    elif isinstance(atacante, TorreBasica):
        resultado = disparo_doble(atacante, objetivo, mapa)

        if turnos_antes + 1 >= atacante.tiempo_activacion:
            return resultado, "Disparo doble"

        return resultado, None

    # Torre pesada: daño aumentado
    elif isinstance(atacante, TorrePesada):
        resultado = danio_aumentado(atacante, objetivo, mapa)

        if turnos_antes + 1 >= atacante.tiempo_activacion:
            return resultado, "Daño aumentado"

        return resultado, None

    # Torre mágica: congelar
    elif isinstance(atacante, TorreMagica):
        resultado = congelar(atacante, objetivo, mapa)

        if turnos_antes + 1 >= atacante.tiempo_activacion:
            return resultado, "Congelar"

        return resultado, None

    # Si no tiene habilidad ofensiva, ataca normal
    resultado = atacar(atacante, objetivo, mapa)
    return resultado, None


def atacar_interfaz(ventana, partida):
    """Realiza un ataque usando el atacante y el objetivo seleccionados.
    Recibe la ventana y la partida.
    No devuelve nada.
    """

    # Verifica que haya un atacante seleccionado
    if ventana.atacante_seleccionado is None:
        messagebox.showwarning("Sin atacante","Primero selecciona un atacante.")
        return

    # Verifica que haya un objetivo seleccionado
    if ventana.objetivo_seleccionado is None:
        messagebox.showwarning( "Sin objetivo", "Primero selecciona un objetivo.")
        return

    # Guarda la vida del objetivo antes del ataque
    vida_antes = ventana.objetivo_seleccionado.vida

    # Intenta realizar el ataque usando la función de combate.py
    ataque_exitoso , habilidad_usada = ejecutar_ataque_con_habilidad(ventana.atacante_seleccionado,ventana.objetivo_seleccionado,partida.mapa)

    # Si el objetivo no estaba al alcance, muestra un mensaje
    if not ataque_exitoso:
        messagebox.showerror("Ataque fallido", "El objetivo no está al alcance o el ataque no se pudo realizar." )
        return

    # Calcula la vida después del ataque
    vida_despues = ventana.objetivo_seleccionado.vida

    # Calcula cuánto daño se realizó
    dano_realizado = vida_antes - vida_despues

    # Si el atacante dañó una torre o la base, gana dinero extra
    if isinstance(ventana.objetivo_seleccionado, (Torre, Base)):
        partida.dinero_atacante += dano_realizado
    
    # Si el objetivo destruido era una unidad, el defensor gana dinero
    if ventana.objetivo_seleccionado.esta_destruida() and isinstance(ventana.objetivo_seleccionado, Unidad):
        partida.dinero_defensor += ventana.objetivo_seleccionado.costo

    # Prepara el texto de la habilidad si se activó alguna
    if habilidad_usada is not None:
        texto_habilidad = f"Habilidad activada: {habilidad_usada}\n"
    else:
        texto_habilidad = ""
   
    # Si el objetivo fue destruido
    if ventana.objetivo_seleccionado.esta_destruida():
        messagebox.showinfo("Objetivo destruido",f"{texto_habilidad}El ataque realizó {dano_realizado} de daño y el objetivo fue destruido.")
    else:
        messagebox.showinfo("Ataque realizado", f"{texto_habilidad}Daño realizado: {dano_realizado}\nVida restante: {vida_despues}")
        
    # Actualiza el tablero y la información visual
    revisar_fin_de_ronda(ventana, partida)

def buscar_objetivo_defensor(unidad, partida):
    """Busca un objetivo del defensor (torre, muro o base) en el alcance de la unidad.
    Da prioridad a torres, luego muros, y por último la base.
    Recibe la unidad atacante y la partida.
    Devuelve el objetivo encontrado o None.
    """
    for torre in partida.mapa.torres:
        if esta_al_alcance(unidad, torre):
            return torre
    for muro in partida.mapa.muros:
        if esta_al_alcance(unidad, muro):
            return muro
    if esta_al_alcance(unidad, partida.mapa.base):
        return partida.mapa.base
    return None


def combate_automatico(partida):
    """Ejecuta toda la fase de combate automáticamente.
    Primero las torres atacan a las unidades en su alcance;
    luego las unidades atacan a las torres, muros o la base en su alcance.
    Recibe la partida.
    Devuelve una lista de textos describiendo lo que ocurrió.
    """
    eventos = []   # textos para el resumen visual

    # 1) las torres atacan a las unidades en su alcance
    for torre in list(partida.mapa.torres):
        for unidad in list(partida.mapa.unidades):
            if esta_al_alcance(torre, unidad):
                vida_antes = unidad.vida
                atacar(torre, unidad, partida.mapa)
                dano = vida_antes - unidad.vida

                if unidad.esta_destruida():
                    eventos.append(f"Torre {torre.nombre} eliminó a {unidad.nombre} ({dano} de daño)")
                else:
                    eventos.append(f"Torre {torre.nombre} dañó a {unidad.nombre}: {dano} (le queda {unidad.vida})")
                break   # cada torre ataca a una sola unidad

    # 2) las unidades atacan a las torres, muros o la base en su alcance
    for unidad in list(partida.mapa.unidades):
        objetivo = buscar_objetivo_defensor(unidad, partida)
        if objetivo is not None:
            vida_antes = objetivo.vida
            atacar(unidad, objetivo, partida.mapa)
            dano = vida_antes - objetivo.vida

            # nombre legible del objetivo
            if isinstance(objetivo, Base):
                nombre_obj = "la Base"
            elif isinstance(objetivo, Muro):
                nombre_obj = "un Muro"
            else:
                nombre_obj = f"la Torre {objetivo.nombre}"

            if objetivo.esta_destruida() and not isinstance(objetivo, Base):
                eventos.append(f"{unidad.nombre} destruyó {nombre_obj} ({dano} de daño)")
            else:
                eventos.append(f"{unidad.nombre} atacó {nombre_obj}: {dano} de daño")

    return eventos


def iniciar_combate_interfaz(ventana, partida):
    """Ejecuta la fase de combate automática (torres y unidades atacan solas) y muestra
    un resumen visual. Solo se inicia en el turno del atacante, tras mover sus unidades.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual != "atacante":
        messagebox.showwarning("No es tu turno", "El combate se inicia en el turno del atacante, luego de mover tus unidades.")
        return

    # ejecuta toda la fase de combate y obtiene el resumen
    eventos = combate_automatico(partida)

    # muestra el resumen visual de lo que pasó
    if eventos:
        resumen = "\n".join(eventos)
        messagebox.showinfo("Fase de combate", resumen)
    else:
        messagebox.showinfo("Fase de combate", "No hubo enemigos en alcance este turno.")

    # revisa si terminó la ronda o la partida tras el combate
    revisar_fin_de_ronda(ventana, partida)
            
def activar_habilidad_interfaz(ventana, partida):
    """Activa la habilidad especial de una unidad seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """

    # Verifica que haya un objeto seleccionado
    if ventana.objeto_seleccionado is None:
        messagebox.showwarning( "Sin objeto", "Primero selecciona una unidad.")
        return

    # Si el objeto seleccionado es un tanque, intenta activar escudo temporal
    if isinstance(ventana.objeto_seleccionado, Tanque):
        habilidad_activada = escudo_temporal(ventana.objeto_seleccionado)

        if habilidad_activada:
            messagebox.showinfo("Habilidad activada","El tanque activó Escudo temporal." )
        else:
            messagebox.showinfo("Habilidad no disponible","El escudo temporal todavía no está listo.")

    # Si el objeto seleccionado es una unidad rápida, intenta activar aumento de velocidad
    elif isinstance(ventana.objeto_seleccionado, UnidadRapida):
        habilidad_activada = aumento_velocidad(ventana.objeto_seleccionado)

        if habilidad_activada:
            messagebox.showinfo( "Habilidad activada", "La unidad rápida activó Aumento de velocidad." )
        else:
            messagebox.showinfo("Habilidad no disponible", "El aumento de velocidad todavía no está listo." )

    # Si selecciona otro objeto, no tiene esta habilidad
    else:
        messagebox.showwarning("Habilidad no válida","Este objeto no tiene una habilidad activable desde este botón.")
        return

    # Actualiza la interfaz
    mostrar_tablero(ventana, partida)

#____________________

def texto_ayuda(partida):
    """Devuelve las instrucciones de juego según el rol del turno actual.
    Recibe la partida.
    Devuelve un texto con los pasos a seguir.
    """
    if partida.jugador_actual == "defensor":
        return ("TURNO DEL DEFENSOR\n"
                "1) Haz clic en una casilla vacia\n"
                "2) Compra un muro o una torre\n"
                "3) Repite para colocar mas defensas\n"
                "4) Presiona 'Terminar turno'")
    else:
        return ("TURNO DEL ATACANTE\n"
                "1) Haz clic en una casilla vacia\n"
                "2) Compra una unidad\n"
                "3) Seleccionala y muevela con las flechas\n"
                "4) Atacar: 'Seleccionar atacante', luego\n"
                "   'Seleccionar objetivo', luego 'Atacar'\n"
                "5) Presiona 'Iniciar combate' (las torres atacan)\n"
                "6) Presiona 'Terminar turno'")


def mostrar_instrucciones_inicio(partida):
    """Muestra un cartel con las reglas e instrucciones al empezar la partida.
    Recibe la partida.
    No devuelve nada.
    """
    texto = ("Bienvenido a Defensa y Asalto de Base\n\n"
             "OBJETIVO:\n"
             "- El defensor protege la base central con muros y torres.\n"
             "- El atacante destruye la base con sus unidades.\n"
             "- Gana el primero en ganar 3 rondas.\n\n"
             "COMO JUGAR:\n"
             "- Cada jugador juega en su turno.\n"
             "- Defensor: coloca torres y muros, luego termina turno.\n"
             "- Atacante: compra unidades, las mueve y ataca.\n"
             "- Las torres atacan solas al terminar el turno del atacante.\n\n"
             "La guia de cada turno aparece en el panel derecho.")
    messagebox.showinfo("Como jugar", texto)

#____________________

def mostrar_tablero(ventana, partida):
    """Muestra el tablero. La primera vez crea toda la interfaz con frames separados
    (panel izquierdo, tablero central y panel derecho); las siguientes veces solo actualiza
    imágenes y textos, sin recrear (evita el parpadeo).
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    global tablero_iniciado
    tamano = 40

    # La primera vez: crear toda la interfaz
    if not tablero_iniciado:
        limpiar_ventana(ventana)
        ventana.configure(bg="#e8e2d0")  # color de fondo

        ancho = partida.mapa.columnas * tamano + 520
        alto = partida.mapa.filas * tamano + 80
        centrar_ventana(ventana, ancho, alto)

        ventana.imagenes = []
        ventana.imagen_vacia = crear_imagen_vacia(tamano)
        ventana.botones = []

        # Permite que el tablero quede en el centro de la ventana
        ventana.grid_columnconfigure(0, weight=1)
        ventana.grid_columnconfigure(1, weight=0)
        ventana.grid_columnconfigure(2, weight=1)

        # ===== PANEL IZQUIERDO: información =====
        frame_info = tk.Frame(ventana, bg="#e8e2d0")
        frame_info.grid(row=0, column=0, padx=15, pady=10, sticky="n")

        # ----- info de la partida -----
        tk.Label(frame_info, text="Información", font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 8))

        ventana.label_atacante = tk.Label(frame_info, text=f"Dinero atacante: {partida.dinero_atacante}", justify="left", fg="#c82558", bg="#e8e2d0", font=("Arial", 9),wraplength=210)
        ventana.label_atacante.grid(row=1, column=0, sticky="w", pady=4)

        ventana.label_defensor = tk.Label(frame_info, text=f"Dinero defensor: {partida.dinero_defensor}", justify="left", fg="#c82558",bg="#e8e2d0", font=("Arial", 9),wraplength=210)
        ventana.label_defensor.grid(row=2, column=0, sticky="w", pady=4)

        ventana.label_turno = tk.Label(frame_info, text=f"Turno: {partida.turno}", justify="left", fg="#c82558", bg="#e8e2d0",font=("Arial", 9),wraplength=210)
        ventana.label_turno.grid(row=3, column=0, sticky="w", pady=4)

        ventana.label_jugador = tk.Label(frame_info, text=f"Jugador actual: {partida.jugador_actual}", justify="left", fg="#c82558", bg="#e8e2d0",font=("Arial", 9),wraplength=210)
        ventana.label_jugador.grid(row=4, column=0, sticky="w", pady=4)

        ventana.label_rondas_defensor = tk.Label(frame_info, text=f"Rondas defensor: {partida.rondas_defensor}", justify="left", fg="#c82558",bg="#e8e2d0", font=("Arial", 9),wraplength=210)
        ventana.label_rondas_defensor.grid(row=5, column=0, sticky="w", pady=4)

        ventana.label_rondas_atacante = tk.Label(frame_info, text=f"Rondas atacante: {partida.rondas_atacante}", justify="left", fg="#c82558", bg="#e8e2d0",font=("Arial", 9),wraplength=210)
        ventana.label_rondas_atacante.grid(row=6, column=0, sticky="w", pady=4)

        # ----- información de selección -----
        tk.Label(frame_info, text="Selección", font=("Arial", 12, "bold")).grid(row=7, column=0, sticky="w", pady=(18, 8))

        ventana.label_casilla = tk.Label(frame_info, text="Casilla seleccionada: Ninguna", justify="left", fg="#c82558",bg="#e8e2d0", font=("Arial", 9),wraplength=210)
        ventana.label_casilla.grid(row=8, column=0, sticky="w", pady=4)

        ventana.label_objeto = tk.Label(frame_info, text="Objeto seleccionado: Ninguno", justify="left", fg="#c82558", bg="#e8e2d0",font=("Arial", 9),wraplength=210)
        ventana.label_objeto.grid(row=9, column=0, sticky="w", pady=4)

        ventana.label_vida = tk.Label(frame_info, text="Vida: -", justify="left", fg="#c82558",bg="#e8e2d0", font=("Arial", 9),wraplength=210)
        ventana.label_vida.grid(row=10, column=0, sticky="w", pady=4)

        # ----- guía de ayuda según el turno -----
        tk.Label(frame_info, text="Ayuda", font=("Arial", 12, "bold")).grid(row=11, column=0, sticky="w", pady=(18, 8))

        ventana.label_ayuda = tk.Label(frame_info, text=texto_ayuda(partida),justify="left", fg="#c82558",bg="#e8e2d0", font=("Arial", 9),wraplength=210)
        ventana.label_ayuda.grid(row=12, column=0, sticky="w", pady=4)

        # ===== FRAME CENTRAL: tablero =====
        frame_tablero = tk.Frame(ventana)
        frame_tablero.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        for fila in range(partida.mapa.filas):
            fila_botones = []
            for columna in range(partida.mapa.columnas):
                boton = tk.Button(frame_tablero, width=tamano, height=tamano, command=lambda f=fila, c=columna: seleccionar_casilla_y_objeto(ventana, f, c, partida.mapa.matriz[f][c]))
                boton.grid(row=fila, column=columna)
                fila_botones.append(boton)
            ventana.botones.append(fila_botones)

        # ===== PANEL DERECHO: acciones =====
        frame_panel = tk.Frame(ventana, bg="#e8e2d0")
        frame_panel.grid(row=0, column=2, padx=15, pady=10, sticky="n")

        tk.Label(frame_panel, text="Acciones", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 8))

        # ----- frame de compras del atacante -----
        frame_atacante = tk.LabelFrame(frame_panel, text="Atacante", padx=10, pady=10, bg="#ffcccc")
        frame_atacante.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        tk.Button(frame_atacante, text="Comprar Soldado", width=18, command=lambda: comprar_soldado_interfaz(ventana, partida)).grid(row=0, column=0, pady=3)
        tk.Button(frame_atacante, text="Comprar Tanque", width=18, command=lambda: comprar_tanque_interfaz(ventana, partida)).grid(row=1, column=0, pady=3)
        tk.Button(frame_atacante, text="Comprar Unidad Rápida", width=18, command=lambda: comprar_unidad_rapida_interfaz(ventana, partida)).grid(row=2, column=0, pady=3)

        # ----- frame de compras del defensor -----
        frame_defensor = tk.LabelFrame(frame_panel, text="Defensor", padx=10, pady=10, bg="#ffcccc")
        frame_defensor.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        tk.Button(frame_defensor, text="Comprar Muro", width=18, command=lambda: comprar_muro_interfaz(ventana, partida)).grid(row=0, column=0, pady=3)
        tk.Button(frame_defensor, text="Comprar Torre Básica", width=18, command=lambda: comprar_torre_basica_interfaz(ventana, partida)).grid(row=1, column=0, pady=3)
        tk.Button(frame_defensor, text="Comprar Torre Pesada", width=18, command=lambda: comprar_torre_pesada_interfaz(ventana, partida)).grid(row=2, column=0, pady=3)
        tk.Button(frame_defensor, text="Comprar Torre Mágica", width=18, command=lambda: comprar_torre_magica_interfaz(ventana, partida)).grid(row=3, column=0, pady=3)

        # ----- frame de movimiento (cruz) -----
        frame_flechas = tk.LabelFrame(frame_panel, text="Mover", padx=10, pady=10, bg="#ffcccc")
        frame_flechas.grid(row=2, column=0, columnspan=2, pady=15)

        tk.Button(frame_flechas, text="↑", width=4, command=lambda: mover_arriba_interfaz(ventana, partida)).grid(row=0, column=1)
        tk.Button(frame_flechas, text="←", width=4, command=lambda: mover_izquierda_interfaz(ventana, partida)).grid(row=1, column=0)
        tk.Button(frame_flechas, text="↓", width=4, command=lambda: mover_abajo_interfaz(ventana, partida)).grid(row=1, column=1)
        tk.Button(frame_flechas, text="→", width=4, command=lambda: mover_derecha_interfaz(ventana, partida)).grid(row=1, column=2)

        # Botón para seleccionar atacante
        boton_seleccionar_atacante = tk.Button(frame_panel, text="Seleccionar atacante", width=20, bg="#ffcccc", command=lambda: seleccionar_atacante(ventana))
        boton_seleccionar_atacante.grid(row=3, column=0, columnspan=2, pady=5)

        # Botón para seleccionar objetivo
        boton_seleccionar_objetivo = tk.Button(frame_panel, text="Seleccionar objetivo", width=20, bg="#ffcccc", command=lambda: seleccionar_objetivo(ventana))
        boton_seleccionar_objetivo.grid(row=4, column=0, columnspan=2, pady=5)

        # boton para atacar
        boton_atacar = tk.Button(frame_panel, text="Atacar", width=20, bg="#ffcccc", command=lambda: atacar_interfaz(ventana, partida))
        boton_atacar.grid(row=5, column=0, columnspan=2, pady=5)

        # boton para activar habilidad
        boton_habilidad = tk.Button(frame_panel, text="Activar habilidad", width=20, bg="#ffcccc", command=lambda: activar_habilidad_interfaz(ventana, partida))
        boton_habilidad.grid(row=6, column=0, columnspan=2, pady=5)

        # botón para iniciar la fase de combate (las torres atacan)
        boton_combate = tk.Button(frame_panel, text="Iniciar combate", width=20, bg="#ffcccc", command=lambda: iniciar_combate_interfaz(ventana, partida))
        boton_combate.grid(row=7, column=0, columnspan=2, pady=5)

        # ----- botón terminar turno -----
        tk.Button(frame_panel, text="Terminar turno", width=20, bg="#ffcccc", command=lambda: terminar_turno_interfaz(ventana, partida)).grid(row=8, column=0, columnspan=2, pady=15)

        # botón para regresar al menú durante la partida
        tk.Button(frame_panel, text="← Regresar al menú", width=20, bg="#ffcccc", command=lambda: regresar_al_menu(ventana, partida)).grid(row=9, column=0, columnspan=2, pady=5)

        tablero_iniciado = True

        # muestra las instrucciones de juego al empezar la partida
        mostrar_instrucciones_inicio(partida)

    # Siempre: actualizar imágenes de casillas y textos del panel
    actualizar_casillas(ventana, partida, tamano)
    actualizar_info(ventana, partida)

def actualizar_casillas(ventana, partida, tamano):
    """Actualiza solo las imágenes de las casillas, sin recrear los botones.
    Recibe la ventana, la partida y el tamaño de casilla.
    No devuelve nada.
    """
    ventana.imagenes = []
    for fila in range(partida.mapa.filas):
        for columna in range(partida.mapa.columnas):
            contenido = partida.mapa.matriz[fila][columna]

            if contenido is None:
                imagen = ventana.imagen_vacia
            else:
                ruta = obtener_imagen(contenido, partida)
                imagen = cargar_imagen(ruta, tamano)
                ventana.imagenes.append(imagen)

            ventana.botones[fila][columna].config(image=imagen)

def actualizar_info(ventana, partida):
    """Actualiza los textos del panel (dinero, turno, rondas) sin recrearlos.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    ventana.label_atacante.config(text=f"Dinero atacante: {partida.dinero_atacante}")
    ventana.label_defensor.config(text=f"Dinero defensor: {partida.dinero_defensor}")
    ventana.label_turno.config(text=f"Turno: {partida.turno}")
    ventana.label_jugador.config(text=f"Jugador actual: {partida.jugador_actual}")
    ventana.label_rondas_defensor.config(text=f"Rondas defensor: {partida.rondas_defensor}")
    ventana.label_rondas_atacante.config(text=f"Rondas atacante: {partida.rondas_atacante}")
    
    # Actualiza la casilla seleccionada
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        texto_casilla = "Casilla seleccionada: Ninguna"
    else:
        texto_casilla = f"Casilla seleccionada: ({ventana.fila_seleccionada}, {ventana.columna_seleccionada})"

    ventana.label_casilla.config(text=texto_casilla)

    # Actualiza el objeto seleccionado
    if ventana.objeto_seleccionado is None:
        texto_objeto = "Objeto seleccionado: Ninguno"
    elif isinstance(ventana.objeto_seleccionado, Base):
        texto_objeto = "Objeto seleccionado: Base"
    elif isinstance(ventana.objeto_seleccionado, Muro):
        texto_objeto = "Objeto seleccionado: Muro"
    else:
        texto_objeto = f"Objeto seleccionado: {ventana.objeto_seleccionado.nombre}"

    ventana.label_objeto.config(text=texto_objeto)

    # Actualiza la guía de ayuda según el turno actual
    ventana.label_ayuda.config(text=texto_ayuda(partida))

def mostrar_ganador(ventana, partida):
    """Muestra la pantalla de fin de partida con el ganador.
    Actualiza las victorias del ganador y muestra quién ganó.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    limpiar_ventana(ventana)
    

    partida.actualizar_victorias()

    ganador = partida.obtener_ganador()

    # obtener el nombre de usuario del jugador ganador según su rol
    if ganador == "defensor":
        nombre_ganador = partida.jugador_defensor.usuario
    else:
        nombre_ganador = partida.jugador_atacante.usuario

    titulo = tk.Label(ventana, text="FIN DE LA PARTIDA", font=("Arial", 24))
    titulo.pack(pady=20)

    mensaje = tk.Label(ventana, text=f"¡Ganó {nombre_ganador} ({ganador})!", font=("Arial", 18))
    mensaje.pack(pady=10)

    boton_menu = tk.Button(ventana, text="Regresar al menú", command=lambda: regresar_al_menu(ventana, partida))
    boton_menu.pack(pady=20)


def regresar_al_menu(ventana, partida):
    """Vuelve al menú principal desde la pantalla de fin de partida.
    Reinicia el tablero para que una próxima partida se dibuje desde cero.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    global tablero_iniciado
    # permite que el tablero se reconstruya en la próxima partida
    tablero_iniciado = False

    # arranca una partida nueva con los mismos jugadores al elegir "Iniciar juego"
    from interfaz_menu import mostrar_menu_principal
    from interfaz_facciones import elegir_faccion_defensor
    from partida import Partida

    jugador_defensor = partida.jugador_defensor
    jugador_atacante = partida.jugador_atacante

    def arrancar_partida_nueva():
        global tablero_iniciado
        tablero_iniciado = False
        nueva = Partida(jugador_defensor, jugador_atacante)
        ventana.fila_seleccionada = None
        ventana.columna_seleccionada = None
        ventana.objeto_seleccionado = None
        ventana.atacante_seleccionado = None
        ventana.objetivo_seleccionado = None
        elegir_faccion_defensor(ventana, nueva)

    mostrar_menu_principal(ventana, arrancar_partida_nueva)

def revisar_fin_de_ronda(ventana, partida):
    """Revisa el estado de la partida y la ronda.
    Si alguien ganó la partida (3 rondas), muestra la pantalla final.
    Si terminó la ronda, registra el punto, avisa quién ganó y reinicia para la siguiente.
    Si no terminó, sigue el juego normal.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.ronda_termino():
        gano_atac = partida.gano_atacante()

        partida.registrar_ronda()

        ganador = partida.obtener_ganador()
        if ganador is not None:
            mostrar_ganador(ventana, partida)
            return

        if gano_atac:
            messagebox.showinfo("Fin de ronda", "¡El atacante destruyó la base y ganó la ronda!")
        else:
            messagebox.showinfo("Fin de ronda", "¡El defensor resistió y ganó la ronda!")

        partida.reiniciar_ronda()

        ventana.fila_seleccionada = None
        ventana.columna_seleccionada = None
        ventana.objeto_seleccionado = None
        ventana.atacante_seleccionado = None
        ventana.objetivo_seleccionado = None

    mostrar_tablero(ventana, partida)