import tkinter as tk
from utilidades import centrar_ventana, limpiar_ventana, cargar_imagen, crear_imagen_vacia
from modelo import (Base, Muro, Torre, Unidad, TorreBasica, TorrePesada, TorreMagica,
                    Soldado, Tanque, UnidadRapida)
from economia import comprar_unidad, comprar_torre, comprar_muro

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

    # Guarda el objeto seleccionado dentro de la ventana
    ventana.objeto_seleccionado = objeto


def mover_arriba_interfaz(ventana, partida):
    """Mueve hacia arriba la unidad seleccionada
    Recibe la ventana y la partida
    No devuelve nada
    """

    # Verifica que haya un objeto seleccionado
    if ventana.objeto_seleccionado is not None:

        # Mueve la unidad usando la lógica del mapa
        partida.mapa.mover_arriba(ventana.objeto_seleccionado)
        # Vuelve a dibujar el tablero actualizado
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

#-------------
def comprar_soldado_interfaz(ventana, partida):
    """Compra un soldado y lo coloca en la casilla seleccionada
    Recibe la ventana y la partida
    No devuelve nada
    """
    # Verifica que el jugador haya seleccionado una casilla
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        print("Primero selecciona una casilla")
        return

    # Crea un soldado
    soldado = Soldado()

    # Intenta comprarlo y colocarlo en la posición (0, 0)
    compra_exitosa = comprar_unidad(partida, soldado, ventana.fila_seleccionada, ventana.columna_seleccionada, "atacante")

    # Si se pudo comprar, se vuelve a dibujar el tablero actualizado
    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
         print("No se pudo comprar")

def comprar_tanque_interfaz(ventana, partida):
    """Compra un tanque y lo coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """

    # Verifica que el jugador haya seleccionado una casilla
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        print("Primero selecciona una casilla")
        return

    # Crea un tanque
    tanque = Tanque()

    # Intenta comprarlo y colocarlo en la casilla seleccionada
    compra_exitosa = comprar_unidad(
        partida,
        tanque,
        ventana.fila_seleccionada,
        ventana.columna_seleccionada,
        "atacante"
    )

    # Si se pudo comprar, redibuja el tablero
    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        print("No se pudo comprar el tanque")

def comprar_unidad_rapida_interfaz(ventana, partida):
    """Compra una unidad rápida y la coloca en la casilla seleccionada.
    Recibe la ventana y la partida.
    No devuelve nada.
    """

    # Verifica que el jugador haya seleccionado una casilla
    if ventana.fila_seleccionada is None or ventana.columna_seleccionada is None:
        print("Primero selecciona una casilla")
        return

    # Crea una unidad rápida
    unidad_rapida = UnidadRapida()

    # Intenta comprarla y colocarla en la casilla seleccionada
    compra_exitosa = comprar_unidad(
        partida,
        unidad_rapida,
        ventana.fila_seleccionada,
        ventana.columna_seleccionada,
        "atacante"
    )

    # Si se pudo comprar, redibuja el tablero
    if compra_exitosa:
        mostrar_tablero(ventana, partida)
    else:
        print("No se pudo comprar la unidad rápida")


def seleccionar_casilla(ventana, fila, columna):
    """Guarda la posición de una casilla seleccionada.

    Recibe la ventana y las coordenadas de la casilla.
    No devuelve nada.
    """

    # Guarda la fila seleccionada
    ventana.fila_seleccionada = fila

    # Guarda la columna seleccionada
    ventana.columna_seleccionada = columna

    print(f"Casilla seleccionada: ({fila}, {columna})")

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

    print(f"Casilla seleccionada: ({fila}, {columna})")

def terminar_turno_interfaz(ventana, partida):
    """Termina el turno actual y pasa al siguiente jugador.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    partida.cambiar_turno()      
    mostrar_tablero(ventana, partida)  
    
def mostrar_tablero(ventana, partida):
    global tablero_iniciado
    limpiar_ventana(ventana)
    
    tamano = 40

    if not tablero_iniciado:
        ancho = partida.mapa.columnas * tamano + 450
        alto = partida.mapa.filas * tamano + 120
        centrar_ventana(ventana, ancho, alto)
        tablero_iniciado = True
    
    ventana.imagenes = []
    ventana.imagen_vacia = crear_imagen_vacia(tamano)
    
    # mostrar dinero del defensor
    label_defensor = tk.Label(ventana, text=f"Dinero defensor: {partida.dinero_defensor}")
    label_defensor.grid(row=0, column=22, padx=15)

    # mostrar dinero del atacante
    label_atacante = tk.Label(ventana, text=f"Dinero atacante: {partida.dinero_atacante}")
    label_atacante.grid(row=1, column=22, padx=15)

    # mostrar turno actual
    label_turno = tk.Label(ventana, text=f"Turno: {partida.turno}")
    label_turno.grid(row=2, column=22, padx=15)

    # mostrar jugador actual
    label_jugador = tk.Label(ventana, text=f"Jugador actual: {partida.jugador_actual}")
    label_jugador.grid(row=3, column=22, padx=15)

    # mostrar marcador de rondas, defensor
    label_rondas_defensor = tk.Label(ventana, text=f"Rondas defensor: {partida.rondas_defensor}")
    label_rondas_defensor.grid(row=4, column=22, padx=15)

    # mostrar marcador de rondas, atacante
    label_rondas_atacante = tk.Label(ventana, text=f"Rondas atacante: {partida.rondas_atacante}")
    label_rondas_atacante.grid(row=5, column=22, padx=15)

    # botón para mover hacia arriba
    boton_arriba = tk.Button(ventana, text="↑", command=lambda: mover_arriba_interfaz(ventana, partida))
    boton_arriba.grid(row=7, column=22)

    # botón para mover hacia la izquierda
    boton_izquierda = tk.Button(ventana,text="←",command=lambda: mover_izquierda_interfaz(ventana, partida))
    boton_izquierda.grid(row=8, column=21)

    # botón para mover hacia la derecha
    boton_derecha = tk.Button(ventana, text="→", command=lambda: mover_derecha_interfaz(ventana, partida))
    boton_derecha.grid(row=8, column=24)

    # btón para mover hacia abajo
    boton_abajo = tk.Button(ventana, text="↓", command=lambda: mover_abajo_interfaz(ventana, partida))
    boton_abajo.grid(row=9, column=22)

    # boton para comprar soldado 
    boton_comprar_soldado = tk.Button(ventana, text="Comprar Soldado", command=lambda: comprar_soldado_interfaz(ventana, partida))
    boton_comprar_soldado.grid(row=11, column=22, padx=15, pady=5)

    # boton para comprar tanque
    boton_comprar_tanque = tk.Button(ventana,text="Comprar Tanque",command=lambda: comprar_tanque_interfaz(ventana, partida))
    boton_comprar_tanque.grid(row=12, column=22, padx=15, pady=5)

    # boton para comprar unidad rápida
    boton_comprar_unidad_rapida = tk.Button(ventana,text="Comprar Unidad Rápida",command=lambda: comprar_unidad_rapida_interfaz(ventana, partida))
    boton_comprar_unidad_rapida.grid(row=13, column=22, padx=15, pady=5)

    
    boton_terminar_turno = tk.Button(ventana, text="Terminar turno", command=lambda: terminar_turno_interfaz(ventana, partida))
    boton_terminar_turno.grid(row=14, column=22, padx=15, pady=5)
    
    for fila in range(partida.mapa.filas):
        for columna in range(partida.mapa.columnas):
            contenido = partida.mapa.matriz[fila][columna]

            if contenido is None:
                imagen = ventana.imagen_vacia
            else:
                ruta = obtener_imagen(contenido, partida)
                imagen = cargar_imagen(ruta, tamano)        
                ventana.imagenes.append(imagen)

            boton = tk.Button(ventana, image=imagen, width=tamano, height=tamano, command=lambda f=fila, c=columna, o=contenido: seleccionar_casilla_y_objeto(ventana, f, c, o)) 
            boton.grid(row=fila, column=columna)

def mostrar_ganador(ventana, partida):
    """Muestra la pantalla de fin de partida con el ganador.
    Actualiza las victorias del ganador y muestra quién ganó.
    Recibe la ventana y la partida.
    No devuelve nada.
    """
    limpiar_ventana(ventana)

    partida.actualizar_victorias()

    ganador = partida.obtener_ganador()

    titulo = tk.Label(ventana, text="FIN DE LA PARTIDA", font=("Arial", 24))
    titulo.pack(pady=20)

    mensaje = tk.Label(ventana, text=f"¡Ganó el {ganador}!", font=("Arial", 18))
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
