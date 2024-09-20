import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import xml.etree.ElementTree as ET
import xmltodict

import json
import os


class CEMTaggerApp:
    def __init__(self, root):
        """Inicializa la aplicación de etiquetado CEM Tagger
        Organigrama de las ventanas
        root
        |-> tagging_window_paragraphs
        |-> tagging_window
        |-> tagging_discurso


        
        """
        self.root = root
        self.root.title("CEM Tagger")

        # Crear una etiqueta de bienvenida con el texto adicional
        welcome_title = "Prototipo de Etiquetado Textual"
        welcome_text = ("\n"
                        "Prototipo en desarrollo para el etiquetado de textos  \n"
                        "Superestructura, tipo de discurso y oraciones. \n")
        self.label_title = tk.Label(root, text=welcome_title, font=("Arial", 24), justify=tk.CENTER)
        self.label_title.pack(pady=10)

        self.label_text = tk.Label(root, text=welcome_text, font=("Arial", 12), justify=tk.LEFT)
        self.label_text.pack(pady=10)

        # Crear un marco para contener los campos de metadata
        metadata_frame = tk.Frame(root)
        metadata_frame.pack(padx=10, pady=10, fill=tk.X)

        # Configurar el grid de la columna para que todos los campos tengan el mismo tamaño
        metadata_frame.columnconfigure(1, weight=1)  # Hacer que la segunda columna expanda

        # Crear campos para mostrar metadata
        self.metadata_fields = {}
        metadata_labels = {
            "Título": "tittle",
            "ID del Documento": "number",
            "Nivel": "level",
            "Género Textual": "textual_genre",
            "País": "country",
            "Responsable": "responsable"
        }

        for row, (label, field) in enumerate(metadata_labels.items()):
            # Etiqueta
            tk.Label(metadata_frame, text=f"{label}:", font=("Arial", 12)).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            # Campo de entrada
            entry = tk.Entry(metadata_frame, font=("Arial", 12))
            entry.grid(row=row, column=1, padx=5, pady=2, sticky="ew")
            entry.config(state=tk.DISABLED)
            self.metadata_fields[field] = entry

    

        # Crear un marco para contener los botones
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20, padx=10, fill=tk.X)

        # Configurar el grid de columnas para los botones
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        # Crear el botón para seleccionar XML
        self.select_xml_button = tk.Button(button_frame, text="Seleccionar XML", command=self.select_xml, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b082", fg="white")
        self.select_xml_button.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # # Crear el botón para convertir XML a JSON
        # self.convert_button = tk.Button(button_frame, text="Convertir XML a JSON", command=self.convert_xml_to_json, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b082", fg="white")
        # self.convert_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Crear el botón para etiquetar el tipo de discurso
        self.tag_sentences_button = tk.Button(button_frame, text="Etiquetar Discurso", command=self.etiquetar_discurso, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.tag_sentences_button.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        
        # Crear el botón para etiquetar parrafos
        self.tag_sentences_button = tk.Button(button_frame, text="Etiquetar Parrafos", command=self.tag_paragraphs, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.tag_sentences_button.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
    
            # Crear el botón para etiquetar oraciones
        self.tag_sentences_button = tk.Button(button_frame, text="Etiquetar Oraciones", command=self.tag_sentences, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.tag_sentences_button.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

        #Crear botón de ayuda de color azul
        self.btn_ayuda = tk.Button(button_frame, text="Ayuda", command=self.ayuda, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#82bfdc", fg="white")
        self.btn_ayuda.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

   

    def ayuda(self):
        """Esta función se encarga de mostrar un mensaje de ayuda"""
        messagebox.showinfo("Ayuda", "Este programa permite etiquetar textos en formato XML. \n\n"
                                     "1. Seleccione un archivo XML. \n"
                                     "2. Etiquete los parrafos \n"
                                        "3. Etiquete el tipo de discurso \n"
                                        "4. Etiquete las oraciones \n\n"
                                        "Al finalizar se generará un archivo JSON con las etiquetas. \n"
                                        "Con el nombre del archivo original y la extensión *par_orac.json")




    def tag_paragraphs(self):
        """Esta función se encarga de etiquetar los párrafos del texto"""

        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            messagebox.showwarning("Archivo No Seleccionado", "Por favor, seleccione un archivo XML antes de etiquetar.")
            return


        #Si existe el archivo "pivot.json" se elimina
        if os.path.exists("pivot.json"):
            os.remove("pivot.json")
        
        # Algoritmo para enumerar los párrafos del xml añadiendo un id
        tree = ET.parse(self.selected_file_path)
        root = tree.getroot()
        id = 1

        for paragraph in root.findall('paragraph'):
            paragraph.set('id', "p"+str(id))
            id += 1

        #Se crea un archivo xml con los párrafos enumerados
        tree.write('paragraphs.xml')

        #Se crea la ventana de etiquetado de párrafos
        self.tagging_window_paragraphs = tk.Toplevel(self.root)
        self.tagging_window_paragraphs.title("Etiquetado de Parrafos")

        # Se cuentan cuantos parrafos hay en el archivo
        num_parrafos = 0
        for paragraph in root.findall('paragraph'):
            num_parrafos += 1

        # Se pone la metadata en la ventana de etiquetado
        metadata_frame = tk.Frame(self.tagging_window_paragraphs)
        metadata_frame.pack(pady=8, padx=21, fill=tk.X)

        # Configurar el grid de la columna para que todos los campos tengan el mismo tamaño
        metadata_frame.columnconfigure(1, weight=1)  # Hacer que la segunda columna expanda

        # Crear campos para mostrar metadata
        self.metadata_fields = {}
        metadata_labels = {
            "Título": "tittle",
            "ID del Documento": "number",
            "Nivel": "level",
            "Género Textual": "textual_genre",
            "País": "country",
            "Responsable": "responsable",
            "Superestructura": "superestructura"  
        }

        for row, (label, field) in enumerate(metadata_labels.items()):
            # Etiqueta
            tk.Label(metadata_frame, text=f"{label}:", font=("Arial", 8)).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            # Campo de entrada
            entry = tk.Entry(metadata_frame, font=("Arial", 8))
            entry.grid(row=row, column=1, padx=5, pady=1, sticky="ew")
            entry.config(state=tk.DISABLED)
            self.metadata_fields[field] = entry

        self.display_metadata()

        # Crear un marco principal para organizar los elementos
        main_frame = tk.Frame(self.tagging_window_paragraphs)
        main_frame.pack(fill="both", expand=True)

        # Configurar main_frame para permitir la expansión de filas y columnas
        main_frame.grid_columnconfigure(0, weight=2)

        # Crear un marco para los botones de párrafos
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Extraer los párrafos
        paragraphs = self.extraer_parrafos('paragraphs.xml')

        # Crear un canvas para contener los botones
        canvas = tk.Canvas(button_frame)
        scrollbar_y = tk.Scrollbar(button_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(button_frame, orient="horizontal", command=canvas.xview)

        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        #lista para almacenar los identificadores de los parrafos
        self.identificadores = []

        #Agregar un campo de texto para mostrar los identificadores de los parrafos etiquetados
        self.text_identificadores = tk.Text(main_frame, height=8, width=50, font=("Arial", 12))
        self.text_identificadores.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        #boton terminar
        self.btn_terminar = tk.Button(self.tagging_window_paragraphs, text="Terminar", command=self.teminar_parrafos, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_terminar.pack(pady=5)

        for paragraph in paragraphs:
            # Crear un botón dentro del frame scrollable
            self.botones_parrafo = tk.Button(self.scrollable_frame, text=paragraph, anchor="w", command=lambda text=paragraph: self.procesar_parrafo(text))
            self.botones_parrafo.pack(fill="both", expand=True)

        return 1
    
    def procesar_parrafo(self, parrafo):
        """Esta función se encarga de procesar el párrafo seleccionado y abrir la ventana de etiquetado de párrafos"""
        # Extraer el identificador del párrafo
        self.identificador = parrafo.split(")")[0].replace("(id= p","")
        self.identificador = self.identificador.split(")")[0].replace("(","")

        #Añadir el identificador al cuadro de texto
        self.text_identificadores.insert(tk.END, self.identificador + ", ")

        # Crear la ventana de etiquetado de párrafos
        self.tagging_window = tk.Toplevel(self.root)
        self.tagging_window.title("Etiquetado de Parrafos")

        # Configurar la ventana para adaptarse al contenido
        self.tagging_window.columnconfigure(0, weight=1)
        self.tagging_window.columnconfigure(1, weight=1)
        self.tagging_window.rowconfigure([0, 1, 2, 3,4,5,6,7,8,9,10,11], weight=1)


        # Crear los títulos
        tk.Label(self.tagging_window, text="Atributos Narrativo", font=("Arial", 14)).grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        tk.Label(self.tagging_window, text="Atributos Argumentativo", font=("Arial", 14)).grid(row=0, column=1, sticky="ew", padx=10, pady=10)

        # Atributos Narrativo

        # Boton "Introducción". Al pulsarlo agrega introduccion al cuadro de texto
        self.btn_introduccion = tk.Button(self.tagging_window, text="Introducción - (N_Intro)", command= lambda: self.text_atributos.insert(tk.END, "N_Intro, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_introduccion.grid(row=2, column=0, padx=10, pady=0, sticky="ew")

        #Boton "Desarrollo". Al pulsarlo agrega desarrollo al cuadro de texto
        self.btn_desarrollo = tk.Button(self.tagging_window, text="Desarrollo (N_Dllo)", command= lambda: self.text_atributos.insert(tk.END, "N_Dllo, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_desarrollo.grid(row=3, column=0, padx=10, pady=0, sticky="ew")

        # Boton "Climax". Al pulsarlo agrega climax al cuadro de texto
        self.btn_climax = tk.Button(self.tagging_window, text="Climax - (N_Clim)", command= lambda: self.text_atributos.insert(tk.END, "N_Clim, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_climax.grid(row=4, column=0, padx=10, pady=0, sticky="ew")

        # Boton "Desenlace". Al pulsarlo agrega desenlace al cuadro de texto
        self.btn_desenlace = tk.Button(self.tagging_window, text="Desenlace - (N_Des)", command= lambda: self.text_atributos.insert(tk.END, "N_Des, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_desenlace.grid(row=5, column=0, padx=10, pady=0, sticky="ew")

        # Boton "Título". Al pulsarlo agrega título al cuadro de texto
        self.btn_titulo = tk.Button(self.tagging_window, text="Título - (N_Tit)", command= lambda: self.text_atributos.insert(tk.END, "N_Tit, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_titulo.grid(row=6, column=0, padx=10, pady=0, sticky="ew")

        # Boton "Subtítulo". Al pulsarlo agrega subtítulo al cuadro de texto
        self.btn_subtitulo = tk.Button(self.tagging_window, text="Subtítulo - (N_Subt)", command= lambda: self.text_atributos.insert(tk.END, "N_Subt, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_subtitulo.grid(row=7, column=0, padx=10, pady=0, sticky="ew")

        # Boton "Datos Autor". Al pulsarlo agrega datos_autor al cuadro de texto
        self.btn_datos_autor = tk.Button(self.tagging_window, text="Datos Autor - (N_DA)", command= lambda: self.text_atributos.insert(tk.END, "N_DA, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_datos_autor.grid(row=8, column=0, padx=10, pady=0, sticky="ew")

        # Atributos Argumentativo

        #Boton "Introduccion o situacion inicial". Al pulsarlo agrega introduccion al cuadro de texto
        self.btn_introduccion_arg = tk.Button(self.tagging_window, text="Introducción - (A_Intro)", command= lambda: self.text_atributos.insert(tk.END, "A_Intro, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_introduccion_arg.grid(row=2, column=1, padx=10, pady=0, sticky="ew")

        #Boton "Desarrollo o argumentos". Al pulsarlo agrega desarrollo al cuadro de texto
        self.btn_desarrollo_arg = tk.Button(self.tagging_window, text="Desarrollo - (A_Dllo)", command= lambda: self.text_atributos.insert(tk.END, "A_Dllo, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_desarrollo_arg.grid(row=3, column=1, padx=10, pady=0, sticky="ew")

        # Boton "Conclusión". Al pulsarlo agrega climax al cuadro de texto
        self.btn_conclusion_arg = tk.Button(self.tagging_window, text="Conclusión - (A_Con)", command= lambda: self.text_atributos.insert(tk.END, "A_Con, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_conclusion_arg.grid(row=4, column=1, padx=10, pady=0, sticky="ew")

        # Boton "Datos bibliograficos". Al pulsarlo agrega datos_bibliograficos al cuadro de texto
        self.btn_datos_bibliograficos = tk.Button(self.tagging_window, text="Datos bibliográficos - (A_DB)", command= lambda: self.text_atributos.insert(tk.END, "A_DB, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_datos_bibliograficos.grid(row=5, column=1, padx=10, pady=0, sticky="ew")

        # Boton "Titulo". Al pulsarlo agrega titulo al cuadro de texto
        self.btn_titulo_arg = tk.Button(self.tagging_window, text="Título - (A_Tit)", command= lambda: self.text_atributos.insert(tk.END, "A_Tit, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_titulo_arg.grid(row=6, column=1, padx=10, pady=0, sticky="ew")

        # Boton "Subtitulo". Al pulsarlo agrega subtitulo al cuadro de texto
        self.btn_subtitulo_arg = tk.Button(self.tagging_window, text="Subtítulo - (A_Subt)", command= lambda: self.text_atributos.insert(tk.END, "A_Subt, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_subtitulo_arg.grid(row=7, column=1, padx=10, pady=0, sticky="ew")

        # Boton "Datos autor". Al pulsarlo agrega datos_autor al cuadro de texto
        self.btn_datos_autor_arg = tk.Button(self.tagging_window, text="Datos Autor - (A_DA)", command= lambda: self.text_atributos.insert(tk.END, "A_DA, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_datos_autor_arg.grid(row=8, column=1, padx=10, pady=0, sticky="ew")

        # Boton "Referencia". Al pulsarlo agrega referencia al cuadro de texto
        self.btn_referencia_arg = tk.Button(self.tagging_window, text="Referencia - (A_Ref)", command= lambda: self.text_atributos.insert(tk.END, "A_Ref, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_referencia_arg.grid(row=9, column=1, padx=10, pady=0, sticky="ew")

        #Cuadro de texto para visualizar los atributos asignados al parrafo. Se expande en todo el ancho
        self.text_atributos = tk.Text(self.tagging_window, height=4, width=50, font=("Arial", 12))
        self.text_atributos.grid(row=10, columnspan=2, padx=5, pady=5, sticky="ew")
        
        #Escribir el parrafo en el cuadro de texto y dejar un espacio en blanco
        self.text_atributos.insert(tk.END, parrafo + "\n\n")

        # Botón de Guardar
        self.btn_guardar = tk.Button(self.tagging_window, text="Guardar", command=self.guardar_etiquetas_parrafo, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_guardar.grid(row=11, column=0, pady=10)

        # Botón de Cancelar
        self.btn_cancelar = tk.Button(self.tagging_window, text="Cancelar", command=self.tagging_window.destroy, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_cancelar.grid(row=11, column=1, pady=10)

        return 1
    



    def guardar_etiquetas_parrafo(self):
        """Esta función se encarga de guardar las etiquetas asignadas al párrafo en el archivo JSON"""
        # Extraer el texto del cuadro de texto
        etiquetas = self.text_atributos.get("1.0", tk.END)
        etiquetas = etiquetas.split("\n\n")[1] # Extraer solo las etiquetas
        etiquetas = etiquetas.split(", ") # Separar las etiquetas por coma
        etiquetas = [x for x in etiquetas if x != "\n"]

        #Abrir archivo json para agregar las etiquetas
        name = "pivot.json"

        #Crear archivo json "pivot.json" si no existe
        if not os.path.exists(name):
            with open(name, "w") as outfile:
                json.dump({"Super_Estructura": {}}, outfile, indent=4)
        
        #Abrir archivo json para agregar las etiquetas
        with open(name, "r") as read_file:
            data = json.load(read_file)
            data["Super_Estructura"][self.identificador] = etiquetas
            with open(name, "w") as write_file:
                json.dump(data, write_file, indent=4)
        
        #Agregar el identificador al cuadro de texto
        self.identificadores.append(self.identificador)

        #Cerrar la ventana de etiquetado de parrafos
        self.tagging_window.destroy()       
        return 1
    


    
    def teminar_parrafos(self):
        """Esta función se encarga de guardar el tipo de discurso seleccionado en el archivo JSON"""
        #Cerrar la ventana de etiquetado de parrafos
        self.tagging_window_paragraphs.destroy()

        #Convertir "paragraphs.xml" a json
        self.convert_xml_to_json("paragraphs.xml")


        #Se etiqueta el tipo de discurso
        self.etiquetar_discurso()

        return 1
    


    
    def etiquetar_discurso(self):
        """Esta función se encarga de etiquetar el tipo de discurso del texto"""

        # Crea una ventana nueva self.tagging_discurso para etiquetar el tipo de discurso
        self.tagging_discurso = tk.Toplevel(self.root)
        self.tagging_discurso.title("Etiquetado de Discurso")

        # Pone un título: "Seleccione el tipo de discurso"
        tk.Label(self.tagging_discurso, text="Seleccione el tipo de discurso", font=("Arial", 14)).pack(pady=10)

        # Crea un frame para organizar los botones en dos columnas
        button_frame = tk.Frame(self.tagging_discurso)
        button_frame.pack(pady=10)

        # Se crean los botones con los tipos de discurso y se organizan en dos columnas

        # Primera columna
        self.btn_politico = tk.Button(button_frame, text="Político - (D_Pol)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Pol, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_politico.grid(row=0, column=0, padx=5, pady=5)

        self.btn_religioso = tk.Button(button_frame, text="Religioso - (D_Rel)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Rel, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_religioso.grid(row=1, column=0, padx=5, pady=5)

        self.btn_didactico = tk.Button(button_frame, text="Didáctico - (D_Did)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Did, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_didactico.grid(row=2, column=0, padx=5, pady=5)

        self.btn_periodistico = tk.Button(button_frame, text="Periodístico - (D_Per)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Per, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_periodistico.grid(row=3, column=0, padx=5, pady=5)

        self.btn_literario = tk.Button(button_frame, text="Literario - (D_Lit)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Lit, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_literario.grid(row=4, column=0, padx=5, pady=5)

        # Segunda columna
        self.btn_juridico = tk.Button(button_frame, text="Jurídico - (D_Jur)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Jur, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_juridico.grid(row=0, column=1, padx=5, pady=5)

        self.btn_comercial = tk.Button(button_frame, text="Comercial o Publicitario - (D_CP)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_CP, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_comercial.grid(row=1, column=1, padx=5, pady=5)

        self.btn_social = tk.Button(button_frame, text="Social - (D_Soc)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Soc, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_social.grid(row=2, column=1, padx=5, pady=5)

        self.btn_cientifico = tk.Button(button_frame, text="Científico - (D_Cien)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Cien, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_cientifico.grid(row=3, column=1, padx=5, pady=5)

        self.btn_academico = tk.Button(button_frame, text="Académico - (D_Acad)", command= lambda: self.text_identificadores_discurso.insert(tk.END, "D_Acad, "), borderwidth=1, relief="raised", width=25, height=1, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_academico.grid(row=4, column=1, padx=5, pady=5)

        # Se crea un campo de texto para mostrar los identificadores de los tipos de discursos seleccionados
        self.text_identificadores_discurso = tk.Text(self.tagging_discurso, height=8, width=50, font=("Arial", 12))
        self.text_identificadores_discurso.pack(pady=10)

        # Botones de Guardar y Cancelar
        self.btn_guardar_discurso = tk.Button(self.tagging_discurso, text="Guardar", command=self.guardar_discurso, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_guardar_discurso.pack(pady=5)

        self.btn_cancelar_discurso = tk.Button(self.tagging_discurso, text="Cancelar", command=self.tagging_discurso.destroy, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_cancelar_discurso.pack(pady=5)

        return 1

        
    def guardar_discurso(self): 
        """Esta función se encarga de guardar el tipo de discurso seleccionado en el archivo JSON"""
  
        #Se extrae la información del campo de texto como una lista
        discurso = self.text_identificadores_discurso.get("1.0", tk.END)
        discurso = discurso.split(", ")

        #Se eliminan los saltos de linea
        discurso = [x for x in discurso if x != "\n"]
        self.tipo_discurso = discurso

        #Agregar "pivot.json" al final de "converter_xml.json"
        name = "converter_xml.json"
        etiquetado = "pivot.json"

        #pegar etiquetado al final de name
        with open(name, "r") as read_file:
            data = json.load(read_file)
            with open(etiquetado, "r") as read_file:
                data_etiquetado = json.load(read_file)
                data["Super_Estructura"] = data_etiquetado["Super_Estructura"]
                with open(name, "w") as write_file:
                    json.dump(data, write_file, indent=4)
        
        if self.tipo_discurso != 0:
            #Agregar el tipo de texto en la document/metadata del json
            with open(name, "r") as read_file:
                data = json.load(read_file)
                data["document"]["metadata"]["tipo_discurso"] = self.tipo_discurso
                with open(name, "w") as write_file:
                    json.dump(data, write_file, indent=4)
   

        #Guardar el json en un archivo con el nombre del archivo xml original sin la extensión y con "_par.json"
        name = self.selected_file_path.split(".")[0] + "_par.json"
        with open(name, "w") as write_file:
            json.dump(data, write_file, indent=4)

        #Eliminar "pivot.json"
        os.remove("pivot.json")

        #Eliminar "paragraphs.xml"
        os.remove("paragraphs.xml")

        #Se cierra la ventana de etiquetado de discurso
        self.tagging_discurso.destroy()
        

        #avisar que se ha terminado de etiquetar los parrafos
        messagebox.showinfo("Terminado", "Se ha terminado de etiquetar los parrafos y discurso")
        return 1

        
    def extraer_parrafos(self,ruta_archivo):
        # Extraer los párrafos del archivo XML
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
        parrafos = []

        for paragraph in root.findall('.//paragraph'):
            parrafo_texto = []
            for token in paragraph.findall('.//token'):
                palabra = token.get('form')
                parrafo_texto.append(palabra)
            
            id = paragraph.get('id')
            parrafo = "(id="+id + ") - " + ' '.join(parrafo_texto) # Unir las palabras en una sola cadena
            parrafos.append(parrafo)
        
        return parrafos


    def tag_sentences(self):
        """Esta función se encarga de etiquetar las oraciones del texto"""

        with open("oraciones.json", "w", encoding="utf-8") as outfile:
          json.dump({"oraciones": {"simples":{},"compuestas" :{}}}, outfile, indent=4)

        # Crear la ventana de etiquetado de oraciones
        self.tagging_window_sentences = tk.Toplevel(self.root)
        self.tagging_window_sentences.title("Etiquetado de Oraciones simples y compuestas")

        # Maximizar la ventana de etiquetado al inicio
        # self.tagging_window_sentences.attributes('-zoomed', True)

        # Crear un marco para los campos de metadata
        metadata_frame = tk.Frame(self.tagging_window_sentences)
        metadata_frame.pack(pady=8, padx=21, fill=tk.X)

        # Configurar el grid de la columna para que todos los campos tengan el mismo tamaño
        metadata_frame.columnconfigure(1, weight=1)  # Hacer que la segunda columna expanda

        # Crear campos para mostrar metadata
        self.metadata_fields = {}
        metadata_labels = {
            "Título": "tittle",
            "ID del Documento": "number",
            "Nivel": "level",
            "Género Textual": "textual_genre",
            "País": "country",
            "Responsable": "responsable",
            "Superestructura": "superestructura"  
        }

        for row, (label, field) in enumerate(metadata_labels.items()):
            # Etiqueta
            tk.Label(metadata_frame, text=f"{label}:", font=("Arial", 8)).grid(row=row, column=0, sticky="w", padx=5, pady=2)
            # Campo de entrada
            entry = tk.Entry(metadata_frame, font=("Arial", 8))
            entry.grid(row=row, column=1, padx=5, pady=1, sticky="ew")
            entry.config(state=tk.DISABLED)
            self.metadata_fields[field] = entry


        self.display_metadata()


        # Crear un marco principal para organizar los elementos
        main_frame = tk.Frame(self.tagging_window_sentences)
        main_frame.pack(fill="both", expand=True)
    
        # Configurar main_frame para permitir la expansión de filas y columnas
        main_frame.grid_columnconfigure(0, weight=2)  # Permitir que la primera columna se expanda

        # Crear un marco para los botones de oraciones
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=0, column=0,padx = 10,pady=10, sticky="ew")


        # Extraer las oraciones y mostrarlas en el cuadro de texto
        oraciones = self.extraer_oraciones(self.selected_file_path)

        # Crear un canvas para contener los botones
        canvas = tk.Canvas(button_frame)
        scrollbar_y = tk.Scrollbar(button_frame, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(button_frame, orient="horizontal", command=canvas.xview)

        self.scrollable_frame = tk.Frame(canvas)
        self.scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))) 

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set) 

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        #lista para almacenar los identificadores de las oraciones
        self.identificadores = []

        #Agregar un campo de texto para mostrar los identificadores de las oraciones etiquetadas
        self.text_identificadores = tk.Text(main_frame, height=8, width=50, font=("Arial", 12))
        self.text_identificadores.grid(row=1, column=0, padx=5, pady=5, sticky="ew")



        #boton terminar 
        self.btn_terminar = tk.Button(self.tagging_window_sentences, text="Terminar", command=self.terminar, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.btn_terminar.pack(pady=5)



        for oracion in oraciones:
            # Crear un botón dentro del frame scrollable
            self.botones_oracion = tk.Button(self.scrollable_frame, text=oracion,anchor="w", command=lambda text=oracion: self.procesar_oracion(text))
            self.botones_oracion.pack(fill="both", expand=True)



    def terminar(self):
        """Esta función se encarga de guardar las etiquetas de las oraciones en un archivo json y cerrar la ventana de etiquetado de oraciones"""

        #Se abre el archivo json convertido para agregar las etiquetas
        name = "017_B1_INOT_esp_Etiq_par.json"
        etiquetado = "oraciones.json"

        #pegar etiquetado al final de name
        with open(name, "r") as read_file:
            data = json.load(read_file)
            with open(etiquetado, "r") as read_file:
                data_etiquetado = json.load(read_file)
                data["oraciones"] = data_etiquetado["oraciones"]
                with open(name, "w") as write_file:
                    json.dump(data, write_file, indent=4)

        #Guardar el json en un archivo con el nombre del archivo del name original sin la extensión y con "_orac.json"
        name = name.split(".")[0] + "_orac.json"
        with open(name, "w") as write_file:
            json.dump(data, write_file, indent=4)

        #Eliminar "oraciones.json"
        os.remove("oraciones.json")

        #Cerrar la ventana de etiquetado de oraciones
        self.tagging_window_sentences.destroy()

        #avisar que se ha terminado de etiquetar las oraciones
        messagebox.showinfo("Terminado", "Se ha terminado de etiquetar las oraciones")

        return 1

 

    def extraer_oraciones(self,ruta_archivo):
        # Extraer las oraciones del archivo XML
        tree = ET.parse(ruta_archivo)
        root = tree.getroot()
        oraciones = []

        for paragraph in root.findall('paragraph'):
            for sentence in paragraph.findall('sentence'):
                # Crear una lista de palabras para cada oración
                palabras = []
                for token in sentence.findall('token'):
                    forma = token.get('form')
                    palabras.append(forma)
                id = sentence.get('id')
                oracion = "(id="+id + ") - " + ' '.join(palabras) # Unir las palabras en una sola cadena
                oraciones.append(oracion)

        return oraciones

    
    def procesar_oracion(self, oracion):
        # Extraer el identificador de la oración
        self.identificador = oracion.split(")")[0].replace("(id=","")

        # Crear la ventana de etiquetado de oraciones
        self.tagging_window = tk.Toplevel(self.root)
        self.tagging_window.title("Etiquetado de Oraciones")

        # Configurar la ventana para adaptarse al contenido
        self.tagging_window.columnconfigure(0, weight=1)
        self.tagging_window.columnconfigure(1, weight=1)
        self.tagging_window.rowconfigure([0, 1, 2 , 3 , 4 , 5,6], weight=1)

        # Crear un campo que muestre el string "oración" en la fila 0
        oracion_label = tk.Label(self.tagging_window, text=oracion, font=("Arial", 8))
        oracion_label.grid(row=0, column=0, columnspan=2, pady=10)  # Ajustar columnspan para que ocupe ambas columnas

        # Crear los títulos
        tk.Label(self.tagging_window, text="Oraciones Simples", font=("Arial", 14)).grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        tk.Label(self.tagging_window, text="Oraciones Compuestas", font=("Arial", 14)).grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        tags_simples = { 
            "segun_la_actitud_del_hablante": {
            "A1": ["Enunciativas afirmativas","Enunciativas negativas","Interrogativas directas totales con sentido literal","Interrogativas directas parciales con sentido literal","no aplica"
            ],
            "A2": ["Interrogativas disyuntivas","Exclamativas","Exhortativas"
            ],
            "B1": [
                "Dubitativas con indicativo"
            ],
            "B2": [
                "Dubitativas con subjuntivo e indicativo"
            ],
            "C1": [
                "Estructura interrogativa con sujeto antepuesto","Interrogativas precedidas de tópico"
            ]
            },

            "segun_la_naturaleza_del_predicado": {
            "A1": ["Impersonales con el verbo 'haber'","Copulativas","Atributivas","Transitivas","Intransitivas","no aplica"
            ],
            "A2": ["Reflexivas","Impersonales con el verbo 'haber'","Impersonales con verbos unipersonales y de fenómenos atmosféricos","Impersonales y pasivas reflejas","Desiderativas"
            ],
            "B1": ["Recíprocas","Impersonales con verbos unipersonales y de fenómenos atmosféricos","Impersonales y pasivas reflejas"
            ],
            "B2": [
                "Pasivas perifrásticas"]}
        }

        oraciones_compuestas = {
            "Copulativas": {
                "A1": 
                    ["Con la conjunción 'y'","Negativas con la conjunción 'ni'","no aplica"],
                "A2": ["Sustitución de 'y' por 'e'"],
                "B1": [],
                "B2": ["Negativas con la conjunción 'ni'"],
                "C1": 
                    ["Asíndeton","Polisíndeton"]
            },
            "Adversativas": {
                "A1": ["Con la conjunción 'pero'","no aplica"],
                "A2": [],
                "B1": ["Sin embargo","Aunque"],
                "B2": ["Sino","No obstante"],
                "C1": []
            },
            "Disyuntivas": {
                "A1": ["Con la conjunción 'o'","no aplica"],
                "A2": ["Sustitución de 'o' por 'u'"],
                "B1": [],
                "B2": [],
                "C1": []
            },
            "Distributivas": {
                "A1": ["Con uno... otro...","no aplica"],
                "A2": [],
                "B1": [],
                "B2": [],
                "C1": []
            }
        }

        niveles = ["A1", "A2", "B1", "B2", "C1"]
        indice = niveles.index(self.level)

        # Oraciones compuestas
        compuestas_copulativas   = [oracion for i in niveles[:indice + 1] for oracion in oraciones_compuestas["Copulativas"][i] if oracion]
        compuestas_adversativas  = [oracion for i in niveles[:indice + 1] for oracion in oraciones_compuestas["Adversativas"][i] if oracion]
        compuestas_disyuntivas   = [oracion for i in niveles[:indice + 1] for oracion in oraciones_compuestas["Disyuntivas"][i] if oracion]
        compuestas_distributivas = [oracion for i in niveles[:indice + 1] for oracion in oraciones_compuestas["Distributivas"][i] if oracion]

        # Oraciones simples
        simples_act_habl = tags_simples["segun_la_actitud_del_hablante"][self.level]

        #Tags de oraciones simples
        simples_act_habl  = [oracion for i in niveles[:indice + 1] for oracion in tags_simples["segun_la_actitud_del_hablante"][i] if oracion]
        simples_predicado = [oracion for i in niveles[:indice + 1] for oracion in tags_simples["segun_la_naturaleza_del_predicado"][i] if oracion]
 

        # Crear los cuadros desplegables para Oraciones Simples
        self.var_simple1 = tk.StringVar(self.tagging_window)
        self.var_simple1.set("Según la actitud del hablante")
        self.menu_simple1 = tk.OptionMenu(self.tagging_window, self.var_simple1, *simples_act_habl)
        self.menu_simple1.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.var_simple2 = tk.StringVar(self.tagging_window)
        self.var_simple2.set("Según la naturaleza del predicado")
        self.menu_simple2 = tk.OptionMenu(self.tagging_window, self.var_simple2, *simples_predicado)
        self.menu_simple2.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
        

        # Crear los cuadros desplegables para Oraciones Compuestas
        self.var_compuesta1 = tk.StringVar(self.tagging_window)
        self.var_compuesta1.set("Copulativas")
        self.menu_compuesta1 = tk.OptionMenu(self.tagging_window, self.var_compuesta1, *compuestas_copulativas)
        self.menu_compuesta1.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        self.var_compuesta2 = tk.StringVar(self.tagging_window)
        self.var_compuesta2.set("Adversativas")
        self.menu_compuesta2 = tk.OptionMenu(self.tagging_window, self.var_compuesta2, *compuestas_adversativas)
        self.menu_compuesta2.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        self.var_compuesta3 = tk.StringVar(self.tagging_window)
        self.var_compuesta3.set("Disyuntivas")
        self.menu_compuesta3 = tk.OptionMenu(self.tagging_window, self.var_compuesta3, *compuestas_disyuntivas)
        self.menu_compuesta3.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        self.var_compuesta4 = tk.StringVar(self.tagging_window)
        self.var_compuesta4.set("Distributivas")
        self.menu_compuesta4 = tk.OptionMenu(self.tagging_window, self.var_compuesta4, *compuestas_distributivas)
        self.menu_compuesta4.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Botón de Guardar Oración simple
        self.btn_guardar = tk.Button(self.tagging_window, text="Asignar Oracion simple", command=self.guardar_datos_oraciones_simples)
        self.btn_guardar.grid(row=6, column=0, pady=10)

        #Boton de guardar oracion compuesta
        self.btn_guardar = tk.Button(self.tagging_window, text="Asignar Oracion compuesta", command=self.guardar_datos_oraciones_compuestas)
        self.btn_guardar.grid(row=6, column=1, pady=10)

        # Boton cancelar
        self.btn_cancelar = tk.Button(self.tagging_window, text="Cancelar", command=self.tagging_window.destroy)
        self.btn_cancelar.grid(row=7, column=0, columnspan=2, pady=10)
        
        return 1




    def guardar_datos_oraciones_simples(self):
        """Esta función guarda los datos de las oraciones simples en el archivo json"""

        # Obtener los valores seleccionados en los cuadros desplegables
        simple1 = self.var_simple1.get()
        simple2 = self.var_simple2.get()

        id = "id_"+str(self.identificador)

        # escribir en el archivo json "oraciones.json"
        with open("oraciones.json", "r") as read_file:
            data = json.load(read_file)
        
        #Si se modifica uno de los campos se guardan los cambios individuales
        if simple1 != "Según la actitud del hablante":
            data["oraciones"]["simples"][id] = {"actitud": simple1}

        if simple2 != "Según la naturaleza del predicado":
            data["oraciones"]["simples"][id] = {"predicado": simple2}

        #Si se modifican ambos campos se guardan los cambios en ambos campos
        if simple1 != "Según la actitud del hablante" and simple2 != "Según la naturaleza del predicado":
            data["oraciones"]["simples"][id] = {"actitud": simple1, "predicado": simple2}

        #Se escribe en el archivo json
        with open("oraciones.json", "w") as write_file:
            json.dump(data, write_file, indent=4)


        #Actualizar el campo de texto con los identificadores de las oraciones etiquetadas
        self.text_identificadores.insert(tk.END, id + " simple,")
        
        #cerrar ventana
        self.tagging_window.destroy()
        return 1


        

    def guardar_datos_oraciones_compuestas(self):
            
            # Obtener los valores seleccionados en los cuadros desplegables
            compuesta1 = self.var_compuesta1.get()
            compuesta2 = self.var_compuesta2.get()
            compuesta3 = self.var_compuesta3.get()
            compuesta4 = self.var_compuesta4.get()

            id = "id_"+str(self.identificador)
    
            # escribir en el archivo json
            with open("oraciones.json", "r") as read_file:
                data = json.load(read_file)

            if compuesta1 != "Copulativas":
                data["oraciones"]["compuestas"][id] = {"Cop": compuesta1}
            if compuesta2 != "Adversativas":
                data["oraciones"]["compuestas"][id] = {"Adv": compuesta2}
            if compuesta3 != "Disyuntivas":
                data["oraciones"]["compuestas"][id] = {"Disy": compuesta3}
            if compuesta4 != "Distributivas":
                data["oraciones"]["compuestas"][id] = {"Dist": compuesta4}
        
            with open("oraciones.json", "w") as write_file:
                json.dump(data, write_file, indent=4)

            #Actualizar el campo de texto con los identificadores de las oraciones etiquetadas
            self.text_identificadores.insert(tk.END, id + " compuesta, ")

            #cerrar ventana
            self.tagging_window.destroy()


    def select_xml(self):
        # Abrir el cuadro de diálogo para seleccionar un archivo XML
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        if not file_path:
            return  # El usuario canceló la selección


        # Guardar la ruta del archivo seleccionado para su uso posterior
        self.selected_file_path = file_path


        # Extraer y mostrar metadata
        self.display_metadata()

    def display_metadata(self):
        try:
            with open(self.selected_file_path, 'r', encoding='utf-8') as xml_file:
                xml_content = xml_file.read()
                data_dict = xmltodict.parse(xml_content, encoding='utf-8', process_namespaces=True)
                self.title = data_dict['document']['metadata']['tittle']
                self.level = data_dict['document']['metadata']['level']
                # Obtener el tipo y subtipo del género textual
                text_type = str(data_dict.get('document', {}).get('metadata', {}).get('textual_genre', {}).get('@type', 'N/A') + ', ' + data_dict.get('document', {}).get('metadata', {}).get('textual_genre', {}).get('@subtype', 'N/A'))
                # Actualizar campos con valores del XML, o 'N/A' si no están presentes
                self.update_metadata_field("tittle", data_dict['document']['metadata']['tittle'])  # Cambio de 'tittle' a 'title'
                self.update_metadata_field("number", data_dict['document']['metadata']['number']["@id_doc"])
                self.update_metadata_field("level", data_dict['document']['metadata']['level'])
                self.update_metadata_field("textual_genre", text_type)
                self.update_metadata_field("Subtipo", data_dict['document']['metadata']['textual_genre']['@subtype'])

                self.update_metadata_field("country", data_dict['document']['metadata']['country']['@name'])
                self.update_metadata_field("responsable", data_dict['document']['metadata']['responsable'])
            
    ## Aqui se podría agregar la nueva función para mostrar el campo de superestructura
                data = {
                   "Noticia": "Titular, entrada (resumen breve de la noticia), cuerpo de la noticia (detalles adicionales organizados de lo más importante a lo menos importante), y conclusión o cierre.",
                    "Notas de enciclopedia": "Título del artículo, definición o descripción inicial, desarrollo del tema (incluye secciones y subsecciones), ejemplos y referencias bibliográficas."
                    }
                subtipo = data_dict['document']['metadata']['textual_genre']['@subtype']
                self.update_metadata_field("superestructura", data[subtipo])
        except Exception as e:
            messagebox.showerror("Error al Extraer Metadata", f"No se pudo extraer la metadata del archivo XML: {str(e)}")


    def update_metadata_field(self, field, value):
        entry = self.metadata_fields.get(field)
        if entry:
            entry.config(state=tk.NORMAL)
            entry.delete(0, tk.END)
            entry.insert(0, value)
            entry.config(state=tk.DISABLED)


    def convert_xml_to_json(self,file_path):
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            messagebox.showwarning("Archivo No Seleccionado", "Por favor, seleccione un archivo XML.")
            return

        # Intentar convertir XML a JSON
        try:
            with open(file_path, 'r', encoding='utf-8') as xml_file:
                xml_content = xml_file.read()
                json_data = xmltodict.parse(xml_content, encoding='utf-8', process_namespaces=True)
        except Exception as e:
            messagebox.showerror("Error de Conversión", f"No se pudo convertir el archivo XML a JSON: {str(e)}")
            return

        # Pedir al usuario que ingrese el nombre del archivo para guardar
        filename = "converter_xml.json"

        # Ruta de destino es la carpeta del archivo XML a la misma direccion de self.selected_file_path
        save_path = os.path.dirname(self.selected_file_path)


        if not save_path:
            return  # El usuario canceló la selección de la carpeta

        # Combinar la ruta y el nombre del archivo
        full_path = os.path.join(save_path, filename)

        try:
            with open(full_path, 'w', encoding='utf-8') as json_file:
                json.dump(json_data, json_file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Error al Guardar", f"No se pudo guardar el archivo JSON: {str(e)}")
            return

if __name__ == "__main__":
    root = tk.Tk()
    app = CEMTaggerApp(root)
    root.mainloop()
