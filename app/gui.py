from tkinter import *
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pyparsing import GoToColumn

from app import api_handler

import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import base64
import pandas as pd
from io import BytesIO

class Interfaz:

    #Inicializa los atributos
    def __init__(self):
        self.root = Tk()
        self.left_frame = Frame(self.root)
        self.right_frame = Frame(self.root)
        self.direction_input = None
        self.numero_slices = None
        self.botonEnviar = None
        self.botonLimpiar = None
        self.frameBotones = None
        self.canvas= None
        self.botonCargarImagen = None
        self.image_in_memory = None #La imagen en memoria
        self.archivo = None #String con la direccion del archivo
        self.consola = None
        self.response = (None,None)
        self.canvas_right = None
        self.top_frame = None
        self.bottom_frame = None
        self.canvas_figura = None
        self.input_prompt_usuario = None






    #Imprime la pantalla
    def mostrar(self):
        self.setUpPantalla()

        self.root.mainloop()

    #Establecemos las propiedades del GUI
    def setUpPantalla(self):
        # Inicializamos el root

        self.root.title("Powder calculator")
        self.root.iconphoto(True, PhotoImage(file="./recursos/imagenes/firecracker.png"))
        self.root.configure(background="#000000") #Se podría borrar
        self.setPantallaSize()
        self.dividirPantalla()
        self.dividirLadoIzquierdo()
        self.dividirLadoDerecho()

    #Establecemos el tamaño de la pantalla
    def setPantallaSize(self):
        # Obtenemos el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Configura la geometría de la ventana para ajustarse a la pantalla
        self.root.geometry(f"{screen_width}x{screen_height}")

    #Dividimos la pantalla en dos
    def dividirPantalla(self):

        #claculamos la mitad de la pantalla
        mitadancho = self.root.winfo_screenwidth() // 2

        # Aseguramos que la ventana haya terminado de renderizar para obtener su altura real
        self.root.update_idletasks()  # Forzamos a Tkinter a actualizar y calcular el tamaño de la ventana
        ventana_altura = self.root.winfo_height()

        #Lado izquierdo
        self.left_frame = Frame(self.root, width= mitadancho, bg="lightgray")
        self.left_frame.place(x=0, y=0, width=mitadancho, height=ventana_altura)

        #lado derecho
        self.right_frame = Frame(self.root, bg="white")
        self.right_frame.place(x=mitadancho, y=0, relwidth=1, relheight=1)

    def dividirLadoIzquierdo(self):

        # Primer recuadro: Entrada para la cantidad de pólvora
        self.direccion_quemado_label = Label(self.left_frame, text="Introduce direction of the burn along the axis of the "
           f"longest face: ", bg="lightgray")
        self.direccion_quemado_label.pack(pady=5)
        self.direction_input = Entry(self.left_frame)
        self.direction_input.pack(pady=5)

        # Segundo recuadro: Entrada para el segundo número
        self.numero_slices_label = Label(self.left_frame, text="Introduce number of slices: ", bg="lightgray")
        self.numero_slices_label.pack(pady=5)
        self.numero_slices = Entry(self.left_frame)
        self.numero_slices.pack(pady=5)

        # Tercer recuadro: Area de canvas para la imagen
        self.parrafo_label = Label(self.left_frame, text="Upload your image here: ", bg="lightgray")
        self.parrafo_label.pack(pady=5)

        # Crear un canvas donde se pueda arrastrar la imagen
        self.canvas = Canvas(self.left_frame, bg="white", height=200, width=200)
        self.canvas.pack(padx=10, pady=5)

        # Botón para cargar la imagen
        self.botonCargarImagen = Button(self.left_frame, text="Load Image", command=self.cargarImagen)
        self.botonCargarImagen.pack(pady=10)

        # Cuarto recuadro: Prompt de usuario
        self.prompt_usuario_label = Label(self.left_frame, text="Enter detailed description about the figure shape: ", bg="lightgray")
        self.prompt_usuario_label.pack(pady=5)
        self.input_prompt_usuario = Text(self.left_frame, bg="white", fg="black", wrap=WORD, height=12, width=90)
        self.input_prompt_usuario.pack(side=TOP, padx=5)

        # Quinto recuadro: Crear un contenedor para los botones
        self.frameBotones = Frame(self.left_frame , bg="lightgray")
        self.frameBotones.pack(pady=20)

        self.botonEnviar = Button(self.frameBotones, text="Submit", command=self.enviarDatos)
        self.botonEnviar.pack(side= LEFT, padx= 10,pady=20)


        self.botonLimpiar = Button(self.frameBotones, text="Clear", command=self.limpiarDatos)
        self.botonLimpiar.pack(side=LEFT, padx=10,pady=20)

    def pintargrafica(self, tabla, canvas):

        # Primero, eliminamos cualquier gráfico anterior en el canvas
        if self.canvas_figura:
            self.canvas_figura.get_tk_widget().destroy()  # Eliminar el widget anterior
            self.canvas_figura = None  # Restablecer la referencia

        # Crear la figura y el gráfico con matplotlib
        fig, ax = plt.subplots()

        tabla.plot(kind='bar',x='Slice', y='Cross-Sectional Area (mm^2)',ax=ax)  # Usar el DataFrame para crear el gráfico
        ax.set_title("Visual Representation of the Results")
        ax.set_xlabel("Slice")
        ax.set_ylabel("Cross-Sectional Area (mm^2)")

        # Convertir la figura de matplotlib a un lienzo de tkinter
        self.canvas_figura = FigureCanvasTkAgg(fig, master=canvas)
        self.canvas_figura.draw()

        # Colocar el lienzo en el canvas de tkinter
        self.canvas_figura.get_tk_widget().pack(fill= BOTH, expand=True)

    def enviarDatos(self):
        # Aquí se pueden tomar los valores de los campos, BORRAR CANTIDAD DE POLVORA
        direction_local = self.direction_input.get()
        numeroslices = self.numero_slices.get()
        prompt_usuario = self.input_prompt_usuario.get("1.0", END)
        ruta_imagen_local = self.archivo
        imagen_codificada = self.encode_local_image(ruta_imagen_local)

        self.consola.insert(END, f"The direction introduced is: {direction_local} \n")
        self.consola.insert(END, f"The number of slices introduced is: {numeroslices} \n")
        self.consola.insert(END, f"Image uploaded from file: {self.archivo} \n")
        self.consola.insert(END, f"Loading... \n")
        self.consola.update()


        #Enviamos datos a Chat GPT y nos guardamos la respuesta en response
        self.response = api_handler.send_data(numeroslices, imagen_codificada,direction_local,prompt_usuario)

        self.consola.insert(END, f"{self.response[1]}\n")
        self.consola.update()
        self.pintargrafica(self.response[1],self.canvas_right)


    def limpiarDatos(self):
        self.direction_input.delete(0, END)
        self.numero_slices.delete(0, END)
        self.canvas.delete("all")
        self.consola.delete(1.0, END)
        self.input_prompt_usuario.delete("1.0", END)
        self.canvas_right.delete("all")
        self.canvas_figura.get_tk_widget().destroy()



    def cargarImagen(self):

        # Abrir un cuadro de diálogo para seleccionar un archivo de imagen
        self.archivo = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg;")])

        if self.archivo:
            # Abrir la imagen con PIL
            imagen = Image.open(self.archivo)
            imagen.thumbnail((200, 200))  # Redimensionar la imagen para ajustarla al tamaño del canvas
            self.image_in_memory = ImageTk.PhotoImage(imagen)

            # Colocar la imagen en el canvas
            self.canvas.create_image(100, 100, image=self.image_in_memory)
            self.canvas.update()

    def encode_local_image(self, ruta_imagen_local):
        with open(ruta_imagen_local, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')



    def dividirLadoDerecho(self):

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Crear dos frames, uno arriba y otro debajo, con las proporciones deseadas
        top_height = int(screen_height * 0.5)  # 70% de la altura
        bottom_height = int(screen_height * 0.5)  # 30% de la altura

        # Creamos dos frames, uno arriba y otro debajo
        self.top_frame = Frame(self.right_frame, bg="white", height= top_height)
        self.top_frame.place(x=0, y=0, width=screen_width // 2, height=top_height)

        self.bottom_frame = Frame(self.right_frame, bg="white",height= bottom_height)
        self.bottom_frame.place(x=0, y=top_height, width=screen_width // 2, height=bottom_height)

        # Crear un canvas donde se pueda representar la imagen
        self.canvas_right = Canvas(self.top_frame, bg="white", width=screen_width // 2)
        self.canvas_right.pack(side=TOP,fill= BOTH, padx=2, expand=True)

        #Parte de abajo, output de la consola. La altura es la mitad de la pantalla
        self.consola = Text(self.bottom_frame, bg="black", fg="white", wrap=WORD, height= self.root.winfo_screenheight() // 2)
        self.consola.pack(fill= BOTH, padx=2)


