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
        # self.crear_infinito()

    # ========================================================
    # PESTAÑA DE INICIO
    # ========================================================

    def crear_inicio(self):
        titulo = ctk.CTkLabel(
            self.tab_inicio,
            text="Projecto Limites",
            font=("Arial", 50, "bold")
        )
        titulo.pack(pady=60, padx=30)

        texto = """
            Esta aplicación fue desarrollada con:\n
            • customtkinter  → interfaz gráfica moderna\n
            • sympy          → cálculo simbólico de límites\n
            • matplotlib     → visualización de funciones\n\n
            Funcionalidades:\n
            ✔ Ingresar una función f(x)\n
            ✔ Calcular el límite en un punto\n
            ✔ Graficar la función\n
            ✔ Mostrar el resultado"""

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
        figura.patch.set_facecolor('#242424')
        eje = figura.add_subplot(111)
        eje.set_facecolor('#1a1a1a')          
        eje.tick_params(colors='white')
        
        canvas = FigureCanvasTkAgg(figura, master=frame)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        return figura, eje, canvas

#======================================
#LIMITE ESTANDAR
#======================================

    def crear_limite(self):
        # Configuramos una cuadrícula en la pestaña para dividir controles y gráfico
        self.tab_limite.grid_columnconfigure(0, weight=4) #izquierda
        self.tab_limite.grid_columnconfigure(1, weight=1) #derecha
        self.tab_limite.grid_rowconfigure(0, weight=1)

        # ---- COLUMNA DERECHA ----
        contenedor_datos = ctk.CTkFrame(self.tab_limite)
        contenedor_datos.grid(row=0, column=1, padx=0, pady=15, sticky="nsew")

        titulo = ctk.CTkLabel(contenedor_datos, text="Menu de Datos", font=("Arial", 22, "bold"))
        titulo.pack(pady=15)

        # Menu de datos
        titulo_fx = ctk.CTkLabel(contenedor_datos, text="Ingrese la función:  Ej: (x**2 - 4)/(x - 2) o sin(x)/x)", font=("Arial", 14))
        titulo_fx.pack(pady=(10, 2))
        self.entrada_fx = ctk.CTkEntry(contenedor_datos, width=250, placeholder_text="f(x)")
        self.entrada_fx.pack(pady=5)

        titulo_h = ctk.CTkLabel(contenedor_datos, text="Ingrese el valor al que tiene x:", font=("Arial", 14))
        titulo_h.pack(pady=(10, 2))
        self.entrada_h = ctk.CTkEntry(contenedor_datos, width=250, placeholder_text="h")
        self.entrada_h.pack(pady=5)

        # Botón de Acción
        self.btn_calcular = ctk.CTkButton(contenedor_datos, text="Calcular y Graficar", command=self.procesar_limite, font=("Arial", 14, "bold"))
        self.btn_calcular.pack(pady=25)

        # Área para mostrar los resultados
        titulo_resultado = ctk.CTkLabel(contenedor_datos, text="Desarrollo:", font=("Arial", 15, "bold"))
        titulo_resultado.pack(pady=(10, 2))

        self.txt_resultado = ctk.CTkTextbox(contenedor_datos, width=350, height=220, font=("Consolas", 12))
        self.txt_resultado.pack(padx=0, pady=5)
        
        # Etiqueta destacada para el resultado final
        self.resultado_final = ctk.CTkLabel(contenedor_datos, text="Límite L = ", font=("Arial", 18, "bold"), text_color="#1f538d")
        self.resultado_final.pack(pady=15)

        # ---- COLUMNA IZQUIERDA ----
        self.grafico = ctk.CTkFrame(self.tab_limite)
        self.grafico.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")
        
        # se inicia el espacio del gráfico usando la función auxiliar
        self.figura, self.eje, self.canvas = self.crea_grafico(self.grafico)

    # ========================================================
    # evaluacion del limite
    # ========================================================

    def procesar_limite(self):
        # Habilitar caja de texto para escribir
        self.txt_resultado.configure(state="normal")
        self.txt_resultado.delete("1.0", "end")

        try:
            # Obtiene los datos
            str_fx = self.entrada_fx.get()
            str_h = self.entrada_h.get()

            if not str_fx or not str_h:
                self.resultado_final.configure(text="Error: Rellene todos los campos", text_color="red")
                return

            # Variable simbolica definida
            x = sp.symbols('x')
            
            # Convertir el string en una expresión matemática que pueda leer sympy
            expresion = sp.sympify(str_fx)
            
            # Convertir el valor h a flotante
            h = float(sp.sympify(str_h).evalf())

            # DESARROLLO ALGORÍTMICO
            self.txt_resultado.insert("end", f"Evaluando entorno alrededor de h = {h}\n")
            self.txt_resultado.insert("end", f"{'Dirección':<12} | {'x':<12} | {'f(x)':<15}\n")
            self.txt_resultado.insert("end", "-" * 48 + "\n")

            # Definimos distancias cercanas h (10^-1, 10^-2, 10^-3, ...) 
            distancias = [0.1, 0.01, 0.001, 0.0001, 0.00001]
            
            limite_izq = None
            limite_der = None

            # Evaluacion por la izquierda (x -> h-)
            for d in distancias:
                x_eval = h - d
                # Se usa subs solo para sustituir :V y evalf para aproximar
                y_eval = expresion.subs(x, x_eval).evalf()
                limite_izq = float(y_eval)
                self.txt_resultado.insert("end", f"Izquierda (-) | {x_eval:<12.5f} | {limite_izq:<15.6f}\n")

            self.txt_resultado.insert("end", "-" * 48 + "\n")

            # Evaluacion por la derecha (x -> h+)
            for d in distancias:
                x_eval = h + d
                y_eval = expresion.subs(x, x_eval).evalf()
                limite_der = float(y_eval)
                self.txt_resultado.insert("end", f"Derecha   (+) | {x_eval:<12.5f} | {limite_der:<15.6f}\n")

            # 3. Validación lógica del Límite 
            # Si la diferencia entre aproximarse por izquierda y derecha es minúscula, el límite existe 
            if abs(limite_izq - limite_der) < 1e-4:
                # Redondeamos el resultado para mostrar el entero o valor representativo
                L = round(limite_izq, 4)
                self.resultado_final.configure(text=f"Límite L = {L}", text_color="#22c55e") # Verde éxito
            else:
                self.resultado_final.configure(text="El límite No Existe (L. Laterales distintos)", text_color="orange")

            # carga la grafica
            self.eje.clear() # Limpia el gráfico anterior
            self.eje.set_facecolor('#1a1a1a') # Mantiene el tema oscuro

            # Genera un rango de x con listas nativas en un entorno de [h - 4, h + 4]
            puntos_x = []
            puntos_y = []
            pasos = 200
            inicio_rango = h - 10
            fin_rango = h + 10
            ancho_paso = (fin_rango - inicio_rango) / pasos

            # ciclo para calcular las cordenadas
            for i in range(pasos + 1):
                cur_x = inicio_rango + (i * ancho_paso)
                # se evita evaluar directameente
                if abs(cur_x - h) < 1e-6:
                    continue
                try:
                    cur_y = float(expresion.subs(x, cur_x).evalf())
                    # Controlamos que no se grafiquen valores infinitos que rompan la escala
                    if abs(cur_y) < 1000:
                        puntos_x.append(cur_x)
                        puntos_y.append(cur_y)
                except Exception:
                    pass # Si hay algún error de dominio matemático, salta el punto

            # Grafica
            self.eje.plot(puntos_x, puntos_y, color='#1f77b4', linewidth=2.5, label=f"f(x) = {str_fx}")
            
            # Remarcar punto h en el eje X
            self.eje.axvline(x=h, color='red', linestyle='--', alpha=0.6, label=f"x = {h}")
            
            # Configuraciones de estilo para el gráfico
            self.eje.grid(True, color='#444444', linestyle=':')
            self.eje.tick_params(colors='white')
            self.eje.legend(loc="upper right")
            
            # Forza la actualización del grafico
            self.canvas.draw()

        except Exception as err:
            # Captura de errores de sintaxis matemática o división imprevista 
            self.resultado_final.configure(text="error de cálculo", text_color="red")
            self.txt_resultado.insert("end", f"\n[ERROR]: {str(err)}\nRevise que ingreso datos correctos (ej: 2*x en vez de 2x).")
        
        # Deshabilitar caja para que el usuario no edite los números generados
        self.txt_resultado.configure(state="disabled")


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

        panel = ctk.CTkFrame(contenedor)
        panel.pack(side="right", fill="x", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Limite Lateral", font=("Arial", 24, "bold")).pack(pady=15)

        ctk.CTkLabel(panel, text="Funcion f(x):").pack()
        self.lat_fx = ctk.CTkEntry(panel, placeholder_text="Ej: x**2 + 4")
        self.lat_fx.pack(pady=5)

        ctk.CTkLabel(panel, text="Valor de h(x-->h)").pack()
        self.lat_h = ctk.CTkEntry(panel, placeholder_text="Ej: 4")
        self.lat_h.pack(pady=5)

        ctk.CTkButton(
            panel,
            text="Calcular",
            command=self.graficar_lateral
        ).pack(pady=20)

        self.resultado_lateral = ctk.CTkTextbox(panel, width=310, height=350)
        self.resultado_lateral.pack(pady=10)

        self.fig_lat, self.ax_lat, self.canvas_lat = self.crea_grafico(grafico)


    def graficar_lateral(self):
        try:
            fx = self.lat_fx.get() #lee lo que el usuario coloca en fx
            h = self.lat_h.get() #lee lo que el usuario coloca en h

            # Evita que no se ingrese nada
            if not h or not fx: #verifica si esta vacia h y fx
                self.resultado_lateral.delete("1.0", "end") #borra todo lo que hay escrito antes
                self.resultado_lateral.insert("1.0", "Ingresa los datos.") #escribe el texto nuevo desde el principio
                return
            # el "1.0" se usa para escribir texto al principio
            x = sp.Symbol('x') #convierte a x en una variable matematica
            expr = sp.sympify(fx) #convierte el texto fx en una expresion
            evaluacion_fx = expr.subs(x, sp.sympify(h)) #evaluacion de la funcion para saber si calcular los laterales
            lim_izq = sp.limit(expr, x, h, '-') #calcular limite cuando se hacerque por -
            lim_der = sp.limit(expr, x, h, '+') #calcular limite cuando se hacerque por +
            h_num = float(sp.sympify(h))

            try: # es número normal, el límite existe
                verifi = float(evaluacion_fx) #verificador de indeterminacion(la indeterminacion no puede ser float)
                self.resultado_lateral.delete("1.0", "end")
                self.resultado_lateral.insert("1.0", "el limite se encuentra en: " + str(evaluacion_fx))

            except: #hay indeterminación o división por cero, calcular laterales
                if lim_der == lim_izq: # verifica si los limites laterales son iguales
                    self.resultado_lateral.delete("1.0", "end")
                    self.resultado_lateral.insert("1.0", "el limite se encuentra en: " + str(lim_der))
                    # si los laterales son iguales es igual existe en el numero lim_der(ya que son iguales no hay problema)

                else: #si los limites laterales no son iguales
                    self.resultado_lateral.delete("1.0", "end")
                    self.resultado_lateral.insert("1.0", "el limite no existe")
                    self.resultado_lateral.insert("end", "\nlimite por la derecha: " + str(lim_der))
                    self.resultado_lateral.insert("end", "\nlimite por la izquierda: " + str(lim_izq))
                    # "end" al principio se usa para agregar al final
        except Exception as error:
            self.resultado_lateral.delete("1.0", "end")
            self.resultado_lateral.insert("1.0", "Error en los datos ingresados:\n" + str(error))
#======================================
#LIMITE INFINITO
#======================================

if __name__ == "__main__":
    app = App()
    app.mainloop()