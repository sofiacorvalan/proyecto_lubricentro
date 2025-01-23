from conexion import *

class CServicios:

    @staticmethod
    def mostrarServiciosRealizados():
        try:
            cone = CConexion.ConexionBaseDeDatos();
            cursor = cone.cursor()
            cursor.execute("select sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha, sg.observaciones, sr.id_servicio, sr.id_servicio_realizado  from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente inner join servicio_general sg on sg.patente = v.patente inner join servicios_realizados sr on sg.id_general = sr.id_general inner join servicios s on s.id_servicio = sr.id_servicio order by sr.id_servicio_realizado desc;")  
            
            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar datos {}",format(error))

    def ingresarServicios(fecha, km_actual, patente, observaciones, servicios):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()

            # Insertar en servicio_general (una sola vez)
            sql_general = """
                INSERT INTO servicio_general (fecha, km_actual, patente, observaciones)
                VALUES (%s, %s, %s, %s);
            """
            valores_generales = (fecha, km_actual, patente, observaciones)
            cursor.execute(sql_general, valores_generales)

            # Obtener el id_general generado
            id_general = cursor.lastrowid

            # Insertar en servicios_realizados (múltiples servicios)
            sql_servicios_realizados = """
                INSERT INTO servicios_realizados (id_general, id_servicio, detalles)
                VALUES (%s, %s, %s);
            """
            for id_servicio, detalles in servicios:
                valores_servicios_realizados = (id_general, id_servicio, detalles)
                cursor.execute(sql_servicios_realizados, valores_servicios_realizados)

            # Confirmar la transacción
            cone.commit()
            print(f"{cursor.rowcount} registros ingresados en servicios_realizados.")
            cone.close()

        except mysql.connector.Error as error:
            print(f"Error de ingreso de datos: {error}")

    def modificarServicios(km_actual, observaciones,id_general, detalles, id_servicio_realizado):
            try:
                cone = CConexion.ConexionBaseDeDatos();
                cursor = cone.cursor()
                sql_servicio_general = "update servicio_general set km_actual = %s, observaciones = %s where id_general=%s;"
                valores_servicio_general = (km_actual, observaciones, id_general)
                cursor.execute(sql_servicio_general, valores_servicio_general)

                sql_servicio_realizado = "update servicios_realizados set detalles= %s where id_servicio_realizado=%s;"
                valores_servicio_realizado = (detalles, id_servicio_realizado)
                cursor.execute(sql_servicio_realizado, valores_servicio_realizado)
                cone.commit()
                print(cursor.rowcount, "Registro actualizado.")
                cone.close()
    
            except mysql.connector.Error as error:
                print("Error al actualizar datos {}".format(error))

    def eliminarServicios(id_seleccionado):
            try:
                cone = CConexion.ConexionBaseDeDatos();
                cursor = cone.cursor()
                sql_servicio = "delete from servicios_realizados where id_servicio_realizado=%s;"
                valores = (id_seleccionado,)
                cursor.execute(sql_servicio, valores)
                cone.commit()
                print(cursor.rowcount, "Registro Eliminado.")
                cone.close()
            except mysql.connector.Error as error:
                print("No fue posible eliminar el registro{}".format(error))