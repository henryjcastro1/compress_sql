import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
from PIL import Image
import datetime
import os
import csv

# Nombre de la carpeta y archivos generados
WEBP_DIR = 'imagenes_webp'
UNL_FILE = 'zimagenes.unl'
CSV_FILE = 'zimagenes.csv'
SQL_FILE = 'zimagenes.sql'

# Crear la carpeta si no existe
os.makedirs(WEBP_DIR, exist_ok=True)

def compress_image(img):
    """ Convertir la imagen a RGB y comprimirla. """
    return img.convert("RGB")

def convert_image_to_webp(input_path):
    """ Convertir una imagen a formato .webp y guardarla. """
    try:
        if input_path.lower().endswith(".webp"):
            return None, None, None  # Ignorar imágenes que ya están en .webp

        with Image.open(input_path) as img:
            img = compress_image(img)
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            webp_name = base_name + '.webp'
            webp_path = os.path.join(WEBP_DIR, webp_name)
            img.save(webp_path, 'webp', quality=85)
        return base_name, webp_name, webp_path
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo convertir la imagen: {input_path}\n{e}")
        return None, None, None

def create_unl_file(image_data):
    """ Crear el archivo zimagenes.unl. """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        with open(UNL_FILE, 'w') as file:
            for original_name, webp_name in image_data:
                file.write(f"{original_name}|{webp_name}|{current_date}|1\n")
        messagebox.showinfo("Éxito", f"Archivo .unl creado exitosamente: {UNL_FILE}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo .unl: {e}")

def create_csv_file(image_data):
    """ Crear el archivo zimagenes.csv. """
    try:
        with open(CSV_FILE, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["Nombre de la Imagen"])
            for _, webp_name in image_data:
                csvwriter.writerow([webp_name])
        messagebox.showinfo("Éxito", f"Archivo .csv creado exitosamente: {CSV_FILE}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo .csv: {e}")

def create_sql_file(image_data, comment_triggers, include_delete):
    """ Crear el archivo zimagenes.sql. """
    try:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql_content = """-- Inicio del archivo SQL
BEGIN WORK;
SET client_encoding=UTF8;
SET datestyle = 'ISO,DMY';
"""
        # Condición para comentar o no los triggers
        if comment_triggers:
            sql_content += "-- "
        
        sql_content += "ALTER TABLE img_product DISABLE TRIGGER ALL;\n"
        
        # Si se quiere borrar la tabla, se incluye el DELETE
        if include_delete:
            sql_content += "DELETE FROM img_product;\n\n"

        for original_name, webp_name in image_data:
            sql_content += (
                f"INSERT INTO img_product (cod_producto, img, fecha_actualizacion, predet) "
                f"VALUES ('{original_name}', '{webp_name}', '{current_date}', 1);\n"
            )

        sql_content += "\nALTER TABLE img_product ENABLE TRIGGER ALL;\nCOMMIT;\n-- Fin del archivo SQL\n"

        with open(SQL_FILE, 'w') as sqlfile:
            sqlfile.write(sql_content)
        messagebox.showinfo("Éxito", f"Archivo .sql creado exitosamente: {SQL_FILE}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear el archivo .sql: {e}")

def browse_images():
    """ Seleccionar imágenes y mostrarlas en la lista. """
    file_paths = filedialog.askopenfilenames(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.gif;*.bmp;*.webp")])
    if file_paths:
        file_listbox.delete(0, tk.END)
        unique_paths = set(file_paths)  # Evitar rutas duplicadas
        for path in unique_paths:
            file_listbox.insert(tk.END, path)
        update_image_count()

def process_images():
    """ Procesar imágenes seleccionadas y generar los archivos. """
    if file_listbox.size() == 0:
        messagebox.showwarning("Advertencia", "No hay imágenes seleccionadas.")
        return

    image_data = []
    progress_bar['maximum'] = file_listbox.size()

    for index in range(file_listbox.size()):
        original_path = file_listbox.get(index)
        base_name, webp_name, webp_path = convert_image_to_webp(original_path)
        if base_name and webp_name:
            image_data.append((base_name, webp_name))
        progress_bar['value'] = index + 1
        root.update_idletasks()

    if image_data:
        create_unl_file(image_data)
        create_csv_file(image_data)
        create_sql_file(image_data, comment_triggers_var.get(), delete_line_var.get())
    else:
        messagebox.showinfo("Información", "No se procesaron nuevas imágenes.")
    update_image_count()
    progress_bar['value'] = 0

def update_image_count():
    """ Actualizar el recuento de imágenes en la interfaz. """
    image_count_label.config(text=f"Imágenes seleccionadas: {file_listbox.size()}")

# Interfaz gráfica
root = ThemedTk(theme="arc")  # Usar un tema moderno
root.resizable(False, False)
root.title("Conversor de Imágenes y Generador de Archivos")

# Frame principal
main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

# Frame para la lista de imágenes
list_frame = ttk.LabelFrame(main_frame, text="Imágenes Seleccionadas", padding="10")
list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

file_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE, width=50, height=15, bg="lightgray")
file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=file_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_listbox.config(yscrollcommand=scrollbar.set)

# Frame para los botones
button_frame = ttk.Frame(main_frame, padding="10")
button_frame.pack(fill=tk.X, pady=(0, 10))

btn_browse = ttk.Button(button_frame, text="Seleccionar Imágenes", command=browse_images)
btn_browse.pack(side=tk.LEFT, padx=(0, 10))

btn_process = ttk.Button(button_frame, text="Comprimir y Convertir", command=process_images)
btn_process.pack(side=tk.LEFT)

# Frame para las opciones
options_frame = ttk.LabelFrame(main_frame, text="Opciones", padding="10")
options_frame.pack(fill=tk.X, pady=(0, 10))

comment_triggers_var = tk.BooleanVar()
comment_triggers_check = ttk.Checkbutton(options_frame, text="Comentar ALTER TABLE", variable=comment_triggers_var)
comment_triggers_check.pack(anchor=tk.W)

delete_line_var = tk.BooleanVar()
delete_line_check = ttk.Checkbutton(options_frame, text="Incluir DELETE FROM img_product;", variable=delete_line_var)
delete_line_check.pack(anchor=tk.W)

# Barra de progreso
progress_bar = ttk.Progressbar(main_frame, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(fill=tk.X, pady=(0, 10))

# Etiqueta para el recuento de imágenes
image_count_label = ttk.Label(main_frame, text="Imágenes seleccionadas: 0")
image_count_label.pack(fill=tk.X)

# Iniciar la aplicación
root.mainloop()