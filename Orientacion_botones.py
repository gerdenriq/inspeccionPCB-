import cv2
import numpy as np
import customtkinter as ctk
from PIL import Image, ImageTk

# Configuración inicial
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

class SelectorEsquina(ctk.CTk):
    def __init__(self, ruta_imagen):
        super().__init__()
        self.title("Selector de Orientación de PCB")
        self.geometry("900x700")

        # Cargar imagen
        self.imagen_original = cv2.imread(ruta_imagen)
        self.imagen_actual = self.imagen_original.copy()

        # Dibujar números en esquinas
        self.imagen_marcada = self.dibujar_esquinas(self.imagen_actual.copy())

        # Convertir imagen para mostrar en Tkinter
        self.imagen_tk = self.cv2_to_imageTk(self.imagen_marcada)

        # Crear widgets
        self.label_instrucciones = ctk.CTkLabel(
            self, 
            text="Usa los botones para rotar la imagen.\nDeja la esquina de referencia en la posición superior izquierda.",
            font=("Arial", 20, "bold"),
            text_color="blue"
        )
        self.label_instrucciones.pack(pady=10)

        self.label_imagen = ctk.CTkLabel(self, image=self.imagen_tk, text="")
        self.label_imagen.pack(pady=10)

        # Botones de rotación
        frame_botones = ctk.CTkFrame(self)
        frame_botones.pack(pady=10)

        self.boton_rotar_izq = ctk.CTkButton(frame_botones, text="↺ Rotar 90° Antihorario", command=self.rotar_izquierda)
        self.boton_rotar_izq.grid(row=0, column=0, padx=20)

        self.boton_rotar_der = ctk.CTkButton(frame_botones, text="↻ Rotar 90° Horario", command=self.rotar_derecha)
        self.boton_rotar_der.grid(row=0, column=1, padx=20)

        # Botón confirmar orientación (ROJO)
        self.boton_confirmar = ctk.CTkButton(
            self, 
            text="✅ Confirmar Orientación", 
            fg_color="red", 
            hover_color="#cc0000", 
            text_color="white",
            font=("Arial", 20, "bold"),
            command=self.confirmar_orientacion
        )
        self.boton_confirmar.pack(pady=20)

    def dibujar_esquinas(self, imagen):
        alto, ancho, _ = imagen.shape
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 4  # Más grande
        color = (0, 0, 255)  # Rojo
        thickness = 6  # Más grueso

        offset_x = 30
        offset_y = 50

        # Posiciones de los números (con espacio para que no se corten)
        posiciones = [
            (offset_x, offset_y),                      # Superior izquierda
            (ancho - 100, offset_y),                   # Superior derecha
            (ancho - 100, alto - 30),                  # Inferior derecha
            (offset_x, alto - 30)                      # Inferior izquierda
        ]

        for idx, pos in enumerate(posiciones):
            cv2.putText(imagen, str(idx + 1), pos, font, font_scale, color, thickness, cv2.LINE_AA)

        return imagen

    def cv2_to_imageTk(self, imagen_cv2):
        imagen_rgb = cv2.cvtColor(imagen_cv2, cv2.COLOR_BGR2RGB)
        imagen_pil = Image.fromarray(imagen_rgb)

        # Ajustar tamaño de previsualización (sin distorsionar)
        imagen_pil = imagen_pil.resize((800, 550), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(imagen_pil)

    def actualizar_preview(self):
        self.imagen_marcada = self.dibujar_esquinas(self.imagen_actual.copy())
        self.imagen_tk = self.cv2_to_imageTk(self.imagen_marcada)
        self.label_imagen.configure(image=self.imagen_tk)
        self.label_imagen.image = self.imagen_tk  # MUY IMPORTANTE

    def rotar_izquierda(self):
        self.imagen_actual = self.rotar_imagen(self.imagen_actual, 270)
        self.actualizar_preview()

    def rotar_derecha(self):
        self.imagen_actual = self.rotar_imagen(self.imagen_actual, 90)
        self.actualizar_preview()

    def rotar_imagen(self, imagen, angulo):
        if angulo == 90:
            return cv2.rotate(imagen, cv2.ROTATE_90_CLOCKWISE)
        elif angulo == 270:
            return cv2.rotate(imagen, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            return imagen  # Por si acaso

    def confirmar_orientacion(self):
        print("Orientación confirmada.")
        self.destroy()

# Ejecutar
if __name__ == "__main__":
    ruta_imagen = r"C:\Users\hgera\Pictures\Camera Roll\WIN_20250415_12_33_52_Pro.jpg"
    app = SelectorEsquina(ruta_imagen)
    app.mainloop()
