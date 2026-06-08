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
        # self.crear_lateral()
        # self.crear_infinito()

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

    def crea_grafico(self, frame):
        figura = Figure(figsize=(6, 5), dpi=100)
        
        figura.patch.set_facecolor('#242424')
        eje = figura.add_subplot(111)
        eje.set_facecolor('#1a1a1a')          
        eje.tick_params(colors='white')
        
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

    #======================================
    # LIMITE
    #======================================

    def crear_limite(self):
        contenedor = ctk.CTkFrame(self.tab_limite)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)
        
        menu_datos = ctk.CTkFrame(contenedor, width=200, height=200)
        menu_datos.pack(side="bottom", fill="both", padx=10, pady=10)
        
        grafica = ctk.CTkFrame(contenedor)
        grafica.pack(side="top", fill="both", expand=True)

        ctk.CTkLabel(menu_datos, text="Límites", font=("Arial", 22, "bold")).pack(pady=5)
        
        ctk.CTkLabel(menu_datos, text="x --> ").pack()
        self.x = ctk.CTkEntry(menu_datos, placeholder_text="Ej: 0 o 2")
        self.x.pack(pady=5)

        ctk.CTkLabel(menu_datos, text="f(x):").pack()
        self.fx = ctk.CTkEntry(menu_datos, placeholder_text="Ej: x**2 - 4")
        self.fx.pack(pady=5)

        ctk.CTkLabel(menu_datos, text="Explicación paso a paso:").pack(pady=2)
        self.caja_explicacion = ctk.CTkTextbox(menu_datos, width=700, height=80, font=("Arial", 13))
        self.caja_explicacion.pack(pady=5)
        self.caja_explicacion.configure(state="disabled")

        self.figura, self.eje, self.canvas = self.crea_grafico(grafica)
        
        ctk.CTkButton(
            menu_datos,
            text="Graficar",
            command=self.graficar_limite
        ).pack(pady=20)

    def graficar_limite(self):
        try:
            tendencia = self.x.get()
            funcion = self.fx.get()

            # Evita que no se ingrese nada
            if not tendencia or not funcion:
                self.mostrar_texto(self.caja_explicacion, "Ingresa los datos.")
                return

            # Definimos la variable x en SymPy
            x = sp.Symbol('x')

            # Se traducen los datos a datos que SymPy pueda leer
            tendencia_trad = sp.sympify(tendencia)
            fx = sp.sympify(funcion)

            # Calcula el limite usando la funcion ingresada y la tendencia de X
            resultado = sp.limit(fx, x, tendencia_trad)

            #Genera los puntos para ingresar en la grafica
            intervalo = float(tendencia_trad.evalf())
            
            puntos_x = []
            puntos_y = []
            
            evaluaciones = 200
            rango_min = intervalo - 5
            rango_max = intervalo + 5
            c_evaluaciones = (rango_max - rango_min) / evaluaciones

            for i in range(evaluaciones):
                valor_x = rango_min + (i * c_evaluaciones)
                try:
                    valor_y = float(fx.subs(x, valor_x).evalf())
                    # Se evitan valores muy grandes
                    if abs(valor_y) < 1000:
                        puntos_x.append(valor_x)
                        puntos_y.append(valor_y)
                except:
                    continue


            self.eje.clear() # Limpia la grafica anterior
            
            # Se genera la grafica
            self.eje.plot(puntos_x, puntos_y, label=f"f(x) = {funcion}", color="#1500ff", linewidth=2)
            
            # Si el límite es un resultado valido, dibujamos el punto de aproximación
            if resultado.is_number:
                valor_y_limite = float(resultado.evalf())
                # se dibuja un punto rojo en el plano donde se intersecta el límite
                self.eje.plot(intervalo, valor_y_limite, 'ro', markersize=8, label=f"Límite = {resultado}")
                self.eje.axhline(valor_y_limite, color='gray', linestyle='--', linewidth=0.7)
                self.eje.axvline(intervalo, color='gray', linestyle='--', linewidth=0.7)

            # Colores de la grafica matplotlib
            self.eje.axhline(0, color='white', linewidth=0.5)
            self.eje.axvline(0, color='white', linewidth=0.5)
            self.eje.grid(True, linestyle=':', color='gray', alpha=0.5)
            self.eje.legend(loc="upper right")
            
            self.canvas.draw()

            # --- MOSTRAR EXPLICACIÓN PASO A PASO ---
            texto_explicativo = f"1. Se identificó la función ingresada f(x) = {fx}\n"
            texto_explicativo += f"2. Evaluando cuando X tiende a {tendencia_trad}\n"
            
            sustitucion_directa = fx.subs(x, tendencia_trad)
            if sustitucion_directa == sp.nan or "0/0" in str(sustitucion_directa):
                texto_explicativo += f"3. La sustitución directa genera una indeterminación por lo que se evaluara con aproximaciones a {tendencia_trad}.\n"
            else:
                texto_explicativo += f"3. Se realizó la evaluación.\n"
                
            texto_explicativo += f"El limite es {resultado}"

            self.mostrar_texto(self.caja_explicacion, texto_explicativo)

        except Exception as error:
            self.mostrar_texto(self.caja_explicacion, f"Error en los datos ingresados:\n{str(error)}")


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