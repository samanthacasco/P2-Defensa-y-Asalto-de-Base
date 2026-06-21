import tkinter as tk
from tkinter import messagebox
from utilidades import centrar_ventana, limpiar_ventana
from jugador import login, registrar
from partida import Partida
from interfaz_facciones import elegir_faccion_defensor
from interfaz_tablero import mostrar_tablero
from interfaz_menu import mostrar_menu_principal
import interfaz_tablero
# Variables globales que comparten todas las pantallas
ventana = None
partida = None
jugador_defensor = None


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
    centrar_ventana(ventana, 400, 320)
    login_defensor()
    ventana.mainloop()


def login_defensor():
    """Pantalla de login del defensor."""
    limpiar_ventana(ventana)
    ventana.configure(bg="#e8e2d0")  # color de fondo

    tk.Label(ventana, text="LOGIN DEFENSOR", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(ventana, text="Usuario:",bg="#e8e2d0").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack(pady=5)
    
    tk.Label(ventana, text="Contraseña:",bg="#e8e2d0").pack()
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.pack(pady=5)

    def intentar():
        usuario = entry_usuario.get().strip()
        clave = entry_clave.get().strip()

        # Validamos campos vacíos ANTES de llamar al login
        if usuario == "" or clave == "":
            messagebox.showerror("Error", "No se pueden usar campos vacíos")
            return

        resultado = login(usuario, clave)
        if resultado is None:
            messagebox.showerror("Error", "Usuario o clave incorrecta")
        else:
            global jugador_defensor
            jugador_defensor = resultado
            login_atacante(jugador_defensor)

    def intentar_registrar():
        usuario = entry_usuario.get().strip()
        clave = entry_clave.get().strip()

        # Validamos campos vacíos ANTES de registrar
        if usuario == "" or clave == "":
            messagebox.showerror("Error", "No se pueden usar campos vacíos")
            return

        if registrar(usuario, clave):
            messagebox.showinfo("Éxito", "Usuario registrado, ahora puede iniciar sesión")
        else:
            messagebox.showerror("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Iniciar sesión", command=intentar, width=15,bg="#ffcccc").pack(pady=5)
    tk.Button(ventana, text="Registrarse", command=intentar_registrar, width=15,bg="#ffcccc").pack(pady=5)


def login_atacante(jugador_defensor_logueado):
    """Pantalla de login del atacante. Recibe el jugador defensor ya logueado."""
    limpiar_ventana(ventana)

    tk.Label(ventana, text="LOGIN ATACANTE", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(ventana, text="Usuario:", bg="#e8e2d0").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack(pady=5)
    
    tk.Label(ventana, text="Contraseña:",bg="#e8e2d0").pack()
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.pack(pady=5)

    def intentar():
        usuario = entry_usuario.get().strip()
        clave = entry_clave.get().strip()

        if usuario == "" or clave == "":
            messagebox.showerror("Error", "No se pueden usar campos vacíos")
            return

        if usuario == jugador_defensor_logueado.usuario:
            messagebox.showerror("Error", "Ese jugador ya entró como defensor")
            return

        resultado = login(usuario, clave)
        if resultado is None:
            messagebox.showerror("Error", "Usuario o clave incorrecta")
        else:
            ir_al_menu(jugador_defensor_logueado, resultado)

    def intentar_registrar():
        usuario = entry_usuario.get().strip()
        clave = entry_clave.get().strip()

        if usuario == "" or clave == "":
            messagebox.showerror("Error", "No se pueden usar campos vacíos")
            return

        if registrar(usuario, clave):
            messagebox.showinfo("Éxito", "Usuario registrado, ahora puede iniciar sesión")
        else:
            messagebox.showerror("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Iniciar sesión", command=intentar, width=15,bg="#ffcccc").pack(pady=5)
    tk.Button(ventana, text="Registrarse", command=intentar_registrar, width=15,bg="#ffcccc").pack(pady=5)


def ir_al_menu(jugador_defensor_obj, jugador_atacante_obj):
    """Muestra el menú principal con las opciones de iniciar juego, ranking y salir."""
    def arrancar_partida():
        crear_partida(jugador_defensor_obj, jugador_atacante_obj)

    mostrar_menu_principal(ventana, arrancar_partida)

def crear_partida(jugador_defensor_obj, jugador_atacante_obj):
    """Crea la partida con los dos jugadores y pasa a elegir facciones."""
    global partida
    partida = Partida(jugador_defensor_obj, jugador_atacante_obj)

    # Reinicia el estado de selección para la partida nueva
    ventana.fila_seleccionada = None
    ventana.columna_seleccionada = None
    ventana.objeto_seleccionado = None

    # Reinicia el tablero para que se dibuje desde cero
    interfaz_tablero.tablero_iniciado = False
    elegir_faccion_defensor(ventana, partida)


if __name__ == "__main__":
    iniciar_juego()