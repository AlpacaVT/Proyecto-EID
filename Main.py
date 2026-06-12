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

        caja = ctk.CTkTextbox(self.tab_inicio, width=900, height=600, font=("Arial", 16))
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
            es_infinito_pos = (str_h.strip() == "oo")
            es_infinito_neg = (str_h.strip() == "-oo")
            es_infinito = es_infinito_pos or es_infinito_neg

            if es_infinito:
                # Si tiende al infinito, x toma valores cada vez más grandes en magnitud
                pasos_infinitos = [10, 100, 1000, 10000, 100000]
                h_imprimible = "+oo" if es_infinito_pos else "-oo"
                self.txt_resultado.insert("end", f"Evaluando tendencia hacia h = {h_imprimible}\n")
                self.txt_resultado.insert("end", f"{'Dirección':<12} | {'x':<12} | {'f(x)':<15}\n")
                self.txt_resultado.insert("end", "-" * 48 + "\n")
                
                limite_final = None
                for paso in pasos_infinitos:
                    # Si es -oo, multiplicamos por -1 para ir hacia la izquierda en el eje X
                    x_eval = paso if es_infinito_pos else -paso
                    y_eval = expresion.subs(x, x_eval).evalf()
                    limite_final = float(y_eval)
                    
                    dir_texto = "Tendencia (+)" if es_infinito_pos else "Tendencia (-)"
                    self.txt_resultado.insert("end", f"{dir_texto:<12} | {x_eval:<12} | {limite_final:<15.6f}\n")
                
                # Asumimos que el último valor de la secuencia es el límite L
                L = round(limite_final, 4)
                self.resultado_final.configure(text=f"Límite L = {L}", text_color="#22c55e")
            else:
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

            # Genera un rango de x con listas nativas en un entorno a [h - 4, h + 4]
            puntos_x = []
            puntos_y = []
            pasos = 200
            # Cambia el rango de X
            if es_infinito:
                if es_infinito_pos:
                    inicio_rango = 0
                    fin_rango = 100  # Muestra el comportamiento hacia la derecha de la gráfica
                else:
                    inicio_rango = -100 # Muestra el comportamiento hacia la izquierda de la gráfica
                    fin_rango = 0
            else:
                inicio_rango = h - 10
                fin_rango = h + 10

            ancho_paso = (fin_rango - inicio_rango) / pasos

            # ciclo para calcular las cordenadas
            for i in range(pasos + 1):
                cur_x = inicio_rango + (i * ancho_paso)
                # se evita evaluar directameente
                if not es_infinito and abs(cur_x - h) < 1e-6:
                    continue
                try:
                    cur_y = float(expresion.subs(x, cur_x).evalf())
                    # Controlamos que no se grafiquen valores infinitos que rompan el tamaño
                    if abs(cur_y) < 1000:
                        puntos_x.append(cur_x)
                        puntos_y.append(cur_y)
                except Exception:
                    pass # Si hay algún error de dominio matemático, salta el punto

            # Grafica
            self.eje.plot(puntos_x, puntos_y, color='#1f77b4', linewidth=2.5, label=f"f(x) = {str_fx}")

            if es_infinito:
                # Si el límite al infinito existe, dibuja una asíntota horizontal en Y = L
                self.eje.axhline(y=0, color='red', linestyle='--', alpha=0.6, label=f"Asín. Horiz. y = {L}")
            else:
                # Remarca el punto h en el eje X
                self.eje.axvline(x=h, color='red', linestyle='--', alpha=0.6, label=f"x = {h}")
            
            # Configuraciones de estilo para el gráfico
            self.eje.grid(True, color='#444444', linestyle=':')
            self.eje.tick_params(colors='white')
            self.eje.legend(loc="upper right")
            
            # Forza la actualización del grafico
            self.canvas.draw()

        except Exception as err:
            # en caso de error
            self.resultado_final.configure(text="error de cálculo", text_color="red")
            self.txt_resultado.insert("end", f"\n[ERROR]: {str(err)}\nRevise que ingreso datos correctos (ej: 2*x en vez de 2x).")
        
        # Deshabilita la caja para que el usuario no edite los números generados
        self.txt_resultado.configure(state="disabled")

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
        panel.pack(side="right", fill="x", padx=10, pady=10)

        grafico = ctk.CTkFrame(contenedor)
        grafico.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(panel, text="Limite Lateral", font=("Arial", 22, "bold")).pack(pady=5)

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



