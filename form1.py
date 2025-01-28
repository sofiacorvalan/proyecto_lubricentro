import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from clientes import *
from form2 import *
from buscador import *

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
            tree = ttk.Treeview(groupBoxLista, style="Custom.Treeview", columns=("Nombre completo", "Teléfono", "Patente", "Vehículo"), show='headings', height=15)
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
            # Verificar que todos los campos tengan datos
            if not all([textBoxFullName.get(), textBoxPhone.get(), textBoxVehicle.get(), textBoxPatente.get()]):
                messagebox.showinfo("Error de datos", "Todos los campos son obligatorios. Por favor, complételos.")
                return  # Salir de la función si falta algún dato

            # Validar nombre completo
            if len(textBoxFullName.get().strip()) < 2:  # Nombre demasiado corto
                messagebox.showinfo("Error de datos", "El nombre completo debe tener al menos 2 caracteres.")
                return
            else: 
                nombre_completo = textBoxFullName.get()

            # Validar teléfono
            if not textBoxPhone.get().isdigit():  # Verificar que sean solo números
                messagebox.showinfo("Error de datos", "El teléfono debe contener solo números.")
                return
            elif len(textBoxPhone.get()) < 10 or len(textBoxPhone.get()) > 13:  # Verificar rango
                messagebox.showinfo("Error de datos", "El teléfono debe tener entre 10 y 13 dígitos.")
                return
            else:
                telefono = textBoxPhone.get()

            # Validar patente
            if len(textBoxPatente.get()) < 6 or len(textBoxPatente.get()) > 8 :  # Ejemplo: Patentes argentinas suelen tener 6-7 caracteres
                messagebox.showinfo("Error de datos", "La patente debe tener entre 6 y 8 caracteres.")
                return
            elif CClientes.verificarPatente(textBoxPatente.get()):
                messagebox.showinfo("Error de datos", "La patente ya está registrada.")
                return
            else:
                patente = textBoxPatente.get()

            # Validar vehículo
            if len(textBoxVehicle.get().strip()) < 3:  # Nombre del vehículo demasiado corto
                messagebox.showinfo("Error de datos", "El nombre del vehículo debe tener al menos 3 caracteres.")
                return
            else:
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

            tree.selection_remove(tree.selection())
            tree.focus("")

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
                print(f"Id:{id_seleccionado}")
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
            # Verificar que todos los campos estén completos
            if not all([textBoxFullName.get(), textBoxPhone.get(), textBoxVehicle.get(), textBoxPatente.get()]):
                messagebox.showinfo("Error de datos", "Todos los campos son obligatorios. Por favor, complételos.")
                return  # Salir de la función si falta algún dato

            # Validación del nombre
            if len(textBoxFullName.get()) < 2:  
                messagebox.showinfo("Error de datos", "El nombre completo debe tener al menos 2 caracteres.")
                return
            nombre_completo = textBoxFullName.get()

            # Validación del teléfono
            if not textBoxPhone.get().isdigit(): 
                messagebox.showinfo("Error de datos", "El teléfono debe contener solo números.")
                return
            elif len(textBoxPhone.get()) < 10 or len(textBoxPhone.get()) > 13:  
                messagebox.showinfo("Error de datos", "El teléfono debe tener entre 10 y 13 dígitos.")
                return
            telefono = textBoxPhone.get()

            # Obtenemos los datos actuales del cliente
            datos_cliente = CClientes.mostrarClienteID(id_seleccionado)  
            print(f'Datos del cliente: {datos_cliente}')
            
            # Validación de la patente
            if len(textBoxPatente.get()) < 6 or len(textBoxPatente.get()) > 8: 
                messagebox.showinfo("Error de datos", "La patente debe tener entre 6 y 8 caracteres.")
                return

            # Verificar si la patente ingresada es diferente de la actual
            if textBoxPatente.get() != datos_cliente[3]:
                print(f"Patente nueva ingresada: {textBoxPatente.get()}")
                
                print('A VER:', CBuscador.verificarServicio(textBoxPatente.get()))

                # Verificar si la nueva patente tiene servicios vinculados
                if CBuscador.verificarServicio(datos_cliente[3]):
                    print("La patente tiene servicios vinculados.")
                    messagebox.showinfo("Aviso", "La patente no se puede modificar porque ya tiene servicios vinculados.")
                    patente = datos_cliente[3]  # Mantener la patente actual
                else:
                    print("La patente no tiene servicios vinculados.")
                    patente = textBoxPatente.get()  # Usar la nueva patente si no tiene servicios vinculados
            else:
                # Si la patente no cambia, mantener la patente actual
                patente = datos_cliente[3]

            # Validación del nombre del vehículo
            if len(textBoxVehicle.get().strip()) < 3:  
                messagebox.showinfo("Error de datos", "El nombre del vehículo debe tener al menos 3 caracteres.")
                return
            vehiculo = textBoxVehicle.get()

            # Actualización de los datos del cliente
            CClientes.modificarClientes(id_seleccionado, nombre_completo, telefono, patente, vehiculo)
            messagebox.showinfo("Información:", "Los datos fueron actualizados.")

            self.actualizarTreeView()
            self.limpiarCampos()

        except ValueError as error:
            print("Error al actualizar los datos:", error)


    def eliminarRegistros(self):
        global id_seleccionado

        try:
            
            respuesta = messagebox.askquestion(
            "¿Está seguro que desea eliminar?",
            "Se eliminará el cliente y todos los servicios vinculados a esta patente.",
            icon="warning")

            if respuesta == "yes":
                CClientes.eliminarClientes(id_seleccionado)
                messagebox.showinfo("Información:", "Los datos fueron eliminados.")
                self.actualizarTreeView()
                self.limpiarCampos()
                Form2.actualizarTreeView()

        except ValueError as error:
            print("Error al eliminar los datos: {}".format(error))
