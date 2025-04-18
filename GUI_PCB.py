# Agregar historial de placas analizadas
import tkinter, os, tkinter.messagebox, customtkinter, cv2
from tkinter import filedialog, font
from PIL import Image, ImageTk

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        #Variables y controles
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # configure window
        self.title("AOI Vision Pro")
        self.attributes("-fullscreen", False)
        # Logo
        logo = customtkinter.CTkImage(Image.open('logo.png'),size=(100,100))
        self.framelogo = customtkinter.CTkLabel(self,fg_color='transparent',text='',width=100,height=100,anchor='center',image=logo)
        self.framelogo.grid(row=0, column=0, padx=(20, 0), pady=(10, 0))
        
        #l298n=customtkinter.CTkImage(Image.open(''),size=(100,100))
        #Placas recientes
        self.frameplacas = customtkinter.CTkLabel(self,width=100,height=120, text='', image=logo)
        self.frameplacas.grid(row=0, column=1, padx=(20, 0), pady=(10,10), sticky="nw")
        self.frameplacas1 = customtkinter.CTkLabel(self,width=100,height=120,text=' ',image=logo)
        self.frameplacas1.grid(row=0, column=1, padx=(140, 0), pady=(10,10), sticky="nw")
        self.frameplacas2 = customtkinter.CTkLabel(self,width=100,height=120,text='',image=logo)
        self.frameplacas2.grid(row=0, column=1, padx=(260, 0), pady=(10,10), sticky="nw")
        self.frameplacas3 = customtkinter.CTkLabel(self,width=100,height=120,text='',image=logo)
        self.frameplacas3.grid(row=0, column=1, padx=(380, 0), pady=(10,10), sticky="nw")
        # Crear Frame de botones de Emergencia
        self.botones_emergencia = customtkinter.CTkLabel(self,width=100,height=100,fg_color='transparent')
        self.botones_emergencia.grid(row=0, column=1, padx=(20, 0), pady=(0, 0), sticky="ne")
        #Crear botones de emergencia
        self.checkbox_1 = customtkinter.CTkButton(master=self.botones_emergencia,corner_radius=100, text="STOP",height=100,width=100, anchor='center',fg_color='red',text_color='black',hover_color='green')
        self.checkbox_1.grid(row=0, column=0, pady=(20), padx=(20), sticky="n")
           
        #Secciones
            #Pestanas de configuraciones
        self.tabview = customtkinter.CTkTabview(self, width=200,height=screen_height-250,anchor='nw')
        self.tabview.grid(row=1, column=0, padx=(20, 0), pady=(0, 0), sticky="nsew")
        boton_inicio=self.tabview.add("      Start       ")
        boton_configuracion=self.tabview.add("      Configuration       ")
        boton_acerca=self.tabview.add("      About       ")
            #Pestana de visualizacion
        self.tabviewvisualizacion = customtkinter.CTkFrame(self, width=1160,height=screen_height-250)
        self.tabviewvisualizacion.grid(row=1, column=1, padx=(20, 0), pady=(0, 0), sticky="nsew")
        # Full Preview
        pcb=customtkinter.CTkImage(Image.open('l298n.png'),size=(500,600))
        self.fullpreview = customtkinter.CTkLabel(self.tabviewvisualizacion,text='',width=650,height=screen_height-250,image=pcb)
        self.fullpreview.grid(row=0, column=0, padx=(0, 0), pady=(10, 10))
        # Close up Preview
        closeuppcb=customtkinter.CTkImage(Image.open('L298NCorte.png'),size=(250,200))
        self.closeuppreview = customtkinter.CTkLabel(self.tabviewvisualizacion,text='',width=500,height=screen_height-250,image=closeuppcb)
        self.closeuppreview.grid(row=0, column=1, padx=(0, 0), pady=(0, 10))


        ##Configurar pestañas individuales

        # Start
        self.tabview.tab("      Start       ").grid_columnconfigure(0, weight=1)
        #Agregar elementos
        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview.tab("      Start       "),text='Cargar Archivos de Ensamble', command=self.cargar_archivos_button_event)
        self.sidebar_button_1.grid(row=0, column=0, padx=20, pady=20,sticky="nsew")

        # Configuracion
        self.tabview.tab("      Configuration       ").grid_columnconfigure(0, weight=1)
        #Agregar elementos
        self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("      Configuration       "), text="Apariencia:", anchor="w"  )
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("      Configuration       "), values=["Light", "Dark", "System"])
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10),sticky='nsew')

        self.scaling_label = customtkinter.CTkLabel(self.tabview.tab("      Configuration       "), text="Escala Interfaz de Usuario:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.tabview.tab("      Configuration       "), values=["80%", "90%", "100%", "110%", "120%"])
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20),sticky='nsew')
        # Acerca de
        self.tabview.tab("      About       ").grid_columnconfigure(0, weight=1)
        
        #Agregar elementos
        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview.tab("      About       "),text='Autores y colaboradores')
        self.sidebar_button_1.grid(row=0, column=0, padx=20, pady=20,sticky="nsew")
        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview.tab("      About       "),text='Manual de Usuario')
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10,sticky="nsew")

      

    def iniciar_button_event(self):

        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview.tab("      Start       "),text='Comenzar', command=self.iniciar_button_event)
        self.sidebar_button_1.grid(row=4, column=0, padx=20, pady=20)     
         
    def cargar_archivos_button_event(self):  
            error_archivo=str("Error: El archivo debe tener la extensión .csv")
            archivo = filedialog.askopenfilename(title="Selecciona un archivo")
            if archivo:
                 extension=os.path.splitext(archivo)[1]
                 self.appearance_mode_label = customtkinter.CTkLabel(self.tabview.tab("      Start       "),text=' ', anchor="w")
                 self.appearance_mode_label.grid(row=1, column=0, padx=20, pady=0)
                 if extension.lower()=='.csv':
                        self.loadedfile_label = customtkinter.CTkButton(self.tabview.tab("      Start       "),text='                        Archivo cargado                        ',anchor='center',bg_color="white")
                        self.loadedfile_label.grid(row=1, column=0, padx=20, pady=0)
                        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview.tab("      Start       "),text=os.path.basename(archivo).split('.')[0][:7],fg_color='green')
                        self.sidebar_button_1.grid(row=2, column=0, padx=20, pady=0)
                        #Entrada dimensiones de la placa
                        self.Dimensiones=customtkinter.CTkLabel(self.tabview.tab("      Start       "),text="Inserte las dimensiones de la placa")
                        self.Dimensiones.grid(row=3, column=0,sticky='n')
                        self.largo = customtkinter.CTkEntry(self.tabview.tab("      Start       "),placeholder_text='Largo', width=50)
                        self.largo.grid(row=4, column=0, padx=100, pady=(0, 0), sticky="w")
                        self.ancho = customtkinter.CTkEntry(self.tabview.tab("      Start       "),placeholder_text='Ancho', width=50)
                        self.ancho.grid(row=4, column=0, padx=(0,100), pady=(0, 0),sticky="e")

                        self.Actuador_label = customtkinter.CTkLabel(self.tabview.tab("      Start       "),text='Distancia del Actuador', anchor="w")
                        self.Actuador_label.grid(row=5, column=0, padx=20, pady=(20,0))
                        self.progressbar_1 = customtkinter.CTkSlider(self.tabview.tab("      Start       "),from_=0,to=10,number_of_steps=10)
                        self.progressbar_1.grid(row=5, column=0, padx=(20, 10), pady=(100, 10), sticky="ew")

                        self.sidebar_button_1 = customtkinter.CTkButton(self.tabview.tab("      Start       "),text='Capturar Imagen',anchor='center')
                        self.sidebar_button_1.grid(row=6, column=0, padx=20, pady=(20,0),sticky='nsew')
 
                 else:
                        self.errorfile_label = customtkinter.CTkButton(self.tabview.tab("      Start       "),text=error_archivo,anchor="center",bg_color='white')
                        self.errorfile_label.grid(row=1, column=0, padx=20, pady=0)
                        self.errorfile_button = customtkinter.CTkButton(self.tabview.tab("      Start       "),text=os.path.basename(archivo).split('.')[0][:7],fg_color='red')
                        self.errorfile_button.grid(row=2, column=0, padx=20, pady=0)                        
    def capturar_imagen():
        top=customtkinter.CTkToplevel()
        top.title('Confirmacion de captura')
        top.geometry('300x200')
        label=customtkinter.CTkLabel(top,text='Continuar con el analisis de la imagen capturada?')
        label.pack(pady=20)
            
            
if __name__ == "__main__":
    app = App()
    app.mainloop()