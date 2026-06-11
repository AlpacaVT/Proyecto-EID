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

#======================================
# FUNCION AUXILIAR
# para mostrar Texto personalizado para los limites
#======================================
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
        contenedor.pack(fill="both", expand=True)

        panel = ctk.CTkFrame(contenedor)
        panel.pack(side="bottom", fill="x", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Limite Lateral", font=("Arial", 22, "bold")).pack(pady=5)

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

        self.resultado_lateral = ctk.CTkTextbox(panel, width=500, height=105, state="disabled")
        self.resultado_lateral.pack(pady=10)

        self.fig_lat, self.ax_lat, self.canvas_lat = self.crea_grafico(grafico)


    def graficar_lateral(self):
        try:
            fx = self.lat_fx.get() #lee lo que el usuario coloca en fx
            h = self.lat_h.get() #lee lo que el usuario coloca en h

            #Evita que no se ingrese nada
            if not h or not fx: #verifica si esta vacia h y fx
                self.mostrar_texto(self.resultado_lateral, "Ingresa los datos.")
                return
            #el "1.0" se usa para escribir texto al principio
            x = sp.Symbol('x') #convierte a x en una variable matematica
            expr = sp.sympify(fx) #convierte el texto fx en una expresion
            evaluacion_fx = expr.subs(x, sp.sympify(h)) #evaluacion de la funcion para saber si calcular los laterales
            lim_izq = sp.limit(expr, x, h, '-') #calcular limite cuando se hacerque por -
            lim_der = sp.limit(expr, x, h, '+') #calcular limite cuando se hacerque por +
            h_numero = float(sp.sympify(h))

            puntos_x = [] #lista para guardar los valores de x
            puntos_y = [] #lista para guardar los valores de f(x)

            evaluaciones = 200 #cantidad de puntos a calcular
            rango_min = h_numero - 5 #inicio del grafico (5 unidades antes de h)
            rango_max = h_numero + 5 #fin del grafico (5 unidades despues de h)
            c_evaluaciones = (rango_max - rango_min) / evaluaciones #espacio entre cada punto

            for i in range(evaluaciones): #recorre los 200 puntos
                valor_x = rango_min + (i * c_evaluaciones) #calcula el valor de x para este punto
                try:
                    valor_y = float(expr.subs(x, valor_x).evalf()) #evalua f(x) en ese punto
                    if abs(valor_y) < 1000: #evita valores muy grandes que distorsionen el grafico
                        puntos_x.append(valor_x) #guarda el valor de x
                        puntos_y.append(valor_y) #guarda el valor de f(x)
                except:
                    continue #si hay error en un punto, salta y sigue con el siguiente
            
            self.ax_lat.clear()
            self.ax_lat.plot(puntos_x, puntos_y, label=f"f(x) = {fx}", color="#1500ff", linewidth=2)
            self.ax_lat.axhline(0, color='white', linewidth=0.5)
            self.ax_lat.axvline(0, color='white', linewidth=0.5)
            self.ax_lat.grid(True, linestyle=':', color='gray', alpha=0.5)
            self.ax_lat.legend(loc="upper right")
            self.canvas_lat.draw()

            try: #es número normal, el límite existe
                verifi = float(evaluacion_fx) #verificador de indeterminacion(la indeterminacion no puede ser float)
                if verifi != verifi:  # nan es el único número que no es igual a sí mismo
                    raise ValueError("nan")

                texto = f"1. Función ingresada: f(x) = {fx}\n" 
                texto += f"2. X tiende a: {h}\n"
                texto += f"3. Evaluación directa f({h}) = {evaluacion_fx}\n"
                texto += f"4. La función está definida en h\n"
                texto += f"5. El límite existe en: {evaluacion_fx}"
                self.mostrar_texto(self.resultado_lateral, texto)

                if evaluacion_fx.is_number:
                    valor_y_limite = float(evaluacion_fx.evalf())
                    self.ax_lat.plot(h_numero, valor_y_limite, 'ro', markersize=8, label=f"Límite = {evaluacion_fx}")
                    self.ax_lat.axhline(valor_y_limite, color='gray', linestyle='--', linewidth=0.7)
                    self.ax_lat.axvline(h_numero, color='gray', linestyle='--', linewidth=0.7)
                    self.canvas_lat.draw()

            except: #hay indeterminación o división por cero, calcular laterales

                numerador = sp.numer(evaluacion_fx) #ve cual es el nummerador de la evaluacion de fx
                tipo_indet = "0/0" if numerador == 0 else "k/0" #identifica que tipo de Indeterminacion es

                if lim_der == lim_izq: # verifica si los limites laterales son iguales
                    texto = f"1. Función ingresada: f(x) = {fx}\n"
                    texto += f"2. X tiende a: {h}\n"
                    texto += f"3. Evaluación directa: indeterminación detectada ({tipo_indet})\n"
                    texto += f"4. Límite por izquierda (x → {h}⁻): {lim_izq}\n"
                    texto += f"5. Límite por derecha (x → {h}⁺): {lim_der}\n"
                    texto += f"6. L⁻ = L⁺ → El límite existe en: {lim_der}"
                    self.mostrar_texto(self.resultado_lateral, texto)
                    #si los laterales son iguales es igual existe en el numero lim_der(ya que son iguales no hay problema)

                    if lim_der.is_number:
                        valor_y_limite = float(lim_der.evalf())
                        self.ax_lat.plot(h_numero, valor_y_limite, 'ro', markersize=8, label=f"Límite = {lim_der}")
                        self.ax_lat.axhline(valor_y_limite, color='gray', linestyle='--', linewidth=0.7)
                        self.ax_lat.axvline(h_numero, color='gray', linestyle='--', linewidth=0.7)
                        self.canvas_lat.draw()

                else: #si los limites laterales no son iguales
                    texto = f"1. Función ingresada: f(x) = {fx}\n"
                    texto += f"2. X tiende a: {h}\n"
                    texto += f"3. Evaluación directa: indeterminación detectada ({tipo_indet})\n"
                    texto += f"4. Límite por izquierda (x → {h}⁻): {lim_izq}\n"
                    texto += f"5. Límite por derecha (x → {h}⁺): {lim_der}\n"
                    texto += f"6. L⁻ ≠ L⁺ → El límite no existe"
                    self.mostrar_texto(self.resultado_lateral, texto)
                    #"end" al principio se usa para agregar al final

        except Exception as error:
            self.mostrar_texto(self.resultado_lateral, "Error en los datos ingresados:\n" + str(error))

#======================================
#LIMITE INFINITO
#======================================

    def crear_infinito(self):
        contenedor = ctk.CTkFrame(self.tab_infinito)
        contenedor.pack(fill="both", expand=True, padx=10, pady=10)

        menu_datos = ctk.CTkFrame(contenedor, width=200, height=200)
        menu_datos.pack(side="bottom", fill="both", padx=10, pady=10)

        grafica = ctk.CTkFrame(contenedor)
        grafica.pack(side="top", fill="both", expand=True)

        ctk.CTkLabel(menu_datos, text="limites al infinito", font=("arial", 22, "bold")).pack(pady=5)

        ctk.CTkLabel(menu_datos, text="tendencia (∞ o -∞):").pack()
        self.x_inf = ctk.CTkEntry(menu_datos, placeholder_text="oo o -oo")
        self.x_inf.pack(pady=5)

        ctk.CTkLabel(menu_datos, text="f(x):").pack()
        self.fx_inf = ctk.CTkEntry(menu_datos, placeholder_text="Ej: (2*x)/x")
        self.fx_inf.pack(pady=5)

        ctk.CTkLabel(menu_datos, text="Explicación:").pack(pady=2)
        self.caja_explicacion_inf = ctk.CTkTextbox(menu_datos, width=700, height=80, font=("arial", 13))
        self.caja_explicacion_inf.pack(pady=5)
        self.caja_explicacion_inf.configure(state="disabled")

        self.figura_inf, self.eje_inf, self.canvas_inf = self.crea_grafico(grafica)

        ctk.CTkButton(
            menu_datos,
            text="calcular y graficar",
            command=self.graficar_infinito
        ).pack(pady=10)

    def graficar_infinito(self):
        try:
            # Captura de datos desde la interfaz
            tendencia = self.x_inf.get() #Rescata el texto de la tendencia (oo o -oo)
            funcion = self.fx_inf.get() #rescata el string de la funcion ingresada

            #Validacion de datos incompletos 
            if not tendencia or not funcion: 
                self.mostrar_texto(self.caja_explicacion_inf, "ingresa los datos.")
                return #corta la ejecucion si falta alfun dato
            x = sp.symbols('x')#Define 'x' como la variable simbolica pra el calculo

            #traducimos la entrada de texto al objeto infinito de SymPy
            if tendencia == "oo":
                tendencia_trad = sp.oo #asigna el objeto de infinito poitivo "es una dolbe 'o'"
            elif tendencia == "-oo":
                tendencia_trad = -sp.oo # se asigna el mismo objeto pero con un "-" antes
            else: 
                #si el usuario escribe cyalquier otra cosa, avisa del error y detiene el proceso
                self.mostrar_texto(self.caja_explicacion_inf, "Para infinito usa exactamente 'oo' o '-oo'.")
                return
            fx = sp.sympify(funcion) #traduce el string de la funcion a una exprecion matematica
            resultado = sp.limit(fx, x, tendencia_trad) # calcula el limite exacto

            # Graficamos un rango amplio fijo (de -50 a 50) para apreciar el comportamiento asintotico 
            puntos_x = []
            puntos_y = []
            for i in range(-50,51):
                try:
                    valor_y = float(fx.subs(x, i).evalf()) # Remplaza 'x' por el valor de 'i' y lo evalua decimal
                    if abs(valor_y) < 100: #acota los valores para evitar desbordes por asintotas verticales 
                        puntos_x.append(i) #guarda el valor en x si pasa el flitro
                        puntos_y.append(valor_y) #guarda el valor calculado de y
                except:
                    continue # si hay una division por cero en ese punto, ignora el error y salta al siguiente 
                # Renderiza el grafico en matplotlib
            self.eje_inf.clear()
            self.eje_inf.plot(puntos_x, puntos_y, label=f"f(x) = {funcion}", color="#1500ff",linewidth=2) # Dibuja la curva principar de la funcion uniendo los puntos con una linea azul

            # si el limite da un numero estable, se dibuja la asintota horizontal
            if resultado.is_number:
                asintota = float(resultado.evalf()) #convierte el resultado del el limite a un valor decimal flotante 
                self.eje_inf.axhline(asintota, color='red', linestyle=':', label=f"Asintota y = {resultado}") # traza una linea horiontal punteada de color rojo en el valor donde convegue la funcion

            self.eje_inf.axhline(0, color='white', linewidth=0.5) #dibuja el eje x
            self.eje_inf.axvline(0, color='white', linewidth=0.5) #dibuja el eje y
            self.eje_inf.grid(True, linestyle=':', color='gray', alpha=0.5)# activa una cuadricula gris 
            self.eje_inf.legend(loc="upper right") #coloca el cuadro de etiquetas/leyendas arriba a la derecha 
            self.canvas_inf.draw() #refresca fisicamente el liezo de la interfaz grafica

            #envia el resultado textual de la operacion limpia a la caja de texto
            self.mostrar_texto(self.caja_explicacion_inf, f"Analizando comportamiento en tendencias extremas hacia {tendencia}. \nResultado del limite:{resultado}")
        except Exception as error:
            #si el usuario ingresa un error de sintaxisa se captura la exepcion y la muestra 
            self.mostrar_texto(self.caja_explicacion_inf, f"Error:\n{str(error)}")

if __name__ == "__main__":
    app = App()
    app.mainloop()