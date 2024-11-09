from tkinter import *

class ventana:
    def __init__(self, size, controlador):
        self.size = size
        self.controlador = controlador
        self.estado_text = None

    def resultado(self, estado, tamano):
        self.estado_text.set(f"{estado} {tamano}")

    def mostrar(self):
        window = Tk()  # diseño de la ventana
        window.title("Sistema de Clasificacion")
        window.resizable(False, False)
        window.configure(background="#17820E")
        window.geometry(self.size)
        self.estado_text = StringVar()
        self.estado_text.set("")

        def analize():
            self.controlador.enviarmensaje("color") # solicita el analisis

        def resultado(): # Aqui es la logica del boton que debe de mostrar los resultados al final
            return

        TLote = Label(window, text="NÚMERO DE LOTE",  font=("Arial", 32,'bold'),bg="#17820E", fg="white").place(x=80, y=50)
        ELote = Entry(window, width = 40, font=("Arial", 32,'bold')).place(x=80, y=120)

        TPeso = Label(window, text="PESO",font=("Arial", 32,'bold'),bg="#17820E", fg="white").place(x=80, y=200)
        EPeso = Entry(window, width=40, font=("Arial", 32,'bold')).place(x=80, y=270)

        AColor = Button(window, text="Analizar",font=("Arial", 30,'bold'),bg="#FCC509", command=analize).place(x=80, y=500)
        ATamano = Button(window, text="Mostrar Resultados",font=("Arial", 30,'bold'),bg="#FCC509", command=resultado).place(x=720, y=500)

        presult = Label(window, textvariable=self.estado_text, font=("Arial", 50,'bold'), bg="#17820E", fg="white")
        presult.place(x=180, y=380)

        window.mainloop()
