import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from customtkinter import *
from servicios import *
from datetime import date
from clientes import *
from buscador import *

class Form2:
    id_servicio=None

    def __init__(self, root):
        
        global textBoxPatente, textBoxKM, textBoxCambioAceite, textBoxFiltroAceite, textBoxFiltroAire, textBoxBuscarPatente
        global textBoxFiltroComb, textBoxFiltroHab, textBoxObservaciones
        global varCambioAceite, varFiltroAceite, varFiltroAire, varFiltroComb, varFiltroHab,tree, habilitar_entry
        global cambioAceiteCheck ,filtroAceiteCheck,filtroAireCheck, filtroCombCheck, filtroHabCheck, id_servicio
        
        def habilitar_entry(var, entry):
            """Habilita o deshabilita el Entry según el estado del Checkbutton"""
            if var.get()== 1:
                entry.configure(state="normal")
            else:
                entry.delete(0, END)
                entry.configure(state="disabled")

        try:
            # Frame principal
            groupBox = CTkFrame(root, corner_radius=10)
            groupBox.pack(padx=5)

            # Patente
            CTkLabel(groupBox, text="Patente:", font=("Arial", 13)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            textBoxPatente = CTkEntry(groupBox, width=200)
            textBoxPatente.grid(row=0, column=1, padx=10, pady=5)

            # Kilómetros
            CTkLabel(groupBox, text="Kilómetros:", font=("Arial", 13)).grid(row=1, column=0, sticky='w', padx=10, pady=5)
            textBoxKM = CTkEntry(groupBox, width=200)
            textBoxKM.grid(row=1, column=1, padx=10, pady=5)

            # Observaciones
            CTkLabel(groupBox, text="Observaciones:", font=("Arial", 13)).grid(row=2, column=0, sticky='w', padx=10, pady=5)
            textBoxObservaciones = CTkEntry(groupBox, width=200)
            textBoxObservaciones.grid(row=2, column=1, padx=10, pady=5)

            # Cambio de aceite
            varCambioAceite = IntVar()
            cambioAceiteCheck = CTkCheckBox(groupBox, text="Cambio aceite", variable=varCambioAceite, command=lambda: habilitar_entry(varCambioAceite, textBoxCambioAceite))
            cambioAceiteCheck.grid(row=3, column=0, sticky='w', padx=10, pady=5)
            textBoxCambioAceite = CTkEntry(groupBox, width=200)
            textBoxCambioAceite.grid(row=3, column=1, padx=10, pady=5)
            textBoxCambioAceite.configure(state="disabled")

            # Filtro de aceite
            varFiltroAceite = IntVar()
            filtroAceiteCheck = CTkCheckBox(groupBox, text="Filtro de aceite", variable=varFiltroAceite, command=lambda: habilitar_entry(varFiltroAceite, textBoxFiltroAceite))
            filtroAceiteCheck.grid(row=0, column=2, sticky='w', padx=10, pady=5)
            textBoxFiltroAceite = CTkEntry(groupBox, width=200)
            textBoxFiltroAceite.grid(row=0, column=3, padx=10, pady=5)
            textBoxFiltroAceite.configure(state="disabled")

            # Filtro de aire
            varFiltroAire = IntVar()
            filtroAireCheck = CTkCheckBox(groupBox, text="Filtro de aire", variable=varFiltroAire, command=lambda: habilitar_entry(varFiltroAire, textBoxFiltroAire))
            filtroAireCheck.grid(row=1, column=2, sticky='w', padx=10, pady=5)
            textBoxFiltroAire = CTkEntry(groupBox, width=200)
            textBoxFiltroAire.grid(row=1, column=3, padx=10, pady=5)
            textBoxFiltroAire.configure(state="disabled")

            # Filtro de combustible
            varFiltroComb = IntVar()
            filtroCombCheck = CTkCheckBox(groupBox, text="Filtro de combustible", variable=varFiltroComb, command=lambda: habilitar_entry(varFiltroComb, textBoxFiltroComb))
            filtroCombCheck.grid(row=2, column=2, sticky='w', padx=10, pady=5)
            textBoxFiltroComb = CTkEntry(groupBox, width=200)
            textBoxFiltroComb.grid(row=2, column=3, padx=10, pady=5)
            textBoxFiltroComb.configure(state="disabled")

            # Filtro de habitáculo
            varFiltroHab = IntVar()
            filtroHabCheck = CTkCheckBox(groupBox, text="Filtro de habitáculo", variable=varFiltroHab, command=lambda: habilitar_entry(varFiltroHab, textBoxFiltroHab))
            filtroHabCheck.grid(row=3, column=2, sticky='w', padx=10, pady=5)
            textBoxFiltroHab = CTkEntry(groupBox, width=200)
            textBoxFiltroHab.grid(row=3, column=3, padx=10, pady=5)
            textBoxFiltroHab.configure(state="disabled")

            frameBotones = CTkFrame(root,corner_radius=10)
            frameBotones.pack(pady=5)

            # Botones
            CTkButton(frameBotones, text="Guardar", fg_color='#8AC859', command=self.guardarRegistros).grid(row=0, column=0, pady=10, padx=5)
            CTkButton(frameBotones, text="Modificar", fg_color='#BBCD5F', command=self.modificarRegistros).grid(row=0, column=1, pady=10, padx=5)
            CTkButton(frameBotones, text="Eliminar", fg_color='#E05349', command=self.eliminarRegistros).grid(row=0, column=2, pady=10, padx=5)
            CTkButton(frameBotones, text="Limpiar", command=self.limpiarCampos).grid(row=0, column=3, pady=10, padx=5)

            # Tabla
            groupBoxTabla = CTkFrame(root, corner_radius=10)
            groupBoxTabla.pack(pady=5)

            # Crear un Frame contenedor para el Treeview y el scrollbar
            treeFrame = CTkFrame(groupBoxTabla)
            treeFrame.pack(pady=5)

            # Crear el scrollbar
            treeScrollbar = ttk.Scrollbar(treeFrame, orient="vertical")
            treeScrollbar.pack(side="right", fill="y")

            # Configurar el Treeview
            columnas = ("Patente", "KMs", "Vehículo", "Servicio", "Detalles", "Fecha", "Observaciones")
            tree = ttk.Treeview(treeFrame, style='Custom.Treeview', columns=columnas, show='headings', height=10, yscrollcommand=treeScrollbar.set)
            tree.pack(side="left", fill="both", expand=True)

            # Configurar el scrollbar para que controle el Treeview
            treeScrollbar.config(command=tree.yview)

            # Configurar encabezados y columnas dinámicamente
            tamanos_columnas = [90, 85, 150, 150, 220, 85, 250]
            for i, col in enumerate(columnas):
                tree.column(f"# {i+1}", anchor=CENTER, width=tamanos_columnas[i])
                tree.heading(f"# {i+1}", text=col)

            # Llenar el Treeview
            self.actualizarTreeView()
            tree.bind("<<TreeviewSelect>>", self.seleccionarRegistros)
            
            #Frame para buscar
            groupBoxBuscar = CTkFrame(root, corner_radius=10)
            groupBoxBuscar.pack(pady=5)

            CTkLabel(groupBoxBuscar, text="Patente:", font=("Arial", 13)).grid(row=0, column=0, sticky="w", padx=10, pady=5)
            textBoxBuscarPatente = CTkEntry(groupBoxBuscar, width=300)
            textBoxBuscarPatente.grid(row=0, column=1, pady=5, padx=5)
            CTkButton(groupBoxBuscar, text='Buscar', command=self.buscarPatente).grid(row=0, column=2, pady=5, padx=5)
            CTkButton(groupBoxBuscar,text='Hoy', command=self.buscarFecha).grid(row=0,column=3, pady=5, padx=5)
            CTkButton(groupBoxBuscar, text='Todos', command=self.actualizarTreeView).grid(row=0, column=4, pady=5, padx=5)

        except ValueError as error:
            print("Error al actualizar los datos{}".format(error))

    def guardarRegistros(self):
        global encontrada
        try:
            # Obtener valores del formulario
            fecha = date.today()
            observaciones = textBoxObservaciones.get().capitalize()

            # Verificar si la patente está en los datos
            datos = CClientes.mostrarClientes()
            patente_ingresada = textBoxPatente.get().strip().upper()  # Eliminar espacios extra
            encontrada = False

            # Validación de la patente
            if len(patente_ingresada) < 6 or len(patente_ingresada) > 8:
                messagebox.showinfo("Error de datos", "La patente debe tener entre 6 y 8 caracteres.")
                return

            for cliente in datos:
                if cliente[3] == patente_ingresada:
                    encontrada = True
                    patente_verificada = patente_ingresada
                    break
            else:
                messagebox.showwarning("Advertencia", "La patente no se encuentra registrada. Por favor verifique el cliente.")
                return  # Salir si la patente no está registrada

            # Validación de los KMs
            km_text = textBoxKM.get().strip()  # Eliminar espacios extra
            if not km_text:
                messagebox.showinfo("Error de datos", "Debe ingresar los KMs.")
                return
            if not km_text.isdigit():
                messagebox.showinfo("Error de datos", "Los KMs deben contener solo números.")
                return

            # Convertir a entero después de validar
            km_ingresados = int(km_text)

            # Verificar que los KMs no sean menores a los ya registrados
            data = CBuscador.buscarPorPatente(patente_verificada)
            for cliente in data:
                kms_registrados = cliente[3]  # Suponiendo que cliente[3] almacena los KMs registrados
                if kms_registrados > km_ingresados:
                    messagebox.showwarning("Advertencia", "Los KMs ingresados no pueden ser menores a los KMs registrados para esta patente.")
                    return  # Salir si los KMs son menores

            # Si todo es válido, asignar a km_actual
            km_actual = km_ingresados  # Esto solo se ejecuta si pasa todas las validaciones

            # Crear una lista de servicios seleccionados
            servicios = []
            if varCambioAceite.get():
                servicios.append((1, textBoxCambioAceite.get().title()))
            if varFiltroAceite.get():
                servicios.append((2, textBoxFiltroAceite.get().title()))
            if varFiltroAire.get():
                servicios.append((3, textBoxFiltroAire.get().title()))
            if varFiltroComb.get():
                servicios.append((4, textBoxFiltroComb.get().title()))
            if varFiltroHab.get():
                servicios.append((5, textBoxFiltroHab.get().title()))

            print(f"Servicios seleccionados: {servicios}")

            # Validar si hay servicios seleccionados
            if not servicios:
                messagebox.showwarning("Advertencia", "No se seleccionó ningún servicio.")
                return

            # Ingresar servicios al sistema
            CServicios.ingresarServicios(
                fecha=fecha,
                km_actual=km_actual,  # Aquí km_actual está correctamente asignado
                patente=patente_verificada,
                observaciones=observaciones,
                servicios=servicios
            )
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")

            # Limpiar campos y actualizar TreeView
            self.limpiarCampos()
            self.actualizarTreeView()

        except ValueError as error:
            messagebox.showerror("Error", f"Ocurrió un error al guardar los datos: {error}")
            print(f"Error al ingresar los datos: {error}")


    def seleccionarRegistros(self, e):
        global id_general,id_servicio
        textBoxPatente.delete(0, END)     
        
        try:
            itemSeleccionado = tree.focus()
            tags = tree.item(itemSeleccionado, "tags")
            print(f"Tags:{tags}")  # Para depurar

            if len(tags) >= 3:
                id_general = tags[0]
                id_servicio = tags[2]
                print(f'id general: {id_general}, id serv: {id_servicio}')
            else:
                print("Error: tags no contienen suficientes elementos.")
                return  # Salir de la función si no se pueden acceder a los tags necesarios
            
            #  Deshabilitar todos los checkboxes
            textBoxPatente.configure(state='disabled')
            cambioAceiteCheck.configure(state="disabled")
            filtroAceiteCheck.configure(state="disabled")
            filtroAireCheck.configure(state="disabled")
            filtroCombCheck.configure(state="disabled")
            filtroHabCheck.configure(state="disabled")
            
            textBoxPatente.delete(0, END)
            textBoxKM.delete(0, END)
            textBoxCambioAceite.delete(0, END)
            textBoxFiltroAceite.delete(0, END)
            textBoxFiltroAire.delete(0, END)
            textBoxFiltroComb.delete(0, END)
            textBoxFiltroHab.delete(0, END)
            textBoxObservaciones.delete(0, END)
            # Desmarcar los Checkbuttons
            varCambioAceite.set(0)
            varFiltroAceite.set(0)
            varFiltroAire.set(0)
            varFiltroComb.set(0)
            varFiltroHab.set(0)
            
            if itemSeleccionado: 
                # Obtener los valores de las columnas del elemento seleccionado
                values = tree.item(itemSeleccionado)['values']
                
                textBoxPatente.delete(0, END)
                textBoxPatente.insert(0,values[0])
                textBoxKM.delete(0, END)
                textBoxKM.insert(0,values[1])
                
                # Verificar cada servicio y habilitar solo los correspondientes
                if "Cambio de aceite" in values[3]:
                    varCambioAceite.set(1)
                    habilitar_entry(varCambioAceite, textBoxCambioAceite)
                    textBoxCambioAceite.insert(0, values[4])
                
                if "Filtro de aceite" in values[3]:
                    varFiltroAceite.set(1)
                    habilitar_entry(varFiltroAceite, textBoxFiltroAceite)
                    textBoxFiltroAceite.insert(0, values[4])
                
                if "Filtro de aire" in values[3]:
                    varFiltroAire.set(1)
                    habilitar_entry(varFiltroAire, textBoxFiltroAire)
                    textBoxFiltroAire.insert(0, values[4])
                
                if "Filtro de combustible" in values[3]:
                    varFiltroComb.set(1)
                    habilitar_entry(varFiltroComb, textBoxFiltroComb)
                    textBoxFiltroComb.insert(0, values[4])
                
                if "Filtro de habitaculo" in values[3]:
                    varFiltroHab.set(1)
                    habilitar_entry(varFiltroHab, textBoxFiltroHab)
                    textBoxFiltroHab.insert(0, values[4])

                textBoxObservaciones.configure(state="normal")
                textBoxObservaciones.insert(0, values[6])
            else:
                print("No se seleccionó ningún elemento.")
        except ValueError as error:
            print(f"Error al seleccionar registros:{error}")

    def modificarRegistros(self):
        global encontrada
        
        try:
            patente_ingresada = textBoxPatente.get().strip().upper()  

            # Validación de los KMs
            km_text = textBoxKM.get().strip()  # Eliminar espacios extra
            if not km_text:
                messagebox.showinfo("Error de datos", "Debe ingresar los KMs.")
                return
            if not km_text.isdigit():
                messagebox.showinfo("Error de datos", "Los KMs deben contener solo números.")
                return

            # Convertir a entero después de validar
            km_ingresados = int(km_text)

            # Verificar que los KMs no sean menores a los ya registrados
            data = CBuscador.buscarPorPatente(patente_ingresada)
            for cliente in data:
                kms_registrados = cliente[3]  # Suponiendo que cliente[3] almacena los KMs registrados
                if kms_registrados > km_ingresados:
                    messagebox.showwarning("Advertencia", "Los KMs ingresados no pueden ser menores a los KMs registrados para esta patente.")
                    return  # Salir si los KMs son menores

            # Si todo es válido, asignar a km_actual
            km_actual = km_ingresados  # Esto solo se ejecuta si pasa todas las validaciones

            observaciones = textBoxObservaciones.get().capitalize()

            if varCambioAceite.get():
                habilitar_entry(varCambioAceite, textBoxCambioAceite)
                detalles= textBoxCambioAceite.get().title()
            if varFiltroAceite.get():
                habilitar_entry(varFiltroAceite, textBoxFiltroAceite)
                detalles= textBoxFiltroAceite.get().title()
            if varFiltroAire.get():
                habilitar_entry(varFiltroAire, textBoxFiltroAire)
                detalles= textBoxFiltroAire.get().title()
            if varFiltroComb.get():
                habilitar_entry(varFiltroComb, textBoxFiltroComb)
                detalles= textBoxFiltroComb.get().title()
            if varFiltroHab.get():
                habilitar_entry(varFiltroHab, textBoxFiltroHab)
                detalles= textBoxFiltroHab.get().title()

            CServicios.modificarServicios(km_actual,observaciones,id_general,detalles,id_servicio)
            messagebox.showinfo("Información:", "Los datos fueron actualizados.")

            self.actualizarTreeView()
            self.limpiarCampos()


        except ValueError as error:
            print("Error al actualizar los datos{}".format(error))

    @classmethod
    def actualizarTreeView(self):
        global tree

        try:
            tree.delete(*tree.get_children())

            for row in CServicios.mostrarServiciosRealizados():
                tags = row[0],row[8],row[9]
                tree.insert("", "end", values=row[1:-2], tags=tags)
            
        except ValueError as error:
            print("Error al actualizar tabla {}".format(error))

    def eliminarRegistros(self):
         
        if id_servicio:
            try:
                respuesta = messagebox.askquestion(
                "ELIMINAR",
                "¿Está seguro que desea eliminar este servicio?",
                icon="warning")

                if respuesta == "yes":
                    CServicios.eliminarServicios(id_servicio)
                    messagebox.showinfo("Información:", "Los datos fueron eliminados.")
                    self.actualizarTreeView()
                    self.limpiarCampos()

            except ValueError as error:
                print("Error al actualizar los datos{}".format(error))
        else:
            print("No hay servicio seleccionado.")
            return

    def limpiarCampos(self):
        global id_servicio
        # Limpiar los campos de detalles de los servicios
        textBoxPatente.delete(0, END)
        textBoxKM.delete(0, END)
        textBoxCambioAceite.delete(0, END)
        textBoxFiltroAceite.delete(0, END)
        textBoxFiltroAire.delete(0, END)
        textBoxFiltroComb.delete(0, END)
        textBoxFiltroHab.delete(0, END)
        textBoxObservaciones.delete(0, END)
        textBoxBuscarPatente.delete(0, END)
        # Desmarcar los Checkbuttons
        varCambioAceite.set(0)
        varFiltroAceite.set(0)
        varFiltroAire.set(0)
        varFiltroComb.set(0)
        varFiltroHab.set(0)

        tree.selection_remove(tree.selection())
        tree.focus("")

        # Deshabilitar los Entry    
        textBoxCambioAceite.configure(state='disabled')
        textBoxFiltroAceite.configure(state='disabled')
        textBoxFiltroAire.configure(state='disabled')
        textBoxFiltroComb.configure(state='disabled')
        textBoxFiltroHab.configure(state='disabled')

        #Habilitar checks
        textBoxPatente.configure(state='normal')
        cambioAceiteCheck.configure(state="normal")
        filtroAceiteCheck.configure(state="normal")
        filtroAireCheck.configure(state="normal")
        filtroCombCheck.configure(state="normal")
        filtroHabCheck.configure(state="normal")

        id_servicio=None

    def buscarPatente(self):
        try:
            tree.delete(*tree.get_children())

            # Obtener y limpiar la patente
            patente = textBoxBuscarPatente.get().strip().upper()

            # Verificar si está vacía
            if not patente:
                messagebox.showinfo("Información", "Ingrese una patente")
                return  # Detener la ejecución si no se ingresó una patente

            # Buscar clientes
            datos = CServicios.buscarPatente(patente)
            print(f'DATOS servicios: {datos}')

            if datos:
                for row in datos:
                    tags = (row[0], row[8], row[9])  # Asegurar que sea una tupla
                    tree.insert("", "end", values=row[1:-2], tags=tags)
            else: 
                messagebox.showinfo("Información", "No hay servicios registrados para esa patente.")

            self.limpiarCampos()
        
        except Exception as error:
            print(f"Error al buscar la patente: {error}")


    def buscarFecha(self):
        try:
            tree.delete(*tree.get_children())

            # Buscar clientes
            datos = CServicios.buscarFecha()
            print(f'DATOS servicios: {datos}')

            if datos:
                for row in datos:
                    tags = row[0],row[8],row[9]
                    tree.insert("", "end", values=row[1:-2], tags=tags)

            else: 
                messagebox.showinfo("Información", "No se realizaron servicios el día de hoy.")
            self.limpiarCampos()
    
        except ValueError as error:
            print("Error al eliminar los datos: {}".format(error))

    
