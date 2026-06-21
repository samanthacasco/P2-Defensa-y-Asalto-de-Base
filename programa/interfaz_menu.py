"""
Módulo de interfaz del menú principal y el ranking.
Muestra el menú (iniciar juego, ranking, salir) tras iniciar sesión,
y la ventana de rankings (top 5 defensores y atacantes).
"""
import tkinter as tk
from utilidades import centrar_ventana, limpiar_ventana
from jugador import ranking_defensores, ranking_atacantes


def mostrar_menu_principal(ventana, al_iniciar_juego):
    """Muestra el menú principal con las opciones del juego.
    Recibe la ventana y la función a llamar cuando se elige 'Iniciar juego'.
    No devuelve nada.
    """
    limpiar_ventana(ventana)
    centrar_ventana(ventana, 400, 350)

    tk.Label(ventana, text="DEFENSA Y ASALTO DE BASE", font=("Arial", 16, "bold")).pack(pady=20)
    tk.Label(ventana, text="Menú principal").pack(pady=5)

    tk.Button(ventana, text="Iniciar juego", width=20,bg="#ffcccc", command=al_iniciar_juego).pack(pady=10)
    tk.Button(ventana, text="Ranking", width=20,bg="#ffcccc",command=lambda: mostrar_ranking(ventana, al_iniciar_juego)).pack(pady=10)
    tk.Button(ventana, text="Salir", width=20,bg="#ffcccc", command=ventana.destroy).pack(pady=10)


def mostrar_ranking(ventana, al_iniciar_juego):
    """Muestra la ventana de rankings (top 5 defensores y atacantes).
    Recibe la ventana y la función de iniciar juego (para el botón regresar).
    No devuelve nada.
    """
    limpiar_ventana(ventana)
    centrar_ventana(ventana, 450, 500)

    # botón regresar al menú
    tk.Button(ventana, text="← Regresar al menú", bg="#ffcccc",command=lambda: mostrar_menu_principal(ventana, al_iniciar_juego)).pack(anchor="w", padx=10, pady=10)

    tk.Label(ventana, text="RANKING DE JUGADORES", font=("Arial", 14, "bold")).pack(pady=10)

    # ----- top defensores -----
    tk.Label(ventana, text="Mejores Defensores", font=("Arial", 12, "bold")).pack(pady=(10, 5))

    top_def = ranking_defensores()
    if not top_def:
        tk.Label(ventana, text="Aún no hay jugadores registrados.").pack()
    else:
        posicion = 1
        for jugador in top_def:
            tk.Label(ventana, text=f"{posicion}. {jugador.usuario} - {jugador.victorias_defensor} victorias", bg="#e8e2d0").pack()
            posicion += 1

    # ----- top atacantes -----
    tk.Label(ventana, text="Mejores Atacantes", font=("Arial", 12, "bold")).pack(pady=(15, 5))

    top_atac = ranking_atacantes()
    if not top_atac:
        tk.Label(ventana, text="Aún no hay jugadores registrados.").pack()
    else:
        posicion = 1
        for jugador in top_atac:
            tk.Label(ventana, text=f"{posicion}. {jugador.usuario} - {jugador.victorias_atacante} victorias",bg="#e8e2d0").pack()
            posicion += 1