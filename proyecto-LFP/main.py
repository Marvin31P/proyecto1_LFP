
from tkinter import *
import tkinter as tk
from tkinter import filedialog
import json

class AplicacionDesktop(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Aplicación de Escritorio")
        self.geometry("600x400")

        self.cuadro_texto1 = tk.Text(self, wrap="word")
        self.cuadro_texto1.pack(expand=True, fill="both", side="left")

        self.cuadro_texto2 = tk.Text(self, wrap="word")
        self.cuadro_texto2.pack(expand=True, fill="both", side="left")

        self.boton_abrir = tk.Button(self, text="Abrir archivo", command=self.abrir_archivo)
        self.boton_abrir.pack(pady=5)

        self.boton_traducir = tk.Button(self, text="Traducir", command=self.traducir)
        self.boton_traducir.pack(pady=5)

    def abrir_archivo(self):
        archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")])
        if archivo:
            with open(archivo, "r") as f:
                contenido = f.read()
                self.cuadro_texto1.delete(1.0, "end")
                self.cuadro_texto1.insert("end", contenido)

    def traducir(self):
        contenido = self.cuadro_texto1.get(1.0, "end").strip()
        if contenido:
            try:
                datos = json.loads(contenido)
                if "Encabezado" in datos and "TituloPagina" in datos["Encabezado"]:
                    html_generado = self.generar_html(datos)
                    self.cuadro_texto2.delete(1.0, "end")
                    self.cuadro_texto2.insert("end", html_generado)
                else:
                    print("Error: Estructura JSON incorrecta.")
            except json.JSONDecodeError as e:
                print("Error de formato JSON:", e)

    def generar_html(self, datos):
        html = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n<title>{}</title>\n</head>\n<body>\n".format(datos["Encabezado"]["TituloPagina"])
        for elemento in datos["Cuerpo"]:
            if "Titulo" in elemento:
                html += "<h1>{}</h1>\n".format(elemento["Titulo"]["texto"])
            elif "Fondo" in elemento:
                html += "<div style='background-color:{};'>\n".format(elemento["Fondo"]["color"])
            elif "Parrafo" in elemento:
                html += "<p>{}</p>\n".format(elemento["Parrafo"]["texto"])
            # Agregar lógica para otros elementos como Texto, Codigo, etc.
        html += "</body>\n</html>"
        return html

if __name__ == "__main__":
    app = AplicacionDesktop()
    app.mainloop()
