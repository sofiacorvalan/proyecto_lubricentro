import tkinter as tk
import customtkinter as ctk
from customtkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import *
from form1 import Form1
from form2 import Form2
from buscador import CBuscador
from conexion import *

class MainApp:

    column_widths = {
        "Nombre y Apellido": 150,
        "Patente": 90,
        "Vehículo": 150,
        "KMs": 90,
        "Próx. Servicio": 90,
        "Servicio": 150,
        "Detalles": 250,
        "Fecha": 90,
        "Observaciones": 350
    }

    tree = None
    
    def __init__(self, root):
        """ Inicializa la ventana principal con una caja de búsqueda y dos botones."""
        self.root = root
        self.root.title("WILLY GARAGE")
        self.root.geometry("1200x600")
        self.root.iconbitmap('bandera1.ico') 
        set_default_color_theme("green")   
        
        self.switch = CTkSwitch(root, text="Tema", command=self.cambiarTema)
        self.switch.pack(anchor="ne", pady=10, padx=10)  # "ne" lo coloca en la esquina superior derecha
        
        self.tab_control = CTkTabview(root)
        self.tab_control.pack(expand=1, fill="both")

        # Agregar las pestañas al Notebook
        self.tab_control.add( 'Inicio')
        self.tab_control.add( 'Clientes')
        self.tab_control.add('Servicios')

        self.tab_inicio = self.tab_control.tab('Inicio')
        self.tab_clientes = self.tab_control.tab('Clientes')
        self.tab_servicios = self.tab_control.tab('Servicios')
    
        # Caja de búsqueda por patente
        frame1 = CTkFrame(self.tab_inicio)
        frame1.pack(pady=5)

        CTkLabel(frame1, text="Buscar por patente: ", font=('Arial',15)).pack(side='left', pady=5)

        self.caja_buscar_patente = CTkEntry(frame1, width=300, font=("Arial", 12))
        self.caja_buscar_patente.pack(side='left', pady=5)
    
        CTkButton(frame1, text='Buscar', width=85, command=self.buscadorPatente).pack(side='left', pady=5)

        # Caja de búsqueda por vehiculo
        frame2 = CTkFrame(self.tab_inicio)
        frame2.pack(pady=5)

        CTkLabel(frame2, text="Buscar por vehículo: ", font=('Arial',15, )).pack(side='left', pady=5)

        self.caja_buscar_vehiculo = CTkEntry(frame2, width=300, font=("Arial", 12))
        self.caja_buscar_vehiculo.pack(side='left', pady=5)
    
        CTkButton(frame2, text='Buscar', width=85, command=self.buscadorVehiculo).pack(side='left', pady=5)
        
        # Caja de búsqueda por cliente
        frame3 = CTkFrame(self.tab_inicio)
        frame3.pack(pady=5)

        CTkLabel(frame3, text="Buscar por cliente: ", font=('Arial',15)).pack(side='left',pady=5)

        self.caja_buscar_cliente = CTkEntry(frame3, width=300, font=("Arial", 12))
        self.caja_buscar_cliente.pack(side='left', pady=5)
    
        CTkButton(frame3, text='Buscar', width=85, command=self.buscadorCliente).pack(side='left', pady=5)

        #Estilizar los treeView
        style = ttk.Style()
        style.theme_use('clam')
        # Configuración del estilo para Treeview
        style.configure("Custom.Treeview",
                        font=("Arial", 10),  # Cambiar la fuente
                        foreground="black",  # Color del texto
                        background="white",  # Color de fondo de las filas
                        rowheight=25)  # Altura de las filas

        # Estilizar las columnas de los encabezados
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 11, "bold"),  # Fuente del encabezado
                        foreground="white",  # Color del texto del encabezado
                        background="#2FA572")
        
        style.map("Custom.Treeview", background=[('selected', '#979DA2')])

        self.frame4 = CTkFrame(self.tab_inicio, corner_radius=10)
        self.frame4.pack(pady=5)

        Form1(self.tab_clientes)
    
        Form2(self.tab_servicios)  

    def cambiarTema(self):
        if self.switch.get():
            set_appearance_mode('light')
            print('claro')
        else:
            print('oscuro')
            set_appearance_mode('dark')

    def destroy_treeview(self):
        if self.tree:
            self.tree.destroy()
            self.tree = None

    def buscadorPatente(self):
        try:
            self.destroy_treeview()
            patente = self.caja_buscar_patente.get() 
            print(f"Buscando patente: {patente}")

            if not patente:
                messagebox.showinfo("Sin resultados", "Ingrese un numero de patente") 
            else: 
                resultados_patente = CBuscador.buscarPorPatente(patente)
                print(f"Resultado de búsqueda: {resultados_patente}")

                if not resultados_patente:
                    messagebox.showinfo("Sin resultados", "No hay servicios registrados para esta patente")
                else:
                    self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs", "Próx. Servicio", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings')  

                    for i, column in enumerate(self.tree["columns"]):
                        width = self.column_widths.get(column, 150)  
                        self.tree.column(f"#{i+1}", anchor="center", width=width)
                        self.tree.heading(f"#{i+1}", text=column)

                    self.tree.pack(side='left', fill='both', expand=True)
                    self.actualizarTreeView(resultados_patente)
            
            self.caja_buscar_patente.delete(0, END)

        except ValueError as error:
            print(f'Error al consultar patente: {error}')
    
    def buscadorVehiculo(self):
        try:
            self.destroy_treeview()       
            vehiculo = self.caja_buscar_vehiculo.get()
            print(f'vehiculo:{vehiculo}')

            if not vehiculo:
                messagebox.showinfo("Sin resultados", "Ingrese un modelo de vehiculo")
            else:
                resultados_vehiculo = CBuscador.buscarPorVehiculo(vehiculo)
                print(f'resultado vehiculo:{vehiculo}')

                if not resultados_vehiculo:
                    messagebox.showinfo("Sin resultados", "Este modelo de vehiculo no tiene servicios registrados.")
                else:       
                    self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs", "Próx. Servicio", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=15)  

                    for i, column in enumerate(self.tree["columns"]):
                        width = self.column_widths.get(column, 150)  
                        self.tree.column(f"#{i+1}", anchor="center", width=width)
                        self.tree.heading(f"#{i+1}", text=column)

                    self.tree.pack(side='left', fill='both', expand=True)
                    self.actualizarTreeView(resultados_vehiculo)
        
            self.caja_buscar_vehiculo.delete(0, END)
            
        except ValueError as error:
            print(f'Error al buscar por vehiculo: {error}')

    def buscadorCliente(self):
        try:
            self.destroy_treeview()

            # Obtener los valores de las cajas de búsqueda
            cliente = self.caja_buscar_cliente.get()
            print(f'cliente: {cliente}')
            
            # Si no hay resultados, mostrar el mensaje
            if not cliente:
                messagebox.showinfo("Sin resultados", "Ingrese el nombre de un cliente.")
            else: 
                resultados_cliente = CBuscador.buscarPorCliente(cliente)
                print(f'resultado cliente: {resultados_cliente}')

                if not resultados_cliente:
                    messagebox.showinfo("Sin resultados", "No hay servicios registrados a nombre del cliente.")
                else:
                    self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs", "Próx. Servicio", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=15)

                    for i, column in enumerate(self.tree["columns"]):
                        width = self.column_widths.get(column, 150)  # Usar un valor predeterminado si no está en el diccionario
                        self.tree.column(f"#{i+1}", anchor="center", width=width)
                        self.tree.heading(f"#{i+1}", text=column)

                    self.tree.pack(side='left', fill='both', expand=True)
                    self.actualizarTreeView(resultados_cliente)
            
            self.caja_buscar_cliente.delete(0, END)

        except ValueError as error:
            print(f'Error al consultar por cliente: {error}')

    def actualizarTreeView(self,data):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)
            for row in data:
                "Nombre y Apellido", "Patente", "Vehículo", "KMs", "Próx. Servicio", "Servicio", "Detalles", "Fecha", "Observaciones"
                values = (row[0], row[2], row[4], row[3], row[11], row[5], row[6], row[7], row[8])
                self.tree.insert("", "end", values=values)
        except ValueError as error:
            print("Error al actualizar tabla {}".format(error))
    
    def open_form1(self):
        """Abre el formulario clientes."""
        Form1(root.tab_clientes)
    def open_form2(self):
        """Abre el formulario servicios."""
        Form2(root.tab_servicios)
 
if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
