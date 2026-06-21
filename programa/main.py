import tkinter as tk
from tkinter import messagebox
from utilidades import centrar_ventana, limpiar_ventana
from jugador import login, registrar
from partida import Partida
from interfaz_facciones import elegir_faccion_defensor
from interfaz_tablero import mostrar_tablero
from interfaz_menu import mostrar_menu_principal

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

    # Objeto que realizará el ataque
    ventana.atacante_seleccionado = None

    # Objeto que recibirá el ataque
    ventana.objetivo_seleccionado = None

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

    def intentar_registrar():
        resultado = registrar(entry_usuario.get(), entry_clave.get())
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado, ahora puede inicia sesión")
        else:
            messagebox.showinfo("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Inicia sesión", command=intentar).pack()
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
            ir_al_menu(jugador_defensor, resultado)

    def intentar_registrar():
        resultado = registrar(entry_usuario.get(), entry_clave.get())
        if resultado:
            messagebox.showinfo("Éxito", "Usuario registrado, ahora puede inicia sesión")
        else:
            messagebox.showinfo("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Inicia sesión", command=intentar).pack()
    tk.Button(ventana, text="Registrarse", command=intentar_registrar).pack()


def ir_al_menu(jugador_defensor, jugador_atacante):
    """Muestra el menú principal con las opciones de iniciar juego, ranking y salir.
    Recibe los dos jugadores ya logueados.
    No devuelve nada.
    """
    # función que arranca la partida cuando se elige "Iniciar juego"
    def arrancar_partida():
        crear_partida(jugador_defensor, jugador_atacante)

    mostrar_menu_principal(ventana, arrancar_partida)

def crear_partida(jugador_defensor, jugador_atacante):
    """Crea la partida con los dos jugadores y pasa a elegir facciones."""
    global partida
    partida = Partida(jugador_defensor, jugador_atacante)

    # reinicia el estado de selección para la partida nueva
    ventana.fila_seleccionada = None
    ventana.columna_seleccionada = None
    ventana.objeto_seleccionado = None

    # reinicia el tablero para que se dibuje desde cero
    import interfaz_tablero
    interfaz_tablero.tablero_iniciado = False

    elegir_faccion_defensor(ventana, partida)


iniciar_juego()
