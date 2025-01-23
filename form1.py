import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from clientes import *

class Form1:
    global ancho, id_seleccionado
    ancho = 140

    def __init__(self, root):
        global textBoxFullName, textBoxPhone, textBoxVehicle, textBoxPatente, tree

        try:
            # Crear el Frame para los datos del cliente
            groupBoxCliente = CTkFrame(root, corner_radius=10)
            groupBoxCliente.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            # Título para el Frame
            CTkLabel(groupBoxCliente, text="Datos del cliente:", font=("Arial", 15, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 10))

            # Campos de entrada para los datos
            CTkLabel(groupBoxCliente, text="Nombre:", font=("Arial", 13)).grid(row=1, column=0, sticky="w", padx=10, pady=5)
            textBoxFullName = CTkEntry(groupBoxCliente, width=200)
            textBoxFullName.grid(row=1, column=1, padx=10, pady=5)

            CTkLabel(groupBoxCliente, text="Teléfono:", font=("Arial", 13)).grid(row=2, column=0, sticky="w", padx=10, pady=5)
            textBoxPhone = CTkEntry(groupBoxCliente, width=200)
            textBoxPhone.grid(row=2, column=1, padx=10, pady=5)

            CTkLabel(groupBoxCliente, text="Patente:", font=("Arial", 13)).grid(row=3, column=0, sticky="w", padx=10, pady=5)
            textBoxPatente = CTkEntry(groupBoxCliente, width=200)
            textBoxPatente.grid(row=3, column=1, padx=10, pady=5)

            CTkLabel(groupBoxCliente, text="Vehículo:", font=("Arial", 13)).grid(row=4, column=0, sticky="w", padx=10, pady=5)
            textBoxVehicle = CTkEntry(groupBoxCliente, width=200)
            textBoxVehicle.grid(row=4, column=1, padx=10, pady=5)

            # Botones para acciones
            CTkButton(groupBoxCliente, text="Guardar", command=self.guardarRegistros).grid(row=5, column=0, pady=10, padx=5)
            CTkButton(groupBoxCliente, text="Modificar", command=self.modificarRegistros).grid(row=5, column=1, pady=10, padx=5)
            CTkButton(groupBoxCliente, text="Eliminar", command=self.eliminarRegistros).grid(row=6, column=0, pady=10, padx=5)
            CTkButton(groupBoxCliente, text="Limpiar", command=self.limpiarCampos).grid(row=6, column=1, pady=10, padx=5)

            # Crear el Frame para la lista de clientes
            groupBoxLista = CTkFrame(root, corner_radius=10)
            groupBoxLista.grid(row=0, column=1, padx=10, pady=10, sticky="ne")

            # Título para el Frame
            CTkLabel(groupBoxLista, text="Lista de clientes:", font=("Arial", 15, 'bold') ).pack(pady=(0, 10))

            # Crear un Treeview
            tree = ttk.Treeview(groupBoxLista, columns=("Nombre completo", "Teléfono", "Patente", "Vehículo"), show='headings', height=15)
            tree.column("#1", anchor=CENTER, width=ancho)
            tree.heading("#1", text="Nombre y Apellido")
            tree.column("#2", anchor=CENTER, width=ancho)
            tree.heading("#2", text="Teléfono")
            tree.column("#3", anchor=CENTER, width=ancho)
            tree.heading("#3", text="Patente")
            tree.column("#4", anchor=CENTER, width=200)
            tree.heading("#4", text="Vehículo")

            # Insertar datos en el Treeview (simulación)
            for row in CClientes.mostrarClientes():
                tree.insert("", "end", values=row[1:], tags=(row[0],))

            tree.bind("<<TreeviewSelect>>", self.seleccionarRegistros)
            tree.pack(pady=5)

        except ValueError as error:
            print(f"Error al mostrar la interfaz, error: {error}")

    def guardarRegistros(self):
        global textBoxFullName, textBoxPhone, textBoxVehicle, textBoxPatente

        try:
            if not all([textBoxFullName, textBoxPhone, textBoxVehicle, textBoxPatente]):
                print("Los widget no están inicializados")
                return
            nombre_completo = textBoxFullName.get()
            telefono = textBoxPhone.get()
            patente = textBoxPatente.get()
            vehiculo = textBoxVehicle.get()

            CClientes.ingresarClientes(nombre_completo, telefono, patente, vehiculo)
            messagebox.showinfo("Información:", "Los datos fueron guardados")
            
            self.actualizarTreeView()
            self.limpiarCampos()
        except ValueError as error:
            print("Error al ingresar los datos: {}".format(error))

    def limpiarCampos(self):
        try:
            textBoxFullName.delete(0, END)
            textBoxPhone.delete(0, END)
            textBoxVehicle.delete(0, END)
            textBoxPatente.delete(0, END)
        except ValueError as error:
            print(f"No se pudieron borrar los campos de entrada: {error}")

    def actualizarTreeView(self):
        global tree

        try:
            tree.delete(*tree.get_children())

            for row in CClientes.mostrarClientes():
                tree.insert("", "end", values=row[1:], tags=(row[0],))
            
        except ValueError as error:
            print("Error al actualizar tabla: {}".format(error))

    def seleccionarRegistros(self, event=None):
        global id_seleccionado
        try:
            itemSeleccionado = tree.focus()

            if itemSeleccionado: 
                id_seleccionado = tree.item(itemSeleccionado, "tags")[0]
                values = tree.item(itemSeleccionado)['values']
                
                textBoxFullName.delete(0, END)
                textBoxFullName.insert(0, values[0])
                textBoxPhone.delete(0, END)
                textBoxPhone.insert(0, values[1])
                textBoxPatente.delete(0, END)
                textBoxPatente.insert(0, values[2])
                textBoxVehicle.delete(0, END)
                textBoxVehicle.insert(0, values[3])
        
        except ValueError as error:
            print("Error al seleccionar registro: {}".format(error))

    def modificarRegistros(self):
        global textBoxFullName, textBoxPhone, textBoxPatente, textBoxVehicle
        
        try:
            if not all([textBoxFullName, textBoxPhone, textBoxPatente, textBoxVehicle]):
                print("Los widget no están inicializados")
                return
            
            nombre_completo = textBoxFullName.get()
            telefono = textBoxPhone.get()
            patente = textBoxPatente.get()
            vehiculo = textBoxVehicle.get()

            CClientes.modificarClientes(id_seleccionado, nombre_completo, telefono, patente, vehiculo)
            messagebox.showinfo("Información:", "Los datos fueron actualizados.")

            self.actualizarTreeView()
            self.limpiarCampos()

        except ValueError as error:
            print("Error al actualizar los datos: {}".format(error))

    def eliminarRegistros(self):
        global id_seleccionado

        try:
            CClientes.eliminarClientes(id_seleccionado)
            messagebox.showinfo("Información:", "Los datos fueron eliminados.")

            self.actualizarTreeView()
            self.limpiarCampos()

        except ValueError as error:
            print("Error al eliminar los datos: {}".format(error))
