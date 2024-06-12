import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk #importamos los widgets
import mysql.connector





class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Iniciar Sesión")
        self.root.geometry("300x150")
        
        self.label_username = tk.Label(root, text="Usuario:")
        self.label_username.pack()
        self.entry_username = tk.Entry(root)
        self.entry_username.pack()
        
        self.label_password = tk.Label(root, text="Clave:")
        self.label_password.pack()
        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.pack()
        
        self.login_button = tk.Button(root, text="Ingresar", command=self.login)
        self.login_button.pack()

    def login(self):
        # Lógica de autenticación de usuario
        username = self.entry_username.get()
        password = self.entry_password.get()
        
        if username == "admin" and password == "admin":
            messagebox.showinfo("Inicio de Sesión", "Login Correcto!")
            self.root.destroy()  # Cerrar la ventana de login
            self.open_main_window()
        else:
            messagebox.showerror("Error al Iniciar Sesión", "Usuario o Clave Incorrectas")