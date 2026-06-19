import tkinter as tk
from utilidades import limpiar_ventana
from modelo import (Base, Muro, Torre, Unidad,TorreBasica, TorrePesada, TorreMagica,
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
    
    ventana.imagenes = []

    for fila in range(partida.mapa.filas):
        for columna in range(partida.mapa.columnas):
            contenido = partida.mapa.matriz[fila][columna]

            if contenido is None:
                boton = tk.Button(ventana, width=2, height=1)
            else:
                ruta = obtener_imagen(contenido, partida)
                imagen = tk.PhotoImage(file=ruta)
                ventana.imagenes.append(imagen)
                boton = tk.Button(ventana, image=imagen, width=40, height=40)
                
            boton.grid(row=fila, column=columna)
