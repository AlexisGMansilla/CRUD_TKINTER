import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk #importamos los widgets
import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexionBD = None
    
    def conexion(self):
        conexionBD = mysql.connector.connect(
            host="localhost",
            user="root" , 
            password="12345678",
            database="crud_tkinter"
            )

        cursor=conexionBD.cursor()
        try:
            cursor.execute('''
                CREATE TABLE PROVEEDORES(
                    provId INT AUTO_INCREMENT PRIMARY KEY,
                    provNom VARCHAR(200),
                    provDom VARCHAR(200),
                    provTel VARCHAR(20)
                )
                            ''')
            
            cursor.execute('''
                CREATE TABLE CATEGORIAS(
                    catId INT AUTO_INCREMENT PRIMARY KEY,
                    catDescripcion VARCHAR(200)
                )
                            ''')

            cursor.execute('''
                CREATE TABLE PRODUCTOS(
                    prodId INT AUTO_INCREMENT PRIMARY KEY,
                    prodDesc VARCHAR(255),
                    prodPrecio DECIMAL(10, 2),
                    prodStock INT,
                    prodStockMin INT,
                    catId INT,
                    provId INT,
                    FOREIGN KEY (catId) REFERENCES Categorias(catid),
                    FOREIGN KEY (provId) REFERENCES Proveedores(provid)
                )
                            ''')

            cursor.execute('''
                CREATE TABLE USUARIOS(
                    userId INT AUTO_INCREMENT PRIMARY KEY,
                    usuNombre VARCHAR(255),
                    usuClave VARCHAR(255)
                )
                            ''')

            messagebox.showinfo("Conexion","Tablas creadas correctamente")
        except:
            messagebox.showinfo("Conexion", "Conexion Exitosa en la BDs")

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.centrarVentana(300, 150)
        
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
        username = self.entry_username.get()
        password = self.entry_password.get()

        conexionBD=mysql.connector.connect(host="localhost",user="root" , password="12345678" , database="crud_tkinter",  auth_plugin='mysql_native_password')

        cursor=conexionBD.cursor()

        if username == "admin" and password == "admin":
            messagebox.showinfo("Inicio de Sesión", "Login Correcto!")
            self.root.destroy()  # Cerrar la ventana de login
            self.open_main_window() # OPEN MAIN WINDOW ABRE LA NUEVA VENTANA XD
        else:
            messagebox.showerror("Error al Iniciar Sesión", "Usuario o Clave Incorrectas")

    def salir(self):
        valor = messagebox.askquestion("Salir","¿Está seguro que desea salir?")
        if valor == "yes":
            self.root.destroy()
            
    def centrarVentana(self, ancho, alto):
        anchoPantalla = self.root.winfo_screenwidth()
        altoPantalla = self.root.winfo_screenheight()
        x = (anchoPantalla // 2) - (ancho // 2)
        y = (altoPantalla // 2) - (alto // 2)
        self.root.geometry(f'{ancho}x{alto}+{x}+{y}')


def main():
    db = Database(host="localhost",
                user="root" , 
                password="12345678",
                database="crud_tkinter"
                  )
    db.conexion()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()