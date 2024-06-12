import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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
    
    def verificar_usuario(self, username, password):
        self.conexion()
        cursor = self.conexionBD.cursor()
        cursor.execute("SELECT * FROM USUARIOS WHERE usuNombre = %s AND usuClave = %s", (username, password))
        usuario = cursor.fetchone()
        self.conexionBD.close()
        return usuario


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
        usuario = self.db.verificar_usuario(username, password)
        if usuario:
            messagebox.showinfo("Login", "Login Correcto!")
            self.login_frame.pack_forget()
            self.root.title("Inventario")
            self.menu_principal = tk.Frame(self.root)
            self.menu_principal.pack()
            
            tk.Button(self.menu_principal, text="Proveedores", command=self.proveedores).grid(row=0, column=0)
            tk.Button(self.menu_principal, text="Productos", command=self.productos).grid(row=0, column=1)
            tk.Button(self.menu_principal, text="Categorías", command=self.categorias).grid(row=0, column=2)
        else:
            messagebox.showerror("Error al Iniciar Sesión", "Usuario o Clave Incorrectas")



    def proveedores(self):
        self.menu_proveedores = tk.Toplevel(self.root)
        self.menu_proveedores.title("Proveedores")

        self.proveedor_ID = tk.StringVar()
        self.proveedor_Nombre = tk.StringVar()
        self.proveedor_Domicilio = tk.StringVar()
        self.proveedor_Telefono = tk.StringVar()

        tk.Label(self.menu_proveedores, text="Nombre:").grid(row=0, column=0)
        tk.Label(self.menu_proveedores, text="Domicilio:").grid(row=1, column=0)
        tk.Label(self.menu_proveedores, text="Teléfono:").grid(row=2, column=0)
        
        self.entry_nombre = tk.Entry(self.menu_proveedores, textvariable=self.proveedor_Nombre)
        self.entry_domicilio = tk.Entry(self.menu_proveedores, textvariable=self.proveedor_Domicilio)
        self.entry_telefono = tk.Entry(self.menu_proveedores, textvariable=self.proveedor_Telefono)
        
        self.entry_nombre.grid(row=0, column=1)
        self.entry_domicilio.grid(row=1, column=1)
        self.entry_telefono.grid(row=2, column=1)
        
        tk.Button(self.menu_proveedores, text="Nuevo", command=self.agregar_proveedor).grid(row=3, column=0)
        tk.Button(self.menu_proveedores, text="Modificar", command=self.modificar_proveedor).grid(row=3, column=1)
        tk.Button(self.menu_proveedores, text="Eliminar", command=self.eliminar_proveedor).grid(row=3, column=2)
        tk.Button(self.menu_proveedores, text="Listar", command=self.cargar_proveedores).grid(row=4, column=1)

        
        self.tree_proveedores = ttk.Treeview(self.menu_proveedores, 
                                             columns=("Nombre", "Domicilio", "Telefono"), show='headings')
        
        self.tree_proveedores.heading("Nombre", text="Nombre")
        self.tree_proveedores.heading("Domicilio", text="Domicilio")
        self.tree_proveedores.heading("Telefono", text="Telefono")
        self.tree_proveedores.grid(row=5, column=0, columnspan=3)
        self.tree_proveedores.bind("<Double-1>", self.seleccionarusandoclick)
        self.cargar_proveedores()

    def borrarCampos(self):
        self.proveedor_ID.set("")
        self.proveedor_Nombre.set("")
        self.proveedor_Domicilio.set("")
        self.proveedor_Telefono.set("")
    
    def seleccionarusandoclick(self, event):
        item = self.tree_proveedores.selection()[0]
        self.proveedor_ID.set(self.tree_proveedores.item(item, "text"))
        self.proveedor_Nombre.set(self.tree_proveedores.item(item, "values")[0])
        self.proveedor_Domicilio.set(self.tree_proveedores.item(item, "values")[1])
        self.proveedor_Telefono.set(self.tree_proveedores.item(item, "values")[2])


    def agregar_proveedor(self):
        nombre = self.entry_nombre.get()
        domicilio = self.entry_domicilio.get()
        telefono = self.entry_telefono.get()
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute(
                "INSERT INTO Proveedores (provNom, provDom, provTel) VALUES (%s, %s, %s)", (nombre, domicilio, telefono))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente")
            self.borrarCampos()
            self.cargar_proveedores()
        except:
            messagebox.showerror("No se pudo agregar el proveedor")

    def modificar_proveedor(self):
        provId = self.proveedor_ID.get()
        if provId == "":
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para modificar.")
            return
        nombre = self.proveedor_Nombre.get()
        domicilio = self.proveedor_Domicilio.get()
        telefono = self.proveedor_Telefono.get()
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute(
                "UPDATE Proveedores SET provNom=%s, provDom=%s, provTel=%s WHERE provId=%s",
                (nombre, domicilio, telefono, provId))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Proveedor modificado correctamente")
            self.borrarCampos()
            self.cargar_proveedores()
        except:
            messagebox.showerror("No se pudo modificar el proveedor")

    def eliminar_proveedor(self):
        provId = self.proveedor_ID.get()
        if provId == "":
            messagebox.showwarning("Advertencia", "Seleccione un proveedor para eliminar.")
            return
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("DELETE FROM Proveedores WHERE provId=%s", (provId,))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Proveedor eliminado correctamente")
            self.borrarCampos()
            self.cargar_proveedores()
        except:
            messagebox.showerror("No se pudo eliminar el proveedor")

    def cargar_proveedores(self):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("SELECT * FROM Proveedores")
            registros = cursor.fetchall()
            for row in self.tree_proveedores.get_children():
                self.tree_proveedores.delete(row)
            for registro in registros:
                self.tree_proveedores.insert('', 'end', text=registro[0], values=(registro[1], registro[2], registro[3]))
        except:
            messagebox.showerror("No se pudo cargar los proveedores")

    def productos(self):
        self.menu_productos = tk.Toplevel(self.root)
        self.menu_productos.title("Productos")

        self.producto_ID = tk.StringVar()
        self.producto_Descripcion = tk.StringVar()
        self.producto_Precio = tk.StringVar()
        self.producto_Stock = tk.StringVar()
        self.producto_StockMin = tk.StringVar()
        self.producto_Categoria = tk.StringVar()
        self.producto_Proveedor = tk.StringVar()

        tk.Label(self.menu_productos, text="Descripción:").grid(row=0, column=0)
        tk.Label(self.menu_productos, text="Precio:").grid(row=1, column=0)
        tk.Label(self.menu_productos, text="Stock:").grid(row=2, column=0)
        tk.Label(self.menu_productos, text="Stock Mínimo:").grid(row=3, column=0)
        tk.Label(self.menu_productos, text="Categoría ID:").grid(row=4, column=0)
        tk.Label(self.menu_productos, text="Proveedor ID:").grid(row=5, column=0)
        
        self.entry_descripcion = tk.Entry(self.menu_productos, textvariable=self.producto_Descripcion)
        self.entry_precio = tk.Entry(self.menu_productos, textvariable=self.producto_Precio)
        self.entry_stock = tk.Entry(self.menu_productos, textvariable=self.producto_Stock)
        self.entry_stock_min = tk.Entry(self.menu_productos, textvariable=self.producto_StockMin)
        self.combo_categoria = ttk.Combobox(self.menu_productos, textvariable=self.producto_Categoria)
        self.combo_proveedor = ttk.Combobox(self.menu_productos, textvariable=self.producto_Proveedor)
        
        self.entry_descripcion.grid(row=0, column=1)
        self.entry_precio.grid(row=1, column=1)
        self.entry_stock.grid(row=2, column=1)
        self.entry_stock_min.grid(row=3, column=1)
        self.combo_categoria.grid(row=4, column=1)
        self.combo_proveedor.grid(row=5, column=1)

        tk.Button(self.menu_productos, text="Nuevo", command=self.agregar_producto).grid(row=6, column=0)
        tk.Button(self.menu_productos, text="Modificar", command=self.modificar_producto).grid(row=6, column=1)
        tk.Button(self.menu_productos, text="Eliminar", command=self.eliminar_producto).grid(row=6, column=2)


        self.tree_productos = ttk.Treeview(self.menu_productos, 
                                           columns=("Descripción", "Precio", "Stock", "Stock Mínimo", "Categoría", "Proveedor"), 
                                           show='headings')
        
        self.tree_productos.heading("Descripción", text="Descripción")
        self.tree_productos.heading("Precio", text="Precio")
        self.tree_productos.heading("Stock", text="Stock")
        self.tree_productos.heading("Stock Mínimo", text="Stock Mínimo")
        self.tree_productos.heading("Categoría", text="Categoría")
        self.tree_productos.heading("Proveedor", text="Proveedor")
        self.tree_productos.grid(row=7, column=0, columnspan=3)
        self.tree_productos.bind("<Double-1>", self.seleccionar_producto)
        self.cargar_categorias_combobox()
        self.cargar_proveedores_combobox()
        self.cargar_productos()

    def cargar_categorias_combobox(self):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("SELECT catDescripcion FROM Categorias")
            categorias = cursor.fetchall()
            self.combo_categoria['values'] = categorias
        except:
            messagebox.showerror("Error", "No se pudieron cargar las categorías")

    def cargar_proveedores_combobox(self):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("SELECT provNom FROM Proveedores")
            proveedores = cursor.fetchall()
            self.combo_proveedor['values'] = proveedores
        except:
            messagebox.showerror("Error", "No se pudieron cargar los proveedores")

    def seleccionar_producto(self, event):
        item = self.tree_productos.selection()[0]
        self.producto_ID.set(self.tree_productos.item(item, "text"))
        self.producto_Descripcion.set(self.tree_productos.item(item, "values")[0])
        self.producto_Precio.set(self.tree_productos.item(item, "values")[1]) 
        self.producto_Stock.set(self.tree_productos.item(item, "values")[2])  
        self.producto_StockMin.set(self.tree_productos.item(item, "values")[3]) 
        self.producto_Categoria.set(self.tree_productos.item(item, "values")[4]) 
        self.producto_Proveedor.set(self.tree_productos.item(item, "values")[5])  

    def borrar_campos_producto(self):
        self.producto_ID.set("")
        self.producto_Descripcion.set("")
        self.producto_Precio.set("")
        self.producto_Stock.set("")
        self.producto_StockMin.set("")
        self.producto_Categoria.set("")
        self.producto_Proveedor.set("")
    
    def agregar_producto(self):
        descripcion = self.entry_descripcion.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        stock_min = self.entry_stock_min.get()
        categoria_desc = self.combo_categoria.get()
        proveedor_nom = self.combo_proveedor.get()
        
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("SELECT catId FROM Categorias WHERE catDescripcion = %s", (categoria_desc,))
            categoria_id = cursor.fetchone()[0] 

            cursor.execute("SELECT provId FROM Proveedores WHERE provNom = %s", (proveedor_nom,))
            proveedor_id = cursor.fetchone()[0] 

            cursor.execute(
                "INSERT INTO Productos (prodDesc, prodPrecio, prodStock, prodStockMin, catId, provId) VALUES (%s, %s, %s, %s, %s, %s)",
                (descripcion, precio, stock, stock_min, categoria_id, proveedor_id))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Producto agregado correctamente")
            self.cargar_productos()
            self.borrar_campos_producto()
        except:
            messagebox.showerror("ERROR", "No se pudo agregar el producto")

    def modificar_producto(self):
        prodId = self.producto_ID.get()
        if not prodId:
            messagebox.showwarning("Advertencia", "Seleccione un producto para modificar.")
            return
        
        descripcion = self.entry_descripcion.get()
        precio = self.entry_precio.get()
        stock = self.entry_stock.get()
        stock_min = self.entry_stock_min.get()
        categoria_desc = self.combo_categoria.get()
        proveedor_nom = self.combo_proveedor.get()
        
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("SELECT catId FROM Categorias WHERE catDescripcion = %s", (categoria_desc,))
            categoria_id = cursor.fetchone()[0] 

            cursor.execute("SELECT provId FROM Proveedores WHERE provNom = %s", (proveedor_nom,))
            proveedor_id = cursor.fetchone()[0] 
            
            cursor.execute(
                "UPDATE Productos SET prodDesc=%s, prodPrecio=%s, prodStock=%s, prodStockMin=%s, catId=%s, provId=%s WHERE prodId=%s",
                (descripcion, precio, stock, stock_min, categoria_id, proveedor_id, prodId))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Producto modificado correctamente")
            self.cargar_productos()
            self.borrar_campos_producto()
        except:
            messagebox.showerror("ERROR", "No se pudo modificar el producto")

    def eliminar_producto(self):
        prodId = self.producto_ID.get()
        if not prodId:
            messagebox.showwarning("Advertencia", "Seleccione un producto para eliminar.")
            return
        
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("DELETE FROM Productos WHERE prodId=%s", (prodId,))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Producto eliminado correctamente")
            self.cargar_productos()
            self.borrar_campos_producto()
        except:
            messagebox.showerror("ERROR", "No se pudo eliminar el producto")
        
    def cargar_productos(self):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute(
                "SELECT P.prodId, P.prodDesc, P.prodPrecio, P.prodStock, P.prodStockMin, C.catDescripcion, Pr.provNom "
                "FROM Productos P "
                "JOIN Categorias C ON P.catId = C.catId "
                "JOIN Proveedores Pr ON P.provId = Pr.provId"
            )
            registros = cursor.fetchall()
            self.tree_productos.delete(*self.tree_productos.get_children())
            for registro in registros:
                self.tree_productos.insert('', 'end', values=(
                    registro[1], 
                    registro[2], 
                    registro[3],  
                    registro[4], 
                    registro[5],  
                    registro[6]   
                ), text=registro[0]) 
        except:
            messagebox.showerror("ERROR", "No se pudieron cargar los productos")


# Categorias
    def categorias(self):
        self.menu_categorias = tk.Toplevel(self.root)
        self.menu_categorias.title("Categorías")
        
        self.catId = tk.StringVar()
        self.catDescripcion = tk.StringVar()
        
        tk.Label(self.menu_categorias, text="Descripción:").grid(row=0, column=0)
        
        self.entry_descripcion = tk.Entry(self.menu_categorias, textvariable=self.catDescripcion)
        self.entry_descripcion.grid(row=0, column=1)

        tk.Button(self.menu_categorias, text="Nuevo", command=self.agregar_categoria).grid(row=1, column=0)
        tk.Button(self.menu_categorias, text="Modificar", command=self.modificar_categoria).grid(row=1, column=1)
        tk.Button(self.menu_categorias, text="Eliminar", command=self.eliminar_categoria).grid(row=1, column=2)
        tk.Button(self.menu_categorias, text="Listar", command=self.cargar_categorias).grid(row=2, column=1)

        self.tree_categorias = ttk.Treeview(self.menu_categorias, columns=("ID", "Descripción"), show='headings')
        self.tree_categorias.heading("ID", text="ID")
        self.tree_categorias.heading("Descripción", text="Descripción")
        self.tree_categorias.grid(row=3, column=0, columnspan=3)


        self.tree_categorias.bind("<Double-1>", self.seleccionar_categoria)
        self.cargar_categorias()


    def seleccionar_categoria(self, event):
        item = self.tree_categorias.selection()[0]
        self.catId.set(self.tree_categorias.item(item, "values")[0])
        self.catDescripcion.set(self.tree_categorias.item(item, "values")[1])


    def borrar_campos_categoria(self):
        self.catId.set("")
        self.catDescripcion.set("")


    def agregar_categoria(self):
        descripcion = self.entry_descripcion.get()
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("INSERT INTO Categorias (catDescripcion) VALUES (%s)", (descripcion,))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Categoría agregada correctamente")
            self.cargar_categorias()
            self.borrar_campos_categoria()
        except:
            messagebox.showerror("Error", "No se pudo agregar la categoria")

    def cargar_categorias(self):
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("SELECT catId, catDescripcion FROM Categorias")
            registros = cursor.fetchall()
            for row in self.tree_categorias.get_children():
                self.tree_categorias.delete(row)
            for registro in registros:
                self.tree_categorias.insert('', 'end', values=registro)
        except:
            messagebox.showerror("Error", "No se pudieron mostrar las categorias")


    def modificar_categoria(self):
        catId = self.catId.get()
        if not catId:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para modificar.")
            return
        
        descripcion = self.entry_descripcion.get()
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute(
                "UPDATE Categorias SET catDescripcion=%s WHERE catId=%s",
                (descripcion, catId))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Categoría modificada correctamente")
            self.cargar_categorias()
            self.borrar_campos_categoria()
        except:
            messagebox.showerror("Error", "No se pudo modificar la categoria")


    def eliminar_categoria(self):
        catId = self.catId.get()
        if not catId:
            messagebox.showwarning("Advertencia", "Seleccione una categoría para eliminar.")
            return
        
        self.db.conexion()
        cursor = self.db.conexionBD.cursor()
        try:
            cursor.execute("DELETE FROM Categorias WHERE catId=%s", (catId,))
            self.db.conexionBD.commit()
            messagebox.showinfo("Éxito", "Categoría eliminada correctamente")
            self.cargar_categorias()
            self.borrar_campos_categoria()
        except:
            messagebox.showerror("Error", "No se pudo eliminar la categoria")


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