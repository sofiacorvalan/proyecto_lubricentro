from conexion import *

class CBuscador:
    
    def buscarPorPatente(patente):
        try:
            cone=CConexion.ConexionBaseDeDatos()
            cursor=cone.cursor()
            sql_consulta=('select c.nombre_apellido, sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha,sg.observaciones, sr.id_servicio, sr.id_servicio_realizado, sg.km_actual+10000 as "Proximo servicio" from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente inner join servicio_general sg on sg.patente = v.patente inner join servicios_realizados sr on sg.id_general = sr.id_general inner join servicios s on s.id_servicio = sr.id_servicio where v.patente = %s order by sg.fecha desc;')
            valores = (patente,)
            cursor.execute(sql_consulta,valores)

            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar datos {}",format(error))

    def buscarPorVehiculo(vehiculo):
        try:
            cone=CConexion.ConexionBaseDeDatos()
            cursor=cone.cursor()
            sql_consulta=('select c.nombre_apellido, sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha,sg.observaciones, sr.id_servicio, sr.id_servicio_realizado, sg.km_actual+10000 as "Proximo servicio" from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente inner join servicio_general sg on sg.patente = v.patente inner join servicios_realizados sr on sg.id_general = sr.id_general inner join servicios s on s.id_servicio = sr.id_servicio where v.modelo_vehiculo like %s order by sr.id_servicio_realizado desc;')
            valores = (f'%{vehiculo}%',)
            cursor.execute(sql_consulta,valores)

            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar datos {}",format(error))

    def buscarPorCliente(cliente):
        try:
            cone=CConexion.ConexionBaseDeDatos()
            cursor=cone.cursor()
            sql_consulta=('select c.nombre_apellido, sg.id_general, v.patente, sg.km_actual, v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha,sg.observaciones, sr.id_servicio, sr.id_servicio_realizado, sg.km_actual+10000 as "Proximo servicio" from clientes c inner join vehiculos v on c.id_cliente = v.id_cliente inner join servicio_general sg on sg.patente = v.patente inner join servicios_realizados sr on sg.id_general = sr.id_general inner join servicios s on s.id_servicio = sr.id_servicio where c.nombre_apellido like %s order by sr.id_servicio_realizado desc;')
            valores = (f'%{cliente}%',)
            cursor.execute(sql_consulta,valores)

            miResultado = cursor.fetchall()
            cone.commit()
            cone.close()
            return miResultado
        
        except mysql.connector.Error as error:
            print("Error al mostrar datos {}",format(error))