import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import cv2
import datetime

# Salir de pantalla completa con la tecla Escape
def salir_pantalla_completa(evento=None):
    ventana_principal.attributes("-fullscreen", False)

# Función para crear encabezado con imágenes y texto
def crear_encabezado(frame, ruta_izquierda, ruta_derecha, texto):
    # Cargar y redimensionar imágenes para el encabezado
    imagen_izquierda = Image.open(ruta_izquierda).resize((100, 100))
    foto_izquierda = ImageTk.PhotoImage(imagen_izquierda)
    
    imagen_derecha = Image.open(ruta_derecha).resize((100, 100))
    foto_derecha = ImageTk.PhotoImage(imagen_derecha)
    
    # Colocar las imágenes y el texto en el encabezado
    tk.Label(frame, image=foto_izquierda).pack(side="left", padx=10, pady=10)
    tk.Label(frame, image=foto_derecha).pack(side="right", padx=10, pady=10)
    etiqueta_texto = tk.Label(frame, text=texto, font=("Arial", 18, "bold"), justify="center")
    etiqueta_texto.pack(side="top", pady=10)
    
    
    # Guardar las imágenes en el objeto Label para que se mantengan en memoria
    etiqueta_texto.image_left = foto_izquierda
    etiqueta_texto.image_right = foto_derecha

ventana_principal = tk.Tk()
ventana_principal.title("Detección de errores en posicionamiento de componentes en PCB")
ventana_principal.attributes("-fullscreen", True)
ventana_principal.bind("<Escape>", salir_pantalla_completa)

# Encabezado
frame_encabezado = tk.Frame(ventana_principal)
frame_encabezado.pack(side="top", fill="x")

# Rutas de imágenes y texto para encabezado
ruta_imagen_izquierda = r"C:\Users\hgera\OneDrive - Instituto Politecnico Nacional\9no semestre\TT1\HMI\IPN.jpg"
ruta_imagen_derecha = r"C:\Users\hgera\OneDrive - Instituto Politecnico Nacional\9no semestre\TT1\HMI\Upiiz.jpg"
texto_encabezado = "Instituto Politécnico Nacional\nUnidad Profesional Interdisciplinaria de Ingeniería Campus Zacatecas\nIngeniería en Mecatrónica"

crear_encabezado(frame_encabezado, ruta_imagen_izquierda, ruta_imagen_derecha, texto_encabezado)



#////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Configuración del Notebook (Pestañas)
notebook = ttk.Notebook(ventana_principal)
notebook.pack(expand=True, fill="both")

pestaña1 = tk.Frame(notebook, bg="gray")
pestaña2 = tk.Frame(notebook, bg="gray")

notebook.add(pestaña1, text="Configuración de parámetros")
notebook.add(pestaña2, text="Visualización de resultados")

# --------------------------
# Pestaña 1 - Configuración
# --------------------------
# Carga y visualización de archivos
frame_carga_archivo = tk.Frame(pestaña1, bg="gray")
frame_carga_archivo.pack(side="left", padx=20, pady=10, fill="y")

def cargar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos de Texto", "*.txt"), ("CSV", "*.csv")])
    if archivo:
        with open(archivo, 'r') as f:
            contenido = f.read()
            text_visualizacion.config(state='normal')
            text_visualizacion.delete(1.0, tk.END)
            text_visualizacion.insert(tk.END, contenido)
            text_visualizacion.config(state='disabled')

tk.Button(frame_carga_archivo, text="Cargar Archivo Pick and Place", font=("Arial", 14), command=cargar_archivo).pack(pady=10)

# Text widget con scrollbar
frame_scroll = tk.Frame(frame_carga_archivo)
frame_scroll.pack(pady=10)
text_visualizacion = tk.Text(frame_scroll, wrap=tk.WORD, height=15, width=40, font=("Arial", 12), state='disabled')
scrollbar = tk.Scrollbar(frame_scroll, command=text_visualizacion.yview)
text_visualizacion.configure(yscrollcommand=scrollbar.set)
text_visualizacion.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Controladores tipo slider
frame_sliders = tk.Frame(pestaña1, bg="lightblue")
frame_sliders.pack(side="left", padx=20, pady=10)

slider1 = tk.Scale(frame_sliders, from_=0, to=300, orient="horizontal", label="Control de iluminación")
slider1.pack(pady=10)
slider2 = tk.Scale(frame_sliders, from_=0, to=100, orient="horizontal", label="Distancia de actuador cámara a PCB")
slider2.pack(pady=10)

# Vista previa de cámara y captura
frame_video = tk.Frame(pestaña1, bg="gray")
frame_video.pack(side="left", padx=20, pady=10, fill="both", expand=True)
label_video = tk.Label(frame_video, text="Vista previa de la cámara")
label_video.pack(fill="both", expand=True)

def mostrar_video():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (700,700))
    imagen = Image.fromarray(frame)
    imagen_tk = ImageTk.PhotoImage(image=imagen)
    label_video.configure(image=imagen_tk)
    label_video.image = imagen_tk
    label_video.after(10, mostrar_video)

def capturar_imagen():
    _, frame = cap.read()
    nombre_imagen = f"captura_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    cv2.imwrite(nombre_imagen, frame)
    print(f"Imagen guardada como {nombre_imagen}")
    mostrar_imagen_capturada(nombre_imagen)

tk.Button(pestaña1, text="Capturar Imagen", font=("Arial", 14), command=capturar_imagen).pack(pady=10)

# Inicialización de la cámara
cap = cv2.VideoCapture(0)
mostrar_video()

# --------------------------
# Pestaña 2 - Visualización de Resultados
# --------------------------
frame_imagenes = tk.Frame(pestaña2, bg="lightgreen")
frame_imagenes.pack(pady=20, fill="both", expand=True)

frame_imagen_capturada = tk.Frame(frame_imagenes, bg="black", width=640, height=480)
frame_imagen_capturada.pack(side="left", padx=20, pady=10, expand=True)
label_imagen_capturada = tk.Label(frame_imagen_capturada, text="Imagen Capturada")
label_imagen_capturada.pack(fill="both", expand=True)

frame_imagen_generada = tk.Frame(frame_imagenes, bg="lightgrey", width=320, height=240)
frame_imagen_generada.pack(side="left", padx=20, pady=10, expand=True, fill="both")
label_imagen_generada = tk.Label(frame_imagen_generada, text="Imagen Generada")
label_imagen_generada.pack(fill="both", expand=True)

def mostrar_imagen_capturada(ruta):
    imagen = Image.open(ruta)
    imagen = imagen.resize((320, 240))
    imagen_tk = ImageTk.PhotoImage(imagen)
    label_imagen_capturada.configure(image=imagen_tk)
    label_imagen_capturada.image = imagen_tk

ventana_principal.mainloop()
cap.release()
cv2.destroyAllWindows()