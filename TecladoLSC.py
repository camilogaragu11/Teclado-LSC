# -*- coding: utf-8 -*-
"""
Created on Mon Mar 5 13:04:12 2024

@author: Cristian Camilo García Agudelo
             ccgarciaa@unal.edu.co
"""
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

def resource_path(relative_path):
    """Obtiene la ruta absoluta del recurso, útil tanto para desarrollo como para PyInstaller."""
    try:
        # Para PyInstaller, _MEIPASS es el directorio temporal en el que se extraen los archivos.
        base_path = sys._MEIPASS
    except Exception:
        # En desarrollo, usa el directorio actual.
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class KeyManager:
    """Clase para manejar el estado de las teclas especiales y acciones de teclas."""
    def __init__(self):
        # Inicializa el estado de Caps Lock como desactivado.
        self.caps_lock_active = False

    def toggle_caps_lock(self):
        """Alterna el estado de Caps Lock y devuelve el estado actualizado."""
        self.caps_lock_active = not self.caps_lock_active
        return self.caps_lock_active

class ImageLoader:
    """Clase para cargar y redimensionar imágenes de las teclas."""
    def __init__(self):
        # Almacena en caché las imágenes cargadas para evitar recargar las mismas imágenes.
        self.image_cache = {}

    def load_image(self, key, size):
        """Carga y redimensiona una imagen para una tecla dada."""
        img_path = resource_path(f'imagenes/{key}.jpg')
        try:
            # Abre la imagen desde el camino especificado.
            image = Image.open(img_path)
            # Redimensiona la imagen al tamaño especificado.
            resized_image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except Exception as e:
            # Imprime un mensaje de error si no se puede cargar la imagen.
            print(f"Error al cargar la imagen {img_path}: {e}")
            return None

class SignLanguageKeyboard:
    """Clase principal para el teclado en pantalla en Lengua de Señas Colombiana."""
    def __init__(self, master):
        # Inicializa la ventana principal y las clases para manejar el teclado.
        self.master = master
        self.key_manager = KeyManager()
        self.image_loader = ImageLoader()

        # Configura la ventana principal.
        self.master.title("Teclado en Lengua de Señas Colombiana")
        self.master.attributes('-topmost', True)
        self.master.config(bg='Light gray')

        # Configura el ícono de la ventana.
        icon_path = resource_path('imagenes/icono.ico')
        try:
            self.master.iconbitmap(icon_path)
        except Exception as e:
            # Imprime un mensaje de error si no se puede cargar el ícono.
            print(f"Error cargando el ícono: {e}")

        # Crea un área de texto para mostrar el texto ingresado.
        self.text_area = tk.Text(master, height=10, width=60, insertbackground='black')
        self.text_area.pack(pady=10)

        # Crea el teclado en pantalla.
        self.create_keyboard()

    def create_keyboard(self):
        """Crea el teclado en pantalla y sus botones."""
        # Define las filas del teclado con las teclas a mostrar.
        rows = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'backspace'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ', 'enter'],
            ['capslock', 'z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ['space']
        ]

        # Crea un marco para el teclado.
        keyboard_frame = tk.Frame(self.master, bg='#f0f0f0', borderwidth=4, relief='ridge')
        keyboard_frame.pack(padx=10, pady=10)

        # Agrega una etiqueta que indica que es el teclado LSC.
        label = tk.Label(keyboard_frame, text='Teclado LSC', font=('futuristic', 12), bg='#f0f0f0')
        label.pack(pady=5)

        # Crea cada fila del teclado.
        for row in rows:
            frame = tk.Frame(keyboard_frame, bg='#f0f0f0')
            frame.pack(side='top', expand=True, fill='both')

            # Espacios adicionales para centrar las teclas en la fila.
            if row == ['capslock', 'z', 'x', 'c', 'v', 'b', 'n', 'm']:
                tk.Label(frame, text=' ', width=4, bg='#f0f0f0').pack(side='left')
                tk.Label(frame, text=' ', width=2, bg='#f0f0f0').pack(side='left')

            if row == ['space']:
                tk.Label(frame, text=' ', width=21, bg='#f0f0f0').pack(side='left')

            # Crea los botones para cada tecla en la fila.
            for key in row:
                self.create_key(frame, key)

            # Espacios adicionales para centrar las teclas en la fila de espacio.
            if row == ['space']:
                tk.Label(frame, text=' ', width=2, bg='#f0f0f0').pack(side='left')

    def create_key(self, frame, key):
        """Crea un botón para una tecla específica y le asigna la imagen y comando correspondiente."""
        # Carga la imagen para la tecla.
        photo = self.image_loader.load_image(key, self.get_key_size(key))
        if photo is None:
            # Si no se pudo cargar la imagen, no crea el botón.
            return

        # Crea el botón con la imagen cargada.
        button = tk.Button(frame, image=photo, command=lambda k=key: self.press_key(k), 
                           activebackground="Misty rose", cursor="hand1")
        button.image = photo
        button.config(bg='#0a0a0a', fg='#f0f0f0', borderwidth=2, relief='ridge')
        button.pack(side='left', padx=4, pady=8)

        # Guarda la referencia del botón Caps Lock para cambiar su apariencia más tarde.
        if key == 'capslock':
            self.caps_lock_button = button

        # Asigna eventos de presionar y soltar el botón para ciertas teclas.
        button.bind('<ButtonPress-1>', lambda event, k=key: self.start_press(k))
        button.bind('<ButtonRelease-1>', lambda event, k=key: self.stop_press(k))

    def get_key_size(self, key):
        """Devuelve el tamaño de la imagen para una tecla dada."""
        if key == 'space':
            return (360, 50)  # Tamaño para la tecla de espacio.
        elif key in ['capslock', 'backspace', 'enter']:
            return (80, 50)   # Tamaño para teclas especiales.
        else:
            return (50, 50)   # Tamaño para otras teclas.

    def press_key(self, key):
        """Maneja la acción correspondiente a cada tecla presionada."""
        if key == 'enter':
            self.text_area.insert(tk.END, '\n')
        elif key == 'space':
            self.text_area.insert(tk.END, ' ')
        elif key == 'capslock':
            self.toggle_caps_lock()
        elif key == 'backspace':
            # El manejo de borrado continuo está en start_press.
            pass
        else:
 #Inserta el carácter en el área de texto considerando el estado de Caps Lock.
            text = key.upper() if self.key_manager.caps_lock_active else key
            self.text_area.insert(tk.END, text)

    def toggle_caps_lock(self):
        """Alterna el estado de Caps Lock y actualiza el botón Caps Lock."""
        active = self.key_manager.toggle_caps_lock()
        if active:
            self.caps_lock_button.config(relief='sunken', bg='green')  # Verde para indicar activado.
        else:
            self.caps_lock_button.config(relief='ridge', bg='#0a0a0a')  # Negro para indicar desactivado.

    def start_press(self, key):
        """Inicia la acción continua para la tecla presionada, como Backspace."""
        if key == 'backspace':
            self.backspace_button_pressed = True
            self.repeat_backspace()

    def stop_press(self, key):
        """Detiene la acción continua para la tecla liberada."""
        if key == 'backspace':
            self.backspace_button_pressed = False

    def repeat_backspace(self):
        """Borra caracteres continuamente mientras la tecla Backspace está presionada."""
        if self.backspace_button_pressed:
            self.text_area.delete('insert-1c', 'insert')
            self.master.after(120, self.repeat_backspace)  # Repite cada 120 ms mientras esté presionada.

if __name__ == "__main__":
    # Crea una instancia de tkinter y la pasa al constructor del teclado.
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')  # Elige un tema para la aplicación. 
    root.config(bg='Light gray')  # Color de fondo de la ventana.
    # Instancia el teclado y ejecuta la aplicación.
    app = SignLanguageKeyboard(root)
    root.mainloop()


