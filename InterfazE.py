import customtkinter as ctk  # type: ignore
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import datetime

# Salir de pantalla completa con la tecla Escape
def salir_pantalla_completa(evento=None):
    ventana_principal.attributes("-fullscreen", False)

# Función para crear encabezado con imágenes y texto
def crear_encabezado(frame, ruta_izquierda, ruta_derecha, texto):
    # Cargar y redimensionar imágenes para el encabezado
    imagen_izquierda = Image.open(ruta_izquierda).resize((150, 150))  # Aumentar tamaño
    foto_izquierda = ImageTk.PhotoImage(imagen_izquierda)

    imagen_derecha = Image.open(ruta_derecha).resize((150, 150))  # Aumentar tamaño
    foto_derecha = ImageTk.PhotoImage(imagen_derecha)

    # Crear un Frame para contener las imágenes y el texto
    frame_encabezado = ctk.CTkFrame(frame, fg_color="transparent")
    frame_encabezado.pack(side="top", pady=10)

    # Colocar las imágenes y el texto en el encabezado usando grid
    label_izquierda = ctk.CTkLabel(frame_encabezado, image=foto_izquierda, text="", fg_color="transparent")
    label_izquierda.grid(row=0, column=0, padx=10)

    etiqueta_texto = ctk.CTkLabel(frame_encabezado, text=texto, font=("Arial", 20, "bold"), justify="center", fg_color="transparent")
    etiqueta_texto.grid(row=0, column=1, padx=10)

    label_derecha = ctk.CTkLabel(frame_encabezado, image=foto_derecha, text="", fg_color="transparent")
    label_derecha.grid(row=0, column=2, padx=10)

    # Guardar las imágenes en el objeto Label para que se mantengan en memoria
    label_izquierda.image = foto_izquierda
    label_derecha.image = foto_derecha

ctk.set_appearance_mode("Dark")  # "System" (default), "Dark", "Light"
ctk.set_default_color_theme("green")  # "blue" (default), "green", "dark-blue", etc.

ventana_principal = ctk.CTk()
ventana_principal.title("Detección de errores en posicionamiento de componentes en PCB")
ventana_principal.attributes("-fullscreen", True)
ventana_principal.bind("<Escape>", salir_pantalla_completa)

# Encabezado
frame_encabezado = ctk.CTkFrame(ventana_principal)
frame_encabezado.pack(side="top", fill="x")

# Rutas de imágenes y texto para encabezado
ruta_imagen_izquierda = r"C:\Users\hgera\OneDrive - Instituto Politecnico Nacional\9no semestre\TT1\HMI\IPN.png"
ruta_imagen_derecha = r"C:\Users\hgera\OneDrive - Instituto Politecnico Nacional\9no semestre\TT1\HMI\Upiiz.jpg"
texto_encabezado = "Instituto Politécnico Nacional\nUnidad Profesional Interdisciplinaria de Ingeniería Campus Zacatecas\nIngeniería en Mecatrónica"

crear_encabezado(frame_encabezado, ruta_imagen_izquierda, ruta_imagen_derecha, texto_encabezado)

# Configuración del Notebook (Pestañas)
notebook = ctk.CTkTabview(ventana_principal)
notebook.pack(expand=True, fill="both")

pestaña1 = notebook.add("Configuración de parámetros")
pestaña2 = notebook.add("Visualización de resultados")

# -------------------------- 
# Pestaña 1 - Configuración 
# -------------------------- 
# Carga y visualización de archivos
frame_carga_archivo = ctk.CTkFrame(pestaña1, width=500, height=500)
frame_carga_archivo.pack(side="left", padx=10, pady=10, fill="y")

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt"), ("CSV", "*.csv")])
    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()
            text_visualizacion.configure(state='normal')  # Cambiado de 'config' a 'configure'
            text_visualizacion.delete(1.0, ctk.END)
            text_visualizacion.insert(ctk.END, contenido)
            text_visualizacion.configure(state='disabled')  # Cambiado de 'config' a 'configure'

ctk.CTkButton(frame_carga_archivo, text="Cargar Archivo Pick and Place", command=cargar_archivo).pack(pady=10)

# Text widget con scrollbar, aumentado en tamaño
frame_scroll = ctk.CTkFrame(frame_carga_archivo)
frame_scroll.pack(pady=10, fill="both", expand=True)

text_visualizacion = ctk.CTkTextbox(frame_scroll, wrap=ctk.WORD, height=40, width=80, state='disabled')  # Aumentar la altura
scrollbar = ctk.CTkScrollbar(frame_scroll, command=text_visualizacion.yview)
text_visualizacion.configure(yscrollcommand=scrollbar.set)
text_visualizacion.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Controladores tipo slider
frame_sliders = ctk.CTkFrame(pestaña1)
frame_sliders.pack(side="left", padx=20, pady=10)

# Labels para los sliders
ctk.CTkLabel(frame_sliders, text="Control de iluminación").pack(pady=5)
slider1 = ctk.CTkSlider(frame_sliders, from_=0, to=300, orientation="horizontal")
slider1.pack(pady=10)
ctk.CTkLabel(frame_sliders, text="Distancia de actuador cámara a PCB").pack(pady=5)
slider2 = ctk.CTkSlider(frame_sliders, from_=0, to=100, orientation="horizontal")
slider2.pack(pady=10)

# Vista previa de cámara y captura
frame_video = ctk.CTkFrame(pestaña1)
frame_video.pack(side="left", padx=20, pady=10, fill="both", expand=True)
label_video = ctk.CTkLabel(frame_video, text="")
label_video.pack(fill="both", expand=True)

def mostrar_video():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (700, 700))
    imagen = Image.fromarray(frame)
    imagen_tk = ImageTk.PhotoImage(image=imagen)
    label_video.configure(image=imagen_tk)
    label_video.image = imagen_tk
    label_video.after(10, mostrar_video)

# Nueva función para capturar la imagen con ventana de confirmación
def capturar_imagen():
    # Captura de imagen
    _, frame = cap.read()
    imagen_capturada = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Crear una ventana de confirmación
    ventana_confirmacion = ctk.CTkToplevel(ventana_principal)
    ventana_confirmacion.title("Confirmar Imagen Capturada")
    ventana_confirmacion.geometry("400x400")
    ventana_confirmacion.grab_set()  # Hacer la ventana modal

    # Convertir a formato que puede mostrar Tkinter
    imagen_tk = Image.fromarray(imagen_capturada)
    imagen_tk = imagen_tk.resize((320, 240))  # Redimensionar para mostrar
    imagen_mostrar = ImageTk.PhotoImage(imagen_tk)

    # Mostrar la imagen en la ventana de confirmación
    label_imagen_confirmacion = ctk.CTkLabel(ventana_confirmacion, image=imagen_mostrar)
    label_imagen_confirmacion.image = imagen_mostrar  # Mantener referencia
    label_imagen_confirmacion.pack(pady=10)

    # Botón para confirmar la imagen
    def confirmar():
        nombre_imagen = f"captura_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        cv2.imwrite(nombre_imagen, frame)  # Guardar la imagen
        mostrar_imagen_capturada(nombre_imagen)  # Mostrar en la pestaña 2
        ventana_confirmacion.destroy()  # Cerrar ventana de confirmación

    # Botón para rechazar la imagen
    def rechazar():
        ventana_confirmacion.destroy()  # Solo cerrar la ventana

    ctk.CTkButton(ventana_confirmacion, text="Aceptar", command=confirmar).pack(pady=5)
    ctk.CTkButton(ventana_confirmacion, text="Rechazar", command=rechazar).pack(pady=5)

ctk.CTkButton(pestaña1, text="Capturar Imagen", command=capturar_imagen).pack(pady=10)

# Inicialización de la cámara
cap = cv2.VideoCapture(0)
mostrar_video()

# -------------------------- 
# Pestaña 2 - Visualización de Resultados 
# -------------------------- 
frame_imagenes = ctk.CTkFrame(pestaña2)
frame_imagenes.pack(expand=True, fill="both")

frame_imagen_capturada = ctk.CTkFrame(frame_imagenes)
frame_imagen_capturada.pack(side="top", pady=10, fill="x")

label_imagen_capturada = ctk.CTkLabel(frame_imagen_capturada, text="Imagen Capturada")
label_imagen_capturada.pack()

frame_imagen_generada = ctk.CTkFrame(frame_imagenes)
frame_imagen_generada.pack(side="top", pady=10, fill="x")

label_imagen_generada = ctk.CTkLabel(frame_imagen_generada, text="Imagen Generada")
label_imagen_generada.pack()

def mostrar_imagen_capturada(ruta_imagen):
    imagen_capturada = Image.open(ruta_imagen)
    imagen_tk = ImageTk.PhotoImage(imagen_capturada.resize((320, 240)))  # Redimensionar para mostrar
    label_imagen_capturada.configure(image=imagen_tk)
    label_imagen_capturada.image = imagen_tk  # Mantener referencia

def mostrar_imagen_generada(ruta_imagen):
    imagen_generada = Image.open(ruta_imagen)
    imagen_tk = ImageTk.PhotoImage(imagen_generada.resize((320, 240)))  # Redimensionar para mostrar
    label_imagen_generada.configure(image=imagen_tk)
    label_imagen_generada.image = imagen_tk  # Mantener referencia

ventana_principal.mainloop()
