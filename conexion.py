import sqlite3
import os
import sys

class CConexion:

    @staticmethod
    def ConexionBaseDeDatos():
         # Detecta si es un ejecutable o un script Python
        if getattr(sys, 'frozen', False):  # Si el script es un ejecutable
            # Si es un ejecutable, busca la base de datos en el directorio temporal
            db_path = os.path.join(sys._MEIPASS, 'data', 'lubricentrodb.sqlite')
        else:  # Si es un script Python
            db_path = os.path.join('data', 'lubricentrodb.sqlite')

        # Verifica si el archivo existe
        if not os.path.exists(db_path):
            print(f"El archivo de la base de datos no se encuentra en la ruta {db_path}.")
            return None

        try:
            conexion = sqlite3.connect(db_path)  # Conexión directa al archivo de la base de datos
            print("Conexión correcta.")
            return conexion
        except sqlite3.Error as error:
            print(f"Error al conectarte a la Base de Datos: {error}")
            return None

CConexion.ConexionBaseDeDatos()
