# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 12:55:01 2024

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
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class KeyManager:
    """Clase para manejar el estado de las teclas especiales y acciones de teclas."""
    def __init__(self):
        self.caps_lock_active = False

    def toggle_caps_lock(self):
        """Alterna el estado de Caps Lock y devuelve el estado actualizado."""
        self.caps_lock_active = not self.caps_lock_active
        return self.caps_lock_active

class ImageLoader:
    """Clase para cargar y redimensionar imágenes de las teclas."""
    def __init__(self):
        self.image_cache = {}

    def load_image(self, key, size):
        """Carga y redimensiona una imagen para una tecla dada."""
        img_path = resource_path(f'imagenes/{key}.jpg')
        try:
            image = Image.open(img_path)
            resized_image = image.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(resized_image)
        except Exception as e:
            print(f"Error al cargar la imagen {img_path}: {e}")
            return None

class SignLanguageKeyboard:
    """Clase principal para el teclado en pantalla en Lengua de Señas Colombiana."""
    def __init__(self, master):
        self.master = master
        self.key_manager = KeyManager()
        self.image_loader = ImageLoader()

        # Carga las palabras desde el archivo spanish_words.txt
        self.word_list = self.load_word_list('spanish_words.txt')

        # Configuración de la ventana
        self.master.title("Teclado en Lengua de Señas Colombiana")
        self.master.attributes('-topmost', True)
        self.master.config(bg='Light gray')

        # Configuración del ícono
        icon_path = resource_path('imagenes/icono.ico')
        try:
            self.master.iconbitmap(icon_path)
        except Exception as e:
            print(f"Error cargando el ícono: {e}")

       
        text_label = tk.Label(master, text='Área de texto', font=('Arial', 12), bg='Light gray')
        text_label.pack(pady=(10, 0))  # Agregar espacio antes del título
        # Crea el área de texto
        self.text_area = tk.Text(master, height=10, width=60, insertbackground='black')
        self.text_area.pack(pady=10)
        
        suggestions_label = tk.Label(master, text='Predicción-palabras', font=('Arial', 12), bg='Light gray')
        suggestions_label.pack(pady=(10, 0))  # Agregar espacio antes del título

        # Caja desplegable para las sugerencias
        self.suggestions_listbox = tk.Listbox(self.master, height=4)
        self.suggestions_listbox.pack(pady=5)
        self.suggestions_listbox.bind("<<ListboxSelect>>", self.on_suggestion_select)
    

        # Vincula evento de tecla para actualizar las sugerencias
        self.text_area.bind('<KeyRelease>', self.update_suggestions)

        # Crea el teclado
        self.create_keyboard()

    def load_word_list(self, file_name):
        """Carga la lista de palabras desde un archivo .txt."""
        try:
            with open(resource_path(file_name), 'r', encoding='utf-8') as f:
                words = [line.strip() for line in f.readlines()]
            return words
        except Exception as e:
            print(f"Error al cargar el archivo {file_name}: {e}")
            return []

    def create_keyboard(self):
        """Crea el teclado en pantalla."""
        rows = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'backspace'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'ñ', 'enter'],
            ['capslock', 'z', 'x', 'c', 'v', 'b', 'n', 'm'],
            ['space']
        ]

        keyboard_frame = tk.Frame(self.master, bg='#f0f0f0', borderwidth=4, relief='ridge')
        keyboard_frame.pack(padx=10, pady=10)

        label = tk.Label(keyboard_frame, text='Teclado LSC', font=('futuristic', 12), bg='#f0f0f0')
        label.pack(pady=5)

        for row in rows:
            frame = tk.Frame(keyboard_frame, bg='#f0f0f0')
            frame.pack(side='top', expand=True, fill='both')

            if row == ['capslock', 'z', 'x', 'c', 'v', 'b', 'n', 'm']:
                tk.Label(frame, text=' ', width=4, bg='#f0f0f0').pack(side='left')
                tk.Label(frame, text=' ', width=2, bg='#f0f0f0').pack(side='left')

            if row == ['space']:
                tk.Label(frame, text=' ', width=21, bg='#f0f0f0').pack(side='left')

            for key in row:
                self.create_key(frame, key)

            if row == ['space']:
                tk.Label(frame, text=' ', width=2, bg='#f0f0f0').pack(side='left')

    def create_key(self, frame, key):
        """Crea un botón para una tecla."""
        photo = self.image_loader.load_image(key, self.get_key_size(key))
        if photo is None:
            return

        button = tk.Button(frame, image=photo, command=lambda k=key: self.press_key(k), 
                           activebackground="Misty rose", cursor="hand1")
        button.image = photo
        button.config(bg='#0a0a0a', fg='#f0f0f0', borderwidth=2, relief='ridge')
        button.pack(side='left', padx=4, pady=8)

        if key == 'capslock':
            self.caps_lock_button = button

        button.bind('<ButtonPress-1>', lambda event, k=key: self.start_press(k))
        button.bind('<ButtonRelease-1>', lambda event, k=key: self.stop_press(k))

    def get_key_size(self, key):
        """Devuelve el tamaño de la imagen para una tecla."""
        if key == 'space':
            return (360, 50)
        elif key in ['capslock', 'backspace', 'enter']:
            return (80, 50)
        else:
            return (50, 50)

    def press_key(self, key):
        """Acción cuando una tecla es presionada."""
        if key == 'enter':
            self.text_area.insert(tk.END, '\n')
        elif key == 'space':
            self.text_area.insert(tk.END, ' ')
        elif key == 'capslock':
            self.toggle_caps_lock()
        elif key == 'backspace':
            pass
        else:
            text = key.upper() if self.key_manager.caps_lock_active else key
            self.text_area.insert(tk.END, text)
            self.update_suggestions(None)

    def toggle_caps_lock(self):
        """Alterna el estado de Caps Lock."""
        active = self.key_manager.toggle_caps_lock()
        if active:
            self.caps_lock_button.config(relief='sunken', bg='green')
        else:
            self.caps_lock_button.config(relief='ridge', bg='#0a0a0a')

    def start_press(self, key):
        """Inicia la acción continua de una tecla."""
        if key == 'backspace':
            self.backspace_button_pressed = True
            self.repeat_backspace()

    def stop_press(self, key):
        """Detiene la acción continua."""
        if key == 'backspace':
            self.backspace_button_pressed = False

    def repeat_backspace(self):
        """Acción continua de backspace."""
        if self.backspace_button_pressed:
            self.text_area.delete('insert-1c', 'insert')
            self.master.after(120, self.repeat_backspace)

    def update_suggestions(self, event):
        """Actualiza la lista de sugerencias."""
        current_text = self.text_area.get("1.0", tk.END).split()[-1]
        matches = [word for word in self.word_list if word.startswith(current_text)]
        self.suggestions_listbox.delete(0, tk.END)
        for match in matches:
            self.suggestions_listbox.insert(tk.END, match)

    def on_suggestion_select(self, event):
        """Completa la palabra al seleccionar una sugerencia."""
        selection = self.suggestions_listbox.get(self.suggestions_listbox.curselection())
        words = self.text_area.get("1.0", tk.END).split()
        words[-1] = selection
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, ' '.join(words) + ' ')
        self.suggestions_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use('clam')
    root.config(bg='Light gray')
    app = SignLanguageKeyboard(root)
    root.mainloop()
