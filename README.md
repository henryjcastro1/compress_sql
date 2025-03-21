﻿# compress_sql
Conversor de Imágenes y Generador de Archivos
Este programa es una herramienta gráfica desarrollada en Python que permite convertir imágenes a formato .webp, comprimirlas y generar archivos en formatos .unl, .csv y .sql para su uso en bases de datos o sistemas de gestión.

Características principales:
Conversión de imágenes a .webp:

Convierte imágenes en formatos como .png, .jpg, .jpeg, .gif y .bmp a .webp, un formato moderno y eficiente.

Las imágenes convertidas se guardan en una carpeta llamada imagenes_webp.

Generación de archivos:

Archivo .unl: Crea un archivo de texto con el formato nombre_original|nombre_webp|fecha|1 para cada imagen procesada.

Archivo .csv: Genera un archivo CSV con los nombres de las imágenes convertidas.

Archivo .sql: Crea un archivo SQL con sentencias INSERT para cargar las imágenes en una tabla de base de datos. Incluye opciones para comentar los ALTER TABLE y agregar un DELETE FROM antes de los INSERT.

Interfaz gráfica moderna:

Utiliza la biblioteca ttkthemes para aplicar un tema visual moderno (arc).

Permite seleccionar múltiples imágenes, ver su lista y procesarlas con un solo clic.

Muestra una barra de progreso durante la conversión de imágenes.

Opciones personalizables:

Comentar ALTER TABLE: Opción para comentar las sentencias ALTER TABLE en el archivo SQL.

Incluir DELETE FROM: Opción para agregar una sentencia DELETE FROM antes de los INSERT en el archivo SQL.

Fácil de usar:

Interfaz intuitiva y amigable.

Proporciona mensajes de éxito o error para cada operación.

**Requisitos:**
Python 3.x

Bibliotecas necesarias:

tkinter (incluida en Python).

ttkthemes (para el tema visual moderno).

Pillow (para la manipulación de imágenes).

csv (incluida en Python).
