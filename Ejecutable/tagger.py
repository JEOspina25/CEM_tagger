import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import xml.etree.ElementTree as ET
import xmltodict
import json
import os


class CEMTaggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CEM Tagger")

        # Maximizar la ventana al inicio
        # self.root.attributes('-fullscreen', True)

        

        # Crear una etiqueta de bienvenida con el texto adicional
        welcome_title = "Prototipo de Etiquetado Corpus Ex Machina"
        welcome_text = ("\n"
                        "Prototipo en desarrollo para el etiquetado de textos \n")
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

        # Crear el botón para convertir XML a JSON
        self.convert_button = tk.Button(button_frame, text="Convertir XML a JSON", command=self.convert_xml_to_json, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b082", fg="white")
        self.convert_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
            # Crear el botón para etiquetar oraciones
        self.tag_sentences_button = tk.Button(button_frame, text="Etiquetar Oraciones", command=self.tag_sentences, borderwidth=1, relief="raised", width=35, height=3, font=("Arial", 16), bg="#25b060", fg="white")
        self.tag_sentences_button.grid(row=0, column=1, columnspan=2, padx=10, pady=10, sticky="ew")






    def tag_sentences(self):
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            messagebox.showwarning("Archivo No Seleccionado", "Por favor, seleccione un archivo XML antes de etiquetar.")
            return

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
        #se convierte el archivo xml a json
        self.convert_xml_to_json()

        #Se abre el archivo json convertido para agregar las etiquetas
        name = "converter_xml.json"
        etiquetado = "oraciones.json"

        #pegar etiquetado al final de name
        with open(name, "r") as read_file:
            data = json.load(read_file)
            with open(etiquetado, "r") as read_file:
                data_etiquetado = json.load(read_file)
                data["oraciones"] = data_etiquetado["oraciones"]
                with open(name, "w") as write_file:
                    json.dump(data, write_file, indent=4)

 

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
                oracion = ' '.join(palabras)+" - (id=" + id + ")"# Unir las palabras en una sola cadena
                oraciones.append(oracion)

        return oraciones

    
    def procesar_oracion(self, oracion):
        # Extraer el identificador de la oración
        self.identificador = oracion.split("id=")[1].replace(")","")

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
            "A1": ["Enunciativas afirmativas","Enunciativas negativas","Interrogativas directas totales con sentido literal","Interrogativas directas parciales con sentido literal"
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
            "A1": ["Impersonales con el verbo 'haber'","Copulativas","Atributivas","Transitivas","Intransitivas"
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
                    ["Con la conjunción 'y'","Negativas con la conjunción 'ni'"],
                "A2": ["Sustitución de 'y' por 'e'"],
                "B1": [],
                "B2": ["Negativas con la conjunción 'ni'"],
                "C1": 
                    ["Asíndeton","Polisíndeton"]
            },
            "Adversativas": {
                "A1": ["Con la conjunción 'pero'"],
                "A2": [],
                "B1": ["Sin embargo","Aunque"],
                "B2": ["Sino","No obstante"],
                "C1": []
            },
            "Disyuntivas": {
                "A1": ["Con la conjunción 'o'"],
                "A2": ["Sustitución de 'o' por 'u'"],
                "B1": [],
                "B2": [],
                "C1": []
            },
            "Distributivas": {
                "A1": ["Con uno... otro..."],
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

    def guardar_datos_oraciones_simples(self):

        # Obtener los valores seleccionados en los cuadros desplegables
        simple1 = self.var_simple1.get()
        simple2 = self.var_simple2.get()

        id = "id_"+str(self.identificador)

        # escribir en el archivo json
        with open("oraciones.json", "r") as read_file:
            data = json.load(read_file)
            if simple1 != "Según la actitud del hablante" and simple2 != "Según la naturaleza del predicado":
                #error, solo se debe seleccionar una opcion
                messagebox.showerror("Error", "Solo se debe seleccionar una opción")
                #se cierra la ventana
                self.tagging_window.destroy()
            else:    
                if simple1 != "Según la actitud del hablante":
                    data["oraciones"]["simples"][id] = {"ADH": simple1}
                if simple2 != "Según la naturaleza del predicado":
                    data["oraciones"]["simples"][id] = {"NDP": simple2}

        
        with open("oraciones.json", "w") as write_file:
            json.dump(data, write_file, indent=4)

        #Actualizar el campo de texto con los identificadores de las oraciones etiquetadas
        self.text_identificadores.insert(tk.END, id + " simple,")
        

        #cerrar ventana
        self.tagging_window.destroy()
        

        

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
                #Si se modifican dos campos hay error
                if compuesta1 != "Copulativas" and compuesta2 != "Adversativas" and compuesta3 != "Disyuntivas" and compuesta4 != "Distributivas":
                    #error, solo se debe seleccionar una opcion
                    messagebox.showerror("Error", "Solo se debe seleccionar una opción")
                    #se cierra la ventana
                    self.tagging_window.destroy()
                else:
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

        















####################################################################################




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
                print(self.selected_file_path)
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


    def convert_xml_to_json(self):
        if not hasattr(self, 'selected_file_path') or not self.selected_file_path:
            messagebox.showwarning("Archivo No Seleccionado", "Por favor, seleccione un archivo XML.")
            return

        file_path = self.selected_file_path

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

        # Obtener la ruta de destino para guardar el archivo JSON
        save_path = filedialog.askdirectory()
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
