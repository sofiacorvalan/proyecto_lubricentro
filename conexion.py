import sqlite3
import os
import sys
import shutil

class CConexion:

    @staticmethod
    def ConexionBaseDeDatos():
        # Carpeta donde se almacenará la base de datos en la PC del usuario
        base_path = os.path.expanduser("~")  # Carpeta del usuario
        db_folder = os.path.join(base_path, 'lubricentro_app')  # Carpeta persistente
        os.makedirs(db_folder, exist_ok=True)  # Crear carpeta si no existe

        # Ruta final de la base de datos
        db_path = os.path.join(db_folder, 'lubricentrodb.sqlite')

        # Solo copiar la base de datos inicial si NO existe en la carpeta persistente
        if getattr(sys, 'frozen', False) and not os.path.exists(db_path):
            original_db = os.path.join(sys._MEIPASS, 'data', 'lubricentrodb.sqlite')
            if os.path.exists(original_db):
                shutil.copy2(original_db, db_path)
                print("Base de datos copiada a la ubicación persistente.")

        # Conectar a la base de datos
        try:
            conexion = sqlite3.connect(db_path)
            conexion.execute("PRAGMA foreign_keys = ON;")  # Habilitar claves foráneas
            print(f"✅ Conectado a la base de datos en: {db_path}")
            return conexion
        except sqlite3.Error as error:
            print(f"❌ Error al conectar a la Base de Datos: {error}")
            return None

CConexion.ConexionBaseDeDatos()
