import tkinter as tk
from utilidades import centrar_ventana, limpiar_ventana
from jugador import login, registrar, ranking_defensores, ranking_atacantes
from tkinter import messagebox
def mostrar_menu():
    """Dibuja la pantalla del menú principal en la ventana.
    Limpia la ventana y muestra el título y los botones para
    iniciar sesión y ver el ranking. No recibe ni devuelve nada.
    """
    limpiar_ventana(ventana)  

    label_titulo = tk.Label(ventana, text="Menu Principal")
    label_titulo.pack()

    boton_ingresar = tk.Button(ventana, text="Iniciar sesion", command=mostrar_login)
    boton_ingresar.pack() 
    
    boton_ranking = tk.Button(ventana, text="Ver Ranking", command=mostrar_ranking)
    boton_ranking.pack() 
    
    boton_salir= tk.Button(ventana, text="Salir", command= ventana.destroy)
    boton_salir.pack() 
    
def mostrar_login():
    """
    Limpia la ventana y dibuja la ventana donde muestran los campos para agregar
    el nombre y la clave del usuario y tres botones, uno para iniciar sesion, 
    otro para registrarse y uno de regresar. No recibe ni devuelve nada
    """
    def intentar_login():
        usuario = entry_usuario.get()
        clave = entry_clave.get()
        resultado = login(usuario, clave)
        if resultado == None:
            messagebox.showinfo("Error", "Usuario o clave incorrecta")
        else:
            messagebox.showinfo("Exito", f"Bienvenido {resultado.usuario}")
            
    def intentar_registrar():
        usuario = entry_usuario.get()
        clave = entry_clave.get()
        resultado = registrar(usuario, clave)
        if resultado == False:
            messagebox.showinfo("Error","El usuario ya esta registado, Inicia Sesion")
        else:
            messagebox.showinfo("Exito","El usuario fue registrado")
     
    limpiar_ventana(ventana)  

    label_usuario = tk.Label(ventana, text="Usuario:")
    label_usuario.pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()

    label_clave = tk.Label(ventana, text="Contraseña:")
    label_clave.pack()
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.pack()

    boton_login = tk.Button(ventana, text="Iniciar sesión", command=intentar_login)
    boton_login.pack()

    boton_registrar = tk.Button(ventana, text="Registrarse", command=intentar_registrar)
    boton_registrar.pack()
    
    boton_regresar = tk.Button(ventana, text="Regresar", command=mostrar_menu)
    boton_regresar.pack()

def mostrar_ranking():
    """
    Limpia la ventana y dibuja la ventana donde se muestra la lista de los top 5
    de defensores y atacantes registrados con sus victorias ordenados de mayor a menor.
    No recibe ni devuelve nada"""
    limpiar_ventana(ventana)

    titulo_def = tk.Label(ventana, text="TOP DEFENSORES")
    titulo_def.pack()
    for jugador in ranking_defensores():
        label_defensor = tk.Label(ventana, text=f"{jugador.usuario}: {jugador.victorias_defensor}")
        label_defensor.pack()

    titulo_atac = tk.Label(ventana, text="TOP ATACANTES")
    titulo_atac.pack()
    for jugador in ranking_atacantes():
        label_atacante = tk.Label(ventana, text=f"{jugador.usuario}: {jugador.victorias_atacante}")
        label_atacante.pack()
        
    boton_regresar = tk.Button(ventana, text="Regresar", command=mostrar_menu)
    boton_regresar.pack()

def iniciar():
    """Crea y configura la ventana principal y arranca la aplicación en el menú."""

    global ventana
    ventana = tk.Tk()
    ventana.title("Defensa y Asalto de Base")
    centrar_ventana(ventana, 400, 300)
    ventana.resizable(False, False)

    mostrar_menu()          
    ventana.mainloop()     
