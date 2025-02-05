import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from customtkinter import *
from clientes import *
from form2 import *
from buscador import *

class Form1:
    global id_seleccionado

    def __init__(self, root):
        global textBoxFullName, textBoxPhone, textBoxVehicle, textBoxPatente, tree, textBoxBuscar

        try:
            # Crear el Frame para los datos del cliente
            groupBoxCliente = CTkFrame(root, corner_radius=10)
            groupBoxCliente.pack(pady=5)

            # Usar grid() para organizar los Labels y Entry en una sola fila
            CTkLabel(groupBoxCliente, text="Nombre:", font=("Arial", 13)).grid(row=0, column=0, padx=5, pady=5, sticky="w")
            textBoxFullName = CTkEntry(groupBoxCliente, width=250)
            textBoxFullName.grid(row=0, column=1, padx=5, pady=5)

            CTkLabel(groupBoxCliente, text="Teléfono:", font=("Arial", 13)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
            textBoxPhone = CTkEntry(groupBoxCliente, width=250)
            textBoxPhone.grid(row=1, column=1, padx=5, pady=5)

            CTkLabel(groupBoxCliente, text="Patente:", font=("Arial", 13)).grid(row=2, column=0, padx=5, pady=5, sticky="w")
            textBoxPatente = CTkEntry(groupBoxCliente, width=250)
            textBoxPatente.grid(row=2, column=1, padx=5, pady=5)

            CTkLabel(groupBoxCliente, text="Vehículo:", font=("Arial", 13)).grid(row=3, column=0, padx=5, pady=5, sticky="w")
            textBoxVehicle = CTkEntry(groupBoxCliente, width=250)
            textBoxVehicle.grid(row=3, column=1, padx=5, pady=5)

            # Crear el Frame para los botones
            groupBoxBotones = CTkFrame(root, corner_radius=10)
            groupBoxBotones.pack(pady=5)

            CTkButton(groupBoxBotones, text="Guardar", fg_color='#8AC859', command=self.guardarRegistros, width=100).grid(row=0, column=0, padx=5, pady=5)
            CTkButton(groupBoxBotones, text="Modificar", fg_color='#BBCD5F', command=self.modificarRegistros, width=100).grid(row=0, column=1, padx=5, pady=5)
            CTkButton(groupBoxBotones, text="Eliminar", fg_color='#E05349', command=self.eliminarRegistros, width=100).grid(row=0, column=2, padx=5, pady=5)
            CTkButton(groupBoxBotones, text="Limpiar", command=self.limpiarCampos, width=100).grid(row=0, column=3, padx=5, pady=5)

            # Crear el Frame para la lista de clientes
            groupBoxLista = CTkFrame(root, corner_radius=10)
            groupBoxLista.pack(pady=5)

            # Crear un Frame contenedor para el Treeview y el scrollbar
            treeFrame = CTkFrame(groupBoxLista)
            treeFrame.pack(pady=5)

            # Crear el scrollbar
            treeScrollbar = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrollbar.pack(side="right", fill="y")

            # Crear el Treeview
            tree = ttk.Treeview(treeFrame, style="Custom.Treeview", columns=("Nombre completo", "Teléfono", "Patente", "Vehículo"), show='headings', height=10, yscrollcommand=treeScrollbar.set)
            tree.pack(side="left", fill="both", expand=True)

            # Configurar el scrollbar para que controle el Treeview
            treeScrollbar.config(command=tree.yview)

            # Configurar columnas y encabezados del Treeview
            tree.column("#1", anchor=CENTER, width=200)
            tree.heading("#1", text="Nombre y Apellido")
            tree.column("#2", anchor=CENTER, width=200)
            tree.heading("#2", text="Teléfono")
            tree.column("#3", anchor=CENTER, width=200)
            tree.heading("#3", text="Patente")
            tree.column("#4", anchor=CENTER, width=200)
            tree.heading("#4", text="Vehículo")

            # Insertar datos en el Treeview (simulación)
            for row in CClientes.mostrarClientes():
                tree.insert("", "end", values=row[1:], tags=(row[0],))

            # Configurar evento para selección en el Treeview
            tree.bind("<<TreeviewSelect>>", self.seleccionarRegistros)

            #Frame para buscar
            groupBoxBuscar = CTkFrame(root, corner_radius=10)
            groupBoxBuscar.pack(pady=5)

            CTkLabel(groupBoxBuscar, text="Cliente:", font=("Arial", 13)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            textBoxBuscar = CTkEntry(groupBoxBuscar, width=300)
            textBoxBuscar.grid(row=0, column=1, pady=5, padx=5)
            CTkButton(groupBoxBuscar, text='Buscar', command=self.buscarCliente).grid(row=0, column=2, pady=5, padx=5)
            CTkButton(groupBoxBuscar, text='Ver todos', command=self.actualizarTreeView).grid(row=0, column=3, pady=5, padx=5)
            
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
                nombre_completo = textBoxFullName.get().title()

            # Validar teléfono
            if not textBoxPhone.get().isdigit():  # Verificar que sean solo números
                messagebox.showinfo("Error de datos", "El teléfono debe contener solo números.")
                return
            elif len(textBoxPhone.get()) < 10 or len(textBoxPhone.get()) > 13:  
                # Verificar rango
                messagebox.showinfo("Error de datos", "El teléfono debe tener entre 10 y 13 dígitos.")
                return
            else:
                telefono = textBoxPhone.get()

            # Validar patente
            if len(textBoxPatente.get()) < 6 or len(textBoxPatente.get()) > 8 :  # Ejemplo: Patentes argentinas suelen tener 6-7 caracteres
                messagebox.showinfo("Error de datos", "La patente debe tener entre 6 y 8 caracteres.")
                return
            elif CClientes.verificarPatente(textBoxPatente.get().upper()):
                messagebox.showinfo("Error de datos", "La patente ya está registrada.")
                return
            else:
                patente = textBoxPatente.get().upper()

            # Validar vehículo
            if len(textBoxVehicle.get().strip()) < 3:  # Nombre del vehículo demasiado corto
                messagebox.showinfo("Error de datos", "El nombre del vehículo debe tener al menos 3 caracteres.")
                return
            else:
                vehiculo = textBoxVehicle.get().upper()


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
            textBoxBuscar.delete(0, END)

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
            nombre_completo = textBoxFullName.get().title()

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
                    patente = textBoxPatente.get().upper() 
            else:
                # Si la patente no cambia, mantener la patente actual
                patente = datos_cliente[3]

            # Validación del nombre del vehículo
            if len(textBoxVehicle.get().strip()) < 3:  
                messagebox.showinfo("Error de datos", "El nombre del vehículo debe tener al menos 3 caracteres.")
                return
            vehiculo = textBoxVehicle.get().upper()

            # Actualización de los datos del cliente
            CClientes.modificarClientes(id_seleccionado, nombre_completo, telefono, patente, vehiculo)
            messagebox.showinfo("Información:", "Los datos fueron actualizados.")

            self.actualizarTreeView()
            Form2.actualizarTreeView()
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

    def buscarCliente(self):
        try:
            tree.delete(*tree.get_children())

            # Obtener el valor de búsqueda
            cliente = textBoxBuscar.get()

            if not cliente:
                messagebox.showinfo("Información", "Ingrese un cliente.")
                return

            # Buscar clientes
            datos = CClientes.buscarCliente(cliente)
            print(f'DATOS CLIENTES: {datos}')

            if datos:
                for row in datos:
                    tree.insert("", "end", values=row[1:], tags=(row[0],))
            else: 
                messagebox.showinfo("Información", "No hay clientes con ese nombre.")
            self.limpiarCampos()
            
        except ValueError as error:
            print("Error al eliminar los datos: {}".format(error))
