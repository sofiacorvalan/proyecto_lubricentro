import sqlite3

class CConexion:

    @staticmethod
    def ConexionBaseDeDatos():
        try:
            conexion = sqlite3.connect('data/lubricentrodb.sqlite')  # Conexión directa al archivo de la base de datos
            print("Conexión correcta.")
            return conexion
        except sqlite3.Error as error:
            print(f"Error al conectarte a la Base de Datos: {error}")
            return None

CConexion.ConexionBaseDeDatos()
