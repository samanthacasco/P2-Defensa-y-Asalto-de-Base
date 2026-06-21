from modelo import Medieval, Futurista, Naturaleza
from utilidades import limpiar_ventana
import tkinter as tk
from interfaz_tablero import mostrar_tablero 

def elegir_faccion_defensor(ventana, partida):
    """Muestra la pantalla para que el defensor elija su facción.
    Recibe la ventana y la partida. Guarda la facción elegida en la partida
    y avanza a la pantalla de selección del atacante.
    """
    def elegir_defensor(faccion):
        partida.faccion_defensor = faccion
        elegir_faccion_atacante(ventana, partida)

    limpiar_ventana(ventana)

    titulo = tk.Label(ventana, text="Defensor, elige tu facción")
    titulo.pack(pady=15)

    boton_medieval = tk.Button(ventana, text="Medieval", width=15, bg="#ffcccc",command=lambda: elegir_defensor(Medieval()))
    boton_medieval.pack(pady=6)

    boton_futurista = tk.Button(ventana, text="Futurista", width=15, bg="#ffcccc",command=lambda: elegir_defensor(Futurista()))
    boton_futurista.pack(pady=6)

    boton_naturaleza = tk.Button(ventana, text="Naturaleza", width=15, bg="#ffcccc",command=lambda: elegir_defensor(Naturaleza()))
    boton_naturaleza.pack(pady=6)

def elegir_faccion_atacante(ventana, partida):
    """Muestra la pantalla para que el atacante elija su facción.
    Recibe la ventana y la partida. Guarda la facción elegida en la partida.
    """
    def elegir_atacante(faccion):
        partida.faccion_atacante = faccion
        mostrar_tablero(ventana, partida)
    
    limpiar_ventana(ventana)

    titulo = tk.Label(ventana, text="Atacante, elige tu facción")
    titulo.pack(pady=15)

    facciones = [Medieval(), Futurista(), Naturaleza()]
    
    for faccion in facciones:
        if faccion.nombre != partida.faccion_defensor.nombre:
            boton = tk.Button(ventana, text=faccion.nombre, width=15, bg="#ffcccc",command=lambda f=faccion: elegir_atacante(f))
            boton.pack(pady=6)
