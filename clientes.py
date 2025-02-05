from conexion import * 

class CClientes:

    @staticmethod
    def mostrarClientes():
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute("select c.id_cliente, c.nombre_apellido, c.tel_cliente, v.patente, v.modelo_vehiculo from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente order by c.id_cliente desc")  
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
    def ingresarClientes(nombre_apellido, tel_cliente, patente, modelo_vehiculo):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql_cliente = "insert into clientes (nombre_apellido, tel_cliente) values (?, ?)"
            valores_cliente = (nombre_apellido, tel_cliente)
            cursor.execute(sql_cliente, valores_cliente)

            id_cliente = cursor.lastrowid
            
            sql_vehiculo = "insert into vehiculos (patente, modelo_vehiculo, id_cliente) values (?, ?, ?)"
            
            valores_vehiculo = (patente, modelo_vehiculo, id_cliente)
            cursor.execute(sql_vehiculo, valores_vehiculo)

            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
        
        except sqlite3.Error as error:
            print("Error de ingreso de datos {}".format(error))
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()
    
    @staticmethod
    def modificarClientes(id_cliente, nombre_apellido, tel_cliente, patente, modelo_vehiculo):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql_cliente = "update clientes set nombre_apellido = ?, tel_cliente = ? where id_cliente= ?"
            valores_cliente = (nombre_apellido, tel_cliente,id_cliente)
            cursor.execute(sql_cliente, valores_cliente)
            sql_vehiculo = "update vehiculos set patente = ?, modelo_vehiculo = ? where id_cliente = ?"
            valores_vehiculo = (patente, modelo_vehiculo, id_cliente)
            cursor.execute(sql_vehiculo, valores_vehiculo)
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
    def eliminarClientes(id_seleccionado):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql_vehiculos = "delete from vehiculos where id_cliente=?"
            valores = (id_seleccionado,)
            cursor.execute(sql_vehiculos, valores)
            sql_clientes = "delete from clientes where id_cliente=?"
            cursor.execute(sql_clientes, valores)
            cone.commit()
            print(cursor.rowcount, "Registro Eliminado.")
        
        except sqlite3.Error as error:
            print("No fue posible eliminar el registro{}".format(error))
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def verificarPatente(patente):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = ' select count(*) from vehiculos where patente= ?'
            valores = (patente,)
            cursor.execute(sql, valores)
            resultado = cursor.fetchone()  # Obtiene el resultado de la consulta
            
            # Retorna True si la patente ya existe, de lo contrario False
            return resultado[0] > 0
        except sqlite3.Error as error:
            print(f"No fue posible obtener la patente{error}")
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def mostrarClienteID(id):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = 'select c.id_cliente, c.nombre_apellido, c.tel_cliente, v.patente, v.modelo_vehiculo from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente where c.id_cliente = ?'
            valores = (id,)
            cursor.execute(sql, valores)
            resultado = cursor.fetchone()  # Obtiene el resultado de la consulta
        
            return resultado
        except sqlite3.Error as error:
            print(f"No fue posible obtener la patente{error}")
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def buscarCliente(nombre):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = 'select c.id_cliente, c.nombre_apellido, c.tel_cliente, v.patente, v.modelo_vehiculo from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente where c.nombre_apellido like ? order by c.id_cliente desc'
            valores = (f'%{nombre}%',)
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
