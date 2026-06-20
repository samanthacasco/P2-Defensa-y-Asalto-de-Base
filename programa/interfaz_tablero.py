import tkinter as tk
from utilidades import centrar_ventana, limpiar_ventana, cargar_imagen, crear_imagen_vacia
from modelo import (Base, Muro, Torre, Unidad, TorreBasica, TorrePesada, TorreMagica,
                    Soldado, Tanque, UnidadRapida)

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

def mostrar_tablero(ventana, partida):
    limpiar_ventana(ventana)
    
    tamano = 50
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

    for fila in range(partida.mapa.filas):
        for columna in range(partida.mapa.columnas):
            contenido = partida.mapa.matriz[fila][columna]

            if contenido is None:
                imagen = ventana.imagen_vacia
            else:
                ruta = obtener_imagen(contenido, partida)
                imagen = cargar_imagen(ruta, tamano)        
                ventana.imagenes.append(imagen)

            boton = tk.Button(ventana, image=imagen, width=tamano, height=tamano)  
            boton.grid(row=fila, column=columna)
