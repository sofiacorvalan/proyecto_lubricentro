import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from customtkinter import *
from servicios import *
from datetime import date
from clientes import *

class Form2:

    def __init__(self, root):

        global ancho_entry, ancho_columnas
        ancho_entry = 25
        ancho_columnas = 140
        
        global textBoxPatente, textBoxKM, textBoxCambioAceite, textBoxFiltroAceite, textBoxFiltroAire
        global textBoxFiltroComb, textBoxFiltroHab, textBoxObservaciones
        global varCambioAceite, varFiltroAceite, varFiltroAire, varFiltroComb, varFiltroHab,tree, habilitar_entry

        
        def habilitar_entry(var, entry):
            """Habilita o deshabilita el Entry según el estado del Checkbutton"""
            if var.get():
                entry.config(state="normal")
            else:
                entry.delete(0, END)
                entry.config(state="disabled")

        try:
            groupBox = LabelFrame(root, text="Ingresa los datos:", padx=5, pady=5)
            groupBox.grid(row=0, column=0, padx=10, pady=10)

            # Patente
            Label(groupBox, text="Patente:", width=ancho_entry, font=("arial", 12)).grid(row=0, column=0)
            textBoxPatente = Entry(groupBox, width=ancho_entry)
            textBoxPatente.grid(row=0, column=1)

            # Kilómetros
            Label(groupBox, text="Kilómetros:", width=ancho_entry, font=("arial", 12)).grid(row=1, column=0)
            textBoxKM = Entry(groupBox, width=ancho_entry)
            textBoxKM.grid(row=1, column=1)

            # Cambio aceite
            varCambioAceite = IntVar()
            cambioAceiteCheck = Checkbutton(groupBox, text="Cambio aceite", variable=varCambioAceite, command=lambda: habilitar_entry(varCambioAceite, textBoxCambioAceite))
            cambioAceiteCheck.grid(row=2, column=0, sticky=W)
            textBoxCambioAceite = Entry(groupBox, width=ancho_entry, state="disabled")
            textBoxCambioAceite.grid(row=2, column=1)

            # Filtro de aceite
            varFiltroAceite = IntVar()
            filtroAceiteCheck = Checkbutton(groupBox, text="Filtro de aceite", variable=varFiltroAceite, command=lambda: habilitar_entry(varFiltroAceite, textBoxFiltroAceite))
            filtroAceiteCheck.grid(row=3, column=0, sticky=W)
            textBoxFiltroAceite = Entry(groupBox, width=ancho_entry, state="disabled")
            textBoxFiltroAceite.grid(row=3, column=1)

            # Filtro de aire
            varFiltroAire = IntVar()
            filtroAireCheck = Checkbutton(groupBox, text="Filtro de aire", variable=varFiltroAire, command=lambda: habilitar_entry(varFiltroAire, textBoxFiltroAire))
            filtroAireCheck.grid(row=4, column=0, sticky=W)
            textBoxFiltroAire = Entry(groupBox, width=ancho_entry, state="disabled")
            textBoxFiltroAire.grid(row=4, column=1)

            # Filtro de combustible
            varFiltroComb = IntVar()
            filtroCombCheck = Checkbutton(groupBox, text="Filtro de combustible", variable=varFiltroComb, command=lambda: habilitar_entry(varFiltroComb, textBoxFiltroComb))
            filtroCombCheck.grid(row=5, column=0, sticky=W)
            textBoxFiltroComb = Entry(groupBox, width=ancho_entry, state="disabled")
            textBoxFiltroComb.grid(row=5, column=1)

            # Filtro de habitáculo
            varFiltroHab = IntVar()
            filtroHabCheck = Checkbutton(groupBox, text="Filtro de habitáculo", variable=varFiltroHab, command=lambda: habilitar_entry(varFiltroHab, textBoxFiltroHab))
            filtroHabCheck.grid(row=6, column=0, sticky=W)
            textBoxFiltroHab = Entry(groupBox, width=ancho_entry, state="disabled")
            textBoxFiltroHab.grid(row=6, column=1)

            # Observaciones
            Label(groupBox, text="Observaciones:", width=ancho_entry, font=("arial", 12)).grid(row=7, column=0)
            textBoxObservaciones = Entry(groupBox, width=ancho_entry)
            textBoxObservaciones.grid(row=7, column=1)

            # Botones
            Button(groupBox, text="Guardar", width=10, command=guardarRegistros).grid(row=8, column=0)
            Button(groupBox, text="Modificar", width=10, command=modificarRegistros).grid(row=8, column=1)
            Button(groupBox, text="Eliminar", width=10, command=eliminarRegistros).grid(row=8, column=2)
            Button(groupBox, text="Limpiar",width=10, command=limpiarCampos).grid(row=9, column=2)

            # Tabla
            groupBoxTabla = LabelFrame(root, text="Servicios realizados:", padx=5, pady=5)
            groupBoxTabla.grid(row=0, column=1, padx=10, pady=10)

            tree = ttk.Treeview(groupBoxTabla, columns=("Patente","KMs", "Vehículo", "Servicio", "Detalles", "Fecha", "Observaciones"), show='headings', height=15)
            tree.column("# 1", anchor=CENTER, width=100)
            tree.heading("# 1", text="Patente")
            tree.column("# 2", anchor=CENTER, width=100)
            tree.heading("# 2", text="KMs")
            tree.column("# 3", anchor=CENTER, width=100)
            tree.heading("# 3", text="Vehículo")
            tree.column("# 4", anchor=CENTER, width=ancho_columnas)
            tree.heading("# 4", text="Servicio")
            tree.column("# 5", anchor=CENTER, width=ancho_columnas)
            tree.heading("# 5", text="Detalles")
            tree.column("# 6", anchor=CENTER, width=100)
            tree.heading("# 6", text="Fecha")
            tree.column("# 7", anchor=CENTER, width=100)
            tree.heading("# 7", text="Observaciones")
            
            
            for row in CServicios.mostrarServiciosRealizados():
                tags = (row[0], row[8], row[9])
                tree.insert("", "end", values=row[1:-2], tags=tags)
               
            tree.bind("<<TreeviewSelect>>", seleccionarRegistros)
            tree.pack()

        except ValueError as error:
            print("Error al actualizar los datos{}".format(error))

def guardarRegistros():
    global encontrada
    try:
        # Obtener valores del formulario
        fecha = date.today()
        km_actual = textBoxKM.get()
        observaciones = textBoxObservaciones.get()
        
        # Verificar si la patente está en los datos
        datos = CClientes.mostrarClientes()
        patente_ingresada = textBoxPatente.get()
        encontrada = False

        for cliente in datos:
            if cliente[3] == patente_ingresada: 
                encontrada = True
                patente = patente_ingresada
                break
        else:
            messagebox.showwarning("Advertencia","La patente no se encuentra registrada. Por favor verifique el cliente.")

        # Crear una lista de servicios seleccionados
        servicios = []
        if varCambioAceite.get():
            servicios.append((1, textBoxCambioAceite.get()))
        if varFiltroAceite.get():
            servicios.append((2, textBoxFiltroAceite.get()))
        if varFiltroAire.get():
            servicios.append((3, textBoxFiltroAire.get()))
        if varFiltroComb.get():
            servicios.append((4, textBoxFiltroComb.get()))
        if varFiltroHab.get():
            servicios.append((5, textBoxFiltroHab.get()))

        print(f"Servicios seleccionados: {servicios}")
        
        # Llamar al método ingresarServicios solo si hay servicios seleccionados
        if servicios:
            CServicios.ingresarServicios(
                fecha=fecha,
                km_actual=km_actual,
                patente=patente,
                observaciones=observaciones,
                servicios=servicios
            )
            messagebox.showinfo("Éxito", "Datos guardados correctamente.")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún servicio.")
        
        limpiarCampos()    
        actualizarTreeView()

    except ValueError as error:
        print(f"Error al ingresar los datos: {error}")


def seleccionarRegistros(e):
    global id_general,id_servicio

    try:
        itemSeleccionado = tree.focus()
        tags = tree.item(itemSeleccionado, "tags")
        print(tags)  # Para depurar

        id_general = tags[0]
        id_servicio = tags[2]
                
        print('id general:', id_general,'id serv:', id_servicio)
        
        limpiarCampos()
        
        textBoxCambioAceite.configure(state="disabled")
        textBoxFiltroAceite.configure(state="disabled")
        textBoxFiltroAire.configure(state="disabled")
        textBoxFiltroComb.configure(state="disabled")
        textBoxFiltroHab.configure(state="disabled")
        textBoxObservaciones.configure(state="disabled")
        
        if itemSeleccionado: 
            # Obtener los valores de las columnas del elemento seleccionado
            values = tree.item(itemSeleccionado)['values']
            print(values)  # Imprime los valores

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

def modificarRegistros():
    global textBoxPatente, textBoxKM, textBoxCambioAceite, textBoxFiltroAceite, textBoxFiltroAire, textBoxFiltroComb, textBoxFiltroHab, textBoxObservaciones,detalles
    
    try:
        if textBoxPatente is None or textBoxKM is None or textBoxCambioAceite is None or textBoxFiltroAceite is None or textBoxFiltroAire is None or textBoxFiltroComb is None or textBoxFiltroHab is None or textBoxObservaciones is None:
            print("Los widget no estan inicializados")
            return
        
        kms = textBoxKM.get()
        observaciones = textBoxObservaciones.get()

        if varCambioAceite.get():
            habilitar_entry(varCambioAceite, textBoxCambioAceite)
            detalles= textBoxCambioAceite.get()
        if varFiltroAceite.get():
            habilitar_entry(varFiltroAceite, textBoxFiltroAceite)
            detalles= textBoxFiltroAceite.get()
        if varFiltroAire.get():
            habilitar_entry(varFiltroAire, textBoxFiltroAire)
            detalles= textBoxFiltroAire.get()
        if varFiltroComb.get():
            habilitar_entry(varFiltroComb, textBoxFiltroComb)
            detalles= textBoxFiltroComb.get()
        if varFiltroHab.get():
            habilitar_entry(varFiltroHab, textBoxFiltroHab)
            detalles= textBoxFiltroHab.get()

        CServicios.modificarServicios(kms,observaciones,id_general,detalles,id_servicio)
        messagebox.showinfo("Información:", "Los datos fueron actualizados.")

        actualizarTreeView()
        limpiarCampos()

    except ValueError as error:
        print("Error al actualizar los datos{}".format(error))

def actualizarTreeView():
    global tree

    try:
        tree.delete(*tree.get_children())

        for row in CServicios.mostrarServiciosRealizados():
            tags = row[0],row[8],row[9]
            tree.insert("", "end", values=row[1:-2], tags=tags)
        
    except ValueError as error:
        print("Error al actualizar tabla {}".format(error))

def eliminarRegistros():
    global id_servicio
    try:
        CServicios.eliminarServicios(id_servicio)
        messagebox.showinfo("Información:", "Los datos fueron eliminados.")

        actualizarTreeView()
        limpiarCampos()
    except ValueError as error:
        print("Error al actualizar los datos{}".format(error))


def limpiarCampos():
    # Limpiar los campos de detalles de los servicios
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
