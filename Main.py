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

    def crear_inicio(self):
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

#======================================
#LIMITE
#======================================

    def crear_limite(self):
        contenedor = ctk.CTkFrame(self.tab_limite)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        
        menu_datos = ctk.CTkFrame(contenedor, width=200, height=200)
        menu_datos.pack(side= "bottom", fill="both", padx=10, pady= 10)
        
        grafica = ctk.CTkFrame(contenedor)
        grafica.pack(side="top", fill="both", expand= True)

        ctk.CTkLabel(menu_datos, "Limites", font=("Arial", 30, "bold") )
        
        ctk.CTkLabel(menu_datos, text="x --> ").pack()
        self.c_h = ctk.CTkEntry(menu_datos, placeholder_text="Ej: x --> 0")
        self.c_h.pack(pady=5)

        ctk.CTkLabel(menu_datos, text="f(x):").pack()
        self.c_k = ctk.CTkEntry(menu_datos, placeholder_text="Ej: x**2 - 4")
        self.c_k.pack(pady=5)


        ctk.CTkButton(
            menu_datos,
            text="Graficar y explicar",
            command=self.graficar_limite
        ).pack(pady=20)

    def mostrar_texto(self, caja, texto):
        caja.configure(state="normal")
        caja.delete("1.0", "end")
        caja.insert("1.0", texto)
        caja.configure(state="disabled")

#======================================
#LIMITE LATERAL
#======================================

    def crear_lateral(self):
        contenedor = ctk.CTkFrame(self.tab_lateral)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        panel = ctk.CTkFrame(contenedor, width=340)
        panel.pack(side="left", fill="y", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Limite Lateral", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Funcion f(x):").pack()
        self.lat_fx = ctk.CTkEntry(panel, placeholder_text="Ej: x**2 + 4")
        self.lat_fx.pack(pady=5)

        ctk.CTkLabel(panel, text="Valor de h(x-->h)").pack()
        self.lat_h = ctk.CTkEntry(panel, placeholder_text="Ej: 4")
        self.lat_h.pack(pady=5)

        ctk.CTkButton(
            panel,
            text="Graficar y explicar",
            command=self.graficar_lateral
        ).pack(pady=20)

        self.resultado_lateral = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_lateral.pack(pady=10)

        self.fig_lat, self.ax_lat, self.canvas_lat = self.crea_grafico(grafico)


    def graficar_lateral(self):
        fX = self.lat_fx.get()
        h = float(self.lat_h.get())

        
#======================================
#LIMITE INFINITO
#======================================