import tkinter as tk
from tkinter import messagebox
from utilidades import centrar_ventana, limpiar_ventana
from jugador import login
from partida import Partida
from interfaz_facciones import elegir_faccion_defensor
from interfaz_tablero import mostrar_tablero

# variables globales que comparten todas las pantallas
ventana = None
partida = None

def iniciar_juego():
    """Arranca el juego: crea la ventana y muestra el login del defensor."""
    global ventana
    ventana = tk.Tk()
    ventana.title("Defensa y Asalto de Base")
    centrar_ventana(ventana, 400, 300)
    login_defensor()
    ventana.mainloop()

def login_defensor():
    """Pantalla de login del defensor."""
    limpiar_ventana(ventana)

    tk.Label(ventana, text="LOGIN DEFENSOR").pack()
    tk.Label(ventana, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()
    tk.Label(ventana, text="Contraseña:").pack()
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.pack()

    def intentar():
        resultado = login(entry_usuario.get(), entry_clave.get())
        if resultado is None:
            messagebox.showinfo("Error", "Usuario o clave incorrecta")
        else:
            global jugador_defensor
            jugador_defensor = resultado
            login_atacante(jugador_defensor)

    tk.Button(ventana, text="Entrar", command=intentar).pack()

def login_atacante(jugador_defensor):
    """Pantalla de login del atacante. Recibe el jugador defensor ya logueado."""
    limpiar_ventana(ventana)

    tk.Label(ventana, text="LOGIN ATACANTE").pack()
    tk.Label(ventana, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()
    tk.Label(ventana, text="Contraseña:").pack()
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.pack()

    def intentar():
        resultado = login(entry_usuario.get(), entry_clave.get())
        if resultado is None:
            messagebox.showinfo("Error", "Usuario o clave incorrecta")
        elif resultado.usuario == jugador_defensor.usuario:
            messagebox.showinfo("Error", "Ese jugador ya entró como defensor")
        else:
            crear_partida(jugador_defensor, resultado)

    tk.Button(ventana, text="Entrar", command=intentar).pack()

def crear_partida(jugador_defensor, jugador_atacante):
    """Crea la partida con los dos jugadores y pasa a elegir facciones."""
    global partida
    partida = Partida(jugador_defensor, jugador_atacante)
    elegir_faccion_defensor(ventana, partida)


iniciar_juego()
