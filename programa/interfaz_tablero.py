import tkinter as tk
from tkinter import messagebox
from utilidades import centrar_ventana, limpiar_ventana
from jugador import login, registrar
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

    # Casilla seleccionada para colocar objetos en el tablero
    ventana.fila_seleccionada = None
    ventana.columna_seleccionada = None

    # Objeto seleccionado para mover unidades
    ventana.objeto_seleccionado = None

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
            login_atacante(resultado)

    def intentar_registrar():
        resultado = registrar(entry_usuario.get(), entry_clave.get())
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado, ahora puede iniciar sesión")
        else:
            messagebox.showinfo("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Iniciar sesión", command=intentar).pack()
    tk.Button(ventana, text="Registrarse", command=intentar_registrar).pack()


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

    def intentar_registrar():
        resultado = registrar(entry_usuario.get(), entry_clave.get())
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado, ahora puede iniciar sesión")
        else:
            messagebox.showinfo("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Iniciar sesión", command=intentar).pack()
    tk.Button(ventana, text="Registrarse", command=intentar_registrar).pack()


def crear_partida(jugador_defensor, jugador_atacante):
    """Crea la partida con los dos jugadores y pasa a elegir facciones."""
    global partida
    partida = Partida(jugador_defensor, jugador_atacante)
    elegir_faccion_defensor(ventana, partida)


iniciar_juego()
