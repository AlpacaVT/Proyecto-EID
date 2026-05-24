import customtkinter as ctk #Libreria que usaremos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sympy as sp


class App(ctk.CTk):

    def __init__(self):
        super().__init__()

        # Configuración básica de la ventana.
        self.title("Calculo de Limites")
        self.geometry("1200x720")

        # Apariencia visual de la aplicación.
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Permite que la ventana se adapte al tamaño disponible.
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # CTkTabview permite crear pestañas.
        self.tabs = ctk.CTkTabview(self)
        self.tabs.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Creación de pestañas.
        self.tab_inicio = self.tabs.add("Inicio")
        self.tab_limite = self.tabs.add("Limite")
        self.tab_lateral = self.tabs.add("L. Lateral")
        self.tab_infinito = self.tabs.add("L. Infinito")

        # Llamamos a los métodos que construyen cada pestaña.
        self.crear_inicio()
        self.crear_limite()
        self.crear_lateral()
        self.crear_infinito()

    # ========================================================
    # PESTAÑA DE INICIO
    # ========================================================

    def pest_inico(self):
        titulo = ctk.CTkLabel(
            self.tab_inicio,
            text="Projecto Limites",
            font=("Arial", 30, "bold")
        )
        titulo.pack(pady=25)

        texto = """

Usando conocimientos de librerias como matplotlib y otras librerias nuevas como customtkinter y sympy
se desarrollo esta aplicacion esta diseñada para :
- ingresar una función
- calcular límite
- graficar la función
- mostrar desarrollo paso a paso

"""

        caja = ctk.CTkTextbox(self.tab_inicio, width=900, height=350, font=("Arial", 16))
        caja.pack(pady=20)
        caja.insert("1.0", texto)
        caja.configure(state="disabled")

    # ========================================================
    # FUNCIÓN AUXILIAR PARA CREAR FIGURAS DE MATPLOTLIB
    # ========================================================
    # Esta función evita repetir código.
    # Crea una figura, un eje y un canvas para incrustar
    # el gráfico dentro de un frame de CustomTkinter.
    # ========================================================

    def crea_grafico(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        eje = figura.add_subplot(111)
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas
    