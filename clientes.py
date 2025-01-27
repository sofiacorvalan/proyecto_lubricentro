from conexion import * 

class CClientes:
    def mostrarClientes():
        try:
            cone = CConexion.ConexionBaseDeDatos();
            cursor = cone.cursor()
            cursor.execute("select c.id_cliente, c.nombre_apellido, c.tel_cliente, v.patente, v.modelo_vehiculo from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente order by c.id_cliente desc;")  
            miResultado = cursor.fetchall()
            cursor.close()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar datos {}",format(error))
    

    def ingresarClientes(nombre_apellido, tel_cliente, patente, modelo_vehiculo):
        try:
            cone = CConexion.ConexionBaseDeDatos();
            cursor = cone.cursor()
            sql_cliente = "insert into clientes (nombre_apellido, tel_cliente) values (%s, %s)"
            valores_cliente = (nombre_apellido, tel_cliente)
            cursor.execute(sql_cliente, valores_cliente)

            id_cliente = cursor.lastrowid
            
            sql_vehiculo = "insert into vehiculos (patente, modelo_vehiculo, id_cliente) values (%s, %s, %s)"
            
            valores_vehiculo = (patente, modelo_vehiculo, id_cliente)
            cursor.execute(sql_vehiculo, valores_vehiculo)

            cone.commit()
            print(cursor.rowcount, "Registro ingresado")
            cursor.close()
            cone.close()

        except mysql.connector.Error as error:
            print("Error de ingreso de datos {}".format(error))

    def modificarClientes(id_cliente, nombre_apellido, tel_cliente, patente, modelo_vehiculo):
        try:
            cone = CConexion.ConexionBaseDeDatos();
            cursor = cone.cursor()
            sql_cliente = "update clientes set nombre_apellido = %s, tel_cliente = %s where id_cliente= %s;"
            valores_cliente = (nombre_apellido, tel_cliente,id_cliente)
            cursor.execute(sql_cliente, valores_cliente)
            sql_vehiculo = "update vehiculos set patente = %s, modelo_vehiculo = %s where id_cliente = %s;"
            valores_vehiculo = (patente, modelo_vehiculo, id_cliente)
            cursor.execute(sql_vehiculo, valores_vehiculo)
            cone.commit()
            print(cursor.rowcount, "Registro actualizado.")
            cursor.close()
            cone.close()
 
        except mysql.connector.Error as error:
            print("Error al actualizar datos {}".format(error))
    
    def eliminarClientes(id_seleccionado):
        try:
            cone = CConexion.ConexionBaseDeDatos();
            cursor = cone.cursor()
            sql_vehiculos = "delete from vehiculos where id_cliente=%s;"
            valores = (id_seleccionado,)
            cursor.execute(sql_vehiculos, valores)
            sql_clientes = "delete from clientes where id_cliente=%s;"
            cursor.execute(sql_clientes, valores)
            cone.commit()
            print(cursor.rowcount, "Registro Eliminado.")
            cursor.close()
            cone.close()
        except mysql.connector.Error as error:
            print("No fue posible eliminar el registro{}".format(error))
    
    def verificarPatente(patente):
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = ' select count(*) from vehiculos where patente= %s;'
            valores = (patente,)
            cursor.execute(sql, valores)
            resultado = cursor.fetchone()  # Obtiene el resultado de la consulta
            cursor.close()
            cone.close()
            # Retorna True si la patente ya existe, de lo contrario False
            return resultado[0] > 0
        except mysql.connector.Error as error:
            print("No fue posible obtener la patente{}".format(error))