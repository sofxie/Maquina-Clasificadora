from tkinter import *
from tkinter import ttk
import os  # Necesario para verificar la existencia del archivo

class ventana:
    def __init__(self, size="1200x800", controlador=None ):
        self.size = size
        self.controlador = controlador
        self.margenes = {
            "peq": 0,
            "mid": 0,
            "max": 0
        }
        # Ruta del archivo de configuración de márgenes
        self.margenes_file = "margenes.txt"

        # Valores por defecto de los márgenes
        self.margenes = {"peq": 2, "mid": 6, "max": 17}

        # Cargar márgenes desde el archivo, si existe
        self.cargar_margenes()

    # Nueva ventana para modificar los márgenes
    def ventana_cambiar_margenes(self):
        margen_window = Toplevel()
        margen_window.title("Configurar Márgenes")
        margen_window.geometry("300x300")

    # Labels y entradas para los márgenes
        Label(margen_window, text="Pequeño:").pack(pady=5)
        peq_entry = Entry(margen_window)
        peq_entry.insert(0, self.margenes["peq"])
        peq_entry.pack()

        Label(margen_window, text="Mediano:").pack(pady=5)
        mid_entry = Entry(margen_window)
        mid_entry.insert(0, self.margenes["mid"])
        mid_entry.pack()

        Label(margen_window, text="Máximo (hasta 17 cm):").pack(pady=5)
        max_entry = Entry(margen_window)
        max_entry.insert(0, self.margenes["max"])
        max_entry.pack()

        # Función para guardar los márgenes
        def guardar():
            try:
        # Validar y guardar los nuevos valores
                peq = int(peq_entry.get())
                mid = int(mid_entry.get())
                maximo = int(max_entry.get())

                if 0 <= peq < mid <= maximo <= 17:
                    self.margenes["peq"] = peq
                    self.margenes["mid"] = mid
                    self.margenes["max"] = maximo
                    self.guardar_margenes()
                    margen_window.destroy()
                else:
                    Label(margen_window, text="¡Valores inválidos!", fg="red").pack()

            except ValueError:
                Label(margen_window, text="¡Introduce números válidos!", fg="red").pack()

        Button(margen_window, text="Guardar", command=guardar).pack(pady=20)

    # Método para cargar márgenes desde el archivo .txt
    def cargar_margenes(self):
        if os.path.exists(self.margenes_file):
            with open(self.margenes_file, "r") as file:
                for line in file:
                    clave, valor = line.strip().split("=")
                    if clave in self.margenes:
                        self.margenes[clave] = int(valor)

    # Método para guardar márgenes en el archivo .txt
    def guardar_margenes(self):
        with open(self.margenes_file, "w") as file:
            for clave, valor in self.margenes.items():
                file.write(f"{clave}={valor}\n")

    def resultado(self, estado, tamano):
        self.estado_text.set(f"{estado} {tamano}")

    def actualizarTabla(self, Tresultado, Promedio, Tabla):
        print(Promedio)
        if Tresultado:  # Actualiza resultados de tomates
            texto_tabla = (f"      {Tabla[0][2]}          {Tabla[1][2]}          {Tabla[2][2]}\n\n"
                           f"      {Tabla[0][1]}          {Tabla[1][1]}          {Tabla[2][1]}\n\n"
                           f"      {Tabla[0][0]}          {Tabla[1][0]}          {Tabla[2][0]}\n"
                           f"{Promedio:.2f} KG")
            self.tablaT_text.set(texto_tabla)
        else:
            texto_tabla = (
                f"          {Tabla[0]}           {Tabla[1]}\n\n"
                f"          {Tabla[2]}           {Tabla[3]}\n\n"
                f"{Promedio:.2f} KG")
            self.tablaP_text.set(texto_tabla)

    def mostrar(self):
        window = Tk()  # diseño de la ventana
        window.title("Sistema de Clasificacion")
        window.resizable(False, False)
        window.configure(background="#17820E")
        window.geometry(self.size)
        self.Tresultado = False  # Varible para procesar datos de papas o tomates, si es False es Papa, si es True es Tomate
        self.estado_text = StringVar()
        self.estado_text.set("") # Label que indica el estado del producto
        self.tablaT_text = StringVar()
        self.tablaT_text.set("")
        self.tablaP_text = StringVar()
        self.tablaP_text.set("")
        self.imagenTT = PhotoImage(file = "TablaResultadosT.png")
        self.imagenTP = PhotoImage(file = "TablaResultadosP.png")

        def analize():
            self.controlador.enviarmensaje(self.Tresultado,"color") # solicita el analisis

        def Pagina_resultado(): # Resultados
            wresult = Toplevel()
            wresult.geometry("1024x768")
            wresult.title("RESULTADOS")

            notebook = ttk.Notebook(wresult)

            tabtomates = Frame(notebook)
            tabpapas = Frame(notebook)

            notebook.add(tabtomates, text = "Resultado de Tomates")
            notebook.add(tabpapas,text = "Resultado de Papas")

            notebook.pack()

            tfondo = Canvas(tabtomates, width=1024, height=768)
            tfondo.create_image(510, 330,image=self.imagenTT)
            rtomate_label = tfondo.create_text(570, 440, text=self.tablaT_text.get(), fill= "black", font=("Arial", 50))
            tfondo.pack()

            tfondo.tag_raise(rtomate_label)

            def actualizar_texto_tomate(*args):
                tfondo.itemconfig(rtomate_label, text=self.tablaT_text.get())

            # Vincular la actualización a la variable self.tablaP_text
            self.tablaP_text.trace_add("write", actualizar_texto_tomate)

            cfondo = Canvas(tabpapas, width=1024, height=768)
            cfondo.create_image(510, 330, image=self.imagenTP)
            rpapa_label = cfondo.create_text(570, 465, text=self.tablaP_text.get(), fill= "black", font=("Arial", 60))
            cfondo.pack()

            cfondo.tag_raise(rpapa_label)

            # Actualizar el texto dinámico de papas
            def actualizar_texto_papas(*args):
                cfondo.itemconfig(rpapa_label, text=self.tablaP_text.get())

            # Vincular la actualización a la variable self.tablaP_text
            self.tablaP_text.trace_add("write", actualizar_texto_papas)

        def DarResultados():
            self.controlador.LAnalisisResultados(self.Tresultado)

        def validate_entry_lote(text):
            if len(text) > 14 :
                return False
            checks = []

            for i , char in enumerate(text):
                if i == 2:  # Solo permite un guion en la posición 2
                    checks.append(char == "-")
                elif i in (0, 1):  # Las primeras dos posiciones deben ser letras
                    checks.append(char.isalpha())
                    self.Tresultado = (char == "T")  # Actualiza Tresultado
                    self.controlador.actualizar_Tresultado(self.Tresultado)  # Notifica al controlador
                else:  # Las posiciones restantes deben ser números
                    checks.append(char.isdecimal())
            return all(checks)

        def validate_entry_peso(text):
            return text.isdecimal()

        def convert_to_uppercase(event):
            text = ELote.get().upper()  # Convierte el texto a mayúsculas
            ELote.delete(0, "end")  # Elimina el texto actual en el Entry
            ELote.insert(0, text)  # Inserta el texto en mayúsculas

        TLote = Label(window, text="NÚMERO DE LOTE",  font=("Arial", 32,'bold'),bg="#17820E", fg="white").place(x=80, y=50)
        ELote = Entry(window, width = 40, font=("Arial", 32,'bold'),validate="key",validatecommand=(window.register(validate_entry_lote), "%P"))
        ELote.place(x=80, y=120)
        ELote.bind("<KeyRelease>", convert_to_uppercase)

        TPeso = Label(window, text="PESO (KG)",font=("Arial", 32,'bold'),bg="#17820E", fg="white").place(x=80, y=200)
        EPeso = Entry(window, width=40, font=("Arial", 32,'bold'),validate="key",validatecommand=(window.register(validate_entry_peso), "%S")).place(x=80, y=270)

        AColor = Button(window, text="Analizar",font=("Arial", 30,'bold'),bg="#FCC509", command=lambda:[analize(),DarResultados()]).place(x=80, y=500)
        ATamano = Button(window, text="Mostrar Resultados",font=("Arial", 30,'bold'),bg="#FCC509", command=Pagina_resultado).place(x=720, y=500)

        presult = Label(window, textvariable=self.estado_text, font=("Arial", 50,'bold'), bg="#17820E", fg="white")
        presult.place(x=180, y=380)

        Button(window, text="Configurar Márgenes", font=("Arial", 20), command=self.ventana_cambiar_margenes).place(x=80, y=600)


        window.mainloop()