from conexion import *

class CServicios:

    @staticmethod
    def mostrarServiciosRealizados():
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute("select sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha, sg.observaciones, sr.id_servicio, sr.id_servicio_realizado  from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente inner join servicio_general sg on sg.patente = v.patente inner join servicios_realizados sr on sg.id_general = sr.id_general inner join servicios s on s.id_servicio = sr.id_servicio order by sr.id_servicio_realizado desc")  
            
            miResultado = cursor.fetchall()
            
            return miResultado
        
        except sqlite3.Error as error:
            print(f"Error al mostrar datos {error}")
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()
    
    @staticmethod    
    def ingresarServicios(fecha, km_actual, patente, observaciones, servicios):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()

            sql_general = """
                INSERT INTO servicio_general (fecha, km_actual, patente, observaciones)
                VALUES (?, ?, ?, ?);
            """
            valores_generales = (fecha, km_actual, patente, observaciones)
            cursor.execute(sql_general, valores_generales)

            # Obtener el id_general generado
            id_general = cursor.lastrowid

            # Insertar en servicios_realizados (múltiples servicios)
            sql_servicios_realizados = """
                INSERT INTO servicios_realizados (id_general, id_servicio, detalles)
                VALUES (?, ?, ?);
            """
            for id_servicio, detalles in servicios:
                valores_servicios_realizados = (id_general, id_servicio, detalles)
                cursor.execute(sql_servicios_realizados, valores_servicios_realizados)

            # Confirmar la transacción
            cone.commit()
            print(f"{cursor.rowcount} registros ingresados en servicios_realizados.")
            
        except sqlite3.Error as error:
            print(f"Error de ingreso de datos: {error}")
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def modificarServicios(km_actual, observaciones,id_general, detalles, id_servicio_realizado):
            try:
                cone = CConexion.ConexionBaseDeDatos();
                cursor = cone.cursor()
                sql_servicio_general = "update servicio_general set km_actual = ?, observaciones = ? where id_general=?;"
                valores_servicio_general = (km_actual, observaciones, id_general)
                cursor.execute(sql_servicio_general, valores_servicio_general)

                sql_servicio_realizado = "update servicios_realizados set detalles= ? where id_servicio_realizado=?"
                valores_servicio_realizado = (detalles, id_servicio_realizado)
                cursor.execute(sql_servicio_realizado, valores_servicio_realizado)
                cone.commit()
                print(cursor.rowcount, "Registro actualizado.")
    
            except sqlite3.Error as error:
                print(f"Error al actualizar datos {error}")
            finally:
                if cursor:
                    cursor.close()
                if cone:
                    cone.close()

    @staticmethod
    def eliminarServicios(id_seleccionado):
            try:
                cone = CConexion.ConexionBaseDeDatos();
                cursor = cone.cursor()
                sql_servicio = "delete from servicios_realizados where id_servicio_realizado=?"
                valores = (id_seleccionado,)
                cursor.execute(sql_servicio, valores)
                cone.commit()
                print(cursor.rowcount, "Registro Eliminado.")
            except sqlite3.Error as error:
                print(f"No fue posible eliminar el registro{error}")
            finally:
                if cursor:
                    cursor.close()
                if cone:
                    cone.close()

    @staticmethod
    def buscarPatente(patente):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = 'select sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha, sg.observaciones, sr.id_servicio, sr.id_servicio_realizado  from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente  inner join servicio_general sg on sg.patente = v.patente inner join servicios_realizados sr on sg.id_general = sr.id_general inner join servicios s on s.id_servicio = sr.id_servicio where v.patente=? order by sr.id_servicio_realizado desc'
            valores = (patente,)
            cursor.execute(sql, valores)
            resultado = cursor.fetchall() 
            
            return resultado
        except sqlite3.Error as error:
            print(f"No fue posible obtener la patente{error}")
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def buscarFecha():
        cone = None
        cursor = None
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute("""
                SELECT sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, 
                    s.nombre_servicio, sr.detalles, sg.fecha, sg.observaciones, 
                    sr.id_servicio, sr.id_servicio_realizado
                FROM clientes c
                INNER JOIN vehiculos v ON c.id_cliente = v.id_cliente
                INNER JOIN servicio_general sg ON sg.patente = v.patente
                INNER JOIN servicios_realizados sr ON sg.id_general = sr.id_general
                INNER JOIN servicios s ON s.id_servicio = sr.id_servicio
                WHERE DATE(sg.fecha) = DATE('now')
                ORDER BY sr.id_servicio_realizado DESC
            """)
            resultado = cursor.fetchall() 
            return resultado
        except sqlite3.Error as error:
            print(f"No fue posible obtener la fecha: {error}")
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

