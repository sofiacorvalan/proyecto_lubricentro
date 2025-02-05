from conexion import *

class CBuscador:

    @staticmethod
    def ejecutarConsulta(sql_consulta, valores=()):
        cone = None
        cursor = None
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            cursor.execute(sql_consulta, valores)
            return cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Error al ejecutar consulta: {error}")
            return None
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def buscarPorPatente(patente):
        sql = '''
            SELECT c.nombre_apellido, sg.id_general, v.patente, sg.km_actual, 
                   v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha, 
                   sg.observaciones, sr.id_servicio, sr.id_servicio_realizado, 
                   sg.km_actual+10000 AS "Proximo servicio"
            FROM clientes c
            INNER JOIN vehiculos v ON c.id_cliente = v.id_cliente
            INNER JOIN servicio_general sg ON sg.patente = v.patente
            INNER JOIN servicios_realizados sr ON sg.id_general = sr.id_general
            INNER JOIN servicios s ON s.id_servicio = sr.id_servicio
            WHERE v.patente = ?
            ORDER BY sg.fecha DESC
        '''
        return CBuscador.ejecutarConsulta(sql, (patente,))

    @staticmethod
    def buscarPorVehiculo(vehiculo):
        sql = '''
            SELECT c.nombre_apellido, sg.id_general, v.patente, sg.km_actual,
                   v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha,
                   sg.observaciones, sr.id_servicio, sr.id_servicio_realizado,
                   sg.km_actual+10000 AS "Proximo servicio"
            FROM clientes c
            INNER JOIN vehiculos v ON c.id_cliente = v.id_cliente
            INNER JOIN servicio_general sg ON sg.patente = v.patente
            INNER JOIN servicios_realizados sr ON sg.id_general = sr.id_general
            INNER JOIN servicios s ON s.id_servicio = sr.id_servicio
            WHERE v.modelo_vehiculo LIKE ?
            ORDER BY sr.id_servicio_realizado DESC
        '''
        return CBuscador.ejecutarConsulta(sql, (f'%{vehiculo}%',))

    @staticmethod
    def buscarPorCliente(cliente):
        sql = '''
            SELECT c.nombre_apellido, sg.id_general, v.patente, sg.km_actual,
                   v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha,
                   sg.observaciones, sr.id_servicio, sr.id_servicio_realizado,
                   sg.km_actual+10000 AS "Proximo servicio"
            FROM clientes c
            INNER JOIN vehiculos v ON c.id_cliente = v.id_cliente
            INNER JOIN servicio_general sg ON sg.patente = v.patente
            INNER JOIN servicios_realizados sr ON sg.id_general = sr.id_general
            INNER JOIN servicios s ON s.id_servicio = sr.id_servicio
            WHERE c.nombre_apellido LIKE ?
            ORDER BY sr.id_servicio_realizado DESC
        '''
        return CBuscador.ejecutarConsulta(sql, (f'%{cliente}%',))

    @staticmethod
    def verificarServicio(patente):
        cone = None
        cursor = None
        try:
            cone = CConexion.ConexionBaseDeDatos()
            cursor = cone.cursor()
            sql = 'SELECT COUNT(*) FROM servicio_general WHERE patente = ?'
            cursor.execute(sql, (patente,))
            resultado = cursor.fetchone()
            return resultado[0] > 0 if resultado else False
        except sqlite3.Error as error:
            print(f"Error al verificar servicios: {error}")
            return False
        finally:
            if cursor:
                cursor.close()
            if cone:
                cone.close()

    @staticmethod
    def mostrarServiciosDiarios():
        sql = '''
            SELECT c.nombre_apellido, sg.id_general, v.patente, sg.km_actual,
                   v.modelo_vehiculo, s.nombre_servicio, sr.detalles, sg.fecha,
                   sg.observaciones, sr.id_servicio, sr.id_servicio_realizado,
                   sg.km_actual+10000 AS "Proximo servicio"
            FROM clientes c
            INNER JOIN vehiculos v ON c.id_cliente = v.id_cliente
            INNER JOIN servicio_general sg ON sg.patente = v.patente
            INNER JOIN servicios_realizados sr ON sg.id_general = sr.id_general
            INNER JOIN servicios s ON s.id_servicio = sr.id_servicio
            WHERE DATE(sg.fecha) = DATE('now')
            ORDER BY sr.id_servicio_realizado DESC
        '''
        return CBuscador.ejecutarConsulta(sql)
