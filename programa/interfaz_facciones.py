from modelo import Medieval, Futurista, Naturaleza
from utilidades import limpiar_ventana
import tkinter as tk

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
    titulo.pack()

    boton_medieval = tk.Button(ventana, text="Medieval",
                               command=lambda: elegir_defensor(Medieval()))
    boton_medieval.pack()

    boton_futurista = tk.Button(ventana, text="Futurista",
                                command=lambda: elegir_defensor(Futurista()))
    boton_futurista.pack()

    boton_naturaleza = tk.Button(ventana, text="Naturaleza",
                                 command=lambda: elegir_defensor(Naturaleza()))
    boton_naturaleza.pack()

def elegir_faccion_atacante(ventana, partida):
    """Muestra la pantalla para que el atacante elija su facción.
    Recibe la ventana y la partida. Guarda la facción elegida en la partida.
    """
    def elegir_atacante(faccion):
        partida.faccion_atacante = faccion
    
    limpiar_ventana(ventana)

    titulo = tk.Label(ventana, text="Atacante, elige tu facción")
    titulo.pack()

    facciones = [Medieval(), Futurista(), Naturaleza()]
    
    for faccion in facciones:
        if faccion.nombre != partida.faccion_defensor.nombre:
            boton = tk.Button(ventana, text=faccion.nombre,
                              command=lambda f=faccion: elegir_atacante(f))
            boton.pack()
