import tkinter as tk
from tkinter import messagebox
# from tkinter import ttk #importamos los widgets
import mysql.connector



class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conexionBD = None
    
    def conexion(self):
        self.conexionBD = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )

    def crearTablas(self):
        self.conexion()
        cursor=self.conexionBD.cursor()
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









class Inventario:
    def __init__(self, root, database):
        self.root = root
        self.db = database
        
        self.root.title("Login")
        self.centrarVentana(300, 150)

        self.login_frame = tk.Frame(root)
        self.login_frame.pack()

        self.label_username = tk.Label(self.login_frame, text="Usuario:")
        self.label_username.pack()
        self.entry_username = tk.Entry(self.login_frame)
        self.entry_username.pack()
        
        self.label_password = tk.Label(self.login_frame, text="Clave:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.login_frame, show="*")
        self.entry_password.pack()
        
        self.login_button = tk.Button(self.login_frame, text="Ingresar", command=self.login)
        self.login_button.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if username == "admin" and password == "admin":
            messagebox.showinfo("Login", "Login Correcto!")
            self.login_frame.pack_forget()
            # self.root.destroy() 
            self.root.title("Inventario")
            self.menu_principal = tk.Frame(self.root)
            self.menu_principal.pack()
            
            tk.Button(self.menu_principal, text="Proveedores", command=self.proveedores).grid(row=0, column=0)
            tk.Button(self.menu_principal, text="Productos", command=self.productos).grid(row=0, column=1)
            tk.Button(self.menu_principal, text="Categorías", command=self.categorias).grid(row=0, column=2)
        else:
            messagebox.showerror("Error al Iniciar Sesión", "Usuario o Clave Incorrectas")


    def proveedores(self):
        menu_proveedores = tk.Toplevel(self.root)
        menu_proveedores.title("Proveedores")

        tk.Label(menu_proveedores, text="Nombre:").grid(row=0, column=0)
        tk.Label(menu_proveedores, text="Domicilio:").grid(row=1, column=0)
        tk.Label(menu_proveedores, text="Teléfono:").grid(row=2, column=0)
        
        entry_nombre = tk.Entry(menu_proveedores)
        entry_domicilio = tk.Entry(menu_proveedores)
        entry_telefono = tk.Entry(menu_proveedores)
        
        entry_nombre.grid(row=0, column=1)
        entry_domicilio.grid(row=1, column=1)
        entry_telefono.grid(row=2, column=1)
        
        tk.Button(menu_proveedores, text="Nuevo", command=lambda: 
                  self.agregar_proveedor(entry_nombre.get(), 
                                         entry_domicilio.get(), 
                                         entry_telefono.get())
                    ).grid(row=3, column=0)

        tk.Button(menu_proveedores, text="Modificar").grid(row=3, column=1)
        tk.Button(menu_proveedores, text="Eliminar").grid(row=3, column=2)

    def productos(self):
        menu_productos = tk.Toplevel(self.root)
        menu_productos.title("Productos")
        
        tk.Label(menu_productos, text="Descripción:").grid(row=0, column=0)
        tk.Label(menu_productos, text="Precio:").grid(row=1, column=0)
        tk.Label(menu_productos, text="Stock:").grid(row=2, column=0)
        tk.Label(menu_productos, text="Stock Mínimo:").grid(row=3, column=0)
        tk.Label(menu_productos, text="Categoría ID:").grid(row=4, column=0)
        tk.Label(menu_productos, text="Proveedor ID:").grid(row=5, column=0)
        
        entry_descripcion = tk.Entry(menu_productos)
        entry_precio = tk.Entry(menu_productos)
        entry_stock = tk.Entry(menu_productos)
        entry_stock_min = tk.Entry(menu_productos)
        entry_categoria = tk.Entry(menu_productos)
        entry_proveedor = tk.Entry(menu_productos)
        
        entry_descripcion.grid(row=0, column=1)
        entry_precio.grid(row=1, column=1)
        entry_stock.grid(row=2, column=1)
        entry_stock_min.grid(row=3, column=1)
        entry_categoria.grid(row=4, column=1)
        entry_proveedor.grid(row=5, column=1)
        
        tk.Button(menu_productos, text="Nuevo", command=lambda: 
                  self.agregar_producto(entry_descripcion.get(), 
                                        entry_precio.get(), 
                                        entry_stock.get(), 
                                        entry_stock_min.get(),
                                        entry_categoria.get(), 
                                        entry_proveedor.get())
                    ).grid(row=6, column=0)

        tk.Button(menu_productos, text="Modificar").grid(row=6, column=1)
        tk.Button(menu_productos, text="Eliminar").grid(row=6, column=2)

    def categorias(self):
        menu_categorias = tk.Toplevel(self.root)
        menu_categorias.title("Categorías")
        
        tk.Label(menu_categorias, text="Descripción:").grid(row=0, column=0)
        
        entry_descripcion = tk.Entry(menu_categorias)
        entry_descripcion.grid(row=0, column=1)
        
        tk.Button(menu_categorias, text="Nuevo", command=lambda: 
                        self.agregar_categoria(entry_descripcion.get())
                  ).grid(row=1, column=0)
    
        tk.Button(menu_categorias, text="Modificar").grid(row=1, column=1)
        tk.Button(menu_categorias, text="Eliminar").grid(row=1, column=2)

    def agregar_proveedor(self, nombre, domicilio, telefono):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        cursor.execute(
            "INSERT INTO Proveedores (provNom, provDom, provTel) VALUES (%s, %s, %s)", (nombre, domicilio, telefono))
        self.db.conexionBD.commit()
        cursor.close()
        self.db.conexionBD.close()
    
    def agregar_producto(self, descripcion, precio, stock, stock_min, categoria, proveedor):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        cursor.execute(
            "INSERT INTO Productos (prodDesc, prodPrecio, prodStock, prodStockMin, catId, provId) VALUES (%s, %s, %s, %s, %s, %s)",(descripcion, precio, stock, stock_min, categoria, proveedor))
        self.db.conexionBD.commit()
        cursor.close()
        self.db.conexionBD.close()
    
    def agregar_categoria(self, descripcion):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        cursor.execute("INSERT INTO Categorias (catDescripcion) VALUES (%s)", (descripcion,))
        self.db.conexionBD.commit()
        cursor.close()
        self.db.conexionBD.close()











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
    db.crearTablas()
    root = tk.Tk()
    app = Inventario(root, db)
    root.mainloop()

if __name__ == "__main__":
    main()