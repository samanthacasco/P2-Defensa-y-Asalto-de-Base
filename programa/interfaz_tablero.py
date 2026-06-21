import tkinter as tk
from tkinter import messagebox
from utilidades import centrar_ventana, limpiar_ventana, cargar_imagen, crear_imagen_vacia
from modelo import (Base, Muro, Torre, Unidad, TorreBasica, TorrePesada, TorreMagica,
                    Soldado, Tanque, UnidadRapida)
from economia import comprar_unidad, comprar_torre, comprar_muro
from combate import atacar, esta_al_alcance
from habilidades import ataque_doble, disparo_doble, danio_aumentado, congelar


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
    if ventana.objeto_seleccionado is not None:
        partida.mapa.mover_arriba(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


def mover_abajo_interfaz(ventana, partida):
    """Mueve hacia abajo la unidad seleccionada"""
    if ventana.objeto_seleccionado is not None:
        partida.mapa.mover_abajo(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


def mover_izquierda_interfaz(ventana, partida):
    """Mueve hacia la izquierda la unidad seleccionada"""
    if ventana.objeto_seleccionado is not None:
        partida.mapa.mover_izquierda(ventana.objeto_seleccionado)
        mostrar_tablero(ventana, partida)


def mover_derecha_interfaz(ventana, partida):
    """Mueve hacia la derecha la unidad seleccionada"""
    if ventana.objeto_seleccionado is not None:
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
    """Termina el turno. Si termina el atacante, las torres atacan automáticamente.
    Luego se pasa al siguiente jugador y se revisa el fin de ronda.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    if partida.jugador_actual == "atacante":
        combate_automatico(partida)

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
    Devuelve True si el ataque se realizó o False en caso contrario.
    """

    # Si el atacante es un soldado, usa su habilidad de ataque doble
    if isinstance(atacante, Soldado):
        return ataque_doble(atacante, objetivo, mapa)

    # Si el atacante es una torre básica, usa disparo doble
    elif isinstance(atacante, TorreBasica):
        return disparo_doble(atacante, objetivo, mapa)

    # Si el atacante es una torre pesada, usa daño aumentado
    elif isinstance(atacante, TorrePesada):
        return danio_aumentado(atacante, objetivo, mapa)

    # Si el atacante es una torre mágica, usa congelar
    elif isinstance(atacante, TorreMagica):
        return congelar(atacante, objetivo, mapa)

    # Si no tiene una habilidad de ataque especial, ataca normal
    return atacar(atacante, objetivo, mapa)


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
    ataque_exitoso = ejecutar_ataque_con_habilidad(ventana.atacante_seleccionado,ventana.objetivo_seleccionado,partida.mapa)

    # Si el objetivo no estaba al alcance, muestra un mensaje
    if not ataque_exitoso:
        messagebox.showerror("Ataque fallido", "El objetivo no está al alcance o el ataque no se pudo realizar." )
        return

    # Calcula la vida después del ataque
    vida_despues = ventana.objetivo_seleccionado.vida

    # Calcula cuánto daño se realizó
    dano_realizado = vida_antes - vida_despues

    # Si el objetivo fue destruido
    if ventana.objetivo_seleccionado.esta_destruida():
        messagebox.showinfo( "Objetivo destruido", f"El ataque realizó {dano_realizado} de daño y el objetivo fue destruido.")
    else:
        messagebox.showinfo("Ataque realizado",f"Daño realizado: {dano_realizado}\nVida restante: {vida_despues}")

    # Actualiza el tablero y la información visual
    revisar_fin_de_ronda(ventana, partida)

def combate_automatico(partida):
    """Todas las torres atacan automáticamente a las unidades en su alcance.
    Recibe la partida.
    No devuelve nada.
    """
    # cada torre ataca a una unidad que tenga en su alcance
    for torre in list(partida.mapa.torres):
        for unidad in list(partida.mapa.unidades):
            if esta_al_alcance(torre, unidad):
                atacar(torre, unidad, partida.mapa)
                break   # cada torre ataca a una sola unidad por turno
            
#____________________

def mostrar_tablero(ventana, partida):
    """Muestra el tablero. La primera vez crea toda la interfaz con frames separados
    (uno para el tablero y otro para el panel); las siguientes veces solo actualiza
    imágenes y textos, sin recrear (evita el parpadeo).
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    global tablero_iniciado
    tamano = 40

    # La primera vez: crear toda la interfaz
    if not tablero_iniciado:
        limpiar_ventana(ventana)

        ancho = partida.mapa.columnas * tamano + 500
        alto = partida.mapa.filas * tamano + 150
        centrar_ventana(ventana, ancho, alto)

        ventana.imagenes = []
        ventana.imagen_vacia = crear_imagen_vacia(tamano)
        ventana.botones = []

        # ===== FRAME DEL TABLERO (izquierda) =====
        frame_tablero = tk.Frame(ventana)
        frame_tablero.grid(row=0, column=0, padx=10, pady=10, sticky="n")

        for fila in range(partida.mapa.filas):
            fila_botones = []
            for columna in range(partida.mapa.columnas):
                boton = tk.Button(frame_tablero, width=tamano, height=tamano,
                                  command=lambda f=fila, c=columna: seleccionar_casilla_y_objeto(ventana, f, c, partida.mapa.matriz[f][c]))
                boton.grid(row=fila, column=columna)
                fila_botones.append(boton)
            ventana.botones.append(fila_botones)

        # ===== FRAME DEL PANEL (derecha) =====
        frame_panel = tk.Frame(ventana)
        frame_panel.grid(row=0, column=1, padx=20, pady=10, sticky="n")

        # ----- info de la partida -----
        ventana.label_atacante = tk.Label(frame_panel, text=f"Dinero atacante: {partida.dinero_atacante}")
        ventana.label_atacante.grid(row=0, column=0, padx=10, pady=4)

        ventana.label_defensor = tk.Label(frame_panel, text=f"Dinero defensor: {partida.dinero_defensor}")
        ventana.label_defensor.grid(row=0, column=1, padx=10, pady=4)

        ventana.label_turno = tk.Label(frame_panel, text=f"Turno: {partida.turno}")
        ventana.label_turno.grid(row=1, column=0, padx=10, pady=4)

        ventana.label_jugador = tk.Label(frame_panel, text=f"Jugador actual: {partida.jugador_actual}")
        ventana.label_jugador.grid(row=1, column=1, padx=10, pady=4)

        ventana.label_rondas_defensor = tk.Label(frame_panel, text=f"Rondas defensor: {partida.rondas_defensor}")
        ventana.label_rondas_defensor.grid(row=2, column=0, padx=10, pady=4)

        ventana.label_rondas_atacante = tk.Label(frame_panel, text=f"Rondas atacante: {partida.rondas_atacante}")
        ventana.label_rondas_atacante.grid(row=2, column=1, padx=10, pady=4)

        # ----- información de selección -----
        ventana.label_casilla = tk.Label(frame_panel,text="Casilla seleccionada: Ninguna")
        ventana.label_casilla.grid(row=6, column=0, columnspan=2, pady=4)

        ventana.label_objeto = tk.Label(frame_panel,text="Objeto seleccionado: Ninguno")
        ventana.label_objeto.grid(row=7, column=0, columnspan=2, pady=4)

        # Muestra la vida del objeto seleccionado
        ventana.label_vida = tk.Label(frame_panel, text="Vida: -")
        ventana.label_vida.grid(row=8, column=0, columnspan=2, pady=4)

        # ----- frame de compras del atacante -----
        frame_atacante = tk.LabelFrame(frame_panel, text="Atacante", padx=10, pady=10)
        frame_atacante.grid(row=3, column=0, padx=10, pady=10, sticky="n")

        tk.Button(frame_atacante, text="Comprar Soldado", width=18, command=lambda: comprar_soldado_interfaz(ventana, partida)).grid(row=0, column=0, pady=3)
        tk.Button(frame_atacante, text="Comprar Tanque", width=18, command=lambda: comprar_tanque_interfaz(ventana, partida)).grid(row=1, column=0, pady=3)
        tk.Button(frame_atacante, text="Comprar Unidad Rápida", width=18, command=lambda: comprar_unidad_rapida_interfaz(ventana, partida)).grid(row=2, column=0, pady=3)

        # ----- frame de compras del defensor -----
        frame_defensor = tk.LabelFrame(frame_panel, text="Defensor", padx=10, pady=10)
        frame_defensor.grid(row=3, column=1, padx=10, pady=10, sticky="n")

        tk.Button(frame_defensor, text="Comprar Muro", width=18, command=lambda: comprar_muro_interfaz(ventana, partida)).grid(row=0, column=0, pady=3)
        tk.Button(frame_defensor, text="Comprar Torre Básica", width=18, command=lambda: comprar_torre_basica_interfaz(ventana, partida)).grid(row=1, column=0, pady=3)
        tk.Button(frame_defensor, text="Comprar Torre Pesada", width=18, command=lambda: comprar_torre_pesada_interfaz(ventana, partida)).grid(row=2, column=0, pady=3)
        tk.Button(frame_defensor, text="Comprar Torre Mágica", width=18, command=lambda: comprar_torre_magica_interfaz(ventana, partida)).grid(row=3, column=0, pady=3)

        # ----- frame de movimiento (cruz) -----
        frame_flechas = tk.LabelFrame(frame_panel, text="Mover", padx=10, pady=10)
        frame_flechas.grid(row=4, column=0, columnspan=2, pady=15)

        tk.Button(frame_flechas, text="↑", width=4, command=lambda: mover_arriba_interfaz(ventana, partida)).grid(row=0, column=1)
        tk.Button(frame_flechas, text="←", width=4, command=lambda: mover_izquierda_interfaz(ventana, partida)).grid(row=1, column=0)
        tk.Button(frame_flechas, text="↓", width=4, command=lambda: mover_abajo_interfaz(ventana, partida)).grid(row=1, column=1)
        tk.Button(frame_flechas, text="→", width=4, command=lambda: mover_derecha_interfaz(ventana, partida)).grid(row=1, column=2)

        # Botón para seleccionar atacante
        boton_seleccionar_atacante = tk.Button(frame_panel,text="Seleccionar atacante",width=20,command=lambda: seleccionar_atacante(ventana))
        boton_seleccionar_atacante.grid(row=9, column=0, columnspan=2, pady=5)

        # Botón para seleccionar objetivo
        boton_seleccionar_objetivo = tk.Button( frame_panel,text="Seleccionar objetivo",width=20, command=lambda: seleccionar_objetivo(ventana))
        boton_seleccionar_objetivo.grid(row=10, column=0, columnspan=2, pady=5)
        
        # boton para atacar
        boton_atacar = tk.Button(frame_panel,text="Atacar",width=20,command=lambda: atacar_interfaz(ventana, partida))
        boton_atacar.grid(row=11, column=0, columnspan=2, pady=5)
        
        # ----- botón terminar turno -----
        tk.Button(frame_panel, text="Terminar turno", width=20, command=lambda: terminar_turno_interfaz(ventana, partida)).grid(row=12, column=0, columnspan=2, pady=15)

        tablero_iniciado = True

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

    boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    boton_salir.pack(pady=20)

def revisar_fin_de_ronda(ventana, partida):
    """Revisa si terminó la ronda y, si hay un ganador de la partida, muestra la pantalla final.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    partida.registrar_ronda()
    ganador = partida.obtener_ganador()

    if ganador is not None:
        mostrar_ganador(ventana, partida)
    else:
        mostrar_tablero(ventana, partida)

