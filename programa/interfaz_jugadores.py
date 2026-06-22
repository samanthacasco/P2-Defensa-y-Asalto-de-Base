import tkinter as tk
from utilidades import centrar_ventana, limpiar_ventana
from jugador import login, registrar, ranking_defensores, ranking_atacantes
from tkinter import messagebox

def mostrar_menu_jugadores(ventana, al_iniciar_sesion_exito):
    """Dibuja la pantalla de gestión de usuarios usando la ventana principal."""
    limpiar_ventana(ventana)  
    centrar_ventana(ventana, 400, 300)

    label_titulo = tk.Label(ventana, text="Gestión de Jugadores", font=("Arial", 14, "bold"))
    label_titulo.pack(pady=10)

    # Pasamos 'ventana' y el callback de éxito al login
    boton_ingresar = tk.Button(ventana, text="Iniciar Sesión", width=20,command=lambda: mostrar_login(ventana, al_iniciar_sesion_exito))
    boton_ingresar.pack(pady=5) 
    
    boton_ranking = tk.Button(ventana, text="Ver Ranking", width=20, bg="#ffcccc", command=lambda: mostrar_ranking(ventana, al_iniciar_sesion_exito))
    boton_ranking.pack(pady=5) 
    
    boton_salir = tk.Button(ventana, text="Salir", width=20,bg="#ffcccc", command=ventana.destroy)
    boton_salir.pack(pady=5) 
    
def mostrar_login(ventana, al_iniciar_sesion_exito):
    """Campos para iniciar sesión o registrarse."""
    limpiar_ventana(ventana)
    
    tk.Label(ventana, text="INICIAR SESIÓN", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(ventana, text="Usuario:").pack()
    entry_usuario = tk.Entry(ventana)
    entry_usuario.pack()
    
    tk.Label(ventana, text="Clave:").pack()
    entry_clave = tk.Entry(ventana, show="*")
    entry_clave.pack()

    def intentar_login():
        usuario = entry_usuario.get()
        clave = entry_clave.get()
        jugador_logeado = login(usuario, clave)
        
        if jugador_logeado is not None:
            messagebox.showinfo("Éxito", f"¡Bienvenido {usuario}!")
            # Si el login es exitoso, ejecutamos la función que nos pasaron desde main.py
            al_iniciar_sesion_exito(jugador_logeado)
        else:
            messagebox.showerror("Error", "Usuario o clave incorrectos")

    def intentar_registrar():
        usuario = entry_usuario.get()
        clave = entry_clave.get()
        if usuario == "" or clave == "":
            messagebox.showwarning("Advertencia", "No se pueden usar campos vacíos")
            return
            
        if registrar(usuario, clave):
            messagebox.showinfo("Éxito", "Usuario registrado. Ya puedes iniciar sesión.")
        else:
            messagebox.showerror("Error", "Ese usuario ya existe")

    tk.Button(ventana, text="Ingresar", command=intentar_login).pack(pady=5)
    tk.Button(ventana, text="Registrarse", command=intentar_registrar).pack(pady=5)
    
    # Botón para volver atrás
    tk.Button(ventana, text="← Regresar", 
              command=lambda: mostrar_menu_jugadores(ventana, al_iniciar_sesion_exito)).pack(pady=10)

def mostrar_ranking(ventana, al_iniciar_sesion_exito):
    """Muestra el top 5 de defensores y atacantes."""
    limpiar_ventana(ventana)
    centrar_ventana(ventana, 450, 400)


    tk.Label(ventana, text="TOP DEFENSORES",font=("Arial", 11, "bold")).pack(pady=5)
    for jugador in ranking_defensores():
        tk.Label(ventana, text=f"{jugador.usuario}: {jugador.victorias_defensor} victorias").pack()

    tk.Label(ventana, text="TOP ATACANTES", font=("Arial", 11, "bold")).pack(pady=(15, 5))
    for jugador in ranking_atacantes():
        tk.Label(ventana, text=f"{jugador.usuario}: {jugador.victorias_atacante} victorias").pack()
        
    tk.Button(ventana, text="← Regresar", command=lambda: mostrar_menu_jugadores(ventana, al_iniciar_sesion_exito)).pack(pady=15)
