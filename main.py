import os
import shutil
from datetime import datetime, timedelta

def backup_db():
    # Ruta de la base de datos original
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/lubricentrodb.sqlite')
    
    # Carpeta donde se guardarán los backups
    backup_folder = os.path.join(os.path.dirname(db_path), 'backups')
    os.makedirs(backup_folder, exist_ok=True)

    # Nombre del archivo de backup con la fecha de hoy
    today = datetime.now().strftime('%Y-%m-%d')
    backup_file = os.path.join(backup_folder, f'backup_{today}.sqlite')

    # Evitar duplicados si ya existe el backup de hoy
    if not os.path.exists(backup_file):
        shutil.copy2(db_path, backup_file)
        print(f'✅ Backup creado: {backup_file}')
    else:
        print('ℹ️ El backup de hoy ya existe.')

    # Llamar a la función para limpiar backups antiguos
    clean_old_backups(backup_folder)

def clean_old_backups(backup_folder, days_to_keep=7):
    # Fecha límite: cualquier archivo anterior a esto será eliminado
    limit_date = datetime.now() - timedelta(days=days_to_keep)

    # Recorrer los archivos de la carpeta de backups
    for filename in os.listdir(backup_folder):
        if filename.startswith('backup_') and filename.endswith('.sqlite'):
            file_path = os.path.join(backup_folder, filename)
            
            # Obtener la fecha del backup desde el nombre del archivo
            try:
                date_str = filename.replace('backup_', '').replace('.sqlite', '')
                file_date = datetime.strptime(date_str, '%Y-%m-%d')
                
                # Eliminar si el archivo es más antiguo que la fecha límite
                if file_date < limit_date:
                    os.remove(file_path)
                    print(f'🗑️ Backup eliminado: {filename}')
            except ValueError:
                # Ignorar archivos que no cumplan con el formato esperado
                pass

# Llamar a la función de backup antes de iniciar la app
backup_db()

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
        "Vehículo": 200,
        "KMs": 85,
        "Servicio": 150,
        "Detalles": 200,
        "Fecha": 85,
        "Observaciones": 350
    }

    tree = None
    
    def __init__(self, root):
        self.root = root
        self.root.title("WILLY GARAGE")
        self.root.geometry("1200x600")
        # Verifica si el programa se está ejecutando desde el ejecutable
        if getattr(sys, 'frozen', False):
            # Si es el ejecutable, usa el directorio temporal generado por PyInstaller
            app_path = sys._MEIPASS
        else:
            # Si es el script original, usa el directorio del script
            app_path = os.path.dirname(os.path.abspath(__file__))

        # Construye la ruta correcta para el archivo .ico
        icon_path = os.path.join(app_path, "bandera1.ico")

        # Establece el ícono en la ventana
        self.root.iconbitmap(icon_path) 
        set_default_color_theme("green")   
        
        self.switch = CTkSwitch(root, text="Tema", command=self.cambiarTema)
        self.switch.pack(anchor="ne", pady=10, padx=10) 
        
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

        CTkButton(self.tab_inicio, text="Ver todos los servicios del día", command=self.verServiciosDiarios).pack(pady=5)

        #Estilizar los treeView
        style = ttk.Style()
        style.theme_use('clam')

        # Configuración del estilo para Treeview
        style.configure("Custom.Treeview",
                        font=("Arial", 10),  
                        foreground="black",  
                        background="white",  
                        rowheight=25) 

        # Estilizar las columnas de los encabezados
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 11, "bold"),  
                        foreground="white", 
                        background="#2FA572")
        
        style.map("Custom.Treeview", background=[('selected', '#979DA2')])

        self.frame4 = CTkFrame(self.tab_inicio, corner_radius=10)
        self.frame4.pack(pady=5)

        Form1(self.tab_clientes)
        Form2(self.tab_servicios)  
        
        #Footer
        footer = CTkFrame(root, height=30, corner_radius=0)
        footer.pack(side="bottom", fill="x")

        footer_label = CTkLabel(footer, text='Desarrollado por Sofía Corvalán ♥ corvalansofia1@gmail.com')
        footer_label.pack()

    def cambiarTema(self):
        current_mode = get_appearance_mode()

        if current_mode.lower() == 'light':  
            set_appearance_mode('dark')
            print('oscuro')
        else:
            set_appearance_mode('light')
            print('claro')

    def destroy_treeview(self):
        if self.tree:
            self.tree.destroy()
            self.tree = None

    def verServiciosDiarios(self):
        try:
            self.destroy_treeview()
            resultados = CBuscador.mostrarServiciosDiarios()
            print(f"Resultado de búsqueda: {resultados}")

            if not resultados:
                messagebox.showinfo("Sin resultados", "No hay servicios registrados el día de hoy.")
            else:
                self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs",  "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=13)  

                for i, column in enumerate(self.tree["columns"]):
                    width = self.column_widths.get(column, 150)  
                    self.tree.column(f"#{i+1}", anchor="center", width=width)
                    self.tree.heading(f"#{i+1}", text=column)

                self.tree.pack(side='left', fill='both', expand=True)
                self.actualizarTreeView(resultados)

        except ValueError as error:
            print(f'Error al mostrar servicios diarios{error}')
    
    def buscadorPatente(self):
        try:
            self.destroy_treeview()
            patente = self.caja_buscar_patente.get().upper() 
            print(f"Buscando patente: {patente}")

            if not patente:
                messagebox.showinfo("Sin resultados", "Ingrese un numero de patente") 
            else: 
                resultados_patente = CBuscador.buscarPorPatente(patente)
                print(f"Resultado de búsqueda: {resultados_patente}")

                if not resultados_patente:
                    messagebox.showinfo("Sin resultados", "No hay servicios registrados para esta patente")
                else:
                    self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=13)  

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
            vehiculo = self.caja_buscar_vehiculo.get().upper()
            print(f'vehiculo:{vehiculo}')

            if not vehiculo:
                messagebox.showinfo("Sin resultados", "Ingrese un modelo de vehiculo")
            else:
                resultados_vehiculo = CBuscador.buscarPorVehiculo(vehiculo)
                print(f'resultado vehiculo:{vehiculo}')

                if not resultados_vehiculo:
                    messagebox.showinfo("Sin resultados", "Este modelo de vehiculo no tiene servicios registrados.")
                else:       
                    self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=13)
                      
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

            cliente = self.caja_buscar_cliente.get().title()
            print(f'cliente: {cliente}')
            
            if not cliente:
                messagebox.showinfo("Sin resultados", "Ingrese el nombre de un cliente.")
            else: 
                resultados_cliente = CBuscador.buscarPorCliente(cliente)
                print(f'resultado cliente: {resultados_cliente}')

                if not resultados_cliente:
                    messagebox.showinfo("Sin resultados", "No hay servicios registrados a nombre del cliente.")
                else:
                    self.tree = ttk.Treeview(self.frame4, style="Custom.Treeview", columns=("Nombre y Apellido", "Patente", "Vehículo", "KMs", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=13)

                    for i, column in enumerate(self.tree["columns"]):
                        width = self.column_widths.get(column, 150) 
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
                "Nombre y Apellido", "Patente", "Vehículo", "KMs", "Servicio", "Detalles", "Fecha", "Observaciones"
                values = (row[0], row[2], row[4], row[3], row[5], row[6], row[7], row[8])
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
