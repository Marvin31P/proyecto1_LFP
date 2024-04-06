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
                if "Inicio" in datos:
                    html_generado = self.generar_html(datos["Inicio"])
                    self.cuadro_texto2.delete(1.0, "end")
                    self.cuadro_texto2.insert("end", html_generado)
                else:
                    print("Error: Estructura JSON incorrecta.")
            except json.JSONDecodeError as e:
                print("Error de formato JSON:", e)

    def generar_html(self, datos):
        html = "<!DOCTYPE html>\n<html>\n<head>\n<meta charset='UTF-8'>\n<title>{}</title>\n</head>\n<body>\n".format(datos["Encabezado"]["TituloPagina"])
        for elemento in datos["Cuerpo"]:
            if "Texto" in elemento:
                estilo = elemento["Texto"]
                html += "<p style='font-family:{}; color:{}; font-size:{};'>{}</p>\n".format(estilo["fuente"], estilo["color"], estilo["tamaño"], estilo["estilo"])
            elif "Cursiva" in elemento:
                estilo = elemento["Cursiva"]
                html += "<p style='font-style: italic; color:{};'>{}</p>\n".format(estilo["color"], estilo["texto"])
            elif "Negrita" in elemento:
                estilo = elemento["Negrita"]
                html += "<p style='font-weight: bold; color:{};'>{}</p>\n".format(estilo["color"], estilo["texto"])
            elif "Subrayado" in elemento:
                estilo = elemento["Subrayado"]
                html += "<p style='text-decoration: underline; color:{};'>{}</p>\n".format(estilo["color"], estilo["texto"])
            elif "Tachado" in elemento:
                estilo = elemento["Tachado"]
                html += "<p style='text-decoration: line-through; color:{};'>{}</p>\n".format(estilo["color"], estilo["texto"])
            elif "Codigo" in elemento:
                estilo = elemento["Codigo"]
                html += "<pre style='font-family: monospace; text-align:{}; color:{}; font-size:{};'>{}</pre>\n".format(estilo["posicion"], estilo["color"], estilo["tamaño"], estilo["texto"])
            elif "Parrafo" in elemento:
                estilo = elemento["Parrafo"]
                html += "<p style='text-align:{}; color:{}; font-size:{};'>{}</p>\n".format(estilo["posicion"], estilo["color"], estilo["tamaño"], estilo["texto"])
            elif "Titulo" in elemento:
                estilo = elemento["Titulo"]
                html += "<h1 style='text-align:{}; color:{}; font-size:{};'>{}</h1>\n".format(estilo["posicion"], estilo["color"], estilo["tamaño"], estilo["texto"])
            elif "Fondo" in elemento:
                estilo = elemento["Fondo"]
                html += "<div style='background-color:{};'>\n".format(estilo["color"])
            elif "Tabla" in elemento:
                tabla = elemento["Tabla"]
                html += "<table border='1'>\n"
                for fila in range(int(tabla["filas"])):
                    html += "<tr>\n"
                    for columna in range(int(tabla["columnas"])):
                        for elem in tabla["elemento"]:
                            if elem["fila"] == str(fila + 1) and elem["columna"] == str(columna + 1):
                                html += "<td>{}</td>\n".format(elem["texto"])
                    html += "</tr>\n"
                html += "</table>\n"
        html += "</body>\n</html>"
        return html

if __name__ == "__main__":
    app = AplicacionDesktop()
    app.mainloop()
