import tkinter as tk
from PIL import Image, ImageTk

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
    
def cargar_imagen(ruta, tamano):
    """Carga una imagen, la redimensiona y la prepara para usar en Tkinter.
    Recibe la ruta de la imagen y el tamaño (un número de píxeles para ancho y alto).
    Devuelve la imagen lista para mostrar en un widget.
    """
    imagen_original = Image.open(ruta)
    imagen_chica = imagen_original.resize((tamano, tamano))
    imagen = ImageTk.PhotoImage(imagen_chica)
    return imagen

def crear_imagen_vacia(tamano):
    """Crea una imagen transparente del tamaño dado, para casillas vacías.
    Devuelve la imagen lista para Tkinter.
    """
    imagen = Image.new("RGBA", (tamano, tamano), (0, 0, 0, 0))
    return ImageTk.PhotoImage(imagen)
