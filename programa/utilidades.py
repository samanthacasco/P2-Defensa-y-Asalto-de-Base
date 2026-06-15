import tkinter as tk

def centrar_ventana(ventana, ancho, alto):
    """
    Centra una ventana de tkinter en la pantalla del usuario, 
    independientemente del tamaño del monitor. Calcula la 
    posición usando las dimensiones de la pantalla.
    """
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    pos_x = (ancho_pantalla - ancho) // 2
    pos_y = (alto_pantalla - alto) // 2
    
    ventana.geometry(f"{ancho}x{alto}+{pos_x}+{pos_y}")

def limpiar_ventana(ventana):
    """Elimina todos los widgets que haya en la ventana recibida.
    Recibe la ventana a limpiar.
    No devuelve nada; se usa para borrar la pantalla anterior antes de dibujar otra.
    """
    for widget in ventana.winfo_children():
        widget.destroy()  
